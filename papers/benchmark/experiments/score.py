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
d = d[d.family_kind.isin(["pq", "stateful"]) & d.is_rep]
if "sig_size_flag" not in d: d = d.assign(sig_size_flag="", pk_size_flag="", max_signatures=float("nan"), timing="", source="")
d = d.fillna({"sig_size_flag": "", "pk_size_flag": "", "timing": "", "source": ""})
Y = yaml.safe_load(open(prof)); P = Y["profiles"]
rows = []
for _, s in d.iterrows():
    nopk = pd.isna(s.length_public_key)
    for pn, p in P.items():
        for m in MODES:
            if m == "full_cert" and nopk:
                continue  # needs the public key size, not stated in the literature note: row omitted, not guessed
            r = score(m, int(s.sig_declared), 0 if nopk else int(s.length_public_key), p, Y["common"])
            kd = None
            if pn.startswith("osnma"):
                kd = (int(s.length_public_key) <= p["auth_budget"]["bytes"] if m == "full" and not nopk else None)
            rows.append({**tag(), "scheme": s.scheme, "family": s.family, "level": None if pd.isna(s.claimed_nist_level) else int(s.claimed_nist_level), "family_kind": s.family_kind,
                         "sig_size_flag": s.sig_size_flag, "pk_size_flag": s.pk_size_flag, "max_signatures": s.max_signatures, "timing": s.timing or "measured", "source": s.source or "liboqs", "class_id": int(s.class_id),
                         "class_members": int(s.class_members), "variant_note": s.variant_note, "sig_declared": int(s.sig_declared),
                         "sig_observed_max": None if pd.isna(s.sig_observed_max) else int(s.sig_observed_max), "pk_bytes": None if nopk else int(s.length_public_key),
                         "profile": pn, "basis": p["basis"], "budget": p["auth_budget"]["bytes"], "budget_derived": p["auth_budget"]["derived"],
                         "mode": m, "auth_bytes": r["auth_bytes"], "peak_bytes": r["peak_bytes"], "avg_bytes": r.get("avg_bytes"),
                         "anchor_bytes": r["anchor_bytes"], "anchor_msgs": r["anchor_msgs"], "share_of_budget": r["share"],
                         "fits": r["fits"], "frames_per_msg": r["frames_per_msg"], "msgs_needed": r["msgs_needed"],
                         "ttfa_s": r["ttfa_s"], "hdr_known": r["hdr_known"], "osnma_pk_fits_budget": kd})
pd.DataFrame(rows).to_csv(out, index=False)
print(len(rows), "rows,", d.class_id.nunique(), "classes")
