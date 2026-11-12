#!/usr/bin/env python3
"""Part B. score.py SIZES_DECLARED.csv PROFILES.yaml OUT_ALL.csv
Scores every distinct size class (all levels). Representative = shortest scheme name of the class. Scores on DECLARED signature length."""
import os, sys
import pandas as pd, yaml
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
from pqsig.accounting import score
from pqsig.common import tag

MODES = ["full", "full_cert", "chain", "hybrid"]
sizes, prof, out = sys.argv[1:4]
d = pd.read_csv(sizes)
d = d[(d.family_kind == "pq") & d.is_rep]
Y = yaml.safe_load(open(prof)); P = Y["profiles"]
rows = []
for _, s in d.iterrows():
    for pn, p in P.items():
        for m in MODES:
            r = score(m, int(s.sig_declared), int(s.length_public_key), p, Y["common"])
            kd = None
            if pn.startswith("osnma"):
                kd = int(s.length_public_key) <= p["auth_budget"]["bytes"] if m == "full" else None
            rows.append({**tag(), "scheme": s.scheme, "family": s.family, "level": int(s.claimed_nist_level), "class_id": int(s.class_id),
                         "class_members": int(s.class_members), "variant_note": s.variant_note, "sig_declared": int(s.sig_declared),
                         "sig_observed_max": int(s.sig_observed_max), "pk_bytes": int(s.length_public_key),
                         "profile": pn, "basis": p["basis"], "budget": p["auth_budget"]["bytes"], "budget_derived": p["auth_budget"]["derived"],
                         "mode": m, "auth_bytes": r["auth_bytes"], "peak_bytes": r["peak_bytes"], "avg_bytes": r.get("avg_bytes"),
                         "anchor_bytes": r["anchor_bytes"], "anchor_msgs": r["anchor_msgs"], "share_of_budget": r["share"],
                         "fits": r["fits"], "frames_per_msg": r["frames_per_msg"], "msgs_needed": r["msgs_needed"],
                         "ttfa_s": r["ttfa_s"], "hdr_known": r["hdr_known"], "osnma_pk_fits_budget": kd})
pd.DataFrame(rows).to_csv(out, index=False)
print(len(rows), "rows,", d.class_id.nunique(), "classes")
