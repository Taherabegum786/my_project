#!/usr/bin/env python3
"""Negative tests (real REJECT tests) and positive controls, reported separately (column `kind`).
negative_tests.py OUT.csv [--quick]

Plan: SIB1 slot period and message size, generous budget B_TEST per slot so that every mode is feasible for every scheme (the tests check
rejection logic, not the budget), E = 8 slots per epoch, 120 slots, no channel loss.  For every test the expected authenticated set is
stated (= the set of an untouched run minus the messages the attacker must be able to deny) and compared with the actual set.  A reject test
passes when the actual set equals the expected set (nothing extra authenticated, nothing the attacker should not be able to block lost),
false_accepts == 0 (accepted bytes differ from sent bytes) and stale_accepted == 0.  A control passes when its stated positive
outcome occurs (e.g. a receiver WITHOUT the check accepts the forgery) - controls prove that a reject test bites and are NOT counted as tests.

Attacker knowledge (attacks.py): hears all frames, knows formats, schedule and public key; has no PQ secret key and no chain secret
(chain keys are os.urandom per build); learns a chain key only through its disclosure."""
import copy
import csv
import os
import random
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "lib"))
sys.path.insert(0, HERE)
import run_proto as RP                                   # noqa: E402
from pqsig.common import tag                             # noqa: E402
from pqsig.proto import attacks as AT                    # noqa: E402
from pqsig.proto import modes as MO                      # noqa: E402
from pqsig.proto.oqs import PQ, Counters, Ed             # noqa: E402

E_ = 8
B_TEST = 9376                                            # 32 x the SIB1 budget
DSTAR = 19                                               # message attacked (epoch 2 of 8-slot epochs, batch 1 of 16 / 2 of 8)


class BadEd(Ed):
    """Ed25519 signer whose signatures are over the wrong bytes (valid key, invalid signature)."""
    def sign(self, msg):
        return super().sign(msg + b"x")


def plan_t():
    P = RP.YAML["profiles"]["sib1"]["proto"]
    return MO.Plan(P["slot_period_s"], B_TEST, P["digest_bytes"], P["app_bytes"], 0, 0, E_, 4, 2, 80)


def with_frames(S, frames):
    S2 = copy.copy(S); S2.frames = frames; return S2


def run_rx(S, frames=None, inject=None, jam=None, rx_kw=None, ed_pk=None, pk=None):
    S2 = with_frames(S, frames if frames is not None else S.frames)
    if pk is not None:
        S2.pk = pk
    mask = np.zeros(S.plan.G, bool)
    rx, rctr, cpu, _ = RP.run_one(S2, ed_pk, mask, 0, False, rx_kw, inject, jam)
    fa = sum(1 for s, a in rx.app.items() if a != S.truth.get(s))
    stale = sum(1 for s, g in rx.auth.items() if g + 1 - s > MO.FRESH_SLOTS)
    return rx, fa, stale


