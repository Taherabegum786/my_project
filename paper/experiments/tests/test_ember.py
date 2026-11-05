"""Correctness and negative tests for EMBER and all baselines.  Run: pytest -q tests/  or  python -m tests.test_ember"""
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from baselines.pertoken import make_scheme, split_cookies
from ember.edge import EmberEdge
from ember.issuer import EmberIssuer, EPOCH_MAX, SignedRoot
from ember.merkle import auth_path, build_tree, path_len, root_from_path
from ember.signers import (CTX_ROOT, DelegatedEd25519, HybridEd25519MLDSA44, KemWrappedHMAC, MLDSA44,
                           MTLMode, VerifyCache, make_signer, Ed25519)
from ember.token import Claims, b64d, b64e, decode_ember, enc, EMBER_SEP

T0 = 1_800_000_000.0
URL = "/v/tenant7/movie123/seg_00042.ts"


def claims(i=0, tenant=7, exp=None, ip=None):
    return Claims("/v/tenant%d/movie%d/" % (tenant, 100 + i % 50), int(exp or T0 + 1800), tenant, ip)


def mkurl(c):
    return c.url_prefix + "seg_00001.ts"


class Fx:
    def __init__(self, signer_name="ML-DSA-44", n=16, kid=1, v_max=3600.0):
        self.signer = make_signer(signer_name, CTX_ROOT)
        self.iss = EmberIssuer(self.signer, kid=kid, n=n, v_max=v_max, t0=T0)
        self.store = {}
        self.edge = EmberEdge(self.signer, kid, n, v_max, fetch_fn=lambda k, e: self.store.get(e))

    def epoch(self, cl, dt=1.0):
        tick = [self.iss.submit(c) for c in cl]
        sr, toks, _ = self.iss.close_epoch(self.iss.t_open + dt)
        self.store[sr.epoch] = sr
        return sr, [toks[t] for t in tick]


def _mutate_blob(tok, fn):
    cs, _, b = tok.rpartition(EMBER_SEP)
    blob = bytearray(b64d(b))
    fn(blob)
    return cs + EMBER_SEP + b64e(bytes(blob))


