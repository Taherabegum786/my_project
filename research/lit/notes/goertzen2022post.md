# Post-Quantum Signatures in DNSSEC via Request-Based Fragmentation (arXiv 2211.14196, 2022)
url: https://arxiv.org/abs/2211.14196
read: full
problem: Post-quantum signatures/keys exceed the recommended 1232-byte DNS UDP message limit; IP fragmentation is fragile and TCP fallback is unreliable/slow.
method: ARRF, application-layer, request-based fragmentation: first response carries a truncated fragment, requester asks for remaining fragments. Implemented as a transparent daemon in front of requester and resolver; Falcon-512, Dilithium2, SPHINCS+-SHA256-128S via liboqs in BIND; simulated network.
numbers: Resolution time with 10 ms latency, 50 MB/s bandwidth (standard / parallel ARRF): Falcon-512 82.11 / 61.96 ms; Dilithium2 82.24 / 62.52 ms; SPHINCS+-SHA256-128S 82.59 / 63.45 ms; RSA-2048 41.50 ms; ECDSA P256 47.78 ms. Data transfer (bytes, standard / parallel ARRF): Falcon-512 3,112 / 2,557; Dilithium2 8,623 / 8,367; SPHINCS+ 26,073 / 26,140; RSA-2048 1,081; ECDSA P256 504. Limit: 1232 bytes.
limits: Simulated network only; real-world network assessment left as next step. PQ algorithms still slower than RSA/ECDSA. Falcon-512 best of the three.
use-for: grid
