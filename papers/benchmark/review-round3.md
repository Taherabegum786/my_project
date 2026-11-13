# Review round 3: benchmark, draft 3 (target venue: ACM WiSec short paper, 6 pages incl. references)

Paper: "Post-Quantum Broadcast Authentication in Per-Message Byte Budgets: Fit and Measured Behaviour of Ten Modes Across Channels" (`paper/main.tex`, `paper/numbers.tex`).

I wrote this review on my own first. Only afterwards did I compare it with `review-round2.md` and `paper/response.md` (Section 7). I did not take `response.md` on trust.

What I checked:
- Evidence: `results/summary.md`; `results/q2_verdicts.csv`; `results/proto_summary.csv`; `results/raw/proto_results_cloud-vm-4core.csv` (100,800 rows); `raw/negative_tests_*.csv`, `raw/loss_crosscheck_*.csv`, `raw/udp_smoke_*.csv`; `budget-evidence.md`; `experiments/profiles.yaml`.
- Code: `lib/pqsig/proto/{modes,erasure,oqs}.py`; `experiments/{run_proto,negative_tests,summarize}.py`; `lib/pqsig/lossform.py` (`make_mask`).
- Literature notes for the cited claims: `research/lit/notes/`.
- Recomputation: I recomputed all Q2 verdict counts from the raw per-seed CSV with my own script. I also ran one attack against the chain receiver (Major 4).
- Provenance: `git diff 694ba76 HEAD -- lib papers/benchmark/experiments` is empty, so the tagged commit contains the code that produced the numbers.

## 0. Tool check

`python3 tools/check_paper.py benchmark`:

```
40 cited keys, 9 problems
  papers/benchmark/paper/main.tex:14: unresolved placeholder
  papers/benchmark/paper/main.tex:36: unresolved placeholder
  papers/benchmark/paper/main.tex:74: unresolved placeholder
  papers/benchmark/paper/main.tex:138: unresolved placeholder
  papers/benchmark/paper/main.tex:156: unresolved placeholder
  papers/benchmark/paper/main.tex:159: unresolved placeholder
  papers/benchmark/paper/main.tex:504: unresolved placeholder
  papers/benchmark/paper/main.tex:547: unresolved placeholder
  papers/benchmark/paper/numbers.tex:8: unresolved placeholder
```

(Exit status 1.) All 40 keys resolve. Line 14 and numbers.tex line 8 are the macro definitions, and line 36 is the draft banner. The PDF is 6 pages in IEEEtran, with the references starting at the bottom of page 5.

**Known placeholders. Acknowledged, listed once, not counted.**
- `\todo` items: the FN-DSA standard (l.74); the full text of wong1998digital/park2002efficient (l.138); the full text of hyoung2026post/fall2025sok (l.156); the NIST additional-signature status (l.159); Cortex-M timings (l.504); the artifact URL (l.547).
- TODO-RESULT macros: `\RunCPU`, `\LMSHigh`, `\BSMSizeCV`, `\PerDNS`, `\HdrSrc`, `\CertMeta`, `\DarziOTARepro`, `\DarziTenRepro`, `\JunqueraKeyRepro`, `\GoertzenRepro`, `\YoshizawaRepro`, `\ChenRepro`.
- Also the author block, the DRAFT banner, and the single-cloud-VM timing caveat.

## 0b. Macro audit (task a)

I checked about 90 macros against `summary.md` or the CSVs. All of them match their source except the integrity items below. The checked macros:

