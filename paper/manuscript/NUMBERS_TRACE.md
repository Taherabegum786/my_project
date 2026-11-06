# NUMBERS_TRACE (revision 2): every numeric claim in the manuscript, mapped to its source

All paths are relative to `paper/results/`. "Derived" means arithmetic on the listed values, with the formula shown.

**Cost runs.**
- **run 2** (post-reboot native OpenSSL 3.5.4; top-level `native_*_agg.csv`) feeds every table and every simulation. This includes the R1 reruns of sweep, dissem, e2e, sens, DoS, oprg and pmove (`RESULTS_R1.md` §1).
- **run 1** (`native_run1/`, `sim_costs_run1/`) feeds only the controller study (`sim_controller_*.csv`, `controller_paired.csv`) and the DES-vs-MC check (`sim_validate.csv`).

"oprg" means `r1_oprg_agg.csv`. Unless stated, its rows are mode `staple_always`.

## Abstract
| Claim | Source |
|---|---|
| 13 baselines and M2 | B1–B13 plus M2 (Table baselines) |
| 148-B URL token (M2) | `token_sizes_r1.csv` M2-B5s, url_path_len 60, with_ip 0: token_bytes 148 |
| 22.33 vs 22.80 µs edge CPU | `proto_capacity_r1_agg.csv`: b5s 22.328, b1 22.796 |
| 19× at 2,000/s | oprg λ̄=2000, tenant/pertoken issuer_cpu_cores 0.817505 vs global/fixed:0.01 0.042461; derived 0.8175/0.04246 = 19.25 |
| 144× at 20,000/s | oprg λ̄=20000: 8.17544 vs 0.056686; derived 144.2 |
| 268-B tokens | `token_sizes_r1.csv` EMBER-O1 log2N 5 path 60: 268. The pool's d_p50 = 5 comes from oprg λ̄=2000 global fixed:0.01 |
| +5.4 ms delay | oprg λ̄=2000 global fixed:0.01 D_mean_s 0.005426 (5.43 ms); text rounds to 5.4 |
| per-tenant 1.2× | oprg λ̄=2000 tenant fixed:0.01 issuer 0.674408 vs 0.817505; derived 1.21 |
| Chrome adopts 64 KiB; curl/Go clamp to 4096 | `hpack_clients.csv` column table_size_updates |

## I. Introduction
| Claim | Source |
|---|---|
| 3,350-B ML-DSA-44 token | `token_sizes.csv` B5 path 60 |
| 2,420-B signature | FIPS 204 |
| 25.7 B/request (Chrome, 64 KiB) | `hpack_clients.csv` chrome-153-headless 65536 steady_block_bytes_mean |
| 24 of 24 rows, 12 configurations | `proto_validate.csv` metric miss_per_token: 24 rows = 12 configs × 2 modes, all pass_mc True |
| ~10³ tokens/s threshold | derived in §VII-A (see below) |
| 2029 roadmap | cited [cf2026roadmap] |

## II. Background
| Claim | Source |
|---|---|
| 8000 octets; 2,083 characters; 4096 B/cookie | RFC 9110; Microsoft KB 208427; RFC 6265 |
| ML-DSA 2420/3309/4627; SLH 7856/17088 | FIPS 204/205 |
| Privacy Pass 85–175 KB | [policharla2023pqpp] |

## IV. Design space
| Claim | Source |
|---|---|
| M2 header 2,420 B; ~138 B hashed per request | `RESULTS_R1.md` §3 (bench_r1; `baselines/stapled.py`) |
| 26-B tweak; 30-B blob header | `experiments/ember/th.py`, `ember/token.py` |
| Encoder sizes 161/268/332/460 B (N = 1, 2^5, 2^8, 2^14); M2 148 B | `token_sizes_r1.csv` path 60, ip 0 |
| Eq. (size) implemented by the encoder | `model_check.csv` token_bytes rel_err 0 (stated as implementation, not validation) |
| 2N−1 hashes; ≤ P/Δ signatures/s | construction |
| Signed root 2,461 B; header line 3,298 B | `token_sizes_r1.csv` staple_raw_bytes, staple_header_http11_bytes |
| Vmax 1 h; 8 B per revoked token | `sim_params.json` v_max_s; design (4 B epoch + 4 B index) |
| ML-DSA-44 category 2 | FIPS 204 |
| +341 B for n=32 at N=2^16 | `token_sizes.csv` O2 844 − O1 503 |
| 2^128 / 2^64 generic bounds | analytic (n = 16 bytes) |
| Padding 12.45% at N=1000 (Python) | `issuer_throughput.csv`: 54,471 → 47,687 tokens/s |
| Worst case +38.9% at N=2^14+1 | `r1_summary.txt` "Padding" section (analytic from `native_issuer_agg.csv` components) |
| 16-B seed proposal | design recommendation (not measured) |

