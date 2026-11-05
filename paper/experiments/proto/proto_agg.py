"""Aggregate E8 P1/P2 run CSVs into means with Student-t 95% CIs over runs.

  python proto_agg.py [results_dir]
in : proto_capacity.csv (per run), proto_latency_runs.csv (per run)
out: proto_capacity_agg.csv, proto_latency.csv (spec schema + extras, per run),
     proto_latency_agg.csv
"""
import csv
import os
import sys
from collections import defaultdict

import numpy as np
from scipy import stats


def tci(x):
    x = np.asarray(x, float)
    m = x.mean()
    if len(x) < 2:
        return m, float("nan"), float("nan")
    h = stats.t.ppf(0.975, len(x) - 1) * x.std(ddof=1) / np.sqrt(len(x))
    return m, m - h, m + h


def read(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def main(res):
    cap = read(os.path.join(res, "proto_capacity.csv"))
    by = defaultdict(list)
    for r in cap:
        by[r["scheme"]].append(r)
    b1 = {r["run"]: float(r["req_per_s"]) for r in by["b1"]}
    out = []
    for s, rows in by.items():
        rps = [float(r["req_per_s"]) for r in rows]
        m, lo, hi = tci(rps)
        cpu = tci([float(r["cpu_util_edge"]) for r in rows])
        p50 = tci([float(r["p50_ms"]) for r in rows])
        p99 = tci([float(r["p99_ms"]) for r in rows])
        # paired ratio vs B1 (same run index)
        ratio = [float(r["req_per_s"]) / b1[r["run"]] for r in rows if r["run"] in b1]
        rm, rlo, rhi = tci(ratio)
        # per-request edge CPU time (us) = cpu_util / req_per_s
        us = tci([float(r["cpu_util_edge"]) / float(r["req_per_s"]) * 1e6 for r in rows])
        out.append(dict(scheme=s, n_runs=len(rows), req_per_s_mean=m, req_per_s_ci_lo=lo, req_per_s_ci_hi=hi,
                        cpu_util_edge_mean=cpu[0], edge_cpu_us_per_req_mean=us[0], edge_cpu_us_per_req_ci_lo=us[1],
                        edge_cpu_us_per_req_ci_hi=us[2], p50_ms_mean=p50[0], p99_ms_mean=p99[0], p99_ms_ci_lo=p99[1],
                        p99_ms_ci_hi=p99[2], ratio_vs_b1_mean=rm, ratio_vs_b1_ci_lo=rlo, ratio_vs_b1_ci_hi=rhi,
                        token_bytes=rows[0]["token_bytes"], net=rows[0]["net"], impl=rows[0]["impl"]))
    write(os.path.join(res, "proto_capacity_agg.csv"), out)

    p = os.path.join(res, "proto_latency_runs.csv")
    if not os.path.exists(p):
        return
    lat = read(p)
    hm = {(r["load_frac"], r["run"]): float(r["p50_ms"]) for r in lat if r["scheme"] == "b1"}
    hm99 = {(r["load_frac"], r["run"]): float(r["p99_ms"]) for r in lat if r["scheme"] == "b1"}
    rows_out = []
    for r in lat:
        k = (r["load_frac"], r["run"])
        rows_out.append(dict(scheme=r["scheme"], load_frac=r["load_frac"], run=r["run"], p50_ms=r["p50_ms"], p99_ms=r["p99_ms"],
                             added_p50_ms_vs_hmac=float(r["p50_ms"]) - hm[k] if k in hm else "",
                             added_p99_ms_vs_hmac=float(r["p99_ms"]) - hm99[k] if k in hm99 else "",
                             rate_target=r["rate_target"], rate_achieved=r["rate_achieved"], n_req=r["n_req"],
                             errors=r["errors"], net=r["net"], impl=r["impl"]))
    write(os.path.join(res, "proto_latency.csv"), rows_out)
    g = defaultdict(list)
    for r in rows_out:
        g[(r["scheme"], r["load_frac"])].append(r)
    agg = []
    for (s, f), rows in sorted(g.items()):
        d = dict(scheme=s, load_frac=f, n_runs=len(rows))
        for col in ("p50_ms", "p99_ms", "added_p50_ms_vs_hmac", "added_p99_ms_vs_hmac", "rate_achieved"):
            vals = [float(r[col]) for r in rows if r[col] != ""]
            if vals:
                d[col + "_mean"], d[col + "_ci_lo"], d[col + "_ci_hi"] = tci(vals)
        d["rate_target_mean"] = np.mean([float(r["rate_target"]) for r in rows])
        d["errors_total"] = sum(int(r["errors"]) for r in rows)
        agg.append(d)
    write(os.path.join(res, "proto_latency_agg.csv"), agg)


def write(path, rows):
    keys = []
    for r in rows:
        for k in r:
            if k not in keys:
                keys.append(k)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.4f}" if isinstance(v, float) else v) for k, v in r.items()})
    print("wrote", path)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "..", "results"))
