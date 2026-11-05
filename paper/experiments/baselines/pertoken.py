"""Per-token baselines B1..B12 sharing the ember.token claim encoding.

Scheme IDs (design.md §5):
 B1 HMAC-SHA256, B2 Ed25519, B3 ECDSA-P256, B4 RSA-2048, B5 ML-DSA-44, B6 ML-DSA-65,
 B7 SLH-DSA-128s, B8 SLH-DSA-128f, B9 Hybrid Ed25519+ML-DSA-44,
 B5v/B6v (+ verified-token cache), B5c/B6c (split over 2 cookies),
 B10 Multi-MAC(k), B11 delegated short-lived Ed25519, B12 ML-KEM-wrapped epoch HMAC key.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ember.signers import (CTX_TOKEN, DelegatedEd25519, KemWrappedHMAC, MultiMAC, VerifyCache,
                           make_signer)
from ember.token import decode_pertoken, encode_pertoken, url_matches

PERTOKEN = {"B1": "HMAC-SHA256", "B2": "Ed25519", "B3": "ECDSA-P256", "B4": "RSA-2048",
            "B5": "ML-DSA-44", "B6": "ML-DSA-65", "B7": "SLH-DSA-128s", "B8": "SLH-DSA-128f",
            "B9": "Hybrid-Ed25519+ML-DSA-44"}


class PerTokenScheme:
    def __init__(self, signer, label=None, vcache=False, tau_skew=5.0):
        self.signer = signer
        self.label = label or signer.name
        self.cache = VerifyCache() if vcache else None
        self.tau = tau_skew

    def issue(self, claims):
        from ember.token import enc
        return encode_pertoken(claims, self.label, self.signer.sign(enc(claims)))

    def verify(self, token, now, url):
        if self.cache is not None and self.cache.check(token, now):
            return True, "cache_hit"
        try:
            c, ce, sig = decode_pertoken(token)
        except Exception:
            return False, "malformed"
        if now > c.expires + self.tau:
            return False, "expired"
        if not url_matches(c, url):
            return False, "url"
        if not self.signer.verify(ce, sig):
            return False, "sig"
        if self.cache is not None:
            self.cache.put(token, c.expires + self.tau)
        return True, "ok"


def make_scheme(sid, **kw):
    """Factory for the per-token baselines.  Returns a PerTokenScheme (keys generated)."""
    if sid in PERTOKEN:
        return PerTokenScheme(make_signer(PERTOKEN[sid], CTX_TOKEN), sid)
    if sid in ("B5v", "B6v"):
        return PerTokenScheme(make_signer(PERTOKEN[sid[:2]], CTX_TOKEN), sid, vcache=True)
    if sid in ("B5c", "B6c"):
        return PerTokenScheme(make_signer(PERTOKEN[sid[:2]], CTX_TOKEN), sid)
    if sid.startswith("B10"):
        k = kw.get("k", 3)
        return PerTokenScheme(MultiMAC(k).keygen(), "B10k%d" % k)
    if sid == "B11":
        s = DelegatedEd25519().keygen()
        cert = s.new_delegation(1, kw.get("not_after", 2 ** 40))
        s.install_cert(cert)
        sch = PerTokenScheme(s, "B11")
        sch.cert = cert
        return sch
    if sid == "B12":
        s = KemWrappedHMAC()
        pk, sk = KemWrappedHMAC.edge_keygen()
        wraps = s.new_epoch(1, [pk])
        assert s.install_wrap(1, wraps[0], sk)
        sch = PerTokenScheme(s, "B12")
        sch.wrap_bytes = len(wraps[0])
        return sch
    raise KeyError(sid)


def split_cookies(token, parts=2):
    """B5c/B6c: split a token across `parts` cookies Edge-Token0..; returns list of cookie strings."""
    L = len(token)
    step = -(-L // parts)
    return ["Edge-Token%d=%s" % (j, token[j * step:(j + 1) * step]) for j in range(parts)]
