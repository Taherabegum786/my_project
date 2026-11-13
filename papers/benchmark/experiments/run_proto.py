#!/usr/bin/env python3
"""Real-protocol experiments at the native message rate (sender + receiver with real liboqs/Ed25519/HMAC/zfec, byte framing, seeded slot channel).

  run_proto.py sweep OUTDIR [--quick] [--procs N] [--machine NAME] [--seeds N]
      proto_results_<machine>.csv   operating point: the profile's real budget, every mode, 14 loss conditions (QUICK: 6), one row per seed
      minbudget_<machine>.csv       budget sweep: bytes per slot x mode x 4 loss conditions (QUICK: 2) -> smallest budget reaching a target share
      attack_<machine>.csv          active attacker: injection rate, receiver clock offset, replay of old epochs
      proto_alloc_<machine>.csv     allocation table (symbol size, k, n, redundancy, feasibility) of every (profile, scheme, mode, budget)
  run_proto.py udp ...              the same protocol over real UDP between two processes (see udp_link.py)

Randomness: the loss mask is drawn from an independent stream per (profile, scheme, loss condition) and seed; modes (and budgets) inside that
cell see the SAME mask (paired comparison).  Chain keys come from os.urandom per build and are never part of any seed.
"""
import argparse
import csv
import math
import multiprocessing as mp
import os
import random
import sys
import time

import numpy as np
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "lib"))
from pqsig import lossform as LF                       # noqa: E402
from pqsig.common import tag                           # noqa: E402
from pqsig.proto import attacks as AT                  # noqa: E402
from pqsig.proto import modes as MO                    # noqa: E402
from pqsig.proto.oqs import PQ, Counters, Ed, version  # noqa: E402

PROFILES = ["sib1", "cv2x_437", "cv2x_j3161"]
PQS = MO.PQ_IDS
YAML = yaml.safe_load(open(os.path.join(HERE, "profiles.yaml")))
COM = YAML["common"]["protocol"]
HYP = yaml.safe_load(open(os.path.join(HERE, "hypotheses.yaml")))
LAGS = 20


def plan_for(profile, pqname, B=None, E=None, n_meas=None):
    P = YAML["profiles"][profile]; pr = P["proto"]; B = int(B or P["auth_budget"]["bytes"])
    cap_cert = 0
    if pr["cert_every"]:
        q = PQ(pqname)
        cap_cert = B - (q.pk_len + 0 + q.sig_len)        # PQ issuer = same scheme; metadata TODO-RESULT (0 = lower bound)
    return MO.Plan(pr["slot_period_s"], B, pr["digest_bytes"], pr["app_bytes"], pr["cert_every"], cap_cert,
                   E or COM["epoch_windows_E"], n_meas or COM["measured_epochs"], COM["key_delay_slots_d"], COM["tail_slots"])


def cond_label(model, p, burst):
    return f"iid {p:g}" if model == "iid" else f"GE {p:g}/b{int(burst)}"


def conditions(kind, quick):
    c = HYP["conditions"][kind]["quick" if quick else "full"]
    return [(m, float(p), int(b)) for m, p, b in c]


def mask_for(profile, pqname, cond, seed, G):
    model, p, burst = cond
    sid = LF.stream_id(profile, pqname, cond_label(*cond))
    return LF.make_mask(G, seed, p, burst or None, stream=sid), f"{sid:x}-{seed}"


def run_one(S, ed_pk, mask, join, with_join=True, rx_kw=None, inject=None, jam=None):
    """Feed one stream through the steady receiver (CPU timed) and the late joiner."""
    P = S.plan; A = S.alloc
    rctr = Counters(); rx = MO.make_rx(A, S.pk, 0, rctr, ed_pk, **(rx_kw or {}))
    rj = MO.make_rx(A, S.pk, join, Counters(), ed_pk) if with_join else None
    tns = time.thread_time_ns; cpu = 0; jdone = not with_join; first = None
    for g in range(P.G):
        if inject and g in inject:
            for f in inject[g]:
                t0 = tns(); rx.deliver(g, *f); cpu += tns() - t0
                if not jdone and g >= join:
                    rj.deliver(g, *f)
        if mask[g] or (jam and g in jam):
            continue
        f = S.frames[g]
        t0 = tns(); rx.deliver(g, *f); cpu += tns() - t0
        if not jdone and g >= join:
            rj.deliver(g, *f)
            if rj.auth:
                jdone = True; first = min(rj.auth.values())
    return rx, rctr, cpu, first


