"""Senders and receivers for the authentication modes, with real byte framing.

Slot model: time is divided into slots of Plan.T seconds; each slot carries ONE frame = (app, auth). `app` is the application
message (SIB1 content / BSM core), repeated in every slot of its window and NOT charged to the budget; `auth` is the
authentication field and must be <= Plan.cap(position) bytes (enforced). A window = M consecutive slots = one application
message (equal channel budget for every mode).  Stream layout: E prelude windows (used only by chain_lead*), N data
windows, then trailing windows (flush of the last Merkle batch / last disclosed key); every mode uses the same fixed
slot count G = (N + 2E) * M so seeded loss masks are paired across modes.

ALLOCATION RULE (identical for all modes, no hand tuning):
  R1 every slot's auth field = header + mode control field + one symbol of the mode's heavy blob, truncated to nothing else;
  R2 symbol room = cap_regular - header - control;  k = ceil(blob / room) source symbols of s = ceil(blob / k) bytes;
     frame length F = header + control + s;
  R3 slot position j is USABLE iff cap(j) >= F (on C-V2X the slot carrying the full certificate usually is not);
  R4 coded modes send n_sym = min(usable slots in the blob's span, 255) MDS symbols round robin over the usable slots
     of the span; repetition modes send the k raw symbols round robin; span = 1 window (frag), n windows (Merkle),
     E windows (chain anchor);
  R5 a mode is infeasible when its span has fewer usable slots than k.
"""
import hashlib
import hmac
import math
import random
import struct
import time

from .erasure import BlobCode
from .oqs import PQ, Ed, Counters

NONE_SEQ = 0xFFFFFFFF
NOEPOCH = 0xFFFF
T_FRAG, T_MERK, T_CHAIN = 1, 2, 3
MODES = ("frag_rep", "frag_mds", "hyb_rep", "hyb_mds", "merkle4", "merkle8", "merkle16",
         "chain", "chain_lead", "chain_lead_cont")
PQ_IDS = ["ML-DSA-44", "Falcon-512", "Falcon-padded-512", "MAYO-1", "SNOVA_24_5_4", "OV-Is", "SLH_DSA_PURE_SHA2_128S"]
TAG_B, KEY_B, COMMIT_B, TS_B = 16, 16, 16, 4          # chain field sizes (profiles.yaml common.chain)
ED_SIG = 64


def alg_id(name):
    return PQ_IDS.index(name) + 1 if name in PQ_IDS else 200


def H(*a):
    return hashlib.sha256(b"".join(a)).digest()


def Fchain(x):
    return hashlib.sha256(b"F" + x).digest()[:KEY_B]


def mac_tag(K, e, i, app, nc):
    mk = hmac.new(K, b"mac", hashlib.sha256).digest()
    return hmac.new(mk, b"T" + struct.pack(">HB", e, i) + app + nc, hashlib.sha256).digest()[:TAG_B]


def mode_kind(mode):
    if mode.startswith(("frag", "hyb")):
        return "frag"
    return "merkle" if mode.startswith("merkle") else "chain"


class Plan:
    """Channel plan: slot period T, per-slot auth capacity (regular / certificate-bearing slot), window size M."""
    def __init__(self, T, cap_reg, app_len, M, cert_every=0, cap_cert=0, E=20, N=80):
        if cert_every and M % cert_every:
            raise ValueError("M must be a multiple of the certificate cadence")
        self.T, self.cap_reg, self.app_len, self.M = T, cap_reg, app_len, M
        self.cert_every, self.cap_cert, self.E, self.N = cert_every, cap_cert, E, N
        self.off = E                                   # prelude windows
        self.G = (N + E + max(E, 16)) * M            # slots in every stream (trailing >= largest Merkle batch)

    def cap(self, j):
        return self.cap_cert if self.cert_every and j % self.cert_every == 0 else self.cap_reg

    def usable(self, F):
        return [j for j in range(self.M) if self.cap(j) >= F]

    def t_end(self, g):                                # arrival time (s) of slot g's frame = end of the slot
        return (g + 1) * self.T


