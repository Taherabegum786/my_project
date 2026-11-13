"""ctypes binding to libpqshim.so (liboqs 0.16.0 static archive, whole-archive linked) plus CPU-time counters."""
import ctypes
import os
import time

_LIB = None
HERE = os.path.dirname(os.path.abspath(__file__))


def lib():
    global _LIB
    if _LIB is None:
        cands = [os.environ.get("PQSHIM_LIB", ""),
                 os.path.join(HERE, "..", "..", "..", "papers", "benchmark", "experiments", "build", "libpqshim.so")]
        path = next((c for c in cands if c and os.path.exists(c)), None)
        if path is None:
            raise RuntimeError("libpqshim.so not found; run run.sh (or set PQSHIM_LIB)")
        L = ctypes.CDLL(path)
        vp, sz, cp = ctypes.c_void_p, ctypes.c_size_t, ctypes.c_char_p
        L.pq_init.restype = None
        L.pq_version.restype = cp
        L.pq_enabled.argtypes = [cp]; L.pq_enabled.restype = ctypes.c_int
        L.pq_new.argtypes = [cp]; L.pq_new.restype = vp
        L.pq_free.argtypes = [vp]
        for f in ("pq_pk_len", "pq_sk_len", "pq_sig_len"):
            getattr(L, f).argtypes = [vp]; getattr(L, f).restype = sz
        L.pq_keypair.argtypes = [vp, vp, vp]; L.pq_keypair.restype = ctypes.c_int
        L.pq_sign.argtypes = [vp, vp, ctypes.POINTER(sz), cp, sz, vp]; L.pq_sign.restype = ctypes.c_int
        L.pq_verify.argtypes = [vp, cp, sz, cp, sz, cp]; L.pq_verify.restype = ctypes.c_int
        L.pq_init()
        _LIB = L
    return _LIB


def version():
    return lib().pq_version().decode()


class Counters:
    """Thread-CPU nanoseconds spent inside signature calls."""
    def __init__(self):
        self.sign_ns = 0; self.verify_ns = 0; self.n_sign = 0; self.n_verify = 0

    def reset(self):
        self.__init__()


class PQ:
    """One liboqs signature scheme: keypair, sign, verify (real calls)."""
    _keys = {}

    def __init__(self, name, ctr=None):
        L = lib()
        self.name = name; self.ctr = ctr or Counters()
        self.h = L.pq_new(name.encode())
        if not self.h:
            raise ValueError(f"liboqs: {name} not enabled")
        self.pk_len = L.pq_pk_len(self.h); self.sk_len = L.pq_sk_len(self.h); self.sig_len = L.pq_sig_len(self.h)

    def keypair(self, cache=True):
        if cache and self.name in PQ._keys:
            return PQ._keys[self.name]
        pk = ctypes.create_string_buffer(self.pk_len); sk = ctypes.create_string_buffer(self.sk_len)
        if not lib().pq_keypair(self.h, pk, sk):
            raise RuntimeError("keypair failed")
        kp = (pk.raw, sk.raw)
        if cache:
            PQ._keys[self.name] = kp
        return kp

    def sign(self, msg, sk):
        sig = ctypes.create_string_buffer(self.sig_len); n = ctypes.c_size_t(0)
        t = time.thread_time_ns()
        ok = lib().pq_sign(self.h, sig, ctypes.byref(n), msg, len(msg), sk)
        self.ctr.sign_ns += time.thread_time_ns() - t; self.ctr.n_sign += 1
        if not ok:
            raise RuntimeError("sign failed")
        return sig.raw[:n.value]

    def verify(self, msg, sig, pk):
        t = time.thread_time_ns()
        ok = lib().pq_verify(self.h, msg, len(msg), sig, len(sig), pk)
        self.ctr.verify_ns += time.thread_time_ns() - t; self.ctr.n_verify += 1
        return bool(ok)


class Ed:
    """Ed25519 through OpenSSL (python-cryptography)."""
    _kp = None

    def __init__(self, ctr=None):
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric import ed25519
        self.ctr = ctr or Counters()
        if Ed._kp is None:
            sk = ed25519.Ed25519PrivateKey.generate()
            Ed._kp = (sk, sk.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw))
        self.sk, self.pk = Ed._kp
        self._pub = ed25519.Ed25519PublicKey

    def sign(self, msg):
        t = time.thread_time_ns(); s = self.sk.sign(msg)
        self.ctr.sign_ns += time.thread_time_ns() - t; self.ctr.n_sign += 1
        return s

    def verify(self, msg, sig, pk=None):
        from cryptography.exceptions import InvalidSignature
        t = time.thread_time_ns()
        try:
            self._pub.from_public_bytes(pk or self.pk).verify(sig, msg); ok = True
        except (InvalidSignature, ValueError):
            ok = False
        self.ctr.verify_ns += time.thread_time_ns() - t; self.ctr.n_verify += 1
        return ok
