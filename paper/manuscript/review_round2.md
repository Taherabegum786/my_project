# Review, Round 2: "Post-Quantum Access Tokens for CDNs: Stapling Fixes the Edge, Batching Fixes the Issuer"

Revision 1 of the former "EMBER" manuscript. Reviewer: the same independent referee as in round 1. Date: 2026-11-06.

**What I read:** `response_round1.md`, the revised `main.tex` and `sections/*.tex`, `references.bib`, `NUMBERS_TRACE.md`, `paper/results/RESULTS_R1.md`, and all new CSVs (`r1_oprg_agg`, `r1_oprg_deciles_agg`, `r1_pmove_agg`, `r1_b11_tradeoff`, `proto_capacity_r1_agg`, `proto_latency_r1`, `wire_bytes_r1`, `hpack_clients`, `token_sizes_r1`, `token_verify_r1`, `native_sig_minmax`, and the regenerated `dos.csv`, `sim_delta_sweep.csv`, `sim_sens.csv` and `sim_e2e_latency.csv`). I also read all 12 pages of `main.pdf` as images, checked that commit `3148c65` exists and contains H1–H9, and inspected the figure script `experiments/plots/make_r1.py`.

## Recommendation

**Minor revision.** Confidence: 4/5.

This is now a credible IEEE Access submission. The revision is substantial and honest. The authors took the central round-1 criticism (batching rarely happens at the recommended operating point), confirmed it with new data, and rebuilt the paper around it. The new framing has two parts:

- **Stapling fixes the edge.** M2 sends a per-token signature once per edge.
- **Pooled batching fixes the issuer.**

This framing is supported by the data, is more useful to practitioners than v1, and states the novelty modestly.

Every one of the 38 numbers I re-checked matches its CSV. Five problems still need fixing before acceptance:

1. One figure plots the wrong quantity.
2. The B11 recommendation misreads its own new citation.
3. The HPACK conclusion overgeneralizes from data that partly contradicts it.
4. M2 has no defined recovery path when an edge loses its verified-token cache entry. This is now the paper's recommended design, so the gap matters.
5. The validation paragraph contradicts itself about what the 24 rows are.

None of these needs new large experiments.

---

## 1. Status of the round-1 required changes

