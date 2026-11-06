# Response to the round-1 review

We thank the reviewer for a careful review that checked our data. The new measurements confirm the reviewer's central point (M1/M2), and the paper has been reframed accordingly.

- **New title:** "Post-Quantum Access Tokens for CDNs: Stapling Fixes the Edge, Batching Fixes the Issuer".
- **New framing:** a design-space and measurement study. EMBER is presented explicitly as a CDN profile of MTL mode and batch signing, not as a new primitive.

Section numbers below refer to the revised manuscript (`main.pdf`, 12 pages, appendices included). New data are described in `paper/results/RESULTS_R1.md`. Every number is traced in `NUMBERS_TRACE.md`.

Note: "Fig. 12–15" below are the result-file names (`fig12_proto_validation`, `fig13_operating_region`, `fig14_pmove_sensitivity`, `fig15_b11_tradeoff`). In the PDF they are Figs. 5, 2, 3 and 4.

---

## Major comments

**M1 (headline numbers come from a regime the recommended configuration never reaches).** Agreed, and confirmed with new runs.
- At the v1 recommendation (per-tenant trees, Δ = 10 ms, λ̄ = 2000/s), 71.5% of tokens sit in single-token trees (59.4% even in the busiest decile), and the issuer saving is 1.2×.
- The abstract no longer contains 503 B, 1.28 M tokens/s or 522×.
- New §VI-C, Table "Operating points" and Fig. 13 report, at each configuration:
  - the N_e distribution;
  - encoder token size;
  - issuer cores;
  - edge µs/request;
  - verifications at the hottest edge;
  - delay.
- The large-N microbenchmark rates now appear only in a paragraph labelled "Microbenchmark capability". It states that N ≥ 2^14 needs λΔ ≥ 1.6·10⁴, which no simulated configuration with Δ ≤ 0.1 s reaches.
- The recommendation is now one pooled tree per issuer key, Δ ≈ 10 ms, with staple-all. That gives 19× (λ̄ = 2000/s) and 144× (20000/s) fewer issuer cores, with every metric reported at that point.
- The paper now says which benefit comes from detaching the signature (stapling) and which from batching (issuer cost only).

**M2 (missing stapled per-token baseline).** Added as **M2**, implemented in Python, the Go prototype and the simulator (§IV-A, §VI-B). M2 matches or beats EMBER on edge CPU, URL bytes, misses and delay:

| Metric | M2 | Comparison |
|---|---|---|
| Go P1 edge CPU, µs/request | 22.33 | HMAC 22.80; EMBER 26.16 |
| URL token | 148 B | — |
| Session bytes, URL form | 27,048 B | HMAC 26,706 B |
| Mean delay (staple-all) | 0.41 ms | EMBER 5.4 ms |

EMBER's only advantage is issuer cost, and only when pooled. This finding is now the paper's second contribution.

**M3 (weak wire-byte baseline in the abstract).**
- The abstract no longer contains the 0.144× comparison.
- Table "wire" (§VI-D) compares like placements at both HPACK table sizes. It states that with a 64 KiB table, B5 in a cookie (11,667 B) is smaller than stapled EMBER (11,853 B).
- We added a real-client experiment (`h2probe`):
  - Chrome 153 adopts an advertised 64 KiB table and sends a 3.3 KB cookie for 25.7 B/request.
  - curl/nghttp2 and the Go client clamp the table to 4096 B.
- The roles of SETTINGS_HEADER_TABLE_SIZE (edge as decoder) and of the encoder's choice are explained with RFC 7541 and RFC 9113 (§II-A).

**M4 (the stapling headline depends on the mobility assumption).**
- The 0.049% figure is now labelled a model output that depends on one assumption (§VI-E).
- A new p_move sweep (Fig. 14) gives the range: 0 at p_move = 0, 0.48% at 5·10⁻³, 0.95% at 10⁻².
- We added **staple-all**, which removes waiting at every p_move for 2,501–6,254 B of stapled roots per session. It is now recommended.
- On the validation (§VI-G):
  - its 24 rows are 12 configurations × 2 modes;
  - P3 counts staple installs as misses;
  - the comparison uses the same definition on both sides;
  - neither re-routes nor the shield tier is validated.
- Validation is claimed only for miss and byte counts.

**M5 (novelty overstated).**
- Contribution 3 and §II-C now say plainly that the EMBER token is an MTL condensed signature over a per-epoch series.
- Root stapling is described as MTL's full signature sent once.
- Pull and push correspond to MTC landmark distribution.
- We added ML-DSA-MTL for DNSSEC, the MTC -05 landmarks, and a CDN operator building an MTC CA.
- We explain that an MTL series restarted at every epoch is structurally EMBER (§V, B13 note).
- The paper is framed as a systems and measurement study.

