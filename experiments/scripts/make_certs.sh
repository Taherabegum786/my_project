#!/bin/bash
# Generates, for each algorithm, (a) a 3-certificate chain root -> intermediate
# -> leaf (the server sends leaf + intermediate; the root is the client's trust
# anchor) and (b) a single self-signed leaf trusted directly (as in the
# original prototype).  All certificates in a chain use the same algorithm.
set -euo pipefail
OSSL=${OSSL:-/opt/ossl}
export LD_LIBRARY_PATH=$OSSL/lib:/opt/liboqs/lib
O="$OSSL/bin/openssl"
P="-provider oqsprovider -provider default"
OUT=${1:-certs}
mkdir -p "$OUT"
cd "$OUT"

newkey() { # alg -> args for req -newkey
  case $1 in
    p256) echo "-newkey ec -pkeyopt ec_paramgen_curve:P-256" ;;
    *)    echo "-newkey $1" ;;
  esac
}

for alg in ${ALGS:-p256 p256_mldsa44 p256_falcon512 p384_mldsa65 p256_sphincssha2128fsimple}; do
  d=$alg; mkdir -p $d
  # Root CA
  $O req $P -x509 -new $(newkey $alg) -nodes -keyout $d/root.key -out $d/root.pem \
     -days 365 -subj "/CN=DAPV Test Root $alg" \
     -addext "basicConstraints=critical,CA:TRUE" -addext "keyUsage=critical,keyCertSign,cRLSign" 2>/dev/null
  # Intermediate CA
  $O req $P -new $(newkey $alg) -nodes -keyout $d/int.key -out $d/int.csr \
     -subj "/CN=DAPV Test Intermediate $alg" 2>/dev/null
  printf "basicConstraints=critical,CA:TRUE,pathlen:0\nkeyUsage=critical,keyCertSign,cRLSign\n" > $d/int.ext
  $O x509 $P -req -in $d/int.csr -CA $d/root.pem -CAkey $d/root.key -CAcreateserial \
     -days 365 -extfile $d/int.ext -out $d/int.pem 2>/dev/null
  # Leaf
  $O req $P -new $(newkey $alg) -nodes -keyout $d/leaf.key -out $d/leaf.csr \
     -subj "/CN=server.test" 2>/dev/null
  printf "basicConstraints=CA:FALSE\nkeyUsage=critical,digitalSignature\nextendedKeyUsage=serverAuth\nsubjectAltName=DNS:server.test,IP:10.77.0.1\n" > $d/leaf.ext
  $O x509 $P -req -in $d/leaf.csr -CA $d/int.pem -CAkey $d/int.key -CAcreateserial \
     -days 365 -extfile $d/leaf.ext -out $d/leaf.pem 2>/dev/null
  cat $d/leaf.pem $d/int.pem > $d/chain.pem
  # Single self-signed leaf (chain length 1)
  $O req $P -x509 -new $(newkey $alg) -nodes -keyout $d/single.key -out $d/single.pem \
     -days 365 -subj "/CN=server.test" -addext "subjectAltName=DNS:server.test" 2>/dev/null
  $O verify $P -CAfile $d/root.pem -untrusted $d/int.pem $d/leaf.pem >/dev/null
  printf "%-16s leaf %5d B  intermediate %5d B  (DER)\n" $alg \
     $($O x509 $P -in $d/leaf.pem -outform DER 2>/dev/null | wc -c) \
     $($O x509 $P -in $d/int.pem -outform DER 2>/dev/null | wc -c)
done