## V. Methodology
| Claim | Source |
|---|---|
| 4 vCPU, Xeon 2.1 GHz, AVX-512, SHA-NI, Linux 6.18, 15 GB | `env.txt`; BRIEF |
| run 1 vs run 2: 122.3 vs 100.9 µs; 15–20% | `native_sig_minmax.csv` / `r1_summary.txt` "NATIVE PRIMITIVES" |
| Misses bit-identical; D moved ≤ 0.1 ms (96.17 → 96.08 ms) | `r1_table6_agg.csv` (run1 and run2 columns); `RESULTS_R1.md` §1 |
| Link delays 10 / 37.5 ms; 1 Gbit/s; MTU 1500 | RESULTS_B testbed |
| P1: 1 core, 64 conns, K=150, 5 runs | `run_proto.sh`; `proto_capacity_r1.csv` |
| P3: V {10,50}, Δ {0.1,1,10}, λ {20,200}, 60 s, 5 runs | `proto_p3_config.json` |
| 3,311-B cookie value; 150 fetches | `hpack_clients.csv` cookie_value_bytes, seg_requests |
| E=500, Zipf 0.8, 50 shields, T=1000 Zipf 1.0, λ̄ ∈ {200, 2000, 20000}, K mean 150, 4 s, p_move 0.0005, RTTs 15/60/120 ms | `sim_params.json` |
| ~7% of sessions move once | RESULTS_A §10.3 (0.0751 re-routes per token, `r1_pmove_agg.csv` moves_per_token at 5e-4) |
| Hypotheses fixed in commit 3148c65 (2026-11-05 18:07 UTC) | `git log -- paper/design/design.md`; the first result commit is 44e8685 (18:31) |

## VI. Results
### A. Primitives and naive tokens
| Claim | Source |
|---|---|
| Table primitives (medians, [min–max]) | `native_sig_agg.csv` (median_us, ci95_lo_us/ci95_hi_us = min/max of the 5 run medians, as listed in `r1_summary.txt`); `native_pathverify_agg.csv` |
| Raw key sizes 65 / 270 | the v1 table's key encoding; the CSV pk_bytes (91 / 294) are SPKI. RSA is dropped from the R1 table |
| Path d=0 0.24 µs, d=16 2.34 µs, HMAC 0.30 µs | `native_pathverify_agg.csv` evp d0 235.01, d16 2341.20, hmac 297.12 ns |
| 43× / 7.9× | derived 100.939/2.3412 = 43.1; 2341.2/297.12 = 7.88 |
| Go 3.07 vs 32.76 µs; 10.7×; circl 3.6–4.0× faster | `proto_go_verify_agg.csv`; RESULTS_A §1 |
| B5 3,350; B6 4,535; B7 10,598; B1 166; B2 209; B11 214; B12 171; B5c cookie 1,687 | `token_sizes.csv` path 60 |

### B. Stapling fixes the edge
| Claim | Source |
|---|---|
| Table P1 (req/s, µs/req, CIs, token B) | `proto_capacity_r1_agg.csv` |
| 7,419 staple verifications / 1,108,422 requests (one run) | `raw/proto_r1/p1_stats_b5s_1.json` (RESULTS_R1 §3) |
| EMBER 17% more than M2 | derived 26.16/22.33 = 1.17 |
| Earlier campaign B1 20.54 vs 22.80 (~10%) | `proto_capacity_agg.csv` b1 20.536 vs `proto_capacity_r1_agg.csv` b1 22.796 |
| M2 D 0.41 ms | oprg λ̄=2000 tenant pertoken D_mean_s 0.000409 |
| K < 154 (d=5), K < 96 (d=8) | derived 100.939/(0.88931−0.23501) = 154.3; 100.939/(1.28394−0.23501) = 96.2 (`native_pathverify_agg.csv`) |
| Mean K = 150 | `sim_params.json` K_mean |
| 0.953 vs 1.509 µs/req | oprg λ̄=2000 pertoken / global fixed:0.01 edge_cpu_us_per_req_mean |

### C. Operating region (Table oprg, Fig. 13)
| Claim | Source |
|---|---|
| All table cells | oprg rows (staple_always). Columns: frac_tok_N1, mean_tokens_per_tree, issuer_cpu_cores, edge_cpu_us_per_req_mean, busiest_edge_verifs_per_s, D_mean_s. Token B is the encoder size at d_p50 (`token_sizes_r1.csv` and Eq. (size) with 118-B claims: d0 161, d1 183, d2 204, d4 247, d5 268, d8 332) |
| 71.5% N_e=1; 1.22/tree; decile 1 69% of tokens, 59.4% N_e=1 | oprg tenant fixed:0.01 λ̄=2000; `r1_oprg_deciles_agg.csv` (RESULTS_R1 §2) |
| 1,646 sig/s | oprg issuer_sigs_per_s 1645.85 |
| 20 and 200 tokens/tree; 100 sig/s | oprg global fixed:0.01 mean_tokens_per_tree 19.998 / 199.99; issuer_sigs_per_s 100 |
| hot edge 1,658 → 151 | oprg λ̄=20000 pertoken 1658.38; global fixed:0.01 151.33 |
| fleet CPU 0.456 vs 0.288; 5.18 vs 2.88; 1.6–1.8× | oprg fleet_edge_cpu_cores; derived 1.58, 1.80 |
| regions: 89.5/s | oprg λ̄=2000 region50 fixed:0.01 busiest_edge_verifs_per_s 89.52 |
| λ̄=200 saving 0.046 cores | derived 0.081729 − 0.035511 |
| 41,774 / 469,254 / 1,275,990 tokens/s; 2,446 | `native_issuer_agg.csv` ML-DSA-44 n16 N=16 / 256 / 16384; derived 1/408.8 µs |
| λΔ ≥ 1.6×10^4 | N = 2^14 = 16,384 |

