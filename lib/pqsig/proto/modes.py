"""Senders and receivers for the authentication modes at the NATIVE message rate, with real byte framing (pass 4).

TRAFFIC MODEL (one slot = one application message, sent ONCE; nothing is repeated):
  slot g (period T) carries application message g (not charged to the budget) and an authentication field `auth` of at most cap(g) bytes
  (cap = the profile's auth budget B minus the digest; on C-V2X every 5th slot carries the certificate and has cap = max(0, B - P - S)).
  Messages 0..G-1 are sent in slots 0..G-1.  Statistics use the steady-state messages W0..W1-1 only (one warm-up epoch and a tail are
  excluded; bytes are counted over the slots W0..W1-1), so the lead/prelude boundary effects of pass 3 are gone.
  A message whose own slot is lost cannot be authenticated by any mode; shares are therefore reported relative to RECEIVED messages.

ALLOCATION RULE (identical for every mode):
  * each object (a message signature, a Merkle batch signature, a chain anchor) is a blob; it is coded into symbols of s bytes
    (k = ceil(blob/s) source symbols; 'mds' = systematic Reed-Solomon, n <= 255 coded symbols; 'rep' = the k raw fragments sent cyclically);
  * every symbol costs s + ov bytes (ov = 1 index byte, +1 age byte when several objects share a slot);
  * s is chosen once per (scheme, mode, budget) by erasure.choose_s (max design-point reliability at slot loss 0.2, MDS assumption);
  * n = as many symbols as the span's free bytes allow (capped at 255 for mds and at ceil(rho*k) when rho is set: chain_r2 uses rho = 2);
  * an object is infeasible when n < k; a mode is infeasible when no sampled object is feasible.
  * spans: frag/hyb = W slots starting at the message's slot; merkle = the n slots after the batch; chain = the E slots of the epoch
    (anchor of epoch e) or of the previous epoch (chain_lead*).

FRESHNESS / SECURITY (pass 4):
  * every signed object carries a timestamp (6 B ms since the Unix epoch) and the receiver rejects it when older than FRESH_SLOTS slots or from the future
    (> half a slot); frag/hyb sign (seq, ts, app); merkle signs (batch, ts, root); chain anchors sign (epoch, commitment, epoch start ts,
    schedule = slot period, E, disclosure delay d, tag/key length, continuity flag) and the receiver takes the time-safety schedule ONLY from
    a verified anchor and checks it against local policy.  Sequence numbers: replay window RW messages.
  * chain keys come from a secret (os.urandom) never visible to the receiver or attacker code path.
  * pollution: receivers keep several candidates per symbol index and decode-and-verify over subsets with at most A_MAX failed signature
    verifications per object (bounded CPU, no extra bytes).
"""
import hashlib
import hmac
import math
import os
import random
import re
import struct
import time

from .erasure import Assembler, BlobCode, choose_s
from .oqs import PQ, Ed, Counters

T0_MS = 1_700_000_000_000                                 # sender clock origin (ms), Unix-epoch ms needs 6 bytes
NONE_SEQ = 0xFFFFFFFF
NOEPOCH = 0xFFFF
T_FRAG, T_MERK, T_CHAIN = 1, 2, 3
MODES = ("frag_rep_w1", "frag_rep_w2", "frag_rep_w4", "frag_rep_w8", "frag_mds_w1", "frag_mds_w2", "frag_mds_w4", "frag_mds_w8",
         "hyb_rep_w1", "hyb_rep_w4", "hyb_mds_w1", "hyb_mds_w4", "merkle4", "merkle8", "merkle16",
         "chain", "chain_r2", "chain_lead", "chain_lead_cont")
FRAG_BEST = tuple(m for m in MODES if m.startswith("frag_"))          # the "best fragmentation mode" set (hybrids are reported separately)
PQ_IDS = ["ML-DSA-44", "Falcon-512", "Falcon-padded-512", "MAYO-1", "SNOVA_24_5_4", "OV-Is", "SLH_DSA_PURE_SHA2_128S"]
TAG_B, KEY_B, COMMIT_B, NODE_B = 16, 16, 16, 16
TS_B, SEQ_B, ED_SIG, SCHED_B = 6, 4, 64, 7
A_MAX = 8                                                  # failed signature verifications per object before the receiver gives up
RW = 64                                                    # replay window (messages)
FRESH_SLOTS = 64                                           # staleness bound of every signed timestamp (slots)
DELTA_SLOTS = 0.5                                          # receiver's configured clock-sync bound (slots)
D_MIN, D_MAX = 1, 16                                       # receiver policy for the signed disclosure delay


def alg_id(name):
    return PQ_IDS.index(name) + 1 if name in PQ_IDS else 200


