"""EMBER issuer: queue claims, close epochs (tree + one root signature), period bundles, revocation."""
import os
import struct
import time
from dataclasses import dataclass, field

from .merkle import auth_path, build_tree, leaf_hash, period_root
from .token import Claims, enc, encode_ember

EPOCH_MAX = 0xFFFFFFFF


@dataclass
class SignedRoot:
    kid: int
    epoch: int
    t_start_ms: int
    delta_ms: int
    N: int
    root: bytes
    sig: bytes = b""

    _S = struct.Struct(">IIQII")  # 24 B header

    def msg(self) -> bytes:
        return b"EMBER-root" + self._S.pack(self.kid, self.epoch, self.t_start_ms, self.delta_ms, self.N) + self.root

    def to_bytes(self) -> bytes:  # stapled / wire form: hdr | n | root | sig
        return self._S.pack(self.kid, self.epoch, self.t_start_ms, self.delta_ms, self.N) + bytes([len(self.root)]) + self.root + self.sig

    @classmethod
    def from_bytes(cls, b: bytes):
        kid, e, ts, d, N = cls._S.unpack_from(b)
        n = b[24]
        return cls(kid, e, ts, d, N, b[25:25 + n], b[25 + n:])

    @property
    def meta_entry(self) -> bytes:  # period-bundle entry: e|t_start|delta|N|R  (20+n B)
        return struct.pack(">IQII", self.epoch, self.t_start_ms, self.delta_ms, self.N) + self.root


@dataclass
class PeriodBundle:
    kid: int
    period: int
    e_first: int
    entries: list            # list of meta_entry bytes
    n: int
    sig: bytes = b""

    def mth(self) -> bytes:
        return period_root(self.kid, self.period, self.entries, self.n)

    def msg(self) -> bytes:
        return b"EMBER-period" + struct.pack(">IIII", self.kid, self.period, self.e_first, len(self.entries)) + self.mth()

    def size_bytes(self) -> int:
        return 16 + sum(len(x) for x in self.entries) + len(self.sig)

    def roots(self):
        out = []
        for x in self.entries:
            e, ts, d, N = struct.unpack_from(">IQII", x)
            out.append(SignedRoot(self.kid, e, ts, d, N, x[20:]))
        return out


@dataclass
class RevocationDelta:
    kid: int
    seq: int
    items: list               # sorted [(e, i)]
    sig: bytes = b""

    def msg(self) -> bytes:
        return b"EMBER-revoke" + struct.pack(">III", self.kid, self.seq, len(self.items)) + b"".join(
            struct.pack(">II", e, i) for e, i in self.items)


class EmberIssuer:
    def __init__(self, signer, kid, n=16, period_m=300, rng=None, pad_pow2=False, v_max=3600.0,
                 alg_name=None, t0=0.0):
        self.signer, self.kid, self.n, self.m = signer, kid, n, period_m
        self.rng = rng or os.urandom
        self.pad_pow2 = pad_pow2
        self.v_max = v_max
        self.alg = alg_name or signer.name
        self.queue = []
        self.next_ticket = 0
        self.epoch = 0
        self.t_open = t0
        self.period_entries = []
        self.period = 0
        self.period_first = 0
        self.revoked = []
        self.rev_seq = 0
        self.roots = {}

    def submit(self, claims: Claims) -> int:
        t = self.next_ticket
        self.next_ticket += 1
        self.queue.append((t, claims))
        return t

    def close_epoch(self, t_now, t_start=None):
        """Returns (SignedRoot, {ticket: token}, timings_ns).  Raises on an empty queue."""
        if not self.queue:
            raise ValueError("empty epoch")
        if self.epoch >= EPOCH_MAX:
            raise OverflowError("epoch counter would wrap; rotate kid")
        t_start = self.t_open if t_start is None else t_start
        e = self.epoch
        batch, self.queue = self.queue, []
        t_start_ms = int(round(t_start * 1000))
        delta_ms = int(round((t_now - t_start) * 1000))
        bound = (t_start_ms + delta_ms) // 1000 + int(self.v_max)
        kid, n = self.kid, self.n
        pc = time.perf_counter_ns
        t0 = pc()
        claims = []
        leaves = []
        salts = []
        for i, (_, c) in enumerate(batch):
            if c.expires > bound:
                c = c.with_(expires=bound)  # epoch-bounded validity
            ce = enc(c)
            r = self.rng(16)
            claims.append((c, ce))
            salts.append(r)
            leaves.append(leaf_hash(kid, e, i, c.tenant, r, ce, n))
        N = len(leaves)
        if self.pad_pow2:
            P = 1 << (N - 1).bit_length()
            leaves.extend(self.rng(n) for _ in range(P - N))
            N = P
        t1 = pc()
        root, levels = build_tree(kid, e, leaves, n)
        t2 = pc()
        sr = SignedRoot(kid, e, t_start_ms, delta_ms, N, root)
        sr.sig = self.signer.sign(sr.msg())
        t3 = pc()
        out = {}
        for i, (tk, _) in enumerate(batch):
            c, _ = claims[i]
            out[tk] = encode_ember(c, kid, e, i, salts[i], auth_path(levels, i), n, self.alg)
        t4 = pc()
        self.epoch += 1
        self.t_open = t_now
        self.roots[e] = sr
        self.period_entries.append(sr.meta_entry)
        timings = dict(t_leaf=t1 - t0, t_tree=t2 - t1, t_sign=t3 - t2, t_encode=t4 - t3, t_epoch=t4 - t0, N=len(batch))
        return sr, out, timings

    def close_period(self) -> PeriodBundle:
        pb = PeriodBundle(self.kid, self.period, self.period_first, self.period_entries, self.n)
        pb.sig = self.signer.sign(pb.msg())
        self.period += 1
        self.period_first = self.epoch
        self.period_entries = []
        return pb

    def revoke(self, epoch, idx):
        self.revoked.append((epoch, idx))

    def revocation_delta(self) -> RevocationDelta:
        rd = RevocationDelta(self.kid, self.rev_seq, sorted(self.revoked))
        rd.sig = self.signer.sign(rd.msg())
        self.rev_seq += 1
        self.revoked = []
        return rd
