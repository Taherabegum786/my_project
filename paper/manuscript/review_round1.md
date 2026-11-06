# Review, Round 1: "EMBER: Post-Quantum CDN Access Tokens via Epoch-Merkle Batched Root Signatures"

Target venue: IEEE Access / Computer Networks
Reviewer role: independent referee with associate-editor-level summary
Material reviewed: `main.tex`, `sections/*.tex`, `references.bib`, `main.pdf` (all 14 pages read as images), `NUMBERS_TRACE.md`, the CSVs in `paper/results/`, and `paper/scout/prior_work.md`. Date: 2026-11-06.

**Recommendation: Major revision.** Confidence: 4/5 (high). I checked the data myself and am confident in the measurement and consistency findings. I am less sure how the editor will weigh novelty: EMBER is mostly an application profile of MTL mode and batch signatures.

---

## 1. Summary

The paper replaces per-token signatures in CDN signed URLs and cookies with Merkle batch signing. An issuer collects the tokens of an epoch into a salted, tweak-separated Merkle tree, signs the root with ML-DSA-44 (or SLH-DSA, or a hybrid), and gives each token its authentication path. Edges get signed roots in one of four ways: pull through the shield tier, push, period roll-up bundles, or "stapling", where the client sends the signed root on its first request to an edge. The paper gives a proof-sketch reduction to EUF-CMA plus sm-tcr. It measures token sizes, HPACK bytes per session, native OpenSSL 3.5.4 primitive costs, a Go edge prototype (capacity P1, latency P2, dissemination P3) and a fleet Monte Carlo simulator, against 13 baselines, including strong ones (multi-MAC, delegated Ed25519, KEM-wrapped MAC keys, ML-DSA with a verification cache). The paper reports several negative results: the adaptive epoch controller gave no gain, roll-up barely helped, and the hybrid root raised simulated edge CPU by 41.6%.

## 2. Strengths

1. **Honest framing of the threat model.** The paper says plainly that HMAC is already post-quantum and that the benefit is removing minting secrets from edges (lateral minting). This avoids the HNDL/authentication confusion that sank the author's earlier submission (prior_work.md §2.6).
2. **Strong baselines.** B10 (multi-MAC), B11 (delegated Ed25519), B12 (KEM-wrapped MAC keys) and B5v (ML-DSA plus verify cache) are the right competitors. The paper admits that B11 and B12 give smaller tokens.
3. **Plausible primitive numbers that trace to data.** ML-DSA-44 verification is about 100 µs in OpenSSL's portable implementation and 25–33 µs in circl, and a d=16 path verification is 2.3 µs. Every number I checked in Tables IV and V matches its CSV row exactly. The earlier "milliseconds of PQ verification" failure mode is gone.
4. **Negative results and measurement problems reported.** These include the contended P1 campaign being rerun, the two native runs differing by 15–20%, and the simulator's latency validation failing in 16 of 24 configurations.
5. **Reproducibility infrastructure.** NUMBERS_TRACE.md is excellent practice and made this audit possible.
6. **Correct citations.** I found no fabricated references (Section 6).

## 3. Weaknesses

### Major

**M1. The headline issuer and size numbers come from a regime the paper's own recommended configuration never reaches.** The abstract and conclusion advertise 503-B tokens at N=2^16 and 1.28 M tokens/s per issuer core, which is 522× per-token signing at N=2^14. Table IX, however, recommends per-tenant trees with a work-conserving or roughly 10 ms epoch. In the simulator at that operating point (λ̄=2000/s, 1000 tenants, Δ=0.01 s, `sim_delta_sweep.csv`, native backend, pool=0), the median token is **147 B**. By Eq. (3) with the simulator's 104-B claims, that means d=0, so the median epoch tree holds a single token. Each token then costs one ML-DSA root signature: issuer throughput falls back to about 2,446 tokens/s per core, B11 issues about 14× *faster* than EMBER instead of 14× slower, and with stapling every first request carries a full ML-DSA signature. At the recommended operating point EMBER is, in effect, "per-token ML-DSA with the signature detached and sent once per edge". The Merkle tree pays off only for high-rate or pooled tenants. The paper must report token size, issuer cost and miss behavior *at the same operating point*, give the distribution of N_e per epoch, and say clearly which benefits come from batching and which come from detaching the signature (stapling).

