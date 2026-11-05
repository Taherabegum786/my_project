"""Claims, canonical encoding and wire formats (signed URL / signed cookie).

claims  = URLPrefix=<b64url(prefix)>:Expires=<unix>:Tenant=<id>[:IP=<cidr>]
EMBER   = claims + ":E="   + b64url(ver|alg|kid|epoch|idx|r|path)      (30 + n*d raw bytes)
per-tok = claims + ":Sig=" + b64url(sig)
b64url is unpadded (RFC 4648 §5).
"""
import base64
import struct
from dataclasses import dataclass, replace
from typing import Optional

VER = 1
# alg byte: high nibble = root signer id, low bit = (n == 32)
ROOT_ALG_IDS = {"ML-DSA-44": 1, "ML-DSA-65": 2, "SLH-DSA-128s": 3, "SLH-DSA-128f": 4,
                "Hybrid-Ed25519+ML-DSA-44": 5, "Ed25519": 6, "ECDSA-P256": 7, "ML-DSA-87": 8}
ROOT_ALG_NAMES = {v: k for k, v in ROOT_ALG_IDS.items()}
_HDR = struct.Struct(">BBIII")  # ver, alg, kid, epoch, idx = 14 B (+16 B r = 30 B)
EMBER_SEP = ":E="
SIG_SEP = ":Sig="


def b64e(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode("ascii")


def b64d(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


@dataclass(frozen=True)
class Claims:
    url_prefix: str
    expires: int
    tenant: int
    ip: Optional[str] = None

    def with_(self, **kw):
        return replace(self, **kw)


def enc(c: Claims) -> bytes:
    s = "URLPrefix=%s:Expires=%d:Tenant=%d" % (b64e(c.url_prefix.encode()), c.expires, c.tenant)
    if c.ip is not None:
        s += ":IP=" + c.ip
    return s.encode("ascii")


def dec_claims(s: str) -> Claims:
    parts = s.split(":")
    kv = {}
    for p in parts:
        k, _, v = p.partition("=")
        if k in kv:
            raise ValueError("dup field")
        kv[k] = v
    if set(kv) - {"URLPrefix", "Expires", "Tenant", "IP"}:
        raise ValueError("unknown field")
    c = Claims(b64d(kv["URLPrefix"]).decode(), int(kv["Expires"]), int(kv["Tenant"]), kv.get("IP"))
    if enc(c).decode() != s:  # canonical form only
        raise ValueError("non-canonical claims")
    return c


def alg_byte(root_signer: str, n: int) -> int:
    return (ROOT_ALG_IDS[root_signer] << 4) | (1 if n == 32 else 0)


def encode_ember(c: Claims, kid: int, epoch: int, idx: int, r: bytes, path, n: int, alg: str) -> str:
    blob = _HDR.pack(VER, alg_byte(alg, n), kid, epoch, idx) + r + b"".join(path)
    return enc(c).decode() + EMBER_SEP + b64e(blob)


@dataclass
class EmberTok:
    claims: Claims
    claims_enc: bytes
    alg: str
    n: int
    kid: int
    epoch: int
    idx: int
    r: bytes
    path: list


def decode_ember(tok: str) -> EmberTok:
    cs, sep, blob_s = tok.rpartition(EMBER_SEP)
    if not sep:
        raise ValueError("no EMBER blob")
    c = dec_claims(cs)
    blob = b64d(blob_s)
    if len(blob) < 30:
        raise ValueError("short blob")
    ver, a, kid, epoch, idx = _HDR.unpack_from(blob)
    if ver != VER:
        raise ValueError("bad version")
    alg = ROOT_ALG_NAMES.get(a >> 4)
    if alg is None or (a & 0x0E):
        raise ValueError("bad alg")
    n = 32 if (a & 1) else 16
    r = blob[14:30]
    rest = blob[30:]
    if len(rest) % n:
        raise ValueError("bad path length")
    path = [rest[k:k + n] for k in range(0, len(rest), n)]
    return EmberTok(c, cs.encode("ascii"), alg, n, kid, epoch, idx, r, path)


def encode_pertoken(c: Claims, scheme: str, sig: bytes) -> str:
    return enc(c).decode() + SIG_SEP + b64e(sig)


def decode_pertoken(tok: str):
    cs, sep, sig_s = tok.rpartition(SIG_SEP)
    if not sep:
        raise ValueError("no Sig")
    c = dec_claims(cs)
    return c, cs.encode("ascii"), b64d(sig_s)


def to_signed_url(base_url: str, token: str) -> str:
    return base_url + "?Token=" + token


def to_cookie(token: str) -> str:
    return "Edge-Token=" + token


def url_matches(c: Claims, url_path: str) -> bool:
    return url_path.startswith(c.url_prefix)
