"""Discrete-event simulator (heapq) used as an internal-consistency check of fleet_mc (sim_validate.csv).

Independent implementation: own RNG streams (no hashing, no shared kernel), explicit FETCH_DONE / PUSH events and
waiter lists.  It replays every root-relevant request (each session's first request and each re-route request);
the remaining segment requests stay on an edge whose root is already cached and cannot wait.
"""
import heapq
import math

import numpy as np

from sim.workload import SEED, lognorm, nhpp, tenant_phases, tenant_rates, zipf_shares

REQ, DONE = 0, 1


def run_des(sim, rep, delta, mode, t0, t1):
    p, c = sim.p, sim.c
    E, S = sim.E, sim.S
    rng0 = np.random.default_rng(SEED + 1000 * rep)
    w = zipf_shares(E, p["alpha_e"], rng0)           # same edge shares / tenant rates as the MC (workload, not randomness of the run)
    lam = tenant_rates(p["T"], p["alpha_t"], p["lam_bar"])
    phase = tenant_phases(p["T"], rng0)
    rng = np.random.default_rng([SEED + 1000 * rep, 555])
    P = p["P_s"]
    ev = []
    seq = 0
    W_sum = 0.0
    ntok = 0
    tok_wait = {}
    for tnt in range(p["T"]):
        arr = nhpp(rng, lam[tnt], p["diurnal_a"], phase[tnt], t0, t1)
        if arr.size == 0:
            continue
        ep = np.floor(arr / delta).astype(np.int64)
        # FIFO signer per tenant
        done = -1e300
        issue = {}
        for k in np.unique(ep):
            Nk = int((ep == k).sum())
            st = max((k + 1) * delta, done)
            done = st + Nk * c.t_tok + c.t_sign
            issue[k] = done
        for i in range(arr.size):
            k = int(ep[i])
            ti = issue[k]
            W_sum += ti - arr[i]
            tid = (tnt, ntok)
            ntok += 1
            tok_wait[tid] = 0.0
            e = int(rng.choice(E, p=w))
            d0 = float(lognorm(rng, p["first_req_ms"], 1)[0])
            K = int(rng.geometric(1.0 / p["K_mean"]))
            heapq.heappush(ev, (ti + d0, seq, REQ, (tid, tnt, k, e, True, ti))); seq += 1
            nsw = int(rng.binomial(K, p["p_move"]))
            for _ in range(nsw):
                off = (math.floor(rng.uniform() * K) + 1) * p["seg_interval_s"]
                e2 = int(rng.choice(E, p=w))
                heapq.heappush(ev, (ti + d0 + off, seq, REQ, (tid, tnt, k, e2, False, ti))); seq += 1
    cache = {}      # (edge, tnt, key) -> ready time, or list of waiters while pending
    scache = {}     # shield-level
    push_at = {}    # (edge, tnt, k) -> push arrival (sampled lazily, once)
    misses = 0

    def es():
        return float(lognorm(rng, sim.es, 1)[0])

    def sr():
        return float(lognorm(rng, sim.sr, 1)[0])

    def fetch(t, edge, tnt, key, skey_tag):
        nonlocal misses, seq
        misses += 1
        rtt = es()
        sh = edge % S
        sk = (sh, tnt, skey_tag)
        at_sh = t + rtt / 2
        sv = scache.get(sk)
        if sv is None:
            ready_sh = at_sh + sr()
            scache[sk] = ready_sh
        else:
            ready_sh = max(sv, at_sh)
        return ready_sh + rtt / 2

    while ev:
        t, _, typ, data = heapq.heappop(ev)
        if typ == DONE:
            ck = data
            waiters = cache[ck]
            cache[ck] = t
            for (tid, tr) in waiters:
                tok_wait[tid] += t - tr
            continue
        tid, tnt, k, e, first, ti = data
        ck = (e, tnt, ("E", k))
        st = cache.get(ck)
        if mode == "pull_staple" and first:
            if not isinstance(st, float) or st > t:
                if isinstance(st, list):   # pending fetch: the stapled root resolves it now
                    for (tid2, tr2) in st:
                        tok_wait[tid2] += t - tr2
                cache[ck] = t
            continue
        if isinstance(st, float):
            continue   # cached (ready times are always <= now once stored as float)
        if isinstance(st, list):
            st.append((tid, t))
            continue
        # not present: rollup / push checks
        if mode in ("pull_rollup", "push_rollup"):
            per = math.floor(((k + 1) * delta) / P)
            bav = (per + 1) * P + c.t_sign
            if mode == "push_rollup":
                bk = (e, tnt, ("Bp", per))
                if bk not in push_at:
                    push_at[bk] = bav + float(lognorm(rng, sim.pu, 1)[0])
                if t >= push_at[bk]:
                    continue
            elif t >= bav:
                bkey = (e, tnt, ("B", per))
                bs = cache.get(bkey)
                if isinstance(bs, float):
                    continue
                if isinstance(bs, list):
                    bs.append((tid, t))
                    continue
                ready = fetch(t, e, tnt, bkey, ("B", per))
                cache[bkey] = [(tid, t)]
                heapq.heappush(ev, (ready, seq, DONE, bkey)); seq += 1
                continue
        if mode == "push":
            pk = (e, tnt, k)
            if pk not in push_at:
                push_at[pk] = ti + float(lognorm(rng, sim.pu, 1)[0])
            pa = push_at[pk]
            if pa <= t:
                cache[ck] = pa
                continue
            rtt = es()
            sk = (e % S, tnt, ("E", k))
            if sk not in scache:
                scache[sk] = ti + 0.5 * float(lognorm(rng, sim.pu, 1)[0])
            at_sh = t + rtt / 2
            via = rtt if scache[sk] <= at_sh else min(rtt + sr(), scache[sk] - at_sh + rtt)
            misses += 1
            ready = min(pa, t + via)
            cache[ck] = [(tid, t)]
            heapq.heappush(ev, (ready, seq, DONE, ck)); seq += 1
            continue
        ready = fetch(t, e, tnt, ck, ("E", k))
        cache[ck] = [(tid, t)]
        heapq.heappush(ev, (ready, seq, DONE, ck)); seq += 1
    D = (W_sum + sum(tok_wait.values())) / ntok
    return dict(miss_per_token=misses / ntok, issue_wait_mean_s=W_sum / ntok, D_mean_s=D, tokens=ntok)
