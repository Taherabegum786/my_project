#!/usr/bin/env bash
# Feasibility probe: real TLS 1.3 handshakes with OpenSSL 3.5.4 (native ML-KEM /
# ML-DSA / SLH-DSA, no oqsprovider). For each leaf algorithm: build a 2-level
# chain (root -> leaf, same algorithm), start s_server pinned to CPU 0, run
# s_time (new handshakes, no resumption) pinned to CPU 1 over loopback for
# $SECS seconds, and record the negotiated group/sigalg and handshakes/s.
# Usage: tls_probe.sh OSSL_PREFIX OUT.csv [SECS]
set -euo pipefail
O=$1; OUT=$2; SECS=${3:-5}
export LD_LIBRARY_PATH=$O/lib OPENSSL_CONF=$O/ssl/openssl.cnf
OSSL=$O/bin/openssl
W=$(mktemp -d); trap 'pkill -f "s_server -accept 1544" || true; rm -rf "$W"' EXIT
echo "leaf_alg,group,negotiated_group,negotiated_sigalg,chain_bytes,handshakes,user_cpu_s,conn_per_user_s,conn_per_wall_s" > "$OUT"
port=15440
# NOTE: SLH-DSA/Falcon certs are rejected by OpenSSL 3.5 TLS ("unknown certificate type";
# TLS sigalgs are only mldsa44/65/87) -> use the oqs-ossl3 docker image for those.
for alg in EC:P-256 ED25519 ML-DSA-44 ML-DSA-65 ML-DSA-87; do
  for grp in X25519 X25519MLKEM768; do
    port=$((port+1)); d=$W/$alg-$grp; mkdir -p "$d"
    if [[ $alg == EC:* ]]; then ka=(-newkey ec -pkeyopt ec_paramgen_curve:${alg#EC:}); else ka=(-newkey "$alg"); fi
    $OSSL req -x509 "${ka[@]}" -keyout "$d/ca.key" -out "$d/ca.crt" -nodes -subj /CN=root -days 3 2>/dev/null
    $OSSL req "${ka[@]}" -keyout "$d/l.key" -out "$d/l.csr" -nodes -subj /CN=localhost 2>/dev/null
    $OSSL x509 -req -in "$d/l.csr" -CA "$d/ca.crt" -CAkey "$d/ca.key" -out "$d/l.crt" -days 3 2>/dev/null
    chain=$(( $($OSSL x509 -in "$d/l.crt" -outform DER | wc -c) + $($OSSL x509 -in "$d/ca.crt" -outform DER | wc -c) ))
    taskset -c 0 $OSSL s_server -accept $port -cert "$d/l.crt" -key "$d/l.key" -cert_chain "$d/ca.crt" \
      -tls1_3 -groups $grp -www -quiet >/dev/null 2>&1 &
    sleep 0.5
    info=$(echo Q | timeout 10 $OSSL s_client -connect 127.0.0.1:$port -CAfile "$d/ca.crt" -groups $grp -tls1_3 -brief 2>&1 || true)
    g=$(echo "$info" | sed -n 's/.*Negotiated TLS1.3 group: //p'); s=$(echo "$info" | sed -n 's/.*Signature type: //p')
    st=$(taskset -c 1 timeout $((SECS+20)) $OSSL s_time -connect 127.0.0.1:$port -new -time $SECS -CAfile "$d/ca.crt" 2>&1 | grep -m1 "connections in" || true)
    # e.g. "1234 connections in 2.30s; 536.52 connections/user sec, bytes read 0"
    n=$(echo "$st" | awk '{print $1}'); u=$(echo "$st" | awk '{print $4}' | tr -d 's;'); r=$(echo "$st" | awk '{print $5}')
    echo "$alg,$grp,${g:-?},${s:-?},$chain,${n:-0},$u,$r,$(python3 -c "print(round(${n:-0}/$SECS,1))")" >> "$OUT"
    pkill -f "s_server -accept $port" || true
  done
done
cat "$OUT"
