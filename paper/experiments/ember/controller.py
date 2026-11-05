"""Epoch policies (design.md §4.4).  The numerical kernels live in sim/fleet_mc.py (numba) and are used both by
the simulator and by this reference wrapper, so there is exactly one implementation of the decision rule.

FixedDelta(delta)            aligned timer epochs + count trigger N_max
WorkConserving()             close as soon as the signer is idle and >= 1 request is pending
Adaptive(...)                per tenant: EWMA rate -> argmin_Delta  Delta/2 + t_build + t_sign + M(lam*Delta)*F(lam*Delta)
                             s.t. p99 wait <= L_SLO, signer capacity, size budget (count trigger)
"""
import numpy as np

from sim import fleet_mc as F
from sim import model as M


class FixedDelta:
    def __init__(self, delta, nmax=1 << 40):
        self.delta, self.nmax = delta, nmax

    def epochs(self, arr):
        return F.epochs_fixed(arr, self.delta, self.nmax)


class WorkConserving:
    def __init__(self, t_tok, t_sign):
        self.t_tok, self.t_sign = t_tok, t_sign

    def epochs(self, arr):
        return F.epochs_wc(arr, self.t_tok, self.t_sign)


class Adaptive:
    def __init__(self, w, S, rtt_es_mean, rtt_sr_mean, t_tok, t_sign, slo=2.0, budget_B=1024, claims_bytes=104,
                 n=16, grid=None, alpha=0.2):
        self.grid = grid if grid is not None else np.logspace(np.log10(0.01), np.log10(60), 25)
        lx = np.linspace(np.log(1e-4), np.log(1e9), 600)
        x = np.exp(lx)
        Mx = M.miss_per_token(x, w)
        ws = np.bincount(np.arange(w.size) % S, weights=w, minlength=S)
        Ms = M.miss_per_token(x, ws)
        Fx = rtt_es_mean + (Ms / np.maximum(Mx, 1e-300)) * rtt_sr_mean
        self.lx, self.lmf = lx, np.log(np.maximum(Mx * Fx, 1e-300))
        self.t_tok, self.t_sign, self.slo, self.alpha = t_tok, t_sign, slo, alpha
        self.nmax = float(1 << min(40, M.d_max(budget_B, claims_bytes, n)))

    def choose(self, lam):
        return F.choose_delta(lam, self.grid, self.lx, self.lmf, self.t_tok, self.t_sign, self.slo, self.nmax)

    def epochs(self, arr, lam0, t_start):
        return F.epochs_adaptive(arr, self.grid, self.lx, self.lmf, self.t_tok, self.t_sign, self.slo,
                                 int(min(self.nmax, 1 << 40)), self.alpha, lam0, t_start)
