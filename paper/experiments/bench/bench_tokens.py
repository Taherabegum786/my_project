"""E2 / E2+: token sizes, edge verify cost (Python), issuer throughput (Python), model check.

taskset -c 2 python -m bench.bench_tokens --out ../results [--quick] [--procs 4]
-> token_sizes.csv, token_verify.csv, issuer_throughput.csv, model_check.csv
All timings here are Python-backend (impl column); native numbers come from bench/native/.
"""
import argparse
import csv
import gc
import math
import multiprocessing as mp
import os
import struct
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from baselines.pertoken import PERTOKEN, make_scheme, split_cookies
from ember.edge import EmberEdge
from ember.issuer import EmberIssuer, SignedRoot
from ember.merkle import leaf_hash, treehash_paths
from ember.signers import (CTX_ROOT, KemWrappedHMAC, MTLMode, VerifyCache, make_signer)
from ember.token import Claims, enc, encode_ember, to_cookie, to_signed_url

BASE = "https://cdn.example.com"
T0 = 1_800_000_000
NOW = T0 + 10
rng = np.random.default_rng(20261105)
OSCHEMES = {"O1": ("ML-DSA-44", 16), "O2": ("ML-DSA-44", 32), "O3": ("SLH-DSA-128s", 16),
            "O4": ("Hybrid-Ed25519+ML-DSA-44", 16)}
IMPL = {"HMAC-SHA256": "hashlib", "Ed25519": "cryptography-50.0.2", "ECDSA-P256": "cryptography-50.0.2",
        "RSA-2048": "cryptography-50.0.2"}


def impl_of(name):
    return IMPL.get(name, "pqcrypto-1.0.0")


def mkpath(L, i=0):
    # deterministic path of exactly L chars: /v/t<ten>/<obj>/... padded
    p = "/v/t7/m%06d/" % i
    return (p + "x" * max(0, L - len(p)))[:L] if L >= len(p) else p[:L]


def mkclaims(L=60, with_ip=0, i=0, tenant=7):
    return Claims(mkpath(L, i), T0 + 1800, tenant, "203.0.113.0/24" if with_ip else None)


def boot_median(x, B=2000):
    m = np.median(x[rng.integers(0, len(x), (B, len(x)))], axis=1)
    return np.percentile(m, 2.5), np.percentile(m, 97.5)


def timed_each(fns, warm=200):
    """fns: list of zero-arg callables (one per verification); returns per-call microseconds."""
    for f in fns[:warm]:
        f()
    gc.disable()
    pc = time.perf_counter_ns
    t = np.empty(len(fns))
    for k, f in enumerate(fns):
        t0 = pc()
        f()
        t[k] = (pc() - t0) / 1000.0
    gc.enable()
    return t


