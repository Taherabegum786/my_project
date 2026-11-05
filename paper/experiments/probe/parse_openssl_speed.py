#!/usr/bin/env python3
"""Parse `openssl speed -kem-algorithms/-signature-algorithms` tables into CSV (us/op)."""
import csv
import sys

src, dst = sys.argv[1], sys.argv[2]
rows, kind = [], None
for line in open(src):
    parts = line.split()
    if not parts:
        continue
    if parts[0] == "keygen":
        kind = "kem" if "encaps" in parts else "sig"
        ops = ["keygen", "encaps", "decaps"] if kind == "kem" else ["keygen", "sign", "verify"]
        continue
    if kind and len(parts) >= 7 and parts[1].endswith("s"):
        alg = parts[0]
        try:
            # use the ops/s columns (more precise than the 1-us-resolution seconds columns)
            secs = [1.0 / float(p) for p in parts[4:7]]
        except ValueError:
            continue
        for op, s in zip(ops, secs):
            rows.append({"algorithm": alg, "kind": kind, "operation": op,
                         "us_per_op": round(s * 1e6, 2), "ops_per_s": round(1.0 / s, 1),
                         "backend": "openssl-3.6.0+oqsprovider-0.11.0 (docker, 1 core)"})
with open(dst, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["algorithm", "kind", "operation", "us_per_op", "ops_per_s", "backend"])
    w.writeheader(); w.writerows(rows)
print(f"wrote {len(rows)} rows to {dst}")
