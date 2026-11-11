"""Seeded Monte-Carlo: fragmented signatures vs PQ-anchored chain over an i.i.d. loss channel.
One frame per slot (slot = one broadcast opportunity, e.g. one SIB1 period).

Fragmented: a message's signature is split in k fragments, sent as r carousel cycles (k*r slots).
  Verified iff every fragment has >=1 received copy and finishes within `deadline` slots.
  time = slot (1-based, from first frame) when the last distinct fragment first arrives.
  bytes sent per message = r * (sig + hdr*k).
Chain (TESLA-like): message i sent in slot i with tag; every slot also discloses a key. Verified iff the
  message frame is received, some key slot >= i+d is received, and one anchor of the epoch is received;
  time = max(first received key slot >= i+d, first received anchor slot of the epoch) - i + 1.
  Epoch = E slots, `a` anchors per epoch at evenly spaced slots starting at the epoch start.
  bytes sent per message = tag + key + a*anchor_bytes/E.
Both use the same `deadline` (slots). Reported per seed; bytes per verified = bytes sent / share verified.
"""
import numpy as np


def frag_sim(rng, p, k, r, n_msgs, deadline):
    rec = rng.random((n_msgs, r, k)) >= p           # copy c of fragment j received
    got = rec.any(axis=1)                            # n_msgs x k
    ok = got.all(axis=1)
    first_cycle = np.where(rec.any(axis=1), rec.argmax(axis=1), r)   # first cycle with copy
    t = (first_cycle * k + np.arange(k)[None, :] + 1).max(axis=1)
    ok &= t <= deadline
    return ok, t


def chain_sim(rng, p, n_msgs, d, E, a, deadline):
    T = n_msgs + d + 4 * deadline + E
    rec = rng.random(T) >= p
    nxt = np.full(T + 1, np.iinfo(np.int64).max // 4, dtype=np.int64)
    for s in range(T - 1, -1, -1):
        nxt[s] = s if rec[s] else nxt[s + 1]
    n_ep = (n_msgs + E - 1) // E + 1
    anchor_slots = (np.arange(n_ep)[:, None] * E + (np.arange(a)[None, :] * (E // a))).astype(int)
    arec = rng.random(anchor_slots.shape) >= p
    big = np.iinfo(np.int64).max // 4
    afirst = np.where(arec, anchor_slots, big).min(axis=1)
    i = np.arange(n_msgs)
    key_t = nxt[i + d]
    t = np.maximum(key_t, afirst[i // E]) - i + 1
    ok = rec[i] & (t <= deadline)
    return ok, t


def run(scheme, p, seed, n_msgs, deadline, **kw):
    rng = np.random.default_rng(seed)
    if scheme == "fragmented":
        k, r, sig, hdr = kw["k"], kw["r"], kw["sig"], kw.get("hdr", 0)
        ok, t = frag_sim(rng, p, k, r, n_msgs, deadline)
        sent = r * (sig + hdr * k)
    else:
        d, E, a = kw["d"], kw["E"], kw["a"]
        ok, t = chain_sim(rng, p, n_msgs, d, E, a, deadline)
        sent = kw["tag"] + kw["key"] + a * kw["anchor"] / E
    share = ok.mean()
    return {"share_verified": share,
            "bytes_sent_per_msg": sent,
            "bytes_per_verified": sent / share if share > 0 else float("nan"),
            "p95_slots": float(np.percentile(t[ok], 95)) if ok.any() else float("nan"),
            "mean_slots": float(t[ok].mean()) if ok.any() else float("nan")}
