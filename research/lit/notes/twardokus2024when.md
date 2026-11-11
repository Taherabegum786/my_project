# When Cryptography Needs a Hand: Practical Post-Quantum Authentication for V2V Communications (NDSS 2024)
url: https://www.ndss-symposium.org/ndss-paper/when-cryptography-needs-a-hand-practical-post-quantum-authentication-for-v2v-communications (also ePrint 2022/483)
read: full
problem: PQ signatures overload V2V spectrum and latency limits; current certificate transmission is up to 93% redundant.
method: Adaptive (learned) scheduling of certificate transmissions to free spectrum; "Partially Hybrid" protocol (classical ECDSA plus PQ signing of selected BSMs) with transition timeline; analyzed Falcon, Dilithium, SPHINCS+ and XMSS; provably secure; tested with USRPs, commercial V2V devices, traffic and V2V simulators.
numbers: average added delay 0.39 ms per message; DSRC payload cap 2,304 bytes; C-V2X max payload 437 bytes (10 MHz channel); IEEE 1609.2 SPDU at most 226 bytes (implicit) vs 330 bytes (explicit cert); BSM every 100 ms; certificate cycle 500 ms; certificate-only SPDU 172 bytes; example saving up to 34% of bytes over 5 s.
limits: States current 5G C-V2X cannot practically support PQC (437-byte limit); CA infrastructure and attacks beyond unforgeability (e.g. exclusive ownership) left to future work; receivers without PQ support get only ECDSA-level security.
use-for: v2x
