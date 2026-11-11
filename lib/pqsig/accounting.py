"""Byte accounting for authentication modes. All sizes in bytes.

Inputs per scheme: pk, sig (sig_bytes_max from the benchmark CSV). Classical hybrid partner
is chosen by the caller (sig_c). Chain parameters are explicit assumptions (CHAIN_DEFAULTS).

Modes (formulas, also printed in summary.md):
  full         auth = sig
  sig_cert     auth = sig + cert, cert = pk + sig   (subject key + same-scheme issuer signature)
  fragmented   auth = sig + hdr * frames, frames = ceil(sig / (frame - hdr)); sent over `frames` frames
  chain        steady = tag + key (per message); anchor = sig + commit + ts (once per epoch);
               fits iff steady <= budget and anchor <= budget; frames = 1 if so, else frames of anchor
  hybrid       auth = sig_c + sig_pq  (concatenated, both verified)
share_of_budget = auth / budget. frames = ceil(auth / frame_payload).
"""
import math

CHAIN_DEFAULTS = {"tag": 16, "key": 16, "commit": 16, "ts": 4}  # tag 16 B from darzi2026a; others assumed


def frames(nbytes, frame, hdr=0):
    return max(1, math.ceil(nbytes / (frame - hdr)))


def score(mode, sig, pk, sig_c, budget, frame, hdr=0, chain=None):
    """Return dict(auth_bytes, anchor_bytes, share, frames, fits)."""
    c = {**CHAIN_DEFAULTS, **(chain or {})}
    anchor = None
    if mode == "full":
        auth = sig
    elif mode == "sig_cert":
        auth = sig + pk + sig
    elif mode == "fragmented":
        f = frames(sig, frame, hdr)
        auth = sig + hdr * f
    elif mode == "chain":
        auth = c["tag"] + c["key"]
        anchor = sig + c["commit"] + c["ts"]
    elif mode == "hybrid":
        auth = sig_c + sig
    else:
        raise ValueError(mode)
    if mode == "chain":
        nf = max(1, frames(auth, frame, hdr)), frames(anchor, frame, hdr)
        fr = max(nf)
        fits = auth <= budget and anchor <= budget
    elif mode == "fragmented":
        fr = frames(sig, frame, hdr)
        fits = auth <= budget      # total bytes in the budget; frames reported separately
    else:
        fr = frames(auth, frame, hdr)
        fits = auth <= budget
    return {"auth_bytes": auth, "anchor_bytes": anchor, "share": auth / budget, "frames": fr, "fits": fits}
