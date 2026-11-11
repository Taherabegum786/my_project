# Benchmarking NIST-Standardised ML-KEM and ML-DSA on ARM Cortex-M0+: Latency, Rejection-Sampling Variance, and Memory on the RP2040 (arXiv 2026)
url: https://arxiv.org/abs/2603.19340 (v6, 11 Aug 2026)
read: full (text skimmed; tables not all checked)
problem: ML-KEM (FIPS 203) and ML-DSA (FIPS 204) are sparsely benchmarked on Cortex-M0+.
method: All six parameter sets on RP2040 (Raspberry Pi Pico) at 125 MHz, PQClean reference C; stack painting for memory; 10,000 ML-DSA-44 signatures to study rejection-sampling tail; open-source suite.
numbers: ML-KEM-512 full exchange 35.7 ms (17x faster than mbedTLS ECDH P-256 on same hardware); ~54 ms estimated on 32-cycle-multiplier silicon. ML-DSA signing CV 66.0-73.5%. ML-DSA-44 n=10,000: p99 584 ms, max 1,157 ms. n=100 campaign: ML-DSA-44 mean 158.9 ms, p99 489.4 ms; ML-DSA-65 mean 256.6 ms, p99 952.8 ms; ML-DSA-87 mean 355.2 ms, p99 1,124.5 ms. About 2.0x slower than published Cortex-M4 reference C. RP2040 has 264 KB SRAM, 2 MB flash.
limits: Reference C only (upper bound on memory); RP2040 single-cycle multiplier is optimistic; FN-DSA/Falcon not evaluated; ML-DSA-65/87 quantiles are lower bounds; no key recovery claimed.
use-for: benchmark
