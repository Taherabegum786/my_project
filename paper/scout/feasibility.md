# Feasibility probe (Scout B) - what we can actually measure on this machine

Machine: 4 vCPU Intel Xeon @ 2.10 GHz (AVX2 + AVX-512F), 15 GB RAM, Linux 6.18, running as root with full
capabilities. Date of probe: 2026-11-05. All numbers below come from code in `paper/experiments/probe/` and
CSVs in `paper/results/` (single run each; treat as probe-quality, not paper-quality - re-run with
repetitions/CIs for the paper).

## 1. Working toolchain recipe (copy-paste)

```bash
SP=/tmp/claude-0/-home-user-my-project/4a27d5c9-46a1-5d35-98ec-9a4e85dfb968/scratchpad
V=$SP/venv
# (a) Python: pqcrypto 1.0.0 is preinstalled; add cryptography for X25519/ECDSA/Ed25519 baselines
$V/bin/pip install cryptography            # -> 50.0.2

# (b) Native OpenSSL 3.5.4 (ML-KEM, ML-DSA, SLH-DSA built in; TLS 1.3 with X25519MLKEM768 + ML-DSA certs)
mkdir -p $SP/src && cd $SP/src
curl -sSLO https://github.com/openssl/openssl/releases/download/openssl-3.5.4/openssl-3.5.4.tar.gz
tar xzf openssl-3.5.4.tar.gz && cd openssl-3.5.4
./Configure --prefix=$SP/opt/ossl35 --libdir=lib no-docs no-tests && make -j4 && make install_sw   # ~4 min
mkdir -p $SP/opt/ossl35/ssl && cp apps/openssl.cnf $SP/opt/ossl35/ssl/   # REQUIRED, else `req` fails silently
export LD_LIBRARY_PATH=$SP/opt/ossl35/lib OPENSSL_CONF=$SP/opt/ossl35/ssl/openssl.cnf

# (c) Docker: daemon is NOT running by default; start it (works, root + full caps)
nohup dockerd > $SP/src/dockerd.log 2>&1 &
docker pull openquantumsafe/oqs-ossl3:latest   # OpenSSL 3.6.0 + oqsprovider 0.11.0 (liboqs): Falcon, MAYO, composites, SPHINCS+ in TLS

# (d) Go 1.24.7 is at /usr/local/go/bin/go: stdlib crypto/mlkem + crypto/tls X25519MLKEM768 (default-on)

# (e) netns / veth / TAP / tc-tbf work; netem does NOT
apt-get install -y iproute2      # provides ip + tc (not preinstalled)
```

Probe scripts:
- `paper/experiments/probe/microbench.py` -> `paper/results/probe_microbench.csv` (Python, pqcrypto + cryptography)
- `paper/experiments/probe/openssl_speed.sh` (+ `parse_openssl_speed.py`) -> `paper/results/probe_openssl_speed.csv` (+ `_raw.txt`) (C-level, docker, 1 pinned core)
- `paper/experiments/probe/tls_probe.sh` -> `paper/results/probe_tls_handshakes.csv` (real TLS 1.3 handshakes, OpenSSL 3.5.4)
- `paper/experiments/probe/go_tls_probe/` (`go run . 2000`) -> `paper/results/probe_go.csv`

## 2. What works / what doesn't