- **Scheme set:** `\NumParamSets` 221, `\NumClasses` 64, `\NumClassesLow` 24, `\NumStateful` 5.
- **Sizes and timings:** `\SigFalcon` 752, `\SigMLDSA` 2420, `\SigSLHs` 7856, `\SignMedFalcon` 235, `\SignMedMLDSA` 68, `\SignMedSLHs` 591.
- **Budgets:** `\BudRID` 201, `\BudSIB` 293, `\BudKROOT` 158, `\BudPKR` 76, `\BudCV` 374, `\BudJ` 2414, `\BudCVSens` 334, `\FitCVSens` 8.
- **Table II:** all 30 cells of `\TabQOneRows`, recounted against the totals and PQ-issuer tables. Also `\KeyFitPKR` 9 and `\CertPQJ`/`\CertPQJmeta`/`\CertClJ` 4/3/4.
- **Margins and message counts:** `\MarFalconJ` 1662, `\MarFalconJpq` 13, `\MarFalconJcl` 660, `\MarMLDSAJ` -6, `\MsgFalconCV` 3 / -378, `\MsgMLDSAsib` 9 / 1.28 s, `\MsgMLDSArid` 13 / 36 s, `\MsgFalconKR` 5 / 2.28e3 s.
- **Join times:** `\JoinOSmin`/`\JoinOSmax` 810 / 5.652e4 s, `\JoinRIDmet` 11, `\JoinRIDmax` 276 s.
- **Consistency checks:** Darzi 13/34, Junquera 68/67.
- **Q2 grid:** `\NumProtoRows` 100,800 = 3 profiles x 7 schemes x 10 modes x 2 M x 12 conditions x 20 seeds. Also `\SlotSIB`/`\SlotCV`/`\SlotJ` 293/366/2406, `\AllocSIB` 2930, `\WinSIB`/`\WinCV` 1600/1000, `\HdrProtoLo`/`\HdrProtoHi` 3/11.
- **Verdict table:** all 12 rows of `\TabVerdictRows`. I recounted the `chain` rows from the raw CSV. My counts are 118/3/341 (H2a), 131/290/19 (H2b), 0/440/0 (H2c) and 25/385/30 (H2d), all identical to the paper. I also confirmed `\HaInfeas` 22 / `\HaRuns` 96 and `\HaWsib`/`\HaWcv`/`\HaWj` 51/51/16.
- **H2b ratios and target share:** `\ByteRatioMed` 1.132 (range 0.706-1.599, 19 pairs) and `\TgtFragMDS` 17/4.
- **Quoted shares:** all eight `\Sh...` values.
- **Table IV:** all 12 rows of `\TabQTwoRows`.
- **Merkle delays:** `\MerkFourDelay`/`\MerkSixteenDelay` 6560/25760 ms.
- **Burst deltas:** `\BurstChain`/`\BurstFragMDS`/`\BurstMerkleEight` -0.119/-0.076/-0.223.
- **Checks:** `\XCells` 1716, `\XOut` 0, `\XMaxDiff` 0.0175; `\NegPassed`/`\NegRuns` 427/427, `\NegCtrl` 21; `\UDPSame` 4/4.
- **SLH-DSA and Q3:** `\SLHInfeas` 8/24, `\SLHSignOverSlot` 24, `\RTCheckSlow` 0/202, `\QThreeSize` 7/0/8.

## 1. Integrity (blocks submission)

1. **`\GEBursts` = "3, 5, 10" is not backed by data.**
   - Method (l.259) says Gilbert-Elliott loss is run "with mean bursts of 3, 5, 10 slots".
   - The sweep (`run_proto.py` `conditions()`) runs bursts (3, 10) only. The raw CSV contains exactly six GE conditions: {0.1, 0.2, 0.3} x {3, 10}.
   - The "3/5/10" in `summary.md`'s parameter table is hard-coded prose (`summarize.py` l.110), not derived from the data. Burst 5 appears only in a UDP smoke row.
   - Fix: set the macro to "3, 10" and correct the summary text.
2. **The target-share sentence is stated without its loss condition, and other conditions contradict it.**
   - The paper says: "The chain reaches share >= 0.95 at M = 10 for all 21 (profile, scheme) pairs; frag_mds does so for 17 and needs M = 40 for the other 4" (l.426-429).
   - `summarize.py` computes this at i.i.d. p = 0.1 only.
   - At GE 0.3/b10 the chain is at 0.888 (SIB1) and 0.875 (C-V2X 437), below 0.95 for every scheme.
   - Fix: state "at i.i.d. p = 0.1", or recompute the claim over all conditions.
3. **"427 negative tests" is the wrong label for what the CSV contains** (abstract, contributions, Sec. III).
   - The 427 rows include 70 "T0 control: untouched stream authenticates everything" rows. These are positive controls.
   - They also include 21 "T4-control" rows, whose "pass" means the forgery *was accepted*.
   - The actual reject tests number 336.
   - Fix: report "336 negative tests plus 70 positive and 21 ablation controls".

