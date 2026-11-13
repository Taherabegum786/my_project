#!/usr/bin/env python3
"""estimate_duration.py RAWDIR MACHINE -> prints the estimated duration of the FULL run, scaled from a QUICK run's phase timings
(raw/run_phases_<machine>.csv, raw/proto_runtime_<machine>.csv, raw/proto_alloc_<machine>.csv). Estimates, +-40%."""
import os
import sys

import pandas as pd
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))


def estimate(raw, mn):
    ph = os.path.join(raw, f"run_phases_{mn}.csv"); rt = os.path.join(raw, f"proto_runtime_{mn}.csv"); al = os.path.join(raw, f"proto_alloc_{mn}.csv")
    if not (os.path.exists(ph) and os.path.exists(rt) and os.path.exists(al)):
        return None
    p = pd.read_csv(ph); r = pd.read_csv(rt).iloc[0]; a = pd.read_csv(al)
    if not int(r.quick):
        return None
    com = yaml.safe_load(open(os.path.join(HERE, "profiles.yaml")))["common"]["protocol"]
    procs = int(r.procs); Ms = com["window_slots_M"]
    ratio_len = sum(Ms) / min(Ms)                      # stream length relative to the QUICK M
    cond_ratio = 1.5   # effective cost ratio of the 12 full loss conditions vs the 4 QUICK ones, MEASURED on a 40-config subset (full run 7.5x quick run = 5x stream length x 1.5)
    proto = (a.build_s.sum() * (5 / 2) * len(Ms) + a.run_s.sum() * ratio_len * cond_ratio) / procs
    sec = dict(zip(p.phase, p.seconds))
    tp = os.path.join(raw, f"oqs_timing_{mn}.csv")
    timing_full = None
    if os.path.exists(tp):
        d = pd.read_csv(tp)
        slow = d.scheme.str.contains("SLH|cross|mqom|SPHINCS")
        n_full = slow.map({True: 100, False: 10000})          # run.sh defaults: ITER=10000, ITER_SLOW=ITER/100
        nk = n_full.clip(upper=200)                            # key generation capped at 200 repetitions in oqs_bench
        timing_full = float(((n_full * (d.sign_mean_us + d.verify_mean_us) + nk * d.keygen_mean_us) / 1e6).sum()) * 1.1
    parts = {
        "build+setup (reused if build/ exists)": sec.get("setup", 0) + sec.get("liboqs_build", 0),
        "timing (ITER=10000, ITER_SLOW=100; from this run's mean op times)": timing_full if timing_full is not None else sec.get("timing", 0) * 50,
        "sizes+scoring": sec.get("sizes_scoring", 0),
        "negative tests (adds SLH-DSA, ~x2)": sec.get("negative_tests", 0) * 2,
        "protocol sweep": proto,
        "crosscheck+udp+summary": sec.get("crosscheck", 0) + sec.get("udp_smoke", 0) + sec.get("summarize", 0) * 1.5,
    }
    return parts, procs


if __name__ == "__main__":
    e = estimate(sys.argv[1], sys.argv[2])
    if e is None:
        print("estimate: no QUICK run timings yet; run `QUICK=1 ./run.sh` once, it prints the full-run estimate for this machine.")
    else:
        parts, procs = e
        for k, v in parts.items():
            print(f"  {k:62s} {v / 60:6.1f} min")
        print(f"  {'ESTIMATED FULL RUN on ' + str(procs) + ' cores (+-40%)':62s} {sum(parts.values()) / 60:6.1f} min")
