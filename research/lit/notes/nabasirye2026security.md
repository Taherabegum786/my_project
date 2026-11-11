# A Security-Aware PQC Benchmarking Framework on Dual-Core Xtensa Silicon (IACR ePrint 2026/2384, 2026)
url: https://eprint.iacr.org/2026/2384
read: abstract-only
problem: Memory-heavy PQC at the smart grid edge conflicts with the IEC 61850 GOOSE tripping window of 3 ms or less.
method: Hardware-in-the-loop benchmarking framework on dual-core Xtensa LX7 (ESP32-S3) under FreeRTOS; crypto pinned to Core 1, grid interrupts on Core 0; heap-auditing methodology; analytical latency model of Octal-SPI PSRAM stall under masked NTT.
numbers:
limits: Abstract only, so no results verified. Abstract does not indicate a comparison of PQ signatures across more than one broadcast domain (grid only; keywords list ML-KEM and ML-DSA). Handshake-free broadcast coverage is not stated in the abstract (GOOSE is mentioned only as a timing constraint).
use-for: grid