## 2. Summary and novelty

The paper derives authentication budgets from sources for Remote ID, SIB1, OSNMA, two C-V2X ceilings and DNS. It scores 24 lowest-level liboqs size classes by declared size. It then compares ten liboqs-backed modes on a seeded, collision-free slot channel at an "equal" slot allocation (fragmented/MDS, hybrid, Merkle, and three PQ-anchored TESLA-chain variants).

Its findings: the chain wins on share, loses on bytes, delay and join time, and gives up non-repudiation.

The Q1 budget work and the Falcon-512 C-V2X reconciliation are careful and useful. The Q2 "findings", however, are largely consequences of the allocation rule and the window model (Majors 2-3). The paper proposes no mechanism, gives no proof and evaluates no adversary. The delta over darzi2026a (which already has a PQ-anchored TESLA chain with a proof and an OTA testbed) and over twardokus2024when / abrar2026deployment is therefore not yet enough for a WiSec short paper.

## 3. Major issues

1. **The verdict rule is not sound, and the cells are not independent (task b).**
   - **Ties are ignored.** H2a is "supported" with 118 wins, 3 losses and 341 ties (74 % ties). Under the rule, 1 win, 0 losses and 1000 ties would also be "supported".
   - **The cells are not replicates.**
     - `make_mask(G, seed, p, burst)` depends only on G = (N + E + max(E,16)) x M. So every profile and every PQ scheme sees the **identical** loss mask for a given (seed, condition, M).
     - The chain's share is identical across all 7 schemes in 96.7 % of (profile, M, condition, seed) tuples. The chain's anchor is decodable regardless of scheme.
     - That is why SIB1 and C-V2X 437 have exactly the same 51 wins.
     - The 462 cells are therefore about 66 (profile, M, condition) groups, each counted up to 7 times against one shared chain outcome.
   - **The minimum effect of 0.005 is smaller than one message of 80** (0.0125). 33 of the 118 wins are below a 0.02 difference.
   - **H2a after separating the infeasible cells** (my recount):

     | Subset | wins / losses / ties |
     |---|---|
     | All cells | 118 / 3 / 341 |
     | `frag_mds` feasible | 96 / 3 / 341 |
     | Feasible, excluding SLH-DSA and ML-DSA-44 | 39 / 3 / 288 |
     | Feasible, i.i.d. loss only | 16 / 0 / 184 |
     | OV-Is and SNOVA (132 cells) | 0 wins |

     80 of the 96 feasible wins are GE burst cells.
     "Supported" survives the separation only because the rule ignores ties. The honest statement is narrower: "under bursts, or for signatures spanning 3 or more slots".
   - **Fix:**
     - Report per-(profile, scheme) effect sizes with paired confidence intervals, using conditions as blocks.
     - Drop the win/loss counting, or count each (profile, M, condition) group once.
     - Add a tie-aware criterion.
     - Restate H2a with its scope in the abstract and conclusion.
2. **H2a, H2b and H2c follow from the design, not from measurement.**
   - Rule R1 puts one heavy-object symbol in *every* usable slot. The chain anchor is therefore sent as 160-200 MDS symbols when k = 1-34 suffice, which is up to 200x redundancy. The 32 B tag+key is repeated in all M slots, and the key again in all M slots of the next window.
   - This buys share (H2a) and costs bytes (H2b) by construction. The paper itself concedes H2b "mostly reflects the share in its denominator", yet the abstract still lists it as "refuted".
   - H2c is fixed by d = 1 window. The chain cannot authenticate before the next window, while a fitting signature authenticates inside its own. "Refuted in every cell" (the minimum chain/frag delay ratio is 1.10) is a tautology.
   - The delay metric is a median over *authenticated* messages only. When frag_mds authenticates 14 % (ML-DSA-44, SIB1, p = 0.3), its "delay" describes the survivors. This conditioning biases H2c and H2d toward the low-share mode.
   - **Fix:**
     - Run the experiment the paper says is missing: for each mode, the smallest allocation (M, or symbols per window) that reaches a target share in each condition. Compare bytes and delay at that operating point.
     - Use an unconditional delay, e.g. a quantile with failures counted as infinite.
     - Present H2c as a stated design consequence, not a tested hypothesis.
