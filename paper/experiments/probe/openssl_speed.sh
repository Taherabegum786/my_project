#!/usr/bin/env bash
# C-level PQC timings via `openssl speed` inside the openquantumsafe/oqs-ossl3
# image (OpenSSL 3.6.0 + oqsprovider 0.11.0 / liboqs). Covers Falcon (FN-DSA
# precursor), which neither pqcrypto nor stock OpenSSL 3.5 provides.
# Requires a running dockerd (start with: nohup dockerd >dockerd.log 2>&1 &).
# Container pinned to one core. Output: raw text + parsed CSV (us per op).
# Usage: openssl_speed.sh OUT_PREFIX [seconds]
set -euo pipefail
OUT=${1:-openssl_speed}
SECS=${2:-2}
IMG=openquantumsafe/oqs-ossl3:latest
HERE=$(cd "$(dirname "$0")" && pwd)
docker run --rm --cpuset-cpus=1 "$IMG" sh -c "
  openssl speed -seconds $SECS -kem-algorithms ML-KEM-512 ML-KEM-768 ML-KEM-1024 X25519MLKEM768 X25519 2>/dev/null | sed -n '/keygen/,\$p'
  openssl speed -seconds $SECS -signature-algorithms ML-DSA-44 ML-DSA-65 ML-DSA-87 falcon512 falcon1024 falconpadded512 SLH-DSA-SHA2-128f SLH-DSA-SHA2-128s SLH-DSA-SHAKE-128f SLH-DSA-SHA2-192f SLH-DSA-SHA2-256f 2>/dev/null | sed -n '/keygen/,\$p'
" > "${OUT}_raw.txt"
python3 "$HERE/parse_openssl_speed.py" "${OUT}_raw.txt" "${OUT}.csv"