class Alloc:
    """Result of the allocation rule for (pq, mode, plan)."""
    def __init__(self, pqname, mode, plan, sig_decl):
        self.pq, self.mode, self.plan, self.kind = pqname, mode, plan, mode_kind(mode)
        self.n = int(mode[6:]) if self.kind == "merkle" else 1
        self.cont = mode.endswith("cont"); self.lead = 1 if mode.startswith("chain_lead") else 0
        self.hybrid = mode.startswith("hyb")
        self.coder = "rep" if mode.endswith("rep") else "mds"
        E = plan.E
        if self.kind == "frag":
            self.hdr, self.control = 3, 0
            self.blob_len = 2 + sig_decl + (ED_SIG if self.hybrid else 0); span_w = 1
        elif self.kind == "merkle":
            self.hdr = 1 + 1 + 2 + 1 + 1                       # type alg batch leaf symidx
            self.control = 32 * int(math.log2(self.n))         # authentication path
            self.blob_len = 2 + sig_decl; span_w = self.n
        else:
            # type alg e i tag ke ki key [nc] ae aidx
            self.hdr = 2 + 2 + 1 + 2 + 1 + 2 + 1
            self.control = TAG_B + KEY_B + (COMMIT_B if self.cont else 0)
            self.blob_len = 2 + COMMIT_B + TS_B + sig_decl; span_w = E
        self.room = plan.cap_reg - self.hdr - self.control
        if self.kind == "frag" and self.coder == "rep":
            pass
        self.k = math.ceil(self.blob_len / self.room) if self.room > 0 else 10 ** 9
        self.s = math.ceil(self.blob_len / self.k) if self.room > 0 else 0
        self.F = self.hdr + self.control + self.s
        self.usable = plan.usable(self.F) if self.room > 0 else []
        self.u = len(self.usable); self.span_slots = self.u * span_w
        self.code = BlobCode(self.coder, self.blob_len, max(self.room, 0), self.span_slots)
        self.n_sym = self.code.n_sym
        self.feasible = bool(self.code.feasible and self.u > 0)
        self.rate = self.k / self.n_sym if self.n_sym else float("nan")

    def row(self):
        return dict(pq=self.pq, mode=self.mode, M=self.plan.M, cap_regular=self.plan.cap_reg, cap_cert_slot=self.plan.cap_cert,
                    cert_every=self.plan.cert_every, header_B=self.hdr, control_B=self.control, blob_B=self.blob_len,
                    symbol_B=self.s, frame_auth_B=self.F, k=self.k, n_sym=self.n_sym, code_rate=self.rate,
                    usable_slots_per_window=self.u, span_windows=(self.n if self.kind == "merkle" else self.plan.E if self.kind == "chain" else 1),
                    coder=self.coder, lead=self.lead, continuity=int(self.cont), feasible=int(self.feasible))


class Stream:
    def __init__(self, alloc):
        self.alloc = alloc; self.plan = alloc.plan
        self.frames = [None] * alloc.plan.G
        self.truth = {}; self.layout = {}; self.air_bytes = 0; self.n_frames = 0
        self.tx_cpu_ns = 0; self.tx_sign_ns = 0; self.n_sign = 0; self.build_seed = 0

    def put(self, g, app, auth):
        cap = self.plan.cap(g % self.plan.M)
        if len(auth) > cap:
            raise AssertionError(f"auth field {len(auth)} B exceeds slot capacity {cap} B")
        self.frames[g] = (app, auth); self.air_bytes += len(auth); self.n_frames += 1


def make_app(plan, build_seed, seq):
    if seq == NONE_SEQ:
        return struct.pack(">I", NONE_SEQ) + bytes(plan.app_len - 4)
    r = random.Random(build_seed * 1000003 + seq)
    return struct.pack(">I", seq) + r.randbytes(plan.app_len - 4)


def _signed(alg, app):
    return b"M" + bytes([alg]) + app