def metrics(S, rx, rctr, cpu, mask, jam=None):
    """Per-run metrics over the steady-state messages W0..W1-1 (see modes.py): share is relative to RECEIVED messages."""
    P = S.plan; lo, hi = P.W0, P.W1
    recv = [g for g in range(lo, hi) if not mask[g] and not (jam and g in jam)]
    rset = set(recv)
    good = [s for s in rx.auth if s in rset and rx.app.get(s) == S.truth.get(s)]
    lags = [rx.auth[s] + 1 - s for s in good]
    out = dict(N_meas=hi - lo, received=len(recv), authenticated=len(good),
               share=(len(good) / len(recv) if recv else float("nan")), delivered_frac=len(recv) / (hi - lo),
               false_accepts=sum(1 for s, a in rx.app.items() if a != S.truth.get(s)),
               stale_accepted=sum(1 for s, g in rx.auth.items() if g + 1 - s > MO.FRESH_SLOTS),
               rejected=rx.rejected, stale_rej=rx.stale_rej, replay_rej=rx.replay_rej)
    for j in range(1, LAGS + 1):
        out[f"lag_{j}"] = sum(1 for x in lags if x == j)
    out["lag_gt20"] = sum(1 for x in lags if x > LAGS)
    ab = S.air_bytes()
    out.update(air_bytes=ab, air_bytes_per_auth=(ab / len(good) if good else ""),
               rx_cpu_us_per_msg=cpu / 1e3 / max(1, hi - lo), rx_verify_us_per_msg=rctr.verify_ns / 1e3 / max(1, hi - lo))
    return out


def sender_fields(S):
    T_us = S.plan.T * 1e6
    cpm = S.cpu_msgs or 1
    return dict(tx_cpu_us_per_msg=S.tx_cpu_ns / 1e3 / cpm, tx_sign_us_per_msg=S.tx_sign_ns / 1e3 / cpm,
                tx_realtime_ratio=S.tx_cpu_ns / 1e3 / cpm / T_us)


def build_streams(profile, pqname, mode, plan, nb, pk, sk, ed):
    return [MO.build(pqname, mode, plan, build_seed=b, key=(pk, sk), ed=ed) for b in range(nb)]


def base_row(tg, exp, profile, pqname, mode, plan, A, cond, seed, bid, B_mult):
    return dict(tg, experiment=exp, profile=profile, pq=pqname, mode=mode, B_slot=plan.B, B_mult=B_mult, bytes_per_s=plan.B / plan.T,
                loss_model=cond[0], loss_p=cond[1], burst_len=cond[2], cond=cond_label(*cond), seed=seed, build_id=bid,
                feasible=int(A.feasible), feas_frac=A.feas_frac, slot_period_ms=plan.T_ms)


def nbuilds(pk_sk_pq, plan, quick):
    q, pk, sk = pk_sk_pq
    t = time.thread_time_ns(); q.sign(b"calibrate" + os.urandom(4), sk, cache=False); s = (time.thread_time_ns() - t) / 1e9
    return 1 if s > 0.02 else 2


def sim_cell(profile, pqname, mode, plan, streams, pk_ed, cond_list, nseeds, exp, B_mult, tg, with_join):
    """Run every condition x seed on the prepared streams; returns rows."""
    rows = []; A = streams[0].alloc; nb = len(streams)
    for cond in cond_list:
        for seed in range(nseeds):
            S = streams[seed % nb]
            mask, mid = mask_for(profile, pqname, cond, seed, plan.G)
            rng = np.random.default_rng(np.random.SeedSequence([seed, LF.stream_id(profile, pqname, "join")]))
            join = plan.W0 + int(rng.integers(0, plan.E))
            base = base_row(tg, exp, profile, pqname, mode, plan, A, cond, seed, seed % nb, B_mult)
            base.update(mask_id=mid, **sender_fields(S))
            if not A.feasible:
                lagz = {f"lag_{j}": 0 for j in range(1, LAGS + 1)}
                recv = sum(1 for g in range(plan.W0, plan.W1) if not mask[g])
                rows.append(dict(base, N_meas=plan.N, received=recv, authenticated=0, share=0.0, delivered_frac=recv / plan.N, false_accepts=0,
                                 stale_accepted=0, rejected=0, stale_rej=0, replay_rej=0, lag_gt20=0, air_bytes=0, air_bytes_per_auth="",
                                 rx_cpu_us_per_msg="", rx_verify_us_per_msg="", ttfa_ms="", ttfa_censored=1, join_slot="", **lagz))
                continue
            rx, rctr, cpu, first = run_one(S, pk_ed, mask, join, with_join)
            m = metrics(S, rx, rctr, cpu, mask)
            m.update(ttfa_ms=((first + 1 - join) * plan.T_ms if first is not None else ""), ttfa_censored=int(first is None) if with_join else "",
                     join_slot=join - plan.W0 if with_join else "")
            rows.append(dict(base, **m))
    return rows


