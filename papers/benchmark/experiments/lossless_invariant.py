#!/usr/bin/env python3
"""Lossless invariant: what the allocation (proto_alloc: feasible, feasible_frac) promises must be what the sender and receiver deliver with ZERO loss.

lossless_invariant.py OUT.csv [--quick] [--procs N]

For every (profile, scheme, mode, budget multiplier) cell of the protocol sweep (same budgets as run_proto.py: operating point 1.0 and the
minimum-budget grid):
  REPLAY (all cells, no cryptography): the sender's symbol layout (modes.Alloc.layout) is checked slot by slot (bytes per slot <= capacity,
    <= 255 symbols, symbols only inside the object's span, nothing in a slot that cannot carry authentication data, scheduled objects deliver >= k
    distinct symbols, unscheduled objects deliver none) and a symbolic receiver written here (independent of Alloc.lossless_set) derives the set of
    authenticated messages from the frames that exist; it must equal the allocation's prediction, and its share over the measured messages must
    equal `feasible_frac` exactly.
  REAL (a sample covering every mode, every profile and every scheme except SLH-DSA, the slow signer): the real sender builds the stream with
    real signatures / MACs / erasure coding, the real receiver processes it without loss, and the authenticated set over the measured messages must
    equal the prediction exactly with 0 false accepts.
Any mismatch is listed and the exit status is 1 (run.sh aborts before the protocol sweep)."""
import argparse
import csv
import multiprocessing as mp
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "lib")); sys.path.insert(0, HERE)
import run_proto as RP                                    # noqa: E402
from pqsig.common import tag                              # noqa: E402
from pqsig.proto import modes as MO                       # noqa: E402
from pqsig.proto.oqs import PQ, Ed                        # noqa: E402

REAL_PQS_QUICK = ["MAYO-1", "SNOVA_24_5_4", "Falcon-padded-512"]
REAL_PQS_FULL = ["ML-DSA-44", "Falcon-512", "Falcon-padded-512", "MAYO-1", "SNOVA_24_5_4", "OV-Is"]


