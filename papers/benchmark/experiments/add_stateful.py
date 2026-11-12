#!/usr/bin/env python3
"""add_stateful.py SIZES.csv  -- append size-only LMS/XMSS rows (idempotent). No timings: `timing: none`, `source: literature`.
Only sizes stated in research/lit/notes/lms2019rfc8554.md and xmss2018rfc8391.md. Flags: 'tabulated' (in the RFC table) or
'derived' (the note author's arithmetic from stated field lengths). Unstated values stay empty (never filled in here)."""
import os, sys
import pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
from pqsig.common import tag

# scheme, family, sig, sig_flag, pk, pk_flag, max_signatures, source note
ROWS = [
    ("LMS_SHA256_M32_H5_LMOTS_W8", "LMS", 1292, "derived", 56, "derived", 2**5, "lms2019rfc8554.md"),
    ("XMSS-SHA2_10_256", "XMSS", 2500, "tabulated", 68, "derived", 2**10, "xmss2018rfc8391.md"),
    ("XMSS-SHA2_16_256", "XMSS", 2692, "tabulated", None, "not stated", 2**16, "xmss2018rfc8391.md"),
    ("XMSS-SHA2_20_256", "XMSS", 2820, "tabulated", None, "not stated", 2**20, "xmss2018rfc8391.md"),
    ("XMSS-SHA2_10_512", "XMSS", 9092, "tabulated", None, "not stated", 2**10, "xmss2018rfc8391.md"),
]
p = sys.argv[1]
d = pd.read_csv(p)
d = d[d.family_kind != "stateful"]
t = tag()
new = pd.DataFrame([{**t, "scheme": s, "family": f, "sig_declared": sg, "length_public_key": pk, "family_kind": "stateful",
                     "sig_size_flag": sf, "pk_size_flag": pf, "max_signatures": ms, "timing": "none", "source": "literature",
                     "source_note": src, "is_rep": True, "class_members": 1, "variant_note": "stateful",
                     "sig_declared_note": "claimed NIST level not stated in note"} for s, f, sg, sf, pk, pf, ms, src in ROWS])
start = int(d.class_id.max()) + 1
new["class_id"] = range(start, start + len(new))
pd.concat([d, new], ignore_index=True).to_csv(p, index=False)
print(len(new), "stateful rows appended")