# ------------------------------------------------------------------ round trip
@pytest.mark.parametrize("n", [16, 32])
@pytest.mark.parametrize("N", [1, 2, 3, 5, 8, 1000, 1025])
def test_roundtrip(N, n):
    fx = Fx("Ed25519" if N > 8 else "ML-DSA-44", n=n)
    cl = [claims(i) for i in range(N)]
    sr, toks = fx.epoch(cl)
    assert sr.N == N
    idxs = range(N) if N <= 8 else [0, 1, N // 2, N - 2, N - 1]
    for i in idxs:
        t = decode_ember(toks[i])
        assert len(t.path) == path_len(N, i)
        assert len(t.path) <= max(0, (N - 1).bit_length())
        ok, why, _ = fx.edge.verify(toks[i], T0 + 10, mkurl(cl[i]))
        assert ok, why


def test_merkle_paths_all_N():
    for N in range(1, 70):
        leaves = [os.urandom(16) for _ in range(N)]
        root, lv = build_tree(1, 2, leaves, 16)
        for i in range(N):
            assert root_from_path(1, 2, i, N, leaves[i], auth_path(lv, i), 16) == root


# ------------------------------------------------------------------ tampering
@pytest.fixture(scope="module")
def fx8():
    fx = Fx("ML-DSA-44", 16)
    cl = [claims(i) for i in range(8)]
    sr0, t0 = fx.epoch(cl)
    sr1, t1 = fx.epoch(cl)
    return fx, cl, t0, t1


def test_valid(fx8):
    fx, cl, t0, t1 = fx8
    assert fx.edge.verify(t0[3], T0 + 5, mkurl(cl[3]))[0]
    assert fx.edge.verify(t1[3], T0 + 5, mkurl(cl[3]))[0]


def test_flip_claims(fx8):
    fx, cl, t0, _ = fx8
    tok = t0[3]
    # semantic change of claims (still canonical)
    c2 = cl[3].with_(expires=cl[3].expires + 1)
    bad = enc(c2).decode() + tok[len(enc(cl[3])):]
    assert not fx.edge.verify(bad, T0 + 5, mkurl(cl[3]))[0]
    c3 = cl[3].with_(url_prefix="/v/")
    bad = enc(c3).decode() + tok[len(enc(cl[3])):]
    assert not fx.edge.verify(bad, T0 + 5, mkurl(cl[3]))[0]
    # raw bit flips over every claims byte
    for k in range(len(enc(cl[3]))):
        b = bytearray(tok.encode())
        b[k] ^= 0x01
        try:
            s = b.decode()
        except UnicodeDecodeError:
            continue
        assert not fx.edge.verify(s, T0 + 5, mkurl(cl[3]))[0], k


def test_flip_salt_path_index(fx8):
    fx, cl, t0, _ = fx8
    tok = t0[3]
    u = mkurl(cl[3])
    for off in list(range(14, 30)) + list(range(30, 30 + 16 * 3)):  # salt bytes, path bytes
        for bit in (0, 7):
            bad = _mutate_blob(tok, lambda b: b.__setitem__(off, b[off] ^ (1 << bit)))
            assert not fx.edge.verify(bad, T0 + 5, u)[0], off
    for newidx in (2, 4, 7):
        bad = _mutate_blob(tok, lambda b: struct.pack_into(">I", b, 10, newidx))
        assert not fx.edge.verify(bad, T0 + 5, u)[0]
    bad = _mutate_blob(tok, lambda b: b.__setitem__(13, b[13] ^ 1))  # idx 3 -> 2
    assert not fx.edge.verify(bad, T0 + 5, u)[0]


def test_epoch_swap(fx8):
    fx, cl, t0, t1 = fx8
    bad = _mutate_blob(t0[3], lambda b: struct.pack_into(">I", b, 6, 1))
    assert not fx.edge.verify(bad, T0 + 5, mkurl(cl[3]))[0]


def test_idx_out_of_range(fx8):
    fx, cl, t0, _ = fx8
    bad = _mutate_blob(t0[7], lambda b: struct.pack_into(">I", b, 10, 8))
    ok, why, _ = fx.edge.verify(bad, T0 + 5, mkurl(cl[7]))
    assert not ok and why == "idx_range"


def test_wrong_kid_root():
    a = Fx("Ed25519", kid=1)
    other = make_signer("Ed25519", CTX_ROOT)
    cl = [claims(i) for i in range(4)]
    sr, toks = a.epoch(cl)
    forged = SignedRoot(1, sr.epoch, sr.t_start_ms, sr.delta_ms, sr.N, sr.root)
    forged.sig = other.sign(forged.msg())
    e = EmberEdge(a.signer, 1, 16, 3600, fetch_fn=lambda k, ep: forged)
    assert not e.verify(toks[0], T0 + 5, mkurl(cl[0]))[0]
    # root signed with correct key but labelled for kid 2
    sr2 = SignedRoot(2, sr.epoch, sr.t_start_ms, sr.delta_ms, sr.N, sr.root)
    sr2.sig = a.signer.sign(sr2.msg())
    e2 = EmberEdge(a.signer, 1, 16, 3600, fetch_fn=lambda k, ep: sr2)
    assert not e2.verify(toks[0], T0 + 5, mkurl(cl[0]))[0]


def test_cross_kid_replay():
    s = make_signer("Ed25519", CTX_ROOT)
    a = EmberIssuer(s, kid=1, t0=T0)
    b = EmberIssuer(s, kid=2, t0=T0)  # same key material, different kid
    c = claims(0)
    ta = a.submit(c)
    sra, toka, _ = a.close_epoch(T0 + 1)
    tb = b.submit(c)
    srb, tokb, _ = b.close_epoch(T0 + 1)
    edge_b = EmberEdge(s, 2, 16, 3600, fetch_fn=lambda k, e: srb)
    assert edge_b.verify(tokb[tb], T0 + 2, mkurl(c))[0]
    assert not edge_b.verify(toka[ta], T0 + 2, mkurl(c))[0]
    # relabel kid in token blob -> path computed under kid 2 tweaks fails
    bad = _mutate_blob(toka[ta], lambda bb: struct.pack_into(">I", bb, 2, 2))
    assert not edge_b.verify(bad, T0 + 2, mkurl(c))[0]


def test_expiry_and_validity_bound():
    fx = Fx("Ed25519", v_max=3600)
    c = claims(0, exp=T0 + 100)
    sr, toks = fx.epoch([c])
    assert fx.edge.verify(toks[0], T0 + 50, mkurl(c))[0]
    ok, why, _ = fx.edge.verify(toks[0], T0 + 200, mkurl(c))
    assert not ok and why == "expired"
    # Issuer with V_max=86400 issues a long-lived token; edge with V_max=3600 must reject it
    big = Fx("Ed25519", v_max=86400)
    c2 = claims(0, exp=T0 + 50000)
    sr2, toks2 = big.epoch([c2])
    edge = EmberEdge(big.signer, 1, 16, 3600, fetch_fn=lambda k, e: sr2)
    ok, why, _ = edge.verify(toks2[0], T0 + 10, mkurl(c2))
    assert not ok and why == "validity_bound"
    # issuer clamps Expires to T_start + delta + V_max
    assert decode_ember(toks2[0]).claims.expires <= T0 + 1 + 86400


def test_clock_skew():
    fx = Fx("Ed25519")
    c = claims(0, exp=T0 + 100)
    sr, toks = fx.epoch([c])
    tau = fx.edge.tau
    assert fx.edge.verify(toks[0], c.expires + tau, mkurl(c))[0]       # +tau skew accepts
    assert fx.edge.verify(toks[0], c.expires - tau, mkurl(c))[0]       # -tau skew accepts
    assert not fx.edge.verify(toks[0], c.expires + 2 * tau, mkurl(c))[0]  # 2tau rejects
    # validity bound boundary: Expires exactly at T_start+delta+V_max+tau accepted, +2tau rejected
    v = 3600.0
    for extra, expect in ((tau, True), (2 * tau, False)):
        iss = EmberIssuer(fx.signer, kid=1, v_max=v + 3 * tau, t0=T0)
        cb = claims(0, exp=T0 + 1 + v + extra)
        iss.submit(cb)
        srb, tk, _ = iss.close_epoch(T0 + 1)
        e = EmberEdge(fx.signer, 1, 16, v, fetch_fn=lambda k, ep: srb)
        assert e.verify(tk[0], T0 + 2, mkurl(cb))[0] == expect, extra


def test_revocation(fx8):
    fx, cl, t0, _ = fx8
    fx.iss.revoke(0, 5)
    rd = fx.iss.revocation_delta()
    assert fx.edge.install_revocations(rd)
    ok, why, _ = fx.edge.verify(t0[5], T0 + 5, mkurl(cl[5]))
    assert not ok and why == "revoked"
    assert fx.edge.verify(t0[4], T0 + 5, mkurl(cl[4]))[0]
    rd.items.append((0, 4))  # tampered delta
    assert not fx.edge.install_revocations(rd)


def test_period_bundle():
    fx = Fx("ML-DSA-44")
    cl = [claims(i) for i in range(3)]
    toks = []
    for _ in range(4):
        toks.append(fx.epoch(cl)[1])
    pb = fx.iss.close_period()
    e = EmberEdge(fx.signer, 1, 16, 3600, fetch_fn=lambda k, ep: pb)
    for ep in range(4):
        assert e.verify(toks[ep][1], T0 + 10, mkurl(cl[1]))[0]
    assert e.stats["sig_verifs"] == 1  # one bundle verification for 4 epochs
    pb.entries[2] = pb.entries[2][:-1] + bytes([pb.entries[2][-1] ^ 1])  # tamper list
    e2 = EmberEdge(fx.signer, 1, 16, 3600, fetch_fn=lambda k, ep: pb)
    assert not e2.verify(toks[2][1], T0 + 10, mkurl(cl[1]))[0]


def test_stapled_root():
    fx = Fx("ML-DSA-44")
    c = claims(0)
    sr, toks = fx.epoch([c, claims(1)])
    e = EmberEdge(fx.signer, 1, 16, 3600, fetch_fn=None)
    assert not e.verify(toks[0], T0 + 5, mkurl(c))[0]
    ok, why, fetched = e.verify(toks[0], T0 + 5, mkurl(c), stapled=sr.to_bytes())
    assert ok and not fetched
    bad = bytearray(sr.to_bytes())
    bad[-1] ^= 1
    e2 = EmberEdge(fx.signer, 1, 16, 3600)
    assert not e2.verify(toks[0], T0 + 5, mkurl(c), stapled=bytes(bad))[0]


def test_hybrid_halves():
    h = HybridEd25519MLDSA44(CTX_ROOT).keygen()
    m = b"root message"
    s = h.sign(m)
    assert h.verify(m, s)
    for off in (5, 64 + 100):
        b = bytearray(s)
        b[off] ^= 1
        assert not h.verify(m, bytes(b))
    fx = Fx("Hybrid-Ed25519+ML-DSA-44")
    c = claims(0)
    sr, toks = fx.epoch([c])
    assert fx.edge.verify(toks[0], T0 + 5, mkurl(c))[0]
    for off in (3, 64 + 7):
        bad = SignedRoot(sr.kid, sr.epoch, sr.t_start_ms, sr.delta_ms, sr.N, sr.root, bytearray(sr.sig))
        bad.sig[off] ^= 1
        bad.sig = bytes(bad.sig)
        e = EmberEdge(fx.signer, 1, 16, 3600, fetch_fn=lambda k, ep: bad)
        assert not e.verify(toks[0], T0 + 5, mkurl(c))[0]


def test_cross_tenant_pooled():
    fx = Fx("Ed25519")
    ca, cb = claims(0, tenant=3), claims(1, tenant=9)
    sr, toks = fx.epoch([ca, cb])
    assert fx.edge.verify(toks[0], T0 + 5, mkurl(ca))[0]
    # replay tenant A's leaf with Tenant=B in the claims
    swapped = ca.with_(tenant=9)
    bad = enc(swapped).decode() + toks[0][len(enc(ca)):]
    assert not fx.edge.verify(bad, T0 + 5, mkurl(ca))[0]


def test_epoch_wrap():
    s = make_signer("Ed25519", CTX_ROOT)
    iss = EmberIssuer(s, 1, t0=T0)
    iss.epoch = EPOCH_MAX
    iss.submit(claims(0))
    with pytest.raises(OverflowError):
        iss.close_epoch(T0 + 1)


def test_negative_cache():
    fx = Fx("Ed25519")
    c = claims(0)
    sr, toks = fx.epoch([c])
    calls = []
    e = EmberEdge(fx.signer, 1, 16, 3600, fetch_fn=lambda k, ep: calls.append(ep), negative_ttl=1.0)
    assert not e.verify(toks[0], T0 + 5, mkurl(c))[0]
    assert not e.verify(toks[0], T0 + 5.5, mkurl(c))[0]
    assert len(calls) == 1 and e.stats["neg_hits"] == 1


def test_pad_pow2():
    s = make_signer("Ed25519", CTX_ROOT)
    iss = EmberIssuer(s, 1, pad_pow2=True, t0=T0)
    cl = [claims(i) for i in range(5)]
    for c in cl:
        iss.submit(c)
    sr, toks, _ = iss.close_epoch(T0 + 1)
    assert sr.N == 8
    e = EmberEdge(s, 1, 16, 3600, fetch_fn=lambda k, ep: sr)
    assert all(e.verify(toks[i], T0 + 2, mkurl(cl[i]))[0] for i in range(5))


# ------------------------------------------------------------------ per-token baselines
@pytest.mark.parametrize("sid", ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B5v", "B6v",
                                 "B10", "B11", "B12"])
