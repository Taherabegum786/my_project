#!/usr/bin/env python3
"""make_sizes.py OQS_BENCH_BIN OBSERVED_TIMING.csv CLASSICAL_TIMING.csv OUT.csv
Declared sizes come from `oqs_bench --list-sizes` (OQS_SIG length_* fields); observed max signature length
comes from the timing CSV (largest of the benchmark's signatures of one 64 B message)."""
import io, os, subprocess, sys
import pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
from pqsig.common import tag
from pqsig.schemes import add_classes

binp, obs, cls, out = sys.argv[1:5]
d = pd.read_csv(io.StringIO(subprocess.check_output([binp, "--list-sizes"], text=True)))
d = d.rename(columns={"length_signature_declared": "sig_declared"})
o = pd.read_csv(obs)[["scheme", "sig_bytes_max", "iterations"]].rename(columns={"sig_bytes_max": "sig_observed_max"})
d = d.merge(o, on="scheme", how="left")
d["family_kind"] = "pq"
c = pd.read_csv(cls)
# Classical: standard encodings, not liboqs. Ed25519 sig 64; ECDSA P-256 raw r||s 64 (DER max 72, observed in timing CSV).
rows = [dict(scheme="Ed25519", claimed_nist_level=1, euf_cma=1, length_public_key=32, length_secret_key=32, sig_declared=64,
             sig_observed_max=int(c[c.scheme == "Ed25519"].sig_bytes_max.iloc[0]), iterations=int(c.iterations.iloc[0]), family_kind="classical", liboqs_version="n/a"),
        dict(scheme="ECDSA-P256", claimed_nist_level=1, euf_cma=1, length_public_key=65, length_secret_key=32, sig_declared=64,
             sig_observed_max=int(c[c.scheme == "ECDSA-P256"].sig_bytes_max.iloc[0]), iterations=int(c.iterations.iloc[0]), family_kind="classical", liboqs_version="n/a")]
d = pd.concat([d, pd.DataFrame(rows)], ignore_index=True)
d["sig_declared_note"] = d.scheme.map(lambda n: "raw r||s; DER max 72 B" if n == "ECDSA-P256" else "")
d = add_classes(d)
t = tag()
for k, v in t.items():
    d.insert(0, k, v)
d.to_csv(out, index=False)
print(len(d), "rows;", d[d.family_kind == "pq"].class_id.nunique(), "distinct PQ size classes")
