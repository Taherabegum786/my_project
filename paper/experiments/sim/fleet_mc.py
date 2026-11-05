"""Fleet Monte Carlo (E5): per-tenant token generation (numpy, common random numbers) + a numba kernel that
replays every *first* request and every *moved* request of each token against per-edge / per-shield root caches.
Requests that stay on the session's edge after the first one are cache hits by construction (sticky edge,
root cached until V_max + P) and are accounted for in bulk.  Constant-memory statistics (log histograms).

Modes: 0 pull, 1 push, 2 pull_staple, 3 pull_rollup, 4 push_rollup (push of period bundles, pull for open period).
Policies: fixed Delta (aligned timer), work-conserving (wc), adaptive controller (ember.controller).
"""
import math
import os

import numpy as np
from numba import njit

MODES = ["pull", "push", "pull_staple", "pull_rollup", "push_rollup"]
MODE_ID = {m: i for i, m in enumerate(MODES)}

# ------------------------------------------------------------------ histograms (seconds), log bins
H_LO, H_HI, H_NB = 1e-7, 1e4, 1100
H_EDGES = np.concatenate([[0.0], np.logspace(np.log10(H_LO), np.log10(H_HI), H_NB)])
H_MID = np.concatenate([[0.0], np.sqrt(H_EDGES[1:-1] * H_EDGES[2:])])


_L0 = np.log10(H_LO)
_STEP = (np.log10(H_HI) - np.log10(H_LO)) / (H_NB - 1)


def hidx(v):
    v = np.asarray(v, float)
    with np.errstate(divide="ignore"):
        i = np.floor((np.log10(np.maximum(v, 1e-300)) - _L0) / _STEP).astype(np.int64) + 1
    i[v < H_LO] = 0
    return np.clip(i, 0, H_NB - 1)


def hist_add(h, v, w=None):
    if np.size(v):
        h += np.bincount(hidx(v), weights=w, minlength=H_NB)[:H_NB]


def hist_q(h, q):
    c = np.cumsum(h)
    if c[-1] <= 0:
        return float("nan")
    return float(H_MID[min(np.searchsorted(c, q * c[-1]), H_NB - 1)])


