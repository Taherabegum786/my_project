"""R2: trace-driven operating region on Meta's public CacheLib CDN traces (cdn/202303: clusters eag, nha, prn).

python -m sim.trace --npz <dir with <cluster>/chunk*.npz> --out ../results [--V 3600] [--clusters reag,rnha,rprn]
Preprocessed input: per-cluster chunk*.npz written by scratchpad trace_tools/prep.py from the raw CSV (see RESULTS_R2_TRACE.md
for the exact download commands and checksums); the raw trace is never committed.

Mapping of the trace onto the EMBER model (assumptions, all stated in RESULTS_R2_TRACE.md):
  * edge     = the trace's CDN cluster (one site; keys are anonymised per cluster, so no cross-site reuse is observable);
  * token    = one signed-URL token per (object key, V-bucket): issued at the first request of the key in each bucket of
               length V after the key's first request in the window, and carried by every request of that key in the bucket;
               K = requests per token (real, the trace is key-sampled so a sampled key keeps all its requests);
  * tenant   = cdn_content_type_id (23 classes); trust-domain pool = vip_type; global pool = all tokens of the cluster;
  * replicate = one 24-h window of one cluster (days from the trace start);
  * rates    = (i) "sampled": the trace as is (exact replay through the simulator's epoch code; a CDN 1/SamplingRate times
               smaller), (ii) "scaled": per-(group, minute) rates multiplied by 1/SamplingRate with Poisson arrivals inside each
               minute (tree sizes then 1+Poisson(lambda*Delta) token-weighted); (ii) at scale 1 is checked against (i).
Edge verifier models: shared (the cluster verifies once per token/tree), keyshard:H (token -> one of H hosts by key hash),
reqspread:H (every request to a uniformly random host).
"""
import argparse
import glob
import math
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sim import fleet_mc as F  # noqa: E402

DAY_MS = 86_400_000
CLAIMS_B = 118                      # measured canonical claims (token_sizes_r1.csv, 60-char path)
M2_TOKEN_B = 148                    # measured M2 URL token (token_sizes_r1.csv)
STAPLE_M2_B, STAPLE_EMBER_B = 3242, 3298   # HTTP/1.1 staple header lines (token_sizes_r1.csv)
SEED = 20261106


def ember_token_b(d):
    return CLAIMS_B + 3 + np.ceil(4 * (30 + 16 * np.asarray(d)) / 3)


def wq(K, q):
    """Request-weighted quantile of the per-token request count."""
    k = np.sort(K)
    c = np.cumsum(k) / k.sum()
    return float(k[np.searchsorted(c, q)])


def load(npzdir):
    fs = sorted(glob.glob(os.path.join(npzdir, "chunk*.npz")))
    parts = {k: [] for k in ("t_ms", "key64", "ctype", "vip", "samp", "resp")}
    for f in fs:
        z = np.load(f)
        for k in parts:
            parts[k].append(z[k])
    d = {k: np.concatenate(v) for k, v in parts.items()}
    o = np.argsort(d["t_ms"], kind="stable")
    return {k: v[o] for k, v in d.items()}


def tokens_of(day, V_ms):
    """Per-token arrays (sorted by issue time) for one window."""
    o = np.lexsort((day["t_ms"], day["key64"]))
    k, t = day["key64"][o], day["t_ms"][o]
    newkey = np.r_[True, k[1:] != k[:-1]]
    kidx = np.cumsum(newkey) - 1
    tfirst = t[newkey][kidx]
    b = (t - tfirst) // V_ms
    start = newkey | np.r_[True, b[1:] != b[:-1]]
    tid = np.cumsum(start) - 1
    K = np.bincount(tid)
    iss = t[start]
    ct = day["ctype"][o][start]
    vp = day["vip"][o][start]
    oo = np.argsort(iss, kind="stable")
    return dict(iss_s=iss[oo] / 1000.0, K=K[oo].astype(np.int64), ctype=ct[oo], vip=vp[oo])


def groups_of(tok):
    g = {"tenant": tok["ctype"].astype(np.int64), "service": tok["vip"].astype(np.int64),
         "global": np.zeros(tok["K"].size, np.int64)}
    return g


