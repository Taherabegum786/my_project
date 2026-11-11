# Flying, Not Floating: Precise Fixed-Point Falcon on Embedded Processors (Cryptology ePrint Archive 2026)
url: https://eprint.iacr.org/2026/2431
read: abstract-only (PDF blocked by Cloudflare challenge)
problem: Falcon/FN-DSA signing needs real-number arithmetic whose precision affects security; floating point is costly on microcontrollers.
method: First fixed-point FN-DSA signer for microcontrollers, 32.64 arithmetic in constant-time Cortex-M4 assembly, Falcon-512 and Falcon-1024. Keeps reciprocals, inverse square roots and small constants wide and rounds once at the consumer. Also derives Falcon-1024 key generation bounds.
numbers: ~45% fewer cycles than double-precision emulation; measured precision supports 2^99.7 (Falcon-512) / 2^96.7 (Falcon-1024) queries per key vs 2^61.5 / 2^58.7 for double precision (target 2^64); 12-byte words raise signing RAM from 59n to 83n bytes; Falcon-1024 key generation accepts 72.3% of keys vs 8.5% for the Falcon-512 values. (Abstract pairing of 512/1024 figures is inferred from order.) Absolute cycle counts not read.
limits: Full text not read; targets Cortex-M4 only; higher RAM use.
use-for: benchmark