def build(pqname, mode, plan, build_seed=0, key=None, ed=None):
    """Sender: produce the whole frame stream (real signatures/MACs/erasure coding). CPU time is recorded."""
    ctr = Counters(); pq = PQ(pqname, ctr)
    pk, sk = key or pq.keypair()
    A = Alloc(pqname, mode, plan, pq.sig_len); S = Stream(A); S.build_seed = build_seed; S.pk = pk
    alg = alg_id(pqname); N, E, M, off = plan.N, plan.E, plan.M, plan.off
    edk = (ed or Ed(ctr)) if A.hybrid else None
    if edk is not None:
        edk.ctr = ctr
    t0 = time.thread_time_ns()
    apps = [make_app(plan, build_seed, d) for d in range(N)]
    S.truth = {d: apps[d] for d in range(N)}
    dummy = make_app(plan, build_seed, NONE_SEQ)
    if not A.feasible:
        # still measure sender cost on a few messages (cannot be transmitted at all)
        for d in range(min(N, 3)):
            pq.sign(_signed(alg, apps[d]), sk)
        S.tx_cpu_ns = time.thread_time_ns() - t0; S.tx_sign_ns = ctr.sign_ns; S.n_sign = ctr.n_sign
        S.cpu_msgs = min(N, 3)
        return S
    S.cpu_msgs = N
    us = A.usable
    if A.kind == "frag":
        S.layout = dict(sym=(3, 3 + A.s))
        for d in range(N):
            m = _signed(alg, apps[d]); sig = pq.sign(m, sk)
            if A.hybrid:
                blob = struct.pack(">H", len(sig)) + edk.sign(m) + sig
            else:
                blob = struct.pack(">H", len(sig)) + sig
            syms = A.code.encode(blob)
            w = off + d
            for r, j in enumerate(us):
                idx = r % A.n_sym
                S.put(w * M + j, apps[d], struct.pack(">BBB", T_FRAG, alg, idx) + syms[idx])
            for j in range(M):
                if j not in us:
                    S.put(w * M + j, apps[d], b"")
    elif A.kind == "merkle":
        n = A.n; lg = int(math.log2(n)); nb = N // n
        trees = []
        for b in range(nb):
            leaves = [H(b"\x00", apps[b * n + j]) for j in range(n)]
            lv = [leaves]
            while len(lv[-1]) > 1:
                x = lv[-1]; lv.append([H(b"\x01", x[2 * t], x[2 * t + 1]) for t in range(len(x) // 2)])
            root = lv[-1][0]
            sig = pq.sign(b"R" + bytes([alg]) + struct.pack(">H", b) + root, sk)
            blob = struct.pack(">H", len(sig)) + sig
            paths = []
            for j in range(n):
                p = []; idx = j
                for lvl in range(lg):
                    p.append(lv[lvl][idx ^ 1]); idx >>= 1
                paths.append(b"".join(p))
            trees.append((A.code.encode(blob), paths))
        a0 = 6 + A.control
        S.layout = dict(path=(5, 5 + A.control), sym=(a0, a0 + A.s))
        for d in range(N + n):
            w = off + d; app = apps[d] if d < N else dummy
            bprev = d // n - 1
            for j in range(M):
                if bprev < 0 or bprev >= nb or j not in us:
                    S.put(w * M + j, app, b"")
            if 0 <= bprev < nb:
                syms, paths = trees[bprev]
                for r, j in enumerate(us):
                    c = (d % n) * A.u + r; idx = c % A.n_sym
                    hdr = struct.pack(">BBHB", T_MERK, alg, bprev, d % n)
                    S.put(w * M + j, app, hdr + paths[d % n] + bytes([idx]) + syms[idx])
    else:
        Ne = N // E; L = A.lead
        chains = []
        for e in range(Ne + 1):
            K = [None] * (E + 1)
            K[E] = H(b"seed", struct.pack(">II", build_seed, e))[:KEY_B]
            for i in range(E, 0, -1):
                K[i - 1] = Fchain(K[i])
            chains.append(K)
        anchors = []
        for a in range(Ne):
            ts = struct.pack(">I", int(a * E * M * plan.T * 1000) & 0xFFFFFFFF)
            to_sign = b"A" + bytes([alg]) + struct.pack(">H", a) + chains[a][0] + ts
            sig = pq.sign(to_sign, sk)
            blob = struct.pack(">H", len(sig)) + chains[a][0] + ts + sig
            anchors.append(A.code.encode(blob))
        o = 2 + 2 + 1
        tag_o = (o, o + TAG_B); ke_o = o + TAG_B; key_o = (ke_o + 3, ke_o + 3 + KEY_B)
        nc_o = (key_o[1], key_o[1] + COMMIT_B) if A.cont else None
        a_o = (nc_o[1] if A.cont else key_o[1]) + 3
        S.layout = dict(tag=tag_o, key=key_o, nc=nc_o, sym=(a_o, a_o + A.s))
        w_first = 0 if L else off
        w_last = off + N                                      # trailing window discloses the last key
        for w in range(w_first, w_last + 1):
            rel = w - off; app = apps[rel] if 0 <= rel < N else dummy
            if 0 <= rel < N:
                e, i = rel // E, rel % E + 1
                nc = chains[e + 1][0] if A.cont else b""
                tg = mac_tag(chains[e][i], e, i, app, nc)
            else:
                e, i, tg, nc = NOEPOCH, 0, bytes(TAG_B), (bytes(COMMIT_B) if A.cont else b"")
            if 0 <= rel - 1 < N:
                pe, pi = (rel - 1) // E, (rel - 1) % E + 1
                ke, ki, key = pe, pi, chains[pe][pi]
            else:
                ke, ki, key = NOEPOCH, 0, bytes(KEY_B)
            erel = rel // E if rel >= 0 else -1
            a = erel + L
            for j in range(M):
                if j not in us:
                    S.put(w * M + j, app, b"")
                    continue
            for r, j in enumerate(us):
                if 0 <= a < Ne:
                    c = (rel - erel * E) * A.u + r; ai = c % A.n_sym
                    ahead = struct.pack(">HB", a, ai); sym = anchors[a][ai]
                else:
                    ahead = struct.pack(">HB", NOEPOCH, 0); sym = b""
                auth = (struct.pack(">BBHB", T_CHAIN, alg, e, i) + tg + struct.pack(">HB", ke, ki) + key + nc + ahead + sym)
                S.put(w * M + j, app, auth)
    S.tx_cpu_ns = time.thread_time_ns() - t0; S.tx_sign_ns = ctr.sign_ns; S.n_sign = ctr.n_sign
    return S


# ----------------------------------------------------------------------------- receivers
class Rx:
    """Receiver base. A message counts as authenticated only when a verification of the received bytes succeeded."""
    def __init__(self, alloc, pk, join=0, ctr=None, ed_pk=None):
        self.A = alloc; self.plan = alloc.plan; self.pk = pk; self.join = join
        self.ctr = ctr or Counters(); self.pq = PQ(alloc.pq, self.ctr); self.alg = alg_id(alloc.pq)
        self.ed = Ed(self.ctr) if alloc.hybrid else None; self.ed_pk = ed_pk
        self.auth = {}; self.app = {}; self.rejected = 0; self.copies = {}

    def deliver(self, g, app, auth):
        if g < self.join:
            return
        self.on_frame(g, app, auth)

    def _accept(self, seq, app, g):
        if seq not in self.auth:
            self.auth[seq] = g; self.app[seq] = app

    def _copy(self, seq, app):
        c = self.copies.setdefault(seq, [])
        if app not in c and len(c) < 4:
            c.append(app)
        return c

    @staticmethod
    def _seq(app):
        return struct.unpack(">I", app[:4])[0]


class FragRx(Rx):
    def __init__(self, *a, **k):
        super().__init__(*a, **k); self.st = {}

    def on_frame(self, g, app, auth):
        A = self.A
        seq = self._seq(app)
        if seq == NONE_SEQ or seq in self.auth or len(auth) < 3 or auth[0] != T_FRAG or auth[1] != self.alg:
            return
        st = self.st.setdefault(seq, dict(syms={}, order=[], blob=None, tries=0, checked=set()))
        copies = self._copy(seq, app)
        idx = auth[2]; sym = auth[3:]
        if idx < A.n_sym and idx not in st["syms"] and len(sym) == A.s:
            st["syms"][idx] = sym; st["order"].append(idx)
            if st["blob"] is not None and st["tries"] < 3 and not self._try(seq, st, copies, g):
                st["blob"] = None
        if st["blob"] is None and A.code.complete(st["syms"]) and st["tries"] < 3:
            use = {i: st["syms"][i] for i in st["order"][-A.k:]} if A.coder == "mds" else st["syms"]
            if A.coder == "mds" and len(use) < A.k:
                use = st["syms"]
            st["blob"] = A.code.decode(use); st["tries"] += 1
            st["checked"] = set()
        if st["blob"] is not None:
            self._try(seq, st, copies, g)

    def _try(self, seq, st, copies, g):
        blob = st["blob"]; ok_any = False
        n = struct.unpack(">H", blob[:2])[0]
        if self.A.hybrid:
            ed_sig, sig = blob[2:2 + ED_SIG], blob[2 + ED_SIG:2 + ED_SIG + n]
        else:
            ed_sig, sig = None, blob[2:2 + n]
        for c in copies:
            if c in st["checked"]:
                continue
            st["checked"].add(c)
            m = _signed(self.alg, c)
            ok = self.pq.verify(m, sig, self.pk)
            if ok and self.A.hybrid:
                ok = self.ed.verify(m, ed_sig, self.ed_pk)
            if ok:
                self._accept(seq, c, g); return True
            self.rejected += 1
        return False


class MerkleRx(Rx):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.bst = {}; self.paths = {}; self.vcache = {}

    def on_frame(self, g, app, auth):
        A = self.A; n = A.n
        seq = self._seq(app)
        if seq != NONE_SEQ:
            self._copy(seq, app)
        if len(auth) < A.hdr + A.control or auth[0] != T_MERK or auth[1] != self.alg:
            return
        b = struct.unpack(">H", auth[2:4])[0]; leaf = auth[4]
        if leaf >= n:
            return
        path = auth[5:5 + A.control]; idx = auth[5 + A.control]; sym = auth[6 + A.control:]
        ref = b * n + leaf
        self.paths.setdefault(ref, path)
        st = self.bst.setdefault(b, dict(syms={}, order=[], blob=None, sig=None, tries=0))
        newblob = False
        if idx < A.n_sym and idx not in st["syms"] and len(sym) == A.s and st["sig"] is None:
            st["syms"][idx] = sym; st["order"].append(idx)
        if st["sig"] is None and A.code.complete(st["syms"]) and st["tries"] < 3:
            use = {i: st["syms"][i] for i in st["order"][-A.k:]} if A.coder == "mds" else st["syms"]
            blob = A.code.decode(use); st["tries"] += 1
            nn = struct.unpack(">H", blob[:2])[0]; st["sig"] = blob[2:2 + nn]; newblob = True
        if st["sig"] is not None:
            for lf in ([ref] if not newblob else range(b * n, b * n + n)):
                self._check(b, lf, g, st)

    def _root(self, ref, copy, path):
        h = H(b"\x00", copy); idx = ref % self.A.n
        for lvl in range(len(path) // 32):
            sib = path[32 * lvl:32 * lvl + 32]
            h = H(b"\x01", sib, h) if idx & 1 else H(b"\x01", h, sib)
            idx >>= 1
        return h

    def _check(self, b, ref, g, st):
        if ref in self.auth or ref not in self.paths:
            return
        for c in self.copies.get(ref, []):
            if self._seq(c) != ref:
                continue
            root = self._root(ref, c, self.paths[ref])
            key = (b, root)
            if key not in self.vcache:
                ok = self.pq.verify(b"R" + bytes([self.alg]) + struct.pack(">H", b) + root, st["sig"], self.pk)
                self.vcache[key] = ok
                if not ok:
                    self.rejected += 1
                    if st["tries"] < 3:
                        st["sig"] = None   # corrupted decode: allow a retry with newer symbols
            if self.vcache[key]:
                self._accept(ref, c, g); return


class ChainRx(Rx):
    def __init__(self, *a, enforce_time_safety=True, **k):
        super().__init__(*a, **k)
        self.enforce = enforce_time_safety
        self.commit = {}; self.kst = {}; self.stash = {}; self.pend = {}; self.asm = {}; self.bad_anchor = {}

    def _win(self, e, i):
        return self.plan.off + e * self.plan.E + i - 1

    def on_frame(self, g, app, auth):
        A = self.A; pl = self.plan
        need = A.hdr + A.control
        if len(auth) < need or auth[0] != T_CHAIN or auth[1] != self.alg:
            return
        e, i = struct.unpack(">HB", auth[2:5]); o = 5
        tag = auth[o:o + TAG_B]; o += TAG_B
        ke, ki = struct.unpack(">HB", auth[o:o + 3]); o += 3
        key = auth[o:o + KEY_B]; o += KEY_B
        nc = b""
        if A.cont:
            nc = auth[o:o + COMMIT_B]; o += COMMIT_B
        ae, ai = struct.unpack(">HB", auth[o:o + 3]); sym = auth[o + 3:]
        seq = self._seq(app)
        if ae != NOEPOCH:
            self._anchor(ae, ai, sym, g)
        if ke != NOEPOCH:
            self._key(ke, ki, key, g)
        if e != NOEPOCH and seq != NONE_SEQ and seq not in self.auth and 1 <= i <= pl.E:
            ok_time = g < (self._win(e, i) + 1) * pl.M                 # received before the key can have been disclosed
            kidx = self.kst.get(e, (0, None))[0]
            if self.enforce and (not ok_time or kidx >= i):
                self.rejected += 1
                return
            lst = self.pend.setdefault((e, i), [])
            item = (app, tag, nc)
            if item not in lst and len(lst) < 4:
                lst.append(item)
            self._resolve(e, g)

    def _anchor(self, ae, ai, sym, g):
        A = self.A
        if ae in self.commit or self.bad_anchor.get(ae, 0) >= 3:
            return
        st = self.asm.setdefault(ae, dict(syms={}, order=[]))
        if ai < A.n_sym and ai not in st["syms"] and len(sym) == A.s:
            st["syms"][ai] = sym; st["order"].append(ai)
        else:
            return
        if not A.code.complete(st["syms"]):
            return
        use = {x: st["syms"][x] for x in st["order"][-A.k:]} if A.coder == "mds" else st["syms"]
        blob = A.code.decode(use)
        n = struct.unpack(">H", blob[:2])[0]
        commit = blob[2:2 + COMMIT_B]; ts = blob[2 + COMMIT_B:2 + COMMIT_B + TS_B]; sig = blob[2 + COMMIT_B + TS_B:2 + COMMIT_B + TS_B + n]
        if self.pq.verify(b"A" + bytes([self.alg]) + struct.pack(">H", ae) + commit + ts, sig, self.pk):
            self._set_commit(ae, commit, g)
        else:
            self.rejected += 1; self.bad_anchor[ae] = self.bad_anchor.get(ae, 0) + 1

    def _set_commit(self, e, commit, g):
        if e in self.commit:
            return
        self.commit[e] = commit
        if e in self.stash:
            ki, key = self.stash.pop(e); self._key(e, ki, key, g)
        self._resolve(e, g)

    def _key(self, ke, ki, key, g):
        if ki > self.plan.E or ki < 1:
            return
        if ke not in self.commit:
            if ki > self.stash.get(ke, (0, None))[0]:
                self.stash[ke] = (ki, key)
            return
        i0, k0 = self.kst.get(ke, (0, self.commit[ke]))
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
        if e not in self.kst:
            return
        idx, key = self.kst[e]
        for i in range(1, idx + 1):
            lst = self.pend.get((e, i))
            if not lst:
                continue
            Ki = key
            for _ in range(idx - i):
                Ki = Fchain(Ki)
            for item in list(lst):
                app, tag, nc = item
                seq = self._seq(app)
                if seq in self.auth:
                    break
                if hmac.compare_digest(mac_tag(Ki, e, i, app, nc), tag):
                    self._accept(seq, app, g)
                    if self.A.cont and nc and (e + 1) not in self.commit:
                        self._set_commit(e + 1, nc, g)
                    lst.clear(); break
                else:
                    self.rejected += 1
                    lst.remove(item)


def make_rx(alloc, pk, join=0, ctr=None, ed_pk=None, **kw):
    cls = {"frag": FragRx, "merkle": MerkleRx, "chain": ChainRx}[alloc.kind]
    if alloc.kind != "chain":
        kw.pop("enforce_time_safety", None)
    return cls(alloc, pk, join=join, ctr=ctr, ed_pk=ed_pk, **kw)
