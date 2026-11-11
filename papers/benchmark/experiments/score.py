#!/usr/bin/env python3
"""Part B. score.py SIZES.csv PROFILES.yaml OUT.csv. Scores every (scheme, mode, profile)."""
import csv, os, sys
import pandas as pd, yaml
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
from pqsig.accounting import score
from pqsig.common import tag

MODES = ["full", "sig_cert", "fragmented", "chain", "hybrid"]
sizes, prof, out = sys.argv[1:4]
df = pd.read_csv(sizes)
df = df.drop_duplicates("scheme", keep="last")
P = yaml.safe_load(open(prof))["profiles"]
classical = df[df.scheme == "Ed25519"]
sig_c = int(classical.sig_bytes_max.iloc[0]) if len(classical) else None
rows = []
for _, s in df.iterrows():
    for pn, p in P.items():
        hdr = p["frag_hdr"] if isinstance(p["frag_hdr"], int) else 0
        for m in MODES:
            if m == "hybrid" and (sig_c is None or s.family == "classical"):
                continue
            r = score(m, int(s.sig_bytes_max), int(s.pk_bytes), sig_c, p["budget_bytes"], p["frame_payload"], hdr)
            rows.append({**tag(), "scheme": s.scheme, "family": s.family, "profile": pn, "profile_source": p["source"],
                         "mode": m, "sig_bytes": int(s.sig_bytes_max), "pk_bytes": int(s.pk_bytes),
                         "auth_bytes": r["auth_bytes"], "anchor_bytes": r["anchor_bytes"], "budget": p["budget_bytes"],
                         "share_of_budget": r["share"], "frames": r["frames"], "fits": r["fits"],
                         "frag_hdr_known": isinstance(p["frag_hdr"], int)})
pd.DataFrame(rows).to_csv(out, index=False)
print(f"wrote {len(rows)} rows")