def attack_rows(profile, pqname, mode, plan, streams, pk_ed, tg, quick, nseeds):
    """Active attacker on the same harness: injection rate, receiver clock offset (with the delayed-forgery attacker), replay of old epochs."""
    A = streams[0].alloc; nb = len(streams); rows = []
    if not A.feasible:
        return rows
    H = HYP["attack"]; bg = ("iid", H["background_loss"], 0)
    rates = H["inject_rates"]["quick" if quick else "full"]; offs = H["clock_offsets_slots"]["quick" if quick else "full"]
    E = plan.E; d = plan.d

    def mk(att, param, S, seed, mask, jam, inject, rx_kw=None, extra=None):
        rx, rctr, cpu, _ = run_one(S, pk_ed, mask, 0, False, rx_kw, inject, jam)
        m = metrics(S, rx, rctr, cpu, mask, jam)
        r = base_row(tg, "attack", profile, pqname, mode, plan, A, bg, seed, seed % nb, 1)
        r.update(attack=att, param=param, **{k: m[k] for k in ("N_meas", "received", "authenticated", "share", "false_accepts", "stale_accepted",
                                                               "rejected", "stale_rej", "replay_rej", "rx_cpu_us_per_msg", "rx_verify_us_per_msg")})
        r.update(extra or {}); return r

    for seed in range(nseeds):
        S = streams[seed % nb]
        mask, mid = mask_for(profile, pqname, bg, seed, plan.G)
        arng = random.Random(LF.stream_id(profile, pqname, "attacker", seed))
        rows.append(dict(mk("none", 0, S, seed, mask, None, None), mask_id=mid))
        for inten in H["inject_intensity"]:
            for r_ in rates:
                inj = {}
                for g in range(plan.G):
                    if arng.random() < r_ and S.fields.get(g):
                        inj[g] = [AT.pollute(S.frames[g], S.fields[g], arng) for _ in range(inten)]
                rows.append(dict(mk("inject" if inten == 1 else f"inject_x{inten}", r_, S, seed, mask, None, inj), mask_id=mid))
        # clock offset sweep with the delayed-forgery attacker: every 5th measured message is jammed and forged after its key is disclosed
        targets = [m_ for m_ in range(plan.W0 + 2, plan.W1, 5)]
        jam = set(targets); inj = {}
        for m_ in targets:
            g_f = m_ + d + 1
            if g_f < plan.G and S.frames[m_][1]:
                inj.setdefault(g_f, []).append(AT.forge_after_disclosure(S, m_))
        for o in offs:
            rx_kw = dict(clock_ms=int(o * plan.T_ms))
            rows.append(dict(mk("clock", o, S, seed, mask, jam, inj, rx_kw), mask_id=mid))
        # replay of an old epoch: the receiver is offline during epoch 1 (messages W0..W0+E-1); the attacker replays the recorded frames
        # 4 epochs later (older than the freshness bound of 64 slots).  Control: the same receiver without freshness checks.
        old = list(range(plan.W0, plan.W0 + E)); shift = 4 * E
        jam = set(old); inj = {}
        for g in old:
            if g + shift < plan.G:
                inj.setdefault(g + shift, []).append(S.frames[g])
        rx_m, rc_m, cpu_m, _ = run_one(S, pk_ed, mask, 0, False, None, inj, jam)
        mm = metrics(S, rx_m, rc_m, cpu_m, mask, jam)
        r_main = base_row(tg, "attack", profile, pqname, mode, plan, A, bg, seed, seed % nb, 1)
        r_main.update(attack="replay", param=shift, **{k: mm[k] for k in ("N_meas", "received", "authenticated", "share", "false_accepts", "stale_accepted",
                                                                          "rejected", "stale_rej", "replay_rej", "rx_cpu_us_per_msg", "rx_verify_us_per_msg")})
        rx_c, rctr_c, cpu_c, _ = run_one(S, pk_ed, mask, 0, False, dict(enforce_fresh=False, enforce_time_safety=False), inj, jam)
        r_main.update(replay_accepted=len(set(rx_m.auth) & set(old)), ctrl_replay_accepted=len(set(rx_c.auth) & set(old)), mask_id=mid)
        rows.append(r_main)
    return rows


