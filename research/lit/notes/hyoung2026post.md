# Post-Quantum Command Authentication for Unmanned Systems: A KpqC Feasibility Study under Real-Time and Bandwidth Constraints (IACR ePrint 2026/2343, 2026)
url: https://eprint.iacr.org/2026/2343
read: abstract-only
problem: UAV/UGV command and authentication channels use classical public-key crypto; PQC keys and signatures are larger and sometimes slower, while command links are limited in message rate, MTU, latency deadline and bandwidth.
method: Studies Korean PQC (HAETAE, AIMer, SMAUG-T, NTRU+) in the authentication and key-establishment path of ROS2/DDS-Security, framed as a size-latency budget problem. Compares classical (ECDSA/ECDH), NIST (ML-KEM, ML-DSA, SLH-DSA) and KpqC on one testbed. Defines a feasibility envelope mapping algorithms to channel conditions, validated with handshake measurements over emulated constrained links on a two-node testbed.
numbers:
limits: Full text not reachable (PDF returned HTTP 403 from Cloudflare); details unverified. Per abstract, scope is the ROS2/DDS-Security handshake on a two-node emulated testbed. Preprint, not peer reviewed.
use-for: drones, benchmark
