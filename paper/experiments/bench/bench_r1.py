"""R1: M2 / B5s (stapled per-token ML-DSA-44) sizes and Python edge-verify cost, same claims as bench_tokens.

taskset -c 2 python -m bench.bench_r1 --out ../results [--no-timing]
-> token_sizes_r1.csv (M2 URL token, staple header, EMBER at N = 1, 2^5, 2^8 for comparison)
-> token_verify_r1.csv (Python; M2 cache hit / staple verify; EMBER warm d = 0 and d = 5 for the same harness)
"""
import argparse
import csv
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from baselines.stapled import HDR, StapledPerTokenEdge, StapledPerTokenIssuer
from bench.bench_tokens import BASE, NOW, T0, boot_median, mkclaims, timed_each
from ember.edge import EmberEdge
from ember.issuer import SignedRoot
from ember.merkle import leaf_hash, treehash_paths
from ember.signers import CTX_ROOT, make_signer
from ember.token import b64e, enc, encode_ember, to_signed_url


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="../results")
    ap.add_argument("--no-timing", action="store_true")
    ap.add_argument("--iters", type=int, default=5000)
    a = ap.parse_args()
    rows = []
    iss = StapledPerTokenIssuer()
    s = make_signer("ML-DSA-44", CTX_ROOT)
    for L in (40, 60, 120, 250):
        for ip in (0, 1):
            c = mkclaims(L, ip)
            tok, sig = iss.issue(c)
            staple_hdr = "%s: %s\r\n" % (HDR, b64e(sig))
            rows.append(dict(scheme="M2-B5s", log2N="", url_path_len=L, with_ip=ip, claims_bytes=len(enc(c)),
                             token_bytes=len(tok), signed_url_bytes=len(to_signed_url(BASE + c.url_prefix, tok)),
                             staple_raw_bytes=len(sig), staple_header_http11_bytes=len(staple_hdr)))
            for log2N in (0, 5, 8, 14):
                N = 1 << log2N
                salt = os.urandom(16)
                lf = leaf_hash(1, log2N, 0, c.tenant, salt, enc(c), 16)
                root, paths = treehash_paths(1, log2N, lambda i: lf if i == 0 else os.urandom(16), N, [0], 16)
                sr = SignedRoot(1, log2N, T0 * 1000, 1000, N, root)
                sr.sig = s.sign(sr.msg())
                et = encode_ember(c, 1, log2N, 0, salt, paths[0], 16, "ML-DSA-44")
                assert EmberEdge(s, 1, 16, 3600, fetch_fn=lambda k, e: sr).verify(et, NOW, c.url_prefix)[0]
                srb = sr.to_bytes()
                rows.append(dict(scheme="EMBER-O1", log2N=log2N, url_path_len=L, with_ip=ip, claims_bytes=len(enc(c)),
                                 token_bytes=len(et), signed_url_bytes=len(to_signed_url(BASE + c.url_prefix, et)),
                                 staple_raw_bytes=len(srb),
                                 staple_header_http11_bytes=len("x-ember-root: %s\r\n" % b64e(srb))))
    with open(os.path.join(a.out, "token_sizes_r1.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        if r["url_path_len"] == 60 and r["with_ip"] == 0:
            print(r)
    if a.no_timing:
        return
    # ---- Python verify timing (secondary; native/Go numbers are primary)
    n = a.iters
    vrows = []
    cl = [mkclaims(60, 0, i) for i in range(n)]
    toks = [iss.issue(c) for c in cl]
    edge = StapledPerTokenEdge(iss.signer, kid=1)
    miss = timed_each([(lambda t=t, c=c: edge.verify(t[0], NOW, c.url_prefix, t[1])) for t, c in zip(toks, cl)], warm=0)
    assert edge.stats["sig_verifs"] == n
    hit = timed_each([(lambda t=t, c=c: edge.verify(t[0], NOW, c.url_prefix)) for t, c in zip(toks, cl)], warm=0)
    for lab, t in (("M2 staple verify (miss)", miss), ("M2 cache hit", hit)):
        lo, hi = boot_median(t)
        vrows.append(dict(scheme=lab, median_us=np.median(t), ci_lo=lo, ci_hi=hi, n=n, impl="python+pqcrypto-1.0.0"))
    for log2N in (0, 5):
        N = 1 << log2N
        salts = [os.urandom(16) for _ in range(min(N, n))]
        reps = (n + N - 1) // N
        toks_e, srs = [], {}
        for e in range(reps):
            cs = cl[e * N:(e + 1) * N]
            leaves = [leaf_hash(1, e, j, c.tenant, salts[j % len(salts)], enc(c), 16) for j, c in enumerate(cs)]
            root, paths = treehash_paths(1, e, lambda i: leaves[i] if i < len(leaves) else os.urandom(16), N,
                                         list(range(len(cs))), 16)
            sr = SignedRoot(1, e, T0 * 1000, 1000, N, root)
            sr.sig = s.sign(sr.msg())
            srs[e] = sr
            toks_e += [(encode_ember(c, 1, e, j, salts[j % len(salts)], paths[j], 16, "ML-DSA-44"), c) for j, c in enumerate(cs)]
        ed = EmberEdge(s, 1, 16, 3600, fetch_fn=lambda k, e: srs[e])
        for t, c in toks_e:
            assert ed.verify(t, NOW, c.url_prefix)[0]
        tw = timed_each([(lambda t=t, c=c: ed.verify(t, NOW, c.url_prefix)) for t, c in toks_e[:n]], warm=0)
        lo, hi = boot_median(tw)
        vrows.append(dict(scheme="EMBER warm d=%d" % log2N, median_us=np.median(tw), ci_lo=lo, ci_hi=hi, n=len(tw),
                          impl="python+pqcrypto-1.0.0"))
    with open(os.path.join(a.out, "token_verify_r1.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(vrows[0]))
        w.writeheader()
        w.writerows(vrows)
    for r in vrows:
        print(r)


if __name__ == "__main__":
    main()
