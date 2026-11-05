"""Uniform Signer interface for root signers, per-token signers and the Critic baselines.

Signer: name; keygen(); sign(msg)->bytes; verify(msg, sig)->bool; sig_len; pk_len
Backends: pqcrypto 1.0.0 (ML-DSA, SLH-DSA, ML-KEM), cryptography 50.0.2 (Ed25519, ECDSA,
RSA, AES-GCM, HKDF), Python hmac/hashlib (HMAC-SHA256).
"""
import hashlib
import hmac as _hmac
import os
import struct
from collections import OrderedDict

from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, ed25519, padding, rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization

import pqcrypto
from pqcrypto.sign import ml_dsa_44, ml_dsa_65, ml_dsa_87, slh_dsa_sha2_128s, slh_dsa_sha2_128f
from pqcrypto.kem import ml_kem_768

from .th import Th, tweak, TYPE_LEAF, TYPE_NODE

CTX_ROOT = b"EMBER-root"
CTX_TOKEN = b"CDN-token"
_RAW = dict(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)


class Signer:
    name = "abstract"
    backend = ""
    sig_len = 0
    pk_len = 0

    def __init__(self, context: bytes = CTX_TOKEN):
        self.ctx = context
        self.pk = None
        self.sk = None

    def keygen(self):
        raise NotImplementedError

    def sign(self, msg: bytes) -> bytes:
        raise NotImplementedError

    def verify(self, msg: bytes, sig: bytes) -> bool:
        raise NotImplementedError


# ---------------------------------------------------------------- symmetric
class HMACSHA256(Signer):
    name, backend, sig_len, pk_len = "HMAC-SHA256", "hashlib", 32, 0

    def keygen(self):
        self.sk = os.urandom(32)
        return self

    def sign(self, msg):
        return _hmac.new(self.sk, msg, hashlib.sha256).digest()

    def verify(self, msg, sig):
        return _hmac.compare_digest(_hmac.new(self.sk, msg, hashlib.sha256).digest(), sig)


class MultiMAC(Signer):
    """B10: k truncated 16-B HMAC-SHA256 tags under independent keys (one per verifier domain)."""
    backend = "hashlib"
    pk_len = 0

    def __init__(self, k=3, context=CTX_TOKEN, domain=0):
        super().__init__(context)
        self.k = k
        self.domain = domain
        self.name = "MultiMAC-k%d" % k
        self.sig_len = 16 * k

    def keygen(self):
        self.keys = [os.urandom(32) for _ in range(self.k)]
        return self

    def sign(self, msg):
        return b"".join(_hmac.new(kk, msg, hashlib.sha256).digest()[:16] for kk in self.keys)

    def verify(self, msg, sig, domain=None):
        j = self.domain if domain is None else domain
        if len(sig) != self.sig_len:
            return False
        tag = _hmac.new(self.keys[j], msg, hashlib.sha256).digest()[:16]
        return _hmac.compare_digest(tag, sig[16 * j:16 * j + 16])


# ---------------------------------------------------------------- classical
class Ed25519(Signer):
    name, backend, sig_len, pk_len = "Ed25519", "cryptography-50.0.2", 64, 32

    def keygen(self):
        self.sk = ed25519.Ed25519PrivateKey.generate()
        self.pk = self.sk.public_key()
        return self

    def sign(self, msg):
        return self.sk.sign(self.ctx + msg)

    def verify(self, msg, sig):
        try:
            self.pk.verify(sig, self.ctx + msg)
            return True
        except InvalidSignature:
            return False


class ECDSAP256(Signer):
    name, backend, sig_len, pk_len = "ECDSA-P256", "cryptography-50.0.2", 72, 65

    def keygen(self):
        self.sk = ec.generate_private_key(ec.SECP256R1())
        self.pk = self.sk.public_key()
        return self

    def sign(self, msg):
        return self.sk.sign(self.ctx + msg, ec.ECDSA(hashes.SHA256()))

    def verify(self, msg, sig):
        try:
            self.pk.verify(sig, self.ctx + msg, ec.ECDSA(hashes.SHA256()))
            return True
        except InvalidSignature:
            return False