| # | Round-1 item | Status | Reason / evidence |
|---|---|---|---|
| 1 | Headline numbers vs. operating point (M1) | **Addressed** | Table IV and Fig. 2 report N_e, token size, issuer cores, edge cost and D at the same configuration. 71.5% of tokens have N_e = 1 at the v1 recommendation. Large-N rates are confined to a "Microbenchmark capability" paragraph. Verified against `r1_oprg_agg.csv` and `r1_oprg_deciles_agg.csv`. |
| 2 | Stapled per-token baseline (M2) | **Addressed** | M2 is implemented in Python, Go and the simulator, and now forms the paper's first finding. New issue N2 below: no cache-miss recovery path. |
| 3 | DoS numbers stale | **Addressed** | `dos.csv` was regenerated with run-2 costs and gives 0.484 / 1.026 / 0.0269, matching the text. The run-1 data are retained in `sim_costs_run1/`. |
| 4 | Table VI mixed configurations | **Addressed** | Separate per-tenant (T) and 8-shard (P8) columns, all cells filled, all matching the run-2 `sim_delta_sweep.csv`. H4 cites the per-tenant 1.0·10⁻⁴. |
| 5 | Stapling depends on p_move; validation does not cover it | **Mostly addressed** | 0.049% is labelled a model output. The p_move sweep (0–0.95%) and staple-all were added, the miss definition is stated, and re-routes and the shield tier are listed as not validated. Re-routes were not added to the prototype, which is acceptable as a stated limitation. The figure showing this sweep has a plotting bug (N1). |
| 6 | Unfair wire-byte comparison | **Addressed** | Like-for-like Table V at both table sizes, plus a real-client probe. New overgeneralization: N3. |
| 7 | Novelty overstated | **Addressed** | EMBER is called an MTL condensed signature, stapling is called MTL's full signature, and pull/push are mapped to MTC landmarks. ML-DSA-MTL, MTC -05 and the MTC-CA post were added. |
| 8 | B11 crossover | **Partially addressed** | The exposure-window analysis (L + V_max) and Fig. 4 are good. The conclusion drawn from Litinski (2023) is selective (N4). |
| 9 | Mixed native runs | **Addressed** | All tables and simulations use run 2, except the controller and DES check, which are justified and in the appendix. Spreads are reported as min–max. |
| 10 | P2 methodology | **Partially addressed (acceptable)** | Relabelled to 0.35–0.40 / 0.57–0.64 utilization, reported as per-run medians with [min, max], and moved to the appendix. Not rerun, as stated. P2 contains no M2 or staple-all runs (N7). |
| 11 | Stapled header size | **Addressed** | 2,461 B raw, 3,298 B as an HTTP/1.1 header line, +2,968 B per h2 session. Unit mixing remains with the "2,501–6,254 B" figure (m3). |
| 12 | Category 2; missing public seed | **Addressed** | Text corrected. The seed is recommended but not implemented, which is stated. |
| 13 | BW_push tenant count | **Addressed** | |
| 14 | Padding bound | **Addressed** | 12.45% measured; the analytic +38.9% at N = 2^14+1 matches `r1_summary.txt`. |
| 15 | 2 KB source | **Addressed** | KB 208427 cited; RFC limits stated. |
| 16 | Citation targets and versions | **Addressed** | The unsupported "open problems" claim was removed and the bib cleaned. ML-DSA-MTL -02 (Sep 2026) now supersedes the cited -01 (m6). |
| 17 | 43× vs 10.7×; e2e means | **Addressed** | Both ratios are given, and the means are given, with B5v 10× better than stapled EMBER on the mean. |
| 18 | "Pre-registered" | **Addressed** | Commit `3148c65` (2026-11-05 18:07 UTC) exists and contains H1–H9 in `paper/design/design.md`, as claimed. |
| 19 | Figures | **Partially addressed** | The old Fig. 9 is fixed (now Fig. 5, log axes). The new Fig. 3 (right) plots the wrong quantity for pull (N1). Table VIII floats into the reference list (m4). |
| 20 | Length | **Addressed** | 12 pages including appendices and references. |
| 21 | Placeholders and PDF | **Partially addressed** | The PDF is rebuilt (`main.pdf` = `main_v2.pdf`, distinct from v1). The DOI, AI declaration, e-mail and funding remain `[Editable]`. These are the author's to fill. |

## 2. Numbers audit (38 claims, revised manuscript vs. CSVs)

All marked OK match to the stated rounding.

