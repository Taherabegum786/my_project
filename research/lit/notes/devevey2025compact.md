# Compact, Efficient and Non-Separable Hybrid Signatures (IACR ePrint 2025/2059, 2025)
url: https://eprint.iacr.org/2025/2059
read: abstract-only
problem: During the PQ transition, hybrid signatures face cross-protocol, separability and recombination attacks; simple concatenation of signatures has separability issues.
method: Introduces a security notion, Hybrid EU-CMA. Adapts the Fiat-Shamir transform (with or without aborts) to build hybrid signatures from two identification schemes. Concrete scheme Silithium combines the identification schemes underlying EC-Schnorr and ML-DSA; needs an ML-DSA implementation with the external mu option at verification plus an elliptic curve library. Claimed safe alongside ML-DSA and either EC-Schnorr or ECDSA. Proof-of-concept OpenSSL implementation.
numbers:
limits: Not stated in the abstract; PDF not read (ePrint bot challenge). Claims smaller signatures and faster runtime than concatenation but gives no figures in the abstract.
use-for: framework
