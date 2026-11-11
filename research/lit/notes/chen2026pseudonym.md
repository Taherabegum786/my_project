# Pseudonym Scheme Based on Hybrid Certificates for SCMS in Vehicular Communications (arXiv preprint 2026)
url: https://arxiv.org/abs/2606.14008
read: full
problem: IEEE/ETSI vehicular security (SCMS, Butterfly Key Expansion) relies on ECC, vulnerable to future quantum attacks; need pseudonym certificates under PQC while meeting V2X constraints.
method: Hybrid certificate combining ECC with PQC, plus a generalized pseudonym scheme compatible with various algorithms, designed so no one can link a pseudonym-certificate public key to the enrollment-certificate public key. Performance evaluation of RSA, ECC and NIST-standardized PQC algorithms (message length, computation time) on a resource-constrained end entity. Recommended: CA uses Falcon-512, end entities use ECDSA P-256, ML-KEM-512 for KEM.
numbers: WSM default maximum 1400 bytes (IEEE 1609.3); BSM sent every 100 milliseconds; with Falcon-512 CA plus ECDSA P-256 EE the PDU stays below 1400 bytes; Falcon-512 verification faster than ECDSA P-256 in their experiment.
limits: Hybrid approach is described as a transitional solution; pure PQC certificates only for infrastructure devices; no revocation/linkage-value treatment noted.
use-for: v2x
