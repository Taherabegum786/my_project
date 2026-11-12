"""Closed forms (i.i.d. slot loss p) and a slot-level simulator (i.i.d. or Gilbert-Elliott) for broadcast authentication
under an EQUAL channel budget: every scheme gets M slots per message (same slots/s, same bytes/slot), message rate 1/M per slot.

Notation: q = 1-p. S signature bytes, C auth bytes per slot, k = ceil(S/C) fragments, k_a = ceil((S+commit+ts)/C) anchor fragments,
E messages per epoch, r_a anchor repetitions (derived, see chain), w key windows, n messages per Merkle batch.

 frag_rep   r = floor(M/k) repetitions of all k fragments.        P = (1 - p^r)^k                      (needs M >= k)
 frag_mds   M erasure-coded fragments, any k reconstruct.          P = P[Bin(M, q) >= k]                (needs M >= k)
 chain      t = M - a_s tag-copy slots per message;  P = (1 - p^t) (1 - p^{t w}) (1 - p^{r_a})^{k_a}
            (message copy received) x (some key-carrying copy in the next w windows) x (anchor fragments all covered)
            a_s = ceil(2 k_a / E) slots per message are reserved for the anchor, so the epoch has E a_s anchor slots and
            r_a = floor(E a_s / k_a) >= 2 repetitions (all reserved slots are used: equal channel use)
 merkle_rep batch of n messages, t = M - ceil(2k/n) message copies; the n(M-t) spare slots carry the batch signature,
            r_s = floor(n(M-t)/k) repetitions.                      P = (1 - p^t) (1 - p^{r_s})^k
 merkle_mds same but erasure-coded:                                  P = (1 - p^t) P[Bin(n(M-t), q) >= k]
Messages whose verification never completes count as missing the deadline (p95 is over ALL messages).
TTA95 (slots, from the start of the message's window, worst message of a batch for merkle):
 frag_rep  rho*k with rho = least rho<=r with (1-p^rho)^k >= .95        frag_mds  least s<=M with P[Bin(s,q)>=k] >= .95
 chain     M + u*M/t with u least with (1-p^t)(1-p^u)(1-p^{r_a})^{k_a} >= .95 (u <= t w)
 merkle    n M + rho*k*M/(M-t)  (rep)  or  n M + s*M/(M-t) (mds), with the (1-p^t) factor included
 inf = the scheme cannot reach 95% at that loss.
"""
import math
import numpy as np
from math import comb


def binom_sf(n, k, q):
    """P[Bin(n,q) >= k]"""
    if k <= 0:
        return 1.0
    if n < k:
        return 0.0
    return float(sum(comb(n, j) * q ** j * (1 - q) ** (n - j) for j in range(k, n + 1)))


def params(S, C, M, commit=16, ts=4, E=20, r_a_min=2, w=2, n=8):
    k = math.ceil(S / C); ka = math.ceil((S + commit + ts) / C)
    a_s = math.ceil(ka * r_a_min / E)            # slots per message reserved for the anchor (>= r_a_min repetitions per epoch)
    return dict(S=S, C=C, M=M, k=k, ka=ka, E=E, r_a=(E * a_s) // ka, a_s=a_s, w=w, n=n,
                t_chain=M - a_s, t_mer=M - math.ceil(2 * k / n))