**M2. A key baseline is missing: "stapled per-token signature".** Following M1, the natural competitor is: issue a per-token ML-DSA signature, send it once per edge in a header, and carry only claims plus a 16-B nonce in the URL, with the edge caching H(claims‖nonce) as verified. This is EMBER with d=0, and it equals B5v without re-sending 3.3 KB on every request. Without this baseline the contribution of the tree itself is not isolated.

**M3. The abstract's wire-byte comparison picks a weak baseline.** The abstract's "0.144× the header bytes of split-cookie ML-DSA-44" compares EMBER in a *URL* with ML-DSA in *two cookies*, using a 4096-B HPACK table. With a 64 KiB table, the B5 single cookie costs 11,667 B per session (`wire_bytes.csv`), about 5× *less* than EMBER in a URL (60,605 B) and close to EMBER in a cookie (9,358 B). The HPACK dynamic table size is advertised by the decoder, which is the CDN edge (SETTINGS_HEADER_TABLE_SIZE), so the CDN controls this setting. The abstract should compare like with like (same placement, both table sizes) and state the 64 KiB result. The discussion should also say whether browsers' HPACK encoders actually use a larger advertised table.

**M4. The stapling headline (0.049% of requests wait) depends entirely on an unvalidated mobility assumption.** In the fleet simulator, stapled misses come only from the assumed per-segment re-route probability p_move=0.0005: misses are 0 with p_move=0 and 0.73 per token at p_move=0.005 and Δ=0.01 (`sim_sens.csv`). The prototype P3 has no re-routes. P3 also counts a stapled-root install as a "miss": pull and pull_staple show identical misses per token in `proto_validate.csv`, for example 0.05116 vs 0.05074. The fleet simulator does not count these installs. So the "24/24 validated" result (a) uses a different miss definition from the one behind Table VI's stapling row, (b) really covers 12 distinct configurations twice, (c) excludes the shield tier (`sim_proto_mc` is run with "no shield tier"), and (d) never exercises the mechanism that produces the 0.049%. Either validate re-routes, or present 0.049% as a model output that depends on an assumption and give the sensitivity range (0–0.56%) in the abstract.

**M5. Novelty relative to MTL mode and MTC is thin and should be stated more modestly.** EMBER tokens are MTL-style "condensed signatures" over a per-epoch series. Stapling is MTL's "full signature" sent once, as the paper itself notes. Pull and push of signed roots are MTC "landmarks"/tree heads distributed ahead of time, which MTC deployments already plan to deliver through CDNs. The B13 comparison ("MTL's series grows with λVmax") argues against a variant of MTL that no one would deploy, because an MTL series can be restarted per epoch. The paper should present itself as a *systems and measurement study of applying MTL/batch signing to CDN tokens*. Contribution 2 should be reworded to make clear that the profile is engineering. "Root stapling" should not be called a new mechanism. This matters because "marginal contribution" was the main reason the previous paper was rejected (R5.1).

**M6. Some numbers in the PDF do not match the CSVs.** See Section 4. The DoS paragraph (0.48 core, 1.03 cores, 0.027 core) uses values from an earlier run. The current `dos.csv` gives 0.586, 1.243 and 0.032. Table VI mixes pooled and per-tenant configurations without saying so. The stapled-header size is stated as 2.4 KB but measures 2,954–3,298 B. Given the venue history (prior_work.md: "implausible/interpolated numbers"), the paper cannot afford any of these mismatches.

**M7. Mixed native runs with absolute values that disagree in the same section.** All simulations use run 1 (ML-DSA-44 verify 122.3 µs). All tables use run 2 (100.9 µs). Readers see "ML-DSA-44 verification takes 100.9 µs" and then "per-token ML-DSA-44 adds 0.122 ms to every request". Rerun the simulations with run 2 (they took minutes, according to the wall-clock times in `sim_params.json`), or add a third run and report all values as a range. The "bootstrap 95% CI over 5 run medians" is close to [min, max] and should be reported as min–max.

**M8. The prototype methodology repeats part of an earlier criticism.** P1 runs over loopback inside the edge namespace, on one 4-vCPU VM, without TLS. P2 uses load levels taken from the *contended* P1 campaign, so its "50%/80% load" labels are wrong: B1's "80%" is about 63% of the reported capacity. P2's B5v latency has a t-CI with a negative lower bound ([−26.4, 186.5] ms), which is meaningless for latency. Recompute P2 load fractions from the quiet P1, rerun P2 or relabel it by actual utilization, and report per-run medians instead of t-CIs over collapsed runs. The paper should say explicitly that P1 is a CPU-cost measurement, which loopback is adequate for, and not a network measurement.

