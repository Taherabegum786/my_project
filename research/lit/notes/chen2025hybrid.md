# Hybrid Scheme of Post-Quantum Cryptography and Elliptic-Curve Cryptography for Certificates - A Case Study of SCMS in V2X Communications (arXiv preprint 2025)
url: https://arxiv.org/abs/2501.07028
read: full (manuscript is in Chinese; abstract in English)
problem: ECC-based SCMS is vulnerable to quantum attacks, but PQC keys/signatures are large and slow relative to V2X limits (packet length, sign/verify speed, security level, privacy).
method: Hybrid certificate scheme: PQC establishes quantum-resistant security level; ECC establishes anonymous (pseudonym) certificates and keeps packets short. Implemented SCMS end entity on Chunghwa Telecom SCMS and Clientron OBU; field tests in Danhai New Town, New Taipei City; compares Dilithium, Falcon, SPHINCS+ with ECC.
numbers: Default WSM length 1400 bytes. Public key / signature (bytes): ECDSA P-256 33/64; Dilithium-2 1,312/2,420; Dilithium-3 1,952/3,309; Falcon-512 897/666; Falcon-1024 1793/1280; SPHINCS+ SHA2-128f 32/16,720; SHA2-192f 48/34,896. Paper concludes only Falcon-512 fits current V2X packet limit.
limits: Field tests with one vendor stack; no ML-KEM or full pseudonym derivation (addressed in later work); Chinese-language text.
use-for: v2x
