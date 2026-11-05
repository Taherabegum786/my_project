#!/usr/bin/env bash
# Experimenter A pipeline (E1, E1n, E2/E2+, E3, E5, E7, figures, tables).  QUICK=1 for a smoke run.
# usage: bash run_all.sh [stage...]   stages: tests native bench sims figs   (default: all)
set -euo pipefail
cd "$(dirname "$0")"
SP=${SP:-/tmp/claude-0/-home-user-my-project/4a27d5c9-46a1-5d35-98ec-9a4e85dfb968/scratchpad}
PY=${PY:-$SP/venv/bin/python}
OUT=${OUT:-../results}
Q=${QUICK:-0}
QF=""; [ "$Q" = 1 ] && QF="--quick"
REPS=5; [ "$Q" = 1 ] && REPS=2
PROCS=${PROCS:-3}
# simulations are timing-insensitive: run them at idle priority so they never perturb timing benchmarks
IDLE="chrt -i 0 nice -n 19"
STAGES=${*:-tests native bench sims figs}
for s in $STAGES; do case $s in
  tests)  $PY -m pytest -q tests/ && $PY -m tests.gen_vectors ;;
  native) bash bench/native/run_native.sh "$OUT" ;;
  bench)  taskset -c 2 $PY -m bench.bench_primitives --out "$OUT" $QF
          taskset -c 2 $PY -m bench.bench_tokens --out "$OUT" $QF --procs ${ISSUER_PROCS:-4}
          $PY -m bench.fit_analysis --out "$OUT" ;;
  sims)   for e in validate sweep_delta controller dissem e2e sens; do
            $IDLE $PY -m sim.run_sim --exp $e --reps $REPS --out "$OUT" --procs $PROCS; done
          $IDLE $PY -m sim.dos --out "$OUT"
          [ -f "$OUT/proto_p3_config.json" ] && $PY -m sim.proto_mc "$OUT" 50 || echo "no E8 P3 config; skipping sim_proto_mc" ;;
  figs)   $PY -m plots.make_figures --in "$OUT" --out "$OUT/figures"
          $PY -m plots.make_tables --in "$OUT" --out "$OUT/tables" ;;
  *) echo "unknown stage $s"; exit 2 ;;
esac; done