3. **The window model changes the application, and the paper does not say so.**
   - The `modes.py` docstring says the application message is "repeated in every slot of its window". One application message per M slots means:
     - C-V2X BSMs run at 1 Hz (M = 10) or 0.25 Hz (M = 40) instead of 10 Hz, each sent 10 or 40 times;
     - SIB1 carries one authenticated message per 1.6 s or 6.4 s.
   - The paper never says this.
   - The chain's share advantage comes mostly from M-fold tag repetition. Its 1-4 s delays on C-V2X are never compared with a BSM latency requirement of about 100 ms.
   - Per-BSM authentication at the native 10 Hz rate is not evaluated at all. M must be a multiple of the certificate cadence, so M >= 5. At M = 5, ML-DSA-44 frag on C-V2X 437 (k = 7 > u = 4) would already be infeasible.
   - **Fix:** state the model explicitly. Add a native-rate configuration (one slot per application message, certificate cadence handled per BSM), and report delay against the application deadline.
4. **The chain implementation has security gaps the paper does not disclose (task c).**
   - **Chain keys come from a public, deterministic seed.**
     - `modes.py` l.225 sets `K[E] = SHA256("seed"||build_seed||e)[:16]`, where `build_seed` is the run index.
     - I recomputed the chain from the build seed alone and injected an *in-time* forged message for Falcon-512 on SIB1 (E = 8, N = 32). `ChainRx` accepted it (`forged message accepted: True`).
     - The same chain keys are also reused across all PQ schemes, all three chain variants, and the T3 "attacker" stream.
     - The measurements are unaffected. But "real cryptography" (Sec. III-C) is not a secure chain.
     - Fix: use a secret random seed per stream, and disclose.
   - **The anchor coverage is incomplete.**
     - The anchor signs `"A"||alg||epoch(16 bit)||commitment||ts`. `ChainRx._anchor` parses `ts` but never checks it.
     - The schedule (T0, interval, disclosure lag d, E) is not signed. The receiver assumes it "exactly", from out of band.
     - Epoch and Merkle batch numbers are 16-bit, and the timestamp is 32-bit ms, so it wraps after about 49.7 days.
     - The frag and Merkle signatures carry no freshness, so old signed messages can be replayed.
     - The paper lists the anchor as "(commitment, timestamp, PQ signature)", which implies a freshness check that does not exist.
   - **There is no symbol authentication, which leaves a cheap pollution DoS.**
     - `FragRx`/`MerkleRx` stop after 3 failed decodes; the anchor is abandoned after 3 bad decodes; the first Merkle path received wins.
     - An injector with a few garbage symbols per message therefore blocks frag_mds, Merkle and the chain anchor.
     - This is in `summary.md` but not in the paper. It is central for a WiSec audience.
   - **What is correct:**
     - The time-safety check is enforced correctly: `ok_time` plus `kidx >= i`, with zero clock error.
     - MAC keys are domain-separated from chain keys.
     - There is no key reuse across epochs within a stream.
     - The 16 B tags and keys give 128-bit symmetric strength, which is acceptable for level 1. State it.
5. **The negative tests do not all test what the paper says (task d).**
   - The counts in Integrity 3 cover the controls.
   - **T4b replay** runs only for the three chain modes (21 rows). The text says the tests run "over 7 PQ schemes and all modes ... replayed frames". Replay is never tested for the frag and Merkle modes, which in fact accept old signed messages.
   - **T6 "forged next-epoch commitment"** flips `nc` inside the MAC input of honest frames. That is the same as a MAC tamper (T1/T2). It does not test whether a continuity commitment can be injected.
   - **T3 "wrong signer"** builds the attacker stream with the victim's `build_seed`, so its chain keys and tags *equal* the victim's. It only shows that anchor signatures are checked.
   - **Missing tests:** key derivability (Major 4), symbol pollution, and receiver clock offset or delay.
   - Fix: correct the description and add these three tests.