class RSA2048(Signer):
    name, backend, sig_len, pk_len = "RSA-2048", "cryptography-50.0.2", 256, 270

    def keygen(self):
        self.sk = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.pk = self.sk.public_key()
        return self

    def sign(self, msg):
        return self.sk.sign(self.ctx + msg, padding.PKCS1v15(), hashes.SHA256())

    def verify(self, msg, sig):
        try:
            self.pk.verify(sig, self.ctx + msg, padding.PKCS1v15(), hashes.SHA256())
            return True
        except InvalidSignature:
            return False


# ---------------------------------------------------------------- PQ (pqcrypto)
class _PQ(Signer):
    backend = "pqcrypto-1.0.0"
    mod = None

    def keygen(self):
        self.pk, self.sk = self.mod.keygen()
        return self

    def sign(self, msg):
        return self.mod.sign(self.sk, msg, context=self.ctx)

    def verify(self, msg, sig):
        try:
            self.mod.verify(self.pk, msg, sig, context=self.ctx)
            return True
        except (pqcrypto.InvalidSignatureError, ValueError):
            return False


class MLDSA44(_PQ):
    name, mod, sig_len, pk_len = "ML-DSA-44", ml_dsa_44, 2420, 1312


class MLDSA65(_PQ):
    name, mod, sig_len, pk_len = "ML-DSA-65", ml_dsa_65, 3309, 1952


class MLDSA87(_PQ):
    name, mod, sig_len, pk_len = "ML-DSA-87", ml_dsa_87, 4627, 2592


class SLHDSA128s(_PQ):
    name, mod, sig_len, pk_len = "SLH-DSA-128s", slh_dsa_sha2_128s, 7856, 32


class SLHDSA128f(_PQ):
    name, mod, sig_len, pk_len = "SLH-DSA-128f", slh_dsa_sha2_128f, 17088, 32


class HybridEd25519MLDSA44(Signer):
    """AND-combiner: sig = sig_Ed25519(64) || sig_ML-DSA-44(2420); both must verify."""
    name, backend, sig_len, pk_len = "Hybrid-Ed25519+ML-DSA-44", "cryptography+pqcrypto", 64 + 2420, 32 + 1312

    def __init__(self, context=CTX_TOKEN):
        super().__init__(context)
        self.ed = Ed25519(context)
        self.ml = MLDSA44(context)

    def keygen(self):
        self.ed.keygen()
        self.ml.keygen()
        return self

    def sign(self, msg):
        return self.ed.sign(msg) + self.ml.sign(msg)

    def verify(self, msg, sig):
        if len(sig) != self.sig_len:
            return False
        a = self.ed.verify(msg, sig[:64])
        b = self.ml.verify(msg, sig[64:])
        return a and b


SIGNERS = {c.name: c for c in [HMACSHA256, Ed25519, ECDSAP256, RSA2048, MLDSA44, MLDSA65, MLDSA87,
                               SLHDSA128s, SLHDSA128f, HybridEd25519MLDSA44]}


def make_signer(name, context=CTX_TOKEN):
    return SIGNERS[name](context).keygen()


# ---------------------------------------------------------------- B11
class DelegatedEd25519(Signer):
    """B11: an ML-DSA-44-signed delegation cert {deleg_id, kid, ed_pk, not_after} per epoch of
    validity V_max; token authenticator = deleg_id(4) || Ed25519 sig(64).  The edge caches verified
    certs (fetched/pushed like EMBER roots)."""
    name, backend, sig_len, pk_len = "Delegated-Ed25519", "cryptography+pqcrypto", 68, 1312
    _CERT = struct.Struct(">II32sQ")

    def __init__(self, context=CTX_TOKEN, kid=1):
        super().__init__(context)
        self.kid = kid
        self.master = MLDSA44(b"EMBER-deleg")
        self.certs = {}        # issuer side: deleg_id -> (ed key, cert bytes)
        self.cur = None
        self.edge_certs = {}   # edge side: deleg_id -> (Ed25519PublicKey, not_after)

    def keygen(self):
        self.master.keygen()
        self.pk = self.master.pk
        return self

    def new_delegation(self, deleg_id, not_after):
        ed = Ed25519(self.ctx).keygen()
        body = self._CERT.pack(deleg_id, self.kid, ed.pk.public_bytes(**_RAW), int(not_after))
        cert = body + self.master.sign(body)
        self.certs[deleg_id] = (ed, cert)
        self.cur = deleg_id
        return cert

    def sign(self, msg):
        ed, _ = self.certs[self.cur]
        return struct.pack(">I", self.cur) + ed.sign(msg)

    # edge side
    def install_cert(self, cert):
        body, sig = cert[:self._CERT.size], cert[self._CERT.size:]
        if not self.master.verify(body, sig):
            return False
        did, kid, edpk, na = self._CERT.unpack(body)
        if kid != self.kid:
            return False
        self.edge_certs[did] = (ed25519.Ed25519PublicKey.from_public_bytes(edpk), na)
        return True

    def verify(self, msg, sig, now=None):
        if len(sig) != 68:
            return False
        did = struct.unpack(">I", sig[:4])[0]
        ent = self.edge_certs.get(did)
        if ent is None:
            return False
        pk, na = ent
        if now is not None and now > na:
            return False
        try:
            pk.verify(sig[4:], self.ctx + msg)
            return True
        except InvalidSignature:
            return False


