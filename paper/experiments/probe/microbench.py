#!/usr/bin/env python3
"""Feasibility probe: PQC primitive microbenchmark (Python bindings).

Backends:
  * pqcrypto 1.0.0 (PQClean/Rust-backed): ML-KEM-512/768/1024, ML-DSA-44/65/87,
    SLH-DSA (SHA2/SHAKE, 128/192/256, s/f).
  * cryptography (OpenSSL 3 backend): X25519, ECDSA P-256, Ed25519 baselines;
    X25519MLKEM768 hybrid is composed from X25519 + ML-KEM-768 exactly as in
    draft-ietf-tls-ecdhe-mlkem (client share = mlkem_pk||x25519_pk,
    server share = mlkem_ct||x25519_pk, ss = mlkem_ss||x25519_ss).

Timing: time.perf_counter_ns per call, single thread; reports median, mean,
p95 in microseconds. Python call overhead (~0.3-1 us) is included; for
C-level numbers see openssl_speed.sh.

Usage: python microbench.py OUT.csv [--quick]
"""
import csv
import os
import platform
import statistics
import sys
import time

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, ed25519, x25519

import pqcrypto.kem.ml_kem_512 as k512
import pqcrypto.kem.ml_kem_768 as k768
import pqcrypto.kem.ml_kem_1024 as k1024
import pqcrypto.sign as S

QUICK = "--quick" in sys.argv
MSG = os.urandom(32)  # ~ a TLS transcript hash


def timeit(fn, n):
    ts = []
    for _ in range(n):
        t0 = time.perf_counter_ns()
        fn()
        ts.append((time.perf_counter_ns() - t0) / 1000.0)
    ts.sort()
    return {
        "n": n,
        "median_us": statistics.median(ts),
        "mean_us": statistics.fmean(ts),
        "p95_us": ts[min(len(ts) - 1, int(0.95 * len(ts)))],
    }


rows = []


def add(alg, family, op, stats, pk=None, sk=None, ct=None, sig=None, ss=None):
    rows.append({
        "algorithm": alg, "family": family, "operation": op, **stats,
        "pk_bytes": pk, "sk_bytes": sk, "ct_bytes": ct, "sig_bytes": sig,
        "ss_bytes": ss, "backend": "pqcrypto-1.0.0" if family.startswith("pq") or family == "hybrid" else "cryptography/OpenSSL",
    })


def bench_kem(name, mod, n):
    pk, sk = mod.keygen()
    ct, ss = mod.encaps(pk)
    assert mod.decaps(sk, ct) == ss
    sizes = dict(pk=len(pk), sk=len(sk), ct=len(ct), ss=len(ss))
    add(name, "pq-kem", "keygen", timeit(mod.keygen, n), **sizes)
    add(name, "pq-kem", "encaps", timeit(lambda: mod.encaps(pk), n), **sizes)
    add(name, "pq-kem", "decaps", timeit(lambda: mod.decaps(sk, ct), n), **sizes)


def bench_sig(name, mod, n_sign, n_verify, n_keygen):
    pk, sk = mod.keygen()
    sig = mod.sign(sk, MSG)
    mod.verify(pk, MSG, sig)
    sizes = dict(pk=len(pk), sk=len(sk), sig=len(sig))
    add(name, "pq-sig", "keygen", timeit(mod.keygen, n_keygen), **sizes)
    add(name, "pq-sig", "sign", timeit(lambda: mod.sign(sk, MSG), n_sign), **sizes)
    add(name, "pq-sig", "verify", timeit(lambda: mod.verify(pk, MSG, sig), n_verify), **sizes)


def raw(pub):
    return pub.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)


