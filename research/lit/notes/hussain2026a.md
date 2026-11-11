# A Lightweight and Post-Quantum Secure Framework for IEC 61869-9 Sampled Value Communication (arXiv 2608.22123, 2026)
url: https://arxiv.org/abs/2608.22123
read: full
problem: Authenticating IEC 61869-9 Sampled Value (SV) process-bus traffic under stringent real-time limits, with key establishment that survives quantum attacks.
method: Field-selective per-frame authentication (only time-varying SV fields; static fields compared to cache) using optimized Chaskey-12 MAC; ML-KEM-based pairwise authentication and key establishment, analyzed in QROM and verified with AVISPA (OFMC, ATSE). C publisher/subscriber prototype on two Raspberry Pi nodes; compared with HMAC-256, AES-GMAC-128, Blake-2s across the eight SV profiles.
numbers: Optimized Chaskey-12 ~90% lower latency than HMAC on SV packets. MAC times averaged over 100,000 executions. ML-KEM (liboqs) KeyGen/Encaps/Decaps in us: ML-KEM-512 43.624/48.394/48.466; ML-KEM-768 67.630/72.043/76.316; ML-KEM-1024 97.556/104.556/113.490. IEC 62351-6 text cites 3 ms protection timing limit.
limits: Two-node testbed only; manuscript submitted for peer review (not yet published); post-quantum protection covers key establishment, not per-frame MAC (symmetric).
use-for: grid