# ------------------------------------------------------------------ tree formation
def exact_trees(tok, gid, delta, costs, policy="fixed"):
    """Exact replay of the (sampled) token stream through the simulator's epoch code, per group.
    Returns per-token tree size n_tok, tree id tree_of, number of trees."""
    nt = tok["K"].size
    n_tok = np.zeros(nt, np.int64)
    tree_of = np.zeros(nt, np.int64)
    base = 0
    for g in np.unique(gid):
        idx = np.nonzero(gid == g)[0]
        arr = tok["iss_s"][idx]
        if policy == "wc":
            te, cl, N = F.epochs_wc(arr, costs.t_tok, costs.t_sign)
        else:
            te, cl, N = F.epochs_fixed(arr, delta, 1 << 40)
        n_tok[idx] = N[te]
        tree_of[idx] = te + base
        base += N.size
    return n_tok, tree_of, base


def exact_contacts(tok, n_tok, tree_of, H, model):
    """Signature verifications (verifier contacts) for EMBER (per tree) and M2 (per token) on the exact stream."""
    K = tok["K"].astype(float)
    ntree = int(tree_of.max()) + 1
    q = 1.0 - 1.0 / H if H > 1 else 0.0
    if model == "shared":
        return float(ntree), float(K.size)
    if model == "keyshard":
        sizes = np.bincount(tree_of, minlength=ntree).astype(float)
        return float(np.sum(H * -np.expm1(sizes * np.log(q)))), float(K.size)
    Kt = np.bincount(tree_of, weights=K, minlength=ntree)
    return float(np.sum(H * -np.expm1(Kt * np.log(q)))), float(np.sum(H * -np.expm1(K * np.log(q))))


