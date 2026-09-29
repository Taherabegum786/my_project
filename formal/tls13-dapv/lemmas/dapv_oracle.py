#!/usr/bin/env python3
"""Proof oracle for the DAPV lemmas in the full TLS 1.3 model.

Tamarin (--heuristic=o --oraclename=dapv_oracle.py) calls this script with
the lemma name as argument and the list of open goals on stdin, one per
line as "<index>: <goal>".  We print goal indices in the order in which
they should be solved.  Goals matching an earlier pattern in the lemma's
priority list are solved first; the rest keep Tamarin's own order, except
that goals matching the lemma's 'last' patterns are postponed.

The rankings encode the intended proof idea of each lemma:
  * dapv_ticket_only_after_promotion: resolve where !DAPV_Full(tid) came
    from (promotion, or PSK mode, which the one_of axioms exclude for a
    session that was provisional).
  * dapv_sigP_origin / dapv_promotion_needs_pq_key: resolve the origin of
    the PQ signature (adversary with the PQ key, or the server's
    UseLtkP) before exploring the state machine.
  * exists-trace lemmas: follow the honest message flow (state facts and
    the in_out channel) before adversary knowledge.
"""
import re
import sys

STATE_MACHINE = [r"State_", r"MessageIn", r"MessageOut"]
ADV_BLOWUP = [r"KU\( h\(", r"KU\( Expand\(", r"KU\( Extract\(", r"KU\( hmac\(",
              r"splitEqs", r"'g'\^"]

RANK = {
    "dapv_ticket_full_origin": {
        "first": [r"!DAPV_Full", r"DAPV_PSKMode", r"DAPV_Pending"],
        "last": STATE_MACHINE + ADV_BLOWUP,
    },
    "dapv_pskfull_excludes_provisional": {
        "first": [r"DAPV_PSKMode", r"C2d_PSK", r"C2d\(", r"State_C2d"],
        "last": ADV_BLOWUP,
    },
    "dapv_ticket_only_after_promotion": {
        "first": [r"!DAPV_Full", r"DAPV_Promoted", r"C2d_PSK", r"C2d\(", r"DAPV_Pending"],
        "last": STATE_MACHINE + ADV_BLOWUP,
    },
    "dapv_sigP_origin": {
        "first": [r"!LtkP", r"UseLtkP", r"KU\( ~ltk", r"KU\( sign\(", r"!KD\( sign\(",
                  r"senc\(", r"RevLtkP"],
        "last": STATE_MACHINE + ADV_BLOWUP,
    },
    "dapv_promotion_needs_pq_key": {
        "first": [r"DAPV_Pending", r"!PkP", r"!LtkP", r"UseLtkP", r"DAPV_ServerSigned",
                  r"KU\( ~ltk", r"KU\( sign\(", r"!KD\( sign\(", r"RevLtkP"],
        "last": STATE_MACHINE + ADV_BLOWUP,
    },
    "dapv_reach_promotion": {
        "first": [r"DAPV_", r"State_", r"MessageIn", r"!Ltk", r"!Pk", r"Fr\("],
        "last": [r"KU\( ~", r"RevLtk", r"RevDHExp"],
    },
    "dapv_provisional_impersonation_exists": {
        "first": [r"DAPV_", r"RevLtk\(", r"KU\( ~ltk", r"State_", r"MessageIn"],
        "last": [r"RevLtkP", r"RevDHExp"],
    },
    "dapv_resumption_with_unissued_ticket": {
        "first": [r"DAPV_", r"RevLtk\(", r"KU\( ~ltk", r"State_", r"MessageIn", r"!ClientPSK"],
        "last": [r"RevLtkP", r"RevDHExp", r"RevealPSK"],
    },
}


def main():
    lemma = sys.argv[1] if len(sys.argv) > 1 else ""
    goals = []
    for line in sys.stdin.read().splitlines():
        m = re.match(r"^\s*(\d+):\s*(.*)$", line)
        if m:
            goals.append((int(m.group(1)), m.group(2)))
    rank = next((v for k, v in RANK.items() if lemma.startswith(k)), None)
    if rank is None:
        return  # no output: Tamarin falls back to its default ranking

    def key(g):
        idx, text = g
        for i, pat in enumerate(rank["first"]):
            if re.search(pat, text):
                return (0, i, idx)
        for pat in rank["last"]:
            if re.search(pat, text):
                return (2, 0, idx)
        return (1, 0, idx)

    for idx, _ in sorted(goals, key=key):
        print(idx)


if __name__ == "__main__":
    main()
