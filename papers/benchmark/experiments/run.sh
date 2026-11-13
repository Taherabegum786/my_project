#!/usr/bin/env bash
# Reproduce everything for paper "benchmark" from a clean Ubuntu 22.04/24.04 install, in one pass:
#   build (liboqs 0.16.0 + ctypes shim + C bench) -> timing (liboqs + OpenSSL classical, C) -> sizes -> stateful rows -> scoring
#   -> negative tests -> real-protocol sweep -> closed-form cross-check -> UDP loopback smoke -> summarize.
# Usage:  MACHINE_NAME=<your-machine> ./run.sh                 full run (see the printed estimate)
#         QUICK=1 ./run.sh                                      few-minute smoke run (fewer iterations/conditions, one M)
# Env:    ITER (default 10000; QUICK 200)  ITER_SLOW (default ITER/100 = 100; QUICK 10; used for SLH-DSA, CROSS, MQOM)  FULL_LIST=1 (benchmark every liboqs scheme)
#         WORK (build dir, reused if present)  SKIP_APT=1  PROCS (default nproc)  SEEDS (default 20)
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../.." && pwd)"
RAW="$HERE/../results/raw"; RES="$HERE/../results"; mkdir -p "$RAW"
QUICK="${QUICK:-0}"
if [ "$QUICK" = 1 ]; then : "${MACHINE_NAME:=quick-smoke}"; ITER="${ITER:-200}"; ITER_SLOW="${ITER_SLOW:-10}"; QARG="--quick"
else : "${MACHINE_NAME:?set MACHINE_NAME to the machine name, e.g. laptop-x86}"; ITER="${ITER:-10000}"; ITER_SLOW="${ITER_SLOW:-$((ITER/100 > 10 ? ITER/100 : 10))}"; QARG=""; fi
export MACHINE_NAME
LIBOQS_TAG="${LIBOQS_TAG:-0.16.0}"
WORK="${WORK:-$HERE/build}"; PREFIX="$WORK/prefix"; PROCS="${PROCS:-$(nproc)}"; SEEDS="${SEEDS:-20}"
SUDO=""; [ "$(id -u)" -ne 0 ] && SUDO=sudo
if [ "${SKIP_APT:-0}" != 1 ] && ! (command -v cmake && command -v ninja && command -v gcc && command -v git && [ -f /usr/include/openssl/evp.h ]) >/dev/null 2>&1; then
  $SUDO apt-get update
  $SUDO apt-get install -y build-essential cmake ninja-build git libssl-dev python3 python3-venv python3-pip curl
fi
# code state recorded in every CSV row (never hard-coded): full commit id and whether lib/ or experiments/ have uncommitted changes
read -r COMMIT DIRTY < <(python3 - <<PY
import sys; sys.path.insert(0, "$ROOT/lib")
from pqsig.common import code_state
c, d = code_state(); print(c, int(d))
PY
)
PHASES="$RAW/run_phases_${MACHINE_NAME}.csv"; echo "phase,seconds,quick,machine,git_commit,git_dirty" > "$PHASES"
T0=$SECONDS
phase_start() { PH="$1"; PT=$SECONDS; echo "== $1"; }
phase_end() { echo "$PH,$((SECONDS-PT)),$QUICK,$MACHINE_NAME,$COMMIT,$DIRTY" >> "$PHASES"; }

echo "machine=$MACHINE_NAME quick=$QUICK ITER=$ITER ITER_SLOW=$ITER_SLOW procs=$PROCS"

phase_start setup
mkdir -p "$WORK"
if [ ! -f "$WORK/venv/.deps_ok" ]; then
  python3 -m venv "$WORK/venv"
  # shellcheck disable=SC1091
  . "$WORK/venv/bin/activate"; pip install -q -r "$HERE/requirements.txt"; touch "$WORK/venv/.deps_ok"
else
  # shellcheck disable=SC1091
  . "$WORK/venv/bin/activate"
fi
phase_end

phase_start liboqs_build
LIBDIR="$PREFIX/lib"; [ -f "$PREFIX/lib64/liboqs.a" ] && LIBDIR="$PREFIX/lib64"
if [ ! -f "$LIBDIR/liboqs.a" ]; then
  [ -d "$WORK/liboqs" ] || git clone --depth 1 --branch "$LIBOQS_TAG" https://github.com/open-quantum-safe/liboqs "$WORK/liboqs"
  cmake -S "$WORK/liboqs" -B "$WORK/liboqs/build" -GNinja -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX="$PREFIX" -DOQS_BUILD_ONLY_LIB=ON -DOQS_DIST_BUILD=OFF \
    -DOQS_ENABLE_SIG_MAYO=ON -DOQS_ENABLE_SIG_UOV=ON -DOQS_ENABLE_SIG_SNOVA=ON -DOQS_ENABLE_SIG_CROSS=ON
  cmake --build "$WORK/liboqs/build" && cmake --install "$WORK/liboqs/build"
  LIBDIR="$PREFIX/lib"; [ -f "$PREFIX/lib64/liboqs.a" ] && LIBDIR="$PREFIX/lib64"
