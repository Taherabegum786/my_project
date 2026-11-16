# Pipeline state

Updated by the orchestrator after every stage. One line per paper.

| paper | survey | design | verify | experiments | write | review |
|---|---|---|---|---|---|---|
| benchmark | done | n/a | n/a | awaiting-approval (pass 4, audited, run on cloud-vm-4core at 95ec879) | todo (draft 4; draft 3 is stale) | todo (round 4) |
| v2x | todo | todo | todo | todo | todo | todo |
| drones | todo | todo | todo | todo | todo | todo |
| grid | todo | todo | todo | todo | todo | todo |
| framework | todo | todo | todo | todo | todo | todo |

Values: todo / running / awaiting-approval / done.

## Open items for the human
- ePrint PDFs are behind a bot challenge, so 14 notes are abstract-only. Download these PDFs
  into `research/lit/pdf/<key>.pdf` so they can be read in full: hyoung2026post (2026/2343),
  fall2025sok (2025/2052), nabasirye2026security (2026/2384), gringiani2023mayo (2023/540),
  bauer2026mayo (2026/1634), aardal2024optimized (2024/1563), pornin2025falcon (2025/123).
- IEEE Xplore, ACM and Springer could not be searched from the cloud session; check them by
  hand for a survey of post-quantum broadcast authentication.
- benchmark experiments: only cloud smoke runs exist. On each of your three machines run
  `MACHINE_NAME=<name> ITER=10000 ITER_SLOW=200 ./run.sh` in `papers/benchmark/experiments`
  (several hours; `run.sh` has not yet completed in a single clean pass), then commit
  `papers/benchmark/results/raw/`.
- benchmark: open TODO-RESULT items are listed at the end of `papers/benchmark/results/summary.md`
  (fragment-header sizes, OSNMA block count, darzi2026a reproduction, loss-model parameters).
- benchmark: scope kept cross-domain (vehicle profile added to the loss analysis); venue to be chosen after pass 3.
- benchmark pass 4: audited (audit.md, audit-2.md: no blockers; 4 minors open) and run in full on
  `cloud-vm-4core` at commit 95ec879 (clean tree). Run `MACHINE_NAME=<name> ./run.sh` in
  `papers/benchmark/experiments` on each of your machines (about 35-45 min) and commit `results/raw/`.
  The three largest raw CSVs are stored gzipped; run.sh regenerates the plain files.
- benchmark: draft 3 and numbers.tex are stale against the pass 4 summary; next is the write stage, then review round 4.
