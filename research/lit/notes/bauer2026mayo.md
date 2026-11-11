# MAYO Lite: a Low-RAM Implementation of the MAYO Signature Scheme (ePrint 2026/1634, preprint)
url: https://eprint.iacr.org/2026/1634
read: abstract-only
problem: MAYO verification (reference in pqm4) needs too much RAM for smart cards and small microcontrollers.
method: Pure-C memory-optimized verification: expand public key vector-by-vector on the fly; reorder SPS matrix product so each P-vector is used once; add precomputed multiples of each P-vector directly onto the result. Measured with pqm4 for MAYO1/2/3; other sets (incl. MAYO5) on the authors' own host framework.
numbers:
limits: Abstract only; exact RAM and cycle figures not read. States 97-99% RAM reduction vs pqm4 reference, runtime +50-200%, code size maintained. Verification only.
use-for: benchmark
