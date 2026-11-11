#!/usr/bin/env python3
"""Part C. run_lossmodel.py OUT.csv [SEEDS] [NMSG]. Cited-parameter scenarios (no liboqs needed):
 frag13: k=13, sig=666 B (FN-DSA k from darzi2026a; Falcon-512 sig from junquera2023assessment)
 frag34: k=34, sig=2420 B (ML-DSA k from darzi2026a; Dilithium2 sig from junquera2023assessment)
 chain anchor = 324 B (darzi2026a). Assumed (not cited): r=2 cycles, d=2, E=20, a=2, key=16 B, slot=160 ms (SIB1 period)."""
import csv, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
from pqsig import lossmodel
from pqsig.common import tag

out = sys.argv[1]
seeds = int(sys.argv[2]) if len(sys.argv) > 2 else 20
n = int(sys.argv[3]) if len(sys.argv) > 3 else 5000
R, D, E, A, KEY, TAG, ANCHOR, SLOT_MS = 2, 2, 20, 2, 16, 16, 324, 160
rows = []
for scen, k, sig in (("frag13", 13, 666), ("frag34", 34, 2420)):
    deadline = R * k
    for p in (0, .05, .10, .15, .20, .25, .30):
        for seed in range(seeds):
            for scheme in ("fragmented", "chain"):
                kw = dict(k=k, r=R, sig=sig, hdr=0) if scheme == "fragmented" else dict(d=D, E=E, a=A, tag=TAG, key=KEY, anchor=ANCHOR)
                res = lossmodel.run(scheme, p, 1000 * seed + int(p * 100) + k, n, deadline, **kw)
                rows.append({**tag(), "scenario": scen, "scheme": scheme, "loss": p, "seed": seed, "n_msgs": n,
                             "deadline_slots": deadline, "slot_ms": SLOT_MS, **res,
                             "p95_ms": res["p95_slots"] * SLOT_MS})
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows), "rows")
