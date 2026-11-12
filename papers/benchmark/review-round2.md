# Review round 2: benchmark (target venue: IEEE VNC short paper, 4-6 pages + references)

Paper: "Post-Quantum Signatures in Broadcast Budgets: A Cross-Domain Accounting Study" (`paper/main.tex`, `paper/numbers.tex`).

What I checked:
- Evidence: the regenerated `results/summary.md`; `results/raw/*.csv`; `budget-evidence.md`; `experiments/profiles.yaml`.
- Code: `lib/pqsig/accounting.py`, `lib/pqsig/lossform.py`, `experiments/score.py`, `experiments/run_loss.py`, `experiments/summarize.py`.
- Notes and history: the cited notes in `research/lit/notes/`, and the git history.

I did not take `paper/response.md` on trust: every claimed fix below was re-checked. Round-1 `review.md` is kept unchanged.

## 0. Tool check

`python3 tools/check_paper.py benchmark`:

```
40 cited keys, 8 problems
  papers/benchmark/paper/main.tex:14: unresolved placeholder
  papers/benchmark/paper/main.tex:37: unresolved placeholder
  papers/benchmark/paper/main.tex:76: unresolved placeholder
  papers/benchmark/paper/main.tex:160: unresolved placeholder
  papers/benchmark/paper/main.tex:164: unresolved placeholder
  papers/benchmark/paper/main.tex:464: unresolved placeholder
  papers/benchmark/paper/main.tex:512: unresolved placeholder
  papers/benchmark/paper/numbers.tex:9: unresolved placeholder
```

All 40 keys resolve. main.tex lines 14 and 37 and numbers.tex line 9 are the macro definitions and the draft banner. The PDF is 6 pages and the references start on page 5, so the length fits a VNC short paper.

**Known placeholders, listed once and not counted below.**
- `\todo`: FN-DSA standard (l.76), full text of hyoung2026post/fall2025sok (l.160), NIST additional-signature status (l.164, new), Cortex-M timings (l.464), artifact URL (l.512).
- `TODO-RESULT`: `\RunCPU`, `\HdrRID`, `\HdrSIB`, `\HdrOS`, `\HdrCV`, `\PerDNS`, `\CertMetaCV`, `\DarziOTARepro`, `\DarziTenRepro`, `\JunqueraKeyRepro`, `\YoshizawaRepro`, `\GoertzenRepro`, `\ChenRepro`.
- Also the author block and the provisional-numbers banner.

## Verification of the claimed fixes (a)-(e)

**(a) Declared sizes are scored. Verified.**
- `score.py` passes `sig_declared` into `accounting.score`.
- `sizes_declared.csv` has Falcon-512 at 752 (observed 663) and Falcon-1024 at 1462 (observed 1280). These match liboqs `length_signature`.
- `run_loss.py` also reads `sig_declared`, so Falcon-512 enters Q2 as k = ceil(752/293) = 3.

**(b) Budgets against `budget-evidence.md`. Mostly verified, with one category error.**
- Remote ID 201 B (RFC 9575 cap), SIB1 293 B (372 - 79), C-V2X 437 to 373 B, J3161 2481 to 2414 B, and DNS 1232 B all match the evidence. The derived values are marked, and the ceiling-based verdicts are labelled as such in Table I, the Method text, the abstract and the Conclusion.
- Table II's column headers do not carry the "ceiling-based" marker (minor 5).
- OSNMA-PKR is used as a *signature* budget. The evidence does not support this (integrity 2).
- The C-V2X 437 derivation is not a guaranteed upper bound (major 7).

