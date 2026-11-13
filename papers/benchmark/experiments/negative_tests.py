#!/usr/bin/env python3
"""Negative tests: every receiver must REJECT tampered / forged / late input, and must still authenticate the untouched messages.
negative_tests.py OUT.csv [--quick]
Plan used: SIB1 slots (293 B), M = 10 (M = 40 for SLH-DSA, which needs more slots), E = 8 windows per epoch, N = 32 messages
(smaller than the sweep so that SLH-DSA signing stays cheap); no channel loss.  Each test: expected set of authenticated messages is stated
and compared with the receiver's actual set; false accepts (accepted bytes != sent bytes) must be 0."""
import csv
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "lib"))
sys.path.insert(0, HERE)
import run_proto as RP                                   # noqa: E402
from pqsig.common import tag                             # noqa: E402
from pqsig.proto import modes as MO                      # noqa: E402
from pqsig.proto.oqs import PQ, Counters, Ed             # noqa: E402

E_, N_ = 8, 32
DSTAR = 14                                               # message index attacked


class BadEd(Ed):
    """Ed25519 signer whose signatures are over the wrong bytes (valid key, invalid signature)."""
    def sign(self, msg):
        return super().sign(msg + b"x")


def plan(pqname, quick):
    M = 40 if "SLH" in pqname else 10
    return RP.plan_for("sib1", pqname, M, N=N_, E=E_)


def frames_of_window(S, d):
    w = S.plan.off + d
    return range(w * S.plan.M, (w + 1) * S.plan.M)


def run_rx(S, frames, inject=None, **kw):
    A = S.alloc; ed = Ed() if A.hybrid else None
    rx = MO.make_rx(A, S.pk, 0, Counters(), ed.pk if ed else None, **kw)
    for g in range(len(frames)):
        for f in (inject or {}).get(g, ()):
            rx.deliver(g, *f)
        if frames[g] is not None:
            rx.deliver(g, *frames[g])
    fa = sum(1 for s, a in rx.app.items() if a != S.truth.get(s))
    return rx, fa


def flip(b, i):
    return b[:i] + bytes([b[i] ^ 0x01]) + b[i + 1:]


