# pqm4 - Benchmarking Additional PQ Signature Schemes (NIST CSRC presentation 2024)
url: https://csrc.nist.gov/presentations/2024/pqm4-benchmarking-additional-pq-signature-schemes
read: abstract-only
problem: Suitability and performance of the 40 round-1 additional PQ signature candidates (50 submitted in 2023) on Arm Cortex-M4.
method: Integrate suitable implementations into the pqm4 framework; benchmark on STM32L4R5ZI (640 KB RAM); describe reasons other candidates cannot be integrated.
numbers: STM32L4R5ZI, 640 KB RAM; pqm4 has reference implementations for 15 submissions and M4-optimized implementations for five.
limits: Abstract only (landing page); authors not listed on page; no cycle counts or sizes read. Main obstacle for non-integrated candidates: large key size or excessive memory use.
use-for: benchmark