| # | Location | Claim | Source | Status |
|---|---|---|---|---|
| 1 | Abstract | M2 URL token 148 B | `token_sizes_r1.csv` M2-B5s, path 60, ip 0 = 148 | OK |
| 2 | Abstract | 22.33 vs 22.80 µs | `proto_capacity_r1_agg.csv` b5s 22.328, b1 22.796 | OK |
| 3 | Abstract | 19× at 2,000/s | `r1_oprg_agg` 0.8175 / 0.04246 = 19.25 | OK |
| 4 | Abstract | 144× at 20,000/s | 8.1754 / 0.05669 = 144.2 | OK |
| 5 | Abstract | 268-B tokens | sim d_p50 = 5, so encoder N = 2^5 gives 268 | OK |
| 6 | Abstract | 5.4 ms delay | global fixed:0.01, D 5.426 ms | OK |
| 7 | Abstract | per-tenant 1.2× | 0.8175 / 0.6744 = 1.21 | OK |
| 8 | Abstract | Chrome adopts 64 KiB; curl and Go do not | `hpack_clients.csv` | Data OK; **conclusion overgeneralized for Go** (N3) |
| 9 | Intro | 25.7 B/request (Chrome) | `hpack_clients.csv` steady_block_bytes_mean 25.7 (×3 runs) | OK |
| 10 | Intro / §VI-B | M2 within 0.4% of smallest PQ in cookie form | 11,711 / 11,667 = 1.0038 | OK |
| 11 | Table III | B1 43,392 / 22.80 [22.23, 23.36]; M2 44,254 / 22.33 [21.60, 23.05]; O1 37,786 / 26.16; B5v 23,232 / 42.53; B5 13,079 / 75.58 | `proto_capacity_r1_agg.csv` | OK |
| 12 | §VI-B | O1 17% more than M2 | 26.16 / 22.33 = 1.172 | OK |
| 13 | §VI-B | K < 154 (d = 5), K < 96 (d = 8) | 100.9 / (0.889 − 0.235) = 154; 100.9 / (1.284 − 0.235) = 96 | OK |
| 14 | §VI-B | 0.953 vs 1.509 µs/request | oprg pertoken vs global 10 ms | OK |
| 15 | Table IV | all 16 rows × 7 columns (N_e = 1 %, tokens/tree, token, issuer, edge, hot, D) | `r1_oprg_agg.csv` staple_always (token size via encoder from d_p50) | OK, every cell checked |
| 16 | §VI-C | busiest decile has 69% of tokens, 59.4% alone | `r1_oprg_deciles_agg` decile 0: 4.99 M of 7.2 M, frac 0.594 | OK |
| 17 | §VI-C | 1,646 signatures/s; 0.674 vs 0.818 cores | oprg tenant fixed:0.01 issuer_sigs 1646 | OK |
| 18 | §VI-C | hot-edge verifications 1,658 → 151/s | λ̄ = 20,000 pertoken vs global 10 ms | OK |
| 19 | §VI-C | fleet edge CPU 0.456 vs 0.288; 5.18 vs 2.88 | oprg fleet_edge_cpu_cores | OK |
| 20 | §VI-C | 89.5/s with 50 regions; 0.046 cores saved at 200/s | oprg region50 89.52; 0.0817 − 0.0355 | OK |
| 21 | §VI-C | microbenchmark 41,774 / 469,254 / 1,275,990 tokens/s | `native_issuer_agg` N = 16, 2^8, 2^14 | OK (the N = 16 CI is very wide: 18,248–50,049) |
| 22 | Table V | all 28 cells | `wire_bytes_r1.csv` (b5s+staple = M2) | OK |
| 23 | §VI-D | 0.095× B5; within 1.3% of HMAC | 43,401 / 457,831; 27,048 / 26,706 | OK |
| 24 | §VI-D | staple +2,968 (EMBER), +2,921 (M2), 3,298 B HTTP/1.1 | `wire_bytes_r1`, `token_sizes_r1` | OK |
| 25 | §VI-D | Chrome at 4,096: 2,993–3,000 B/request; about 6.5 KB total at 64 KiB | `hpack_clients.csv` | OK |
| 26 | Table VI | T: 1.069 / 96.1 / 0.710 / 2.4e-5 … P8: 1.054 / 94.3 … | `sim_delta_sweep.csv`, native run 2 | OK (all 20 cells) |
| 27 | §VI-E | push 2.27 GB/s; roll-up 1.4–2.3% | `sim_delta_sweep`, `sim_dissem` | OK |
| 28 | §VI-E | p_move: 0 / 0.049 / 0.48 / 0.95%; staple-all 2,501–6,254 B | `r1_pmove_agg` tenant fixed:0.01 | OK (unit caveat, m3) |
| 29 | §VI-F | B11 0.383 MB/s; L = 60 s gives 16.7 fetches/s/edge, 0.17% core, 23 MB/s | `r1_b11_tradeoff.csv` | OK |
| 30 | §VI-F | issuer µs/token: B11 30.1, M2 408.8, per-tenant 337.2, pooled 21.2 / 2.83 | oprg issuer_cpu_us_per_token | OK |
| 31 | §VI-F | 38 h per key (2D-local) | Litinski 2023 abstract | Quote OK; **inference misread** (N4) |
| 32 | §VI-G | max error 4.4%; 76.9–78.5 vs 75.9 ms; 118–137 ms; 0.074–0.086 vs 0.026 ms | `proto_validate.csv` | Numbers OK; **row description inconsistent** (N5) |
| 33 | §VI-H | DoS 9,270–9,636; 4,630; 0.484; 7,680 → 65; 1.026; 0.0269 | `dos.csv` (run 2) | OK (fixed since round 1) |
| 34 | §VI-H | hybrid 1.405 → 1.982 µs (+41.1%) | `sim_sens` root_signer | OK |
| 35 | §VI-H | e2e means 0.0503 / 0.0049 / 0.101 / 0.486 ms; p99.9 112 ms | recomputed from `sim_e2e_latency.csv` | OK |
| 36 | App. B | SLH-DSA root D 0.575 → 0.881 s | `sim_sens` | OK |
| 37 | App. B | P2: O1 −2.60 [−6.29, 0.55]; B5 +12.14 [3.17, 16.52]; B5v +11.75 [2.61, 203.82]; utilization 0.35–0.40 / 0.57–0.64 | `proto_latency_r1.csv` | OK |
| 38 | Table VIII | H6 "p99 ≤ 2.61 µs" | the trace cites `sim_delta_sweep` max; `RESULTS_R1.md` states a max of 1.71 µs (oprg) and 1.42 µs (sweep); the oprg max is 2.21 µs | **Inconsistent source statements** (m5); the H6 verdict is unaffected |