def tests_for(pqname, mode, quick):
    pl = plan(pqname, quick)
    out = []
    pqq = PQ(pqname); key = pqq.keypair()
    ed_good = Ed()
    S = MO.build(pqname, mode, pl, 0, key=key, ed=ed_good)
    A = S.alloc
    if not A.feasible:
        return [dict(test="all", expected="n/a", note="allocation infeasible on this plan", passed="")]
    allm = set(range(N_))
    ep = lambda e: set(range(e * E_, (e + 1) * E_))        # noqa: E731
    lay = S.layout

    def record(name, expected_set, rx, fa, extra="", control=None):
        got = set(rx.auth)
        ok = (got == expected_set) and fa == 0 and (control is None or control)
        out.append(dict(test=name, expected=f"{len(expected_set)} auth", got=len(got), missing_expected=len(expected_set - got),
                        unexpected_auth=len(got - expected_set), false_accepts=fa, rejected=rx.rejected, passed=int(ok), note=extra))

    rx, fa = run_rx(S, S.frames)
    record("T0 control: untouched stream authenticates everything", allm, rx, fa)

    # T1 tampered payload in every slot of window DSTAR
    fr = list(S.frames)
    for g in frames_of_window(S, DSTAR):
        if fr[g]:
            fr[g] = (flip(fr[g][0], 20), fr[g][1])
    rx, fa = run_rx(S, fr)
    record("T1 tampered payload (all slots of one window)", allm - {DSTAR}, rx, fa)

    # T2 tampered authenticator
    fr = list(S.frames)
    if A.kind == "frag":
        a, b = lay["sym"]
        for g in frames_of_window(S, DSTAR):
            if fr[g] and fr[g][1]:
                au = fr[g][1]; fr[g] = (fr[g][0], au[:a] + bytes(x ^ 0xFF for x in au[a:b]) + au[b:])
        rx, fa = run_rx(S, fr); record("T2 tampered signature symbols (all slots of one window)", allm - {DSTAR}, rx, fa)
    elif A.kind == "merkle":
        a, b = lay["path"]; n = A.n; bprev = DSTAR // n - 1   # window carrying the path of message DSTAR is in the NEXT batch
        tgt = ((DSTAR // n) + 1) * n + DSTAR % n
        for g in frames_of_window(S, tgt):
            if fr[g] and fr[g][1]:
                au = fr[g][1]; fr[g] = (fr[g][0], au[:a] + flip(au[a:b], 3) + au[b:])
        rx, fa = run_rx(S, fr); record("T2 tampered Merkle authentication path", allm - {DSTAR}, rx, fa)
        fr = list(S.frames); sa, sb = lay["sym"]; bb = DSTAR // n
        for d in range((bb + 1) * n, (bb + 2) * n):
            for g in frames_of_window(S, d):
                if fr[g] and fr[g][1]:
                    au = fr[g][1]; fr[g] = (fr[g][0], au[:sa] + bytes(x ^ 0xFF for x in au[sa:sb]) + au[sb:])
        rx, fa = run_rx(S, fr); record("T2b tampered batch-signature symbols (whole batch)", allm - set(range(bb * n, (bb + 1) * n)), rx, fa)
    else:
        a, b = lay["tag"]
        for g in frames_of_window(S, DSTAR):
            if fr[g] and fr[g][1]:
                au = fr[g][1]; fr[g] = (fr[g][0], au[:a] + flip(au[a:b], 2) + au[b:])
        rx, fa = run_rx(S, fr); record("T2 tampered MAC tag (all slots of one window)", allm - {DSTAR}, rx, fa)
        fr = list(S.frames); ka, kb = lay["key"]
        for g in frames_of_window(S, DSTAR + 1):
            if fr[g] and fr[g][1]:
                au = fr[g][1]; fr[g] = (fr[g][0], au[:ka] + flip(au[ka:kb], 1) + au[kb:])
        rx, fa = run_rx(S, fr)
        record("T2c tampered disclosed key (one window): bad key rejected, later keys still authenticate", allm, rx, fa,
               control=rx.rejected > 0)

    # T3 wrong signer (attacker's own PQ key and a complete valid-looking stream)
    atk_key = PQ(pqname).keypair(cache=False)
    Sa = MO.build(pqname, mode, pl, 0, key=atk_key, ed=ed_good)
    ed2 = Ed(); A2 = Sa.alloc
    rx = MO.make_rx(A2, S.pk, 0, Counters(), ed_good.pk if A2.hybrid else None)   # receiver holds the VICTIM's public key
    for g, f in enumerate(Sa.frames):
        if f:
            rx.deliver(g, *f)
    record("T3 wrong signer / wrong anchor key (attacker stream, victim public key)", set(), rx, 0)

    if A.hybrid:
        bad = BadEd()
        Sb = MO.build(pqname, mode, pl, 0, key=key, ed=bad)
        rx = MO.make_rx(Sb.alloc, S.pk, 0, Counters(), ed_good.pk)
        for g, f in enumerate(Sb.frames):
            if f:
                rx.deliver(g, *f)
        record("T7 hybrid: valid PQ half, invalid Ed25519 half", set(), rx, 0)

    if A.kind == "chain":
        # T4 forged message after key disclosure (attacker knows K_i from window i+1), honest window i jammed
        w = pl.off + DSTAR; M = pl.M
        e, i = DSTAR // E_, DSTAR % E_ + 1
        ka, kb = lay["key"]
        disclosed = next(S.frames[g][1][ka:kb] for g in range((w + 1) * M, (w + 2) * M) if S.frames[g] and S.frames[g][1])
        app_f = flip(S.truth[DSTAR], 20)
        nc = S.frames[w * M + A.usable[0]][1][lay["nc"][0]:lay["nc"][1]] if A.cont else b""
        tag_f = MO.mac_tag(disclosed, e, i, app_f, nc)
        fr = list(S.frames); inj = {}
        forged = None
        for g in frames_of_window(S, DSTAR):
            if fr[g] and fr[g][1]:
                au = fr[g][1]
                au2 = au[:lay["tag"][0]] + tag_f + au[lay["tag"][1]:]
                forged = (app_f, au2) if forged is None else forged
                fr[g] = None                                   # honest window jammed
        for g in range((w + 1) * M, (w + 2) * M):                # forged frames arrive in the window that discloses K_i
            inj.setdefault(g, []).append(forged)
        rx, fa = run_rx(S, fr, inj)
        record("T4 forged message with tag computed from the disclosed key (late delivery)", allm - {DSTAR}, rx, fa)
        rx0, fa0 = run_rx(S, fr, inj, enforce_time_safety=False)
        out.append(dict(test="T4-control: same attack against a receiver WITHOUT the time-safety check", expected="forgery accepted (shows the test bites)",
                        got=len(rx0.auth), false_accepts=fa0, passed=int(fa0 >= 1), note="control, not a receiver requirement"))
        # T4b honest frames of window DSTAR replayed 25 windows late
        fr = list(S.frames); inj = {}
        late = []
        for g in frames_of_window(S, DSTAR):
            if fr[g]:
                late.append(fr[g]); fr[g] = None
        for k_, f in enumerate(late):
            inj.setdefault((w + 25 - 8) * M + k_, []).append(f) if (w + 17) * M + k_ < len(fr) else None
        rx, fa = run_rx(S, fr, inj)
        record("T4b late-delivered (replayed) honest frames of one window", allm - {DSTAR}, rx, fa)
        # T5 wrong / corrupted anchor of epoch 1
        fr = list(S.frames); sa, sb = lay["sym"]; ao = lay["sym"][0] - 3
        for g in range(len(fr)):
            if fr[g] and len(fr[g][1]) >= sb and fr[g][1][0] == MO.T_CHAIN:
                au = fr[g][1]
                if struct.unpack(">H", au[ao:ao + 2])[0] == 1:
                    fr[g] = (fr[g][0], au[:sa] + bytes(x ^ 0xFF for x in au[sa:sb]) + au[sb:])
        rx, fa = run_rx(S, fr)
        exp = allm - ep(1) if not A.cont else allm
        record("T5 corrupted anchor of epoch 1" + (" (continuity: next commitment authenticated by the previous chain)" if A.cont else ""), exp, rx, fa)
        if A.cont:
            fr = list(S.frames); na, nb_ = lay["nc"]
            for g in range(len(fr)):
                if fr[g] and fr[g][1] and g < (pl.off + E_) * M and g >= pl.off * M:
                    au = fr[g][1]; fr[g] = (fr[g][0], au[:na] + flip(au[na:nb_], 0) + au[nb_:])
            rx, fa = run_rx(S, fr)
            record("T6 forged next-epoch commitment in epoch 0 (inside MAC input): epoch 0 rejected, epoch 1 unaffected", allm - ep(0), rx, fa)
    return out


def job(a):
    pq, mode, quick = a
    return [{"pq": pq, "mode": mode, **r} for r in tests_for(pq, mode, quick)]


def main():
    import multiprocessing as mp
    outp = sys.argv[1]; quick = "--quick" in sys.argv
    jobs = [(pq, mode, quick) for pq in RP.PQS for mode in MO.MODES
            if not (quick and "SLH" in pq and mode not in ("chain", "merkle8", "chain_lead_cont"))]   # QUICK: SLH-DSA signing is slow
    jobs.sort(key=lambda j: "SLH" not in j[0])
    tg = tag()
    with mp.Pool(os.cpu_count()) as pool:
        rows = [{**tg, **r} for res in pool.imap_unordered(job, jobs) for r in res]
    cols = list(dict.fromkeys(k for r in rows for k in r))
    with open(outp, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
    bad = [r for r in rows if r.get("passed") == 0]
    print(f"negative tests: {sum(1 for r in rows if r.get('passed') in (0, 1))} run, {len(bad)} failed")
    for r in bad[:20]:
        print("FAIL", r["pq"], r["mode"], r["test"], r.get("got"), r.get("expected"), "fa", r.get("false_accepts"))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