# ---------------------------------------------------------------- B12
class KemWrappedHMAC(Signer):
    """B12: per-epoch HMAC key k_e, wrapped to each edge with ML-KEM-768 + HKDF-SHA256 + AES-256-GCM.
    Token authenticator = epoch(4) || HMAC-SHA256(k_e, msg)(32)."""
    name, backend, sig_len, pk_len = "KEM-wrapped-HMAC", "pqcrypto+cryptography", 36, 1184

    def __init__(self, context=CTX_TOKEN):
        super().__init__(context)
        self.keys = {}       # issuer: epoch -> k_e
        self.cur = None
        self.edge_keys = {}  # edge: epoch -> k_e

    def keygen(self):
        return self

    @staticmethod
    def edge_keygen():
        return ml_kem_768.keygen()  # (pk, sk)

    @staticmethod
    def _kek(ss, epoch):
        return HKDF(algorithm=hashes.SHA256(), length=32, salt=None,
                    info=b"EMBER-B12" + struct.pack(">I", epoch)).derive(ss)

    def new_epoch(self, epoch, edge_pks):
        k = os.urandom(32)
        self.keys[epoch] = k
        self.cur = epoch
        wraps = []
        for pk in edge_pks:
            ct, ss = ml_kem_768.encaps(pk)
            wraps.append(ct + AESGCM(self._kek(ss, epoch)).encrypt(b"\0" * 12, k, struct.pack(">I", epoch)))
        return wraps

    def install_wrap(self, epoch, wrap, edge_sk):
        ct, body = wrap[:1088], wrap[1088:]
        ss = ml_kem_768.decaps(edge_sk, ct)
        try:
            k = AESGCM(self._kek(ss, epoch)).decrypt(b"\0" * 12, body, struct.pack(">I", epoch))
        except InvalidTag:
            return False
        self.edge_keys[epoch] = k
        return True

    def sign(self, msg):
        return struct.pack(">I", self.cur) + _hmac.new(self.keys[self.cur], msg, hashlib.sha256).digest()

    def verify(self, msg, sig):
        if len(sig) != 36:
            return False
        e = struct.unpack(">I", sig[:4])[0]
        k = self.edge_keys.get(e)
        if k is None:
            return False
        return _hmac.compare_digest(_hmac.new(k, msg, hashlib.sha256).digest(), sig[4:])


