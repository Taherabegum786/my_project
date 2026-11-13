#!/usr/bin/env python3
"""crosscheck_loss.py RAWDIR MACHINE -> RAWDIR/loss_crosscheck_<machine>.csv
Compares the measured share (real implementation, i.i.d. loss) with the closed forms of lib/pqsig/lossform.py (symmetric model).
z = (impl mean - closed) / SE_used with SE_used = max(SE_sample, SE_binom): SE_sample = sd over seeds / sqrt(seeds);
SE_binom = sqrt(closed (1-closed) / (seeds * N_msgs)) is the standard error if every message were an independent trial (it only matters in
near-deterministic cells where all seeds agree and SE_sample = 0). Both are written to the CSV; the rule is stated in summary.md.
Cells without a closed form (symbol span > 255, continuity, GE loss) are not compared."""
import os
import sys

import numpy as np
import pandas as pd
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "lib"))
from pqsig import lossform as LF          # noqa: E402
from pqsig.common import tag              # noqa: E402

raw, machine = sys.argv[1:3]
Y = yaml.safe_load(open(os.path.join(HERE, "profiles.yaml")))["common"]["protocol"]
res = pd.read_csv(os.path.join(raw, f"proto_results_{machine}.csv"))
al = pd.read_csv(os.path.join(raw, f"proto_alloc_{machine}.csv"))
iid = res[(res.loss_model == "iid") & (res.feasible == 1)]
g = iid.groupby(["profile", "pq", "mode", "M", "loss_p"]).share.agg(["mean", "std", "count"]).reset_index()
rows = []
T = tag()
for _, r in g.iterrows():
    a = al[(al.profile == r.profile) & (al.pq == r.pq) & (al["mode"] == r["mode"]) & (al.M == r.M)].iloc[0]
    n = int(r["mode"][6:]) if r["mode"].startswith("merkle") else 1
    d = dict(u=int(a.usable_slots_per_window), M=int(r.M), k=int(a.k), E=Y["epoch_windows_E"], n=n, feasible=bool(a.feasible))
    c = LF.share(r["mode"], r.loss_p, d)
    if c is None:
        continue
    se_s = r["std"] / np.sqrt(r["count"]) if r["count"] > 1 else 0.0
    se_b = float(np.sqrt(max(c * (1 - c), 0.0) / (r["count"] * Y["data_windows_N"])))
    se = max(se_s, se_b)
    diff = r["mean"] - c
    z = 0.0 if abs(diff) <= 1e-9 else (diff / se if se > 0 else float("inf"))
    rows.append({**T, "profile": r.profile, "pq": r.pq, "mode": r["mode"], "M": int(r.M), "loss_p": r.loss_p, "closed": c,
                 "impl_mean": r["mean"], "impl_sd": r["std"], "seeds": int(r["count"]), "se_sample": se_s, "se_binom": se_b, "se": se, "diff": diff, "z": z,
                 "beyond_3se": bool(abs(z) > 3)})
out = pd.DataFrame(rows)
out.to_csv(os.path.join(raw, f"loss_crosscheck_{machine}.csv"), index=False)
print(f"crosscheck: {len(out)} cells compared, {int(out.beyond_3se.sum())} beyond 3 SE, max |diff| = {out['diff'].abs().max():.4f}")
