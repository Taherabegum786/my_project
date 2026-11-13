#!/usr/bin/env python3
"""Real-protocol experiments (sender + receiver with real liboqs/Ed25519/HMAC/zfec, byte framing, seeded slot channel).

  run_proto.py sweep OUTDIR [--quick] [--procs N] [--machine NAME]
      writes OUTDIR/proto_results_<machine>.csv (one row per profile x pq x mode x M x loss condition x seed)
             OUTDIR/proto_alloc_<machine>.csv   (the allocation table: slots, bytes per slot, k, n, rate per scheme)
  run_proto.py udp --role sender|receiver --udp HOST:PORT --profile P --pq SCHEME --mode MODE --M 10 --loss iid:0.1 --seed 3 [--speed X]
      same protocol over real UDP between two processes (or two machines); loss injected at the receiver from the same seeded mask.
"""
import argparse
import csv
import itertools
import math
import multiprocessing as mp
import os
import statistics
import sys
import time

import numpy as np
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "lib"))
from pqsig import lossform as LF                       # noqa: E402
from pqsig.common import tag                           # noqa: E402
from pqsig.proto import modes as MO                    # noqa: E402
from pqsig.proto.oqs import PQ, Counters, Ed, version  # noqa: E402

PROFILES = ["sib1", "cv2x_437", "cv2x_j3161"]
PQS = MO.PQ_IDS
YAML = yaml.safe_load(open(os.path.join(HERE, "profiles.yaml")))
COM = YAML["common"]["protocol"]


def plan_for(profile, pqname, M, N=None, E=None):
    P = YAML["profiles"][profile]; pr = P["proto"]; B = P["auth_budget"]["bytes"]
    N = N or COM["data_windows_N"]; E = E or COM["epoch_windows_E"]
    cap_reg = B - pr["digest_bytes"]
    cap_cert = 0
    if pr["cert_every"]:
        q = PQ(pqname)
        meta = 0                                        # TODO-RESULT in profiles.yaml (lower bound on certificate size)
        cap_cert = max(0, B - (q.pk_len + meta + q.sig_len))   # PQ issuer = same scheme
    return MO.Plan(pr["slot_period_s"], cap_reg, pr["app_bytes"], M, pr["cert_every"], cap_cert, E, N)


def conditions(quick):
    if quick:
        return [("iid", 0.0, 0), ("iid", 0.1, 0), ("iid", 0.3, 0), ("ge", 0.1, 5)]
    c = [("iid", p, 0) for p in (0.0, 0.02, 0.05, 0.1, 0.2, 0.3)]
    c += [("ge", p, b) for p in (0.1, 0.2, 0.3) for b in (3, 10)]
    return c


def one_run(S, rx, rj, mask, join):
    """Feed one seed's stream through the steady receiver (rx, CPU timed) and the late joiner (rj)."""
    fr = S.frames; tns = time.thread_time_ns; cpu = 0; jdone = False; first = None
    for g in range(len(fr)):
        f = fr[g]
        if f is None or mask[g]:
            continue
        t0 = tns(); rx.deliver(g, f[0], f[1]); cpu += tns() - t0
        if not jdone and g >= join:
            rj.deliver(g, f[0], f[1])
            if rj.auth:
                jdone = True; first = min(rj.auth.values())
    return cpu, first


def delays_ms(rx, plan):
    out = []
    for seq, g in rx.auth.items():
        out.append(((g + 1) - (plan.off + seq) * plan.M) * plan.T * 1000.0)
    return out