### D. Wire bytes and HPACK clients
| Claim | Source |
|---|---|
| Table wire | `wire_bytes_r1.csv` (h2-hpack, h2-hpack-t64k; url and cookie); `tables/tab_r1_hpack.tex` |
| 0.095× | derived 43,401/457,831 |
| M2 within 1.3% of HMAC | derived 27,048/26,706 = 1.013 |
| 11.7–12.0 KB; HMAC 9.1 KB | table cookie 64 KiB column |
| Staple increments 2,968 (EMBER), 2,921 (M2); 3,298 B header line | `wire_bytes_r1.csv` (RESULTS_R1 §9 item 11) |
| Chrome 65536 update in 3 runs; 25.7 B/req; ~6.5 KB total; 2,993–3,000 B/req at 4096 | `hpack_clients.csv` |
| curl / Go clamp to 4096 | `hpack_clients.csv` table_size_updates [4096] |
| Go default 4096 (source) | x/net v0.38.0 `http2/config.go:98` (RESULTS_R1 §7) |

### E. Dissemination and stapling sensitivity
| Claim | Source |
|---|---|
| Table dissem (T and P8) | `r1_table6_agg.csv` / `tables/tab_r1_table6.tex` Δ = 0.01 rows (run 2) |
| push 2.27 GB/s | `sim_delta_sweep.csv` push pool0 Δ=0.01 λ̄=2000 native root_bw_fleet_Bps 2.267e9 |
| 150 vs 120 ms | `sim_params.json` push_ms, first_req_ms |
| roll-up 1.4–2.3%: 6,098 → 6,011; 1.069 → 1.045 | `sim_dissem.csv` E=500 Δ=1 miss_per_mreq 6097.6 / 6010.7 (1.4%); `sim_delta_sweep.csv` pool0 Δ=0.01: 1.069464 → 1.044814 (2.3%) |
| ≤ 1.0e-4 except per-tenant push | table root/served |
| 0 / 0.049% / 0.48% / 0.95% | `r1_pmove_agg.csv` tenant fixed:0.01 pull_staple frac_req_waiting at p_move 0 / 5e-4 / 5e-3 / 1e-2 |
| staple-all 0%; 2,501–6,254 B | `r1_pmove_agg.csv` staple_always staple_bytes_per_session |

### F. B11
| Claim | Source |
|---|---|
| B11 214 B; 30.1 µs/token; 0.383 MB/s at L=1 h; EMBER pull 8.41 MB/s | `token_sizes.csv`; `native_sig_agg.csv` Ed25519 sign; `r1_b11_tradeoff.csv` L=3600; `sim_dissem.csv` |
| L=60 s: 16.7 fetches/s/edge, 0.17% core, 23 MB/s | `r1_b11_tradeoff.csv` L=60 |
| 38 h per key (2D-local) | [litinski2023ecc] abstract |
| Issuer µs/token 408.8 / 337.2 / 21.2 / 2.83 | oprg issuer_cpu_us_per_token |

### G. Validation
| Claim | Source |
|---|---|
| 24/24, max 4.4% | `proto_validate.csv` miss_per_token and root bytes rows |
| 76.9–78.5 vs 75.9 ms; 118–137 ms; ~4,400 tokens; 0.074–0.086 vs 0.026 ms | `proto_validate.csv` miss_lat_mean_ms; RESULTS_B §5 |
| Installs counted as misses | RESULTS_R1 §6 |

### H. Other
| Claim | Source |
|---|---|
| DoS 9,270–9,636 fetches/s; 4,630 verifs/s; 0.484 core; 7,680 → 65; staple flood 1.026; limited 0.0269 (run 2) | `dos.csv` (run 2), `r1_summary.txt` "DoS" section |
| Hybrid 1.405 → 1.982 µs (+41.1%) | `sim_sens.csv` root_signer fixed:1 pull edge_cpu_us_per_req_mean; derived 1.4106 |
| ~141 requests per verification | `r1_summary.txt` amortisation: tenant fixed:0.01 pull 141.2 |
| Ed25519 verify 94.6 µs | `native_sig_agg.csv` |
| P1 O4 vs O1 0.09% | `proto_capacity_agg.csv` o4 22.9285 / o1 22.9086 |
| E2E means 0.0503 / 0.0049 / 0.101 / 0.486 ms; p99.9 112 ms; 10× | `sim_e2e_latency.csv` (r1_summary "E2E means"); derived 0.0503/0.0049 = 10.3 |

