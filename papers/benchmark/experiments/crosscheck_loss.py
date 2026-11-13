#!/usr/bin/env python3
"""crosscheck_loss.py RAWDIR MACHINE -> RAWDIR/loss_crosscheck_<machine>.csv
Compares the measured share (real implementation, i.i.d. loss) of the MDS fragmentation modes with an independent closed form:
the sender's symbol placement is recomputed WITHOUT cryptography (modes.place_all on the allocation), giving c_{d,l} symbols of object d in
span slot d+l.  Given that the message's own slot arrived (the share is relative to received messages), the object decodes iff the symbols
of the received span slots number at least k:  P_d = P[ c_{d,0} + sum_{l>=1} c_{d,l} B_l >= k ],  B_l ~ Bernoulli(1-p) independent.
Expected share = mean over the measured messages of P_d.
z = (measured mean - closed form) / SE with SE = max(SE over seeds, binomial SE sqrt(c(1-c)/(seeds * mean received))): the binomial term
only matters where all seeds agree (disclosed rule, no hidden floor).  Lossless (p = 0) cells are NOT compared (both sides are trivially 1).
Not compared: repetition modes, Merkle, chain (no independent closed form in this pass), Gilbert-Elliott loss."""
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "lib")); sys.path.insert(0, HERE)
import run_proto as RP                       # noqa: E402
from pqsig.common import tag                 # noqa: E402
from pqsig.proto import modes as MO         # noqa: E402
from pqsig.proto.erasure import prob_k_of    # noqa: E402
from pqsig.proto.oqs import PQ               # noqa: E402


def closed_share(A, p):
    P = A.plan; G = P.G; k = A.k
    free = [max(0, A.slot_room(g)) for g in range(G)]
    reqs = []
    for d in range(G):
        nd, ns = A.obj_params(d)
        if ns >= k:
            reqs += [(d, j, d, A.W) for j in range(ns)]
    slots = MO.place_all(reqs, free, G, A.s + A.ov)
    cnt = {}
    for t in range(G):
        for d, j in slots[t]:
            cnt.setdefault(d, [0] * A.W)[t - d] += 1
    out = []
    for d in range(P.W0, P.W1):
        c = cnt.get(d)
        if c is None or sum(c) < k:
            out.append(0.0); continue
        base = c[0]                                         # own slot received (conditioning)
        out.append(prob_k_of(c[1:], max(0, k - base), p) if k - base > 0 else 1.0)
    return float(np.mean(out))


def main():
    raw, machine = sys.argv[1:3]
    res = pd.read_csv(os.path.join(raw, f"proto_results_{machine}.csv"))
    sel = res[(res.loss_model == "iid") & (res.loss_p > 0) & (res.feasible == 1) & res["mode"].str.contains("mds") & res["mode"].str.match(r"^(frag|hyb)_")]
    g = sel.groupby(["profile", "pq", "mode", "loss_p"]).agg(mean=("share", "mean"), std=("share", "std"), count=("share", "count"), recv=("received", "mean")).reset_index()
    rows = []; T = tag(); cache = {}
    for _, r in g.iterrows():
        key = (r.profile, r.pq, r["mode"])
        if key not in cache:
            plan = RP.plan_for(r.profile, r.pq); cache[key] = MO.Alloc(r.pq, r["mode"], plan, PQ(r.pq).sig_len)
        c = closed_share(cache[key], r.loss_p)
        se_s = r["std"] / np.sqrt(r["count"]) if r["count"] > 1 else 0.0
        se_b = float(np.sqrt(max(c * (1 - c), 0.0) / (r["count"] * max(1.0, r.recv))))
        se = max(se_s, se_b); diff = r["mean"] - c
        z = 0.0 if abs(diff) <= 1e-9 else (diff / se if se > 0 else float("inf"))
        rows.append({**T, "profile": r.profile, "pq": r.pq, "mode": r["mode"], "loss_p": r.loss_p, "closed": c, "impl_mean": r["mean"], "impl_sd": r["std"],
                     "seeds": int(r["count"]), "mean_received": r.recv, "se_sample": se_s, "se_binom": se_b, "se": se, "diff": diff, "z": z, "beyond_3se": bool(abs(z) > 3),
                     "zero_seed_se_nonzero_diff": bool(se_s == 0 and abs(diff) > 1e-9)})
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(raw, f"loss_crosscheck_{machine}.csv"), index=False)
    print(f"crosscheck: {len(out)} cells compared (MDS fragmentation, iid p>0), {int(out.beyond_3se.sum())} beyond 3 SE, max |diff| = {out['diff'].abs().max():.4f}")


if __name__ == "__main__":
    main()