def H16(*a):
    return hashlib.sha256(b"".join(a)).digest()[:NODE_B]


def Fchain(x):
    return hashlib.sha256(b"F" + x).digest()[:KEY_B]


def mac_tag(K, e, i, app, nc):
    mk = hmac.new(K, b"mac", hashlib.sha256).digest()
    return hmac.new(mk, b"T" + struct.pack(">HB", e & 0xFFFF, i) + app + nc, hashlib.sha256).digest()[:TAG_B]


def mode_kind(mode):
    if mode.startswith(("frag", "hyb")):
        return "frag"
    return "merkle" if mode.startswith("merkle") else "chain"


def ts_bytes(ms):
    return int(ms).to_bytes(TS_B, "big")


def signed_frag(alg, seq, ts, app):
    return b"M" + bytes([alg]) + struct.pack(">I", seq) + ts_bytes(ts) + app


def signed_root(alg, b, ts, root):
    return b"R" + bytes([alg]) + struct.pack(">I", b) + ts_bytes(ts) + root


def signed_anchor(alg, e32, commit, t_e0, sched):
    return b"A" + bytes([alg]) + struct.pack(">I", e32) + commit + ts_bytes(t_e0) + sched


def make_sched(plan, cont):
    return struct.pack(">HBBBBB", plan.T_ms, plan.E, plan.d, TAG_B, KEY_B, int(cont))


class Plan:
    """Channel plan: slot period T (s), budget B per slot, digest bytes, certificate cadence/capacity, epoch length E, disclosure delay d."""
    def __init__(self, T, B, digest, app_len, cert_every=0, cap_cert=0, E=20, n_meas=4, d=2, tail=40):
        self.T, self.B, self.digest, self.app_len = T, B, digest, app_len
        self.T_ms = int(round(T * 1000)); self.cap_reg = B - digest
        self.cert_every, self.cap_cert = cert_every, max(0, cap_cert)
        self.E, self.d = E, d
        self.W0, self.W1 = E, (n_meas + 1) * E               # measured messages W0..W1-1 (one warm-up epoch before, `tail` slots after)
        self.N = self.W1 - self.W0; self.G = self.W1 + tail
        self.period = cert_every or 1
        self.delta_ms = int(DELTA_SLOTS * self.T_ms); self.fresh_ms = FRESH_SLOTS * self.T_ms

    def cap(self, g):
        return self.cap_cert if self.cert_every and g % self.cert_every == 0 else self.cap_reg

    def t_start(self, g):
        return T0_MS + g * self.T_ms

    def t_arr(self, g):
        return T0_MS + (g + 1) * self.T_ms


