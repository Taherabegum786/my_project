# Fast and Post-Quantum Authentication for Real-time Next Generation Networks with Bloom Filter (arXiv 2409.10813 2024)
url: https://arxiv.org/abs/2409.10813
read: full
problem: Signatures for delay-aware smart grid and vehicular networks; conventional signatures already add delay and PQ signatures are costlier.
method: TVPD-HORS: HORS variant using a One-hash Bloom Filter as the one-way function, with tunable PQ security; shorter security parameters for short-lived, safety-critical ("time valid") messages. Can underpin time-valid versions of XMSS and SPHINCS+.
numbers: Verification 2.7x faster than HORS (high security) and 5x faster (time valid); key generation up to 6x faster (time valid), up to 1.3x (high security); signing speed similar to HORS. Message size 256 Bytes; SHA-256 (SHA-512 at 128-bit level); parameters (t,k,l)=(64,16,32) for kappa=32, (128,32,64) for kappa=64. Verification 103x faster than SPHINCS+, 15x than Dilithium, 8x than Falcon (128-bit level).
limits: Time-valid mode gives reduced (tunable) security for short-lived messages only; HORS-based, so one-time/few-time keys, not a full multi-use standard by itself. Comparable or slightly worse than HORS in some non-standard-hash settings.
use-for: v2x
