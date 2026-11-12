# Review: benchmark (target venue: IEEE CNS)

Paper: "Which Post-Quantum Signature Modes Fit Broadcast Budgets? A Cross-Domain Scoring of
Authentication Modes for Handshake-Free Cyber-Physical Broadcasts" (`paper/main.tex`).
Evidence used: `gap.md`, `results/summary.md`, `results/raw/*.csv`, plus the code that produced
them (`lib/pqsig/accounting.py`, `lib/pqsig/lossmodel.py`, `lib/pqsig/oqs_bench.c`,
`experiments/profiles.yaml`) and the cited notes in `research/lit/notes/`. This paper has no
`design.md` or `model/results.md`.

## 0. Tool check

`python3 tools/check_paper.py benchmark`:

```
34 cited keys, 7 problems
  papers/benchmark/paper/main.tex:14: unresolved placeholder
  papers/benchmark/paper/main.tex:36: unresolved placeholder
  papers/benchmark/paper/main.tex:78: unresolved placeholder
  papers/benchmark/paper/main.tex:175: unresolved placeholder
  papers/benchmark/paper/main.tex:442: unresolved placeholder
  papers/benchmark/paper/main.tex:501: unresolved placeholder
  papers/benchmark/paper/numbers.tex:9: unresolved placeholder
```

All 34 cited keys resolve. Lines 14 and 36 (main.tex) and 9 (numbers.tex) are the macro
definitions and the draft banner, not open items in the text.

**Known placeholders, listed once and not counted below.**
- `\todo`: FN-DSA standard citation (l.78); full-text check of hyoung2026post and fall2025sok (l.175); Cortex-M timings for UOV/SNOVA/MAYO (l.442); artifact URL (l.501).
- `TODO-RESULT`: `\RunCPU`, `\HdrCV`, `\HdrSIB`, `\HdrDNS`, `\JunqueraBlocksRepro`, `\DarziFragRepro`, `\DarziTenRepro`, `\YoshizawaRepro`, `\GoertzenRepro`.
- Also: the author block placeholder, and the draft banner saying every number is a provisional cloud smoke test.

**Number spot-check.** I checked 70+ macros in `numbers.tex` against `summary.md` and the raw CSVs, and they all match. The checked values are:
- Every size macro in Part A, and every timing macro in Part A (sign/verify p99, the Falcon-1024 keygen, the SLH-DSA 1.282 s median).
- The Q1 totals 104/97/0 of 1105. I recounted these from `scoring.csv`: full 104, fragmented 104, chain 97, hybrid 89, sig_cert 0.
- The per-profile fits 23/17/13/21/30. I recounted these from the scheme lists, and they sum to 104.
- Every cell of `\TabQOneRows`, after mapping the column reordering.
- Every Q2 cell macro, the 22/24/24 of 24 counts, the 110/142/142 of 144 sweep counts, and the deadlines 4160 ms and 10 880 ms.
- Every row of `\TabQThreeRows`. I re-derived the misfit fractions from the Q1 table, and the over-3 ms fractions from the per-scheme p99s and medians.

No macro mismatches. One problem with an evidence file: `summary.md` Q2 lists "slot 160 ms (SIB1 period)" under "Assumed, not cited". The paper cites darzi2026a for it, and the darzi2026a note does back it ("SIB1 every 160 ms"). So `summary.md` is wrong here, not the paper (minor 7).

## 1. Integrity (blocks submission)

1. **"Falcon-512 signatures are at most 663 B (666 B padded)" (Sec. V-A) and "Let s be the maximum signature size ... measured" (Sec. III-B) are not supported.**
   - `oqs_bench.c` records `sig_bytes_max` as the largest length seen over 1000 signatures of one fixed 64-byte message. It is not the scheme's maximum.
   - The liboqs 0.16.0 checkout used for the runs defines `OQS_SIG_falcon_512_length_signature 752` and `OQS_SIG_falcon_1024_length_signature 1462`. The CSV value for Falcon-1024 is 1280.
   - The wording "at most" and "maximum signature size" therefore contradicts the library the paper cites as its source.
   - The Q2 "oqs" scenarios also use the observed 663 B.
   - Fix: use `length_signature`, or the padded variants, as s. Re-score, and reword.