class Alloc:
    """Allocation of (scheme, mode, plan): coding parameters per object, feasibility."""
    def __init__(self, pqname, mode, plan, sig_len, rho=None):
        self.pq, self.mode, self.plan, self.kind = pqname, mode, plan, mode_kind(mode)
        self.sig_len = sig_len
        self.hybrid = mode.startswith("hyb"); self.coder = "rep" if "_rep" in mode else "mds"
        self.n = int(mode[6:]) if self.kind == "merkle" else 1
        self.lg = int(math.log2(self.n)) if self.kind == "merkle" else 0
        self.lead = 1 if mode.startswith("chain_lead") else 0; self.cont = mode.endswith("cont")
        m = re.search(r"_w(\d+)$", mode); self.W = int(m.group(1)) if m else 1
        self.rho = 2.0 if mode == "chain_r2" else rho
        if self.kind == "frag":
            self.hdr = 3; self.ov = 2; self.mand = 3
            self.blob_len = 2 + SEQ_B + TS_B + (ED_SIG if self.hybrid else 0) + sig_len
            self.span_w = self.W
        elif self.kind == "merkle":
            self.hdr = 4; self.ov = 1; self.mand = 4 + 2 * (1 + NODE_B * self.lg)
            self.blob_len = 2 + SEQ_B + TS_B + sig_len; self.span_w = self.n
        else:
            self.hdr = 5; self.ov = 1
            self.mand = 5 + TAG_B + 3 + KEY_B + (COMMIT_B if self.cont else 0) + 3
            self.blob_len = 2 + COMMIT_B + SEQ_B + TS_B + SCHED_B + sig_len; self.span_w = plan.E
        self._p = {}
        P = plan
        if self.kind == "frag":
            sample = range(P.W0, P.W0 + 4 * P.period)
        elif self.kind == "merkle":
            sample = range(1, 1 + 5)
        else:
            sample = range(1 + self.lead, 6 + self.lead)
        samples = [(self.span_w, (lambda s, o=o: self.cap_syms(s, o))) for o in sample]
        ch = choose_s(self.blob_len, self.coder, samples, self.rho)
        if ch is None:
            self.s, self.k, self.feas_frac, self.feasible = 0, 0, 0.0, False
            self.codes = {}
            return
        self.s, self.k = ch
        self.codes = {}
        feas = [self.obj_params(o)[1] >= self.k for o in sample]
        self.feas_frac = sum(feas) / len(feas)
        self.feasible = self.feas_frac > 0
        self.n_typ = max(self.obj_params(o)[0] for o in sample)

    # ---- geometry
    def slot_room(self, g):
        c = self.plan.cap(g)
        if self.kind == "frag":
            r = c - self.mand
        else:
            r = c - self.mand if c >= self.mand else -1
        return r

    def span(self, oid):
        P = self.plan
        if self.kind == "frag":
            return range(oid, oid + self.W)
        if self.kind == "merkle":
            return range((oid + 1) * self.n, (oid + 2) * self.n)
        return range((oid - self.lead) * P.E, (oid - self.lead + 1) * P.E)

    def cap_syms(self, s, oid):
        if self.kind == "frag":
            tot = sum(max(0, self.slot_room(g)) for g in self.span(oid)) / self.W
            return int(tot // (s + self.ov))
        return sum(max(0, self.slot_room(g)) // (s + self.ov) for g in self.span(oid))

    def obj_params(self, oid):
        """(n_distinct, n_send) for object oid (deterministic from the plan; sender and receiver both compute it)."""
        if oid in self._p:
            return self._p[oid]
        if not self.s:
            return (0, 0)
        cap = self.cap_syms(self.s, oid); k = self.k
        if self.coder == "mds":
            cap = min(cap, 255)
        if self.rho:
            cap = min(cap, math.ceil(self.rho * k))
        if cap < k:
            r = (0, 0)
        elif self.coder == "mds":
            r = (cap, cap)
        else:
            r = (k, cap)
        self._p[oid] = r
        return r

    def code(self, oid):
        n = self.obj_params(oid)[0]
        if n not in self.codes:
            self.codes[n] = BlobCode(self.coder, self.blob_len, self.s, n)
        return self.codes[n]

    def row(self):
        P = self.plan
        nd, ns = self.obj_params({"frag": P.W0, "merkle": 1, "chain": 1 + self.lead}[self.kind]) if self.s else (0, 0)
        return dict(pq=self.pq, mode=self.mode, B_slot=P.B, cap_regular=P.cap_reg, cap_cert_slot=P.cap_cert, cert_every=P.cert_every,
                    blob_B=self.blob_len, symbol_B=self.s, k=self.k, n_distinct_typ=nd, n_send_typ=ns,
                    code_rate=(self.k / nd if nd else float("nan")), redundancy=(ns / self.k if self.k else float("nan")),
                    feasible_frac=self.feas_frac, feasible=int(self.feasible), span_slots=self.span_w, rho=self.rho or "",
                    coder=self.coder, lead=self.lead, continuity=int(self.cont))


class Stream:
    def __init__(self, alloc):
        self.alloc = alloc; self.plan = alloc.plan
        self.frames = []; self.fields = {}; self.truth = {}; self.air = [0] * alloc.plan.G
        self.tx_cpu_ns = 0; self.tx_sign_ns = 0; self.n_sign = 0; self.cpu_msgs = 0
        self.build_seed = 0; self.pk = None; self.chains = None

    def air_bytes(self, lo=None, hi=None):
        lo = self.plan.W0 if lo is None else lo; hi = self.plan.W1 if hi is None else hi
        return sum(self.air[lo:hi])


class FB:
    """frame builder that remembers where the attacker-relevant payload fields are"""
    def __init__(self):
        self.b = bytearray(); self.f = []

    def pack(self, fmt, *a):
        self.b += struct.pack(fmt, *a)

    def raw(self, data, kind=None):
        if kind:
            self.f.append((len(self.b), len(self.b) + len(data), kind))
        self.b += data


def place_all(reqs, free, G, cost):
    """Two-pass symbol placement.  reqs = [(oid, j, start, W)] in priority order.  Pass 1 puts symbol j of every object in its preferred slot
    start + (j mod W) if it has room; pass 2 spills the leftovers into the other slots of the span.  Returns per-slot lists of (oid, j)."""
    out = [[] for _ in range(G)]; left = []
    for oid, j, st, W in reqs:
        t = st + (j % W)
        if 0 <= t < G and free[t] >= cost and len(out[t]) < 255:
            free[t] -= cost; out[t].append((oid, j))
        else:
            left.append((oid, j, st, W))
    for oid, j, st, W in left:
        for off in range(1, W):
            t = st + ((j + off) % W)
            if 0 <= t < G and free[t] >= cost and len(out[t]) < 255:
                free[t] -= cost; out[t].append((oid, j)); break
    return out


def make_app(plan, build_seed, seq):
    r = random.Random(build_seed * 1000003 + seq)
    return struct.pack(">I", seq) + r.randbytes(plan.app_len - 4)


def chain_seed_legacy(build_seed, e):
    """CONTROL ONLY: the pass-3 derivation from the public run seed (forgeable); used by the regression test to show the forgery worked."""
    return hashlib.sha256(b"".join([b"seed", struct.pack(">II", build_seed, e)])).digest()[:KEY_B]


def chain_seed_secret(secret, e):
    return hmac.new(secret, b"chain" + struct.pack(">I", e), hashlib.sha256).digest()[:KEY_B]


def build(pqname, mode, plan, build_seed=0, key=None, ed=None, chain_secret=None, legacy_public_seed=False, rho=None):
    """Sender: produce the whole frame stream (real signatures/MACs/erasure coding). CPU time is recorded."""
    ctr = Counters(); pq = PQ(pqname, ctr)
    pk, sk = key or pq.keypair()
    A = Alloc(pqname, mode, plan, pq.sig_len, rho); S = Stream(A); S.build_seed = build_seed; S.pk = pk
    alg = alg_id(pqname); P = plan; G = P.G; E = P.E
    edk = (ed or Ed(ctr)) if A.hybrid else None
    if edk is not None:
        edk.ctr = ctr
    t0 = time.thread_time_ns()
    apps = [make_app(P, build_seed, g) for g in range(G)]
    S.truth = {g: apps[g] for g in range(G)}
    S.frames = [(apps[g], b"") for g in range(G)]
    if not A.feasible:
        for g in range(3):
            pq.sign(signed_frag(alg, g, P.t_start(g), apps[g]), sk, cache=False)
        S.cpu_msgs = 3
        S.tx_cpu_ns = (time.thread_time_ns() - t0 - ctr.real_sign_ns) + ctr.sign_ns; S.tx_sign_ns = ctr.sign_ns; S.n_sign = ctr.n_sign
        return S
    S.cpu_msgs = G
    s, k = A.s, A.k

    def put(g, auth, fields):
        if len(auth) > P.cap(g):
            raise AssertionError(f"auth field {len(auth)} B exceeds slot capacity {P.cap(g)} B (slot {g})")
        S.frames[g] = (apps[g], auth); S.fields[g] = fields; S.air[g] = len(auth)

    if A.kind == "frag":
        free = [max(0, A.slot_room(g)) for g in range(G)]
        reqs = []; tab = {}
        for d in range(G):
            nd, ns = A.obj_params(d)
            if ns < k:
                continue
            ts = P.t_start(d)
            sig = pq.sign(signed_frag(alg, d, ts, apps[d]), sk)
            body = (edk.sign(signed_frag(alg, d, ts, apps[d])) if A.hybrid else b"") + sig
            blob = struct.pack(">HI", len(sig), d) + ts_bytes(ts) + body
            tab[d] = (nd, A.code(d).encode(blob))
            reqs += [(d, j, d, A.W) for j in range(ns)]
        slot_syms = place_all(reqs, free, G, s + A.ov)
        for t in range(G):
            if slot_syms[t]:
                fb = FB(); fb.pack(">BBB", T_FRAG, alg, len(slot_syms[t]))
                for d, j in sorted(slot_syms[t]):
                    nd, syms = tab[d]; idx = j % nd
                    fb.pack(">BB", t - d, idx); fb.raw(syms[idx], "sym")
                put(t, bytes(fb.b), fb.f)
    elif A.kind == "merkle":
        n, lg = A.n, A.lg; nb = G // n
        free = [max(0, A.slot_room(g)) if A.slot_room(g) >= 0 else -1 for g in range(G)]
        paths_of = {}; reqs = []; tab = {}
        for b in range(nb):
            leaves = [H16(b"\x00", struct.pack(">I", b * n + j), apps[b * n + j]) for j in range(n)]
            lv = [leaves]
            while len(lv[-1]) > 1:
                x = lv[-1]; lv.append([H16(b"\x01", x[2 * t], x[2 * t + 1]) for t in range(len(x) // 2)])
            root = lv[-1][0]; ts = P.t_start(b * n)
            sig = pq.sign(signed_root(alg, b, ts, root), sk)
            blob = struct.pack(">HI", len(sig), b) + ts_bytes(ts) + sig
            for j in range(n):
                p = []; idx = j
                for lvl in range(lg):
                    p.append(lv[lvl][idx ^ 1]); idx >>= 1
                paths_of[b * n + j] = b"".join(p)
            nd, ns = A.obj_params(b)
            if ns < k:
                continue
            tab[b] = (nd, A.code(b).encode(blob))
            reqs += [(b, j, (b + 1) * n, n) for j in range(ns)]
        slot_syms = place_all(reqs, free, G, s + A.ov)
        for t in range(n, G):
            b = t // n - 1
            if b >= nb or P.cap(t) < A.mand:
                continue
            jj = t % n
            fb = FB(); fb.pack(">BBBB", T_MERK, alg, 2, len(slot_syms[t]))
            for leaf in (jj, (jj + n // 2) % n):
                fb.pack(">B", t - (b * n + leaf)); fb.raw(paths_of[b * n + leaf], "path")
            for bb, j in slot_syms[t]:
                nd, syms = tab[bb]; idx = j % nd
                fb.pack(">B", idx); fb.raw(syms[idx], "sym")
            put(t, bytes(fb.b), fb.f)
    else:
        Ne = G // E; L = A.lead; cont = A.cont
        secret = chain_secret if chain_secret is not None else os.urandom(32)
        S.chains = chains = []
        for e in range(Ne + 1):
            K = [None] * (E + 1)
            K[E] = chain_seed_legacy(build_seed, e) if legacy_public_seed else chain_seed_secret(secret, e)
            for i in range(E, 0, -1):
                K[i - 1] = Fchain(K[i])
            chains.append(K)
        sched = make_sched(P, cont)
        anchors = {}
        for a in range(Ne):
            t_e0 = P.t_start(a * E)
            sig = pq.sign(signed_anchor(alg, a, chains[a][0], t_e0, sched), sk)
            blob = struct.pack(">H", len(sig)) + chains[a][0] + struct.pack(">I", a) + ts_bytes(t_e0) + sched + sig
            anchors[a] = blob
        free = [A.slot_room(g) if A.slot_room(g) >= 0 else -1 for g in range(G)]
        reqs = []; tab = {}
        for a in range(Ne):
            if a - L < 0:
                continue
            nd, ns = A.obj_params(a)
            if ns < k:
                continue
            tab[a] = (nd, A.code(a).encode(anchors[a]))
            reqs += [(a, j, (a - L) * E, E) for j in range(ns)]
        slot_syms = place_all(reqs, free, G, s + A.ov)
        for g in range(G):
            if P.cap(g) < A.mand:
                continue
            e, i = g // E, g % E + 1
            nc = chains[e + 1][0] if cont else b""
            tg = mac_tag(chains[e][i], e, i, apps[g], nc)
            m = g - P.d
            fb = FB(); fb.pack(">BBHB", T_CHAIN, alg, e & 0xFFFF, i); fb.raw(tg, "tag")
            if m >= 0:
                ke, ki = m // E, m % E + 1; fb.pack(">HB", ke & 0xFFFF, ki); fb.raw(chains[ke][ki], "key")
            else:
                fb.pack(">HB", NOEPOCH, 0); fb.raw(bytes(KEY_B), "key")
            if cont:
                fb.raw(nc, "nc")
            if slot_syms[g]:
                a = slot_syms[g][0][0]
                fb.pack(">HB", a & 0xFFFF, len(slot_syms[g]))
                for _, j in slot_syms[g]:
                    nd, syms = tab[a]; idx = j % nd
                    fb.pack(">B", idx); fb.raw(syms[idx], "sym")
            else:
                fb.pack(">HB", NOEPOCH, 0)
            put(g, bytes(fb.b), fb.f)
    S.tx_cpu_ns = (time.thread_time_ns() - t0 - ctr.real_sign_ns) + ctr.sign_ns
    S.tx_sign_ns = ctr.sign_ns; S.n_sign = ctr.n_sign
    return S


# ----------------------------------------------------------------------------- receivers
class Rx:
    """Receiver base. A message counts as authenticated only when a verification of the received bytes succeeded and the
    freshness / replay checks passed.  clock_ms = receiver clock offset (positive = receiver clock ahead)."""
    def __init__(self, alloc, pk, join=0, ctr=None, ed_pk=None, clock_ms=0, enforce_fresh=True):
        self.A = alloc; self.plan = alloc.plan; self.pk = pk; self.join = join
        self.ctr = ctr or Counters(); self.pq = PQ(alloc.pq, self.ctr); self.alg = alg_id(alloc.pq)
        self.ed = Ed(self.ctr) if alloc.hybrid else None; self.ed_pk = ed_pk
        self.clock_ms = clock_ms; self.enf_fresh = enforce_fresh
        self.auth = {}; self.app = {}; self.apps = {}; self.hi = -1
        self.rejected = 0; self.stale_rej = 0; self.replay_rej = 0; self.t = 0; self.g = 0

    def deliver(self, g, app, auth):
        if g < self.join:
            return
        self.g = g; self.t = self.plan.t_arr(g) + self.clock_ms
        if len(app) >= 4:
            self.on_frame(g, app, auth)

    def fresh(self, t_msg):
        if not self.enf_fresh:
            return True
        return self.t - t_msg <= self.plan.fresh_ms and t_msg <= self.t + self.plan.delta_ms

    def _accept(self, seq, app, g):
        if seq in self.auth:
            return False
        if self.enf_fresh and seq + RW <= self.hi:
            self.replay_rej += 1
            return False
        self.auth[seq] = g; self.app[seq] = app; self.hi = max(self.hi, seq)
        return True

    def _copy(self, seq, app):
        """remember an application-message candidate for seq; returns True when it is new"""
        c = self.apps.setdefault(seq, [])
        if app not in c and len(c) < 4:
            c.append(app)
            return True
        return False

    @staticmethod
    def _seq(app):
        return struct.unpack(">I", app[:4])[0]


class FragRx(Rx):
    def __init__(self, *a, **k):
        super().__init__(*a, **k); self.asm = {}

    def on_frame(self, g, app, auth):
        A = self.A; s = A.s
        seq_f = self._seq(app); new_app = self._copy(seq_f, app)
        touched = set()
        if new_app and seq_f in self.asm and seq_f not in self.auth:
            touched.add(seq_f)                                      # the message arrived after its signature symbols (reordering / replay)
        if len(auth) < 3 or auth[0] != T_FRAG or auth[1] != self.alg:
            for obj in touched:
                self._try(obj, g)
            return
        ns = auth[2]; o = 3
        for _ in range(ns):
            if o + 2 + s > len(auth):
                break
            age, idx = auth[o], auth[o + 1]; data = auth[o + 2:o + 2 + s]; o += 2 + s
            obj = seq_f - age
            if obj < 0 or obj >= self.plan.G or obj in self.auth:
                continue
            a = self.asm.get(obj)
            if a is None:
                nd = A.obj_params(obj)[0]
                if nd < A.k:
                    continue
                a = self.asm[obj] = Assembler(A.code(obj), seed=obj)
            if a.add(idx, data):
                touched.add(obj)
        for obj in sorted(touched):
            self._try(obj, g)

    def _try(self, obj, g):
        a = self.asm[obj]; apps = self.apps.get(obj)
        if not apps or a.dead:
            return
        for blob, _ in a.blobs():
            r = self._verify(obj, blob, apps, g)
            if r is True or r == "stale":
                a.dead = True; break
            if r is False:
                a.fails += 1; self.rejected += 1
                if a.fails >= A_MAX:
                    a.dead = True; break

    def _verify(self, obj, blob, apps, g):
        A = self.A
        n = struct.unpack(">H", blob[:2])[0]; sq = struct.unpack(">I", blob[2:6])[0]; ts = int.from_bytes(blob[6:6 + TS_B], "big")
        off = 6 + TS_B
        if n == 0 or n > A.sig_len or sq != obj:
            return None
        if not self.fresh(ts):
            self.stale_rej += 1
            return "stale"
        ed_sig = None
        if A.hybrid:
            ed_sig = blob[off:off + ED_SIG]; off += ED_SIG
        sig = blob[off:off + n]
        for c in apps:
            m = signed_frag(self.alg, obj, ts, c)
            ok = self.pq.verify(m, sig, self.pk)
            if ok and A.hybrid:
                ok = self.ed.verify(m, ed_sig, self.ed_pk)
            if ok:
                self._accept(obj, c, g); return True
        return False


class MerkleRx(Rx):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.asm = {}; self.paths = {}; self.root = {}; self.bfail = {}

    def _root(self, leaf_seq, copy, path):
        h = H16(b"\x00", struct.pack(">I", leaf_seq), copy); idx = leaf_seq % self.A.n
        for lvl in range(len(path) // NODE_B):
            sib = path[NODE_B * lvl:NODE_B * lvl + NODE_B]
            h = H16(b"\x01", sib, h) if idx & 1 else H16(b"\x01", h, sib)
            idx >>= 1
        return h

    def on_frame(self, g, app, auth):
        A = self.A; n = A.n; s = A.s; lg = A.lg
        seq_f = self._seq(app); new_app = self._copy(seq_f, app)
        if new_app and seq_f in self.paths and seq_f // n in self.asm:
            self._try(seq_f // n, g)                                # the message arrived after its path / batch signature
        if len(auth) < A.mand or auth[0] != T_MERK or auth[1] != self.alg:
            return
        npth, nsym = auth[2], auth[3]; o = 4; b = seq_f // n - 1
        if b < 0 or b >= self.plan.G // n + 2:
            return
        touched = set()
        for _ in range(min(npth, 4)):
            if o + 1 + NODE_B * lg > len(auth):
                return
            lage = auth[o]; path = auth[o + 1:o + 1 + NODE_B * lg]; o += 1 + NODE_B * lg
            ls = seq_f - lage
            if ls // n != b or ls < 0:
                continue
            c = self.paths.setdefault(ls, [])
            if path not in c and len(c) < 3:
                c.append(path); touched.add(b)
        if b in self.root and b not in touched and nsym == 0:
            return
        a = self.asm.get(b)
        if a is None:
            if A.obj_params(b)[0] < A.k:
                a = None
            else:
                a = self.asm[b] = Assembler(A.code(b), seed=b)
        for _ in range(nsym):
            if o + 1 + s > len(auth):
                break
            idx = auth[o]; data = auth[o + 1:o + 1 + s]; o += 1 + s
            if a is not None and b not in self.root and a.add(idx, data):
                touched.add(b)
        if touched:
            self._try(b, g)

    def _pending(self, b):
        n = self.A.n; out = []
        for j in range(n):
            ls = b * n + j
            if ls in self.auth or ls not in self.paths or ls not in self.apps:
                continue
            out.append(ls)
        return out

    def _try(self, b, g):
        n = self.A.n
        pend = self._pending(b)
        if b in self.root:
            root, ts = self.root[b]
            for ls in pend:
                if not self.fresh(ts + (ls - b * n) * self.plan.T_ms):     # a verified root does not make a stale (replayed) leaf fresh
                    continue
                for c in self.apps[ls]:
                    if any(self._root(ls, c, p) == root for p in self.paths[ls]):
                        self._accept(ls, c, g); break
            return
        a = self.asm.get(b)
        if a is None or a.dead or not pend:
            return
        cands = {}
        for ls in pend:
            for c in self.apps[ls]:
                for p in self.paths[ls]:
                    cands.setdefault(self._root(ls, c, p), []).append((ls, c))
        for blob, _ in a.blobs():
            nn = struct.unpack(">H", blob[:2])[0]; bb = struct.unpack(">I", blob[2:6])[0]; ts = int.from_bytes(blob[6:6 + TS_B], "big")
            if nn == 0 or nn > self.A.sig_len or bb != b:
                continue
            if not self.fresh(ts):
                self.stale_rej += 1; a.dead = True; return
            sig = blob[6 + TS_B:6 + TS_B + nn]
            for root, items in list(cands.items())[:6]:
                if self.bfail.get((b, root, sig)):
                    continue
                if self.pq.verify(signed_root(self.alg, b, ts, root), sig, self.pk):
                    self.root[b] = (root, ts)
                    for ls, c in items:
                        self._accept(ls, c, g)
                    self._try(b, g); return
                self.bfail[(b, root, sig)] = 1; self.rejected += 1; a.fails += 1
                if a.fails >= 2 * A_MAX:
                    a.dead = True; return


class ChainRx(Rx):
    def __init__(self, *a, enforce_time_safety=True, **k):
        super().__init__(*a, **k)
        self.enforce = enforce_time_safety
        self.sched = {}; self.anc = {}; self.kst = {}; self.stash = {}; self.pend = {}; self.anc_dead = set()

    def on_frame(self, g, app, auth):
        A = self.A; pl = self.plan
        if len(auth) < A.mand or auth[0] != T_CHAIN or auth[1] != self.alg:
            return
        e, i = struct.unpack(">HB", auth[2:5]); o = 5
        tag = auth[o:o + TAG_B]; o += TAG_B
        ke, ki = struct.unpack(">HB", auth[o:o + 3]); o += 3
        key = auth[o:o + KEY_B]; o += KEY_B
        nc = b""
        if A.cont:
            nc = auth[o:o + COMMIT_B]; o += COMMIT_B
        ae, nsym = struct.unpack(">HB", auth[o:o + 3]); o += 3
        seq = self._seq(app); self._copy(seq, app)
        if ae != NOEPOCH and nsym:
            syms = []
            for _ in range(nsym):
                if o + 1 + A.s > len(auth):
                    break
                syms.append((auth[o], auth[o + 1:o + 1 + A.s])); o += 1 + A.s
            self._anchor(ae, syms, g)
        if ke != NOEPOCH:
            self._key(ke, ki, key, g)
        if e != NOEPOCH and seq not in self.auth and 1 <= i <= pl.E:
            lst = self.pend.setdefault((e, i), [])
            item = (app, tag, nc, self.t)
            if not any(x[:3] == item[:3] for x in lst) and len(lst) < 4:
                lst.append(item)
            self._resolve(e, g)

    # ---- anchors
    def _anchor(self, ae, syms, g):
        A = self.A
        if ae in self.sched or ae in self.anc_dead:
            return
        a = self.anc.get(ae)
        if a is None:
            if not A.s or A.k == 0:
                return
            # 16-bit epoch ids wrap, so the coding parameters come from a canonical epoch (the pattern is periodic for epochs >= 1)
            a = self.anc[ae] = Assembler(A.code(1 + A.lead), seed=ae)
        new = False
        for idx, data in syms:
            new |= a.add(idx, data)
        if not new:
            return
        for blob, _ in a.blobs():
            r = self._verify_anchor(ae, blob, g)
            if r is True:
                return
            if r == "stale":
                self.anc_dead.add(ae); return
            if r is False:
                a.fails += 1; self.rejected += 1
                if a.fails >= A_MAX:
                    self.anc_dead.add(ae); return

    def _verify_anchor(self, ae, blob, g):
        A = self.A; pl = self.plan
        n = struct.unpack(">H", blob[:2])[0]
        if n == 0 or n > A.sig_len:
            return None
        commit = blob[2:2 + COMMIT_B]; o = 2 + COMMIT_B
        e32 = struct.unpack(">I", blob[o:o + 4])[0]; o += 4
        t_e0 = int.from_bytes(blob[o:o + TS_B], "big"); o += TS_B
        sched = blob[o:o + SCHED_B]; o += SCHED_B
        sig = blob[o:o + n]
        if e32 & 0xFFFF != ae:
            return None
        T_ms, E, d, tl, kl, cont = struct.unpack(">HBBBBB", sched)
        if T_ms != pl.T_ms or E != pl.E or not (D_MIN <= d <= D_MAX) or tl != TAG_B or kl != KEY_B or cont != int(A.cont):
            self.rejected += 1
            return None                                            # signed schedule outside local policy
        if self.enf_fresh and self.t < t_e0 - E * T_ms - pl.delta_ms:
            return None                                             # too early for this epoch's anchor: ignore, later symbols retry
        if self.enf_fresh and self.t > t_e0 + E * T_ms + pl.fresh_ms:
            self.stale_rej += 1
            return "stale"
        if self.pq.verify(signed_anchor(self.alg, e32, commit, t_e0, sched), sig, self.pk):
            self._set_commit(ae, commit, dict(t_e0=t_e0, T=T_ms, E=E, d=d), g)
            return True
        return False

    def _set_commit(self, e, commit, sch, g):
        if e in self.sched:
            return
        self.sched[e] = dict(sch, commit=commit); self.kst[e] = (0, commit)
        if e in self.stash:
            ki, key = self.stash.pop(e); self._key(e, ki, key, g)
        self._resolve(e, g)

    # ---- keys and tags
    def _key(self, ke, ki, key, g):
        if ki > self.plan.E or ki < 1:
            return
        if ke not in self.sched:
            if ki > self.stash.get(ke, (0, None))[0]:
                self.stash[ke] = (ki, key)
            return
        i0, k0 = self.kst[ke]
        if ki <= i0:
            return
        x = key
        for _ in range(ki - i0):
            x = Fchain(x)
        if x == k0:
            self.kst[ke] = (ki, key); self._resolve(ke, g)
        else:
            self.rejected += 1

    def _resolve(self, e, g):
        if e not in self.sched:
            return
        sch = self.sched[e]; idx, key = self.kst[e]
        for i in range(1, idx + 1):
            lst = self.pend.get((e, i))
            if not lst:
                continue
            Ki = key
            for _ in range(idx - i):
                Ki = Fchain(Ki)
            t_start = sch["t_e0"] + (i - 1) * sch["T"]; t_rel = t_start + sch["d"] * sch["T"]
            for item in list(lst):
                app, tag, nc, t_arr = item
                seq = self._seq(app)
                if seq in self.auth:
                    lst.remove(item); continue
                if self.enforce and t_arr + self.plan.delta_ms > t_rel:      # time safety: must arrive before the key can have been released
                    self.rejected += 1; lst.remove(item); continue
                if hmac.compare_digest(mac_tag(Ki, e, i, app, nc), tag):
                    if self.enf_fresh and self.t - t_start > self.plan.fresh_ms:
                        self.stale_rej += 1; lst.remove(item); continue
                    if self._accept(seq, app, g):
                        if self.A.cont and nc and (e + 1) not in self.sched:
                            self._set_commit(e + 1, nc, dict(t_e0=sch["t_e0"] + sch["E"] * sch["T"], T=sch["T"], E=sch["E"], d=sch["d"]), g)
                    lst.clear(); break
                else:
                    self.rejected += 1; lst.remove(item)


def make_rx(alloc, pk, join=0, ctr=None, ed_pk=None, **kw):
    cls = {"frag": FragRx, "merkle": MerkleRx, "chain": ChainRx}[alloc.kind]
    if alloc.kind != "chain":
        kw.pop("enforce_time_safety", None)
    return cls(alloc, pk, join=join, ctr=ctr, ed_pk=ed_pk, **kw)
