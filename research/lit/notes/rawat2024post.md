# Post-Quantum DNSSEC over UDP via QNAME-Based Fragmentation (Cryptology ePrint Archive 2024/1320, 2024)
url: https://eprint.iacr.org/2024/1320
read: abstract-only
problem: DNS(SEC) messages over 1232 bytes need IP fragmentation (unreliable) or TCP retry (not supported by a non-trivial number of servers); post-quantum signatures exceed this.
method: QNAME-Based Fragmentation (QBF), a DNS-layer scheme that fragments/reassembles large post-quantum DNS(SEC) messages over UDP in 1 round-trip using only standard DNS records.
numbers:
limits: Not assessed (abstract only). Abstract reports experiments only for QTYPE A queries with Falcon-512, Dilithium-2, SPHINCS+.
use-for: grid
