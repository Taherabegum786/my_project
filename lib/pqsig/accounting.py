"""Byte and frame accounting for authentication modes (single-object fit; loss and latency are measured in lib/pqsig/proto).

Notation: S = declared signature bytes (liboqs OQS_SIG length_signature), P = public-key bytes,
B = profile auth_budget (bytes per message), h = fragment header per message (TODO-RESULT -> 0, flagged),
F1/Fn = payload of the first / later frames of a message, Tm = message period, Tf = frame period.
 frames(x)   = 1 if x <= F1 else 1 + ceil((x - F1)/Fn)         frames needed for x bytes in ONE message
 msgs(x)     = ceil(x / (B - h))                               messages needed when x bytes are spread over messages
 ttfa(x)     = (msgs-1)*Tm + (frames_in_last_message - 1)*Tf   from first fragment to last, no loss, no join wait, no processing
margin = B - x (negative = does not fit, bytes over budget).
Modes (auth object x; `fits` means x <= B, i.e. msgs = 1):
  full            x = S
  full_cert_pq    certificate with an explicit PQ issuer (issuer scheme = subject scheme): cert = P + metadata + S_issuer.
                  steady x = S + digest bytes; peak x = S + P + metadata + S (message signature + certificate); metadata is
                  TODO-RESULT (0 used = lower bound; fit also reported at the two derived sensitivity values). Only for
                  profiles whose source sends a certificate (peak_extra pk+fixed).
  full_cert_cl    the source's classical-issuer case (abrar2026deployment): cert = P + 105 B (metadata + classical issuer
                  signature, derived from the Falcon-512 certificate). Separately labelled; only where the source states it.
  full_cert_pk    bare public key delivered with the signature (peak_extra pk: Remote ID endorsement, DNSKEY): x = S + P
  chain           steady x = tag + key (per message); anchor = S + commit + ts, spread over msgs(anchor) messages;
                  join time = ttfa(anchor) + d*Tm.  `fits` is NOT a meaningful column (the 32 B steady cost always fits): the
                  chain is judged by join time against a deadline (summary.md), not by a fit count.
  hybrid          x = S_partner + S   (partner = the classical scheme the profile's source uses)
  key_delivery    (role public-key-space profiles only) x = P against the key space (OSNMA DSM-PKR); no signature is scored there.
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
    role = prof.get("role", "signature")
    hv = prof["fragment_header_bytes"]
    h = _num(hv)
    f1, fn = prof["frames"]["first_payload_bytes"], prof["frames"]["next_payload_bytes"]
    Tm, Tf = prof["message_period_s"], prof["frame_period_s"]
    c = common["chain"]
    cm = common.get("cert", {})
    meta = _num(cm.get("metadata_bytes"))
    ch = prof["cert_handling"]
    out = {"peak_bytes": None, "anchor_bytes": None, "anchor_msgs": None, "fits_meta41": None, "fits_meta73": None}
    if role == "public-key-space":
        if mode != "key_delivery":
            raise ValueError("public-key-space profile is scored for key_delivery only")
        x = P; pk = x
    elif mode == "key_delivery":
        raise ValueError("key_delivery only on public-key-space profiles")
    elif mode == "full":
        x = S; pk = x
    elif mode in ("full_cert_pq", "full_cert_cl", "full_cert_pk"):
        pe = ch["peak_extra"]
        x = S + ch["steady_extra_bytes"]
        n = ch["peak_every_n"]
        if mode == "full_cert_pq":
            if pe != "pk+fixed":
                raise ValueError("no certificate in this profile")
            pk = S + P + meta + S
            for mm in (41, 73):
                out[f"fits_meta{mm}"] = (S + P + mm + S) <= B and x <= B
        elif mode == "full_cert_cl":
            if pe != "pk+fixed":
                raise ValueError("no classical-issuer data point in this profile")
            pk = S + P + ch["peak_fixed_bytes"]
        else:
            if pe != "pk":
                raise ValueError("no bare-key delivery in this profile")
            pk = S + P
        out["peak_bytes"] = pk
        out["avg_bytes"] = ((n - 1) * x + pk) / n if isinstance(n, (int, float)) else x
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
    fits = (x <= B) and (pk <= B if mode.startswith("full_cert") else True)
    if mode == "chain":
        fits = x <= B
    out.update(auth_bytes=x, share=x / B, fits=fits, margin_bytes=B - (x if mode == "chain" else worst),
               frames_per_msg=frames(min(worst, B), f1, fn),
               msgs_needed=msgs(worst, B, h),
               ttfa_s=ttfa(worst, B, h, f1, fn, Tm, Tf) + (common["chain_key_delay_messages"] * Tm if mode == "chain" and isinstance(Tm, (int, float)) else 0),
               hdr_known=isinstance(hv, (int, float)))
    return out
