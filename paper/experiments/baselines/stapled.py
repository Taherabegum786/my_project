"""M2 / B5s (revision round 1, reviewer item M2): stapled per-token ML-DSA-44.

The issuer signs every token individually with ML-DSA-44, exactly like B5, but the 2,420-B signature is NOT carried
in the URL/cookie.  The URL carries only the canonical claims plus a short reference (kid | 16-B nonce).  The client
sends the full signature once per edge connection in a header (`X-Token-Sig`, "staple"); the edge verifies it and
caches H(claims | kid | nonce) as verified until the claims' expiry.  Later requests on that edge cost one hash and a
table lookup.  This is EMBER with every tree of size N = 1 and without the epoch/index/salt fields, i.e. the
reviewer's "stapled per-token signature" baseline that isolates the value of the Merkle tree.

Wire forms (b64url unpadded, RFC 4648 §5):
  URL token  = claims ":S=" b64url(kid[4] | nonce[16])            (20 raw bytes -> 27 chars)
  staple hdr = "x-token-sig: " b64url(sig[2420])                   (3,227 chars)
  signed msg = "CDN-token-staple" | kid[4] | nonce[16] | claims
An edge that receives a token it has not verified and no staple answers `staple_required` (the client retries
with the header: +1 client-edge RTT), or, if a fetch function is configured, pulls the per-token signature from the
issuer's signature store keyed by the reference (no sharing between tokens, so every (token, edge) pair is a miss).
"""
import hashlib
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ember.signers import make_signer
from ember.token import b64d, b64e, dec_claims, enc, url_matches

SEP = ":S="
CTX = b"CDN-token-staple"
HDR = "x-token-sig"


def _msg(kid, nonce, claims_enc):
    return CTX + struct.pack(">I", kid) + nonce + claims_enc


class StapledPerTokenIssuer:
    def __init__(self, alg="ML-DSA-44", kid=1):
        self.signer = make_signer(alg, CTX)
        self.kid = kid
        self.store = {}          # reference -> signature (optional pull path)

    def issue(self, claims):
        """Returns (url_token, staple_signature_bytes)."""
        ce = enc(claims)
        nonce = os.urandom(16)
        sig = self.signer.sign(_msg(self.kid, nonce, ce))
        ref = struct.pack(">I", self.kid) + nonce
        self.store[ref] = sig
        return ce.decode() + SEP + b64e(ref), sig


def decode(tok):
    cs, sep, ref_s = tok.rpartition(SEP)
    if not sep:
        raise ValueError("no ref")
    c = dec_claims(cs)
    ref = b64d(ref_s)
    if len(ref) != 20:
        raise ValueError("bad ref")
    return c, cs.encode("ascii"), ref


class StapledPerTokenEdge:
    def __init__(self, pk_signer, kid=1, tau_skew=5.0, fetch_fn=None, capacity=1_000_000):
        self.signer, self.kid, self.tau = pk_signer, kid, tau_skew
        self.fetch_fn = fetch_fn
        self.cache = {}          # 16-B H(claims | ref) -> expiry
        self.capacity = capacity
        self.stats = dict(sig_verifs=0, fetches=0, staple_required=0)

    @staticmethod
    def key(ce, ref):
        return hashlib.sha256(ref + ce).digest()[:16]

    def verify(self, tok, now, url, staple: bytes = None):
        """Returns (ok, reason)."""
        try:
            c, ce, ref = decode(tok)
        except Exception:
            return False, "malformed"
        if struct.unpack(">I", ref[:4])[0] != self.kid:
            return False, "unknown_kid"
        if now > c.expires + self.tau:
            return False, "expired"
        if not url_matches(c, url):
            return False, "url"
        k = self.key(ce, ref)
        exp = self.cache.get(k)
        if exp is not None and exp >= now:
            return True, "cache_hit"
        sig = staple
        if sig is None and self.fetch_fn is not None:
            self.stats["fetches"] += 1
            sig = self.fetch_fn(ref)
        if sig is None:
            self.stats["staple_required"] += 1
            return False, "staple_required"
        self.stats["sig_verifs"] += 1
        if not self.signer.verify(_msg(self.kid, ref[4:], ce), sig):
            return False, "sig"
        if len(self.cache) >= self.capacity:
            self.cache.pop(next(iter(self.cache)))
        self.cache[k] = c.expires + self.tau
        return True, "ok"