2. **Table I and Sec. III-A describe the C-V2X 437 B as an "authentication budget per message". The evidence says otherwise.**
   - The cited note (twardokus2024when) gives 437 B as the *maximum C-V2X payload* on a 10 MHz channel. It gives the IEEE 1609.2 SPDU as at most 226 B (implicit certificate) or 330 B (explicit certificate).
   - The project's own `profiles.yaml` says "budget is the whole payload, not auth-only".
   - The paper never discloses this. It presents C-V2X fit counts (23 full-signature fits) as fits to an authentication budget, which overstates them.
   - Fix: state that B is the whole payload for C-V2X and that the C-V2X counts are upper bounds, or derive an authentication-only budget from the cited SPDU figures.

## 2. Summary and novelty

The paper scores five authentication modes (full, sig+cert, fragmented, PQ-anchored TESLA chain, Ed25519 hybrid) for 221 liboqs parameter sets against five byte budgets (C-V2X, Remote ID, OSNMA, SIB1, DNS). It adds an i.i.d. loss model comparing chain and fragmentation, and an x86 size-versus-timing comparison. Findings: only UOV, SNOVA, MAYO-2 and two Falcon sets fit; same-scheme certificates never fit; the chain is cheaper but the comparison is labelled "inconclusive"; and size rather than timing binds on x86.

The delta over the baselines is thin, and not enough for CNS:
- Q1 is arithmetic on published sizes, and most of it can be read off spec tables.
- Q2 reduces exactly to two closed-form expressions (major 2), and its "inconclusive" label follows from assumed parameters.
- Q3 is near-tautological on a cloud VM.
- The paper offers no new mechanism, no security analysis, no constrained-hardware measurement, and no reproduced baseline (all four baselines are `TODO-RESULT`).
- The closest prior work (hyoung2026post) was read as an abstract only.

## 3. Major issues

1. **The Q1 "fragmented" mode adds nothing, and the mode definitions do not agree with each other.**
   - With h = 0 and "fits iff total bytes ≤ B", fragmented equals full in every one of the 1105 pairs (104 = 104; Table II rows are identical).
   - B is a per-message budget, so fragmentation *across messages* (the 13/34 SIB1 fragments of darzi2026a, ARRF in goertzen2022post) is never modelled in Q1. Q2 then uses a different, multi-slot definition.
   - In Remote ID (F = 23) and OSNMA (F = 13), "full" already spans several frames, so full and fragmented collapse into one mode.
   - The chain fit rule (anchor + 20 B must fit one budget) is what makes "chain fits fewer than full" (97 < 104). That is an artifact of the rule, since an anchor sent once per epoch can itself be fragmented.
   - Fix: define fragmentation over m messages, with a per-message budget and a reassembly/latency cost. Let the chain anchor be fragmented the same way. Use one definition in both Q1 and Q2.
2. **The Q2 result is a closed form, and the "unexplained" crossover is caused by unequal redundancy.**
   - The simulated shares match closed forms exactly. Fragmented: (1 - p^r)^k (for example 0.91^13 = 0.293 and 0.91^34 = 0.040 at 30% loss). Chain: (1 - p)(1 - p^a) (0.9 x 0.99 = 0.891 and 0.7 x 0.91 = 0.637).
   - So fragments get r = 2 repetitions while each chain message frame is sent once. That alone explains why fragmentation wins at 5% loss with k = 13. In `lossmodel.py`, losing a disclosed key does not cause failure unless every later key before the deadline is also lost, so the paper's suggested cause ("disclosed key or anchor lost") is contradicted by its own model.
   - The ">2 std over seeds" test only measures Monte-Carlo noise around a deterministic quantity. It is not evidence for or against a conclusion, and calling the outcome "inconclusive" misreads what it shows.
   - Fix: present the closed forms. Compare at equal redundancy (repeat chain frames r times, or give fragments the same budget of FEC/repetition). Report the parameter region (p, k, r, a) where each mode wins, instead of cell counts.
3. **Q2 does not compare at equal channel use, and its baseline is a strawman.**
   - A fragmented message occupies r·k slots (26 or 68 slots, i.e. 4.2-10.9 s), while the chain sends one message per slot. "Bytes per verified message" hides that the fragmented scheme cannot sustain the chain's message rate at all.
   - Sign-every-message is not the baseline a broadcast-authentication reviewer expects. The standard competitors are signature amortization (one signature over a batch or Merkle tree, erasure-coded signature amortization, hash chaining). SIB1 content is also largely static between changes.
   - Fix: fix the message rate and the slot capacity for both schemes. Add at least one amortized-signature baseline.