def poisson_model(tok, gid, delta, scale, H, model, rng):
    """Scaled-rate model: in (group, minute) m tokens arrive as Poisson with rate lam_m = c_m*scale/60 (c_m sampled tokens).
    Token-weighted tree size = 1 + Poisson(mu_m), mu_m = lam_m*delta (sampled per token, independent of its real K).
    Closed forms per minute (q = 1 - 1/H, phi = E[q^K] from the group's real K in that minute):
      trees/s           = (1 - e^-mu)/delta
      shared contacts/s = trees/s (EMBER), lam (M2)
      keyshard contacts = H(1 - e^{-mu/H})/delta (EMBER), lam (M2)
      reqspread         = H(1 - e^{-mu(1-phi)})/delta (EMBER), lam*H*(1-phi) (M2).
    All per-second quantities are returned for the scaled cluster (multiply sampled counts by scale)."""
    minute = (tok["iss_s"] // 60).astype(np.int64)
    K = tok["K"].astype(float)
    n_tok = np.zeros(K.size, np.int64)
    trees = c_em = c_m2 = 0.0
    q = 1.0 - 1.0 / H if H > 1 else 0.0
    for g in np.unique(gid):
        idx = np.nonzero(gid == g)[0]
        mins, inv, cnt = np.unique(minute[idx], return_inverse=True, return_counts=True)
        lam = cnt * scale / 60.0
        mu = lam * delta
        n_tok[idx] = 1 + rng.poisson(mu[inv])
        tr = -np.expm1(-mu) / delta * 60.0                       # trees per minute
        trees += tr.sum()
        if model == "shared":
            c_em += tr.sum(); c_m2 += float(np.sum(lam * 60.0))
        elif model == "keyshard":
            c_em += float(np.sum(H * -np.expm1(-mu / H) / delta * 60.0)); c_m2 += float(np.sum(lam * 60.0))
        else:
            phi = np.bincount(inv, weights=np.exp(K[idx] * np.log(q)), minlength=mins.size) / cnt
            c_em += float(np.sum(H * -np.expm1(-mu * (1 - phi)) / delta * 60.0))
            c_m2 += float(np.sum(lam * 60.0 * H * (1 - phi)))
    return n_tok, trees, c_em, c_m2


def costs_per_req(tok, n_tok, c_em, c_m2, R, costs):
    """c_em/c_m2: verifications over the window, R: requests over the window (same scale)."""
    K = tok["K"].astype(float)
    d = np.ceil(np.log2(np.maximum(n_tok, 1))).astype(np.int64)
    path = costs.path_cost(np.minimum(d, 24))
    return dict(cpu_m2_us=1e6 * (c_m2 * costs.t_verify / R + costs.t_hash),
                cpu_em_us=1e6 * (c_em * costs.t_verify / R + float(np.sum(K * path) / K.sum())),
                contacts_per_req_m2=c_m2 / R, contacts_per_req_em=c_em / R,
                bytes_per_req_m2=M2_TOKEN_B + c_m2 * STAPLE_M2_B / R,
                bytes_per_req_em=float(np.sum(K * ember_token_b(d)) / K.sum()) + c_em * STAPLE_EMBER_B / R)


def tree_stats(tok, n_tok):
    d = np.ceil(np.log2(np.maximum(n_tok, 1))).astype(np.int64)
    Kw = tok["K"].astype(float)
    return dict(frac_tok_N1=float(np.mean(n_tok == 1)), median_N=float(np.median(n_tok)),
                d_p50=int(np.median(d)), d_p99=int(np.percentile(d, 99)),
                tok_bytes_p50=float(np.median(ember_token_b(d))),
                tok_bytes_reqweighted=float(np.sum(Kw * ember_token_b(d)) / Kw.sum()))


VERIFIERS = (("shared", 1), ("keyshard", 1000), ("reqspread", 1000))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--npz", required=True)
    ap.add_argument("--out", default="../results")
    ap.add_argument("--clusters", default="reag,rnha,rprn")
    ap.add_argument("--V", type=float, default=3600.0)
    ap.add_argument("--min_hours", type=float, default=20.0)
    ap.add_argument("--tag", default="", help="suffix for output files (parallel per-cluster runs; merge with --merge)")
    a = ap.parse_args()
    costs = F.Costs(a.out)
    pv = pd.read_csv(os.path.join(a.out, "native_pathverify_agg.csv"))
    costs.t_hash = float(pv[(pv.impl == "evp") & (pv.op == "th_200B") & (pv.n == 16)].ns_median.iloc[0]) * 1e-9
    rows, trows, krows = [], [], []
    for cl in a.clusters.split(","):
        D = load(os.path.join(a.npz, cl))
        p = float(np.median(D["samp"]))
        scale = 1.0 / p
        t0 = int(D["t_ms"][0])
        nday = int((D["t_ms"][-1] - t0) // DAY_MS) + 1
        for day in range(nday):
            lo, hi = t0 + day * DAY_MS, t0 + (day + 1) * DAY_MS
            s, e = np.searchsorted(D["t_ms"], [lo, hi])
            span_h = (D["t_ms"][e - 1] - D["t_ms"][s]) / 3.6e6 if e > s else 0
            if span_h < a.min_hours:
                continue
            W = {k: v[s:e] for k, v in D.items()}
            tok = tokens_of(W, int(a.V * 1000))
            secs = span_h * 3600.0
            G = groups_of(tok)
            rep = dict(cluster=cl, day=day, V_s=a.V, sampling_rate=p, hours=round(span_h, 2), requests_sampled=int(e - s),
                       tokens_sampled=int(tok["K"].size), req_per_s_sampled=(e - s) / secs,
                       tok_per_s_sampled=tok["K"].size / secs, tok_per_s_scaled=tok["K"].size / secs * scale,
                       K_mean=float(tok["K"].mean()), K_p50=float(np.median(tok["K"])),
                       K_reqweighted_p50=wq(tok["K"], 0.5), K_max=int(tok["K"].max()),
                       frac_req_K_lt_97=float(tok["K"][tok["K"] < 97].sum() / tok["K"].sum()),
                       frac_req_K_lt_155=float(tok["K"][tok["K"] < 155].sum() / tok["K"].sum()),
                       frac_tok_K1=float(np.mean(tok["K"] == 1)))
            krows.append(rep)
            # per-group scaled rates (tokens/s): distribution over (group, minute)
            minute = (tok["iss_s"] // 60).astype(np.int64)
            for gname, gid in G.items():
                key = gid * 10**8 + minute
                _, c = np.unique(key, return_counts=True)
                lam = c * scale / 60.0
                ug, gc = np.unique(gid, return_counts=True)
                trows.append(dict(cluster=cl, day=day, V_s=a.V, pooling=gname, groups=int(ug.size),
                                  group_rate_scaled_p50=float(np.median(gc / secs * scale)),
                                  group_rate_scaled_max=float(np.max(gc / secs * scale)),
                                  minute_rate_scaled_p10=float(np.percentile(lam, 10)),
                                  minute_rate_scaled_p50=float(np.percentile(lam, 50)),
                                  minute_rate_scaled_p90=float(np.percentile(lam, 90)),
                                  tok_share_groups_ge_1000ps=float(np.sum(gc[gc / secs * scale >= 1000]) / gc.sum()),
                                  tok_share_minutes_ge_1000ps=float(np.sum(c[lam >= 1000]) / c.sum())))
            rng = np.random.default_rng([SEED, day, sum(map(ord, cl))])
            R_s = float(tok["K"].sum())
            for gname, gid in G.items():
                for delta in (0.01, 1.0):
                    n_ex, tree_of, ntree = exact_trees(tok, gid, delta, costs)
                    for mode, sc in (("sampled", 1.0), ("poisson_check", 1.0), ("scaled", scale)):
                        lam_tot = tok["K"].size / secs * sc
                        for vname, H in VERIFIERS:
                            if mode == "sampled":
                                n_tok = n_ex
                                c_em, c_m2 = exact_contacts(tok, n_ex, tree_of, H, vname)
                                trees = ntree
                            else:
                                n_tok, trees, c_em, c_m2 = poisson_model(tok, gid, delta, sc, H, vname, rng)
                            R = R_s * sc
                            rows.append(dict(rep, pooling=gname, policy="fixed:%g" % delta, rates=mode,
                                             verifier=vname if H == 1 else "%s:%d" % (vname, H), **tree_stats(tok, n_tok),
                                             issuer_sigs_per_s=trees / secs, tokens_per_s=lam_tot,
                                             mean_tokens_per_tree=lam_tot * secs / max(trees, 1e-9),
                                             issuer_cores_ember=trees / secs * costs.t_sign + lam_tot * costs.t_tok,
                                             issuer_cores_m2=lam_tot * costs.t_sign,
                                             issue_wait_mean_ms_ember=1e3 * (delta / 2 + costs.t_sign),
                                             issue_wait_mean_ms_m2=1e3 * costs.t_sign,
                                             **costs_per_req(tok, n_tok, c_em, c_m2, R, costs)))
                n_ex, tree_of, ntree = exact_trees(tok, gid, 0, costs, "wc")
                lam_tot = tok["K"].size / secs
                rows.append(dict(rep, pooling=gname, policy="wc", rates="sampled", verifier="shared", **tree_stats(tok, n_ex),
                                 issuer_sigs_per_s=ntree / secs, tokens_per_s=lam_tot, mean_tokens_per_tree=tok["K"].size / ntree,
                                 issuer_cores_ember=ntree / secs * costs.t_sign + lam_tot * costs.t_tok,
                                 issuer_cores_m2=lam_tot * costs.t_sign))
            print("trace %s day %d: %.1f h, %d req, %d tokens (%.1f tok/s sampled, %.0f scaled), K mean %.2f" % (
                cl, day, span_h, e - s, tok["K"].size, rep["tok_per_s_sampled"], rep["tok_per_s_scaled"], rep["K_mean"]), flush=True)
    sfx = ("" if a.V == 3600 else "_V%d" % int(a.V)) + (("_" + a.tag) if a.tag else "")
    pd.DataFrame(rows).to_csv(os.path.join(a.out, "trace_oprg%s.csv" % sfx), index=False)
    pd.DataFrame(trows).to_csv(os.path.join(a.out, "trace_rates%s.csv" % sfx), index=False)
    pd.DataFrame(krows).to_csv(os.path.join(a.out, "trace_replicates%s.csv" % sfx), index=False)
    print("wrote trace_oprg%s.csv (%d rows)" % (sfx, len(rows)))


if __name__ == "__main__":
    main()
