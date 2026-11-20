# Project handoff

Everything a new Claude Code conversation needs to continue this PhD project without the old chat.
Last updated: 2026-11-20, at branch `ccr-13230261-tcy4yq`.

## 1. How to start a new conversation

Open Claude Code in the repository on branch `ccr-13230261-tcy4yq` and paste:

```
Read HANDOFF.md, research/STATE.md, research/brief.md and CLAUDE.md before doing anything.
Then continue from section 8 ("What to do next") of HANDOFF.md, starting with step <N>.
This machine is <ubuntu-i5 | wsl-i7 | wsl-ryzen7 | a cloud session>.
```

On a machine of your own, clone first:

```
git clone https://github.com/Taherabegum786/my_project.git
cd my_project && git checkout ccr-13230261-tcy4yq
claude
```

## 2. The research

**Thesis.** Post-quantum (PQ) broadcast authentication for constrained cyber-physical systems:
systems where each message has a tight size or latency budget, receivers have no prior relationship
with the sender, and there is no handshake. Vehicles (V2X) are the first application, not the only one.
Full scope and fixed decisions: `research/brief.md`.

**Core idea.** Each target system is a *budget profile* (bytes per message, deadline, message rate,
loss, privacy). The technology offers authentication modes (full PQ signature, fragmented signature,
Merkle batch signing, a hash chain anchored by a PQ signature, classical+PQ hybrid) and picks one per
profile.

**Planned papers** (one directory each under `papers/`), in this order:

| id | Paper | Status |
|---|---|---|
| benchmark | Cross-domain benchmark of PQ broadcast authentication | experiments done in the cloud, needs runs on your machines, then rewrite and review |
| v2x | Vehicles | not started |
| drones | Drone Remote ID | not started |
| grid | Substation GOOSE (optional) | not started |
| framework | General framework and formal model (last) | not started |

**Your resources.** CS background, no lab. Machines: Windows i7 16 GB, Windows Ryzen 7 8 GB,
Ubuntu i5 8 GB, all CPU-only. Google Cloud access is available on request for runs (not set up).

## 3. Repository map

| Path | What it is |
|---|---|
| `CLAUDE.md` | Rules every session follows (never invent citations or numbers; files, not chat) |
| `HANDOFF.md` | This file |
| `research/brief.md` | Thesis scope and fixed decisions |
| `research/STATE.md` | Pipeline progress table and open items; update after every stage |
| `research/lit/candidates.jsonl` | 57 verified candidate papers |
| `research/lit/notes/` | 42 structured paper notes (some abstract-only; each note says which) |
| `research/lit/refs.bib` | 42 BibTeX entries shared by all papers |
| `.claude/agents/` | The nine pipeline agents (section 4) |
| `.claude/skills/research-pipeline/SKILL.md` | The orchestrator: `/research-pipeline <paper> <stage>` |
| `tools/check_paper.py` | Checks a manuscript's citations and leftover placeholders |
| `lib/pqsig/` | Shared code: liboqs timing harness, byte accounting, loss model |
| `lib/pqsig/proto/` | Real protocol implementations (senders, receivers, erasure coding, attacker) |
| `papers/benchmark/gap.md` | Approved gap statement |
| `papers/benchmark/budget-evidence.md` | Quoted evidence for every budget profile |
| `papers/benchmark/experiments/` | `run.sh` (does everything), `hypotheses.yaml` (pre-registered criteria), `profiles.yaml`, `ENV.md` |
| `papers/benchmark/results/summary.md` | Generated results, verdicts and limitations (source of every paper number) |
| `papers/benchmark/results/raw/` | Raw CSVs; the three largest are stored as `.csv.gz` |
| `papers/benchmark/paper/` | `main.tex`, `numbers.tex` (all numbers as macros), `response.md` |
| `papers/benchmark/review*.md`, `audit*.md` | Three paper reviews and two code audits |
| `papers/benchmark/review-artifacts/` | The reviewer's forgery script against the old chain (frozen) |

## 4. The pipeline

Run a stage with `/research-pipeline <paper-id> <stage>`; `/research-pipeline status` shows progress.

| Agent | Job | Model |
|---|---|---|
| `lit-scout` | Finds candidate papers | Haiku |
| `paper-reader` | Reads one paper, writes a note and BibTeX | Sonnet |
| `gap-analyst` | Gap statement and research questions | Opus |
| `protocol-designer` | Exact scheme specification | Opus |
| `formal-verifier` | Tamarin model and proofs | Opus |
| `experiment-engineer` | Code, benchmarks, simulations | Sonnet |
| `code-auditor` | Independent read-only audit of experiment code before a full run | Opus |
| `paper-writer` | LaTeX manuscript and revisions | Opus |
| `reviewer` | Sceptical committee review, checks every claim against evidence | Opus |

