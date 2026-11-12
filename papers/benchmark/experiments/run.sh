#!/usr/bin/env bash
# Reproduce everything for paper "benchmark" from a clean Ubuntu install.
# Usage: MACHINE_NAME=<your-machine> [ITER=10000] ./run.sh
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../.." && pwd)"
RAW="$HERE/../results/raw"; mkdir -p "$RAW"
: "${MACHINE_NAME:?set MACHINE_NAME to the machine name, e.g. laptop-x86}"
export MACHINE_NAME
ITER="${ITER:-10000}"; ITER_SLOW="${ITER_SLOW:-$((ITER/10 > 10 ? ITER/10 : 10))}"  # slow schemes
LIBOQS_TAG="${LIBOQS_TAG:-0.16.0}"
WORK="${WORK:-$HERE/build}"; PREFIX="$WORK/prefix"

SUDO=""; [ "$(id -u)" -ne 0 ] && SUDO=sudo
$SUDO apt-get update
$SUDO apt-get install -y build-essential cmake ninja-build git libssl-dev python3 python3-venv python3-pip curl
mkdir -p "$WORK"; python3 -m venv "$WORK/venv"
# shellcheck disable=SC1091
. "$WORK/venv/bin/activate"
pip install numpy pandas pyyaml matplotlib tabulate cryptography

if [ ! -f "$PREFIX/lib/liboqs.a" ] && [ ! -f "$PREFIX/lib64/liboqs.a" ] && [ ! -f "$PREFIX/lib/liboqs.so" ]; then
  mkdir -p "$WORK"
  [ -d "$WORK/liboqs" ] || git clone --depth 1 --branch "$LIBOQS_TAG" https://github.com/open-quantum-safe/liboqs "$WORK/liboqs"
  # Extra signature families (cmake ignores options a tag does not know).
  cmake -S "$WORK/liboqs" -B "$WORK/liboqs/build" -GNinja -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX="$PREFIX" -DOQS_BUILD_ONLY_LIB=ON -DOQS_DIST_BUILD=OFF \
    -DOQS_ENABLE_SIG_MAYO=ON -DOQS_ENABLE_SIG_UOV=ON -DOQS_ENABLE_SIG_SNOVA=ON -DOQS_ENABLE_SIG_CROSS=ON
  cmake --build "$WORK/liboqs/build" && cmake --install "$WORK/liboqs/build"
fi
git -C "$WORK/liboqs" rev-parse HEAD > "$WORK/liboqs_commit.txt"

cc -O2 -I"$PREFIX/include" "$ROOT/lib/pqsig/oqs_bench.c" -L"$PREFIX/lib" -L"$PREFIX/lib64" -loqs -lm -lcrypto -lpthread -o "$WORK/oqs_bench"
export LD_LIBRARY_PATH="$PREFIX/lib:$PREFIX/lib64:${LD_LIBRARY_PATH:-}"
COMMIT="$(git -C "$ROOT" rev-parse --short HEAD)"; DATE="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
OUT="$RAW/oqs_timing_${MACHINE_NAME}.csv"
"$WORK/oqs_bench" --header > "$OUT"
for A in $("$WORK/oqs_bench" --list); do
  N="$ITER"; case "$A" in *SLH*|*SPHINCS*|*cross*|*MQOM*|*mqom*) N="$ITER_SLOW";; esac
  "$WORK/oqs_bench" "$N" "$MACHINE_NAME" "$DATE" "$COMMIT" "$A" >> "$OUT"
done
CL="$RAW/classical_timing_${MACHINE_NAME}.csv"; rm -f "$CL"
python3 "$ROOT/lib/pqsig/classical_bench.py" "$CL" "$ITER"

# Part B: declared sizes (OQS_SIG length_*) + observed, then scoring on the declared length. Part C: closed forms + simulation.
python3 "$HERE/make_sizes.py" "$WORK/oqs_bench" "$OUT" "$CL" "$RAW/sizes_declared.csv"
python3 "$HERE/score.py" "$RAW/sizes_declared.csv" "$HERE/profiles.yaml" "$RAW/scoring_all_levels.csv"
python3 "$HERE/run_loss.py" "$RAW/sizes_declared.csv" "$HERE/profiles.yaml" "$RAW" 20 4000
python3 "$HERE/summarize.py"
echo "done: $HERE/../results/summary.md"