**Summary:** no numerical mismatch in the paper text against the CSVs. The problems are interpretation and presentation issues (N1–N5).

## 3. New citations

| Entry | Real? | Supports its sentence? |
|---|---|---|
| liang2014httpscdn (S&P 2014, pp. 67–82) | Yes | Yes: CDNs hold customers' keys and secrets |
| cangialosi2016keysharing (CCS 2016, pp. 628–640) | Yes | Yes |
| springall2016shortcuts (IMC 2016) | Yes | Partly: it is about shared ticket and ephemeral secrets; acceptable for "sharing keys across servers enlarges damage" |
| litinski2023ecc (arXiv:2306.08585) | Yes (verified) | The quoted 38 h per key (strict 2D-local) is correct, **but** the same abstract reports a 300–700× lower cost with non-local connections (about 10 min per key in one cited regime). That is below V_max = 1 h, so it contradicts the paper's "B11 with a short L remains safe for some time" (N4). |
| rfc9113 (HTTP/2) | Yes | Yes: SETTINGS_HEADER_TABLE_SIZE semantics |
| ms-urllength (KB 208427, 2,083 characters) | Yes | Yes |
| cf2023pqorigins (Cloudflare, Sep 2023) | Yes | Yes: ML-KEM toward origins |
| draft-mldsa-mtl-dnssec (Kaizer, Harvey, Kaliski, Sheth; -01) | Yes (verified) | Yes: it uses ML-DSA-44 with MTL. A -02 (Sep 2026) exists; cite the latest (m6). |
| draft-mtc -05 (Jul 2026) | Yes (verified) | Yes |
| cf2026mtcca ("Building a post-quantum CA with MTCs") | Yes | Yes |
| draft-slhdsa-mtl-dnssec -06 (Mar 2026) | Yes | Yes |
| fregly2023mtl (LNCS 13871, pp. 415–441) | Yes | Yes |

No fabricated references. The two removed survey citations were correctly dropped together with the claim they were attached to.

## 4. New problems introduced by the revision

### Moderate (must fix)

**N1. Fig. 3 (right) plots the wrong quantity for pull.**
- The axis is "root installs + fetches per token (P3-style miss definition)", but the pull curve sits at 0.
- `make_r1.py:247` plots `staple_installs_per_token + (miss_per_token if mode != "pull" else 0)`. For pull this is installs (0) plus nothing.
- Pull should be plotted at its fetches, 0.996 → 2.43 per token over the sweep (`r1_pmove_agg.csv`).
- Fix: plot `miss_per_token` for pull, then regenerate the figure.

