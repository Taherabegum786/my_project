"""Run the fleet_mc numba kernel at the exact E8 P3 prototype configuration (results/proto_p3_config.json) and
write results/sim_proto_mc.csv (mode,V,delta_s,lambda,metric,mc_mean,mc_ci_lo,mc_ci_hi,reps) for
experiments/proto/validate.py (H8).

Mapping: E = V virtual edges, Zipf(0.8) shares not permuted, one edge per session (p_move = 0), no shield tier
(shield->root RTT = 0, so every edge miss costs the edge->origin RTT), root-fetch RTT = lognormal fitted to the
measured keep-alive RTT samples (results/proto_rtt.csv, path=edge_origin), plus the measured Go ML-DSA-44 root
verify time added to every waiting request; 60 s Poisson issuance window, aligned timer epochs with a random phase,
receipt->first request lognormal(120 ms, 0.5).  Segment requests after the first are cache hits.
"""
import csv
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sim import fleet_mc as F
from sim.workload import SEED

SR_BYTES = 4 + 4 + 8 + 4 + 4 + 1 + 16 + 2420


def main(res, reps=50):
    cfg = json.load(open(os.path.join(res, "proto_p3_config.json")))
    rtt = np.array([float(r["rtt_ms"]) for r in csv.DictReader(open(os.path.join(res, "proto_rtt.csv")))
                    if r["path"] == "edge_origin"])
    lr = np.log(rtt)
    rtt_med, rtt_sig = float(np.exp(np.median(lr))), float(lr.std())
    verify_ms = None
    vp = os.path.join(res, "proto_go_verify.csv")
    if os.path.exists(vp):
        for r in csv.DictReader(open(vp)):
            if r.get("op") in ("verify_root_mldsa44", "verify_root"):
                verify_ms = float(r["median_us"]) / 1000
    if verify_ms is None:
        verify_ms = 0.1
        print("WARNING: proto_go_verify.csv not found; using 0.1 ms root verify")
    rows = []
    for mode in cfg["modes"]:
        mid = F.MODE_ID[mode]
        for V in cfg["V_edges"]:
            w = 1.0 / np.arange(1, V + 1) ** 0.8
            w /= w.sum()
            cumw = np.cumsum(w)
            cumw[-1] = 1
            for d in cfg["delta_s"]:
                for lam in cfg["lambda_tokens_per_s"]:
                    acc = {k: [] for k in ("miss_per_token", "miss_lat_mean_ms", "wait_all_mean_ms", "wait_all_p99_ms",
                                           "root_bytes_per_token")}
                    for r in range(reps):
                        rng = np.random.default_rng([SEED, r, V, int(d * 1000), int(lam), mid])
                        n = rng.poisson(lam * 60.0)
                        arr = np.sort(rng.uniform(0, 60.0, n))
                        ph = rng.uniform(0, d)
                        tok_ep, close, N = F.epochs_fixed(arr + ph, d, 1 << 40)
                        close = close - ph
                        edge = np.minimum(np.searchsorted(cumw, rng.uniform(0, 1, n), side="right"), V - 1).astype(np.int64)
                        d0 = 0.120 * np.exp(0.5 * rng.standard_normal(n))
                        z = np.zeros(0, np.int64)
                        tw, nver, rw, rk, cnt = F.kernel(mid, tok_ep, close[tok_ep], edge, d0, z, np.zeros(0), z,
                                                         close, np.zeros(close.size, np.int64), np.zeros(1), 1,
                                                         SEED + r * 7 + V, rtt_med, rtt_sig, 0.0, 0.0, 150.0, 0.5)
                        if mode == "pull_staple":
                            misses = int(cnt[4])
                            waits = np.full(misses, verify_ms)
                            ml = verify_ms
                        else:
                            misses = int(cnt[0])
                            waits = rw * 1000 + verify_ms
                            ml = float(waits[rk == 1].mean()) if misses else 0.0
                        acc["miss_per_token"].append(misses / n)
                        acc["miss_lat_mean_ms"].append(ml)
                        acc["wait_all_mean_ms"].append(float(waits.mean()) if waits.size else 0.0)
                        acc["wait_all_p99_ms"].append(float(np.percentile(waits, 99)) if waits.size else 0.0)
                        acc["root_bytes_per_token"].append(misses * SR_BYTES / n)
                    for k, v in acc.items():
                        v = np.array(v)
                        h = 1.96 * v.std(ddof=1) / np.sqrt(len(v))
                        rows.append(dict(mode=mode, V=V, delta_s=d, **{"lambda": lam}, metric=k, mc_mean="%.6g" % v.mean(),
                                         mc_ci_lo="%.6g" % (v.mean() - h), mc_ci_hi="%.6g" % (v.mean() + h), reps=reps,
                                         rtt_lognorm_median_ms="%.4f" % rtt_med, rtt_lognorm_sigma="%.5f" % rtt_sig,
                                         verify_ms="%.4f" % verify_ms, impl="fleet_mc-kernel"))
    with open(os.path.join(res, "sim_proto_mc.csv"), "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0]))
        wr.writeheader()
        wr.writerows(rows)
    print("wrote sim_proto_mc.csv", len(rows), "rows; RTT lognormal median %.3f ms sigma %.4f; verify %.3f ms" % (rtt_med, rtt_sig, verify_ms))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../results", int(sys.argv[2]) if len(sys.argv) > 2 else 50)