def replay(A):
    """(problems, authenticated set) from the layout and a symbolic receiver."""
    P = A.plan; G = P.G; k = A.k; prob = []
    if not A.s:
        return prob, set()
    L = A.layout(); cost = A.s + A.ov
    got = {}
    for t, lst in enumerate(L.slots):
        room = A.slot_room(t)
        if len(lst) > MO.MAX_SLOT_SYMS:
            prob.append(f"slot {t}: {len(lst)} symbols")
        if lst and (room < 0 or len(lst) * cost > room):
            prob.append(f"slot {t}: {len(lst)} symbols x {cost} B > room {room}")
        for o, j in lst:
            sp = A.span(o)
            if not (sp.start <= t < sp.stop):
                prob.append(f"slot {t}: object {o} outside its span")
            nd = A.obj_params(o)[0]
            if nd == 0:
                prob.append(f"slot {t}: symbol of unscheduled object {o}")
                continue
            got.setdefault(o, set()).add(j % nd)
    decoded = {o for o, ix in got.items() if len(ix) >= k}
    if decoded != set(L.sched):
        prob.append(f"scheduled {len(L.sched)} != decoded {len(decoded)}")

    def frame(t):                                         # does slot t carry an authentication frame at all
        return 0 <= t < G and P.cap(t) >= A.mand
    if A.kind == "frag":
        return prob, {o for o in decoded if 0 <= o < G}
    if A.kind == "merkle":
        n = A.n; out = set()
        for g in range(G):
            b = g // n
            paths = [t for t in range(n, G) if frame(t) and t // n - 1 == b and (g % n) in (t % n, (t % n + n // 2) % n)]
            if b in decoded and paths:
                out.add(g)
        return prob, out
    E = P.E; d = P.d; out = set(); prev_any = False
    if d < 1 + MO.DELTA_SLOTS:
        return prob, out
    for e in range(G // E):
        known = (e in decoded) or (A.cont and prev_any)
        cur = set()
        for i in range(1, E + 1):
            g = e * E + i - 1
            keys = [e * E + i2 - 1 + d for i2 in range(i, E + 1)]
            if known and frame(g) and any(frame(t) for t in keys):
                cur.add(g)
        out |= cur; prev_any = bool(cur)
    return prob, out


def real_run(A, S, ed_pk):
    mask = np.zeros(S.plan.G, bool)
    rx, _, _, _ = RP.run_one(S, ed_pk, mask, 0, False)
    fa = sum(1 for s, a in rx.app.items() if a != S.truth.get(s))
    return set(rx.auth), fa, rx.rejected


def job(args):
    profile, pqname, quick, do_real = args
    tg = tag(); rows = []
    PQ._sig_cache.clear()
    plan0 = RP.plan_for(profile, pqname)
    mults = sorted(set([1.0] + list(RP.HYP["minbudget"]["multipliers"]["quick" if quick else "full"])))
    sig_len = PQ(pqname).sig_len
    key = PQ(pqname).keypair() if do_real else None
    ed = Ed() if do_real else None
    for mult in mults:
        plan = RP.plan_for(profile, pqname, int(round(plan0.B * mult)))
        for mode in MO.MODES:
            A = MO.Alloc(pqname, mode, plan, sig_len)
            meas = set(range(plan.W0, plan.W1))
            prob, rset = replay(A)
            pred = A.pred
            r = dict(tg, profile=profile, pq=pqname, B_mult=mult, mode=mode, B_slot=plan.B, feasible=int(A.feasible), feasible_frac=A.feas_frac,
                     predicted_n=len(pred & meas), measured_n=len(meas), replay_n=len(rset & meas),
                     replay_share=len(rset & meas) / len(meas), replay_ok=int(rset == pred and not prob and abs(len(rset & meas) / len(meas) - A.feas_frac) < 1e-12),
                     replay_note="; ".join(prob[:3]) if prob else ("" if rset == pred else f"replay set != prediction ({len(rset)} vs {len(pred)})"),
                     real_checked=0, real_n="", real_ok="", real_false_accepts="", real_note="")
            if do_real and A.feasible:
                S = MO.build(pqname, mode, plan, 0, key=key, ed=ed)
                a, fa, rej = real_run(A, S, ed.pk if A.hybrid else None)
                ok = (a & meas) == (pred & meas) and fa == 0
                r.update(real_checked=1, real_n=len(a & meas), real_ok=int(ok), real_false_accepts=fa,
                         real_note="" if ok else f"missing {sorted((pred & meas) - a)[:6]} extra {sorted((a & meas) - pred)[:6]}")
            elif do_real:
                r.update(real_checked=1, real_n=0, real_ok=int(A.feas_frac == 0), real_false_accepts=0)
            rows.append(r)
    PQ._sig_cache.clear()
    return rows


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("out"); ap.add_argument("--quick", action="store_true"); ap.add_argument("--procs", type=int, default=os.cpu_count())
    a = ap.parse_args(); t0 = time.time()
    real_pqs = REAL_PQS_QUICK if a.quick else REAL_PQS_FULL
    tasks = [(p, q, a.quick, q in real_pqs) for p in RP.PROFILES if "proto" in RP.YAML["profiles"][p] and RP.YAML["profiles"][p]["proto"] for q in RP.PQS]
    tasks.sort(key=lambda x: not x[3])
    with mp.Pool(a.procs) as pool:
        rows = [r for res in pool.imap_unordered(job, tasks) for r in res]
    cols = list(dict.fromkeys(k for r in rows for k in r))
    with open(a.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
    bad = [r for r in rows if not r["replay_ok"] or r["real_ok"] == 0]
    real = [r for r in rows if r["real_checked"] == 1]
    print(f"lossless invariant: {len(rows)} cells replayed, {len(real)} cells run with the real sender+receiver "
          f"({sum(1 for r in real if r['feasible'])} of them feasible), {len(bad)} mismatches, {time.time() - t0:.0f} s")
    for r in bad[:40]:
        print("MISMATCH", r["profile"], r["pq"], f"x{r['B_mult']}", r["mode"], "feas_frac", r["feasible_frac"], "replay", r["replay_n"], "real", r["real_n"],
              r["replay_note"], r["real_note"])
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
