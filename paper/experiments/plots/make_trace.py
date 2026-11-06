"""R2 trace-driven results: aggregate sim.trace outputs over replicates (cluster-days), write tables/figures/summary.

python -m plots.make_trace --in ../results
Inputs: trace_oprg*.csv, trace_replicates*.csv, trace_rates*.csv (sim.trace), r1_oprg_agg.csv (synthetic comparison),
native_*_agg.csv.  Outputs: trace_agg.csv, tables/tab_r2_trace.tex, figures/fig16_trace_operating_region,
figures/fig17_trace_rates, r2_trace_summary.txt.
"""
import argparse
import glob
import math
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from plots.style import COL, DCOL, INK2, LINES, MARKERS, SERIES, save, setup  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

IN = None
LOG = []
CL = {"reag": "eag", "rnha": "nha", "rprn": "prn"}


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def tci(x):
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    n = len(x)
    if n < 2:
        return (x.mean() if n else np.nan), np.nan, np.nan
    h = stats.t.ppf(0.975, n - 1) * x.std(ddof=1) / np.sqrt(n)
    return x.mean(), x.mean() - h, x.mean() + h


MET = ["frac_tok_N1", "median_N", "d_p50", "tok_bytes_reqweighted", "issuer_sigs_per_s", "tokens_per_s",
       "mean_tokens_per_tree", "issuer_cores_ember", "issuer_cores_m2", "cpu_m2_us", "cpu_em_us", "contacts_per_req_m2",
       "contacts_per_req_em", "bytes_per_req_m2", "bytes_per_req_em", "issue_wait_mean_ms_ember", "issue_wait_mean_ms_m2"]


def agg(d, keys):
    rows = []
    for k, g in d.groupby(keys, sort=False, dropna=False):
        r = dict(zip(keys, k))
        r["replicates"] = len(g)
        for m in MET:
            if m in g:
                mm, lo, hi = tci(pd.to_numeric(g[m], errors="coerce"))
                r[m], r[m + "_lo"], r[m + "_hi"] = mm, lo, hi
        rows.append(r)
    return pd.DataFrame(rows)


def thresholds():
    nat = pd.read_csv(os.path.join(IN, "native_sig_agg.csv")).set_index(["scheme", "op"]).median_us
    ts = nat[("ML-DSA-44", "sign")] * 1e-6
    ia = pd.read_csv(os.path.join(IN, "native_issuer_agg.csv"))
    r = ia[(ia.root_alg == "ML-DSA-44") & (ia.N == 16384) & (ia.n == 16)].iloc[0]
    tt = (r.t_leaf_us + r.t_tree_us + r.t_encode_us) / 16384 * 1e-6
    out = {}
    for delta in (0.01, 1.0):
        lam = np.logspace(-1, 7, 4000)
        mu = lam * delta
        em = ts * (-np.expm1(-mu)) / mu + tt
        ratio = ts / em
        for x in (2, 10, 100):
            i = np.argmax(ratio >= x)
            out[(delta, x)] = lam[i] if ratio[i] >= x else np.nan
    say("\n=== RATE THRESHOLDS (analytic, native run-2: t_sign %.1f us, t_tok %.3f us) ===" % (ts * 1e6, tt * 1e6))
    for (delta, x), v in out.items():
        say("Delta=%g s: EMBER issuer >= %dx cheaper than M2 when pool rate >= %.4g tokens/s" % (delta, x, v))
    say("M2 issuer needs > 1 core above %.0f tokens/s" % (1 / ts))
    return out