fi
git -C "$WORK/liboqs" rev-parse HEAD > "$WORK/liboqs_commit.txt" 2>/dev/null || echo unknown > "$WORK/liboqs_commit.txt"
# C benchmark (liboqs + OpenSSL classical) and the ctypes shim (liboqs.a linked whole into a shared object: same build, no second compile)
cc -O2 -I"$PREFIX/include" "$ROOT/lib/pqsig/oqs_bench.c" -L"$LIBDIR" -loqs -lm -lcrypto -lpthread -o "$WORK/oqs_bench"
cc -O2 -shared -fPIC "$ROOT/lib/pqsig/proto/pqshim.c" -I"$PREFIX/include" -Wl,--whole-archive "$LIBDIR/liboqs.a" -Wl,--no-whole-archive -lcrypto -lpthread -o "$WORK/libpqshim.so"
export PQSHIM_LIB="$WORK/libpqshim.so"
phase_end

echo "-- estimate of the full run (from a previous QUICK run on this machine, if any):"
python3 "$HERE/estimate_duration.py" "$RAW" "$MACHINE_NAME" || true

DATE="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "code commit $COMMIT dirty=$DIRTY"

phase_start timing
OUT="$RAW/oqs_timing_${MACHINE_NAME}.csv"; CL="$RAW/classical_timing_${MACHINE_NAME}.csv"
"$WORK/oqs_bench" --header > "$OUT"
LIST="--list"; [ "${FULL_LIST:-0}" = 1 ] && LIST="--list-all"
for A in $("$WORK/oqs_bench" $LIST); do
  N="$ITER"; case "$A" in *SLH*|*SPHINCS*|cross*|*MQOM*|mqom*) N="$ITER_SLOW";; esac
  "$WORK/oqs_bench" "$N" "$MACHINE_NAME" "$DATE" "$COMMIT" "$DIRTY" "$A" >> "$OUT"
done
"$WORK/oqs_bench" --header > "$CL"
"$WORK/oqs_bench" --classical "$ITER" "$MACHINE_NAME" "$DATE" "$COMMIT" "$DIRTY" >> "$CL"
phase_end

phase_start sizes_scoring
python3 "$HERE/make_sizes.py" "$WORK/oqs_bench" "$OUT" "$CL" "$RAW/sizes_declared.csv"
python3 "$HERE/add_stateful.py" "$RAW/sizes_declared.csv"
python3 "$HERE/score.py" "$RAW/sizes_declared.csv" "$HERE/profiles.yaml" "$RAW/scoring_all_levels.csv"
phase_end

phase_start negative_tests
python3 "$HERE/negative_tests.py" "$RAW/negative_tests_${MACHINE_NAME}.csv" $QARG
phase_end

phase_start protocol_sweep
python3 "$HERE/run_proto.py" sweep "$RAW" $QARG --procs "$PROCS" --seeds "$SEEDS" --machine "$MACHINE_NAME"
phase_end

phase_start crosscheck
python3 "$HERE/crosscheck_loss.py" "$RAW" "$MACHINE_NAME"
phase_end

phase_start udp_smoke
# two real processes over loopback; same seeded loss; compared with the in-process outcome (use two hosts: see udp_link.py)
UDPCSV="$RAW/udp_smoke_${MACHINE_NAME}.csv"; rm -f "$UDPCSV"; KF="$(mktemp -u)"; PORT=$((20000 + RANDOM % 20000))
for CFG in "ML-DSA-44 frag_mds iid:0.2 5" "MAYO-1 chain ge:0.2:5 7" "Falcon-padded-512 merkle8 iid:0.1 9" "ML-DSA-44 hyb_mds iid:0.1 11"; do
  set -- $CFG; rm -f "$KF"; PORT=$((PORT + 1))
  python3 "$HERE/run_proto.py" udp --role receiver --udp 127.0.0.1:$PORT --profile sib1 --pq "$1" --mode "$2" --M 10 --loss "$3" --seed "$4" \
      --keyfile "$KF" --out "$UDPCSV" --check --machine "$MACHINE_NAME" --timeout 60 > /dev/null &
  RXPID=$!
  python3 "$HERE/run_proto.py" udp --role sender --udp 127.0.0.1:$PORT --profile sib1 --pq "$1" --mode "$2" --M 10 --speed 400 --keyfile "$KF" --start-delay 2 --machine "$MACHINE_NAME" > /dev/null
  wait $RXPID
done
phase_end

phase_start summarize
python3 "$HERE/summarize.py"
phase_end

echo "total $((SECONDS-T0)) s"
if [ "$QUICK" = 1 ]; then
  echo "-- estimated duration of the FULL run on this machine ($PROCS cores):"
  python3 "$HERE/estimate_duration.py" "$RAW" "$MACHINE_NAME"
fi
echo "done: $RES/summary.md"