**M6 (numbers that did not match the CSVs).**
- **DoS:** RESULTS_R1 §4 shows that the v1 values (0.48 / 1.03 / 0.027 cores) were the run-2 values. The committed `dos.csv` the reviewer checked held a later run-1 rerun. `dos.csv` has now been regenerated with run-2 costs (0.484 / 1.026 / 0.0269), and §VI-H says "second-run costs". The run-1 values (0.586 / 1.243 / 0.032) are kept in `sim_costs_run1/dos.csv`.
- **Table VI:** replaced by Table "dissem", with per-tenant (T) and 8-shard pooled (P8) columns. Every cell is filled. H4 now cites the per-tenant push+roll-up value, 1.04·10⁻⁴.
- **Stapled header:** now given consistently (§IV-C, §VI-D):

  | Form | Size |
  |---|---|
  | Signed root (raw) | 2,461 B |
  | HTTP/1.1 header line | 3,298 B |
  | HTTP/2 session increment | +2,968 B |
  | M2 equivalent (HTTP/2 session increment) | 2,921 B |

- **Token sizes:** taken from the encoder, not the simulator (the simulator's 104-B claims give values 14 B smaller).

**M7 (mixed native runs).**
- All simulations were rerun with run-2 costs (sweep, dissem, e2e, sens, DoS, oprg, pmove), except the controller study and the DES consistency check. Both are now in Appendix B.
- We state explicitly that the run-2 sweep left misses bit-identical and moved D by at most 0.1 ms (96.17 → 96.08 ms). The controller effects are all far below the 10 ms threshold, so its conclusions cannot change.
- Primitive spreads are reported as [min–max] of the run medians (Table "primitives").

**M8 (prototype methodology).**
- §V states that P1 is a CPU-cost measurement on loopback, not a network measurement.
- P2 has been relabelled against the quiet P1 capacities: nominal 50% and 80% become 0.35–0.40 and 0.57–0.64 utilization.
- P2 is now reported with per-run medians and [min, max], with no t-CIs, and moved to Appendix B as secondary.
- P2 was not rerun; Limitations says so.

**M9 (B11 comparison).** New §VI-F and Fig. 15.
- B11's exposure window is L + V_max. It is safe only if t_break > L + V_max, so V_max, not L, is the binding constraint.
- Short L is cheap: at L = 60 s, 0.17% of an edge core and 23 MB/s fleet-wide.
- We cite a published 38-h-per-key estimate (2D-local architecture) and state the crossover.
- B11 issuer cost (30.1 µs/token) is compared with M2 and per-tenant EMBER (both higher) and with pooled EMBER (lower).

## Minor comments

| # | Change |
|---|---|
| m1 | ML-DSA-44 is now called category 2. With n = 16 the *token* is category 1 (§IV-E). The recommendations table was rewritten accordingly. |
| m2 | We acknowledge the missing public seed. We recommend a 16-B per-kid seed in the tweak, carried in SR_e (+16 B per staple, 0 B per token), and state that it was not measured (§IV-E, Limitations). |
| m3 | BW_push now includes T_active (§IV-C). |
| m4 | Padding is reported as measured 12.45% at N = 1000 (Python), with an analytic worst case of +38.9% at N = 2^14+1 (§IV-E). |
| m5 | Eq. (size) is described as what the encoder implements, not as a validation (§IV-B). |
| m6 | "Pre-registered" is replaced by "fixed before the experiments in commit 3148c65 (2026-11-05 18:07 UTC)". H1–H9 are listed separately (Appendix C). H6's p99 CPU result is reported (≤ 2.61 µs). |
| m7 | The 2 KB figure is attributed to legacy clients and cited (Microsoft KB 208427: 2,083 characters). The abstract no longer says "exceed URL budgets". §VI-A states that B5 fits RFC 9110 and RFC 6265. |
| m8 | The re-route numbers now come from the p_move sweep at Δ = 10 ms (Fig. 14). |
| m9 | Table "primitives" states that key sizes are raw (65 B and 270 B), not SPKI. |
| m10 | Both ratios are given: 43× (OpenSSL) and 10.7× (circl) (§VI-A). |
| m11 | Table "dissem" has every cell filled. |
| m12 | Fig. 12 uses log axes on both panels. |
| m13 | §VI-H gives the means: stapled EMBER 0.0503 ms, B5v 0.0049 ms (10× lower), B5 0.101 ms. |
| m14 | The amortization is explained: about 141 requests per root verification in the simulator, versus one verification per run in warm P1 (§VI-H). |
| m15 | Availability is discussed: fail-closed pull edges depend on the root service, and staple-all removes that dependency (§IV-C, §VII-A). |
| m16 | ML-KEM toward origins now cites the Cloudflare 2023 post and Akamai. The ML-DSA origin-authentication post is cited for ML-DSA only. |
| m17 | The abstract was rewritten around the two findings, with 6 numbers. |
| m18 | We added ML-DSA-MTL DNSSEC, MTC landmarks and the MTC CA post (§II-C). |

## Numbers audit (§4)

- **#2, #6:** removed from the abstract. These values now appear only as labelled microbenchmark capability.
- **#7:** removed from the abstract. The like-for-like table replaces it.
- **#8:** labelled model-dependent, with the p_move range.
- **#9:** given as 1.4–2.3% (the 2.3% is computed from unrounded values).
- **#10:** run-2 value, +41.1%.
- **#16:** fixed (M6).
- **#18:** encoding stated (m9).
- **#28:** P2 relabelled (M8).
- **#30:** Table "dissem" (M6).
- **#33:** fixed (m8).
- **#34:** means added (m13).
- **#36:** miss definition stated (M4).
- **#37, #38:** explained, and `dos.csv` regenerated (M6).
- **#40:** fixed (m4).
- `main.pdf` has been rebuilt, and `main_v1.pdf` is kept.

## Citation audit (§6)

- **Updated:**
  - fregly2023mtl: volume 13871, pages 415–441.
  - MTC: -05 (Jul 2026).
  - SLH-DSA-MTL: -06 (Mar 2026).
  - TLS batch signing: marked as expired.
  - cf2026pqauthorigins: month removed, because sources disagree.
- **Removed:** kampanakis2023vision and alnahawi2024survey, together with the unsupported "open problems" claim.
- **Uncited entries:** sikeridis2022suppression, cf2021sizingup and cf2026pqdnssec are removed. springall2016shortcuts is now cited for key sharing.
- **New, each verified by web search:**
  - draft-kaizer-dnsop-ml-dsa-mtl-dnssec-01;
  - Cloudflare, "Building a post-quantum CA with MTC";
  - Cangialosi et al. (CCS 2016);
  - Liang et al. (S&P 2014);
  - Litinski (arXiv:2306.08585);
  - RFC 9113;
  - Microsoft KB 208427;
  - Cloudflare's 2023 post on PQ to origins.
- **Not cited:**
  - "ML-DSA will have to do": we could not verify the title.
  - The arXiv 2604.* papers and `pqbatch`: we did not verify them.
  - The Let's Encrypt MTC plan: we found it only in secondary reporting.

## Related work (§7)

- **Added:** ML-DSA-MTL for DNSSEC, MTC landmarks, the MTC CA blog, and the CDN key-sharing literature (Cangialosi, Liang). The key-sharing papers support the "no secret at edges" requirement.
- **Not added:** the three arXiv 2026 preprints and `pqbatch`, because we could not verify their content well enough to characterize them accurately.

## Questions to the author (§5)

1. **N_e distribution.** Fig. 13a and Table "Operating points": 71.5% of tokens have N_e = 1 at the v1 setting.
2. **Stapled per-token baseline.** M2 (see M2 above).
3. **Browser HPACK tables.**
   - Chrome 153: yes, it adopts 64 KiB, and the 3.3 KB cookie then costs 25.7 B/request.
   - curl and Go: no, they clamp to 4096 B.
   - Firefox and Safari: not tested (Limitations).
4. **When B11 is as safe as EMBER.** When t_break exceeds L + V_max (Fig. 15).
5. **Public seed.** See m2.
6. **Replay of a valid staple.**
   - At an edge that has the root cached: it costs nothing, because the root cache is checked before verifying.
   - Elsewhere: at most one verification per (kid, e).
   - Fake staples: bounded by per-client limits, which bring a staple flood from 1.026 cores to 0.0269 cores (§IV-E, §VI-H).
7. **2 s SLO.** It was a design parameter of the controller. Since the controller is now a secondary appendix result, the SLO no longer drives any recommendation. D includes the root-miss RTTs but not the client→issuer RTT; the latter is about 95 ms in P3, where it is reported.
8. **Root-service or shield outage.** Fail-closed pull-only edges reject tokens of uncached epochs. Staple-all and M2 do not depend on the root service (§IV-C).

## Required-changes checklist (§10)

| # | Status |
|---|---|
| 1 | Done (M1). |
| 2 | Done (M2). |
| 3 | Done (M6). |
| 4 | Done (M6). |
| 5 | Done: labelled model-dependent, with the range in §VI-E. The abstract no longer cites 0.049%. P3 re-routes not added (Limitations). |
| 6 | Done (M3). |
| 7 | Done (M5). |
| 8 | Done (M9). |
| 9 | Done, except the controller and DES runs, which are justified (M7). |
| 10 | Relabelled with nonparametric ranges; not rerun (M8). |
| 11 | Done. |
| 12 | Done (m1, m2). |
| 13 | Done (m3). |
| 14 | Done (m4). |
| 15 | Done (m7). |
| 16 | Done (citation audit). |
| 17 | Done (m10, m13). Fig. 8 is no longer in the paper; its means are in the text. |
| 18 | Done (m6). |
| 19 | Done: Fig. 12 uses log axes. Fig. 2 is removed. Figs. 13–15 were regenerated with fonts ≥ 7 pt. |
| 20 | Done: 12 pages including appendices and references (v1 was 13.3 + references). Secondary material is in Appendix B. The abstract is 211 words. |
| 21 | PDF rebuilt. The DOI, the AI declaration and the e-mail remain [Editable] placeholders for the author to fill. |
