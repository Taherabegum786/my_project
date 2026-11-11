#!/usr/bin/env python3
"""Part C. run_lossmodel.py OUT.csv SWEEP_OUT.csv [SIZES.csv] [SEEDS] [NMSG]
Scenarios (k fragments from darzi2026a; frames-per-signature is not recomputed from sizes):
 cited13 / cited34: sig 666 / 2420 B (junquera2023assessment), anchor 324 B (darzi2026a)
 oqs13 / oqs34    : sig = liboqs-measured Falcon-512 / ML-DSA-44 sig_bytes_max; anchor = measured MAYO_1 sig + commit(16) + ts(4)
                    (only when SIZES.csv holds those rows)
Assumed (not cited): r=2 cycles, d=2, E=20, a=2, key=16 B, slot=160 ms (SIB1 period), deadline = r*k slots.
Sweep: one-at-a-time over r in {1,2,3}, d in {1,2,4}, E in {10,20,40}, a in {1,2,4}, at loss 0.05/0.10/0.30."""
import csv, os, sys
import pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
from pqsig import lossmodel
from pqsig.common import tag

out, sweep_out = sys.argv[1], sys.argv[2]
sizes = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] != "-" else None
seeds = int(sys.argv[4]) if len(sys.argv) > 4 else 20
n = int(sys.argv[5]) if len(sys.argv) > 5 else 5000
BASE = dict(R=2, D=2, E=20, A=2, KEY=16, TAG=16, SLOT_MS=160)
LOSSES = (0, .05, .10, .15, .20, .25, .30)

scen = [("cited13", 13, 666, 324), ("cited34", 34, 2420, 324)]
if sizes:
    df = pd.read_csv(sizes).drop_duplicates("scheme", keep="last").set_index("scheme")
    try:
        anc = int(df.loc["MAYO-1", "sig_bytes_max"]) + 16 + 4
        scen += [("oqs13", 13, int(df.loc["Falcon-512", "sig_bytes_max"]), anc),
                 ("oqs34", 34, int(df.loc["ML-DSA-44", "sig_bytes_max"]), anc)]
    except KeyError as e:
        print("missing scheme in sizes:", e, "- oqs scenarios skipped")


def cell(name, k, sig, anchor, p, seed, R, D, E, A, extra=None):
    deadline = R * k
    rows = []
    for scheme in ("fragmented", "chain"):
        kw = dict(k=k, r=R, sig=sig, hdr=0) if scheme == "fragmented" else dict(d=D, E=E, a=A, tag=BASE["TAG"], key=BASE["KEY"], anchor=anchor)
        res = lossmodel.run(scheme, p, 1000 * seed + int(p * 100) + k, n, deadline, **kw)
        rows.append({**tag(), "scenario": name, "scheme": scheme, "loss": p, "seed": seed, "n_msgs": n,
                     "sig_bytes": sig, "anchor_bytes": anchor, "k": k, "r": R, "d": D, "E": E, "a": A,
                     "deadline_slots": deadline, "slot_ms": BASE["SLOT_MS"], **res, "p95_ms": res["p95_slots"] * BASE["SLOT_MS"]})
    return rows

rows = []
for name, k, sig, anchor in scen:
    for p in LOSSES:
        for seed in range(seeds):
            rows += cell(name, k, sig, anchor, p, seed, BASE["R"], BASE["D"], BASE["E"], BASE["A"])
sw = []
sseeds, sn = max(seeds // 2, 10), n
for name, k, sig, anchor in scen:
    for var, vals in (("r", (1, 2, 3)), ("d", (1, 2, 4)), ("E", (10, 20, 40)), ("a", (1, 2, 4))):
        for v in vals:
            par = dict(R=BASE["R"], D=BASE["D"], E=BASE["E"], A=BASE["A"])
            par[{"r": "R", "d": "D", "E": "E", "a": "A"}[var]] = v
            for p in (.05, .10, .30):
                for seed in range(sseeds):
                    for r_ in cell(name, k, sig, anchor, p, seed, **par):
                        sw.append({**r_, "sweep_var": var, "sweep_val": v})
for path, rr in ((out, rows), (sweep_out, sw)):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rr[0])); w.writeheader(); w.writerows(rr)
print(len(rows), len(sw), "rows")