**(c) Closed forms. The algebra is correct, and "equal channel" holds in slot count. Two modelling choices make the chain comparison unsound (majors 1 and 2).**
- I re-derived the forms (frag_rep (1-p^r)^k; frag_mds P[Bin(M,q) >= k]; chain (1-p^t)(1-p^{tw})(1-p^{r_a})^{k_a}; merkle_rep and merkle_mds). They match the code and the CSV values. Examples: ML-DSA-44, M = 12, p = 0.1 gives chain 0.99^9 = 0.914, frag_rep 0.9^9 = 0.387, frag_mds 0.974.
- The events use disjoint slots, so the product form is valid under i.i.d. loss.
- Every scheme gets M slots per message. Some leave slots idle, though: frag_rep leaves M mod k, and the chain leaves E·a_s - r_a·k_a. So the docstring's "all reserved slots are used" is not accurate (minor 6).
- Simulation check: the maximum |sim - closed| = 0.0121 is confirmed. The "3 of 240 beyond 3 SE" figure, however, depends on an undisclosed floor of 1e-4 on the SE (`summarize.py` l.201). Without the floor, 104 of 240 cells exceed 3 SE, mostly near-deterministic cells (minor 1).

**(d) Merkle and erasure-coded baselines.**
- The *share* side is fair or generous to the baselines: the best n is chosen per cell, and the signature is sent causally after the batch, in the next batch's spare slots.
- The *latency* side is not fair (major 3). The batch size is picked to maximise share, with ties going to n = 16. This reports TTA95 of 216-294 slots, while n = 4 reaches the same share in 72-90 slots.
- The per-message Merkle path (log2 n hashes) is not stated (minor 7).
- frag_mds is a fair ideal-MDS baseline.

**(e) Macro spot-check.** I checked 90+ macros against `summary.md` and the CSVs (`sizes_declared.csv`, `loss_closed.csv`, `loss_simcheck.csv`, `loss_ge.csv`). They cover:
- the scheme-set counts and all size and timing macros;
- every profile macro and the Table I rows;
- every cell of `\TabQOneRows`, recounted from the per-family table;
- the fit min/max, the chain pair count, and the message counts, TTFAs and join times;
- the Falcon conflict values, the baseline counts, and all Q2 parameters;
- k values; region counts 55/54/78, 30/30, 25/30 and 0/18; every cell of `\TabQTwoRows`, recomputed from `loss_closed.csv`; the GE values and mean drops;
- every row of `\TabQThreeRows`, and the UOV counts 0/6 and 2/12.

No macro differs from its source. The problems below are in what the numbers are claimed to mean.

## 1. Integrity (blocks submission)

1. **"Falcon-512 ... fits one [J3161 message] even with a full certificate (1754 B peak)" and "certificate handling fits ... under the J3161 ceiling (4 classes)" are not backed as PQ certificates.**
   - The paper defines f = 105 B as "metadata and issuer signature" (Sec. III-C). It is derived as 1002 - 897 from abrar2026deployment's Falcon-512 certificate.
   - 105 B cannot hold any PQ issuer signature from the families that matter. A Falcon-512 issuer signature is 752 B declared (666 B padded). Abrar's 1002 B certificate must therefore carry a classical (about 64 B) issuer signature, or it is incomplete.
   - So the scored "full certificate" is a PQ subject key signed by a non-PQ issuer. That is not a post-quantum certificate chain, and the Limitations even say mixed chains are "not modelled".
   - With a same-scheme issuer (S + P + S + about 41 B of metadata), Falcon-512 needs about 2442 B, which exceeds 2414 B. The J3161 count drops from 4 to 3; Falcon-padded-512, MAYO-1 and SNOVA_24_5_4 still fit.
   - Fix: state that f implies a classical issuer, or model a PQ issuer, and re-score.
2. **The OSNMA-PKR 204 B profile is used as a signature budget. The evidence says it is not one.**
   - `budget-evidence.md` (OSNMA (b)/(c)) says the 1632 bits are DSM-PKR cryptographic material, "shared with a 1024-bit Merkle signature and public key". DSM-PKR delivers the *public key*; signatures travel in DSM-KROOT.
   - Every PKR signature result is therefore unsupported: the PKR column of Table II (7 full-signature fits), "Falcon-512 takes 4 messages and 1740 s on the PKR variant", and the chain joins of 6210 s and 960 s "on OSNMA-PKR".
   - Fix: score signatures only against KROOT (158 B, derived). Score public keys against the PKR key space, which is about 608 bit = 76 B after the 1024-bit Merkle proof, derived from the same source figures. That check is informative: SLH-DSA (32 B), CROSS (54-77 B) and MQOM (60 B) keys fit, while none of the small-signature families' keys do.
