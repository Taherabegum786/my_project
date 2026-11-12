# Response to review (round 1), papers/benchmark

Venue changed to IEEE VNC short paper (IEEEtran conference, 4-6 pages + references). One line per review comment.

- Integrity 1.1 (Falcon "at most 663 B", observed max as s): fixed. S is now the declared liboqs `length_signature` (Falcon-512 752 B, Falcon-1024 1462 B); the observed 663 B is mentioned only as the contrast; the scoring and Q2 use the declared sizes.
- Integrity 1.2 (C-V2X 437 B is a payload ceiling): fixed. Table I separates ceiling and auth budget; C-V2X and DNS are labelled ceiling-based upper bounds (373 B and 2414 B after stated overheads), with derivations from budget-evidence.md.
- Major 1 (fragmented mode collapses into full; inconsistent definitions): fixed. Fragmentation is no longer a mode but the cost (messages m, TTFA) of any object over B; the chain anchor is fragmented the same way; Q2 uses k = ceil(S/C) with the same C = 293 B as the SIB1 budget.
- Major 2 (Q2 is closed form; unequal redundancy; >2 std test): fixed. Closed forms are given; the comparison is at equal channel use; results are reported as regions over (signature, M, loss); the wrong causal explanation and the std test are removed.
- Major 3 (no equal channel use; strawman baseline): fixed. Every scheme gets M slots per message; erasure-coded fragmentation and Merkle-batch amortized signing (repeated and erasure-coded) are added as baselines.
- Major 4 (oqs anchor 474 B does not fit SIB1; k reused; anchor occupies no slot): fixed. Anchor is S + 20 B fragmented into k_a slots reserved within the window; k recomputed from C = 293 B; the darzi2026a k values are no longer reused.
- Major 5 (chain model directions; no security analysis): limitation stated. Join time is now reported, but chain continuity across epochs and a security analysis (non-repudiation, time sync, hybrid separability) are not done; stated in Limitations.
- Major 6 (counts inflated by API variants): fixed. Counts are over 64 distinct size classes, 24 at the lowest level per family; Fig. 1 plots one dot per class.
- Major 7 (security level not controlled): fixed. Main tables use the lowest level per family (level 1, ML-DSA level 2), stated in Method; Q2 signatures' levels stated in Limitations; other levels are in the appendix CSV, not in the paper.
- Major 8 (budgets questionable; contradicting work): fixed. Remote ID 201 B, SIB1 293 B, OSNMA 204/158 B variants (derived), C-V2X 437 and J3161 ceilings, DNS kept only as a ceiling reference and stated to be request-response; Falcon-512 conflict with abrar2026deployment explained via the two ceilings.
- Major 9 (sig_cert strawman): fixed in part. full_cert now follows each source's certificate handling (digest plus periodic certificate for C-V2X, DET for Remote ID, out-of-band keys for SIB1/OSNMA); the single-data-point 105 B overhead and the unmodelled mixed PQ-CA/classical chains are stated as limitations.
- Major 10 (Q3 method): fixed. Same denominator ((class, profile) pairs), deadlines tied to each profile's packet period, 3 ms reported separately with its correct attribution, UOV claim narrowed; keygen/throughput out of scope and the near-tautology on x86 are stated.
- Major 11 (missing related work, LMS/XMSS, maturity): fixed. Added perrig2000efficient, park2002efficient, wong1998digital, reyzin2002better, perrig2005tesla (cited for title-level contributions only), lms2019rfc8554, xmss2018rfc8391, nist2020sp800208, eaton2024provably; LMS/XMSS size-only rows scored; maturity paragraph added (NIST status citation still a \todo).
- Major 12 (contribution insufficient for CNS): limitation stated. Repositioned as a short measurement/accounting paper for IEEE VNC; the paper states it has no new mechanism, no security analysis and no MCU data. Baselines: darzi2026a 13/34 packets now reproduced; the others remain TODO-RESULT.
- Minor 1 (hybrid totals not reported): fixed (Table II hybrid row).
- Minor 2 (\HdrCV used for all three profiles): fixed (separate \HdrRID, \HdrSIB, \HdrOS, \HdrCV; DNS 15 B).
- Minor 3 (OSNMA 204 B): fixed (204 B PKR and 158 B KROOT variants, both marked derived).
- Minor 4 (hybrid partner per profile, raw vs DER): fixed (Ed25519 for Remote ID, ECDSA-P256 raw 64 B elsewhere, DER up to 72 B noted; SIB1 partner marked assumed).
- Minor 5 (Python classical timings): fixed (classical timings no longer used).
- Minor 6 (p95 over verified messages only): fixed (TTA95 over all messages; non-verifying messages count as missing).
- Minor 7 (summary.md mislabels 160 ms slot): fixed in the regenerated summary.md (slot period marked stated, darzi2026a).
- Minor 8 (3 ms attribution): fixed ("IEC 62351-6 text quoted in hussain2026a"; not tied to any profile).
- Minor 9 (chain deadline inherited from fragmented competitor): fixed (no shared deadline; TTA95 reported for every scheme at the same M).
- Minor 10 (one-at-a-time sweep, i.i.d. only): fixed (grid over M and loss for three signatures with different k; Gilbert-Elliott bursts added).
- Minor 11 (Remote ID header): fixed (budget is the RFC 9575 201 B cap; fragment headers stated unknown and set to 0, message counts are lower bounds).
- Minor 12 (one 64 B message, one machine): limitation stated.
- Minor 13 (title too long): fixed (one subtitle).
- Minor 14 (abstract presents smoke numbers as results): limitation stated (abstract says numbers are provisional and x86-only; must be updated after publication runs).
- Minor 15 (Fig. 1 dominated by SLH-DSA variants): fixed (one dot per lowest-level size class).
