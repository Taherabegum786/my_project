"""Symbol coding of a blob (plain repetition 'rep' or systematic Reed-Solomon over GF(256) via zfec 'mds', any k of n),
the code-size rule (choose_s) and the Assembler that rebuilds a blob from possibly polluted symbols (decode-and-verify over subsets).
"""
import math
import random

import numpy as np
import zfec

_ENC = {}; _DEC = {}


def _enc(k, n):
    if (k, n) not in _ENC:
        _ENC[(k, n)] = zfec.Encoder(k, n)
    return _ENC[(k, n)]


def _dec(k, n):
    if (k, n) not in _DEC:
        _DEC[(k, n)] = zfec.Decoder(k, n)
    return _DEC[(k, n)]


class BlobCode:
    """k source symbols of s bytes. rep: n distinct symbols = k raw fragments (the sender repeats them cyclically);
    mds: n coded symbols (k <= n <= 255, any k decode)."""
    def __init__(self, coder, blob_len, s, n):
        self.coder, self.s = coder, s
        self.k = max(1, math.ceil(blob_len / s))
        self.n = self.k if coder == "rep" else max(n, self.k)

    def encode(self, blob):
        k, s = self.k, self.s
        blob = blob + bytes(k * s - len(blob))
        src = [blob[i * s:(i + 1) * s] for i in range(k)]
        if self.coder == "rep" or self.n == k:
            return src
        return [bytes(b) for b in _enc(k, self.n).encode(src)]

    def decode(self, chosen):
        """chosen: list of (idx, symbol) with >= k distinct idx (rep: exactly the idx 0..k-1). Returns the padded blob."""
        k = self.k
        if self.coder == "rep" or self.n == k:
            d = dict(chosen)
            return b"".join(d[i] for i in range(k))
        items = chosen[:k]
        out = _dec(k, self.n).decode([v for _, v in items], [i for i, _ in items])
        return b"".join(bytes(b) for b in out)


def prob_k_of(counts, k, p0):
    """P[sum_l counts[l] * Bernoulli(1-p0) >= k] (slot-level independent loss p0; the symbols of a slot are all received or all lost)."""
    dist = np.zeros(sum(counts) + 1); dist[0] = 1.0
    for c in counts:
        if c == 0:
            continue
        nd = dist * p0
        nd[c:] += dist[:len(dist) - c] * (1 - p0)
        dist = nd
    return float(dist[k:].sum()) if k <= len(dist) - 1 else 0.0


def spread(n, W):
    """symbols per span slot when n symbols are dealt round robin over W slots"""
    return [len(range(l, n, W)) for l in range(W)]


K_CAND = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 64, 96, 128, 192, 255]


def choose_s(blob_len, coder, samples, rho=None, p0=0.2):
    """Code-size rule (same for every mode, no per-mode tuning): among symbol sizes s = ceil(blob/k) for k in K_CAND, pick the one that
    (1) is feasible (n >= k) for the largest share of sample objects, then (2) maximises the mean design-point reliability
    P[at least k of the n symbols arrive] at slot loss p0 = 0.2 (MDS assumption, symbols spread over the object's span), then (3) larger s.
    samples: list of (W, cap_fn) per sample object: W = slots of its span, cap_fn(s) = number of symbols of size s that fit in its span.
    Returns (s, k) or None."""
    best = None
    seen = set()
    for kc in K_CAND:
        s = max(4, math.ceil(blob_len / kc))
        if s in seen:
            continue
        seen.add(s)
        k = math.ceil(blob_len / s)
        if k > 255:
            continue
        feas = 0; tot = 0.0
        for W, fn in samples:
            n = int(fn(s))
            if coder == "mds":
                n = min(n, 255)
            if rho:
                n = min(n, math.ceil(rho * k))
            if n >= k:
                feas += 1
                nd = n if coder == "mds" else n
                tot += prob_k_of(spread(nd, W), k, p0)
        sc = (feas / len(samples), tot / len(samples), s)
        if feas and (best is None or sc > best[0]):
            best = (sc, s, k)
    return None if best is None else (best[1], best[2])


class Assembler:
    """Collects symbols of one object (up to CAND distinct candidates per index, so a polluted symbol that arrives first does not
    displace the genuine one) and yields candidate blobs decoded from different symbol subsets (decode-and-verify).
    The caller verifies each blob (signature / hash); total subset decodes per object are bounded by DEC_MAX."""
    CAND = 3
    DEC_MAX = 16

    def __init__(self, code, seed=0):
        self.code = code
        self.c = {}               # idx -> list of candidate symbols (arrival order)
        self.order = []           # (idx, pos) arrival order
        self.tried = set(); self.decodes = 0; self.fails = 0; self.dead = False
        self.rng = random.Random(seed); self.nadd = 0; self.seen_nadd = -1

    def add(self, idx, data):
        if idx >= self.code.n:
            return False
        lst = self.c.setdefault(idx, [])
        if data in lst or len(lst) >= self.CAND:
            return False
        lst.append(data); self.order.append((idx, len(lst) - 1)); self.nadd += 1
        return True

    def ready(self):
        if self.code.coder == "rep":
            return all(i in self.c for i in range(self.code.k))
        return len(self.c) >= self.code.k

    def _subset(self, i):
        k = self.code.k
        if self.code.coder == "rep":
            idxs = list(range(k))
        elif i == 0:                                   # earliest-arrived k distinct indices
            idxs = []; seen = set()
            for ix, _ in self.order:
                if ix not in seen:
                    seen.add(ix); idxs.append(ix)
                if len(idxs) == k:
                    break
        elif i == 1:                                   # latest-arrived k distinct indices
            idxs = []; seen = set()
            for ix, _ in reversed(self.order):
                if ix not in seen:
                    seen.add(ix); idxs.append(ix)
                if len(idxs) == k:
                    break
        else:
            idxs = self.rng.sample(sorted(self.c), k)
        if i == 0:
            pos = {ix: 0 for ix in idxs}
        elif i == 1:
            pos = {ix: len(self.c[ix]) - 1 for ix in idxs}
        else:
            pos = {ix: self.rng.randrange(len(self.c[ix])) for ix in idxs}
        return tuple(sorted((ix, pos[ix]) for ix in idxs))

    def blobs(self, max_new=3):
        """Yield (blob, key) for at most max_new untried subsets (only when new symbols arrived since the last call)."""
        if self.dead or not self.ready() or self.nadd == self.seen_nadd:
            return
        self.seen_nadd = self.nadd
        got = 0; i = 0; guard = 0
        while got < max_new and self.decodes < self.DEC_MAX and guard < 6:
            key = self._subset(i if i < 2 else 2); i += 1; guard += 1
            if key in self.tried:
                continue
            self.tried.add(key); self.decodes += 1; got += 1
            yield self.code.decode([(ix, self.c[ix][p]) for ix, p in key]), key