## VII. Discussion
| Claim | Source |
|---|---|
| Trust table | bytes: `token_sizes.csv` / `token_sizes_r1.csv`; verify: `native_sig_agg.csv`, `native_pathverify_agg.csv` (M2 hit ≤ th_200B 207 ns; B5v hit sha256_3500B 2,191 ns; d=5 889 ns; d=0–4 235–752 ns); dissemination: `sim_dissem.csv` (B12 283.5 MB/s, EMBER pull 8.41 MB/s), `r1_b11_tradeoff.csv`, `wire_bytes_r1.csv` staple increments |
| 0.41 cores per 10³ tokens/s | derived 1000 × 408.8 µs |
| ≤ 0.057 cores up to 20,000/s; ≥ 10 tokens/tree at λ ≥ 10³ | oprg global fixed:0.01; derived λΔ = 10 |
| 120–184 more bytes | derived 268−148, 332−148 |
| WC 0.62 ms at 20,000/s; 1 core | oprg λ̄=20000 global wc D 0.000624, issuer 0.99997 |
| τ = 5 s | design default |

## Appendix
| Claim | Source |
|---|---|
| Controller: −0.001 [−0.004, 0.002]; +0.005 [0.001, 0.010]; −0.83 [−0.91, −0.75]; WC 4.93 / 4.41; SLO | `controller_paired.csv` (run 1) |
| D moved ≤ 0.1 ms: 96.17 → 96.08 | `r1_table6_agg.csv` / RESULTS_R1 §1 |
| DES vs MC 0.56 / 0.09 / 0.08%, 45 rows | `sim_validate.csv` (run 1) |
| P2 utilisation 0.35–0.40 and 0.57–0.64; O1 −2.60 [−6.29, 0.55]; B5 +12.14 [3.17, 16.52]; B5v +11.75 [2.61, 203.82] | `proto_latency_r1.csv` (r1_summary "P2 RELABELLED") |
| 260–450 Mbit/s; 624 Mbit/s | RESULTS_B §4 |
| Earlier campaign values 20.54 / 22.91 / 22.93 / 37.38 / 66.24 / 71.04 / 98.04 / 115.74 | `proto_capacity_agg.csv` (quiet run, 2026-11-05 23:53) |
| SLH-128s root D 0.575 → 0.881 s; RTT×0.5 staple D 0.503 s | `sim_sens.csv` (run 2) |
| Hypothesis table | the rows above; H1 v1 data: `token_sizes.csv` 503/588, `wire_bytes.csv` 0.144/0.256; H2 whole request derived 26.16/22.80 = 1.15; H6 p99 max 2.61 µs (`sim_delta_sweep.csv` native max edge_cpu_us_per_req_p99); H9 192–522× (`native_issuer_agg.csv` N=2^8 and 2^14 / 2,446) |

## Figures
- Fig. 1 is TikZ and has no data.
- Figs. 13, 14 and 15 come from `r1_oprg_agg.csv` + `r1_oprg_deciles_agg.csv`, `r1_pmove_agg.csv` and `r1_b11_tradeoff.csv`. They were regenerated for legibility by `experiments/plots/writer_r1_figs.py`, which calls the `make_r1.py` plotting functions with fonts ≥ 7 pt, legends moved outside the data and encoder token sizes in Fig. 13c. No CSV changed (checked by md5), and `r1_summary.txt` was not rewritten.
- Fig. 12 comes from `proto_validate.csv` (log axes, `make_figures.py`).

## Addendum
| Claim | Source |
|---|---|
| M2 within 0.4% of the smallest in cookie form | `wire_bytes_r1.csv` cookie h2 64 KiB: M2 11,711 vs B5 11,667; derived 1.0038. At 4 KiB M2 (12,114) is the smallest PQ option |