def tests_for(pqname, mode):
    out = []
    P = plan_t(); E = E_
    q = PQ(pqname); key = q.keypair(); ed_good = Ed()
    S = MO.build(pqname, mode, P, 0, key=key, ed=ed_good)
    A = S.alloc
    if not A.feasible:
        return [dict(test="build", kind="n/a", note=f"allocation infeasible at B_TEST ({B_TEST} B)", passed="")]
    edpk = ed_good.pk if A.hybrid else None
    base_rx, fa0, st0 = run_rx(S, ed_pk=edpk)
    base = set(base_rx.auth)
    ep = lambda e: set(range(e * E, (e + 1) * E))                         # noqa: E731
    D = DSTAR; M = P.d; n = A.n if A.kind == "merkle" else 1
    F = S.frames

    def rec(name, kind, expected, rx, fa, stale, note="", ok_extra=True):
        got = set(rx.auth)
        ok = (got == expected) and fa == 0 and stale == 0 and ok_extra
        out.append(dict(test=name, kind=kind, expected=len(expected), got=len(got), missing_expected=len(expected - got),
                        unexpected_auth=len(got - expected), false_accepts=fa, stale_accepted=stale, rejected=rx.rejected, passed=int(ok), note=note))

    def ctl(name, ok, rx, fa, note=""):
        out.append(dict(test=name, kind="control", expected="", got=len(rx.auth), false_accepts=fa, stale_accepted="", rejected=rx.rejected,
                        passed=int(bool(ok)), note=note))

    rec("C0 untouched stream authenticates (positive control)", "control", base, base_rx, fa0, st0, ok_extra=len(base) >= 16)

    # ---- R1 tampered application payload (every frame of message D's slot)
    fr = list(F); fr[D] = (AT.flip(F[D][0], 20), F[D][1])
    rx, fa, st = run_rx(S, fr, ed_pk=edpk); rec("R1 tampered application payload", "reject", base - {D}, rx, fa, st)

    # ---- R2 tampered authenticator of message D
    fr = list(F)
    if A.kind == "frag":
        for t in range(D, D + A.W):
            for age, idx, a0, a1 in AT.frag_symbols(S, t):
                if t - age == D:
                    fr[t] = AT.replace_range(fr[t], a0, a1, bytes(x ^ 0xFF for x in fr[t][1][a0:a1]))
        rx, fa, st = run_rx(S, fr, ed_pk=edpk); rec("R2 tampered signature symbols of one message", "reject", base - {D}, rx, fa, st)
    elif A.kind == "merkle":
        b = D // n; leaf = D % n; hit = 0
        for jj in range(n):
            t = (b + 1) * n + jj
            ents = [jj, (jj + n // 2) % n]
            if leaf in ents and t < P.G and S.fields.get(t):
                paths = [f for f in S.fields[t] if f[2] == "path"]
                a0, a1, _ = paths[ents.index(leaf)]
                fr[t] = AT.replace_range(fr[t], a0, a1, AT.flip(fr[t][1][a0:a1], 3)); hit += 1
        rx, fa, st = run_rx(S, fr, ed_pk=edpk); rec("R2 tampered Merkle authentication path (all copies)", "reject", base - {D}, rx, fa, st)
        fr = list(F)
        for t in range((b + 1) * n, (b + 2) * n):
            for f in S.fields.get(t, []):
                if f[2] == "sym":
                    fr[t] = AT.replace_range(fr[t], f[0], f[1], bytes(x ^ 0xFF for x in fr[t][1][f[0]:f[1]]))
        rx, fa, st = run_rx(S, fr, ed_pk=edpk); rec("R2b tampered batch-signature symbols (whole batch)", "reject", base - set(range(b * n, (b + 1) * n)), rx, fa, st)
    else:
        for f in S.fields.get(D, []):
            if f[2] == "tag":
                fr[D] = AT.replace_range(fr[D], f[0], f[1], AT.flip(fr[D][1][f[0]:f[1]], 2))
        rx, fa, st = run_rx(S, fr, ed_pk=edpk); rec("R2 tampered MAC tag", "reject", base - {D}, rx, fa, st)
        fr = list(F); g = D + M
        for f in S.fields.get(g, []):
            if f[2] == "key":
                fr[g] = AT.replace_range(fr[g], f[0], f[1], AT.flip(fr[g][1][f[0]:f[1]], 1))
        rx, fa, st = run_rx(S, fr, ed_pk=edpk)
        rec("R2c tampered disclosed key (one slot): rejected, later keys still authenticate", "reject", base, rx, fa, st, ok_extra=rx.rejected > 0)

    # ---- R3 wrong signer: an attacker with its own PQ key and its own random chain secret (NOT the victim's) builds a full stream
    atk_key = PQ(pqname).keypair(cache=False)
    Sa = MO.build(pqname, mode, P, 0, key=atk_key, ed=ed_good)
    rx, fa, st = run_rx(S, Sa.frames, ed_pk=edpk); rec("R3 wrong signer (attacker stream alone, victim public key)", "reject", set(), rx, fa, st)
    inj = {g: [Sa.frames[g]] for g in range(P.G)}
    rx, fa, st = run_rx(S, F, inject=inj, ed_pk=edpk); rec("R3b wrong signer interleaved with the genuine stream", "reject", base, rx, fa, st)

    if A.hybrid:
        bad = BadEd(); Sb = MO.build(pqname, mode, P, 0, key=key, ed=bad)
        rx, fa, st = run_rx(S, Sb.frames, ed_pk=ed_good.pk); rec("R7 hybrid: valid PQ half, invalid Ed25519 half", "reject", set(), rx, fa, st)

    # ---- R5 replay of old signed messages, every mode: the receiver is offline for epoch 2, the attacker replays the recorded frames 72 slots later
    old = list(range(2 * E, 3 * E)); shift = MO.FRESH_SLOTS + 3 * E
    jam = set(old); inj = {}
    for g in old:
        if g + shift < P.G:
            inj.setdefault(g + shift, []).append(F[g])
    rxj, _, _ = run_rx(S, F, jam=jam, ed_pk=edpk)                        # same outage, no attacker: what honest reception yields
    rx, fa, st = run_rx(S, F, inject=inj, jam=jam, ed_pk=edpk)
    rec("R5 replay of an old epoch (frames recorded while the receiver was offline)", "reject", set(rxj.auth), rx, fa, st,
        ok_extra=not (set(rx.auth) & set(old)))
    rxc, fac, stc = run_rx(S, F, inject=inj, jam=jam, rx_kw=dict(enforce_fresh=False, enforce_time_safety=False), ed_pk=edpk)
    ctl("C5 replay accepted by a receiver WITHOUT freshness (and time-safety) checks", len({s for s in rxc.auth if s in set(old)}) >= 1, rxc, fac,
        "control: shows the replay test bites")

    # R5b: only message D is lost to the receiver, everything else (including a verified batch root / disclosed keys) arrives; the attacker replays D's frame late
    inj = {D + shift: [F[D]]}
    rxj, _, _ = run_rx(S, F, jam={D}, ed_pk=edpk)
    rx, fa, st = run_rx(S, F, inject=inj, jam={D}, ed_pk=edpk)
    rec("R5b late replay of one message frame after the rest of the stream was verified", "reject", set(rxj.auth), rx, fa, st, ok_extra=D not in rx.auth)
    rxc, fac, stc = run_rx(S, F, inject=inj, jam={D}, rx_kw=dict(enforce_fresh=False, enforce_time_safety=False), ed_pk=edpk)
    ctl("C5b late single-frame replay accepted by a receiver WITHOUT freshness (and time-safety) checks", D in rxc.auth, rxc, fac, "control: shows the test bites")

    # ---- R10 symbol injection / pollution
    rng = random.Random(7)
    inj = {g: [AT.pollute(F[g], S.fields[g], rng)] for g in range(P.G) if S.fields.get(g)}
    rx, fa, st = run_rx(S, F, inject=inj, ed_pk=edpk)
    rec("R10 polluted copy of every frame injected (random payload bytes)", "reject", set(rx.auth), rx, fa, st,
        note=f"authenticated {len(rx.auth)}/{len(base)} of the unattacked set", ok_extra=set(rx.auth) <= base)
    fr = list(F)
    if A.kind == "frag":
        for t in range(D, D + A.W):
            for age, idx, a0, a1 in AT.frag_symbols(S, t):
                if t - age == D:
                    fr[t] = AT.replace_range(fr[t], a0, a1, rng.randbytes(a1 - a0))
        rx, fa, st = run_rx(S, fr, ed_pk=edpk); rec("R10b all symbols of one message replaced by random bytes (blocking attack)", "reject", base - {D}, rx, fa, st)

    if A.kind == "chain":
        # ---- R4 forged message with the disclosed key, delivered after the key was released; the honest frame is jammed
        forged = AT.forge_after_disclosure(S, D)
        inj = {D + M + 1: [forged]}
        rx, fa, st = run_rx(S, F, inject=inj, jam={D}, ed_pk=edpk); rec("R4 forged message with the disclosed key (late delivery)", "reject", base - {D}, rx, fa, st)
        rx0, fa0_, _ = run_rx(S, F, inject=inj, jam={D}, rx_kw=dict(enforce_time_safety=False), ed_pk=edpk)
        ctl("C4 same attack against a receiver WITHOUT the time-safety check", fa0_ >= 1, rx0, fa0_, "control: shows the time-safety test bites")
        for off in (-0.5, 0.5):
            rx, fa, st = run_rx(S, F, inject=inj, jam={D}, rx_kw=dict(clock_ms=int(off * P.T_ms)), ed_pk=edpk)
            rec(f"R4c same attack, receiver clock offset {off:+.1f} slot (within the configured bound)", "reject",
                set(rx.auth) - {D}, rx, fa, st, ok_extra=D not in rx.auth)
        rx, fa, st = run_rx(S, F, inject=inj, jam={D}, rx_kw=dict(clock_ms=int(-3 * P.T_ms)), ed_pk=edpk)
        ctl("C4c clock offset -3 slots (beyond the bound): the forgery is accepted", fa >= 1, rx, fa, "control: documents the sync assumption")
        # ---- R8 key derivability regression (pass-3 review: chain keys derived from the public run seed)
        fl = AT.legacy_key_forgery(S, D, 0)
        fr = list(F); fr[D] = fl
        rx, fa, st = run_rx(S, fr, ed_pk=edpk); rec("R8 forgery with chain keys recomputed from the public run seed (legacy derivation)", "reject", base - {D}, rx, fa, st)
        Sl = MO.build(pqname, mode, P, 0, key=key, ed=ed_good, legacy_public_seed=True)
        fl2 = AT.legacy_key_forgery(Sl, D, 0); frl = list(Sl.frames); frl[D] = fl2
        rxl, fal, _ = run_rx(Sl, frl, ed_pk=edpk)
        ctl("C8 the same forgery against the OLD derivation succeeds", fal >= 1, rxl, fal, "control: pass-3 behaviour (forge_chain_seed.py)")
        # ---- R6 anchor of epoch 1 corrupted / tampered fields
        a = 2                                                     # epoch 0 has no anchor in the lead modes, so epoch 1 depends on its own anchor; epoch 2 can be bridged by continuity
        fr = AT.tamper_anchor_blob(S, a, lambda b: bytes(x ^ 0xFF for x in b[:A.blob_len]) + b[A.blob_len:])
        exp = base if A.cont else base - ep(a)
        rx, fa, st = run_rx(S, fr, ed_pk=edpk); rec("R6 corrupted anchor of epoch 2" + (" (continuity covers it)" if A.cont else ""), "reject", exp, rx, fa, st)
        for field in ("ts", "d", "E", "epoch", "commit"):
            fr = AT.tamper_anchor_blob(S, a, AT.anchor_field_edit(field))
            rx, fa, st = run_rx(S, fr, ed_pk=edpk)
            rec(f"R9 anchor field '{field}' modified after signing", "reject", exp, rx, fa, st)
        # validly SIGNED but policy-violating schedules (the sender signs them): the receiver must refuse them
        for dd in (0, 40):
            P2 = plan_t(); P2.d = dd
            S2 = MO.build(pqname, mode, P2, 0, key=key, ed=ed_good)
            rx, fa, st = run_rx(S2, ed_pk=edpk); rec(f"R9 validly signed schedule with disclosure delay d={dd} (outside receiver policy)", "reject", set(), rx, fa, st)
        # ---- R9 stale anchor: replay of the epoch-3 anchor frames long after the epoch (receiver offline for the epoch)
        # (covered by R5 for the whole epoch; here only the anchor symbols)
        # ---- R7 real T6: attacker without chain keys injects a forged next-epoch commitment (continuity) and forged tags for epoch 1
        evil = random.Random(11).randbytes(MO.COMMIT_B)
        inj = {}
        for g in range(E, 2 * E):
            if S.fields.get(g):
                app, au = F[g]; b = bytearray(au)
                for a0, a1, k_ in S.fields[g]:
                    if k_ == "tag":
                        b[a0:a1] = random.Random(g).randbytes(a1 - a0)
                    if k_ == "nc":
                        b[a0:a1] = evil
                inj[g] = [(app, bytes(b))]
        rx, fa, st = run_rx(S, F, inject=inj, ed_pk=edpk)
        rec("R11 forged next-epoch commitment and forged tags injected by an attacker without chain keys", "reject", base, rx, fa, st,
            ok_extra=all(v["commit"] != evil for v in rx.sched.values()))
    return out


def job(a):
    pq, mode = a
    return [{"pq": pq, "mode": mode, **r} for r in tests_for(pq, mode)]


def main():
    import multiprocessing as mp
    outp = sys.argv[1]; quick = "--quick" in sys.argv
    jobs = [(pq, mode) for pq in RP.PQS for mode in MO.MODES
            if not (quick and "SLH" in pq and mode not in ("chain", "merkle8", "chain_lead_cont", "frag_mds_w4"))
            and not (quick and mode in ("frag_rep_w2", "frag_rep_w8", "frag_mds_w2", "frag_mds_w8", "hyb_rep_w1", "hyb_mds_w1", "merkle4", "merkle16"))]
    jobs.sort(key=lambda j: "SLH" not in j[0])
    tg = tag()
    with mp.Pool(os.cpu_count()) as pool:
        rows = [{**tg, **r} for res in pool.imap_unordered(job, jobs) for r in res]
    cols = list(dict.fromkeys(k for r in rows for k in r))
    with open(outp, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
    rej = [r for r in rows if r.get("kind") == "reject"]; ctl_ = [r for r in rows if r.get("kind") == "control"]
    bad = [r for r in rows if r.get("passed") == 0]
    print(f"negative tests: {sum(r['passed'] for r in rej)}/{len(rej)} reject tests passed; {sum(r['passed'] for r in ctl_)}/{len(ctl_)} controls passed")
    for r in bad[:25]:
        print("FAIL", r["pq"], r["mode"], r["test"], "got", r.get("got"), "expected", r.get("expected"), "fa", r.get("false_accepts"), "stale", r.get("stale_accepted"),
              "missing", r.get("missing_expected"), "unexpected", r.get("unexpected_auth"))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