Stages: survey → design → verify → experiments → write → review. The benchmark paper skips design and verify.

Rules that matter:
- Agents hand off through files, not chat; each reads only the files its stage names.
- Experiments stage is an engineer–auditor loop: no full run and no writing while the audit lists a blocker.
- Full runs are started by the orchestrator from a **clean commit**, so every result row records the code commit.
- Hypotheses and decision rules are written in `hypotheses.yaml` before results; any later change must be disclosed in `summary.md`.
- If an agent stops on a usage limit, resume it with SendMessage after the reset rather than starting a new one.
- The pipeline stops for human approval after the gap statement, after the design, and before submission.

## 5. What has been done (benchmark paper)

**Literature survey.** 57 candidates verified, 42 read, gap statement approved: no work compares the same set
of PQ authentication modes against several handshake-free broadcast budget profiles. The gap is narrower
than first assumed (`yoshizawa2026a` already compares many PQ signatures for vehicle messages), so the
novelty is cross-domain, mode-level comparison.

**Experiments, four passes**, each driven by a review:

| Pass | What changed | Why |
|---|---|---|
| 1 | liboqs timing and sizes; byte-accounting scoring; Monte-Carlo loss model | First version |
| 2 | Declared (not observed) signature sizes; budgets corrected from full texts; size classes instead of parameter sets; closed-form loss model | Review 1: reject (Falcon size understated, vehicle budget was the whole payload) |
| 3 | Real implementations of ten modes with liboqs; negative tests; UDP mode; PQ certificate issuer | Review 2: major revision (unfair comparison, OSNMA budget misused) |
| 4 | Secure chain keys, signed anchor schedule, freshness, pollution handling; native message rate; independent loss masks; paired confidence intervals; minimum-budget and active-attacker experiments | Review 3: major revision (chain keys derived from a public seed, forgery demonstrated; cells not independent; vehicles not at the real rate) |

After pass 4, two code audits (`audit.md`, `audit-2.md`) found and fixed: an overstated clock-safety margin,
a denial of service through candidate caps, lenient timing tests, slot binding that used harness-only
information, and a verdict rule changed after results. Debugging also fixed a sender that silently
dropped messages (more than 255 fragments per slot) and a placement error on the vehicle profiles.

**Full run.** Pass 4 ran end to end on `cloud-vm-4core` at commit `95ec879` (clean tree), 35 minutes:
1,701/1,701 reject tests and 625/625 controls passed; the loss-free check found 0 mismatches in 3,192 cells.

**Paper.** Draft 3 (6 pages, IEEEtran) exists but is **stale**: it was written against pass 3.

## 6. Current results (from `results/summary.md`, one cloud VM)

- **What fits:** of 24 lowest-level size classes, a full signature fits one message for 7 (Remote ID, 201 B),
  8 (5G SIB1, 293 B), 5 (OSNMA signature space), 8 (C-V2X 437 B ceiling), 11 (C-V2X 2,481 B ceiling), 11 (DNS ceiling).
  No ML-DSA or SLH-DSA variant fits the small budgets; MAYO, UOV and SNOVA fit several.
- **Feasibility at the real message rate:** of 21 profile-scheme pairs, no fragmentation mode is feasible in 12,
  the chain is infeasible in 2, Merkle-8 in 4.
- **Chain vs best fragmentation mode** (9 decidable groups per loss type):
  share authenticated inconclusive (random loss) / refuted (burst); bytes per message inconclusive;
  delay refuted; minimum budget inconclusive. The 100 ms vehicle latency need is unreachable by design (minimum delay 3 slots).
- **Security:** no forgery or replay accepted under injection, replay, or clock error within 0.5 slot.
  Injection resistance holds for the pre-registered weak attacker (72/72 cells) and fails for the strong same-slot flooder.
  Forgeries become possible from 0.6 slots of receiver clock lag (prompt attacker); a 0.5-slot guard restores a 1-slot margin at about +120 ms delay.
- **Size vs timing:** size binds in 7 of 8 families on x86 (near-tautological).

Plain reading: where a PQ signature can be fragmented within the budget, signing every message is as good or
better and always faster; the chain's value is coverage where fragmentation cannot run, at the cost of delay,
no non-repudiation, tight clock synchronisation, and an 80% ceiling on the vehicle profiles.