def run_config(args):
    profile, pqname, mode, M, quick, nseeds = args
    plan = plan_for(profile, pqname, M)
    tg = tag(); rows = []
    ctr0 = Counters(); pqq = PQ(pqname, ctr0); pk, sk = pqq.keypair()
    A0 = MO.Alloc(pqname, mode, plan, pqq.sig_len)
    t = time.thread_time_ns(); pqq.sign(b"calibrate", sk); sign_s = (time.thread_time_ns() - t) / 1e9
    nb = 1 if (sign_s > 0.02 and not quick) or sign_s > 0.1 else (2 if quick else 5)
    ed = Ed() if A0.hybrid else None
    tb = time.time()
    streams = [MO.build(pqname, mode, plan, build_seed=b, key=(pk, sk), ed=ed) for b in range(nb)]
    build_s = time.time() - tb; tr = time.time()
    A = streams[0].alloc
    alloc_row = A.row()
    conds = conditions(quick)
    win_ms = M * plan.T * 1000.0
    alloc_B = sum(plan.cap(j) for j in range(M))
    for (model, p, burst) in conds:
        for seed in range(nseeds):
            S = streams[seed % nb]
            base = dict(tg, profile=profile, pq=pqname, mode=mode, M=M, n_batch=A.n if A.kind == "merkle" else "",
                        loss_model=model, loss_p=p, burst_len=burst, seed=seed, build_id=seed % nb, transport="inproc",
                        feasible=int(A.feasible), N_msgs=plan.N, window_ms=win_ms, alloc_bytes_per_msg=alloc_B,
                        tx_cpu_us_per_msg=S.tx_cpu_ns / 1e3 / S.cpu_msgs, tx_sign_us_per_msg=S.tx_sign_ns / 1e3 / S.cpu_msgs)
            base["tx_realtime_ratio"] = base["tx_cpu_us_per_msg"] / 1e3 / win_ms
            if not A.feasible:
                rows.append(dict(base, authenticated=0, share=0.0, false_accepts=0, rejected=0, delay_median_ms="", delay_p95_ms="",
                                 ttfa_ms="", ttfa_censored=1, join_slot="", air_auth_bytes_total=0, air_bytes_per_auth_msg="",
                                 rx_cpu_us_per_msg="", rx_verify_us_per_msg=""))
                continue
            mask = LF.make_mask(plan.G, seed, p, burst or None)
            rng = np.random.default_rng(np.random.SeedSequence([seed, 77]))
            join = plan.off * M + int(rng.integers(0, plan.E * M))
            rctr = Counters()
            rx = MO.make_rx(A, S.pk, 0, rctr, ed.pk if ed else None)
            rj = MO.make_rx(A, S.pk, join, Counters(), ed.pk if ed else None)
            cpu, first = one_run(S, rx, rj, mask, join)
            d = delays_ms(rx, plan)
            fa = sum(1 for s, a in rx.app.items() if a != S.truth.get(s))
            na = len(rx.auth)
            rows.append(dict(base, authenticated=na, share=na / plan.N, false_accepts=fa, rejected=rx.rejected,
                             delay_median_ms=(statistics.median(d) if d else ""),
                             delay_p95_ms=(float(np.percentile(d, 95)) if d else ""),
                             ttfa_ms=((first + 1 - join) * plan.T * 1000.0 if first is not None else ""),
                             ttfa_censored=int(first is None), join_slot=join - plan.off * M,
                             air_auth_bytes_total=S.air_bytes, air_bytes_per_auth_msg=(S.air_bytes / na if na else ""),
                             rx_cpu_us_per_msg=cpu / 1e3 / plan.N, rx_verify_us_per_msg=rctr.verify_ns / 1e3 / plan.N))
    alloc_row.update(build_s=round(build_s, 3), run_s=round(time.time() - tr, 3), n_builds=nb)
    return alloc_row, rows


def write_csv(path, rows):
    cols = list(dict.fromkeys(k for r in rows for k in r))
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)


def sweep(a):
    machine = a.machine or os.environ.get("MACHINE_NAME", "unknown")
    os.environ["MACHINE_NAME"] = machine
    Ms = [10] if a.quick else COM["window_slots_M"]
    nseeds = a.seeds or 20
    tasks = [(p, q, m, M, a.quick, nseeds) for p in a.profiles for q in a.pqs for m in MO.MODES for M in Ms]
    # longest first (SLH-DSA, big M) for load balance
    tasks.sort(key=lambda t: -(t[3] * (3 if "SLH" in t[1] else 1)))
    t0 = time.time(); allr = []; alloc = []
    with mp.Pool(a.procs) as pool:
        for i, (ar, rows) in enumerate(pool.imap_unordered(run_config, tasks)):
            alloc.append(dict(tag(), profile=rows[0]["profile"] if rows else "", **ar)); allr += rows
            if (i + 1) % 20 == 0:
                print(f"  {i + 1}/{len(tasks)} configs, {time.time() - t0:.0f}s", flush=True)
    os.makedirs(a.outdir, exist_ok=True)
    write_csv(os.path.join(a.outdir, f"proto_results_{machine}.csv"), allr)
    write_csv(os.path.join(a.outdir, f"proto_alloc_{machine}.csv"), alloc)
    el = time.time() - t0
    print(f"sweep done: {len(tasks)} configs, {len(allr)} rows, {el:.0f}s wall on {a.procs} procs")
    with open(os.path.join(a.outdir, f"proto_runtime_{machine}.csv"), "w") as f:
        t = tag()
        f.write("machine,quick,configs,seeds,procs,wall_s,liboqs,git_commit,git_dirty\n")
        f.write(f"{machine},{int(a.quick)},{len(tasks)},{nseeds},{a.procs},{el:.1f},{version()},{t['git_commit']},{t['git_dirty']}\n")


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("sweep"); s.add_argument("outdir"); s.add_argument("--quick", action="store_true")
    s.add_argument("--procs", type=int, default=os.cpu_count()); s.add_argument("--machine"); s.add_argument("--seeds", type=int)
    s.add_argument("--profiles", nargs="+", default=PROFILES); s.add_argument("--pqs", nargs="+", default=PQS)
    u = sp.add_parser("udp")
    from udp_link import add_args
    add_args(u)
    a = ap.parse_args()
    if a.cmd == "sweep":
        sweep(a)
    else:
        from udp_link import run_udp
        run_udp(a)


if __name__ == "__main__":
    main()
