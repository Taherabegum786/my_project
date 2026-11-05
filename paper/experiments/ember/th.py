"""Tweakable hash Th(T, x) = trunc_n(SHA-256(T || x)).

Tweak layout (EMBER v1, 26 bytes, big-endian):
    ctx(8)="EMBERv1\\0" | kid(4) | epoch(4) | type(1) | level(1) | index(4) | tenant(4)

The spec (experiment_spec.md §2) lists a 22-B tweak; we append a 4-B tenant id
so that leaves of different tenants in a pooled tree live in distinct hash
domains (Critic D6: "the tenant id is in the leaf tweak").  Internal nodes,
period trees and the root use tenant = 0.  This layout is normative for the Go
port (see tests/vectors.json).
"""
import hashlib
import struct

CTX = b"EMBERv1\0"
TYPE_LEAF, TYPE_NODE, TYPE_ROOT, TYPE_PERIOD = 0, 1, 2, 3
TWEAK_LEN = 26
_PACK = struct.Struct(">8sIIBBII")
_sha256 = hashlib.sha256


def tweak(kid: int, epoch: int, typ: int, level: int, index: int, tenant: int = 0) -> bytes:
    return _PACK.pack(CTX, kid, epoch, typ, level, index, tenant)


def Th(tw: bytes, data: bytes, n: int) -> bytes:
    return _sha256(tw + data).digest()[:n]
