"""Symbol coding of a blob: plain repetition ('rep') or systematic Reed-Solomon over GF(256) via zfec ('mds', any k of n)."""
import math
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
    """k source symbols of s bytes; rep: n_sym = k raw fragments; mds: n_sym coded symbols (k <= n_sym <= 256)."""
    def __init__(self, coder, blob_len, room, n_slots_span):
        self.coder = coder
        self.k = max(1, math.ceil(blob_len / room)) if room > 0 else 10 ** 9
        self.s = math.ceil(blob_len / self.k) if room > 0 else 0
        self.n_sym = self.k if coder == "rep" else min(max(n_slots_span, 0), 255)
        if coder == "mds" and self.n_sym < self.k:
            self.n_sym = self.k  # symbols exist but cannot all be sent: caller marks infeasible
        self.feasible = room > 0 and n_slots_span >= self.k and self.k <= 255

    def encode(self, blob):
        k, s = self.k, self.s
        blob = blob + bytes(k * s - len(blob))
        src = [blob[i * s:(i + 1) * s] for i in range(k)]
        if self.coder == "rep":
            return src
        if self.n_sym == k:
            return src
        return [bytes(b) for b in _enc(k, self.n_sym).encode(src)]

    def decode(self, got):
        """got: dict idx -> symbol (>= k entries). Returns the padded blob."""
        k = self.k
        items = list(got.items())[:k]
        if self.coder == "rep" or self.n_sym == k:
            return b"".join(got[i] for i in range(k))
        out = _dec(k, self.n_sym).decode([v for _, v in items], [i for i, _ in items])
        return b"".join(bytes(b) for b in out)

    def complete(self, got):
        if self.coder == "rep" or self.n_sym == self.k:
            return len(got) >= self.k and all(i in got for i in range(self.k))
        return len(got) >= self.k
