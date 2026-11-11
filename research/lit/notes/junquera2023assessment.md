# Assessment of cryptographic approaches for a quantum-resistant Galileo OSNMA (arXiv 2312.11080; published NAVIGATION 71(2), 2024)
url: https://arxiv.org/abs/2312.11080 (doi 10.33012/navi.648)
read: full
problem: Galileo OSNMA signs TESLA root keys with ECDSA, which Shor's algorithm would break; can NIST PQC fit the navigation-message bandwidth?
method: Reviews OSNMA message structure (DSM-PKR, DSM-KROOT, 16 DSM blocks max) and compares Dilithium, Falcon, SPHINCS+, and stateful XMSS/LMS against space available; proposes transitory countermeasures.
numbers: OSNMA ECDSA P-256 signature 512 bits, P-521 1056 bits. Signature / public key: Dilithium2 19360 bits (2420 B) / 10496 bits (1312 B); Falcon-512 5328 bits (666 B) / 7176 bits (897 B); SPHINCS+-128s 62848 bits (7856 B) / 256 bits (32 B). OSNMA: 104-bit DSM blocks, 1664 bits for two use cases, 1632 bits cryptographic material; TESLA key <=512 bits, tag <=40 bits. Shortest Falcon key needs 71 DSM blocks, shortest Falcon signature 67 DSM blocks; BID field is 4 bits (16 blocks). Falcon signature nearly 5 times bigger than ECDSA P-521.
limits: Concludes OSNMA is not ready for PQC and needs significant change; Falcon best but does not fit; no implementation or timing evaluation.
use-for: framework, benchmark