| Item | Status | How |
|---|---|---|
| ML-KEM-512/768/1024 | WORKS | pqcrypto; OpenSSL 3.5.4/3.6 native; Go crypto/mlkem (768, 1024 only) |
| X25519MLKEM768 hybrid | WORKS | OpenSSL `-groups X25519MLKEM768` (TLS + speed); Go TLS; composed in Python |
| ML-DSA-44/65/87 | WORKS | pqcrypto; OpenSSL native (also as TLS certs: sigalgs mldsa44/65/87) |
| SLH-DSA (all 12 SHA2/SHAKE sets) | WORKS (primitive) | pqcrypto; OpenSSL native `speed`/`req` |
| SLH-DSA as TLS certificate | NOT in OpenSSL 3.5.4 (`unknown certificate type`) | WORKS in oqs-ossl3 docker as `sphincssha2128fsimple` (oqsprovider codepoint) |
| Falcon-512/1024 (FN-DSA precursor; FIPS 206 not final) | WORKS via docker only | oqs-ossl3 `falcon512`, `falcon1024`, `falconpadded512`; TLS certs too |
| Composite/hybrid certs (e.g. `p256_mldsa44`, `p256_falcon512`) | WORKS via docker | oqsprovider; TLS handshake verified with X25519MLKEM768 |
| MAYO, CROSS, BIKE, FrodoKEM, HQC-type extras | available in oqs docker | not benchmarked |
| Real TLS 1.3 handshake, PQ KEX + PQ certs | WORKS | native OpenSSL 3.5.4 `s_server`/`s_client`/`s_time`; Go TLS (KEX only, no ML-DSA certs in Go 1.24) |
| liboqs-python | NOT USABLE | pip has 0.16.0.x but it needs a liboqs shared lib; GitHub archive of `open-quantum-safe/liboqs` is blocked by the session proxy ("GitHub access to this repository is not enabled"); could be retried via `add_repo` or by copying from the docker image. Not needed: OpenSSL + docker cover everything. |
| Docker | WORKS after `dockerd &` | hub pulls work through proxy |
| network namespaces, veth, TAP (`/dev/net/tun`) | WORKS | `ip netns add`, `ip link add ... type veth`, `ip tuntap add mode tap` |
| `tc qdisc ... netem` | **NOT AVAILABLE** (`CONFIG_NET_SCH_NETEM` not set: "Specified qdisc kind is unknown") | delay/loss must be emulated in userspace (prior work's `tapbridge.c`) or simulated |
| `tc qdisc ... tbf` / htb (rate limiting) | WORKS | `tc qdisc add dev va root tbf rate 50mbit ...` |
| BBR / CUBIC | built in (`CONFIG_TCP_CONG_BBR=y`) | `fq` qdisc is NOT available (BBR without fq pacing falls back to internal pacing) |

Caveats: everything runs on one 4-vCPU VM (pin server/client/emulator to disjoint cores; state this honestly).
pqcrypto's ML-DSA *sign* (7.5 ms median for ML-DSA-44) is ~10x slower than OpenSSL's (0.67 ms) -
pqcrypto appears to be a portable (non-AVX2) build; **use OpenSSL numbers as the C-level reference** and pqcrypto
only for sizes / Python-driven simulation. OpenSSL's native ML-DSA is itself not the fastest AVX2 implementation
(the prior paper measured 37-59 us per ML-DSA/FN-DSA verification with liboqs 0.14 AVX2), so state the implementation used.

## 3. Measured numbers

### 3.1 C-level, `openssl speed` (OpenSSL 3.6.0 + oqsprovider 0.11.0, docker, 1 pinned core, 2 s per op)

| Algorithm | keygen (us) | encaps / sign (us) | decaps / verify (us) |
|---|---:|---:|---:|
| X25519 (as KEM) | 39.8 | 87.8 | 44.3 |
| ML-KEM-512 | 29.5 | 21.3 | 29.0 |
| ML-KEM-768 | 48.6 | 23.8 | 37.0 |
| ML-KEM-1024 | 69.3 | 32.7 | 49.5 |
| X25519MLKEM768 | 93.6 | 111.1 | 84.0 |
| ML-DSA-44 | 137.5 | 675.0 | 122.8 |
| ML-DSA-65 | 213.1 | 1054.1 | 201.6 |
| ML-DSA-87 | 302.2 | 1277.6 | 333.8 |
| Falcon-512 | 7418 | 330.1 | 44.1 |
| Falcon-padded-512 | 7587 | 391.2 | 50.5 |
| Falcon-1024 | 24814 | 613.4 | 83.9 |
| SLH-DSA-SHA2-128s | 71429 | ~555,556 (only ~4 ops in 2 s) | 518.2 |
| SLH-DSA-SHA2-128f | 1098 | 26110 | 1592.9 |
| SLH-DSA-SHA2-192f | 1599 | 44053 | 2388.9 |
| SLH-DSA-SHA2-256f | 4474 | 97087 | 2518.9 |
| SLH-DSA-SHAKE-128f | 2308 | 52632 | 3005.7 |

### 3.2 Sizes (bytes, from pqcrypto; match FIPS 203/204/205)

| Scheme | pk | sk | ct / sig |
|---|---:|---:|---:|
| ML-KEM-512 / 768 / 1024 | 800 / 1184 / 1568 | 1632 / 2400 / 3168 | ct 768 / 1088 / 1568 |
| X25519MLKEM768 key shares | client 1216 | - | server 1120 |
| ML-DSA-44 / 65 / 87 | 1312 / 1952 / 2592 | 2560 / 4032 / 4896 | sig 2420 / 3309 / 4627 |
| SLH-DSA-128s / 128f | 32 | 64 | sig 7856 / 17088 |
| SLH-DSA-192s / 192f | 48 | 96 | sig 16224 / 35664 |
| SLH-DSA-256s / 256f | 64 | 128 | sig 29792 / 49856 |
| ECDSA-P256 / Ed25519 | 65 / 32 | 32 / 32 | sig ~71 (DER) / 64 |

Full per-op medians/means/p95 for all 12 SLH-DSA sets, ML-KEM, ML-DSA, X25519, ECDSA, Ed25519 (Python call overhead
included, n = 2000 for fast ops, 3-200 for SLH-DSA) are in `results/probe_microbench.csv`. Examples (median us):
ML-KEM-768 keygen/encaps/decaps 66.3/76.6/95.7; X25519MLKEM768 client-keygen/server-encaps/client-decaps
104.5/161.4/138.3; ML-DSA-44 verify 133.9; ECDSA-P256 sign/verify 28.3/84.0; SLH-DSA-SHA2-128s sign 306,343.

### 3.3 Real TLS 1.3 handshakes (OpenSSL 3.5.4, loopback, s_server on CPU 0, s_time on CPU 1, 5 s, full handshakes, 2-cert chain root+leaf of the same algorithm)

| Leaf/root alg | Server group | Chain bytes (DER) | Handshakes/s (wall) | conn/client-user-s |
|---|---|---:|---:|---:|
| ECDSA P-256 | X25519 | 739 | 824 | 1309 |
| ECDSA P-256 | X25519MLKEM768 | 739 | 745 | 1246 |
| Ed25519 | X25519 | 608 | 813 | 1251 |
| Ed25519 | X25519MLKEM768 | 608 | 737 | 1192 |
| ML-DSA-44 | X25519 | 7930 | 522 | 1124 |
| ML-DSA-44 | X25519MLKEM768 | 7930 | 610 | 1117 |
| ML-DSA-65 | X25519 | 10988 | 466 | 958 |
| ML-DSA-65 | X25519MLKEM768 | 10988 | 468 | 959 |
| ML-DSA-87 | X25519 | 14904 | 425 | 781 |
| ML-DSA-87 | X25519MLKEM768 | 14904 | 425 | 785 |

Single run, no CIs; s_time's client offers its default groups (X25519MLKEM768 + X25519 key shares), so the
"X25519" rows still include client-side ML-KEM keygen; the X25519 rows' negotiated group is not printed by
`-brief` (shows "?" in CSV). Run-to-run noise is visibly ~10% (ML-DSA-44 X25519 vs hybrid is inverted). The
server-side cost ordering (ML-DSA sign ~0.7-1.3 ms dominates the server per-handshake CPU) is the robust signal.
oqs docker image additionally completed TLS 1.3 + X25519MLKEM768 handshakes with `falcon512`, `p256_mldsa44`,
`sphincssha2128fsimple` (SLH-DSA-128f-equivalent) and `mayo1` certificates (Verification: OK).

### 3.4 Go 1.24.7 stdlib (`results/probe_go.csv`)

ML-KEM-768 keygen/encaps/decaps 63.2/56.3/75.7 us; ML-KEM-1024 97.3/96.2/128.9 us (median, n = 2000).
Loopback TLS 1.3 full handshake (P-256 cert, only the named group offered, n = 300, goroutine server):
X25519MLKEM768 0.95 ms vs X25519 0.79 ms median.

## 4. Implications for the CDN x PQC paper design

- **Crypto costs are tiny vs network RTTs** (ML-KEM < 0.1 ms; hybrid KEX ~0.3 ms total; ML-DSA verify ~0.1-0.3 ms),
  except SLH-DSA signing (26 ms - 0.56 s) and Falcon keygen (7-25 ms). ML-DSA *signing* (0.7-1.3 ms here) is the
  dominant server-side CPU cost per full handshake -> CDN edge capacity / handshake-rate / resumption ratio /
  keyless-signing-offload questions are measurable here.
- **Bytes are the big cost**: an ML-DSA-44 2-cert chain is 7.9 KB vs 0.6-0.7 KB classical; ML-DSA-87 14.9 KB;
  an SLH-DSA-128f leaf+root chain carries two 17,088-B signatures (> 34 KB). With TCP IW10 (~14.6 KB) these cross the initial window - but the
  initcwnd round-trip model is the **prior paper's** contribution (see `prior_work.md`), so use it only as a
  cited building block.
- Full PQ TLS testbed is feasible: netns + veth/TAP + pinned cores + OpenSSL 3.5.4 (ML-DSA certs) or oqs docker
  (Falcon/SLH-DSA/composites). **Latency/loss emulation needs a userspace emulator** (netem unavailable);
  rate limiting via tbf works. Multi-tier CDN topologies (client-edge-shield-origin) can be built with several
  namespaces, but at 4 vCPU only a handful of processes; scale-out effects should be **simulated**, driven by
  the measured per-op costs and byte counts above.
