# MAYO: Optimized Implementation with Revised Parameters for ARMv7-M (ePrint 2023/540, preprint)
url: https://eprint.iacr.org/2023/540
read: abstract-only
problem: Efficient constant-time MAYO (UOV-based multivariate signature) on ARMv7-M.
method: Builds on UOV optimization techniques; new approach for evaluating polar forms of quadratic maps; revised parameters (slightly larger keys, shorter signatures, same security level). Evaluated on STM32H753ZIT6.
numbers: NIST level I: signing approx. 43M cycles, verification approx. 6M cycles; both 2.6 times faster than with original parameters.
limits: Abstract only; key/signature sizes and RAM not read. Single board, level I figures only in abstract.
use-for: benchmark