3. **The provenance in the draft banner is wrong.**
   - The banner says sizes, scoring and loss were redone at commits `6ca9403, 408d1b4`.
   - `lossform.py` and `run_loss.py` first appear in `3230670`, which comes after `6ca9403`, the commit the loss CSVs are tagged with.
   - The stateful rows and the `score.py`/`summarize.py` changes that produced `scoring_all_levels.csv` were committed in `1b09a13`, after `408d1b4`.
   - Neither cited commit contains the code that produced the numbers. The "traceable to commit" claim does not hold.
   - Fix: regenerate everything from a clean, committed tree and tag that commit.

## 2. Summary and novelty

The paper derives source-backed authentication budgets for Remote ID, SIB1, OSNMA, C-V2X (two ceilings) and DNS. It accounts four modes against them for 64 deduplicated liboqs size classes plus LMS/XMSS. It compares a TESLA chain, fragmentation and Merkle batching on a SIB1 slot model at equal slot use, using closed forms.

The rewrite is much more careful than round 1. Declared sizes, deduplication, the separation of ceiling and budget, the C-V2X conflict explanation, the closed forms and the amortization baselines are all real improvements.

The delta is still thin for VNC. The vehicular part is static byte accounting against two C-V2X ceilings: the only loss analysis is on 5G SIB1, and nothing is evaluated on a V2X channel. The Q2 conclusions that matter most (the chain loses for ML-DSA-44; batching takes much longer) are artifacts of the modelling choices in majors 1-3. A short paper is a plausible fit only after these are fixed and the evaluation includes a V2X channel.

## 3. Major issues

1. **The chain's anchor is repetition-coded while its competitors are erasure-coded, and its slot split ignores M. This produces the "chain loses for ML-DSA-44" result.**
   - The anchor gets a_s = ceil(2k_a/E) slots per message whatever M is. At M = 48 the chain sends 47 copies of a 32 B tag and 1 anchor slot.
   - The k_a = 9 anchor fragments are repeated (r_a = 2), while frag_mds and merkle_mds get ideal MDS codes.
   - If the anchor is erasure-coded over the *same* 20 reserved slots per epoch, the result flips. At M = 12 the chain's share is 0.995 at p = 0.3 and 1.000 at p = 0.1. frag_mds gets 0.493 and 0.974. My computation uses the paper's own closed form with P[Bin(20,q) >= 9] replacing (1 - p^2)^9.
   - The abstract's "never for ML-DSA-44" and the conclusion's "it loses for ML-DSA-44" do not survive a symmetric comparison.
   - The chain also uses 32 B of each 293 B tag slot. The unused 261 B could carry anchor symbols at no channel cost.
   - Fix: add a chain_mds variant. Optimise (or at least sweep) the chain's split between tags and anchor, the same way n is chosen for Merkle. Re-derive the region counts.
2. **The chain's TTA95 leaves out the wait for the anchor.**
   - `tta95` for the chain is M + u·M/t: it only counts the key wait, even though verification requires the epoch's anchor.
   - In the simulator's own layout, the anchor fragments arrive spread over the epoch's reserved slots. Messages early in an epoch wait for them.
   - Re-simulating that layout with the anchor wait included gives Falcon-512 (k_a = 3) at M = 12 a TTA95 of 36 slots at p = 0.1 and 72 slots at p = 0.3. Table III reports 14.2 and 15.3. MAYO-2 (k_a = 1) is unaffected.
   - The text's "the chain needs about 14-15 slots" is therefore understated by up to about 5x whenever k_a > 1.
   - Fix: include the anchor term in TTA, or send each anchor one epoch ahead (and say so), then re-run.
