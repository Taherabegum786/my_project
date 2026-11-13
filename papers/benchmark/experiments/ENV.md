# Environment

`run.sh` reproduces everything from a clean Ubuntu 22.04/24.04 (apt: build-essential cmake ninja-build git libssl-dev python3 python3-venv python3-pip curl).
`MACHINE_NAME=<name> ./run.sh` is the full run; `QUICK=1 ./run.sh` is the few-minute smoke run (it also prints the estimated duration of the full run on that machine).

## Pinned versions

| component | version | where |
|---|---|---|
| liboqs | tag `0.16.0` (git commit recorded in `build/liboqs_commit.txt`; the smoke run used 5a1a854b0dc9f2141bdc771c555ee60c37950183) | built by run.sh with MAYO, UOV, SNOVA, CROSS enabled, Release, static; `LIBOQS_TAG` overrides |
| ctypes shim | `lib/pqsig/proto/pqshim.c`, liboqs.a linked whole into `libpqshim.so` (same compile as the benchmark; no second liboqs build) | run.sh |
| OpenSSL | system libssl-dev (3.0.13 on Ubuntu 24.04): Ed25519 and ECDSA P-256 baselines in C (`oqs_bench --classical`), Ed25519 in the protocols through python-cryptography | |
| Python | 3.10+ (smoke run: 3.13.18), venv at `build/venv` | |
| Python packages | `requirements.txt`: numpy 2.5.3, pandas 3.0.5, PyYAML 6.0.3, matplotlib 3.11.2, tabulate 0.10.0, cryptography 50.0.1, **zfec 1.6.0.0** (Reed-Solomon erasure coding) | pip in venv |
| compilers/tools (smoke run) | gcc 13.3.0, cmake 3.28.3, ninja 1.11.1 | |

Hardware of the smoke run: 4 cores, 15 GB RAM, shared cloud VM (Linux 6.18). Protocol runs use at most `PROCS` (default `nproc`) worker processes, each well under 1 GB.

## Pieces

- `lib/pqsig/oqs_bench.c` - C timing harness (liboqs + OpenSSL); default scheme list = lowest-level class of each family plus all levels of ML-DSA, Falcon, MAYO, UOV, SNOVA and only the pure SLH-DSA sets; `FULL_LIST=1` in run.sh benchmarks all 221. Key generation is repeated at most 200 times.
- `lib/pqsig/proto/modes.py` - native-rate senders / receivers (traffic model, allocation rule and security rules in the docstring); `erasure.py` (zfec Reed-Solomon, code-size rule, pollution-tolerant Assembler); `attacks.py` (attacker toolkit); `oqs.py` (liboqs through ctypes; per-process signature cache shared by modes of one (profile, scheme)).
- `lib/pqsig/lossform.py` - seeded loss masks (`make_mask(..., stream=...)`: independent stream per profile / scheme / condition). The pass-3 closed forms were removed; the cross-check is in `crosscheck_loss.py`.
- `experiments/hypotheses.yaml` - conditions, grids, deadlines, minimum effects and decision rules, read by `summarize.py` (fixed before the pass-4 results were seen).
- `experiments/run_proto.py` - sweep (operating point, minimum-budget sweep, active attacker) and UDP runner; `udp_link.py`; `negative_tests.py` (reject tests and controls); `crosscheck_loss.py`; `estimate_duration.py`; `score.py`; `summarize.py`.
- Pass-4 pins: one extra requirement-free dependency (none): scipy is NOT used (Student-t table in `summarize.py`).

## Two-machine UDP run

See `udp_link.py` docstring and the last section of `results/summary.md`.