def P_closed(scheme, p, a):
    q = 1 - p; M, k = a["M"], a["k"]
    if scheme == "frag_rep":
        r = M // k
        return 0.0 if r < 1 else (1 - p ** r) ** k
    if scheme == "frag_mds":
        return 0.0 if M < k else binom_sf(M, k, q)
    if scheme == "chain":
        t = a["t_chain"]
        return 0.0 if t < 1 else (1 - p ** t) * (1 - p ** (t * a["w"])) * (1 - p ** a["r_a"]) ** a["ka"]
    t = a["t_mer"]; n = a["n"]
    if t < 1 or n * (M - t) < k:
        return 0.0
    if scheme == "merkle_rep":
        return (1 - p ** t) * (1 - p ** (n * (M - t) // k)) ** k
    if scheme == "merkle_mds":
        return (1 - p ** t) * binom_sf(n * (M - t), k, q)
    raise ValueError(scheme)


def tta95(scheme, p, a, target=0.95):
    q = 1 - p; M, k = a["M"], a["k"]
    if P_closed(scheme, p, a) < target:
        return math.inf
    if scheme == "frag_rep":
        for rho in range(1, M // k + 1):
            if (1 - p ** rho) ** k >= target: return rho * k
    if scheme == "frag_mds":
        for s in range(k, M + 1):
            if binom_sf(s, k, q) >= target: return s
    if scheme == "chain":
        t = a["t_chain"]
        for u in range(1, t * a["w"] + 1):
            if (1 - p ** t) * (1 - p ** u) * (1 - p ** a["r_a"]) ** a["ka"] >= target: return M + u * M / t
    t = a["t_mer"]; n = a["n"]
    if scheme == "merkle_rep":
        for rho in range(1, n * (M - t) // k + 1):
            if (1 - p ** t) * (1 - p ** rho) ** k >= target: return n * M + rho * k * M / (M - t)
    if scheme == "merkle_mds":
        for s in range(k, n * (M - t) + 1):
            if (1 - p ** t) * binom_sf(s, k, q) >= target: return n * M + s * M / (M - t)
    return math.inf


SCHEMES = ("frag_rep", "frag_mds", "chain", "merkle_rep", "merkle_mds")


# ---------------- simulation (cross-check and Gilbert-Elliott) ----------------
def loss_sequence(rng, N, p, burst_len=None):
    """Boolean array, True = slot lost. burst_len None -> i.i.d.; else Gilbert-Elliott with loss 1 in Bad, 0 in Good,
    mean Bad sojourn = burst_len slots, stationary P(Bad) = p."""
    if burst_len is None:
        return rng.random(N) < p
    if p <= 0: return np.zeros(N, bool)
    pbg = 1.0 / burst_len; pgb = pbg * p / (1 - p)
    out = []; tot = 0; bad = rng.random() < p
    while tot < N:
        m = max(64, int((N - tot) / max(1.0, burst_len + burst_len * (1 - p) / p)) * 2 + 64)
        g = rng.geometric(pgb, m); b = rng.geometric(pbg, m)
        for i in range(m):
            L = int(b[i] if bad else g[i])
            out.append((bad, L)); tot += L; bad = not bad
            if tot >= N: break
    return np.repeat(np.array([o[0] for o in out]), [o[1] for o in out])[:N]


def sim(scheme, p, a, n_msgs, rng, burst_len=None):
    """Share of messages verified. n_msgs must be a multiple of E and n."""
    M, k = a["M"], a["k"]
    if scheme in ("frag_rep", "frag_mds"):
        if M < k: return 0.0
        rec = ~loss_sequence(rng, n_msgs * M, p, burst_len).reshape(n_msgs, M)
        if scheme == "frag_mds":
            return float((rec.sum(1) >= k).mean())
        r = M // k
        cov = np.zeros((n_msgs, k), bool)
        for j in range(r * k):
            cov[:, j % k] |= rec[:, j]
        return float(cov.all(1).mean())
    if scheme == "chain":
        t, E, ka, ra, w = a["t_chain"], a["E"], a["ka"], a["r_a"], a["w"]
        if t < 1: return 0.0
        nm = (n_msgs // E) * E
        rec = ~loss_sequence(rng, nm * M, p, burst_len).reshape(nm, M)
        tag = rec[:, :t].any(1)
        res = rec[:, t:].reshape(nm // E, -1)             # reserved slots of each epoch, in order
        need = ka * ra
        cov = np.zeros((nm // E, ka), bool)
        for j in range(need):
            cov[:, j % ka] |= res[:, j]
        anc = np.repeat(cov.all(1), E)
        key_any = rec[:, :t].any(1)                       # window carries key copies in its t tag slots
        keyw = np.zeros(nm, bool)
        for off in range(1, w + 1):
            keyw[:nm - off] |= key_any[off:]
        return float((tag & keyw & anc).mean())
    t, n = a["t_mer"], a["n"]
    if t < 1 or n * (M - t) < k: return 0.0
    nm = (n_msgs // n) * n
    rec = ~loss_sequence(rng, nm * M, p, burst_len).reshape(nm // n, n, M)
    tag = rec[:, :, :t].any(2)
    spare = rec[:, :, t:].reshape(nm // n, -1)
    if scheme == "merkle_mds":
        sig = spare.sum(1) >= k
    else:
        cov = np.zeros((nm // n, k), bool)
        for j in range((spare.shape[1] // k) * k):
            cov[:, j % k] |= spare[:, j]
        sig = cov.all(1)
    return float((tag & sig[:, None]).mean())