## Round-2 additions
| Claim | Location | Source |
|---|---|---|
| Recovery RTT 20.98 ms | §IV-A | `proto_rtt.csv` client→edge mean (RESULTS_B §5) |
| M2 staple header line 3,242 B | §IV-A | `token_sizes_r1.csv` M2-B5s staple_header_http11_bytes |
| Cache entry 24 B (16-B key + 8-B expiry) | §IV-A | `experiments/proto/edge/main.go`: `scache map[[16]byte]int64` (payload only; hash-table overhead not measured) |
| 165.8/s and 1,658/s new (token, edge) pairs at the busiest edge | §IV-A, §VII-A | oprg tenant/pertoken staple_always busiest_edge_verifs_per_s: 165.80 (λ̄=2000), 1658.38 (λ̄=20000) |
| 0.60 M / 5.97 M entries; 14.3 / 143 MB | §IV-A, §VII-A | derived 165.80×3600 = 596,879 × 24 B = 14.3 MB; 1658.38×3600 = 5,970,175 × 24 B = 143.3 MB (upper bound: entries live ≤ V_max = 3600 s) |
| B1 100 B vs 166 B; M2 83 B vs 148 B | Table P1 caption | `proto_capacity_r1_agg.csv` token_bytes; `token_sizes.csv` / `token_sizes_r1.csv` path 60 |
| 16-B nonce vs 32-B tag | §VI-B | token formats (`baselines/stapled.py`; HMAC-SHA256 tag) |
| circl sign 121.2 µs (root), 123.9 µs (token) | §VI-C, §VII-A | `proto_go_verify_agg.csv` sign_root_mldsa44 121.170, sign_token_b5 123.858 |
| ~3.4-fold fewer cores with circl | §VI-C | derived 408.8/121.17 = 3.37 |
| 0.12 cores per 10³ tokens/s with circl | §VII-A | derived 1000 × 121.2 µs = 0.121 |
| threshold ≈3.4×10³ tokens/s (circl) vs ≈10³ (OpenSSL) | Intro, §VI-C, §VII-A, Conclusion | derived: rate at which per-token signing costs 0.4088 cores: 0.4088/121.17 µs = 3,374/s; 0.4088/408.8 µs = 1,000/s |
| N=16 issuer CI 18,248–50,049 | §VI-C | `native_issuer_agg.csv` ML-DSA-44 N=16 tps_ci95_lo/hi (bootstrap) |
| ~570 B of other headers per request | Table wire caption | RESULTS_B §1 (hpackbytes header set) |
| Go client 228 B/request at 4096; curl 2,671 B/request | Abstract, Intro, §VI-D | `hpack_clients.csv` go-x-net 228.4/228.5; curl 2670.7/2675.7 |
| Litinski: 38 h/key (2D-local); 300–700× cheaper and ~10 min/key with non-local connections | §VI-F, §VII-A, Conclusion | [litinski2023ecc] arXiv abstract (verified by web search 2026-11-06): "one key every 10 minutes using 6000 modules" at 10% threshold, 10-µs code cycle |
| Fig. 3 right, pull curve 1.0–2.4 fetches/token | Fig. 3 caption | `r1_pmove_agg.csv` tenant fixed:0.01 pull miss_per_token 0.996126 → 2.432818 (plotted as installs + misses after the `make_r1.py` fix) |
| 24 rows per metric = 12 configs × 2 modes; 12 independent comparisons | §VI-G, Intro | `proto_validate.csv` (12 configurations × {pull, pull_staple} per metric) |
| H6 p99 ≤ 2.61 µs | App. B | single source: `sim_delta_sweep.csv` native, max edge_cpu_us_per_req_p99 = 2.613 (`r1_oprg_agg` max is 2.21; RESULTS_R1's 1.71/1.42 refer to subsets) |
| Staple bytes units | §IV-C, §VI-D, §VI-E | raw signed root 2,461 B and HTTP/1.1 line 3,298 B (`token_sizes_r1.csv`); h2 session increments 2,968/2,921 B (`wire_bytes_r1.csv`); simulator raw bytes per session 2,501–6,254 B (`r1_pmove_agg.csv` staple_bytes_per_session) |

## R2 experiments (trace replay and prototype R2), added by the R2 writer

Trace sources: `RESULTS_R2_TRACE.md`, `r2_trace_summary.txt` (console output of `plots/make_trace.py`), `trace_agg.csv` (mean and Student-t 95% CI over 9 cluster-days, `cluster = all` rows unless a cluster is named), `trace_replicates.csv`, `trace_rates.csv`, `trace_oprg_V600.csv`, `trace_oprg_V86400.csv`, `tables/tab_r2_trace.tex`. "scaled" = rates × 1/SamplingRate (Poisson within minute); "sampled" = exact replay of the published trace. Assumption throughout: one signed-URL token per (object key, 1-h bucket).

### Title, abstract, introduction, conclusion
| Claim | Source |
|---|---|
| issuer 0.38–1.08 cores vs 177 (M2), full trace rates | `trace_agg.csv` scaled, verifier shared, fixed:0.01: global issuer_cores_ember 0.3826, tenant 1.0820; issuer_cores_m2 176.713 (r2_trace_summary "TREE SIZES / ISSUER") |
| K = 1.7–2.4 (mean requests per token) | `trace_replicates.csv` via r2_trace_summary "REPLICATES": eag 2.36, nha 1.71, prn 1.72 |
| 53.8 vs 1.9 µs/request; 1,869 vs 426 B/request | r2_trace_summary "EDGE CPU": scaled global fixed:0.01 shared: M2 53.79 [47.44, 60.13], EMBER 1.88 [1.80, 1.96]; bytes M2 1869, EMBER 426 |
| 28× edge crypto; 4.4× bytes | derived 53.79/1.88 = 28.6 (RESULTS_R2_TRACE §7 "28×"); 1869/426 = 4.39 |
| median 547 tokens per per-type tree; R1 degeneracy only at low rates | scaled tenant fixed:0.01 medianN 547, N1 0.0002; sampled tenant fixed:0.01 N1 0.9153 |
| K*_cpu ≈ 48–154 (d = 16…5); K*_bytes ≈ 9–27 | `r2_k_crossover.csv` (from `experiments/plots/writer_r2_crossover.py`; see derivation below) |
| 19–144× issuer (simulation) | unchanged, oprg (see Abstract rows above) |

### Derivation of the requests-per-token crossover (Fig. 18, §VI-D, §VII-A)
Inputs (native run 2): t_v = ML-DSA-44 verify median 100.939 µs (`native_sig_agg.csv`); path(d) = `native_pathverify_agg.csv` evp pathverify n=16 ns_median: path(0) 0.23501, path(5) 0.88931, path(8) 1.28394, path(12) 1.81025, path(16) 2.34120, path(24) 3.40698 µs; M2 token 148 B and staple line 3,242 B, EMBER S_tok(d) = 118 + 3 + ⌈4(30+16d)/3⌉ (`token_sizes_r1.csv`; the script asserts the formula reproduces 161/268/332/460 B at log2N 0/5/8/14).
- Per request at one verifier, root already held: M2 = t_v/K + path(0); EMBER = path(d). Equal at K*_cpu = t_v / (path(d) − path(0)):
  - d=5: 100.939/(0.88931−0.23501) = 154.3; d=8: 96.2; d=12: 100.939/1.57524 = 64.1; d=16: 100.939/2.10619 = 47.9; d=24: 31.8.
  - Using the trace model's M2 hit cost th_200B = 0.20736 µs instead of path(0) gives 148.0 / 93.8 / 63.0 / 47.3 (≤ 4% lower); the paper uses path(0) as in §VI-B.
- Bytes per request: M2 = 148 + 3242/K; EMBER = S_tok(d). Equal at K*_bytes = 3242/(S_tok(d) − 148):
  - d=5: S 268 → 3242/120 = 27.0; d=12: S 417 → 3242/269 = 12.1; d=16: S 503 → 3242/355 = 9.1.
- Check against the trace: with K ≈ 1.88 (1/0.5308 M2 contacts per request, shared verifier), M2 = 100.939 × 0.5308 + 0.207 = 53.78 µs, matching `trace_agg.csv` 53.79.
- Synthetic K̄ = 150 ≥ K*_cpu for d ≥ 6 and ≈ K*_cpu (154) at d = 5; trace request-weighted median K = 2–4 < K*_bytes and K*_cpu at every d ≤ 24.

### §V Methodology (trace paragraph)
| Claim | Source |
|---|---|
| 3 clusters, first 3 full days, 15–18 Mar 2023, 9 replicates | `trace/README.md`; `trace_replicates.csv` |
| sampling 1e-4 (eag, prn), 4e-4 (nha) | `r2_trace_summary.txt` REPLICATES |
| 23–24 content types; 10–12 VIP types | `trace_rates.csv` groups (r2_trace_summary "POOL RATES") |
| 71% of sampled requests on keys seen ≥ 2 times within 5 h | RESULTS_R2_TRACE §1 (sampling check) |
| Poisson check: 0.07–0.69% sig/s; N1 within 0.010; edge CPU within 0.6% | r2_trace_summary "POISSON-WITHIN-MINUTE CHECK": rel 0.07–0.69%; N1 max |Δ| 0.0097 (tenant fixed:0.01, 0.9153 vs 0.9250); CPU 51.374 vs 51.663 = 0.56% |
| ≈390–2,200 hosts per cluster | derived from the CacheLib doc's traffic factors (eag 1/13.4, nha 1/6.37, prn 1/4.58; doc read 2026-11-06) ÷ SamplingRate: (1/13.4)/1e-4 = 746; (1/6.37)/4e-4 = 392; (1/4.58)/1e-4 = 2,183 |

### §VI-D Real CDN trace (Table trace, Fig. 18)
| Claim | Source |
|---|---|
| per-cluster tokens/s scaled 302,631 / 226,150 / 768,027; K 2.36 [2.14, 2.57] / 1.71 [1.47, 1.95] / 1.72 [1.69, 1.76]; K=1 78.4 / 81.2 / 84.1%; req-weighted median K 4 / 2 / 2 | r2_trace_summary REPLICATES |
| 2.3·10⁵–7.7·10⁵ tokens/s; 100–400× synthetic | derived 226,150/2,000 = 113; 768,027/2,000 = 384 |
| table rows (scaled, Δ=10 ms): per type N1 0.02%, median 547, 335 B, 1.08 cores, 1.6 / 61.8 µs, 345 B; VIP 0.02%, 2,164, 390 B, 0.73, 1.8 / 38.7, 394 B; cluster 0, 4,369, 425 B, 0.38, 1.9 / 17.6, 426 B; M2 176.7 cores, 53.8 / 87.3 µs, 1,869 B | r2_trace_summary TREE SIZES and EDGE CPU (shared and reqspread:1000 rows); `tab_r2_trace.tex`. Cluster reqspread 17.55 printed 17.6 (the generated .tex rounds to 17.5) |
| sampled rows: per type 91.5%, median 1, 163 B, 0.0256 cores, 51.4 / 87.3 µs, 1,833 B; M2 0.0269 cores | r2_trace_summary sampled tenant fixed:0.01; issuer_cores_m2 0.02692 (`tab_r2_trace.tex`) |
| 66 tokens/s (sampled) | `tab_r2_trace.tex` tokens/s sampled |
| 1.08 [0.91, 1.26] vs 176.7 [96.9, 256.6]; 0.38 [0.23, 0.54] | r2_trace_summary scaled tenant/global fixed:0.01 |
| leaf/encode 0.76 µs/token ≈ 0.33 cores | r2_trace_summary RATE THRESHOLDS t_tok 0.761 µs; derived 0.761e-6 × 432,269 = 0.329 |
| ≥ 10× above 1,021 tokens/s at Δ = 10 ms | r2_trace_summary RATE THRESHOLDS |
| 99.5–99.9% of tokens in type pools ≥ 10³/s | r2_trace_summary POOL RATES tenant "token share in groups >= 1000/s" 0.997 / 0.995 / 0.999 |
| Δ = 1 s: median 54,780 per type; 477 B | scaled tenant fixed:1 medianN 54780, tokB 477 |
| V = 10 min / 24 h (nha): median 312 / 245 | `trace_oprg_V600.csv`, `trace_oprg_V86400.csv` (r2_trace_summary V sensitivity) |
| 1,000 hosts: EMBER cluster 16.7–17.6 vs M2 53.8–87.3 µs | scaled global fixed:0.01 keyshard:1000 16.67, reqspread:1000 17.55; M2 53.79 / 87.30 |
| contacts/request: M2 0.53–0.86; EMBER cluster 0.0002–0.16 | r2_trace_summary contacts/req (shared 0.5308 / 0.0002; reqspread 0.8628 / 0.1554) |

### §VII Discussion and limitations
| Claim | Source |
|---|---|
| rule 2/4 numbers (K*, 28×, 4.4×, 0.38 vs 177, 99.5–99.9%, ~10³/s) | as above |
| rule 4: 51.4 vs 53.8 µs on the sampled trace | sampled tenant fixed:0.01 shared EMBER 51.37, M2 53.79 |
| rule 3: 1.6–1.8× fleet edge crypto, 120–184 B, 5.4 ms | unchanged, oprg (§VI-C rows above) |
| trace limitation 100–400× | derived above |

### Prototype R2 (`RESULTS_R2_PROTO.md`; run 2026-11-06 17:22–18:09 UTC; mean [Student-t 95% CI] over 5 runs; `agg_r2.py`)
| Claim | Location | Source |
|---|---|---|
| P1 R2: B1 25.90 [25.03, 26.76]; M2 25.35 [24.01, 26.70]; pooled EMBER 2^5 27.23 [26.50, 27.96]; B5 77.52 [73.79, 81.25] µs/req; tokens 100/83/202/3284 B | Abstract, Table P1, §VI-B | `proto_capacity_r2_agg.csv` edge_cpu_us_per_req_mean/ci, token_bytes (K = 150: `run_r2.sh` p1 `-K 150`, tree 32) |
| M2 throughput ratio 1.02 [0.94, 1.10] | §VI-B | `proto_capacity_r2_agg.csv` b5s ratio_vs_b1 1.0212 [0.94268, 1.0998] |
| pooled EMBER 5% more than HMAC | §VI-B | derived 27.23/25.897 = 1.051 |
| link-bound 24.4–24.7k req/s; B5 edge-bound 12,226/s | §VI-B | `proto_capacity_tb_r2_agg.csv` req_per_s_mean b1 24,678, b5s 24,420, o1 24,600 (util 0.69–0.71); b5 12,226 (util 0.989) |
| P2: M2/EMBER added p50 −0.11 … +0.01 ms, CIs include 0; B5 +0.81 [0.77, 0.84] and +1.55 [0.94, 2.16] ms | §VI-B | `proto_latency_r2_agg.csv` added_p50_ms_vs_hmac: b5s 0.006 [−0.045, 0.057] (0.5), −0.052 [−0.203, 0.099] (0.8); o1 −0.0044 [−0.026, 0.017], −0.106 [−0.258, 0.046]; b5 0.806 [0.769, 0.843], 1.548 [0.938, 2.157] |
| P4 setup: 200 tokens/s per scheme, V = 10, p_move 0.01, 30-s window, event at 15 s, caps 64/256, 5 runs | §V, §IV-A | `experiments/proto/run_r2.sh` (P4_DUR 30s, P4_EVENT_AT 15, P4_PMOVE 0.01, `-p4pipes m2:200:11,ember:200:12 -V 10 -kmean 20`) |
| ~20.6 requests per token (P4); "about 20" | §VII-B | `proto_recovery_r2_agg.csv` requests_per_token_mean 20.604 (m2), 20.483 (ember) |
| flush: retry +35.8 ms mean, p99 62 ms | §IV-A, Abstract ("about one extra round trip"), §VII-A | `proto_recovery_r2_agg.csv` flush m2 retry_extra_mean_ms 35.78, p99 62.37 (ember 35.81 / 61.93) |
| base RTT 20.3 ms | §IV-A | `proto_recovery_r2_agg.csv` cold req_lat_p50_ms 20.304 / 20.307 |
| restart: reconnect 263 ms mean (p99 427), EMBER 258 ms; ~13 RTTs | §IV-A, Abstract, §VII-A, Conclusion | restart m2 reconnect_extra_mean_ms 262.9 [234.5, 291.3], p99 426.67; ember 257.67; derived 262.9/20.3 = 12.95 |
| ~6 recoveries per 1,000 requests per flush/restart; no failures | §IV-A | recoveries_per_1k_req: flush m2 6.08, ember 4.40; restart m2 6.17, ember 6.38; fails_mean 0 in all rows |
| cache 64: M2 retries on 55% of requests (551 [533, 570] per 1,000); EMBER 10% (100 [87, 113]); M2 median latency 41.7 ms ("doubled" vs 20.3–20.4) | Abstract, §IV-A, §VII-A | evict64 m2 retries_per_1k_req 551.22 [532.93, 569.51], affected_frac 0.551; ember 100.06, 0.100; req_lat_p50 41.709 vs ember 20.371; derived 41.7/20.3 = 2.05 |
| ~6,000 tokens per run | §IV-A | tokens_mean 5,976.6 (m2), 6,012.8 (ember) |
| cache 256: neither retried | §IV-A | evict256 m2 retries_per_1k 0.044 [−0.077, 0.165] (CI includes 0); ember 0 |

### Changed or removed numbers (R2 writer)
| Change | Location | Source |
|---|---|---|
| "Separate P1 campaigns differed by about 10%" → "up to 26% (B1: 20.54, 22.80, 25.90 µs), M2/HMAC ratio 0.98" | §VII-B | `proto_capacity_agg.csv` b1 20.54; `proto_capacity_r1_agg.csv` b1 22.796, b5s 22.328 (ratio 0.979); `proto_capacity_r2_agg.csv` b1 25.897, b5s 25.353 (ratio 0.979); derived 25.90/20.54 = 1.26 |
| "recovery costs one RTT (20.98 ms)" replaced by the P4 measurements | §IV-A | superseded; the 20.98 ms (`proto_rtt.csv`) is no longer cited |
| "We did not measure how often recovery occurs" removed; replaced by P4 per-event rates (production frequency still unknown) | §IV-A | as above |
| Appendix P2 (R1): utilisation relabelling (0.35–0.40 / 0.57–0.64) and the 260–450 / 624 Mbit/s figures dropped for space; remaining values unchanged | App. A | `proto_latency_r1.csv` |
| §VI-B "Its absolute values differ by about 10% for B1 (20.54 vs 22.80 µs)" removed (now in §VII-B) | §VI-B | — |
| Pull misses when λΔw_v ≫ 1: M ≈ E/(λΔ) | §IV-C | analytic limit of Eq. (miss): 1 − e^{−x} → 1 |
| Fig. 13 → `fig13` at 0.88 textwidth; fig14/fig12 resized (0.62/0.58 textwidth); fig12 moved earlier in the source | layout only | no data change |
| "about 36 ms (1.8 round trips)" on a live connection; "258–263 ms reconnect" | Abstract, §IV-A, §VII-A, Conclusion | flush retry_extra_mean 35.78 (m2) / 35.81 (ember) ms; derived 35.8/20.3 = 1.76; restart reconnect_extra_mean 257.67 (ember) – 262.9 (m2) ms |

### Final check R2 (corrections)
| Change | Location | Source |
|---|---|---|
| "about 6 recoveries per 1,000 requests" → "4.4--6.4" (EMBER flush is 4.40) | §IV-A | `proto_recovery_r2_agg.csv` recoveries_per_1k_req: flush m2 6.08, ember 4.40; restart m2 6.17, ember 6.38 |
| Retry hint "403 with X-Reject" → R2 uses 401 with a `Staple-Required` header (R1 used 403) | §IV-A | `experiments/proto/edge/r2.go` (`-staple-status` default 401; `stapleRequired` sets `Staple-Required`); `run_r2.sh` P4 `-ember-miss 401` |
| P4 EMBER epoch Δ = 100 ms | §V | `run_r2.sh` P4 issuer `-kids 12:100` (kid:delta_ms) |
| Abstract trimmed to 244 rendered words; R1 P1 pair (22.33 vs 22.80) dropped from the abstract, still in Table III | Abstract | unchanged sources |