**M9. The comparison with B11 needs to be central and quantitative.** B11 has smaller tokens (214 B), about 22× less dissemination traffic than EMBER pull (383 vs 8,411 kB/s in Table VIII), and faster issuance at realistic N. It also leaves no secret at edges. Its only drawback is assuming that no CRQC breaks an Ed25519 key within the delegation lifetime (≤ Vmax = 1 h). The paper should discuss that assumption seriously: published resource estimates put first-generation CRQCs at hours to days per key, so a 5-minute delegation may remain safe for years. It should also state the delegation lifetime at which EMBER becomes preferable. As written, the reader is not told when EMBER beats B11.

### Minor

- m1. Truncation section: ML-DSA-44 is NIST category **2**, not category 1 (FIPS 204). Table IX says "ML-DSA-44 or SLH-DSA-128 roots (category 1)".
- m2. The tweak contains no random per-key public seed (SLH-DSA's PK.seed). sm-tcr is defined for a keyed family. Justify why kid‖epoch is enough, or add a 16-B random seed to SR_e.
- m3. Eq. for BW_push omits the number of active tenants T. The GB/s figures come from per-tenant pushes. Write BW_push = T_active · E · (|σ|+40)/Δ.
- m4. "Padding to 2^d (at most 12% issuer slowdown)": the measured slowdown is 12.45% at N=1000, and it is not an upper bound, since for N = 2^k+1 padding nearly doubles the leaf and tree work. Give the worst case analytically.
- m5. "Eq. (3) reproduces all 26 measured token sizes exactly" is true by construction (the measurement is the same encoder) and should not be presented as validation.
- m6. "Pre-registered hypotheses": no registry or timestamped commit is cited. Cite the commit hash that fixed H1–H9, or say "fixed before the experiments". The text says nine hypotheses, but Table X has eight rows (H3/H9 merged). The p99 CPU < 1 ms part of H6 is not reported.
- m7. The "2 KB URL length that is common practice" has no source. CloudFront's own URL limit is 8,192 B. Either cite a source for 2 KB or soften the abstract's "exceed URL budgets": B5 fits RFC 9110's 8000-octet recommendation and RFC 6265's 4096-B cookie minimum.
- m8. Re-route sensitivity: the "0.56 at p=0.005" value is for Δ=1 s. At the Δ=0.01 s operating point that the sentence discusses, it is 0.73.
- m9. Table V mixes key encodings: ECDSA pk 65 (raw point) vs 91 in the CSV (SPKI), RSA 270 vs 294. State which encoding is used.
- m10. "43× less than ML-DSA-44 verification" uses OpenSSL's portable ML-DSA. With circl the ratio is 10.7×. The abstract should give the conservative number or both.
- m11. Table VI: half its cells are "–". Fill them from `sim_delta_sweep.csv` or drop those columns.
- m12. Fig. 9 (right): the stapled points overlap at the origin and the horizontal error bars swamp the panel. Use a log axis or an inset.
- m13. The e2e comparison (Fig. 8) reports p99 only. The means are EMBER-staple 0.051 ms, B5v 0.006 ms and B5 0.122 ms (`sim_e2e_latency.csv`). By mean added latency B5v beats EMBER by about 8×, which should be stated.
- m14. "In the Go prototype O4 and O1 differ by 0.09%" vs "+41.6% simulated": explain that the difference is amortization (150 requests per root in P1, about 1 session per root in the simulator), and give the simulated per-root amortization factor.
- m15. Availability: fail-closed edges make the root service a new availability dependency that HMAC does not have. Discuss behavior during an outage of the root service or shield tier.
- m16. Reference [27] (Cloudflare PQ auth to origins) is cited for "CDNs already deploy ML-KEM key exchange ... toward origins". That post is about ML-DSA authentication. Cite a KEX source.
- m17. Writing: the abstract is long (about 220 words with 12 numbers). "We contribute a threat model stating that HMAC is already post-quantum" reads oddly as a contribution.
- m18. "Searches of the literature and of IETF drafts up to November 2026 found no published scheme..." This is fine, but add MTC landmark distribution and ML-DSA-MTL for DNSSEC (Section 7).

## 4. Numbers audit (36 claims checked against NUMBERS_TRACE.md and the CSVs)

Legend: OK = matches the CSV row; MISMATCH = differs; CTX = the number is correct but its context or rounding changes the meaning.

| # | Location | Claim | Source checked | Status |
|---|---|---|---|---|
| 1 | Abstract/Intro | B5 3,350; B6 4,535; B7 10,598; B8 22,907 B | token_sizes.csv path 60, ip 0 | OK |
| 2 | Abstract | EMBER 503 B at 2^16 | token_sizes.csv O1 n16 log2N16 | OK (CTX: see M1; operating-point median is 147 B) |
| 3 | Abstract | 2.34 µs warm verify | native_pathverify_agg evp d16 n16 2341.20 | OK |
| 4 | Abstract | 43× < ML-DSA-44 | 100.939/2.3412 = 43.1 | OK (CTX m10) |
| 5 | Abstract | 7.9× HMAC | 2341.2/297.12 = 7.88 | OK |
| 6 | Abstract | 1.28 M tokens/s | native_issuer_agg ML-DSA-44 N16384 n16 1,275,989.6 | OK (CTX M1) |
| 7 | Abstract | 0.144× split-cookie | 66,344/460,984 = 0.1439 | OK (CTX M3) |
| 8 | Abstract | 0.049% waiting | sim_delta_sweep pull_staple fixed:0.01 pool0 native, mean 0.0486% | OK (CTX M4) |
| 9 | Abstract | roll-up 1.4–2.2% | sim_dissem 6,097.6→6,010.7 (1.4%); 1.0695→1.0448 (2.3% unrounded; 1.069→1.045 = 2.2%) | OK (2.3% if computed from unrounded values) |
| 10 | Abstract | hybrid +41.6% | sim_sens 2.3691/1.67309 = 1.416 | OK |
| 11 | §VII-A | B9 3,435; B1 166; B2 209; B4 465; B12 171; B11 214; B10k3 187 | token_sizes.csv | OK |
| 12 | §VII-A | O1 375/503/588/673; O2 844 | token_sizes.csv | OK |
| 13 | Table IV | all 44 cells | wire_bytes.csv (h2-hpack, http1.1, h2-hpack-t64k) | OK |
| 14 | §VII-A | 0.256× HTTP/1.1 | 151,451/592,522 = 0.2556 | OK |
| 15 | §VII-A | 3,036.9 B/req | wire_bytes b5 cookie h2 3036.87 | OK |
| 16 | §VII-A / §V | staple 2,954 B / header "2.4 KB" | 69,298−66,344 = 2,954; RESULTS_B P3 header 3,298 B | MISMATCH ("2.4 KB" in §V is the raw signature size; the base64 header is about 3.3 KB) |
| 17 | Table V | ML-DSA-44 408.8 [386.9, 452.4] / 100.9 [100.2, 120.4]; Ed25519 30.1/94.6; P-256 23.0/69.6; RSA 314.1/20.7; SLH 306,464 / 14,436 | native_sig_agg.csv | OK |
| 18 | Table V | ECDSA pk 65, RSA pk 270 | native_sig_agg pk_bytes 91, 294 | MISMATCH (different encoding; m9) |
| 19 | §VII-B | d≤8: 1.28 µs, 4.3× | 1283.94/297.12 = 4.32 | OK |
| 20 | §VII-B | 0.75 µs d=4, 3.41 µs d=24 | 751.67, 3406.98 | OK |
| 21 | §VII-B | Go 3.074 / 0.853 / 32.76; 3.6×, 10.7× | proto_go_verify_agg.csv | OK |
| 22 | §VII-B P1 | B1 20.54 [20.25, 20.82], 48,340; O1 22.91 [22.49, 23.33], 43,355; B5 66.24, 15,040; B5v 37.38, 26,620; O4 22.93 | proto_capacity_agg.csv | OK |
| 23 | §VII-B P1 | 1.12×, 0.897×, 2.89×, 1.63× | derived | OK |
| 24 | §VII-C | 469,254 [319,698, 729,692]; 192×, 522× | native_issuer_agg N256; derived | OK |
| 25 | §VII-C | SLH-128s 49,063 at 2^14; 3.26/s | native_issuer_agg; 1/0.306464 s | OK |
| 26 | §VII-C | D 0.575→0.927 s | sim_sens root_signer | OK |
| 27 | §VII-C | Go issuer 432k/s, 53× | 1024/2.3724 ms = 431.6k; 8.07k | OK |
| 28 | §VII-D P2 | B2 −1.25, B3 −1.39; O1 −3.24 [−6.82, 0.34]; B5 +11.47 [5.09, 17.85]; B5v 80.05 | proto_latency_agg.csv | OK (CTX M8: load labels; the B5v t-CI includes negative latency) |
| 29 | Table VI | pull 0.01: 1.069 / 96.2 / 0.71% / 2.4e-5 | sim_delta_sweep pool0 native | OK |
| 30 | Table VI | push_rollup 0.01: 0.997 / 0.67% / 5.3e-5 | per-tenant (pool0): 1.0115 / 0.67% / 1.0e-4; pooled (pool1): 0.9972 / 0.668% / 5.3e-5 | MISMATCH (this row is the pooled config, the others are per-tenant; H4's "≤5.3e-5" relies on it) |
| 31 | §VII-E | 387 vs 6,098 per 1e6 | sim_dissem E500 Δ1: 387.3, 6097.6 | OK |
| 32 | §VII-E | staple BW 0.46–0.65 MB/s; push 140 MB/s–2.75 GB/s; B12 57 MB/s–1.13 GB/s; B11 0.08–1.5 MB/s; push 2.27 GB/s at Δ=0.01 | sim_dissem, sim_delta_sweep | OK |
| 33 | §VII-E | re-route sensitivity "0.56 when 0.005" (in Δ=0.01 context) | sim_sens p_move 0.005: 0.562 at fixed:1, 0.726 at adaptive (Δ≈0.01) | CTX (m8) |
| 34 | §VII-E | p99 0.0017 ms, 0.05% > 1 ms, p99.9 0.12 ms; pull p99 0.123 / p99.9 112 ms; B5v p99 0.125 | sim_e2e_latency.csv (recomputed: 0.0017, 0.050%, 0.1238; 0.1230, 112.0; 0.1248) | OK (CTX m13: means omitted) |
| 35 | §VII-F | controller −0.83 [−0.91, −0.75]; +0.005 [0.001, 0.010]; −0.001; WC 4.93 / 4.41 / −1.0 ms | controller_paired.csv | OK |
| 36 | §VII-G | 24/24, max 4.4%, model 14.8%; 0.05116 [0.05036, 0.05196] vs 0.05067; 8/8; staple 0.074–0.086 vs 0.026 | proto_validate.csv | OK (CTX M4: staple "misses" defined differently from the fleet simulator) |
| 37 | §VII-H | 9,270–9,636 fetches/s, 4,630 verifs/s, **0.48 core** | dos.csv 10k all_tenants: edge_cpu_frac **0.586** | **MISMATCH** |
| 38 | §VII-H | staple flood **1.03 cores**; rate-limited **0.027** | dos.csv: **1.243**, **0.032** | **MISMATCH** (values from an earlier run; RESULTS_A §7 was not updated after the rerun with run-1 costs) |
| 39 | §VII-H | 7,680 → 65 fetches/s | dos.csv low_tenant | OK |
| 40 | §IV | padding "at most 12%" | issuer_throughput.csv 54,471→47,687 = 12.45% | CTX (m4) |
| 41 | §VI | RTT 20.98 / 76.10 ms | proto_rtt.csv means | OK |
| 42 | §VI | DES vs MC 0.56% / 0.09% / 0.08%, 45 rows | sim_validate.csv max 0.557%, 0.089%, 0.082% | OK |
| 43 | Table VIII | dissem 8,411 / 689,374 / 283,521 / 383.2 kB/s | sim_dissem.csv | OK |

**Claims with no data source:** "2 KB URL ... common practice" (no citation); "about 2^43 quantum collision cost" (analytic, acceptable); "Industry roadmaps ... 2029" (cited and verified).

**Stale artifact:** `main.pdf` is byte-identical to `main_v1.pdf`. Rebuild after the fixes and keep the versions distinct.

## 5. Questions to the author

1. What is the distribution of N_e (tokens per epoch tree) at the Table IX configuration, per tenant-rate decile? What fraction of tokens sit in trees with N_e = 1?
2. How does EMBER compare with a "stapled per-token ML-DSA" baseline (M2), on bytes, edge CPU and issuer CPU?
3. Do Chrome, Safari and Firefox HPACK encoders use a dynamic table larger than 4096 B when the server advertises 64 KiB? If so, what is left of the cookie-form advantage?
4. Below what delegation lifetime is B11 as safe as EMBER under current CRQC resource estimates?
5. Why is there no random public seed in the tweak (m2)?
6. Can a stapled root be replayed to an edge to force verifications of *valid* roots (amplification), and is that covered by the per-client limit?
7. How is the 2 s issuance SLO motivated, and what is the client→issuer RTT in D?
8. What happens to sessions in progress when the root service or shield tier is unreachable (fail closed)?

## 6. Citation audit

All 39 cited entries were checked. The well-known ones were checked from knowledge, and the 2025–2026 items and drafts by web search.

| Key | Verdict | Note |
|---|---|---|
| fips203/204/205 | OK | |
| rfc2104, 6265, 7541, 9110, 9162, 9345, 9449 | OK | RFC 9110 does recommend ≥8000-octet URIs; RFC 6265 does give ≥4096 B per cookie |
| rfc9964 | OK (verified) | Prorock & Steele, May 2026; its caution about ML-DSA and small signatures is correctly quoted |
| shor1997, merkle1989, macaroons2014, bindel2017hybrid, sphincsplus2019 | OK | |
| batchsig2024 | OK | CT-RSA 2024, LNCS 14643, authors correct |
| fregly2023mtl | OK, incomplete | add volume and pages (CT-RSA 2023, LNCS 13871) |
| draft-mtl-mode (-09, Mar 2026) | OK (verified) | |
| draft-slhdsa-mtl-dnssec (-05, Sep 2025) | Outdated | a March 2026 revision exists; cite the latest |
| draft-mtc (-02, Mar 2026) | OK but outdated | authors verified; -04 is current; cite the latest |
| draft-batch-signing | OK (verified) | WG draft-00, Jan 2020; mark as expired |
| draft-mtac (Burls, -01, Oct 2026) | OK (verified) | the paraphrase "specifies no runtime authorization" matches the draft |
| cf2025mtc | OK | |
| cf2026roadmap | OK (verified) | Westerbaan, Apr 2026 |
| cf2026pqauthorigins | OK (verified, Jul 2026) | **misused** in §II-B as a source for ML-KEM toward origins (m16); dated Jun in the bib, published 29 Jul 2026 per Cloudflare's announcement; the changelog entry is 17 Jun 2026; check the date |
| akamai2026e2epqc | OK (verified) | Aug 2026 |
| sikeridis2020ndss, paquin2020benchmarking, sosnowski2023conext, kampanakis2024ttlb, schwabe2020kemtls, celi2021measuring | OK | they support "size more than CPU" |
| policharla2023pqpp | OK (verified) | 85–175 KB matches the final ePrint |
| kampanakis2023vision, alnahawi2024survey | Real, **support doubtful** | cited for "list such application-layer artifacts as open problems"; neither discusses CDN tokens as far as I know; quote the section or drop the claim |
| mediacdn-sig, cloudfront-signers, akamai-edgeauth | OK (vendor documentation) | |
| Uncited bib entries | cf2021sizingup, cf2026pqdnssec, sikeridis2022suppression, springall2016shortcuts | harmless; delete or cite (springall2016 is relevant to key sharing at edges) |

No reference could not be verified, and I found no hallucinated entries.

## 7. Novelty: related work from 2024–2026 that the paper misses

My searches found no paper or draft on post-quantum CDN signed URLs or cookies with Merkle batching, so the gap the paper claims seems real. The following closely related work should still be discussed:

- **draft-kaizer-dnsop-ml-dsa-mtl-dnssec** (Verisign, ML-DSA + MTL for DNSSEC). This is the same ML-DSA-root/condensed-signature pattern as EMBER O1, and closer than the cited SLH-DSA-MTL draft.
- **MTC landmark distribution via CDN** (draft-ietf-plants-merkle-tree-certs-04; Cloudflare, "Building a post-quantum CA with Merkle Tree Certificates", 2026; Let's Encrypt MTC plan, June 2026). Distributing signed tree heads to relying parties, including through CDNs, is the direct precedent for EMBER's root dissemination.
- Cloudflare, "ML-DSA will have to do" (2026), on ML-DSA-44 as the default signer and its category 2 rating.
- arXiv 2604.24869 (2026), on the network impact of PQ certificate-chain sizes on TTFB, and arXiv 2604.06100 (2026), on signature placement in PQ TLS hierarchies. Both are recent measurement work in the same community.
- arXiv 2604.04191 (2026), on MTC-based PQ PKI for Kubernetes: Merkle batching for workload identity tokens.
- `pqbatch` (GitHub), ML-DSA Merkle batching for event streams, which notes that an isolated verifier needs a full signature (EMBER's dissemination problem).
- CDN key-sharing literature, which supports R3 (no secret at edges): Cangialosi et al., "Measurement and Analysis of Private Key Sharing in the HTTPS Ecosystem" (CCS 2016); Liang et al., "When HTTPS Meets CDN" (IEEE S&P 2014); Keyless SSL.

## 8. Clarity, structure and length

- **Contribution statement:** clear in the introduction, but the abstract lists five contributions and 12 numbers. Rewrite it around one sentence: "Merkle batching plus stapling lets edges verify PQ tokens without holding secrets, at X B and Y µs, *at operating point Z*; the main costs are a dissemination path and an extra round trip per cold edge."
- **Overclaims to fix:** "validated fleet simulator" (validated only for miss counts at V≤50, without re-routes or a shield tier); "pre-registered"; "Stapling is the decisive mode" (it depends on p_move); "1.28 million tokens/s" (not reached at the recommended operating point); "exceed URL budgets" (only for a 2 KB budget); "a security theorem" (a proof sketch, which the paper does admit).
- **Length (13.3 pages):** longer than needed. Suggested cuts, about 3 pages:
  - Move to an appendix or supplement: Fig. 4 left panel (Python, a secondary source), Table III (simulator parameters), the DES-vs-MC cross-check, the two-native-runs paragraph, Table X (shorten to one paragraph or move it out), and the per-scheme P2 details. P2 is inconclusive and could become two sentences.
  - Shorten Section V-B and Table VII (controller) to one paragraph. Given Eq. (6), an optimum at the smallest Δ is close to analytically predictable once λΔ ≪ E, so it does not need a full subsection.
  - Merge Algorithms 1 and 2 into one figure or move Algorithm 1 to the appendix.
  - Table IX duplicates text in §VII. Keep either the table or the text.
- **Figures:** most are readable at print size. Fig. 9 (right) needs rework (m12). Fig. 2 has dense small labels, so check the ≥7 pt claim at 100% zoom. Fig. 8 should show the full range or add the means.

## 9. Check against the earlier rejection's failure modes (prior_work.md)

| Failure mode | Status in this paper |
|---|---|
| Implausible numbers, ms-scale PQ verification | Fixed. Primitive values are plausible and traced. |
| Projected or interpolated results shown as measured | Mostly fixed. Simulation outputs are labeled. However, the stapling headline (0.049%) and E=2000 results are model extrapolations driven by assumptions, and the abstract does not say so (M4). Stale DoS values (M6). |
| Marginal contribution | **At risk** (M1, M2, M5). |
| Single host / loopback | Partly repeated (M8). The paper acknowledges it honestly, but P1 is still loopback on one VM. |
| Unjustified metrics or constants | Mostly fixed. The 2 KB budget and 2 s SLO need justification (m7, Q7). The "10 ms / 10%" demotion rule is fine. |
| HNDL / authentication confusion | Fixed. Stated explicitly in the introduction. |
| No artifacts | Fixed in intent. The DOI/URL is still a placeholder. |

---

## 10. Required changes checklist (in priority order)

| # | Priority | Location | Problem | Concrete fix |
|---|---|---|---|---|
| 1 | P0 | Abstract, §VII-C, Conclusion, Table IX | 503 B / 1.28 M tok/s / 522× are measured at N=2^14–2^16, but the recommended Δ≈10 ms with per-tenant trees gives N_e≈1 (median token 147 B) | Add a table of N_e distribution, token size, issuer CPU and misses **at the recommended operating point** (per-tenant and pooled). Restate the abstract's issuer and size claims for that point, or recommend pooling or larger Δ explicitly and report the latency cost. |
| 2 | P0 | §VI-A, §VII | No "stapled per-token ML-DSA" baseline, so the value of the tree is not isolated | Add baseline B5s: per-token ML-DSA signature sent once per edge in a header, URL carries claims + nonce, edge caches H(claims‖nonce). Report bytes, edge CPU, issuer CPU. |
| 3 | P0 | §VII-H, NUMBERS_TRACE | DoS CPU numbers 0.48 / 1.03 / 0.027 do not match dos.csv (0.586 / 1.243 / 0.032) | Regenerate the paragraph from the current dos.csv (state which native run). Update RESULTS_A §7 and the trace. |
| 4 | P0 | Table VI, H4 row of Table X | push_rollup row is the pooled config (0.997, 5.3e-5); the other rows are per-tenant (per-tenant push_rollup: 1.0115, 1.0e-4) | Use per-tenant values throughout, or add a pooled column. Fill the "–" cells. Fix H4 evidence. |
| 5 | P0 | Abstract, §VII-E, §VII-G | The stapling result (0.049%) depends on the assumed p_move; P3 has no re-routes and counts staple installs as misses, so validation does not cover it | Add re-routes to P3, or label 0.049% as model-dependent with the 0–0.56% sensitivity range in the abstract. Use one consistent miss definition across P3 and the fleet simulator. Say that the 24 configurations are 12 distinct ones and that the shield tier is not validated. |
| 6 | P0 | Abstract, §VII-A, Table IV discussion | 0.144× compares EMBER-URL with B5-two-cookies at a 4 KiB HPACK table; with a 64 KiB table B5 cookie (11,667 B) beats EMBER-URL (60,605 B) | Compare like placements at both table sizes in the abstract. Discuss who sets the table size (the edge, via SETTINGS) and real browser encoder behavior. |
| 7 | P1 | Intro contributions 2–3, §II-D, §V | Novelty relative to MTL/MTC is overstated; "root stapling" is MTL's full signature; the B13 comparison argues against an MTL variant no one would deploy | Reframe as a systems and measurement study of MTL/batch signing for CDN tokens. Compare with an MTL series restarted per epoch. Add the related work in Section 7 (ML-DSA-MTL DNSSEC, MTC landmarks via CDN, key-sharing literature). |
| 8 | P1 | §VII-I, §VIII-A | When to prefer EMBER over B11 is not quantified | Add a paragraph and figure: B11 safety as a function of delegation lifetime vs CRQC time-to-break estimates. State the crossover. Give B11 issuer and dissemination costs at the same operating point as EMBER. |
| 9 | P1 | §VI-B, all simulation-derived numbers | Simulations use run 1 and tables use run 2 (122.3 vs 100.9 µs in adjacent sentences); 5-point bootstrap CIs | Rerun the simulations with run-2 costs (or a third run) and report primitive spreads as min–max over runs. |
| 10 | P1 | §VII-D (P2), Limitations | Load labels come from contended capacities; B5v t-CI includes negative latency | Recompute utilization from the quiet P1. Rerun P2 or relabel loads. Report per-run medians and a nonparametric CI. Shorten P2 to a paragraph if it stays inconclusive. |
| 11 | P1 | §V, §VII-A | Stapled header given as "2.4 KB"; measured 2,954 B (HPACK) and 3,298 B (P3 header) | State the encoded header size (about 3.3 KB) consistently. |
| 12 | P1 | §IV-D Truncation, Table IX | ML-DSA-44 called category 1; tweak lacks a random public seed | Correct to category 2 (n=16 then sets the overall level at category 1). Add a per-kid random seed to T or justify its absence. |
| 13 | P2 | §V-A | BW_push omits the tenant count | BW_push = T_active · E · (|σ|+40)/Δ. |
| 14 | P2 | §IV-D Privacy | "at most 12%" padding cost is 12.45% and not a bound | Report the worst case (N = 2^k+1) analytically and the measured value with its N. |
| 15 | P2 | §II-A, Abstract, Intro | "2 KB URL practice" is unsourced; "exceed URL budgets" overgeneralizes | Cite a source (for example, browser or CDN limits) or soften the claim. Mention RFC 9110's 8000 octets in the abstract. |
| 16 | P2 | §II-B, §II-D | [27] cited for ML-KEM toward origins; [36], [37] cited for "open problems" they may not state; outdated draft versions | Fix the citation targets. Update MTC to -04 and SLH-DSA-MTL to the latest revision. Add volume and pages for fregly2023mtl. Remove unused bib entries. |
| 17 | P2 | Abstract, §VII-B, Fig. 8 | 43× uses OpenSSL's portable ML-DSA; e2e reports p99 only | Give both 43× (OpenSSL) and 10.7× (circl). Add means to Fig. 8 and say that B5v's mean added latency is lower than EMBER-staple's. |
| 18 | P2 | Table X, §VI | "Pre-registered", nine vs eight hypotheses, H6 part missing | Cite the commit hash, list H1–H9 separately, and report p99 CPU for H6. |
| 19 | P2 | Fig. 9 right, Fig. 2 | Stapled points illegible; dense labels | Log axis or inset; check font sizes at print scale. |
| 20 | P2 | Overall length | 13.3 pages, some of it redundant | Apply the cuts in Section 8 (about 3 pages to an appendix). Shorten the abstract to about 180 words and 5–6 numbers. |
| 21 | P2 | Front matter, Data Availability | Placeholders; main.pdf identical to main_v1.pdf | Fill in the DOI, AI declaration and affiliation email. Rebuild the PDF. |
