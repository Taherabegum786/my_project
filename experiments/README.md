# DAPV experiments

This directory reproduces every measurement in Sections 5–6 of `manuscript/main.pdf`.

## What is here

| Path | Purpose |
|---|---|
| `patches/oqs-provider-0.10.0-dapv.patch` | 32-line hook in oqs-provider. After the classical half of a hybrid signature verifies, it hands the PQ half to the host process (`dapv_submit`). |
| `src/tlsclient.c` | TLS 1.3 client and load generator. Implements DAPV with a `thread` (one thread per job) or `pool:M` worker model, or `none` (synchronous). |
| `src/tlsserver.c` | Multi-threaded TLS 1.3 server (unmodified with respect to DAPV). |
| `src/tapbridge.c` | Userspace link emulator between two TAP devices: one-way delay plus 1 Gbit/s serialisation. It replaces `tc netem`, which the evaluation kernel lacked. |
| `scripts/make_certs.sh` | Builds root → intermediate → leaf chains, and a single self-signed leaf, for each algorithm. |
| `scripts/net.sh` | Creates the `srv`/`cli` network namespaces (MTU 1500, offloads off), starts the emulator, and sets the RTT. |
| `scripts/run_e1_latency.py` | E1: sequential handshakes and per-job Δt at RTT 0/20/50/100/150 ms. |
| `scripts/run_e2_throughput.py` | E2: closed-loop handshake rate, with separate vs co-located CPU placement. |
| `scripts/analyse.py` | Summary CSVs and figures. |
| `results/` | Raw per-handshake and per-job CSVs (E2 raw files are in `e2_raw.tar.gz`), plus summaries. |
| `figures/` | Figures produced by `analyse.py`. |

## Software versions

- OpenSSL 3.5.4
- liboqs 0.14.0 (AVX2)
- oqs-provider 0.10.0 with the patch applied
- Linux 6.18, GCC 13.3

## Reproducing

```bash
# 1. Build OpenSSL 3.5.4 -> /opt/ossl, liboqs 0.14.0 -> /opt/liboqs,
#    and the patched oqs-provider -> /opt/ossl/lib/ossl-modules/
make                                   # builds bin/
scripts/make_certs.sh /opt/dapv_certs
scripts/net.sh up 3                    # emulator on CPU 3
python3 scripts/run_e1_latency.py      # about 55 min
python3 scripts/run_e2_throughput.py   # about 25 min
python3 scripts/analyse.py
```

CPU placement is fixed in the drivers:
- server on CPU 0
- client on CPUs 1–2
- link emulator on CPU 3

## Summary of results

- **Latency:** DAPV − synchronous median latency is within ±0.2 ms for ML-DSA-44, ML-DSA-65 and FN-DSA-512 at every RTT. For SLH-DSA-128f it is −1.59 ms at RTT 0. A thread per job adds +0.15 ms.
- **Δt (bounded pool, ML-DSA-44):** median 0.079 ms, p99 0.42 ms.
- **Throughput:** no gain from DAPV in either CPU placement.
- **Round trips:** 1 for P-256, FN-DSA-512 and ML-DSA-44; 2 for ML-DSA-65; 3 for SLH-DSA-128f. This matches the initial-congestion-window model.