def main():
    global IN
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default="../results")
    a = ap.parse_args()
    IN = a.inp
    d = pd.read_csv(os.path.join(IN, "trace_oprg.csv"))
    rep = pd.read_csv(os.path.join(IN, "trace_replicates.csv"))
    rates = pd.read_csv(os.path.join(IN, "trace_rates.csv"))
    say("=== REPLICATES (trace_replicates.csv): cluster-days of >= 20 h ===")
    for c, g in rep.groupby("cluster"):
        m = {k: tci(g[k]) for k in ("req_per_s_sampled", "tok_per_s_sampled", "tok_per_s_scaled", "K_mean", "frac_tok_K1",
                                    "K_reqweighted_p50", "frac_req_K_lt_97")}
        say("%s (%s): %d days, sampling %.4g; req/s sampled %.1f [%.1f, %.1f]; tokens/s sampled %.1f, scaled %.0f [%.0f, %.0f]; "
            "K mean %.2f [%.2f, %.2f]; tokens with K=1 %.3f; request-weighted median K %.0f; requests on tokens with K<97: %.3f" % (
                c, CL[c], len(g), g.sampling_rate.iloc[0], *m["req_per_s_sampled"][:1], m["req_per_s_sampled"][1],
                m["req_per_s_sampled"][2], m["tok_per_s_sampled"][0], *m["tok_per_s_scaled"], *m["K_mean"],
                m["frac_tok_K1"][0], m["K_reqweighted_p50"][0], m["frac_req_K_lt_97"][0]))
    say("\n=== POOL RATES, scaled to the full cluster (trace_rates.csv; mean over days) ===")
    ra = rates.groupby(["cluster", "pooling"]).mean(numeric_only=True).reset_index()
    for r in ra.itertuples():
        say("%s %-7s groups=%2.0f group rate p50 %.0f max %.0f tok/s; minute-rate p10/p50/p90 %.0f/%.0f/%.0f; "
            "token share in groups >= 1000/s: %.3f" % (r.cluster, r.pooling, r.groups, r.group_rate_scaled_p50,
                                                      r.group_rate_scaled_max, r.minute_rate_scaled_p10,
                                                      r.minute_rate_scaled_p50, r.minute_rate_scaled_p90,
                                                      r.tok_share_groups_ge_1000ps))
    keys = ["cluster", "pooling", "policy", "rates", "verifier"]
    A = agg(d, keys)
    d2 = d.copy()
    d2["cluster"] = "all"
    A = pd.concat([A, agg(d2, keys)])
    A.to_csv(os.path.join(IN, "trace_agg.csv"), index=False)
    say("\nwrote trace_agg.csv (%d rows); CIs are Student-t 95%% over cluster-days" % len(A))

    def g(cl, pool, pol, rt, ver="shared"):
        r = A[(A.cluster == cl) & (A.pooling == pool) & (A.policy == pol) & (A.rates == rt) & (A.verifier == ver)]
        return r.iloc[0] if len(r) else None

    say("\n=== TREE SIZES / ISSUER (shared verifier rows; all clusters pooled, mean [95% CI] over cluster-days) ===")
    for rt in ("sampled", "poisson_check", "scaled"):
        for pool in ("tenant", "service", "global"):
            for pol in ("fixed:0.01", "fixed:1", "wc"):
                r = g("all", pool, pol, rt)
                if r is None:
                    continue
                say("%-13s %-7s %-10s N1=%.4f [%.4f,%.4f] medianN=%.0f d50=%.1f tokB(req-w)=%.0f sig/s=%.1f tok/s=%.0f "
                    "N/tree=%.1f issuer EMBER %.4f [%.4f,%.4f] cores vs M2 %.3f [%.3f,%.3f]" % (
                        rt, pool, pol, r.frac_tok_N1, r.frac_tok_N1_lo, r.frac_tok_N1_hi, r.median_N, r.d_p50,
                        r.tok_bytes_reqweighted, r.issuer_sigs_per_s, r.tokens_per_s, r.mean_tokens_per_tree,
                        r.issuer_cores_ember, r.issuer_cores_ember_lo, r.issuer_cores_ember_hi, r.issuer_cores_m2,
                        r.issuer_cores_m2_lo, r.issuer_cores_m2_hi))
    say("\n=== EDGE CPU / BYTES / CONTACTS per request, M2 vs EMBER (all clusters; scaled and sampled) ===")
    for rt in ("scaled", "sampled"):
        for pool in ("tenant", "service", "global"):
            for pol in ("fixed:0.01", "fixed:1"):
                for ver in ("shared", "keyshard:1000", "reqspread:1000"):
                    r = g("all", pool, pol, rt, ver)
                    if r is None:
                        continue
                    say("%-7s %-7s %-10s %-14s CPU us/req M2 %.2f [%.2f,%.2f] EMBER %.2f [%.2f,%.2f]; contacts/req M2 %.4f EMBER %.4f; "
                        "bytes/req M2 %.0f EMBER %.0f" % (rt, pool, pol, ver, r.cpu_m2_us, r.cpu_m2_us_lo, r.cpu_m2_us_hi,
                                                          r.cpu_em_us, r.cpu_em_us_lo, r.cpu_em_us_hi, r.contacts_per_req_m2,
                                                          r.contacts_per_req_em, r.bytes_per_req_m2, r.bytes_per_req_em))
    say("\n=== POISSON-WITHIN-MINUTE CHECK (sampled exact vs poisson_check at the sampled rate; all cluster-days) ===")
    for pool in ("tenant", "service", "global"):
        for pol in ("fixed:0.01", "fixed:1"):
            x, y = g("all", pool, pol, "sampled"), g("all", pool, pol, "poisson_check")
            say("%-7s %-10s N1 exact %.4f model %.4f; sig/s exact %.2f model %.2f (rel %.2f%%); EMBER CPU exact %.3f model %.3f" % (
                pool, pol, x.frac_tok_N1, y.frac_tok_N1, x.issuer_sigs_per_s, y.issuer_sigs_per_s,
                100 * (y.issuer_sigs_per_s / x.issuer_sigs_per_s - 1), x.cpu_em_us, y.cpu_em_us))
    th = thresholds()
    # V sensitivity
    for f in sorted(glob.glob(os.path.join(IN, "trace_oprg_V*.csv"))):
        v = pd.read_csv(f)
        v["cluster"] = "all"
        B = agg(v, keys)
        say("\n=== V sensitivity: %s ===" % os.path.basename(f))
        for pool in ("tenant", "global"):
            for pol in ("fixed:0.01",):
                for rt in ("sampled", "scaled"):
                    r = B[(B.pooling == pool) & (B.policy == pol) & (B.rates == rt) & (B.verifier == "shared")]
                    if len(r):
                        r = r.iloc[0]
                        say("%s %s %s: tok/s %.0f N1 %.4f medianN %.0f issuer EMBER %.4f vs M2 %.3f; CPU M2 %.2f EMBER %.2f us/req" % (
                            rt, pool, pol, r.tokens_per_s, r.frac_tok_N1, r.median_N, r.issuer_cores_ember, r.issuer_cores_m2,
                            r.cpu_m2_us, r.cpu_em_us))
    # synthetic comparison
    syn = os.path.join(IN, "r1_oprg_agg.csv")
    if os.path.exists(syn):
        s = pd.read_csv(syn)
        say("\n=== SYNTHETIC (r1_oprg_agg.csv) for comparison, pull_staple ===")
        for lam in (2000, 20000):
            for pool, pol in (("tenant", "fixed:0.01"), ("global", "fixed:0.01"), ("tenant", "pertoken")):
                r = s[(s.lambda_bar == lam) & (s.pooling == pool) & (s.policy == pol) & (s["mode"] == "pull_staple")]
                if len(r):
                    r = r.iloc[0]
                    say("syn lam=%d %s %s: N1=%.3f issuer %.4f cores; edge %.2f us/req; req/sig-verify %.0f" % (
                        lam, pool, pol, r.frac_tok_N1, r.issuer_cpu_cores, r.edge_cpu_us_per_req_mean, r.req_per_sig_verify))
    # ---- table
    rows = []
    for rt in ("sampled", "scaled"):
        for pool in ("tenant", "service", "global"):
            for pol in ("fixed:0.01", "fixed:1"):
                r = g("all", pool, pol, rt)
                rk = g("all", pool, pol, rt, "reqspread:1000")
                if r is None:
                    continue
                rows.append([rt, {"tenant": "content type", "service": "VIP type", "global": "cluster"}[pool], pol.split(":")[1],
                             "%.0f" % r.tokens_per_s, "%.1f\\%%" % (100 * r.frac_tok_N1), "%.0f" % r.median_N,
                             "%.0f" % r.tok_bytes_reqweighted, "%.4g" % r.issuer_cores_ember, "%.4g" % r.issuer_cores_m2,
                             "%.1f/%.1f" % (r.cpu_em_us, r.cpu_m2_us), "%.1f/%.1f" % (rk.cpu_em_us, rk.cpu_m2_us),
                             "%.0f/%.0f" % (r.bytes_per_req_em, r.bytes_per_req_m2)])
    hdr = ["rates", "tree pool", "$\\Delta$ s", "tokens/s", "tok. $N_e{=}1$", "median $N_e$", "token B (req-w.)",
           "issuer cores EMBER", "issuer cores M2", "edge $\\mu$s/req EMBER/M2 (shared)",
           "edge $\\mu$s/req EMBER/M2 (1000 hosts, spread)", "B/req EMBER/M2"]
    os.makedirs(os.path.join(IN, "tables"), exist_ok=True)
    with open(os.path.join(IN, "tables", "tab_r2_trace.tex"), "w") as f:
        f.write("%% generated by plots/make_trace.py -- do not edit\n\\begin{table*}[t]\n\\centering\\scriptsize\n")
        f.write("\\caption{Trace-driven operating region on Meta's public CDN traces (3 clusters, Mar 2023; mean over cluster-days). "
                "Tokens: one signed-URL token per object per hour; sampled = trace as published; scaled = rates $\\times$ 1/SamplingRate "
                "with Poisson arrivals within each minute.}\\label{tab:r2-trace}\n")
        f.write("\\begin{tabular}{lll" + "r" * 9 + "}\n\\toprule\n" + " & ".join(hdr) + " \\\\\n\\midrule\n")
        for r in rows:
            f.write(" & ".join(r) + " \\\\\n")
        f.write("\\bottomrule\n\\end{tabular}\n\\end{table*}\n")
    say("wrote tables/tab_r2_trace.tex")
    # ---- figures
    setup()
    fig, axs = plt.subplots(1, 3, figsize=(DCOL, 2.3))
    pools = ["tenant", "service", "global"]
    plab = ["content type", "VIP type", "cluster"]
    ax = axs[0]
    w = 0.2
    for k, (rt, pol) in enumerate((("sampled", "fixed:0.01"), ("scaled", "fixed:0.01"), ("sampled", "fixed:1"), ("scaled", "fixed:1"))):
        v = [g("all", p, pol, rt) for p in pools]
        ax.bar(np.arange(3) + (k - 1.5) * w, [100 * x.frac_tok_N1 for x in v], w * 0.9, color=SERIES[k],
               yerr=[[100 * (x.frac_tok_N1 - x.frac_tok_N1_lo) for x in v], [100 * (x.frac_tok_N1_hi - x.frac_tok_N1) for x in v]],
               label="%s, $\\Delta$=%s s" % (rt, pol.split(":")[1]), error_kw=dict(lw=0.6))
    ax.set_xticks(range(3), plab)
    ax.set_ylabel("% of tokens in single-token trees")
    ax.set_title("(a) tree sizes on the trace", fontsize=7)
    ax.legend(fontsize=6)
    ax = axs[1]
    for k, pool in enumerate(pools):
        r = g("all", pool, "fixed:0.01", "scaled")
        ax.bar(k, r.issuer_cores_ember, 0.6, color=SERIES[k], yerr=[[r.issuer_cores_ember - r.issuer_cores_ember_lo],
                                                                     [r.issuer_cores_ember_hi - r.issuer_cores_ember]])
    r = g("all", "global", "fixed:0.01", "scaled")
    ax.bar(3, r.issuer_cores_m2, 0.6, color=SERIES[4], yerr=[[r.issuer_cores_m2 - r.issuer_cores_m2_lo], [r.issuer_cores_m2_hi - r.issuer_cores_m2]])
    ax.set_xticks(range(4), ["EMBER\nper type", "EMBER\nper VIP", "EMBER\ncluster", "M2"])
    ax.set_yscale("log")
    ax.set_ylabel("issuer cores (scaled cluster rate)")
    ax.set_title("(b) issuer, $\\Delta$=10 ms", fontsize=7)
    ax = axs[2]
    vers = ["shared", "keyshard:1000", "reqspread:1000"]
    for k, (pool, lab) in enumerate((("global", "EMBER cluster pool"), ("tenant", "EMBER per type"))):
        v = [g("all", pool, "fixed:0.01", "scaled", x) for x in vers]
        ax.bar(np.arange(3) + (k - 1) * 0.27, [x.cpu_em_us for x in v], 0.25, color=SERIES[k], label=lab)
    v = [g("all", "global", "fixed:0.01", "scaled", x) for x in vers]
    ax.bar(np.arange(3) + 0.27, [x.cpu_m2_us for x in v], 0.25, color=SERIES[4], label="M2")
    ax.set_xticks(range(3), ["shared\nverifier", "1000 hosts\nkey-sharded", "1000 hosts\nrequest-spread"])
    ax.set_ylabel("edge crypto $\\mu$s per request")
    ax.set_title("(c) edge CPU with real K, $\\Delta$=10 ms", fontsize=7)
    ax.legend(fontsize=6)
    fig.tight_layout()
    save(fig, os.path.join(IN, "figures"), "fig16_trace_operating_region")
    fig, ax = plt.subplots(figsize=(COL, 2.2))
    for k, c in enumerate(sorted(rep.cluster.unique())):
        r = rep[rep.cluster == c]
        ax.plot(r.day, r.tok_per_s_scaled, marker=MARKERS[k], ls=LINES[k], color=SERIES[k], label="cluster " + CL[c])
    for v, lab in ((th[(0.01, 10)], "EMBER 10x issuer gain ($\\Delta$=10 ms)"), (2446, "M2 issuer > 1 core")):
        ax.axhline(v, color=INK2, lw=0.7, ls=":")
        ax.text(0, v * 1.15, lab, fontsize=6, color=INK2)
    ax.set_yscale("log")
    ax.set_xlabel("day of trace (24-h window)")
    ax.set_ylabel("token issuance, tokens/s\n(scaled to full cluster)")
    ax.legend(fontsize=6)
    save(fig, os.path.join(IN, "figures"), "fig17_trace_rates")
    with open(os.path.join(IN, "r2_trace_summary.txt"), "w") as f:
        f.write("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