def bench_classical(n):
    # X25519
    a = x25519.X25519PrivateKey.generate(); b = x25519.X25519PrivateKey.generate()
    bp = b.public_key()
    add("X25519", "classical-kex", "keygen", timeit(x25519.X25519PrivateKey.generate, n), pk=32, sk=32, ss=32)
    add("X25519", "classical-kex", "derive", timeit(lambda: a.exchange(bp), n), pk=32, sk=32, ss=32)
    # ECDSA P-256
    k = ec.generate_private_key(ec.SECP256R1()); kp = k.public_key()
    s = k.sign(MSG, ec.ECDSA(hashes.SHA256()))
    add("ECDSA-P256", "classical-sig", "keygen", timeit(lambda: ec.generate_private_key(ec.SECP256R1()), n), pk=65, sk=32, sig=len(s))
    add("ECDSA-P256", "classical-sig", "sign", timeit(lambda: k.sign(MSG, ec.ECDSA(hashes.SHA256())), n), pk=65, sk=32, sig=len(s))
    add("ECDSA-P256", "classical-sig", "verify", timeit(lambda: kp.verify(s, MSG, ec.ECDSA(hashes.SHA256())), n), pk=65, sk=32, sig=len(s))
    # Ed25519
    e = ed25519.Ed25519PrivateKey.generate(); ep = e.public_key(); es = e.sign(MSG)
    add("Ed25519", "classical-sig", "keygen", timeit(ed25519.Ed25519PrivateKey.generate, n), pk=32, sk=32, sig=64)
    add("Ed25519", "classical-sig", "sign", timeit(lambda: e.sign(MSG), n), pk=32, sk=32, sig=64)
    add("Ed25519", "classical-sig", "verify", timeit(lambda: ep.verify(es, MSG), n), pk=32, sk=32, sig=64)


def bench_hybrid(n):
    """X25519MLKEM768 as used in TLS 1.3 (client keyshare / server keyshare / client finish)."""
    def client_share():
        pk, sk = k768.keygen(); x = x25519.X25519PrivateKey.generate()
        return pk + raw(x.public_key()), (sk, x)

    def server_respond(share):
        pk, xpub = share[:1184], x25519.X25519PublicKey.from_public_bytes(share[1184:])
        ct, ss = k768.encaps(pk); y = x25519.X25519PrivateKey.generate()
        return ct + raw(y.public_key()), ss + y.exchange(xpub)

    def client_finish(state, resp):
        sk, x = state
        ss = k768.decaps(sk, resp[:1088])
        return ss + x.exchange(x25519.X25519PublicKey.from_public_bytes(resp[1088:]))

    share, st = client_share()
    resp, ss_s = server_respond(share)
    assert client_finish(st, resp) == ss_s
    sz = dict(pk=len(share), ct=len(resp), ss=len(ss_s))
    add("X25519MLKEM768", "hybrid", "client_keygen", timeit(client_share, n), **sz)
    add("X25519MLKEM768", "hybrid", "server_encaps", timeit(lambda: server_respond(share), n), **sz)
    add("X25519MLKEM768", "hybrid", "client_decaps", timeit(lambda: client_finish(st, resp), n), **sz)


def main():
    out = [a for a in sys.argv[1:] if not a.startswith("--")]
    out = out[0] if out else "probe_microbench.csv"
    f = 0.1 if QUICK else 1.0
    n_fast = max(20, int(2000 * f))
    for name, mod in [("ML-KEM-512", k512), ("ML-KEM-768", k768), ("ML-KEM-1024", k1024)]:
        bench_kem(name, mod, n_fast)
    bench_hybrid(n_fast)
    bench_classical(n_fast)
    for v in ("44", "65", "87"):
        bench_sig(f"ML-DSA-{v}", getattr(S, f"ml_dsa_{v}"), n_fast // 2, n_fast, n_fast // 4)
    for h in ("sha2", "shake"):
        for lvl in ("128", "192", "256"):
            for var in ("f", "s"):
                mod = getattr(S, f"slh_dsa_{h}_{lvl}{var}")
                ns = 3 if var == "s" else 20
                nv = 50 if var == "f" else 200
                nk = 3 if var == "s" else 20
                if QUICK:
                    ns, nv, nk = 2, 10, 2
                bench_sig(f"SLH-DSA-{h.upper()}-{lvl}{var}", mod, ns, nv, nk)
    meta = f"{platform.processor() or platform.machine()} python{platform.python_version()}"
    with open(out, "w", newline="") as fh:
        cols = ["algorithm", "family", "operation", "n", "median_us", "mean_us", "p95_us",
                "pk_bytes", "sk_bytes", "ct_bytes", "sig_bytes", "ss_bytes", "backend"]
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader()
        for r in rows:
            w.writerow({k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items()})
    print(f"wrote {len(rows)} rows to {out} ({meta})")


if __name__ == "__main__":
    main()