**N2. M2, the recommended design, has no defined behavior when an edge does not hold the verified entry.**
- M2's URL token is just claims plus a 16-B nonce reference. Unlike EMBER, it has no pull fallback: an edge without the cached H(ref‖claims) cannot verify the token and must fail closed.
- This happens after cache eviction under memory pressure, a server restart or drain, a different server behind the same VIP that does not share the cache, or a client that wrongly assumes it is on a known edge.
- The paper says "once per edge connection" (abstract, conclusion), "on its first request to an edge" (§IV-A) and "every request to an edge it has not used before" (§IV-C, staple-all). A client cannot observe "edge"; it observes connections. The unit needs to be one thing.
- The simulator models stapling per edge. P1 ran one process with one cache.
- Fix:
  1. Specify the recovery protocol, for example a 401 with `X-Staple-Required`, the client retries with the staple, at a cost of one RTT plus about 3 KB.
  2. State the staple unit (per connection) and make the simulator and the text consistent.
  3. Estimate the edge cache state: live tokens × entry size for V_max = 1 h at the busiest edge.
  4. Say how often recovery is expected and what it costs.
- This also bears on the "Stapling removes the root service as an availability dependency" claim: true, but M2 then depends on edge cache retention.

**N3. The HPACK conclusion contradicts part of its own data.**
- The abstract and §VI-D say "Chrome adopts a 64 KiB table, which makes ML-DSA cookies cheap, but curl and Go do not" and "affordable for Chrome users but not for other clients".
- In `hpack_clients.csv`, the Go client clamps to 4,096 B **yet sends the cookie for 228 B/request**, because with its small header set the 3.3 KB cookie fits alone in the 4 KiB table. RESULTS_R1 says so explicitly.
- curl/nghttp2 also has a 4,096-B table but re-sends the cookie (2,671 B/request). Table size is therefore not the only determinant. The rest of the header set and each encoder's indexing heuristics also matter.
- The Go-encoder rows of Table V (458,568 B at 4,096) assume about 570 B of other, changing headers. That is the reason, and it should be stated.
- Fix: reword to "whether a 3.3 KB cookie stays indexed depends on the encoder's table limit, its indexing policy and the other headers. Chrome (64 KiB) and our Go client (4 KiB, small header set) kept it indexed; curl did not." Then state the header-set assumption behind Table V.

**N4. The B11 recommendation misreads Litinski (2023).**
- The paper quotes the 38 h per key (strict 2D-local) and concludes "under such estimates B11 with a short L remains safe for some time".
- The same abstract's headline result is a 300–700× cheaper non-local architecture. That gives roughly 10 minutes per key in one regime, which is below V_max = 1 h, the paper's own binding constraint.
- These are estimates for hypothetical future machines and say nothing about *when* B11 becomes unsafe. The honest statement is that B11's safety depends on CRQC architecture, and plausible designs break a key faster than V_max.
- Fix: report both figures and drop "remains safe for some time", or tie it to a dated threat-timeline source. Consider recommending a shorter V_max (for example 10 min, already plotted in Fig. 4) as the lever if B11 is used.

**N5. The validation paragraph contradicts itself on what the 24 rows are.**
- §VI-G says "P3 covers 12 configurations, each scored on two metrics, giving 24 rows".
- The trace, Fig. 5 caption and Introduction say 24 rows = 12 configurations × 2 modes (pull, staple-first) for *one* metric (misses per token), and another 24 for root bytes.
- In P3, pull and staple-first give the same miss counts by definition, so there are really 12 independent comparisons per metric.
- Fix: "12 configurations × 2 modes = 24 rows per metric; because P3 counts staple installs as misses, the two modes are not independent."

### Minor

- **N6. "14 baselines" includes M2,** the paper's own recommended scheme (abstract, §V). Say "13 baselines plus M2" or "14 schemes".
- **N7. No prototype measurement of the recommended configurations.**
  - P3 covers pull and staple-first EMBER only, and P2 has no M2.
  - M2 + staple-all and pooled EMBER + staple-all are evaluated for dissemination and latency only in the simulator.
  - Acceptable, but add one sentence to Limitations.
  - If time permits, run a P3 configuration of M2 staple-all with V = 50. That would be cheap and would anchor the headline.
