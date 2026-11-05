"""H8 validation: prototype (E8 P3) vs simulator vs analytic model, same configuration.

  python validate.py [results_dir] [--mc-reps 50]

Inputs (results_dir):
  proto_p3_runs.csv       per-run prototype metrics (loadgen -mode p3)
  proto_rtt.csv           measured keep-alive HTTP RTT samples, path=edge_origin (root fetch RTT)
  proto_go_verify.csv     Go ML-DSA-44 root verify cost (op=verify_root), optional
  sim_proto_mc.csv        OPTIONAL: Experimenter A's fleet_mc run at the identical configuration,
                          columns mode,V,delta_s,lambda,metric,mc_mean  (preferred MC source)
Output:
  proto_validate.csv: mode,V,delta_s,lambda,metric,proto_mean,proto_ci_lo,proto_ci_hi,mc_mean,model_value,
                      rel_err_mc,rel_err_model,mc_impl,pass_mc
  pass_mc = |rel_err_mc| <= 0.15 or mc_mean inside the prototype 95% CI (H8 criterion).

MC sources: if sim_proto_mc.csv exists its values are used (mc_impl=fleet_mc). Otherwise this script runs
its own epoch-level replica of the fleet_mc pull/staple algorithm (spec §3 E5 steps 1-7, with E edges = V
virtual edges and no shield tier, i.e. every edge miss goes straight to the root service) at the same
parameters and the measured RTT distribution (mc_impl=validate-replica).  The replica is independent of the
prototype code (numpy only); it does not read any prototype outcome other than the RTT probe and the
verify microbenchmark.
"""
import argparse
import csv
import os
from collections import defaultdict

import numpy as np
from scipy import stats

SEED = 20261105
SR_BYTES = 4 + 4 + 8 + 4 + 4 + 1 + 16 + 2420  # signed-root wire bytes, n = 16, ML-DSA-44
METRICS = ["miss_per_token", "miss_lat_mean_ms", "wait_all_mean_ms", "wait_all_p99_ms", "root_bytes_per_token"]
# Prototype parameters (run_proto.sh p3)
T_WINDOW = 60.0
ALPHA = 0.8
FIRST_MED_MS, FIRST_SIGMA = 120.0, 0.5


def tci(x):
    x = np.asarray(x, float)
    m = x.mean()
    if len(x) < 2:
        return m, np.nan, np.nan
    h = stats.t.ppf(0.975, len(x) - 1) * x.std(ddof=1) / np.sqrt(len(x))
    return m, m - h, m + h


def zipf_w(V, a):
    w = 1.0 / np.arange(1, V + 1) ** a
    return w / w.sum()


def model(mode, V, delta, lam, fetch_mean_ms, verify_ms):
    """Analytic steady-state model: tokens/epoch ~ Poisson(lam*delta); one edge per session (Zipf);
    misses per epoch = expected number of distinct edges hit."""
    w = zipf_w(V, ALPHA)
    mu = lam * delta
    mpt = np.sum(1 - np.exp(-mu * w)) / mu
    lat = verify_ms if mode == "pull_staple" else fetch_mean_ms + verify_ms
    return {"miss_per_token": mpt, "miss_lat_mean_ms": lat, "wait_all_mean_ms": np.nan, "wait_all_p99_ms": np.nan,
            "root_bytes_per_token": mpt * SR_BYTES}