3. **The Merkle-batch latency is selected unfavourably.**
   - Table III and the text ("TTA95 ... 216-294 slots", and the abstract's "takes much longer") use the batch size that maximises share, with ties broken toward n = 16.
   - n = 4 gives the same share (1.000 within the 0.005 tolerance) much faster: 78 instead of 252 slots (Falcon-512, p = 0.1), 72 instead of 216 (MAYO-2), 76.8 instead of 264 (ML-DSA-44, p = 0.1).
   - Fix: report the (share, TTA95) Pareto front over n, or pick n by minimum TTA subject to a share target. State the per-message Merkle path cost.
4. **Certificate accounting (integrity 1).** Beyond fixing the claim itself, the full_cert mode should include a PQ issuer. The mixed PQ-CA/classical-subscriber chain that chen2026pseudonym recommends should also be modelled, because it is the realistic V2X option. With a PQ issuer, the J3161 certificate fits and the Falcon-512 "consistent with both papers" story have to be redone.
5. **The OSNMA profile mapping (integrity 2).** Re-scoring has to separate key delivery (PKR) from the signature (KROOT). The "two variants" framing in Table I should become "PKR = key, KROOT = signature".
6. **The paper does not yet fit VNC, and its contribution is thin.**
   - The only channel-level analysis is on 5G SIB1.
   - C-V2X appears only as two static ceilings, with no PC5 Mode 4 / semi-persistent scheduling (SPS) behaviour, no congestion, no packet delivery ratio (PDR), and no cost of the every-5th-BSM certificate under loss. abrar2026deployment already shows that Falcon-512 fits but fails the 90% PDR target outside LOS level of service A. That is the question a VNC audience cares about, and the paper does not engage with it.
   - Remote ID, OSNMA and DNS take space that a vehicular venue will not value.
   - Fix: run Q2 on a C-V2X profile (100 ms BSM period, 373/2414 B budgets, digest/certificate pattern, the C-V2X loss levels from abrar2026deployment). Shrink the non-vehicular profiles to one summary table. Alternatively, retarget to a venue that values the cross-domain angle.
7. **The budget derivations are inconsistent, and the verdicts sit on razor-thin margins.**
   - cv2x_437 subtracts a 40 B frame overhead that the source may not include in 437 B (`budget-evidence.md`: "does not say"). It does not subtract the 39 B BSM core that cv2x_j3161 does subtract.
   - So "373 B is an upper bound" is not guaranteed: if the 40 B is outside 437, the budget is 413 - BSM, which is 374 B with abrar's 39 B core.
   - Verdicts change on a few bytes. ML-DSA-44 misses J3161 by 6 B (2420 against 2414, a derived budget), and the UOV hybrid misses KROOT by 2 B (160 against "about 158").
   - Fix: apply one subtraction rule to both C-V2X profiles, and report the margin (B - x) next to each fit.
8. **The chain row of Table II is empty of information, yet the text leans on it.**
   - The chain "fits" 24/24 in every profile because fit is defined by its 32 B steady traffic.
   - The abstract and conclusion turn this into "makes every scheme's per-message cost fit", while the real cost is the join time: 4.6 s for SLH-DSA-128F on C-V2X 437, and many hours for CROSS, MQOM and SLH-DSA on OSNMA (up to 5.2·10^4 s).
   - Fix: drop the chain from the fit table, and judge it by its join time against a stated per-profile join deadline.
9. **There is still no security analysis (round-1 major 5 remains open), and V2X makes this worse.**
   - The chain gives no non-repudiation. V2X misbehaviour reporting and revocation in SCMS (brecht2018security, cited) depend on signed, attributable BSMs.
   - The chain also needs loose time synchronisation, which is an attack surface in vehicular settings.
   - Presenting the chain as a byte-for-byte alternative to signatures for C-V2X without saying this is misleading for a VNC audience.
   - Fix: add at least a one-paragraph property comparison (non-repudiation, time sync, hybrid separability) and state that the chain is not a drop-in for V2X BSM signing.

## 4. Minor issues

1. The simulation check's "3 of 240 cells beyond 3 SE" uses an SE floor of 1e-4. Without it, 104 of 240 exceed 3 SE, mostly in near-deterministic cells. State the floor or use an absolute tolerance. The simulator shares the model's assumptions, so call it a code check, not a validation.
2. The GE figures in the text (chain 0.998 to 0.874, frag_mds 1.000 to 0.853, merkle_mds 0.989 to 0.882) are for **Falcon-padded-512 with n = 8**, while Table III uses Falcon-512 with the best n. Name the signature and n.
3. "Burst loss lowers the share ... for the erasure-coded schemes" is not uniform. For ML-DSA-44 at p = 0.3, bursts *raise* frag_mds from 0.493 to 0.605. The averaged drops mix very different cells; report them per signature.
4. In Fig. 2, four of the six panels are flat at 1.0. Use the space for ML-DSA-44 and Falcon across several M, or for a TTA panel.
5. The Table II headers (CV437, J3161, DNS) do not carry the ceiling-based marker used in Table I and `summary.md`.
6. The `lossform.py` docstring says "all reserved slots are used". In fact E·a_s - r_a·k_a reserved slots stay idle (2 per epoch for Falcon-512 and ML-DSA-44), and frag_rep idles M mod k.
7. The per-message Merkle authentication path (log2 n hashes) is not mentioned in the model.
8. The LMS row uses H = 5, which allows 32 signatures per key, or 3.2 s of BSMs at 10 Hz. "Only LMS fits ... J3161" is then operationally empty. Add H = 15/20 rows (same formula: 1612/1772 B) or say so in the text.
9. The darzi2026a "reproduction" divides darzi's own crypto-byte totals by 293 B. That is a consistency check, not a reproduction from liboqs sizes; call it one.
10. The `summary.md` headline says "All runs are smoke tests (machine: cloud-smoke)", but the run tags include machine `vm`.
11. Remote ID uses the 3 s static-message period. The 1 s dynamic-wrapper period from the same RFC would cut TTFAs threefold (ML-DSA-44: 36 s to 12 s). Justify the choice.
12. Q3 is acknowledged as near-tautological, yet it takes a table and a line of the abstract in a 6-page paper. Cut it to one sentence.
13. The four classical amortization papers and SP 800-208 were read as abstracts or titles only. The Merkle and erasure-coded baselines should name their correspondence to them (Wong-Lam tree signing, SAIDA-style erasure-coded amortization).
14. The OSNMA frames use fractional payloads (12.75 B and 9.875 B per block). That is fine for counting, but state that frame counts come from the bit capacity.
15. The abstract still states provisional smoke-test findings as results (round-1 minor 14, open as a limitation).

## 5. Round-1 issues: status

| Round-1 item | Status |
|---|---|
| Integrity 1.1 (observed Falcon size) | Closed |
| Integrity 1.2 (C-V2X budget) | Closed in labelling; residual derivation problem moved to major 7 |
| M1 (fragmented mode) | Closed; new chain-row problem (major 8) |
| M2 (closed form, redundancy) | Closed as stated; new chain-coding and TTA flaws (majors 1-2) |
| M3 (equal channel, baselines) | Partly open: equal slot count done, but chain allocation and Merkle latency are unfair (majors 1, 3) |
| M4 (oqs anchor) | Closed |
| M5 (security, chain continuity) | Open (major 9) |
| M6 (variant inflation) | Closed |
| M7 (security level) | Closed for Q1; Q2 compares level 1 with level 2 (stated) |
| M8 (budgets) | Partly open: OSNMA-PKR (integrity 2), C-V2X subtraction (major 7) |
| M9 (sig_cert strawman) | Partly open: new non-PQ issuer problem (integrity 1, major 4) |
| M10 (Q3 method) | Closed (now acknowledged as tautological; minor 12) |
| M11 (related work) | Mostly closed; NIST status cite still `\todo`; classical papers abstract-level only (minor 13) |
| M12 (contribution) | Open, re-judged against VNC (major 6) |
| Minors 1-13, 15 | Closed |
| Minor 14 (provisional numbers in abstract) | Open as a stated limitation |

## 6. Verdict

**Major revision** for IEEE VNC (short paper).

The three integrity issues must be fixed before any submission: a certificate overhead that cannot hold a PQ issuer signature, signatures scored against the OSNMA key-delivery budget, and commit hashes that do not contain the producing code.

The Q2 headline conclusions also have to be re-derived after a symmetric chain model (erasure-coded anchor, optimised allocation, anchor wait in TTA) and a Pareto-reported Merkle latency.

For VNC specifically, the paper needs a C-V2X channel-level evaluation and a statement of why the chain cannot replace signed BSMs. If the authors want to keep the cross-domain framing rather than adding V2X depth, a security or PQ-migration workshop would suit it better than VNC.
