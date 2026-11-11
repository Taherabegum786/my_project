"""Ed25519 and ECDSA P-256 baselines (python-cryptography / OpenSSL).
Usage: classical_bench.py OUT.csv [ITER] ; appends rows in the same schema as oqs_bench.c.
Note: Python call overhead is included; flagged by backend column."""
import csv
import os
import sys
import time

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, ed25519

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from pqsig.common import stats, tag  # noqa: E402

COLS = ["machine", "date", "git_commit", "backend", "scheme", "family", "iterations", "msg_bytes",
        "pk_bytes", "sk_bytes", "sig_bytes_max", "sig_bytes_mean"]
for op in ("keygen", "sign", "verify"):
    COLS += [f"{op}_{s}_us" for s in ("mean", "median", "p95", "p99", "std")]
    COLS += [f"{op}_frac_gt3ms", f"{op}_frac_gt100ms"]

MSG = bytes(range(256)) * 0 + b"\x5a" * 64


def timeit(fn, n):
    out = []
    for _ in range(n):
        t = time.perf_counter_ns()
        fn()
        out.append((time.perf_counter_ns() - t) / 1000.0)
    return out


def row_for(name, gen, signer, verifier, pk_raw, n):
    kg = timeit(gen, n)
    key = gen()
    sigs = []
    sg = []
    for _ in range(n):
        t = time.perf_counter_ns()
        s = signer(key, MSG)
        sg.append((time.perf_counter_ns() - t) / 1000.0)
        sigs.append(len(s))
    s = signer(key, MSG)
    vf = timeit(lambda: verifier(key, s, MSG), n)
    r = {**tag(), "backend": "python-cryptography", "scheme": name, "family": "classical",
         "iterations": n, "msg_bytes": len(MSG), "pk_bytes": len(pk_raw(key)),
         "sk_bytes": 32, "sig_bytes_max": max(sigs), "sig_bytes_mean": sum(sigs) / len(sigs)}
    for op, v in (("keygen", kg), ("sign", sg), ("verify", vf)):
        st = stats(v)
        for k, x in st.items():
            r[f"{op}_{k}_us"] = x
        r[f"{op}_frac_gt3ms"] = sum(x > 3000 for x in v) / len(v)
        r[f"{op}_frac_gt100ms"] = sum(x > 100000 for x in v) / len(v)
    return r


def main():
    out = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
    raw = serialization
    rows = [
        row_for("Ed25519", ed25519.Ed25519PrivateKey.generate,
                lambda k, m: k.sign(m), lambda k, s, m: k.public_key().verify(s, m),
                lambda k: k.public_key().public_bytes(raw.Encoding.Raw, raw.PublicFormat.Raw), n),
        row_for("ECDSA-P256", lambda: ec.generate_private_key(ec.SECP256R1()),
                lambda k, m: k.sign(m, ec.ECDSA(hashes.SHA256())),
                lambda k, s, m: k.public_key().verify(s, m, ec.ECDSA(hashes.SHA256())),
                lambda k: k.public_key().public_bytes(raw.Encoding.X962,
                                                      raw.PublicFormat.UncompressedPoint), n),
    ]
    new = not os.path.exists(out)
    with open(out, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        if new:
            w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