- **N8. P1 token sizes differ from the encoder table.** In P1, B1 is 100 B and M2 83 B; in the encoder, 166 and 148 B. The claims differ, so state that in Table III's caption. Also note that M2's URL token is *smaller* than HMAC's, since the 16-B nonce is shorter than the 32-B tag. This partly explains "M2 matches HMAC", and B10's 16-B truncated tag shows HMAC could shrink too.
- **N9. Issuer costs use OpenSSL's portable ML-DSA signing (408.8 µs).** circl signs in about 121 µs (`proto_go_verify_agg.csv`). Absolute issuer cores and the "about 10³ tokens/s" threshold scale with this, by about 3.4×. Add a sentence. The 19× and 144× ratios are less affected.
- **N10. Title and abstract scope.** "Batching fixes the issuer" holds only for one pooled tree per issuer key, so tenants must share an issuer key, normally a CDN-operated issuer. The abstract says "per issuer key" but not that this excludes the content-owner-issued, multi-CDN scenario used to motivate the paper. Add half a sentence. Consider "Pooled Batching" in the title.
- **N11. "Microbenchmark capability" N = 16 value.** 41,774 tokens/s has a 95% CI of 18,248–50,049. Report the interval or drop the value.

### Presentation (m)

- m1. Fig. 3 legend: "M2, staple first req." and EMBER staple-first overlap almost exactly. Say so in the caption, or use distinct markers or offsets.
- m2. Fig. 4: the left y-axis is in minutes and the x-axis in hours. Mark V_max = 1 h on the x-axis, as the dotted line partly does, and label the 10-min V_max curve as the "lever".
- m3. Staple byte units: 2,461 B (raw), 2,968 / 2,921 B (h2 increment), 3,298 B (HTTP/1.1) and the "2,501–6,254 B" figure (simulator raw bytes per session). Label each consistently.
- m4. Table VIII (hypotheses) floats into the reference list on p. 11, and the "Appendix C" heading on p. 10 has no content under it. Use `[h!]` or `\FloatBarrier`.
- m5. H6 evidence "p99 ≤ 2.61 µs": the trace (`sim_delta_sweep`), RESULTS_R1 (1.71 / 1.42 µs) and `r1_oprg_agg` (2.21 µs max) disagree. State one source.
- m6. Cite ML-DSA-MTL -02 (Sep 2026).
- m7. Table VIII H3 says "(Python)". The hypothesis in commit 3148c65 does not mention Python, so remove it or explain.
- m8. Conclusion: "the problem is sending and verifying a 2.4 KB signature on every request". The token is 3.3 KB including the encoding. Minor.

## 5. Overclaims and consistency check of the reframing

- **Supported:** both findings, the 1.2× per-tenant result, the 19× and 144× pooled savings with their costs (268–332 B and 5.4 ms), the like-for-like wire comparison, DoS, hybrid, and the e2e means. The paper now states openly that B5v beats stapled EMBER on mean latency and that M2 beats EMBER on edge CPU. This is good scientific practice.
- **Overclaims remaining:** N3 ("but curl and Go do not"), N4 ("B11 remains safe for some time"), N10 (scope of "batching fixes the issuer"). "Stapling ... fixes the edge for any signature scheme" (§VII-A, rec. 2) is true only if the cache-miss path (N2) is specified.
- **Dropped figures:** I found no dangling `\ref` (every ref resolves to a label, no `??` in the PDF). Claims whose figures were dropped are now in text or tables with CSV sources: e2e means, dissemination modes (Table VI), token sizes (§VI-A text and Table VII). Fig. 1 (architecture) was redrawn for M2 and EMBER and is consistent with the text.
- **Internal consistency:** the staple unit (N2) and the validation row count (N5) are the remaining inconsistencies.

## 6. Is it a credible IEEE Access submission?

**Yes, after the changes below.** The contribution is now crisp and honestly scoped: a systems and measurement study that separates two mechanisms and gives actionable deployment rules. The rules are backed by traced data, a working prototype, real-browser HPACK measurements and a simulator with explicitly scoped validation.

