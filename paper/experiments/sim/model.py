"""Analytical model (design.md §4.4-4.5).  Model values are always labelled 'model' in outputs."""
import math

import numpy as np


def token_bytes(claims_bytes, n, d):
    return claims_bytes + 3 + math.ceil(4 * (30 + n * d) / 3)


def d_max(B, claims_bytes, n):
    """Largest path length such that the encoded token fits in B bytes."""
    return int(((3 * B) // 4 - 30 - claims_bytes) // n)


def miss_per_token(x, w):
    """M(Delta) for x = lambda*Delta expected tokens per epoch, pull mode, per-epoch roots."""
    x = np.asarray(x, float)
    out = np.empty_like(x)
    for i, xi in enumerate(x.ravel()):
        out.ravel()[i] = -np.expm1(-xi * w).sum() / xi if xi > 0 else 1.0
    return out


class MTable:
    """Tabulated M(x) on a log grid (used by the controller for speed)."""

    def __init__(self, w, lo=1e-4, hi=1e9, k=1200):
        self.lx = np.linspace(np.log(lo), np.log(hi), k)
        self.ly = np.log(np.maximum(miss_per_token(np.exp(self.lx), w), 1e-300))

    def __call__(self, x):
        return np.exp(np.interp(np.log(np.maximum(x, 1e-12)), self.lx, self.ly))


def fetch_penalty(w, E, S, rtt_es_mean, rtt_sr_mean, x):
    """Expected miss penalty F: edge->shield RTT plus shield->root RTT when the shield also misses.
    Shield share = sum of its edges' shares (edge e -> shield e % S)."""
    ws = np.bincount(np.arange(E) % S, weights=w, minlength=S)
    me = miss_per_token(np.atleast_1d(x), w)[0]
    ms = miss_per_token(np.atleast_1d(x), ws)[0]
    return rtt_es_mean + (ms / max(me, 1e-12)) * rtt_sr_mean


def D_model(delta, lam, w, F, t_tok, t_sign):
    x = lam * delta
    return delta / 2 + x * t_tok + t_sign + miss_per_token(np.atleast_1d(x), w)[0] * F


def push_bw(E, S, sr_bytes, nonempty_epochs_per_s):
    return (E + S) * sr_bytes * nonempty_epochs_per_s
