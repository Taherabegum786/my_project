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