4. **The "oqs" anchor does not fit the profile it is simulated in.**
   - In oqs13/oqs34 the anchor is MAYO-1 + 20 = 474 B (`lossmodel.csv`), which exceeds the 372 B SIB1 budget. It is nevertheless received atomically in one slot.
   - This contradicts Q1, where MAYO-1 does not fit SIB1 and only MAYO-2 (186 B) does.
   - k is also reused from darzi2026a (663 B in 13 fragments of about 51 B each), while Q1 uses F = 372 B for SIB1.
   - Fix: use MAYO-2, or fragment the anchor. Recompute k from the profile payload. Give the anchor its own slot in the loss process: it is currently drawn from a separate random stream and occupies no slot.
5. **The chain model is pessimistic in one direction and optimistic in another, and security is absent.**
   - Pessimistic: each epoch is treated as independent, so losing both anchors loses the epoch, even though a TESLA receiver that already holds an authenticated chain or commitment would not need it.
   - Optimistic: the cost and security of loose time synchronization (perrig2005tesla, darzi2026a), cold-start or join latency, and the loss of non-repudiation are ignored.
   - For a security venue, comparing modes with different trust models (no non-repudiation, time-sync attacks, hybrid downgrade or stripping) on bytes alone is not enough. The paper itself lists "security of the modes is not analysed".
   - Fix: add a threat model and a per-mode security-property comparison. Model chain continuity across epochs and the join latency.
6. **Parameter-set counts are inflated by API variants.**
   - 156 of the 221 "parameter sets" are SLH-DSA pure and prehash variants with only 6 distinct signature sizes (12 parameter sets).
   - The UOV pkc/skc variants and the SNOVA SHAKE/esk variants also repeat sizes.
   - So "104 of 1105 pairs", the family fractions in Table III, and the SLH-DSA tie in Q3 are all weighted by liboqs API variants.
   - Fix: deduplicate to distinct parameter sets, or to distinct (sig, pk) pairs, and report counts per NIST security level.
7. **Security level is not controlled.**
   - The counts mix NIST levels 1, 3 and 5 (OV-V, MAYO-5, SLH-256 alongside level-1 sets).
   - Q2 pairs a MAYO-1 anchor against FN-DSA/ML-DSA without stating the levels.
   - Fix: stratify Q1 to Q3 by level, and compare like with like.
8. **Several budgets are questionable or not like-for-like, and the related work that contradicts them is not discussed.**
   - (a) C-V2X: see integrity 1.2. Also, abrar2026deployment (read in full) finds Falcon-512 *feasible* within the J3161 transport block, and chen2025hybrid/chen2026pseudonym report Falcon-512 fitting a 1400 B WSM. Q1 reports Falcon 0/4 for C-V2X. The paper must reconcile these results.
   - (b) OSNMA: the 16 DSM blocks belong to the DSM-PKR/KROOT channel that carries keys. They are not a per-message authentication budget; per-message authentication in OSNMA uses 40-bit TESLA tags. Of the 1664 bits, 1632 are crypto material (204 B, not 208 B).
   - (c) DNS is request-response, not handshake-free broadcast, which undercuts the paper's own framing. 1232 B is also a recommendation, not a hard limit.
   - (d) SIB1: 372 B is the SIB1 maximum, not the space left for authentication.
   - Fix: give an authentication-available budget per profile, with the header accounting justified, or drop or re-frame DNS.
9. **The sig_cert result (0/1105) is a strawman.**
   - The mode attaches the full public key plus a same-scheme issuer signature to *every* message.
   - V2X practice sends a certificate digest most of the time and the full certificate periodically. twardokus2024when, which the paper cites, gives a 500 ms certificate cycle and 172 B certificate-only SPDUs. chen2026pseudonym recommends a PQ CA with a classical end entity.
   - Fix: model digest plus periodic certificate (amortized bytes), and mixed-scheme chains.
10. **The Q3 method does not support the conclusion "size, not timing, is binding".**
    - (a) The two fractions have different denominators: (set, profile) pairs for size, sets for timing.
    - (b) The 3 ms deadline comes from IEC 62351-6/61850 grid protection (hussain2026a), but none of the five profiles is a grid channel. The 100 ms BSM period is then applied to every family regardless of profile.
    - (c) Single-operation latency ignores receiver verification throughput (V2X receivers verify many messages per second) and ignores keygen (Falcon keygen of 6-18 ms matters for pseudonym rotation).
    - (d) On a cloud x86 VM almost everything is sub-millisecond, so the result is close to tautological.
    - (e) "UOV parameter set choice is timing-constrained" is overstated. Only the pkc-skc variants miss the deadline, and those trade storage for speed; a designer picks another UOV variant.
    - Fix: tie each deadline and throughput requirement to a profile, measure on the target class of MCU, or narrow the claim.
