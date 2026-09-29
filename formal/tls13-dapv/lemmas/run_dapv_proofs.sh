#!/bin/bash
# Proves the DAPV lemmas in the full TLS 1.3 model one at a time.
# Requires Tamarin 1.8.0 (1.10.0 crashes on the rev21 model: "shapeTerm ... not enough pairs").
# Budget per lemma: $TIMEOUT seconds, 12 GB heap (4-core, 15 GB machine).
export LANG=C.UTF-8 LC_ALL=C.UTF-8
TIMEOUT=${TIMEOUT:-2400}
TAM="tamarin-prover-1.8.0 +RTS -N4 -M12G -RTS"
run() { # file lemma heuristic
  local f=$1 l=$2 h=$3
  local out=results/${f%.spthy}__$l.txt
  mkdir -p results
  echo "== $f $l (heuristic $h)"
  local t0=$(date +%s)
  timeout $TIMEOUT $TAM $f --prove=$l --heuristic=$h > $out 2>&1
  local rc=$?
  echo "time $(( $(date +%s) - t0 )) s" >> $out
  grep -E "^  $l .*(verified|falsified|analysis incomplete)" $out || echo "  $l: no result (exit $rc: $( [ $rc = 124 ] && echo timeout || echo error/out-of-memory ))"
  grep -E "^time" $out
}
run dapv.spthy dapv_ticket_only_after_promotion S
run dapv_naive.spthy dapv_ticket_only_after_promotion S
run dapv.spthy dapv_sigP_origin S
run dapv.spthy dapv_promotion_needs_pq_key S
run dapv.spthy dapv_reach_promotion S
run dapv.spthy dapv_provisional_impersonation_exists S
run dapv_naive.spthy dapv_resumption_with_unissued_ticket S