# ------------------------------------------------------------------ hashing helpers (numba)
@njit(cache=True, inline="always")
def _mix(x):
    x = (x + np.uint64(0x9E3779B97F4A7C15))
    x = (x ^ (x >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
    x = (x ^ (x >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
    return x ^ (x >> np.uint64(31))


@njit(cache=True, inline="always")
def _u01(key, salt):
    h = _mix(np.uint64(key) ^ _mix(np.uint64(salt)))
    return ((h >> np.uint64(11)) + np.uint64(1)) * (1.0 / 9007199254740994.0)


@njit(cache=True, inline="always")
def _lognorm(key, salt, med, sig):
    u1 = _u01(key, salt)
    u2 = _u01(key, salt + 7919)
    z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
    return med * math.exp(sig * z)


@njit(cache=True, inline="always")
def _find(keys, key, mask):
    h = np.int64(_mix(np.uint64(key)) & np.uint64(mask))
    while True:
        k = keys[h]
        if k == key or k == -1:
            return h
        h = (h + 1) & mask


# ------------------------------------------------------------------ kernel
KB = np.int64(1) << np.int64(40)
TYPE_SHIELD = np.int64(1) << np.int64(60)
TYPE_BUNDLE = np.int64(1) << np.int64(61)


@njit(cache=True)
def kernel(mode, tok_ep, tok_issue, tok_edge, tok_d0, mv_tok, mv_off, mv_edge,
           ep_issue, ep_period, per_avail, S, salt, es_ms, es_sig, sr_ms, sr_sig, push_ms, push_sig):
    """Returns (tok_wait[n], tok_nver[n], req_wait[], req_kind[], counters[8]).
    counters: 0 edge root fetches, 1 shield root fetches, 2 edge bundle fetches, 3 shield bundle fetches,
              4 staple installs, 5 coalesced waits, 6 fallback fetches in push modes, 7 requests replayed."""
    n = tok_ep.size
    m = mv_tok.size
    R = n + m
    t = np.empty(R)
    for i in range(n):
        t[i] = tok_issue[i] + tok_d0[i]
    for j in range(m):
        i = mv_tok[j]
        t[n + j] = tok_issue[i] + tok_d0[i] + mv_off[j]
    order = np.argsort(t)
    cap = 1
    while cap < 4 * R + 16:
        cap *= 2
    mask = cap - 1
    keys = np.full(cap, -1, np.int64)
    vals = np.zeros(cap)
    flag = np.zeros(cap, np.int8)
    tok_wait = np.zeros(n)
    tok_nver = np.zeros(n, np.int32)
    rw = np.empty(R)
    rk = np.empty(R, np.int8)  # 1 = miss (fetch initiator), 2 = coalesced waiter
    nw = 0
    cnt = np.zeros(8, np.int64)
    es_med = es_ms / 1000.0
    sr_med = sr_ms / 1000.0
    pu_med = push_ms / 1000.0
    for q in range(R):
        r = order[q]
        tr = t[r]
        if r < n:
            i = r
            e = tok_edge[i]
            first = True
        else:
            i = mv_tok[r - n]
            e = mv_edge[r - n]
            first = False
        k = tok_ep[i]
        sh = e % S
        ekey = e * KB + k
        h = _find(keys, ekey, mask)
        wait = 0.0
        kind = 0
        if mode == 2 and first:
            # stapled root on the first request: verify and install (or replace a pending fetch) at once
            if keys[h] == -1 or vals[h] > tr:
                keys[h] = ekey
                vals[h] = tr
                flag[h] = 1
                cnt[4] += 1
                tok_nver[i] += 1
        elif keys[h] != -1 and (mode != 1 or flag[h] == 1 or vals[h] <= tr):
            if vals[h] > tr:
                wait = vals[h] - tr
                kind = 2
                cnt[5] += 1
        else:
            # root for this epoch not usable at this edge yet
            use_bundle = False
            pushed_bundle = False
            if mode == 3 or mode == 4:
                p = ep_period[k]
                ba = per_avail[p]
                if mode == 4:
                    ba = ba + _lognorm(TYPE_BUNDLE + e * KB + p, salt + 3, pu_med, push_sig)
                    if tr >= ba:
                        pushed_bundle = True
                elif tr >= ba:
                    use_bundle = True
            if pushed_bundle:
                pass
            elif use_bundle:
                bkey = TYPE_BUNDLE + e * KB + ep_period[k]
                hb = _find(keys, bkey, mask)
                if keys[hb] != -1:
                    if vals[hb] > tr:
                        wait = vals[hb] - tr
                        kind = 2
                        cnt[5] += 1
                else:
                    es = _lognorm(bkey, salt, es_med, es_sig)
                    skey = TYPE_BUNDLE + TYPE_SHIELD + sh * KB + ep_period[k]
                    hs = _find(keys, skey, mask)
                    arr_sh = tr + es / 2
                    if keys[hs] == -1:
                        sr = _lognorm(skey, salt + 1, sr_med, sr_sig)
                        keys[hs] = skey
                        vals[hs] = arr_sh + sr
                        cnt[3] += 1
                        F = es + sr
                    elif vals[hs] > arr_sh:
                        F = vals[hs] - arr_sh + es
                    else:
                        F = es
                    keys[hb] = bkey
                    vals[hb] = tr + F
                    flag[hb] = 1
                    wait = F
                    kind = 1
                    cnt[2] += 1
                    tok_nver[i] += 1
            else:
                push_av = 1e300
                if mode == 1:
                    if keys[h] == -1:
                        push_av = ep_issue[k] + _lognorm(ekey, salt + 2, pu_med, push_sig)
                    else:
                        push_av = vals[h]
                if push_av <= tr:
                    keys[h] = ekey
                    vals[h] = push_av
                else:
                    es = _lognorm(ekey, salt, es_med, es_sig)
                    skey = TYPE_SHIELD + sh * KB + k
                    hs = _find(keys, skey, mask)
                    arr_sh = tr + es / 2
                    if mode == 1:
                        sh_av = ep_issue[k] + 0.5 * _lognorm(skey, salt + 2, pu_med, push_sig)
                        F = es if sh_av <= arr_sh else min(es + _lognorm(skey, salt + 1, sr_med, sr_sig), sh_av - arr_sh + es)
                    elif keys[hs] == -1:
                        sr = _lognorm(skey, salt + 1, sr_med, sr_sig)
                        keys[hs] = skey
                        vals[hs] = arr_sh + sr
                        cnt[1] += 1
                        F = es + sr
                    elif vals[hs] > arr_sh:
                        F = vals[hs] - arr_sh + es
                    else:
                        F = es
                    avail = min(push_av, tr + F)
                    keys[h] = ekey
                    vals[h] = avail
                    flag[h] = 1
                    wait = avail - tr
                    kind = 1
                    if mode == 1:
                        cnt[6] += 1
                    cnt[0] += 1
                    tok_nver[i] += 1
        if kind > 0:
            tok_wait[i] += wait
            rw[nw] = wait
            rk[nw] = kind
            nw += 1
    cnt[7] = R
    return tok_wait, tok_nver, rw[:nw], rk[:nw], cnt


# ------------------------------------------------------------------ epoch policies
@njit(cache=True)
def epochs_fixed(arr, delta, nmax):
    """Aligned timer epochs [k*delta, (k+1)*delta) plus a count trigger nmax.  Returns tok_ep, ep_close, ep_N."""
    n = arr.size
    tok_ep = np.empty(n, np.int64)
    close = np.empty(n)
    N = np.empty(n, np.int64)
    k = -1
    cur = -1
    cnt = 0
    for i in range(n):
        g = np.int64(math.floor(arr[i] / delta))
        if g != cur or cnt >= nmax:
            if k >= 0 and cnt >= nmax and g == cur:
                close[k] = arr[i - 1]
            k += 1
            cur = g
            cnt = 0
            close[k] = (g + 1) * delta
        tok_ep[i] = k
        cnt += 1
        N[k] = cnt
    return tok_ep, close[:k + 1], N[:k + 1]


@njit(cache=True)
def epochs_wc(arr, t_tok, t_sign):
    n = arr.size
    tok_ep = np.empty(n, np.int64)
    close = np.empty(n)
    N = np.empty(n, np.int64)
    busy = -1e300
    i = 0
    k = 0
    while i < n:
        C = max(arr[i], busy)
        j = i
        while j < n and arr[j] <= C:
            tok_ep[j] = k
            j += 1
        close[k] = C
        N[k] = j - i
        busy = C + (j - i) * t_tok + t_sign
        i = j
        k += 1
    return tok_ep, close[:k], N[:k]


@njit(cache=True)
def choose_delta(lam, grid, lx, lmf, t_tok, t_sign, slo, nmax):
    """argmin_{Delta in grid} Delta/2 + lam*Delta*t_tok + t_sign + M(lam*Delta)*F(lam*Delta)
    s.t. p99 issuance wait 0.99*Delta + t_build + t_sign <= slo, signer capacity t_build + t_sign <= Delta,
    expected batch lam*Delta <= nmax (size budget).  lmf = log(M*F) tabulated on lx = log(x)."""
    best = -1
    bv = 1e300
    for g in range(grid.size):
        d = grid[g]
        x = lam * d
        tb = x * t_tok
        if 0.99 * d + tb + t_sign > slo or tb + t_sign > d or x > nmax:
            continue
        lxv = math.log(max(x, 1e-12))
        if lxv <= lx[0]:
            mf = math.exp(lmf[0])
        elif lxv >= lx[-1]:
            mf = math.exp(lmf[-1])
        else:
            j = np.searchsorted(lx, lxv)
            a = (lxv - lx[j - 1]) / (lx[j] - lx[j - 1])
            mf = math.exp(lmf[j - 1] * (1 - a) + lmf[j] * a)
        v = d / 2 + tb + t_sign + mf
        if v < bv:
            bv = v
            best = g
    if best < 0:
        return grid[0]
    return grid[best]


@njit(cache=True)
def epochs_adaptive(arr, grid, lx, lmf, t_tok, t_sign, slo, nmax, alpha, lam0, t_start):
    """Per-tenant adaptive controller: EWMA rate estimate, choose Delta at every epoch close; aligned timer
    from the previous close; empty epochs are skipped (no root); count trigger nmax.
    Returns tok_ep, ep_close, ep_N, ep_delta."""
    n = arr.size
    tok_ep = np.empty(n, np.int64)
    close = np.empty(n)
    N = np.empty(n, np.int64)
    dl = np.empty(n)
    lam = lam0
    delta = choose_delta(lam, grid, lx, lmf, t_tok, t_sign, slo, nmax)
    last = t_start
    C = t_start + delta
    i = 0
    k = 0
    while i < n:
        if arr[i] >= C:
            C = C + delta * (math.floor((arr[i] - C) / delta) + 1)
        j = i
        while j < n and arr[j] < C and (j - i) < nmax:
            tok_ep[j] = k
            j += 1
        cl = C if (j - i) < nmax else arr[j - 1]
        close[k] = cl
        N[k] = j - i
        dl[k] = delta
        lam = (1 - alpha) * lam + alpha * (j - i) / max(cl - last, 1e-6)
        last = cl
        delta = choose_delta(lam, grid, lx, lmf, t_tok, t_sign, slo, nmax)
        C = cl + delta
        i = j
        k += 1
    return tok_ep, close[:k], N[:k], dl[:k]


@njit(cache=True)
def issue_times(close, N, t_tok, t_sign):
    """Single signer per tenant/shard: epochs are processed FIFO; issue = max(close, prev done) + build + sign."""
    out = np.empty(close.size)
    done = -1e300
    for k in range(close.size):
        st = max(close[k], done)
        done = st + N[k] * t_tok + t_sign
        out[k] = done
    return out


# ------------------------------------------------------------------ costs
class Costs:
    """Crypto costs from the native OpenSSL 3.5.4 CSVs (primary) or the Python E1 CSV (secondary)."""

    def __init__(self, results_dir, backend="native", root_signer="ML-DSA-44", n=16):
        import pandas as pd
        self.backend = backend
        self.n = n
        nat = pd.read_csv(os.path.join(results_dir, "native_sig_agg.csv"))
        pv = pd.read_csv(os.path.join(results_dir, "native_pathverify_agg.csv"))
        sname = {"ML-DSA-44": "ML-DSA-44", "ML-DSA-65": "ML-DSA-65", "SLH-DSA-128s": "SLH-DSA-SHA2-128s",
                 "SLH-DSA-128f": "SLH-DSA-SHA2-128f", "Hybrid-Ed25519+ML-DSA-44": None}[root_signer]
        sigb = {"ML-DSA-44": 2420, "ML-DSA-65": 3309, "SLH-DSA-128s": 7856, "SLH-DSA-128f": 17088,
                "Hybrid-Ed25519+ML-DSA-44": 2484}[root_signer]
        self.sig_bytes = sigb

        def nat_op(s, op):
            return float(nat[(nat.scheme == s) & (nat.op == op)].median_us.iloc[0]) * 1e-6

        if backend == "native":
            if sname is None:
                self.t_sign = nat_op("ML-DSA-44", "sign") + nat_op("ED25519", "sign")
                self.t_verify = nat_op("ML-DSA-44", "verify") + nat_op("ED25519", "verify")
            else:
                self.t_sign = nat_op(sname, "sign")
                self.t_verify = nat_op(sname, "verify")
            g = pv[(pv.impl == "evp") & (pv.op == "pathverify") & (pv.n == n)].sort_values("d")
            self.path_d = g.d.values.astype(int)
            self.path_s = g.ns_median.values * 1e-9
            th200 = float(pv[(pv.impl == "evp") & (pv.op == "th_200B") & (pv.n == n)].ns_median.iloc[0]) * 1e-9
            th64 = float(pv[(pv.impl == "evp") & (pv.op == "th_64B") & (pv.n == n)].ns_median.iloc[0]) * 1e-9
            iss = os.path.join(results_dir, "native_issuer_agg.csv")
            enc = 0.55e-6
            if os.path.exists(iss):
                ia = pd.read_csv(iss)
                r = ia[(ia.root_alg == "ML-DSA-44") & (ia.N == 16384) & (ia.n == 16)]
                if len(r):
                    enc = float(r.t_encode_us.iloc[0]) / 16384 * 1e-6
            self.t_tok = th200 + th64 + enc
        else:
            mp = pd.read_csv(os.path.join(results_dir, "micro_primitives.csv"))

            def py(s, op):
                return float(mp[(mp.scheme == s) & (mp.op == op)].median_us.iloc[0]) * 1e-6
            self.t_sign = py(root_signer, "sign")
            self.t_verify = py(root_signer, "verify")
            th = py("Th-n%d-tweak+hash" % n, "hash")
            th200 = py("Th-n%d-200B" % n, "hash")
            self.path_d = np.arange(0, 41)
            self.path_s = 6e-6 + th200 + self.path_d * th  # parse overhead ~6us (B1 python verify minus HMAC)
            self.t_tok = th200 + th + 3e-6
        self.sr_bytes = 4 + 4 + 8 + 4 + 4 + 1 + n + sigb + 40   # signed-root wire + 40 B HTTP framing

    def path_cost(self, d):
        d = np.asarray(d)
        idx = np.searchsorted(self.path_d, d)
        idx = np.clip(idx, 0, self.path_d.size - 1)
        if not np.all(self.path_d[idx] == np.minimum(d, self.path_d[-1])):
            raise ValueError("path verify cost not measured for some d: %s" % np.unique(d[self.path_d[idx] != d]))
        return self.path_s[idx]

    def bundle_bytes(self, m):
        return 16 + m * (20 + self.n) + self.sig_bytes + 40