def test_pertoken(sid):
    sch = make_scheme(sid)
    c = claims(0)
    tok = sch.issue(c)
    assert sch.verify(tok, T0, mkurl(c))[0]
    if sid.endswith("v"):
        ok, why = sch.verify(tok, T0, mkurl(c))
        assert ok and why == "cache_hit"
    # tamper signature and claims
    i = (tok.index(":Sig=") + 7) if sid == "B10" else len(tok) - 3  # B10 domain 0 checks tag 0
    bad = tok[:i] + ("A" if tok[i] != "A" else "B") + tok[i + 1:]
    sch2 = make_scheme(sid) if sid.endswith("v") else sch
    if sid.endswith("v"):  # use a fresh cache, same keys
        sch.cache = VerifyCache()
        sch2 = sch
    assert not sch2.verify(bad, T0, mkurl(c))[0]
    c2 = c.with_(expires=c.expires + 1)
    bad2 = enc(c2).decode() + tok[len(enc(c)):]
    assert not sch2.verify(bad2, T0, mkurl(c))[0]
    assert not sch2.verify(tok, c.expires + 100, mkurl(c))[0]  # expired (cache respects Expires)


def test_multimac_domains():
    for k in (1, 3, 10):
        sch = make_scheme("B10", k=k)
        c = claims(0)
        tok = sch.issue(c)
        from ember.token import decode_pertoken
        _, ce, sig = decode_pertoken(tok)
        assert len(sig) == 16 * k
        for j in range(k):
            assert sch.signer.verify(ce, sig, domain=j)
            b = bytearray(sig)
            b[16 * j] ^= 1
            assert not sch.signer.verify(ce, bytes(b), domain=j)