def write_csv(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow({k: (("%.4f" % v) if isinstance(v, float) else v) for k, v in r.items()})


# ============================================================ sizes
def sizes(out, quick):
    rows = []
    variants = [(L, ip) for L in (40, 60, 120, 250) for ip in (0, 1)]

    def row(scheme, rs, n, log2N, L, ip, c, auth_raw, tok, ncookies=1, cookie=None):
        url = to_signed_url(BASE + c.url_prefix, tok)
        ck = cookie if cookie is not None else to_cookie(tok)
        rows.append(dict(scheme=scheme, root_signer=rs, n=n, log2N=log2N, url_path_len=L, with_ip=ip,
                         claims_bytes=len(enc(c)), auth_bytes_raw=auth_raw, token_bytes=len(tok),
                         signed_url_bytes=len(url.encode()), cookie_bytes=len(ck.encode()), n_cookies=ncookies))

    # per-token baselines
    for sid in list(PERTOKEN) + ["B5c", "B6c", "B10k1", "B10k3", "B10k10", "B11", "B12"]:
        if sid.startswith("B10"):
            sch = make_scheme("B10", k=int(sid[4:]))
        else:
            sch = make_scheme(sid)
        for L, ip in variants:
            c = mkclaims(L, ip)
            tok = sch.issue(c)
            from ember.token import decode_pertoken
            _, _, sig = decode_pertoken(tok)
            assert sch.verify(tok, NOW, c.url_prefix)[0]
            if sid in ("B5c", "B6c"):
                cks = split_cookies(tok, 2)
                row(sid, "", "", "", L, ip, c, len(sig), tok, 2, cookie=max(cks, key=len))
            else:
                row(sid, "", "", "", L, ip, c, len(sig), tok)
    print("sizes: per-token done", flush=True)

    # EMBER: real trees (streaming treehash for power-of-two N, variants at leaves 0..7; random filler leaves)
    max_log = 20 if quick else 24
    for n in (16, 32):
        signers = {o: make_signer(rs, CTX_ROOT) for o, (rs, nn) in OSCHEMES.items() if nn == n}
        for log2N in range(0, max_log + 1, 2):
            N = 1 << log2N
            groups = [[v] for v in variants] if N < len(variants) else [variants]
            for grp in groups:
                cl = [mkclaims(L, ip, i=j) for j, (L, ip) in enumerate(grp)]
                salts = [os.urandom(16) for _ in cl]
                leaves = [leaf_hash(1, log2N, j, c.tenant, salts[j], enc(c), n) for j, c in enumerate(cl)]
                fill = os.urandom
                root, paths = treehash_paths(1, log2N, lambda i: leaves[i] if i < len(leaves) else fill(n), N,
                                             list(range(len(cl))), n)
                for o, s in signers.items():
                    rs = OSCHEMES[o][0]
                    sr = SignedRoot(1, log2N, T0 * 1000, 1000, N, root)
                    sr.sig = s.sign(sr.msg())
                    edge = EmberEdge(s, 1, n, 3600, fetch_fn=lambda k, e: sr)
                    for j, c in enumerate(cl):
                        tok = encode_ember(c, 1, log2N, j, salts[j], paths[j], n, rs)
                        ok, why, _ = edge.verify(tok, NOW, c.url_prefix)
                        assert ok, (o, log2N, why)
                        row(o, rs, n, log2N, grp[j][0], grp[j][1], c, 30 + n * log2N, tok)
            print("sizes: EMBER n=%d log2N=%d" % (n, log2N), flush=True)

    # B13 MTL mode: real series up to 2^max; condensed signature for a leaf in the largest rung
    s = make_signer("ML-DSA-44", CTX_ROOT)
    mtl_max = 16 if quick else 20
    mtl = MTLMode(s, kid=1, n=16)
    filler = enc(mkclaims(60, 0, 999))
    cl = [mkclaims(L, ip, i=j) for j, (L, ip) in enumerate(variants)]
    for c in cl:
        mtl.append(enc(c), c.tenant)
    S = len(cl)
    for log2S in range(4, mtl_max + 1, 2):
        while len(mtl.nodes[0]) < (1 << log2S):
            mtl.append(filler, 7)
        S, rungs, sig = mtl.sign_ladder()
        lad = {(h, st): x for h, st, x in rungs}
        for j, c in enumerate(cl):
            tok = mtl.encode(enc(c), j, S)
            assert MTLMode.verify_token(tok, lad, 1, 16)
            h, _ = mtl.condensed(j, S)
            row("B13", "ML-DSA-44", 16, log2S, variants[j][0], variants[j][1], c, 31 + 16 * h, tok)
    write_csv(os.path.join(out, "token_sizes.csv"), rows)
    return rows


# ============================================================ verify
def verify_bench(out, quick):
    rows = []
    iters = 1000 if quick else 5000
    K = 150

    def add(scheme, rs, n, log2N, cache, t, impl, amort=None):
        lo, hi = boot_median(t)
        rows.append(dict(scheme=scheme, root_signer=rs, n=n, log2N=log2N, cache=cache, iters=len(t),
                         median_us=float(np.median(t)), p99_us=float(np.percentile(t, 99)), mean_us=float(t.mean()),
                         ci95_lo_us=lo, ci95_hi_us=hi, impl=impl, amortised_us_per_req=amort if amort is not None else ""))
        print("verify %-6s %-28s log2N=%-3s %-6s %9.2f us" % (scheme, rs, log2N, cache, np.median(t)), flush=True)

    # discarded warm-up pass (the first timed loop in a process is ~1.7x slower; observed in QUICK runs)
    _w = make_scheme("B1")
    _c = [mkclaims(60, 0, i) for i in range(2000)]
    _t = [_w.issue(c) for c in _c]
    timed_each([(lambda t=_t[k], u=_c[k].url_prefix: _w.verify(t, NOW, u)) for k in range(2000)])
    slow = {"B5": 500, "B6": 500, "B9": 500, "B7": 20, "B8": 100}  # distinct tokens (cycled to `iters`)
    for sid in list(PERTOKEN) + ["B10k1", "B10k3", "B10k10", "B11", "B12"]:
        sch = make_scheme("B10", k=int(sid[4:])) if sid.startswith("B10") else make_scheme(sid)
        nd = min(iters, slow.get(sid, iters))
        if quick:
            nd = min(nd, 50)
        cl = [mkclaims(60, 0, i) for i in range(nd)]
        toks = [sch.issue(c) for c in cl]
        fns = [(lambda t=toks[k % nd], u=cl[k % nd].url_prefix: sch.verify(t, NOW, u)) for k in range(iters)]
        assert all(f()[0] for f in fns[:5])
        name = sch.signer.name
        add(sid, name, "", "", "none", timed_each(fns), impl_of(name) if sid in PERTOKEN else "python-mixed")
    # verify-cache variants (B5v, B6v): miss = full verify + insert; hit = cache lookup
    for sid in ("B5v", "B6v"):
        sch = make_scheme(sid)
        nd = 50 if quick else 500
        cl = [mkclaims(60, 0, i) for i in range(nd)]
        toks = [sch.issue(c) for c in cl]
        sch.cache = VerifyCache(10 ** 6)
        miss = timed_each([(lambda t=toks[k], u=cl[k].url_prefix: sch.verify(t, NOW, u)) for k in range(nd)], warm=0)
        hit = timed_each([(lambda t=toks[k % nd], u=cl[k % nd].url_prefix: sch.verify(t, NOW, u)) for k in range(iters)])
        am = (np.median(miss) + K * np.median(hit)) / (K + 1)
        add(sid, sch.signer.name, "", "", "miss", miss, "pqcrypto-1.0.0+hashlib", am)
        add(sid, sch.signer.name, "", "", "hit", hit, "hashlib", am)

    # EMBER warm / cold at log2N
    logs = (4, 8, 12, 16) if quick else (4, 8, 12, 16, 20)
    for o in ("O1", "O2", "O3", "O4"):
        rs, n = OSCHEMES[o]
        s = make_signer(rs, CTX_ROOT)
        for log2N in logs:
            if o in ("O3", "O4") and log2N not in (8, 16):
                continue
            N = 1 << log2N
            iss = EmberIssuer(s, kid=1, n=n, t0=T0)
            cl = [mkclaims(60, 0, i) for i in range(N)]
            tk = [iss.submit(c) for c in cl]
            sr, toks, _ = iss.close_epoch(T0 + 1)
            edge = EmberEdge(s, 1, n, 3600, fetch_fn=lambda k, e: sr)
            idx = rng.integers(0, N, iters)
            fns = [(lambda t=toks[tk[i]], u=cl[i].url_prefix: edge.verify(t, NOW, u)) for i in idx]
            assert all(f()[0] for f in fns[:5])
            add(o, rs, n, log2N, "warm", timed_each(fns), "hashlib")
            if log2N in (8, 16):
                ncold = 50 if rs.startswith("SLH") and quick else min(iters, 2000)

                def cold(t, u):
                    edge.roots.clear()
                    return edge.verify(t, NOW, u)
                fns = [(lambda t=toks[tk[i]], u=cl[i].url_prefix: cold(t, u)) for i in idx[:ncold]]
                add(o, rs, n, log2N, "cold", timed_each(fns, warm=20), impl_of(rs.split("+")[-1]))
            if o == "O1" and log2N == 16:  # EMBER + verify cache ablation
                vc = VerifyCache(10 ** 6)

                def cached(t, u):
                    if vc.check(t, NOW):
                        return True
                    ok = edge.verify(t, NOW, u)[0]
                    vc.put(t, T0 + 1800)
                    return ok
                fns = [(lambda t=toks[tk[i]], u=cl[i].url_prefix: cached(t, u)) for i in idx]
                miss = timed_each(fns, warm=0)
                hit = timed_each(fns, warm=0)
                am = (np.median(miss) + K * np.median(hit)) / (K + 1)
                add("O1v", rs, n, log2N, "miss", miss, "hashlib", am)
                add("O1v", rs, n, log2N, "hit", hit, "hashlib", am)
        del iss, toks
    # B13 MTL verify (ladder cached), series 2^16
    s = make_signer("ML-DSA-44", CTX_ROOT)
    mtl = MTLMode(s, 1, n=16)
    cl = [mkclaims(60, 0, i) for i in range(1 << 16)]
    for c in cl:
        mtl.append(enc(c), c.tenant)
    S, rungs, _ = mtl.sign_ladder()
    lad = {(h, st): x for h, st, x in rungs}
    idx = rng.integers(0, S, iters)
    toks = {i: mtl.encode(enc(cl[i]), i, S) for i in set(idx.tolist())}
    fns = [(lambda t=toks[i]: MTLMode.verify_token(t, lad, 1, 16)) for i in idx]
    add("B13", "ML-DSA-44", 16, 16, "warm", timed_each(fns), "hashlib")
    write_csv(os.path.join(out, "token_verify.csv"), rows)
    return rows


# ============================================================ issuer throughput
def _pertoken_worker(args):
    sid, window = args
    sch = make_scheme(sid)
    c = mkclaims(60, 0, 0)
    n = 0
    t0 = time.perf_counter()
    while time.perf_counter() - t0 < window:
        sch.issue(c.with_(expires=c.expires + n))
        n += 1
    return n, time.perf_counter() - t0


def _ember_worker(args):
    rs, n, N, reps = args
    s = make_signer(rs, CTX_ROOT)
    iss = EmberIssuer(s, kid=1, n=n, t0=T0)
    cl = [mkclaims(60, 0, i) for i in range(N)]
    tot = 0.0
    tm = []
    for r in range(reps):
        for c in cl:
            iss.submit(c)
        t0 = time.perf_counter()
        _, toks, tim = iss.close_epoch(T0 + r + 1)
        tot += time.perf_counter() - t0
        tm.append(tim)
    return N * reps, tot, tm


def issuer_bench(out, quick, procs):
    rows = []
    window = 2.0 if quick else 10.0

    def prow(scheme, rs, n, N, p, tl, tt, ts, te, tep, tps, impl, extra=""):
        rows.append(dict(scheme=scheme, root_signer=rs, n=n, N=N, procs=p, t_leaf_us=tl, t_tree_us=tt, t_sign_us=ts,
                         t_encode_us=te, t_epoch_us=tep, tokens_per_s=tps, impl=impl, note=extra))

    for sid in list(PERTOKEN) + ["B11"]:
        w = 30 if sid == "B7" else window
        if sid == "B7":
            sch = make_scheme(sid)
            c = mkclaims()
            t0 = time.perf_counter()
            for i in range(5 if quick else 30):
                sch.issue(c.with_(expires=c.expires + i))
            cnt, el = (5 if quick else 30), time.perf_counter() - t0
        else:
            cnt, el = _pertoken_worker((sid, w))
        name = make_scheme(sid).signer.name if sid != "B11" else "Delegated-Ed25519"
        prow(sid, name, "", 1, 1, "", "", el / cnt * 1e6, "", el / cnt * 1e6, cnt / el, impl_of(name) if sid in PERTOKEN else "cryptography-50.0.2")
        print("issuer %s %.1f tok/s" % (sid, cnt / el), flush=True)

    Ns = [1, 4, 16, 64, 256, 1024, 4096, 16384, 65536, 262144]
    if quick:
        Ns = Ns[:8]
    for rs in ("ML-DSA-44", "ML-DSA-65", "SLH-DSA-128s", "SLH-DSA-128f", "Hybrid-Ed25519+ML-DSA-44"):
        for N in Ns:
            if N == 262144 and rs not in ("ML-DSA-44", "SLH-DSA-128s"):
                continue
            reps = max(1, min(20, 20000 // N)) if not rs.startswith("SLH-DSA-128s") else (1 if N >= 1024 else 3)
            if quick:
                reps = 1
            tot_tok, tot, tm = _ember_worker((rs, 16, N, reps))
            mean = {k: np.mean([t[k] for t in tm]) / 1000.0 for k in ("t_leaf", "t_tree", "t_sign", "t_encode", "t_epoch")}
            prow("EMBER", rs, 16, N, 1, mean["t_leaf"], mean["t_tree"], mean["t_sign"], mean["t_encode"], mean["t_epoch"],
                 N / (mean["t_epoch"] / 1e6), "python(hashlib)+" + impl_of(rs.split("+")[-1]))
            print("issuer EMBER %s N=%d %.0f tok/s" % (rs, N, N / (mean["t_epoch"] / 1e6)), flush=True)
    # pad_pow2 rows (O1) at non-power-of-two N
    for N in (1000, 5000, 20000):
        s = make_signer("ML-DSA-44", CTX_ROOT)
        for pad in (0, 1):
            iss = EmberIssuer(s, 1, 16, pad_pow2=bool(pad), t0=T0)
            for i in range(N):
                iss.submit(mkclaims(60, 0, i))
            _, _, tim = iss.close_epoch(T0 + 1)
            prow("EMBER-pad%d" % pad, "ML-DSA-44", 16, N, 1, tim["t_leaf"] / 1e3, tim["t_tree"] / 1e3, tim["t_sign"] / 1e3,
                 tim["t_encode"] / 1e3, tim["t_epoch"] / 1e3, N / (tim["t_epoch"] / 1e9), "python(hashlib)+pqcrypto-1.0.0")
    # B12: per-epoch wrap cost for E edges (python: pqcrypto ML-KEM-768 encaps + HKDF + AES-GCM)
    pk, _ = KemWrappedHMAC.edge_keygen()
    for E in (100, 500, 2000):
        b = KemWrappedHMAC()
        t0 = time.perf_counter()
        wr = b.new_epoch(1, [pk] * E)
        el = time.perf_counter() - t0
        prow("B12-epoch", "ML-KEM-768", "", E, 1, "", "", el * 1e6, "", el * 1e6, "", "pqcrypto-1.0.0+cryptography-50.0.2",
             "E=%d edges; wrap bytes per edge=%d; per-epoch push bytes=%d" % (E, len(wr[0]), E * len(wr[0])))
    write_csv(os.path.join(out, "issuer_throughput.csv"), rows)
    return rows


def issuer_mp(out, quick, procs):
    """One issuer shard per core.  Must NOT run under a single-core taskset (workers inherit the affinity):
    each worker pins itself to core (rank % ncpu)."""
    window = 2.0 if quick else 10.0
    rows = []
    ncpu = os.cpu_count()
    for p in sorted({1, procs}):
        for sid, fn, arg in (("B5", _pertoken_worker, ("B5", window)),
                             ("EMBER", _ember_worker, ("ML-DSA-44", 16, 16384, 2 if quick else 10))):
            with mp.get_context("fork").Pool(p, initializer=_pin, initargs=(ncpu,)) as pool:
                res = pool.map(fn, [arg] * p)
            tps = sum(r[0] / r[1] for r in res)
            rows.append(dict(scheme=sid, root_signer="ML-DSA-44", N=1 if sid == "B5" else 16384, procs=p,
                             tokens_per_s=tps, per_proc=tps / p, impl="pqcrypto-1.0.0" + ("" if sid == "B5" else "+hashlib")))
            print("mp %s procs=%d %.0f tok/s" % (sid, p, tps), flush=True)
    write_csv(os.path.join(out, "issuer_throughput_mp.csv"), rows)


_PIN_CTR = mp.Value("i", 0) if hasattr(mp, "Value") else None


def _pin(ncpu):
    with _PIN_CTR.get_lock():
        k = _PIN_CTR.value
        _PIN_CTR.value += 1
    os.sched_setaffinity(0, {k % ncpu})


# ============================================================ model check
def model_check(out, size_rows, verify_rows, issuer_rows):
    import pandas as pd
    rows = []
    mp_ = pd.read_csv(os.path.join(out, "micro_primitives.csv")) if os.path.exists(os.path.join(out, "micro_primitives.csv")) else None
    for r in size_rows:
        if r["scheme"] in ("O1", "O2") and r["with_ip"] == 0 and r["url_path_len"] == 60:
            pred = r["claims_bytes"] + 3 + math.ceil(4 * (30 + r["n"] * r["log2N"]) / 3)
            rows.append(dict(quantity="token_bytes", scheme=r["scheme"], param="log2N=%d" % r["log2N"], predicted=pred,
                             measured=r["token_bytes"], rel_err=(r["token_bytes"] - pred) / pred))
    if mp_ is not None:
        th = float(mp_[mp_.scheme == "Th-n16-tweak+hash"].median_us.iloc[0])
        th200 = float(mp_[mp_.scheme == "Th-n16-200B"].median_us.iloc[0])
        for r in verify_rows:
            if r["scheme"] == "O1" and r["cache"] == "warm":
                b1 = [x for x in verify_rows if x["scheme"] == "B1"][0]["median_us"]  # parse+policy+HMAC as t_parse proxy
                hm = float(mp_[(mp_.scheme == "HMAC-SHA256") & (mp_.op == "verify")].median_us.iloc[0])
                pred = (b1 - hm) + th200 + r["log2N"] * th
                rows.append(dict(quantity="edge_verify_us", scheme="O1", param="log2N=%d" % r["log2N"], predicted=pred,
                                 measured=r["median_us"], rel_err=(r["median_us"] - pred) / pred))
        ts = float(mp_[(mp_.scheme == "ML-DSA-44") & (mp_.op == "sign")].median_us.iloc[0])
        for r in issuer_rows:
            if r["scheme"] == "EMBER" and r["root_signer"] == "ML-DSA-44" and r["procs"] == 1 and r["t_epoch_us"] != "":
                N = r["N"]
                ser = r["t_encode_us"] / N
                pred_epoch = N * th200 + (N - 1) * th + ts + N * ser
                rows.append(dict(quantity="issuer_tokens_per_s", scheme="O1", param="N=%d" % N, predicted=N / pred_epoch * 1e6,
                                 measured=r["tokens_per_s"], rel_err=(r["tokens_per_s"] - N / pred_epoch * 1e6) / (N / pred_epoch * 1e6)))
    write_csv(os.path.join(out, "model_check.csv"), rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="../results")
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--procs", type=int, default=4)
    ap.add_argument("--only", default="sizes,verify,issuer")  # add ",mp" (unpinned) for issuer_throughput_mp.csv
    a = ap.parse_args()
    only = a.only.split(",")
    t0 = time.time()
    S = sizes(a.out, a.quick) if "sizes" in only else []
    V = verify_bench(a.out, a.quick) if "verify" in only else []
    I = issuer_bench(a.out, a.quick, a.procs) if "issuer" in only else []
    if "mp" in only:
        issuer_mp(a.out, a.quick, a.procs)
    if S and V and I:
        model_check(a.out, S, V, I)
    print("bench_tokens done in %.0f s" % (time.time() - t0))


if __name__ == "__main__":
    main()
