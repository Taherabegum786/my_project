"""E7: root-fetch / signature-verification DoS against one edge.

python -m sim.dos --out ../results
Attacker sends A fake tokens/s for 60 s (Poisson), each naming a (tenant, epoch) drawn uniformly from the
edge's acceptance window (epochs within V_max + P of now; Delta = 1 s) - over all T tenants, the highest-rate
tenant only, or the lowest-rate tenant only.
A named epoch exists (has a signed root) with the probability that the tenant issued >= 1 token in it
(workload defaults, lam_bar = 2000).  Edge CPU uses native OpenSSL 3.5.4 costs.
Variants:
  naive            every request whose root is not cached triggers a fetch; 404s are not cached; no coalescing
  coalesce+neg     one in-flight fetch per (tenant, epoch); 404s negatively cached for 60 s
  staple_flood     each fake token carries a stapled root with an invalid signature (one verification each)
  staple_flood+rl  as above, with a per-client limit of 1 stapled-root verification/s (attacker uses 100 clients)
"""
import argparse
import csv
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sim.fleet_mc import Costs
from sim.workload import DEFAULTS, SEED, lognorm, tenant_rates


def run(variant, A, keyspace, costs, rng, dur=60.0, delta=1.0, neg_ttl=60.0, clients=100):
    p = DEFAULTS
    W = int((p["v_max_s"] + p["P_s"]) / delta)
    lam = tenant_rates(p["T"], p["alpha_t"], p["lam_bar"])
    pexist = 1 - np.exp(-lam * delta)
    n = rng.poisson(A * dur)
    t = np.sort(rng.uniform(0, dur, n))
    if keyspace == "all_tenants":
        ten = rng.integers(0, p["T"], n)
    elif keyspace == "top_tenant":
        ten = np.zeros(n, np.int64)
    else:  # lowest-rate tenant: most named epochs do not exist (404)
        ten = np.full(n, p["T"] - 1, np.int64)
    ep = rng.integers(0, W, n)
    # existence is a property of the key (not of the request): derived from a per-key hash
    key = ten.astype(np.int64) * (W + 1) + ep
    u = (np.frombuffer(np.random.default_rng(SEED).bytes(8), np.uint64)[0] ^ key.astype(np.uint64)) * np.uint64(0x9E3779B97F4A7C15)
    ukey = (u >> np.uint64(11)).astype(np.float64) / 2.0 ** 53
    exists = ukey < pexist[ten]
    rtt = lognorm(rng, p["rtt_es_ms"], n) + lognorm(rng, p["rtt_sr_ms"], n)
    ready, neg, inflight = {}, {}, {}
    fetches = verifs = 0
    cli = rng.integers(0, clients, n)
    last_staple = {}
    for i in range(n):
        k, ti = int(key[i]), t[i]
        if variant.startswith("staple_flood"):
            if variant.endswith("+rl"):
                if ti - last_staple.get(cli[i], -1e9) < 1.0:
                    continue  # over the per-client staple limit: rejected without verification
                last_staple[cli[i]] = ti
            verifs += 1      # invalid stapled signature checked once, then rejected
            continue
        if ready.get(k, 1e300) <= ti:
            continue                       # root cached: only the (failing) path check is paid
        if variant == "coalesce+neg":
            if neg.get(k, -1.0) >= ti:
                continue
            if inflight.get(k, -1.0) > ti:
                continue                   # coalesced onto the in-flight fetch
        fetches += 1
        done = ti + rtt[i]
        inflight[k] = done
        if exists[i]:
            verifs += 1                    # each completed fetch verifies the root signature
            ready[k] = min(ready.get(k, 1e300), done)
        elif variant == "coalesce+neg":
            neg[k] = done + neg_ttl
    path = costs.path_cost(np.array([11]))[0]
    cpu = (verifs * costs.t_verify + n * path) / dur
    return dict(variant=variant, keyspace=keyspace, attack_rate=A, fake_tokens=n,
                root_fetches_per_s=fetches / dur, sig_verifs_per_s=verifs / dur, edge_cpu_frac_1core=cpu,
                p_epoch_exists=float(pexist[ten].mean()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="../results")
    ap.add_argument("--reps", type=int, default=5)
    a = ap.parse_args()
    c = Costs(a.out)
    rows = []
    for v in ("naive", "coalesce+neg", "staple_flood", "staple_flood+rl"):
        for ks in ("all_tenants", "top_tenant", "low_tenant"):
            for A in (1e2, 1e3, 1e4):
                rs = [run(v, A, ks, c, np.random.default_rng([SEED, r, int(A)])) for r in range(a.reps)]
                r0 = dict(rs[0])
                for k in ("root_fetches_per_s", "sig_verifs_per_s", "edge_cpu_frac_1core"):
                    vals = np.array([x[k] for x in rs])
                    r0[k] = vals.mean()
                    r0[k + "_sd"] = vals.std(ddof=1)
                r0["reps"] = a.reps
                rows.append(r0)
                print(v, ks, A, "%.1f fetch/s %.1f verif/s cpu %.3f" % (r0["root_fetches_per_s"], r0["sig_verifs_per_s"], r0["edge_cpu_frac_1core"]))
    with open(os.path.join(a.out, "dos.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