11. **Related work is missing.**
    - Classical broadcast-authentication amortization is missing, and it supplies the baselines Q2 should face: TESLA/EMSS (Perrig et al., IEEE S&P 2000), SAIDA (Park, Chong and Siegel), Merkle-tree batch signing (Wong and Lam), BiBa/HORS (Reyzin and Reyzin).
    - eaton2024provably (PQ butterfly key expansion for SCMS) is in the notes but not cited.
    - Stateful LMS/XMSS are excluded, although junquera2023assessment evaluates them for OSNMA. They are standardized and suit the single-signer broadcasters studied here.
    - The paper does not say that UOV, MAYO, SNOVA, CROSS and MQOM (all its "fitting" families except Falcon) are NIST additional-signature candidates, not standards. The practical conclusions rest on these schemes.
    - Fix: add and position this work, and state the maturity of each family.
12. **The contribution is not enough for the CNS main track.**
    - The novelty claim is "cross-domain, mode-level scoring", but the scoring is simple accounting.
    - The one nontrivial analysis (Q2) is reducible to closed form and labelled inconclusive.
    - Q3 does not cover constrained devices.
    - No baseline is reproduced, so nothing anchors the method against prior results.
    - Fix: add at least two of the following: a security analysis of the modes; MCU measurements; a new or optimized mode, such as amortized or erasure-coded PQ signatures per profile; reproduced baselines (darzi2026a, junquera2023assessment).

## 4. Minor issues

1. The hybrid total (89/1105) is in `scoring.csv` but not reported in the text.
2. Sec. III-A (l.194) shows `\HdrCV` for all three profiles. Use `\HdrCV`, `\HdrSIB` and `\HdrDNS`.
3. The OSNMA budget should be 204 B of crypto material (1632 bit), or the paper should justify counting 1664 bit.
4. The hybrid partner is Ed25519, but V2X (IEEE 1609.2) uses ECDSA-P256. Use the deployed partner per profile, and state raw (64 B) versus DER (72 B) encoding.
5. Classical timings go through Python (for example, Ed25519 verify at 83 µs against ML-DSA-44 at 21 µs). Measure in C, or drop the classical timing row.
6. The p95 is taken over verified messages only. Report a percentile over all messages, with failures counted as missing the deadline.
7. `summary.md` labels the 160 ms slot as "assumed, not cited", although darzi2026a backs it. Correct the evidence file.
8. The 3 ms attribution: the limit comes from the IEC 62351-6 text as quoted in hussain2026a, not from an IEC 61869-9 requirement. Say so (l.145-146, l.276-277).
9. The chain's deadline is set to r·k, which is inherited from the fragmented competitor. Use an application deadline for both modes.
10. The sweep is one-at-a-time, with no interactions and no variation of k, and loss is i.i.d. only. Report a 2-D region, add burst loss (Gilbert-Elliott), or narrow the claims.
11. The fragment header for Remote ID is set to 0 because "the 2 B are already excluded". Say this in the text.
12. Sizes and timings come from one 64 B message on one machine. State that per-message variance is not sampled.
13. The title has two subtitles and is too long for IEEEtran; shorten it.
14. The abstract presents the findings as results while the data is a smoke test. Once publication runs exist, make sure the abstract matches the final numbers rather than these ones.
15. Fig. 1 is on a log scale with one dot per variant, so the 156 SLH-DSA points visually dominate. Deduplicate (see major 6).

## 5. Verdict

**Reject** for IEEE CNS (main track) in its current form.

Integrity issues 1.1 and 1.2 must be fixed before any submission. Beyond them, the Q1 modes collapse into each other, and the Q2 model compares unequal redundancy and channel use, includes an anchor that does not fit its own profile, and reduces to closed form. There is also no security analysis, which matters at a security venue. The novelty over darzi2026a, junquera2023assessment and yoshizawa2026a is not enough for a main-track security conference.

A better venue would be a workshop or short-paper track on applied PQ migration or vehicular/CPS security, for example a CNS-co-located workshop, IEEE VNC, or escar. It would need to be framed as a measurement and accounting study, with the fixes to the byte accounting (majors 1, 6, 9) and the closed-form, equal-redundancy loss analysis (majors 2-4). A full-venue resubmission would also need majors 5, 8, 10 and 12: a security analysis, MCU measurements, and reproduced baselines.