The single-VM and loopback limitations remain but are stated plainly and do not bear on the main conclusions, which are about CPU per request, bytes and counting. The earlier rejection's failure modes are fixed:

- no implausible numbers;
- no projected results presented as measured;
- no HNDL confusion;
- modest novelty claims;
- pre-registration verifiable in the repository.

For Computer Networks, the absence of any multi-PoP or real-network measurement would weigh more heavily. For IEEE Access, it is acceptable.

---

## 7. Required changes (in priority order)

| # | Priority | Location | Problem | Concrete fix |
|---|---|---|---|---|
| 1 | P0 | Fig. 3 right; `experiments/plots/make_r1.py:247` | Pull curve plotted as 0; it should be 0.996–2.43 fetches per token | Plot `miss_per_token` for pull, then regenerate and recheck the caption |
| 2 | P0 | §IV-A, §IV-C, Abstract, Conclusion, Limitations | M2 has no recovery when the edge lacks the cached entry; the staple unit (edge vs. connection) is inconsistent | Specify the miss path (for example 401 + retry with staple: one RTT plus about 3 KB), define the staple unit as per connection, estimate edge cache memory and expected recovery frequency, and qualify "fixes the edge" and the availability claim |
| 3 | P0 | Abstract, Intro contrib. 4, §VI-D | "curl and Go do not [make cookies cheap]"; Go measured 228 B/request with a 4 KiB table | Reword: indexing depends on table limit, indexing policy and header set. Report the Go result. State the about 570 B of changing headers assumed in Table V. |
| 4 | P0 | §VI-F, §VII-A rec. 4 | Litinski (2023) quoted selectively; the non-local estimate (about 10 min per key) is below V_max | Report both regimes, drop "remains safe for some time", and recommend V_max reduction as the lever |
| 5 | P1 | §VI-G | "12 configurations, each scored on two metrics, giving 24 rows" contradicts the caption and trace | "12 configurations × 2 modes = 24 rows per metric (misses, root bytes); modes not independent in P3" |
| 6 | P1 | Limitations, §V | Recommended configurations (M2 staple-all, pooled EMBER) have no prototype dissemination or latency run | Add a sentence, or run one small P3 configuration of M2 staple-all |
| 7 | P1 | §VI-C, §VII-A rec. 3 | Issuer costs use OpenSSL's portable ML-DSA (408.8 µs); circl signs in about 121 µs | State that absolute cores and the about 10³ tokens/s threshold scale with the signer implementation, and give the circl-based threshold |
| 8 | P1 | Title, Abstract | Pooled batching requires tenants to share an issuer key (CDN-operated issuance), which is incompatible with the content-owner, multi-CDN motivation | Add the scope in the abstract; consider "Pooled Batching Fixes the Issuer" |
| 9 | P2 | Table III caption, §VI-B | P1 claim strings differ from the encoder's; M2's token is smaller than HMAC's | State the claim lengths. Note that the 16-B nonce vs 32-B tag partly explains the parity. |
| 10 | P2 | Abstract, §V | "14 baselines" includes M2 | "13 baselines and M2" or "14 schemes" |
| 11 | P2 | Table VIII, trace, RESULTS_R1 | H6 p99 source inconsistent (2.61 / 2.21 / 1.71 µs); H3 "(Python)" | Use one source. Align H3 wording with commit 3148c65. |
| 12 | P2 | §VI-E, §IV-C, Table VII | Staple byte units mixed (raw vs h2 vs HTTP/1.1) | Label each figure's encoding |
| 13 | P2 | p. 10–11 | Table VIII floats into the references; empty "Appendix C" heading | Force placement (`[h!]`/`\FloatBarrier`) |
| 14 | P2 | §VI-C | 41,774 tokens/s at N = 16 has a wide CI (18k–50k) | Report the interval or drop it |
| 15 | P2 | references.bib | ML-DSA-MTL -01 superseded by -02 (Sep 2026) | Update |
| 16 | P2 | Front matter, Data Availability, AI declaration | `[Editable]` placeholders | Fill before submission (author action) |