6. **"Equal channel budget" does not hold at the stream boundaries, and the horizon is short.**
   - `chain_lead*` gets E = 20 prelude windows: 25 % more slots for N = 80 messages.
   - Merkle gets n trailing windows; the chain gets 1.
   - Bytes on air exceed the per-message allocation for `chain_lead*`. Examples at i.i.d. p = 0.1, share 1.0: ML-DSA-44 SIB1 `chain_lead` 2993 B and Falcon-padded `chain_lead_cont` 3045 B per authenticated message, against 2930 B allocated.
   - With only 4 epochs, boundary effects drive join time (17,376 ms for lead variants, joiner confined to the first epoch) and part of the share.
   - Fix: measure in steady state (longer runs, discard warm-up and flush) or charge the prelude and trailing slots, and state this in Sec. III.
7. **The abstract and conclusion claim more than the evidence supports (task e).**
   - **"Bursts hurt it more than them on average"** (conclusion) is a cross-scheme mean that reverses per scheme:

     | Scheme (SIB1, i.i.d. 0.3 to GE 0.3/b10) | chain | frag_mds |
     |---|---|---|
     | Falcon-512 | -0.112 | -0.168 |
     | MAYO-1 | -0.112 | -0.137 |
     | OV-Is / SNOVA | -0.112 | -0.108 |
     | ML-DSA-44 | -0.112 | +0.40 |

     The frag_mds mean also includes two infeasible SLH-DSA cells (share 0 to 0). Excluding them moves the frag_mds burst delta from -0.076 to -0.084.
   - The abstract's "authenticates a larger share" has no scope (Major 1). "Refuted on bytes" and "authenticates later in every cell" are design consequences (Major 2). "At an equal channel budget" does not hold for the lead variants (Major 6).
   - The limitations omit:
     - the window and repetition model (Major 3);
     - the public key seed, unchecked timestamp, unsigned schedule and missing freshness (Major 4);
     - pollution DoS;
     - the shared loss masks;
     - the Python receivers behind the CPU numbers.
8. **The contribution is thin for WiSec (task f).**
   - Q1 is arithmetic on declared sizes against derived budgets. Q3 is self-declared tautological.
   - Q2 re-implements an EMULSION-style chain against fragmentation on a benign, collision-free synthetic channel.
   - **The smallest addition that would make this a WiSec short paper:**
     - an *active-adversary* experiment on the existing harness and sweep: symbol pollution or injection against frag_mds, Merkle and the chain anchor, plus a receiver clock offset for the chain, reporting share under attack;
     - run at the native message rate (Major 3);
     - together with the minimum-budget comparison (Major 2).
   - Without these, a PQC-migration or vehicular-security workshop is the better fit.

## 4. Minor issues

1. **The cross-check needs its scope and SE rule in the paper.**
   - The 1716 cross-check cells include about 286 lossless (p = 0) cells.
   - 1195 cells use the binomial SE term, and 1145 of them have zero seed SE with a non-zero difference.
   - The paper says "beyond 3 SE" without stating the SE rule. State the rule and exclude p = 0.
2. **"Bytes on air per message are nearly equal across modes" (l.432-433) is not accurate.**
   - The ratio range is 0.706-1.599.
   - OV-Is frag_mds sends 1010 B against 1615 B for the chain, both at share 1.0.
   - Frames do not fill slots (F = 101 B of 293 B).
3. **"For 11 on Remote ID (up to 276 s)" is ambiguous.** 276 s is the maximum over all 24 classes, not over the 11 that meet the deadline.
4. **Seed and key reuse is not stated.**
   - The 20 seeds reuse 1-5 built streams (`nb` = 1 when signing takes over 20 ms), and each scheme uses one cached key pair. So seeds vary only the loss.
   - The CPU and real-time ratios come from at most 5 builds through Python/ctypes.
   - State both.
5. **The late-joiner setup is not described.** The paper does not say there is one join per seed (20 samples), confined to the first epoch.
6. **perrig2005tesla is abstract-only, yet the paper relies on it.**
   - The note says abstract and section headings only, but the paper cites it for the time-safety check that the receiver claims to implement.
   - Read Sec. 3 of RFC 4082 before submission, or cite a source read in full.