# ---------------------------------------------------------------- B13 MTL mode
class MTLMode:
    """B13: a profile of MTL mode (draft-harvey-cfrg-mtl-mode).  One growing message series per
    (kid, series id); every Delta the signer signs a *ladder* = the perfect-subtree peaks (rungs)
    covering the series so far.  Condensed signature = idx | rung height | r | path-to-rung.
    Path length = rung height, which grows with the series length (not with the epoch batch)."""
    _HDR = struct.Struct(">BBIIIB")  # ver, alg, kid, sid, idx, rung_h  (15 B) + r(16)

    def __init__(self, signer, kid=1, sid=0, n=16):
        self.signer, self.kid, self.sid, self.n = signer, kid, sid, n
        self.nodes = [[]]   # nodes[l][j] covers leaves [j*2^l, (j+1)*2^l)
        self.salts = []

    def append(self, enc_c, tenant=0):
        i = len(self.nodes[0])
        r = os.urandom(16)
        self.salts.append(r)
        x = Th(tweak(self.kid, self.sid, TYPE_LEAF, 0, i, tenant), r + enc_c, self.n)
        self.nodes[0].append(x)
        l, j = 0, i
        while j & 1:  # complete the parent
            if len(self.nodes) <= l + 1:
                self.nodes.append([])
            p = Th(tweak(self.kid, self.sid, TYPE_NODE, l + 1, j >> 1),
                   self.nodes[l][j - 1] + self.nodes[l][j], self.n)
            self.nodes[l + 1].append(p)
            l += 1
            j >>= 1
        return i

    def ladder(self):
        """Rungs (h, start, hash) of the current series, high to low."""
        S = len(self.nodes[0])
        rungs, start = [], 0
        for h in range(S.bit_length() - 1, -1, -1):
            if S >> h & 1:
                rungs.append((h, start, self.nodes[h][start >> h]))
                start += 1 << h
        return S, rungs

    def ladder_msg(self, S, rungs):
        return b"MTL-ladder" + struct.pack(">III", self.kid, self.sid, S) + b"".join(
            struct.pack(">BI", h, s) + x for h, s, x in rungs)

    def sign_ladder(self):
        S, rungs = self.ladder()
        return S, rungs, self.signer.sign(self.ladder_msg(S, rungs))

    def condensed(self, i, S):
        """Condensed signature for leaf i relative to the ladder at series size S."""
        start = 0
        for h in range(S.bit_length() - 1, -1, -1):
            if S >> h & 1:
                if i < start + (1 << h):
                    path = []
                    for l in range(h):
                        path.append(self.nodes[l][(i >> l) ^ 1])
                    return h, path
                start += 1 << h
        raise ValueError("i not covered")

    def encode(self, claims_enc, i, S):
        h, path = self.condensed(i, S)
        blob = self._HDR.pack(1, 0x90 | (1 if self.n == 32 else 0), self.kid, self.sid, i, h) + self.salts[i] + b"".join(path)
        from .token import b64e
        return claims_enc.decode() + ":M=" + b64e(blob)

    @classmethod
    def verify_token(cls, tok, ladder_rungs, kid, n):
        """ladder_rungs: {(h, start): hash} from a verified ladder.  Returns True/False."""
        from .token import b64d, dec_claims
        cs, sep, b = tok.rpartition(":M=")
        if not sep:
            return False
        c = dec_claims(cs)
        blob = b64d(b)
        _, _, k, sid, i, h = cls._HDR.unpack_from(blob)
        if k != kid:
            return False
        r = blob[15:31]
        rest = blob[31:]
        if len(rest) != n * h:
            return False
        start = (i >> h) << h
        target = ladder_rungs.get((h, start))
        if target is None:
            return False
        x = Th(tweak(kid, sid, TYPE_LEAF, 0, i, c.tenant), r + cs.encode(), n)
        for l in range(h):
            sib = rest[l * n:(l + 1) * n]
            j = i >> l
            x = Th(tweak(kid, sid, TYPE_NODE, l + 1, j >> 1), (sib + x) if (j & 1) else (x + sib), n)
        return _hmac.compare_digest(x, target)


# ---------------------------------------------------------------- verify cache
class VerifyCache:
    """LRU keyed by SHA-256(token) -> Expires; a hit skips all crypto until Expires."""

    def __init__(self, capacity=100000):
        self.cap = capacity
        self.d = OrderedDict()
        self.hits = self.misses = 0

    def check(self, token: str, now) -> bool:
        k = hashlib.sha256(token.encode()).digest()
        e = self.d.get(k)
        if e is not None and now <= e:
            self.d.move_to_end(k)
            self.hits += 1
            return True
        self.misses += 1
        return False

    def put(self, token: str, expires):
        k = hashlib.sha256(token.encode()).digest()
        self.d[k] = expires
        self.d.move_to_end(k)
        if len(self.d) > self.cap:
            self.d.popitem(last=False)
