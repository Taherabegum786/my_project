"""Closed forms for i.i.d. slot loss p, matching EXACTLY the packing of lib/pqsig/proto/modes.py (symmetric model):
every mode gets M slots per application message; u = usable slots per window (cap >= frame length, see modes.py ALLOCATION RULE);
the heavy blob (signature / batch signature / anchor) is split into k source symbols and sent as erasure-coded (MDS, any k of n_sym
distinct symbols) or repeated symbols round robin over the usable slots of its span. q = 1 - p.

  frag_rep / hyb_rep   r_j = u//k + [j < u mod k] copies of fragment j        P = prod_j (1 - p^r_j)                 (u >= k)
  frag_mds / hyb_mds   P = P[Bin(u, q) >= k]
  merkle (batch n)     message copy in own window (all M slots carry the app message): 1 - p^M; leaf path in window j of the
                       NEXT batch (X ~ Bin(u,q) received there, X >= 1) and k of the n*u signature symbols (the same slots):
                       P = (1 - p^M) * sum_{x>=1} b(u,x) P[Bin((n-1)u, q) >= k - x]                 (valid if n*u <= 255)
  chain  (lead 0)      message at position i of an epoch of E windows needs: tag copy in own window (x1 >= 1 of u slots),
                       a key in windows i+1..E or in the first window of the next epoch (x2 >= 1 of u(E-i) slots, else one of the
                       u slots of the next window), and the epoch's anchor: x1 + x2 + Y >= k_a, Y ~ Bin(u(i-1), q)
                       (all of them use slots of the same epoch -> correlated; summed exactly).  Averaged over i = 1..E.
  chain_lead (lead 1)  the anchor of epoch e is sent during epoch e-1 (prelude for e = 0): independent of the message's own slots:
                       P = mean_i (1 - p^u)(1 - p^{u(E-i+1)}) P[Bin(E u, q) >= k_a]
  chain_lead_cont      no closed form (continuity couples consecutive epochs)
Modes whose symbol span exceeds 255 distinct symbols use cyclic duplicates: no closed form (returns None).
Gilbert-Elliott loss has no closed form here; it is measured only.
"""
import math

import numpy as np


def _pmf(n, q):
    if n == 0:
        return np.array([1.0])
    k = np.arange(n + 1)
    lg = np.array([math.lgamma(n + 1) - math.lgamma(x + 1) - math.lgamma(n - x + 1) for x in k])
    with np.errstate(divide="ignore", invalid="ignore"):
        lp = lg + k * (math.log(q) if q > 0 else -np.inf) + (n - k) * (math.log(1 - q) if q < 1 else -np.inf)
    out = np.exp(lp)
    if q >= 1:
        out = np.zeros(n + 1); out[n] = 1.0
    if q <= 0:
        out = np.zeros(n + 1); out[0] = 1.0
    return out


def sf_arr(n, q):
    """arr[r] = P[Bin(n,q) >= r] for r = 0..n+1 (arr[n+1] = 0); r < 0 handled by caller."""
    pm = _pmf(n, q)
    s = np.concatenate([np.cumsum(pm[::-1])[::-1], [0.0]])
    return s


def sf(n, k, q):
    if k <= 0:
        return 1.0
    if k > n:
        return 0.0
    return float(sf_arr(n, q)[k])


def share(mode, p, a):
    """a: dict with u, M, k, n_sym, E, n (batch), span (usable symbols in span). Returns expected share or None."""
    q = 1 - p; u, M, k, E = a["u"], a["M"], a["k"], a["E"]
    if u == 0 or not a["feasible"]:
        return 0.0
    if mode in ("frag_rep", "hyb_rep"):
        if u < k:
            return 0.0
        base, rem = divmod(u, k)
        return float(np.prod([1 - p ** (base + (1 if j < rem else 0)) for j in range(k)]))
    if mode in ("frag_mds", "hyb_mds"):
        return sf(u, k, q)
    if mode.startswith("merkle"):
        n = a["n"]
        if n * u > 255:
            return None
        pm = _pmf(u, q); s = sf_arr((n - 1) * u, q)
        tot = 0.0
        for x in range(1, u + 1):
            r = k - x
            tot += pm[x] * (1.0 if r <= 0 else (s[r] if r <= (n - 1) * u else 0.0))
        return (1 - p ** M) * float(tot)
    if mode.startswith("chain"):
        if E * u > 255 or mode == "chain_lead_cont":
            return None
        ka = k
        if mode == "chain_lead":
            pa = sf(E * u, ka, q)
            return float(np.mean([(1 - p ** u) * (1 - p ** (u * (E - i + 1))) * pa for i in range(1, E + 1)]))
        pm1 = _pmf(u, q); res = []
        for i in range(1, E + 1):
            pm2 = _pmf(u * (E - i), q); s4 = sf_arr(u * (i - 1), q); n4 = u * (i - 1)
            w2 = np.ones(len(pm2)); w2[0] = 1 - p ** u
            tot = 0.0
            for x1 in range(1, u + 1):
                x2 = np.arange(len(pm2)); r = ka - x1 - x2
                tail = np.where(r <= 0, 1.0, np.where(r > n4, 0.0, s4[np.clip(r, 0, n4 + 1)]))
                tot += pm1[x1] * float(np.sum(pm2 * w2 * tail))
            res.append(tot)
        return float(np.mean(res))
    raise ValueError(mode)


def loss_sequence(rng, N, p, burst_len=None):
    """Boolean array, True = slot lost. burst_len None -> i.i.d.; else Gilbert-Elliott with loss 1 in Bad, 0 in Good,
    mean Bad sojourn = burst_len slots, stationary P(Bad) = p."""
    if burst_len is None:
        return rng.random(N) < p
    if p <= 0:
        return np.zeros(N, bool)
    pbg = 1.0 / burst_len; pgb = pbg * p / (1 - p)
    out = []; tot = 0; bad = rng.random() < p
    while tot < N:
        m = max(64, int((N - tot) / max(1.0, burst_len + burst_len * (1 - p) / p)) * 2 + 64)
        g = rng.geometric(pgb, m); b = rng.geometric(pbg, m)
        for i in range(m):
            L = int(b[i] if bad else g[i])
            out.append((bad, L)); tot += L; bad = not bad
            if tot >= N:
                break
    return np.repeat(np.array([o[0] for o in out]), [o[1] for o in out])[:N]


def make_mask(G, seed, p, burst_len=None):
    """Deterministic loss mask for a slot stream of length G: same (seed, p, burst) -> same mask in every process/machine."""
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), int(round(p * 1000)), int(burst_len or 0)]))
    return loss_sequence(rng, G, p, burst_len)