## 7. Known limitations and open items

- Timing numbers are from one shared cloud VM; publication numbers must come from your machines.
- Loss is synthetic (i.i.d. and Gilbert-Elliott); no radio scheduling, congestion or measured traces.
- No microcontroller timings; Remote ID and DNS are not in the real-protocol runs.
- UDP mode tested on loopback only.
- Same-slot flooding defeats every mode; not solved.
- Missing values (TODO-RESULT): certificate metadata size, SIB1 latency need, BSM size, LMS H=15/20,
  Remote ID/DNS rates, a primary source for the 100 ms vehicle need, three source-paper reproductions.
- 14 literature notes are abstract-only because IACR ePrint PDFs are behind a bot challenge; the list is in `research/STATE.md`.
  IEEE Xplore, ACM and Springer could not be searched from the cloud.
- Four minor audit findings open (listed in `audit-2.md`).
- Venue: reviewers judged the paper too thin for a main track; current target is a short paper (ACM WiSec short or a PQC-migration / vehicular-security workshop). Not decided.

## 8. What to do next

1. **Run the full benchmark on each of your machines.** On Windows, use Ubuntu 24.04 in WSL2 and work under `~`, not `/mnt/c`. Ubuntu 24.04 is required (the pinned Python packages need Python 3.11+).
   ```
   sudo apt update && sudo apt install -y build-essential cmake ninja-build git libssl-dev python3 python3-venv python3-pip curl
   cd papers/benchmark/experiments
   QUICK=1 PROCS=<n> ./run.sh                                         # 10-15 min check, prints the full-run estimate
   MACHINE_NAME=<name> PROCS=<n> ./run.sh 2>&1 | tee ~/run_<name>.log  # 35-60 min
   ```
   Names and worker counts: `ubuntu-i5` 4, `wsl-i7` 6, `wsl-ryzen7` 3. Keep the machine plugged in, no sleep,
   and idle during the first 15-20 minutes (timing phase).
2. **Commit only that machine's raw results**, from the repository root:
   ```
   git add $(git ls-files -o -m --exclude-standard papers/benchmark/results/raw | grep '_<name>\.')
   git commit -m "benchmark: results from <name>"
   git restore papers/benchmark/results
   git pull --rebase origin ccr-13230261-tcy4yq
   git push origin ccr-13230261-tcy4yq
   ```
   Do not commit `summary.md` or figures from your machines; each run overwrites them. Pushing needs a GitHub personal access token.
3. **Per-machine summaries:** `MACHINE_NAME=<name> build/venv/bin/python summarize.py` for each machine, and compare timings across machines.
4. **Two-machine UDP test** (native Ubuntu as receiver; receiving inside WSL needs extra network setup). Commands are in the docstring of `papers/benchmark/experiments/udp_link.py`.
5. **Fill what you can of the TODO-RESULT list** (section 7), and download the abstract-only ePrint PDFs into `research/lit/pdf/<key>.pdf`.
6. **Decide the venue**, then run `/research-pipeline benchmark write` (draft 4 against pass 4 results) and `/research-pipeline benchmark review` (round 4).
7. **Read the protocol code yourself** (`lib/pqsig/proto/modes.py`) before submitting anything: three reviews found real defects, and the paper carries your name.
8. **Then start the vehicle paper:** `/research-pipeline v2x survey`.

## 9. Environment notes

- Cloud sessions use the environment `my_project`, which allows the paper sites (arxiv.org, eprint.iacr.org, csrc.nist.gov,
  rfc-editor.org and others) plus github.com. IACR ePrint PDFs still return a bot challenge; abstract pages work.
- A fresh cloud container has no LaTeX; install with
  `apt-get install -y texlive-latex-recommended texlive-latex-extra texlive-publishers texlive-fonts-recommended latexmk`.
- liboqs 0.16.0 is built by `run.sh` under `papers/benchmark/experiments/build/` (git-ignored) and reused if present.
- GitHub pushes from the cloud occasionally fail with a temporary 503; retry with a short backoff.

## 10. Do not

- Invent citations, numbers or proof results; missing data is `TODO-RESULT`.
- Change a criterion in `hypotheses.yaml` after seeing results without disclosing it.
- Commit results from a dirty working tree or from a QUICK run as publication numbers.
- Commit `summary.md` or figures from your own machines.
- Submit any paper without reading it and its code yourself, and check each venue's AI-assistance disclosure policy.