def replica_mc(mode, V, delta, lam, rtt_ms, verify_ms, reps):
    """Epoch-level Monte Carlo replica of fleet_mc (pull / pull_staple), finite window T_WINDOW."""
    w = zipf_w(V, ALPHA)
    out = defaultdict(list)
    for r in range(reps):
        rng = np.random.default_rng(SEED + 1000 * r + int(lam) + 7 * V + int(delta * 1000))
        n = rng.poisson(lam * T_WINDOW)
        t = np.sort(rng.uniform(0, T_WINDOW, n))
        phase = rng.uniform(0, delta)
        ep = np.floor((t + phase) / delta).astype(np.int64)
        edge = rng.choice(V, size=n, p=w)
        arr = np.exp(np.log(FIRST_MED_MS) + FIRST_SIGMA * rng.standard_normal(n))  # ms after epoch close
        key = ep * 100000 + edge
        order = np.lexsort((arr, key))
        key, arr = key[order], arr[order]
        first = np.ones(n, bool)
        first[1:] = key[1:] != key[:-1]
        nmiss = first.sum()
        if mode == "pull_staple":
            F = np.full(nmiss, verify_ms)
        else:
            F = rng.choice(rtt_ms, size=nmiss) + verify_ms
        grp = np.cumsum(first) - 1
        done = arr[first][grp] + F[grp]
        wait = np.where(first, F[grp], np.maximum(done - arr, 0.0))
        waiting = first | (arr < done)
        out["miss_per_token"].append(nmiss / n)
        out["miss_lat_mean_ms"].append(F.mean())
        out["wait_all_mean_ms"].append(wait[waiting].mean())
        out["wait_all_p99_ms"].append(np.percentile(wait[waiting], 99))
        out["root_bytes_per_token"].append(nmiss * SR_BYTES / n)
    return {k: float(np.mean(v)) for k, v in out.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("res", nargs="?", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "results"))
    ap.add_argument("--mc-reps", type=int, default=50)
    a = ap.parse_args()
    res = a.res
    rows = list(csv.DictReader(open(os.path.join(res, "proto_p3_runs.csv"))))
    rtt = np.array([float(r["rtt_ms"]) for r in csv.DictReader(open(os.path.join(res, "proto_rtt.csv")))
                    if r["path"] == "edge_origin"])
    verify_ms = 0.1
    vp = os.path.join(res, "proto_go_verify.csv")
    if os.path.exists(vp):
        for r in csv.DictReader(open(vp)):
            if r["op"] == "verify_root_mldsa44":
                verify_ms = float(r["median_us"]) / 1000
    ext = {}
    sp = os.path.join(res, "sim_proto_mc.csv")
    if os.path.exists(sp):
        for r in csv.DictReader(open(sp)):
            ext[(r["mode"], int(r["V"]), float(r["delta_s"]), float(r["lambda"]), r["metric"])] = float(r["mc_mean"])
    g = defaultdict(list)
    for r in rows:
        g[(r["mode"], int(r["V"]), float(r["delta_s"]), float(r["lambda"]))].append(r)
    out = []
    for (mode, V, d, lam), rs in sorted(g.items()):
        mdl = model(mode, V, d, lam, rtt.mean(), verify_ms)
        rep = None if ext else replica_mc(mode, V, d, lam, rtt, verify_ms, a.mc_reps)
        for m in METRICS:
            vals = [float(r[m]) for r in rs if r[m] not in ("", "NaN", "nan")]
            if not vals:
                continue
            pm, plo, phi = tci(vals)
            if ext:
                mc, impl = ext.get((mode, V, d, lam, m), np.nan), "fleet_mc"
            else:
                mc, impl = rep[m], "validate-replica"
            mv = mdl[m]
            rel_mc = (mc - pm) / pm if pm else np.nan
            rel_md = (mv - pm) / pm if pm and not np.isnan(mv) else np.nan
            ok = bool((abs(rel_mc) <= 0.15) or (plo <= mc <= phi)) if not np.isnan(mc) else ""
            out.append(dict(mode=mode, V=V, delta_s=d, **{"lambda": lam}, metric=m, n_runs=len(vals), proto_mean=pm,
                            proto_ci_lo=plo, proto_ci_hi=phi, mc_mean=mc, model_value=mv, rel_err_mc=rel_mc,
                            rel_err_model=rel_md, mc_impl=impl, pass_mc=ok))
    path = os.path.join(res, "proto_validate.csv")
    with open(path, "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        wr.writeheader()
        for r in out:
            wr.writerow({k: (f"{v:.5g}" if isinstance(v, (float, np.floating)) else v) for k, v in r.items()})
    print("wrote", path, "| measured edge->origin RTT mean %.3f ms (n=%d), verify %.3f ms" % (rtt.mean(), len(rtt), verify_ms))
    for m in ("miss_per_token", "miss_lat_mean_ms"):
        sel = [r for r in out if r["metric"] == m]
        print("%-18s pass %d/%d  max|rel_err_mc| %.3f  max|rel_err_model| %.3f" % (
            m, sum(1 for r in sel if r["pass_mc"] is True), len(sel), max(abs(r["rel_err_mc"]) for r in sel),
            max(abs(r["rel_err_model"]) for r in sel)))


if __name__ == "__main__":
    main()