def test_b11_delegation():
    s = DelegatedEd25519().keygen()
    cert = s.new_delegation(7, not_after=T0 + 100)
    assert s.install_cert(cert)
    m = enc(claims(0))
    sig = s.sign(m)
    assert s.verify(m, sig, now=T0 + 50)
    assert not s.verify(m, sig, now=T0 + 101)  # expired delegated key
    rogue = Ed25519().keygen()  # Ed25519 under a non-certified key
    assert not s.verify(m, struct.pack(">I", 7) + rogue.sign(m), now=T0)
    assert not s.verify(m, struct.pack(">I", 8) + sig[4:], now=T0)  # unknown deleg id
    bad = bytearray(cert)
    bad[10] ^= 1
    s2 = DelegatedEd25519()
    s2.master = s.master
    assert not s2.install_cert(bytes(bad))


def test_b12_wrong_epoch():
    s = KemWrappedHMAC()
    pk, sk = KemWrappedHMAC.edge_keygen()
    w1 = s.new_epoch(1, [pk])
    assert s.install_wrap(1, w1[0], sk)
    m = enc(claims(0))
    sig1 = s.sign(m)
    w2 = s.new_epoch(2, [pk])
    assert s.install_wrap(2, w2[0], sk)
    sig2 = s.sign(m)
    assert s.verify(m, sig1) and s.verify(m, sig2)
    assert not s.verify(m, struct.pack(">I", 2) + sig1[4:])  # epoch-1 tag under epoch-2 key
    assert not s.verify(m, struct.pack(">I", 3) + sig1[4:])  # unknown epoch
    assert not s.install_wrap(2, w1[0], sk)                   # wrap bound to its epoch
    pk2, sk2 = KemWrappedHMAC.edge_keygen()
    assert not s.install_wrap(1, w1[0], sk2)                  # other edge cannot unwrap


def test_mtl_mode():
    signer = make_signer("Ed25519", CTX_ROOT)
    mtl = MTLMode(signer, kid=1, n=16)
    cl = [claims(i) for i in range(37)]
    for c in cl:
        mtl.append(enc(c), c.tenant)
    S, rungs, sig = mtl.sign_ladder()
    assert signer.verify(mtl.ladder_msg(S, rungs), sig)
    lad = {(h, s): x for h, s, x in rungs}
    for i in (0, 5, 31, 32, 35, 36):
        tok = mtl.encode(enc(cl[i]), i, S)
        assert MTLMode.verify_token(tok, lad, 1, 16)
        bad = tok[:-2] + ("A" if tok[-2] != "A" else "B") + tok[-1]
        assert not MTLMode.verify_token(bad, lad, 1, 16)


def test_split_cookies():
    sch = make_scheme("B5c")
    tok = sch.issue(claims(0))
    parts = split_cookies(tok, 2)
    assert "".join(p.split("=", 1)[1] for p in parts) == tok
    assert all(len(p) <= 4096 for p in parts)


if __name__ == "__main__":
    sys.exit(pytest.main([os.path.abspath(__file__), "-q"]))
