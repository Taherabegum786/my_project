"""Byte and frame accounting for authentication modes (single-object fit; loss is in lossform.py).

Notation: S = declared signature bytes (liboqs OQS_SIG length_signature), P = public-key bytes,
B = profile auth_budget (bytes per message), h = fragment header per message (TODO-RESULT -> 0, flagged),
F1/Fn = payload of the first / later frames of a message, Tm = message period, Tf = frame period.
 frames(x)   = 1 if x <= F1 else 1 + ceil((x - F1)/Fn)         frames needed for x bytes in ONE message
 msgs(x)     = ceil(x / (B - h))                               messages needed when x bytes are spread over messages
 ttfa(x)     = (msgs-1)*Tm + (frames_in_last_message - 1)*Tf   from first fragment to last, no loss, no join wait, no processing
Modes (auth object x; `fits` means x <= B, i.e. msgs = 1):
  full       x = S
  full_cert  the certificate handling the profile's source uses:
             steady x = S + digest bytes (profile cert_handling.steady_extra_bytes)
             peak   x = S + P              (peak_extra = pk)       or S + P + f (pk+fixed: full certificate = subject key
                        + f bytes of metadata and issuer signature; f = 105 B from abrar2026deployment, Falcon-512
                        certificate 1,002 B minus 897 B key, derived, one data point applied to every scheme)
             average = ((n-1)*steady + peak)/n, n = peak_every_n; fits needs steady and peak <= B; ttfa (cold start) uses peak
  chain      steady x = tag + key (per message); anchor = S + commit + ts, spread over msgs(anchor) messages,
             each counted; join time = ttfa(anchor) + d*Tm; fits = steady <= B (anchor is fragmented, cost reported)
  hybrid     x = S_partner + S   (partner = the classical scheme the profile's source uses)
A mode with x > B is not a single-message fit; its cost is the message count and ttfa columns.
share_of_budget = x / B.
"""
import math


def frames(x, f1, fn):
    if x <= f1:
        return 1
    return 1 + math.ceil((x - f1) / fn - 1e-9)


def msgs(x, B, h):
    return max(1, math.ceil(x / (B - h) - 1e-9))


def ttfa(x, B, h, f1, fn, Tm, Tf):
    if not isinstance(Tm, (int, float)):
        return float("nan")
    m = msgs(x, B, h)
    last = x - (m - 1) * (B - h) if m > 1 else x
    return (m - 1) * Tm + (frames(min(last, B), f1, fn) - 1) * Tf


def _num(v, default=0.0):
    return v if isinstance(v, (int, float)) else default


def score(mode, S, P, prof, common):
    B = prof["auth_budget"]["bytes"]
    hv = prof["fragment_header_bytes"]
    h = _num(hv)
    f1, fn = prof["frames"]["first_payload_bytes"], prof["frames"]["next_payload_bytes"]
    Tm, Tf = prof["message_period_s"], prof["frame_period_s"]
    c = common["chain"]
    out = {"peak_bytes": None, "anchor_bytes": None, "anchor_msgs": None}
    if mode == "full":
        x = S; pk = x
    elif mode == "full_cert":
        ch = prof["cert_handling"]
        x = S + ch["steady_extra_bytes"]
        pe = ch["peak_extra"]
        pk = S + (P if pe == "pk" else P + ch["peak_fixed_bytes"] if pe == "pk+fixed" else ch["steady_extra_bytes"])
        n = ch["peak_every_n"]
        out["peak_bytes"] = pk
        out["avg_bytes"] = ((n - 1) * x + pk) / n if isinstance(n, (int, float)) and pe != "none" else x
    elif mode == "chain":
        x = c["tag"] + c["key"]
        a = S + c["commit"] + c["ts"]
        out["anchor_bytes"] = a; out["anchor_msgs"] = msgs(a, B, h)
        pk = a
    elif mode == "hybrid":
        x = prof["hybrid_partner"]["sig_bytes"] + S; pk = x
    else:
        raise ValueError(mode)
    worst = max(x, pk)
    fits = (x <= B) and (pk <= B if mode in ("full_cert",) else True)
    if mode == "chain":
        fits = x <= B
    out.update(auth_bytes=x, share=x / B, fits=fits,
               frames_per_msg=frames(min(worst, B), f1, fn),
               msgs_needed=msgs(worst, B, h),
               ttfa_s=ttfa(worst, B, h, f1, fn, Tm, Tf) + (common["chain_key_delay_messages"] * Tm if mode == "chain" and isinstance(Tm, (int, float)) else 0),
               hdr_known=isinstance(hv, (int, float)))
    return out