7. **ML-DSA-44 is NIST level 2; the other Q2 schemes are level 1.** Say so in Sec. III-C.
8. **"Budget profiles for five channels" counts DNS,** which the paper itself treats as a request-response ceiling reference. Say four broadcast channels plus a reference.

## 5. Verdict

**Major revision.** The three integrity items must be fixed first. Each is small, but each is a statement in the paper that the evidence does not back.

The substantive problems:
- H2a-H2c are mostly consequences of R1, d = 1 window, and an undisclosed M-fold repetition model. The win/loss counting over non-independent cells overstates H2a.
- The "real" chain implementation is forgeable from public parameters, and several protocol-security gaps are undisclosed.

For WiSec, the paper also needs an adversarial evaluation (pollution, injection, clock offset) at the native message rate. If the authors do not want to add it, a PQC-migration or vehicular-security workshop is the more suitable venue.

## 6. The three most important fixes

1. **Replace the win/loss count with effects that respect the design.**
   - Use per-scheme paired CIs, condition-blocked, and count shared-mask groups once.
   - Add the minimum-budget-to-target-share experiment and an unconditional delay.
   - Restate H2a's scope, and present H2b and H2c as design consequences. (Majors 1-2, Integrity 2.)
2. **Disclose, and add a native-rate configuration for, the M-slot repetition model.** BSMs currently run at 1 or 0.25 Hz with each message repeated 10 or 40 times; report delay against the application deadline. (Major 3.)
3. **Fix and disclose the implementation's security gaps, and add the matching tests.**
   - Gaps: chain keys from a public seed (forgery demonstrated), unchecked anchor timestamp, unsigned schedule, no freshness, pollution DoS.
   - Tests: key derivability, pollution, clock offset.
   - Relabel the 427 count. (Majors 4-5, Integrity 3.)

## 7. Round-2 issues: status (checked against the evidence, not against `response.md`)

| Round-2 item | Status in draft 3 |
|---|---|
| I1 certificate cannot hold a PQ issuer | **Closed.** `full_cert_pq` = P + meta + S; Q2's certificate slot is also sized B - (P + S). |
| I2 OSNMA-PKR used as a signature budget | **Closed.** KROOT 158 B for signatures, PKR 76 B for keys. |
| I3 banner commits | **Closed.** All rows are tagged 694ba76 with git_dirty 0, and the code has no diff to HEAD. |
| M1 anchor repetition vs MDS | **Closed as stated.** It is superseded by a new artefact: the R1 over-redundancy (Major 2). |
| M2 anchor wait missing from TTA | **Closed.** Delays are measured from the actual authentication slot. |
| M3 Merkle n selection | **Closed.** All n are reported. |
| M4 PQ issuer / mixed chain | PQ issuer **closed**; the mixed PQ-CA chain remains a stated limitation. |
| M5 OSNMA mapping | **Closed.** |
| M6 V2X channel depth | **Partly open.** C-V2X is now in Q2, but at a 1 Hz / 0.25 Hz repeated-BSM model on a collision-free channel (Majors 3, 8). |
| M7 budget derivations / margins | **Closed.** |
| M8 chain fit row | **Closed.** |
| M9 security analysis | **Partly open.** A properties paragraph was added, but the implementation gaps are undisclosed (Major 4) and the test coverage is overstated (Major 5). |
| m1 SE floor | **Partly open.** It is disclosed in `summary.md`, not in the paper (minor 1). |
| m3 non-uniform burst effect | Closed in the body, but the conclusion reintroduces it as a cross-scheme mean (Major 7). |
| m8, m11, m15 | Stated limitations (acceptable). |
| m13 classical amortization correspondence | **Open** (acknowledged `\todo`, not counted). |
| m2, m4-m7, m9, m10, m12, m14 | Closed. |

`response.md` marks Major 9 as handled through "427/427 negative tests". That count includes 91 controls (Integrity 3), and the tests miss the forgery shown in Major 4. Its "resolved" claim for Major 1 holds only in the narrow sense noted above.