def run_pair(args):
    profile, pqname, quick, nseeds_oper, nseeds_min, do_attack = args
    tg = tag(); out = dict(oper=[], minb=[], attack=[], alloc=[])
    PQ._sig_cache.clear()                                    # signatures are shared across modes / budgets of THIS pair only
    t_start = time.time()
    plan0 = plan_for(profile, pqname)
    q = PQ(pqname); pk, sk = q.keypair()
    nb = nbuilds((q, pk, sk), plan0, quick)
    ed = Ed()
    conds_o = conditions("operating", quick); conds_m = conditions("minbudget", quick)
    mults = HYP["minbudget"]["multipliers"]["quick" if quick else "full"]
    t_build = 0.0
    for B_mult in sorted(set([1.0] + list(mults))):
        B = int(round(plan0.B * B_mult)); plan = plan_for(profile, pqname, B)
        for mode in MO.MODES:
            tb = time.time()
            streams = build_streams(profile, pqname, mode, plan, nb, pk, sk, ed)
            t_build += time.time() - tb
            A = streams[0].alloc
            out["alloc"].append(dict(tg, profile=profile, B_mult=B_mult, n_builds=nb, **A.row()))
            ed_pk = ed.pk if A.hybrid else None
            if B_mult == 1.0:
                out["oper"] += sim_cell(profile, pqname, mode, plan, streams, ed_pk, conds_o, nseeds_oper, "operating", B_mult, tg, True)
                if do_attack:
                    out["attack"] += attack_rows(profile, pqname, mode, plan, streams, ed_pk, tg, quick, nseeds_min)
            if B_mult in mults:
                out["minb"] += sim_cell(profile, pqname, mode, plan, streams, ed_pk, conds_m, nseeds_min, "minbudget", B_mult, tg, False)
    PQ._sig_cache.clear()
    out["secs"] = time.time() - t_start; out["build_s"] = t_build; out["nb"] = nb
    return (profile, pqname), out


def write_csv(path, rows):
    cols = list(dict.fromkeys(k for r in rows for k in r))
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)


def sweep(a):
    machine = a.machine or os.environ.get("MACHINE_NAME", "unknown")
    os.environ["MACHINE_NAME"] = machine
    nso = a.seeds or 20; nsm = min(10, nso)               # operating point: --seeds (default 20); minimum-budget sweep and attacker: at most 10
    attack_pairs = {tuple(x) for x in HYP["attack"]["pairs"]}
    tasks = [(p, q, a.quick, nso, nsm, (p, q) in attack_pairs) for p in a.profiles for q in a.pqs]
    tasks.sort(key=lambda t: -(10 if "SLH" in t[1] else 1) * (1 + 0.2 * t[5]))
    t0 = time.time(); R = dict(oper=[], minb=[], attack=[], alloc=[]); per = []
    with mp.Pool(a.procs) as pool:
        for i, (key, o) in enumerate(pool.imap_unordered(run_pair, tasks)):
            for k in R:
                R[k] += o[k]
            per.append(dict(tag(), profile=key[0], pq=key[1], secs=round(o["secs"], 1), build_s=round(o["build_s"], 1), n_builds=o["nb"],
                            rows_oper=len(o["oper"]), rows_minb=len(o["minb"]), rows_attack=len(o["attack"])))
            print(f"  {i + 1}/{len(tasks)} (profile, scheme) done, {time.time() - t0:.0f}s", flush=True)
    os.makedirs(a.outdir, exist_ok=True)
    write_csv(os.path.join(a.outdir, f"proto_results_{machine}.csv"), R["oper"])
    write_csv(os.path.join(a.outdir, f"minbudget_{machine}.csv"), R["minb"])
    write_csv(os.path.join(a.outdir, f"attack_{machine}.csv"), R["attack"])
    write_csv(os.path.join(a.outdir, f"proto_alloc_{machine}.csv"), R["alloc"])
    write_csv(os.path.join(a.outdir, f"proto_pairtime_{machine}.csv"), per)
    el = time.time() - t0
    print(f"sweep done: {len(tasks)} (profile, scheme) tasks, rows oper={len(R['oper'])} minbudget={len(R['minb'])} attack={len(R['attack'])}, {el:.0f}s wall on {a.procs} procs")
    with open(os.path.join(a.outdir, f"proto_runtime_{machine}.csv"), "w") as f:
        t = tag()
        f.write("machine,quick,tasks,seeds_oper,seeds_min,procs,wall_s,liboqs,git_commit,git_dirty\n")
        f.write(f"{machine},{int(a.quick)},{len(tasks)},{nso},{nsm},{a.procs},{el:.1f},{version()},{t['git_commit']},{t['git_dirty']}\n")


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
