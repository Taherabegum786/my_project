"""EMBER edge verifier: root cache (with coalescing bookkeeping and a negative cache), epoch-bounded
validity, revocation, stapled roots and period bundles."""
import hmac

from .issuer import PeriodBundle, RevocationDelta, SignedRoot
from .merkle import leaf_hash, root_from_path
from .token import decode_ember, url_matches


class EmberEdge:
    def __init__(self, pk_signer, kid, n, v_max, fetch_fn=None, negative_ttl=1.0, tau_skew=5.0,
                 epoch_window=None):
        self.signer, self.kid, self.n, self.v_max = pk_signer, kid, n, v_max
        self.fetch_fn = fetch_fn
        self.neg_ttl = negative_ttl
        self.tau = tau_skew
        self.epoch_window = epoch_window  # optional callable(epoch, now) -> bool
        self.roots = {}      # (kid, e) -> (root, N, t_start_s, delta_s)
        self.neg = {}        # (kid, e) -> negative-cache expiry
        self.revoked = set()
        self.stats = dict(fetches=0, sig_verifs=0, neg_hits=0)

    # ------------------------------------------------------------ root installation
    def install_root(self, sr: SignedRoot) -> bool:
        if sr.kid != self.kid:
            return False
        self.stats["sig_verifs"] += 1
        if not self.signer.verify(sr.msg(), sr.sig):
            return False
        self.roots[(sr.kid, sr.epoch)] = (sr.root, sr.N, sr.t_start_ms / 1000.0, sr.delta_ms / 1000.0)
        return True

    def install_bundle(self, pb: PeriodBundle) -> bool:
        if pb.kid != self.kid:
            return False
        self.stats["sig_verifs"] += 1
        if not self.signer.verify(pb.msg(), pb.sig):
            return False
        for sr in pb.roots():
            self.roots[(sr.kid, sr.epoch)] = (sr.root, sr.N, sr.t_start_ms / 1000.0, sr.delta_ms / 1000.0)
        return True

    def install_revocations(self, rd: RevocationDelta) -> bool:
        if rd.kid != self.kid or not self.signer.verify(rd.msg(), rd.sig):
            return False
        self.revoked.update(rd.items)
        return True

    def _install(self, obj):
        if isinstance(obj, SignedRoot):
            return self.install_root(obj)
        if isinstance(obj, PeriodBundle):
            return self.install_bundle(obj)
        return False

    # ------------------------------------------------------------ verify
    def verify(self, token_str, now, url, stapled: bytes = None):
        """Returns (ok, reason, needed_fetch)."""
        try:
            t = decode_ember(token_str)
        except Exception:
            return False, "malformed", False
        if t.kid != self.kid or t.n != self.n:
            return False, "unknown_kid", False
        c = t.claims
        if now > c.expires + self.tau:
            return False, "expired", False
        if not url_matches(c, url):
            return False, "url", False
        if (t.epoch, t.idx) in self.revoked:
            return False, "revoked", False
        key = (t.kid, t.epoch)
        ent = self.roots.get(key)
        fetched = False
        if ent is None:
            if stapled is not None:
                try:
                    sr = SignedRoot.from_bytes(stapled)
                except Exception:
                    return False, "bad_staple", False
                if sr.epoch != t.epoch or not self.install_root(sr):
                    return False, "bad_staple", False
            else:
                if self.neg.get(key, -1) >= now:
                    self.stats["neg_hits"] += 1
                    return False, "neg_cached", False
                if self.epoch_window is not None and not self.epoch_window(t.epoch, now):
                    return False, "epoch_window", False
                if self.fetch_fn is None:
                    return False, "no_root", False
                self.stats["fetches"] += 1
                fetched = True
                obj = self.fetch_fn(t.kid, t.epoch)
                if obj is None or not self._install(obj) or key not in self.roots:
                    self.neg[key] = now + self.neg_ttl
                    return False, "root_unavailable", True
            ent = self.roots[key]
        root, N, t_start, delta = ent
        if c.expires > t_start + delta + self.v_max + self.tau:
            return False, "validity_bound", fetched
        if t.idx >= N:
            return False, "idx_range", fetched
        x = leaf_hash(t.kid, t.epoch, t.idx, c.tenant, t.r, t.claims_enc, self.n)
        r = root_from_path(t.kid, t.epoch, t.idx, N, x, t.path, self.n)
        if r is None or not hmac.compare_digest(r, root):
            return False, "path", fetched
        return True, "ok", fetched
