# Signer-Optimal Multiple-Time Post-Quantum Hash-Based Signature for Heterogeneous IoT Systems (arXiv 2411.01380 2024)
url: https://arxiv.org/abs/2411.01380
read: full
problem: Lightweight PQ signatures for low-end IoT (wearable sensors, telemetry); NIST PQC standards are too costly, HORS wastes keys when reused.
method: MUM-HORS: multiple-time HORS with compact key-management data structures (bitmap) for high key utilization in offline/online settings and optimized resistance to weak-message attacks. Tested on ARM Cortex A-72, 8-bit AVR ATmega2560 and commodity hardware.
numbers: Up to 40x better key utilization at same signing capacity (2^20 messages, 128-bit security) vs multiple-time HORS; 2x and 156-2463x faster signing than conventional-secure and NIST PQ-secure schemes on ARM Cortex. On A-72: 24x faster than Falcon-512, 200x Dilithium, 3900x SPHINCS+, 243-670x XMSS variants. Commodity: signing 17x/24x/511x faster than Falcon-512/Dilithium-II/SPHINCS+. Signing 1.75x slower than baseline HORS on A-72.
limits: Stateful key management; finite signing capacity (e.g. 2^20 messages); signature size similar to HORS (larger than conventional); no broadcast/time-valid mechanism.
use-for: grid
