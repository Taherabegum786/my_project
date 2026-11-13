"""Attacker toolkit used by the negative tests and the active-attacker experiment.
Knowledge model: the attacker hears every frame (public), knows the formats, the schedule and the public key; it does NOT hold the sender's
PQ secret key or the chain secret; it learns a chain key only when the sender discloses it in a frame."""
import random
import struct

from . import modes as MO


def pollute(frame, fields, rng, kinds=("sym", "tag", "key", "path", "nc")):
    """Copy of a genuine frame (same application message, same headers and indices) whose payload fields are random bytes."""
    app, auth = frame
    b = bytearray(auth)
    for a, z, kind in fields:
        if kind in kinds:
            b[a:z] = rng.randbytes(z - a)
    return (app, bytes(b))


def flip(b, i, bit=1):
    return b[:i] + bytes([b[i] ^ bit]) + b[i + 1:]


def forge_after_disclosure(S, m, app_forged=None):
    """The classic TESLA attack on message m: the attacker takes the key K_m from the sender's chain (it is public once disclosed, in slot
    m + d) and returns a frame (forged app, forged tag) that claims slot m.  Non-chain modes: the genuine auth field with a modified app."""
    A = S.alloc; P = S.plan
    app, auth = S.frames[m]
    if app_forged is None:
        app_forged = flip(app, 20)
    if A.kind != "chain":
        return (app_forged, auth)
    e, i = m // P.E, m % P.E + 1
    nc = auth[S.fields[m][[k for _, _, k in S.fields[m]].index("nc")][0]:][:MO.COMMIT_B] if A.cont and any(k == "nc" for _, _, k in S.fields[m]) else b""
    tag_f = MO.mac_tag(S.chains[e][i], e, i, app_forged, nc)
    a0, a1, _ = next(f for f in S.fields[m] if f[2] == "tag")
    return (app_forged, auth[:a0] + tag_f + auth[a1:])


def legacy_key_forgery(S, m, build_seed):
    """Regression attack of the pass-3 review (forge_chain_seed.py): recompute the chain keys from the PUBLIC run seed with the old derivation
    and forge an in-time message.  Returns the forged frame for slot m (chain modes only)."""
    A = S.alloc; P = S.plan; E = P.E
    e, i = m // E, m % E + 1
    K = [None] * (E + 1)
    K[E] = MO.chain_seed_legacy(build_seed, e)
    for j in range(E, 0, -1):
        K[j - 1] = MO.Fchain(K[j])
    app, auth = S.frames[m]
    app_f = flip(app, 20)
    nc = b""
    if A.cont:
        f = next(f for f in S.fields[m] if f[2] == "nc"); nc = auth[f[0]:f[1]]
    tag_f = MO.mac_tag(K[i], e, i, app_f, nc)
    a0, a1, _ = next(f for f in S.fields[m] if f[2] == "tag")
    return (app_f, auth[:a0] + tag_f + auth[a1:])


# ---------------------------------------------------------------- field-level helpers for the negative tests
def frag_symbols(S, t):
    """[(age, idx, a0, a1)] of the symbols in the frag-mode auth field of slot t"""
    A = S.alloc; auth = S.frames[t][1]
    out = []
    if len(auth) < 3:
        return out
    o = 3
    for _ in range(auth[2]):
        out.append((auth[o], auth[o + 1], o + 2, o + 2 + A.s)); o += 2 + A.s
    return out


def replace_range(frame, a0, a1, data):
    app, auth = frame
    return (app, auth[:a0] + data + auth[a1:])


def anchor_symbols(S, t):
    """[(epoch16, idx, a0, a1)] of the anchor symbols in chain slot t"""
    A = S.alloc; auth = S.frames[t][1]
    if len(auth) < A.mand:
        return []
    o = 5 + MO.TAG_B + 3 + MO.KEY_B + (MO.COMMIT_B if A.cont else 0)
    ae, ns = struct.unpack(">HB", auth[o:o + 3]); o += 3
    out = []
    for _ in range(ns):
        out.append((ae, auth[o], o + 1, o + 1 + A.s)); o += 1 + A.s
    return out


def tamper_anchor_blob(S, epoch, edit):
    """Attacker decodes the (public) anchor of `epoch` from the frames, applies edit(blob) -> blob', re-encodes it with the public code and
    overwrites every anchor symbol of that epoch in the stream.  Returns the new frame list."""
    A = S.alloc; P = S.plan
    syms = {}
    for t in range(P.G):
        for ae, idx, a0, a1 in anchor_symbols(S, t):
            if ae == epoch & 0xFFFF:
                syms.setdefault(idx, S.frames[t][1][a0:a1])
    code = A.code(epoch)
    blob = code.decode(sorted(syms.items())[:code.k]) if code.coder == "mds" else code.decode(sorted(syms.items()))
    new = code.encode(edit(blob[:A.blob_len] + bytes(len(blob) - A.blob_len)))
    frames = list(S.frames)
    for t in range(P.G):
        for ae, idx, a0, a1 in anchor_symbols(S, t):
            if ae == epoch & 0xFFFF:
                frames[t] = replace_range(frames[t], a0, a1, new[idx])
    return frames


def anchor_field_edit(field):
    """edit functions for tamper_anchor_blob; blob = len(2) commit(16) e32(4) t_e0(6) sched(7) sig"""
    def f(blob):
        b = bytearray(blob)
        if field == "ts":
            o = 2 + MO.COMMIT_B + 4; v = int.from_bytes(b[o:o + MO.TS_B], "big") - 3_600_000; b[o:o + MO.TS_B] = v.to_bytes(MO.TS_B, "big")
        elif field == "d":
            o = 2 + MO.COMMIT_B + 4 + MO.TS_B + 3; b[o] = 14
        elif field == "E":
            o = 2 + MO.COMMIT_B + 4 + MO.TS_B + 2; b[o] ^= 0x01
        elif field == "epoch":
            o = 2 + MO.COMMIT_B + 3; b[o] ^= 0x01
        elif field == "commit":
            b[2] ^= 0x01
        return bytes(b)
    return f
