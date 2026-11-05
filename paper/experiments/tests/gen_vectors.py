"""Generate tests/vectors.json: shared test vectors the Go port (proto/tokens) must verify identically.

Run: python -m tests.gen_vectors
"""
import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cryptography.hazmat.primitives import serialization

from baselines.pertoken import make_scheme
from ember.edge import EmberEdge
from ember.issuer import EmberIssuer
from ember.signers import CTX_ROOT, CTX_TOKEN, make_signer
from ember.th import Th, tweak
from ember.token import Claims, EMBER_SEP, b64d, b64e, enc

T0 = 1_800_000_000.0
NOW = 1_800_000_010.0


def claims(i, tenant=7):
    return Claims("/v/tenant%d/movie%d/" % (tenant, 100 + i), int(T0 + 1800), tenant, "203.0.113.0/24" if i % 3 == 0 else None)


def mut(tok, off):
    cs, _, b = tok.rpartition(EMBER_SEP)
    blob = bytearray(b64d(b))
    blob[off] ^= 1
    return cs + EMBER_SEP + b64e(bytes(blob))


def main():
    out = {"doc": {
        "tweak": "26 B big-endian: ctx(8)='EMBERv1\\0' | kid u32 | epoch u32 | type u8 (0 leaf,1 node,2 root,3 period) | level u8 | index u32 | tenant u32 (leaf only; 0 otherwise)",
        "Th": "SHA-256(tweak || data)[:n]",
        "leaf": "Th(tweak(kid,e,LEAF,0,i,tenant), r16 || claims_ascii)",
        "node": "level l+1 node j = Th(tweak(kid,e,NODE,l+1,j,0), left||right); unpaired last node promoted unchanged; root = top node",
        "token": "claims ':E=' b64url_nopad( ver u8=1 | alg u8 (signer_id<<4 | n==32) | kid u32 | epoch u32 | idx u32 | r[16] | path n*d )",
        "claims": "URLPrefix=<b64url_nopad(prefix)>:Expires=<int>:Tenant=<int>[:IP=<cidr>]",
        "signed_root_msg": "'EMBER-root' | kid u32 | epoch u32 | t_start_ms u64 | delta_ms u32 | N u32 | root ; ML-DSA context 'EMBER-root'",
        "signed_root_wire": "kid u32|epoch u32|t_start_ms u64|delta_ms u32|N u32|n u8|root|sig",
        "pertoken": "claims ':Sig=' b64url_nopad(sig) ; signed message = claims ASCII; ML-DSA context 'CDN-token'; Ed25519/ECDSA sign 'CDN-token'||claims (prefix); HMAC over claims (no prefix)",
        "B11": "sig = deleg_id u32 | Ed25519(prefix 'CDN-token'||claims); cert = deleg_id u32|kid u32|ed_pk[32]|not_after u64 || ML-DSA-44 sig (context 'EMBER-deleg') over the 48-B body",
        "B12": "sig = epoch u32 | HMAC-SHA256(k_e, claims)",
        "validity": "accept iff now <= Expires+tau and Expires <= t_start+delta+V_max+tau (seconds; tau=5, V_max=3600) and idx < N and URL has prefix",
        "alg_ids": {"ML-DSA-44": 1, "ML-DSA-65": 2, "SLH-DSA-128s": 3, "SLH-DSA-128f": 4, "Hybrid-Ed25519+ML-DSA-44": 5, "Ed25519": 6},
        "now": NOW, "v_max": 3600, "tau_skew": 5,
    }}
    out["th"] = [{"kid": 1, "epoch": 2, "type": 1, "level": 3, "index": 4, "tenant": 0, "data": "00" * 32, "n": n,
                  "tweak": tweak(1, 2, 1, 3, 4, 0).hex(), "out": Th(tweak(1, 2, 1, 3, 4, 0), bytes(32), n).hex()} for n in (16, 32)]

    ember = []
    for signer_name in ("ML-DSA-44", "Ed25519", "Hybrid-Ed25519+ML-DSA-44"):
        for n in (16, 32):
            for N in (1, 5, 1000):
                if signer_name != "ML-DSA-44" and N == 1000:
                    continue
                s = make_signer(signer_name, CTX_ROOT)
                iss = EmberIssuer(s, kid=7, n=n, t0=T0)
                cl = [claims(i) for i in range(N)]
                tk = [iss.submit(c) for c in cl]
                sr, toks, _ = iss.close_epoch(T0 + 1)
                edge = EmberEdge(s, 7, n, 3600, fetch_fn=lambda k, e: sr)
                if signer_name == "ML-DSA-44":
                    pk = s.pk.hex()
                elif signer_name == "Ed25519":
                    pk = s.pk.public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw).hex()
                else:
                    pk = s.ed.pk.public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw).hex() + s.ml.pk.hex()
                cases = []
                for i in sorted({0, N // 2, N - 1}):
                    t = toks[tk[i]]
                    url = cl[i].url_prefix + "seg_1.ts"
                    assert edge.verify(t, NOW, url)[0]
                    cases.append({"token": t, "url": url, "valid": True, "reason": "ok"})
                    if N > 1:
                        bad = mut(t, 30 if N > 1 else 20)
                        assert not edge.verify(bad, NOW, url)[0]
                        cases.append({"token": bad, "url": url, "valid": False, "reason": "path bit flip"})
                    bad = mut(t, 20)
                    assert not edge.verify(bad, NOW, url)[0]
                    cases.append({"token": bad, "url": url, "valid": False, "reason": "salt bit flip"})
                    cases.append({"token": t, "url": "/other/x.ts", "valid": False, "reason": "url prefix"})
                ember.append({"root_signer": signer_name, "n": n, "N": N, "pk_hex": pk,
                              "signed_root_hex": sr.to_bytes().hex(), "root_hex": sr.root.hex(),
                              "root_msg_hex": sr.msg().hex(), "cases": cases})
    out["ember"] = ember

    per = []
    for sid in ("B1", "B2", "B3", "B5", "B11", "B12"):
        sch = make_scheme(sid)
        c = claims(1)
        tok = sch.issue(c)
        url = c.url_prefix + "seg_1.ts"
        bad = tok[:-3] + ("A" if tok[-3] != "A" else "B") + tok[-2:]
        assert sch.verify(tok, NOW, url)[0] and not sch.verify(bad, NOW, url)[0]
        sg = sch.signer
        if sid == "B1":
            key = {"hmac_key_hex": sg.sk.hex()}
        elif sid == "B2":
            key = {"ed25519_pk_hex": sg.pk.public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw).hex()}
        elif sid == "B3":
            key = {"p256_pk_uncompressed_hex": sg.pk.public_bytes(encoding=serialization.Encoding.X962, format=serialization.PublicFormat.UncompressedPoint).hex()}
        elif sid == "B5":
            key = {"mldsa44_pk_hex": sg.pk.hex()}
        elif sid == "B11":
            key = {"mldsa44_master_pk_hex": sg.master.pk.hex(), "cert_hex": sch.cert.hex()}
        else:
            key = {"epoch": 1, "k_e_hex": sg.keys[1].hex()}
        per.append({"scheme": sid, **key, "cases": [
            {"token": tok, "url": url, "valid": True}, {"token": bad, "url": url, "valid": False}]})
    out["pertoken"] = per
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vectors.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print("wrote", path, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    main()
