#!/usr/bin/env bash
# E1n: PRIMARY native timings (OpenSSL 3.5.4, scratchpad build). 5 fresh-process runs per point, pinned core.
# usage: bash bench/native/run_native.sh <results_dir>     (QUICK=1 for a smoke run)
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
OUT=$(cd "${1:-$HERE/../../../results}" && pwd)
SP=${SP:-/tmp/claude-0/-home-user-my-project/4a27d5c9-46a1-5d35-98ec-9a4e85dfb968/scratchpad}
export LD_LIBRARY_PATH=$SP/opt/ossl35/lib OPENSSL_CONF=$SP/opt/ossl35/ssl/openssl.cnf
CORE=${CORE:-2}
RUNS=${RUNS:-5}
Q=${QUICK:-0}
make -C "$HERE" -s
B=$HERE/build
mkdir -p "$OUT/raw"
envlog() {
  { echo "## $1 $(date -Is)"; grep -E '^cpu ' /proc/stat; cat /sys/devices/system/cpu/cpu$CORE/cpufreq/scaling_governor 2>/dev/null || echo "governor: n/a"; } >> "$OUT/env_native_runs.txt"
}
ONLY=${ONLY:-all}
issuer() {
  IC=$OUT/native_issuer.csv
  echo "root_alg,N,n,reps,t_leaf_us,t_tree_us,t_sign_us,t_encode_us,t_epoch_us,tokens_per_s,run,impl" > "$IC"
  for alg in ML-DSA-44 ML-DSA-65 SLH-DSA-SHA2-128s SLH-DSA-SHA2-128f ED25519; do
    for N in 1 4 16 64 256 1024 4096 16384 65536 262144; do
      reps=5; [ "$alg" = SLH-DSA-SHA2-128s ] && reps=1; [ "$Q" = 1 ] && reps=1
      for r in $(seq 1 "$RUNS"); do
        taskset -c "$CORE" "$B/issuerbench" "$alg" "$N" "$reps" 16 | sed "s/\$/,$r,openssl-3.5.4-native/" >> "$IC"
      done
    done
    echo "issuer done $alg" >&2
  done
  for N in 256 16384; do for r in $(seq 1 "$RUNS"); do
    taskset -c "$CORE" "$B/issuerbench" ML-DSA-44 "$N" 5 32 | sed "s/\$/,$r,openssl-3.5.4-native/" >> "$IC"; done; done
}
pathverify() {
  PV=$OUT/native_pathverify.csv
  echo "impl,op,d,n,iters,ns_per_op_median,ns_per_op_p99,run" > "$PV"
  IT=200000; [ "$Q" = 1 ] && IT=20000
  for impl in evp ll; do
    for r in $(seq 1 "$RUNS"); do
      taskset -c "$CORE" "$B/pathverify" "$IT" 1000 "$impl" | tail -n +2 | sed "s/\$/,$r/" >> "$PV"
    done
  done
}
if [ "$ONLY" = pathverify ]; then pathverify; "${PY:-$SP/venv/bin/python}" "$HERE/aggregate_native.py" "$OUT"; exit 0; fi
if [ "$ONLY" = issuer ]; then issuer; "${PY:-$SP/venv/bin/python}" "$HERE/aggregate_native.py" "$OUT"; exit 0; fi
CSV=$OUT/native_sig.csv
echo "scheme,op,impl,run,n_iter,median_us,p99_us,mean_us,sig_bytes,pk_bytes" > "$CSV"
# scheme op iters
POINTS="
ML-DSA-44 keygen 2000
ML-DSA-44 sign 2000
ML-DSA-44 verify 2000
ML-DSA-65 keygen 2000
ML-DSA-65 sign 2000
ML-DSA-65 verify 2000
ML-DSA-87 keygen 2000
ML-DSA-87 sign 2000
ML-DSA-87 verify 2000
SLH-DSA-SHA2-128s keygen 20
SLH-DSA-SHA2-128s sign 10
SLH-DSA-SHA2-128s verify 2000
SLH-DSA-SHA2-128f keygen 2000
SLH-DSA-SHA2-128f sign 100
SLH-DSA-SHA2-128f verify 2000
ED25519 keygen 2000
ED25519 sign 2000
ED25519 verify 2000
ECDSA-P256 keygen 2000
ECDSA-P256 sign 2000
ECDSA-P256 verify 2000
RSA-2048 keygen 50
RSA-2048 sign 2000
RSA-2048 verify 2000
ML-KEM-768 keygen 2000
ML-KEM-768 encaps 2000
ML-KEM-768 decaps 2000
"
envlog "sig start"
while read -r s op n; do
  [ -z "$s" ] && continue
  [ "$Q" = 1 ] && n=$(( n > 50 ? 50 : n ))
  w=200; [ "$n" -le 100 ] && w=2
  for r in $(seq 1 "$RUNS"); do
    line=$(taskset -c "$CORE" "$B/evp_sigbench" "$s" "$op" "$n" "$w" "$OUT/raw/native_${s}_${op}_r$r.bin")
    IFS=, read -r a b c med p99 mean sl pl <<< "$line"
    echo "$s,$op,openssl-3.5.4-native,$r,$c,$med,$p99,$mean,$sl,$pl" >> "$CSV"
  done
  echo "done $s $op" >&2
done <<< "$POINTS"
envlog "sig end"
pathverify
envlog "pathverify end"
issuer
envlog "issuer end"
"${PY:-$SP/venv/bin/python}" "$HERE/aggregate_native.py" "$OUT"
