# Deployment Feasibility Analysis of Post-Quantum Digital Signatures in Safety-Critical C-V2X Communication for Urban Mobility Scenario (arXiv 2608.05087 preprint, 2026)
url: https://arxiv.org/abs/2608.05087
read: full
problem: Which NIST PQ signature algorithms fit the SAE J3161 C-V2X transport-block limit, and what they cost in PDR and latency.
method: Transport-block feasibility analysis (IEEE 1609.2 structures, J3161 radio parameters) for ECDSA P-256, Falcon-512, Dilithium-2, SPHINCS+; then full-stack C-V2X PC5 Mode 4 co-simulation of Falcon-512 vs ECDSA, 24 scenarios (six traffic levels of service, LOS and NLOS), measured at a roadside unit.
numbers: Falcon-512 mean latency near 52 ms; 95th-percentile latency 97-98 ms; 90% PDR threshold met by Falcon-512 only at LOS level of service A; ECDSA met it through level of service C; neither met it under NLOS; 24 scenarios.
limits: Dilithium-2 and SPHINCS+ excluded as exceeding transport-block capacity; Falcon-512 degrades PDR with traffic; no algorithm meets threshold under NLOS; study notes simulated certificate transmission differs from a fully compliant implementation.
use-for: v2x
