# NUMBERS_TRACE: every numeric claim in the EMBER manuscript, mapped to its source

All paths are relative to `paper/results/`. "run 1" / "run 2" refer to the two native OpenSSL 3.5.4 runs:
- run 1 (before the VM reboot) is in `native_run1/`;
- run 2 (after the reboot) is in the top-level `native_*_agg.csv` files.

Primitive tables and figures use run 2. Every simulation uses run 1 (`sim_params.json`, `*_costs_dir`).
"Derived" means arithmetic done on the listed values, with the formula shown.

## Abstract / Introduction / Conclusion
| Claim | Source |
|---|---|
| Token sizes 3,350 (B5) to 22,907 (B8) B; B6 4,535; B7 10,598 | `token_sizes.csv` rows with `url_path_len=60, with_ip=0`, column `token_bytes` |
| EMBER token 503 B at N=2^16 | `token_sizes.csv` O1, n=16, log2N=16, path 60 |
| Warm verify 2.34 µs (native) | `native_pathverify_agg.csv` impl=evp, d=16, n=16, ns_median 2341.2 [2334.1, 2455.5] (run 2) |
| 43× less than ML-DSA-44 verify | derived: 100.9 µs (`native_sig_agg.csv` ML-DSA-44 verify) / 2.3412 µs = 43.1 |
| 7.9× HMAC | derived: 2341.2 ns / 297.1 ns (`native_pathverify_agg.csv` op=hmac) = 7.88 |
| 1.28 million tokens/s per issuer core | `native_issuer_agg.csv` ML-DSA-44, N=16384, n=16: tokens_per_s 1,275,990 |
| 0.144× header bytes of B5c (HTTP/2, URL) | derived from `wire_bytes.csv`: O1 N=2^14 url h2-hpack 66,344 / B5c cookie2 h2-hpack 460,984 |
| 0.049% of requests wait (stapling) | `sim_delta_sweep.csv` mode=pull_staple, Δ=0.01, λ̄=2000, frac_req_waiting (mean over 5 reps); RESULTS_A §5 |
| Controller no better than fixed 10 ms | `controller_paired.csv`, `sim_controller_summary.csv` (see Table controller) |
| Roll-up removed only 1.4–2.2% of misses | derived: `sim_dissem.csv` E=500, Δ=1: pull 6,098 vs pull_rollup 6,011 per 1e6 req (1.4%); `sim_delta_sweep.csv` Δ=0.01: 1.069 vs 1.045 misses/token (2.2%) |
| Hybrid root +41.6% simulated edge CPU | `sim_sens_raw.csv`, root_signer hybrid vs ML-DSA-44, edge_cpu_us_per_req_mean 2.37 vs 1.67 (RESULTS_A §9, H7) |
| 13 baselines | B1–B13, Table baselines (design.md §5) |
| Misses/token within 4.4% in 24/24 configurations | `proto_validate.csv` metric=miss_per_token, max \|rel_err_mc\| 0.044, pass_mc True ×24 |
| Industry target ~2029 | cited [cf2026roadmap] (not a measurement) |

## Section IV (design)
| Claim | Source |
|---|---|
| 26-byte tweak; 30-byte header | `experiments/ember/th.py`, `ember/token.py`; RESULTS_A §0 (spec deviation) |
| Eq. (2) reproduces all 26 measured sizes exactly | `model_check.csv` quantity=token_bytes, rel_err 0.0000 (26 rows) |
| Padding ≤12% issuer slowdown | `issuer_throughput.csv` (Python): N=1000, 54.5k → 47.7k tokens/s |
| 51 tests; 128 cross-implementation vectors | `experiments/tests/test_ember.py` (pytest: 51 passed); `raw/proto/go_test.log` |
| Revocation entry 8 B | design: (epoch 4 B, index 4 B) |
| ~2^43 quantum collision cost for 128-bit output | generic BHT bound 2^(128/3) (design.md §4.6; analytic, not measured) |

## Section V (dissemination)
| Claim | Source |
|---|---|
| Stapled header 2.4 KB for ML-DSA-44 | ML-DSA-44 signature 2,420 B (FIPS 204) plus root fields |
| Root signature 2,420 B per token if carried | FIPS 204 |
| 25-point grid [0.01, 60] s; SLO 2 s; B = 1024; EWMA 0.2 | `sim_params.json` |

## Section VI (methodology)
| Claim | Source |
|---|---|
| 4 vCPU Xeon 2.1 GHz, AVX-512, SHA-NI, KVM, Linux 6.18 | `env.txt` |
| pqcrypto ML-DSA-44 sign 15.4× native | `notes_A1_mldsa_sign.md`; derived: 6,301 µs (`micro_primitives.csv`) / 408.8 µs |
| Run 1 vs run 2: 501.8/122.3 vs 408.8/100.9 µs; 2,846.9 vs 2,341.2 ns | `native_run1/native_sig_agg.csv`, `native_run1/native_pathverify_agg.csv` vs top-level files |
| 118-B canonical claims | `token_sizes.csv` claims_bytes for path 60 |
| ~570 B other headers; K=150; 4096-B table | RESULTS_B §1; `experiments/proto/hpackbytes/` |
| Link delays 10 / 37.5 ms; 1 Gbit/s; MTU 1500 | RESULTS_B testbed; `raw/proto/net_check.txt` |
| RTT 20.98 / 76.10 ms (mean keep-alive) | `proto_rtt.csv` (RESULTS_B §5) |
| P1: 64 conns, 150 req/token, 5 s + 20 s, 5 runs | `experiments/proto/run_proto.sh`; RESULTS_B §3 |
| P3: 24 configurations, 60 s window, 5 runs | `proto_p3_config.json`, `proto_p3_runs.csv` |
| DES vs MC: 0.56% / 0.09% / 0.08%; 45 rows | `sim_validate.csv` (RESULTS_A §5) |
| Table simparams values | `sim_params.json`, `tables/tab4_simparams.tex` |

## Section VII (results)
### A. Size and wire bytes
| Claim | Source |
|---|---|
| B9 3,435; B1 166; B2 209; B4 465; B12 171; B11 214; B10 k=3 187 | `token_sizes.csv` path 60 |
| 0% of B5/B6 URLs fit 2 KB; 0% of B6 cookies fit 4 KB; B7/B8 fit nothing | `fit.csv`, `tables/tab3_fit.tex` |
| O1: 375 (2^10), 503 (2^16), 588 (2^20), 673 (2^24); O2 844 at 2^16 | `token_sizes.csv` |
| ~21 B per level | derived: (503 − 375)/6 = 21.3 |
| 6.7× smaller than B5 | derived: 3,350 / 503 = 6.66 |
| B13 504 B at a 2^16 series | `token_sizes.csv` B13 rows (RESULTS_A §3) |
| Table wire-bytes rows | `wire_bytes.csv`: session_bytes for h2-hpack, http1.1 and h2-hpack-t64k |
| 0.256× in HTTP/1.1 | derived: 151,451 / 592,522 |
| ~87 KB token-independent headers | `wire_bytes.csv` none/http1.1 86,823 |
| 3,036.9 B per request | `wire_bytes.csv` B5 cookie h2-hpack bytes_per_req_mean |
| Staple +2,954 B per session | derived: 69,298 − 66,344 |

### B. Edge verification
| Claim | Source |
|---|---|
| Table primitives (sign/verify medians, CIs) | `native_sig_agg.csv` (run 2); `tables/tab2_primitives.tex` |
| ML-DSA-44 verify 100.9 [100.2, 120.4]; Ed25519 94.6 | `native_sig_agg.csv` |
| d ≤ 8 → 4.3×: 1,283.9 ns | `native_pathverify_agg.csv` d=8; derived 1283.9/297.1 = 4.32 |
| 0.75 µs at d=4, 3.41 µs at d=24; ~0.13 µs per level | `native_pathverify_agg.csv`; derived (3407.0 − 751.7)/20 = 132.8 ns |
| Go: 3.074 µs, HMAC 0.853, ML-DSA-44 32.76; 3.6× and 10.7× | `proto_go_verify_agg.csv`; derived 3.074/0.853 = 3.60; 32.76/3.074 = 10.66 |
| circl 3.6–4.0× faster than OpenSSL | RESULTS_A §1 cross-implementation check (`proto_go_verify.csv` root verify 25–28 µs vs 100.9 µs) |
| P1 numbers | see the P1 section below |

### C. Issuer
| Claim | Source |
|---|---|
| ≈2,446 tokens/s per-token ML-DSA-44 | derived: 1 / 408.8 µs |
| 469,254 [319,698, 729,692] at 2^8; 1,275,990 [1,161,768, 1,282,009] at 2^14 | `native_issuer_agg.csv` |
| 192× and 522× | derived: 469,254/2,446 = 191.8; 1,275,990/2,446 = 521.7 |
| SLH-128s per-token ≈ 3.26 tokens/s; 49,063 at 2^14 | derived 1/306.464 ms; `native_issuer_agg.csv` SLH-DSA-128s N=16384 |
| D 0.575 → 0.927 s with SLH-128s root | `sim_sens.csv` param=root_signer (RESULTS_A §5) |
| B11 ~33,000 tokens/s; ≥14× | derived 1/30.1 µs = 33.2k; 469,254/33,223 = 14.1 |
| B12 wraps 37.6 ms at E=500 | `issuer_throughput.csv` B12 wrap rows (Python) |
| Go issuer ~432k tokens/s at N=1024; 53× | `proto_go_verify_agg.csv` issue_epoch_1024 2,372 µs → 1024/2.372 ms; sign_token_b5 123.9 µs → 8.07k/s |

### D. P2
| Claim | Source |
|---|---|
| B2 −1.25, B3 −1.39 ms at 50% | `proto_latency_agg.csv` added_p50_ms_vs_hmac_mean |
| O1 −3.24 [−6.82, 0.34]; B5 +11.47 [5.09, 17.85]; B5v p50 80.05 | `proto_latency_agg.csv` load_frac 0.80 |
| 9.5k / 16.4k req/s; ~260 / 450 Mbit/s; tapbridge ~624 Mbit/s | `proto_latency_agg.csv` rate_achieved; RESULTS_B §4 (derived) |
| zero errors | `proto_latency_agg.csv` errors_total |

### E. Dissemination / end-to-end
| Claim | Source |
|---|---|
| Table operating points | `sim_delta_sweep.csv` λ̄=2000, E=500 (means over 5 reps; RESULTS_A §5) |
| Model 0.862 vs simulated 0.921 | `sim_delta_sweep.csv` pull, Δ=1, columns model_miss_per_token, miss_per_token |
| Re-route sensitivity: 0 / 0.058 / 0.56 | `sim_sens.csv` param=p_move |
| 387 vs 6,098 misses per 1e6 req | `sim_dissem.csv` E=500, Δ=1 |
| Staple fleet bandwidth 0.46–0.65 MB/s; push 140 MB/s–2.75 GB/s; B12 57 MB/s–1.13 GB/s; B11 0.08–1.5 MB/s | `sim_dissem.csv` root_bw_fleet_Bps (means) |
| Push 2.27 GB/s at Δ=0.01 | `sim_delta_sweep.csv` push Δ=0.01 root_bw_fleet_Bps |
| Revocation propagation 150 s | `sim_dissem.csv` revocation_propagation_s |
| E2E p99 / p99.9 / >1 ms shares | `sim_e2e_latency.csv` (RESULTS_A §5 table) |
| Simulated edge CPU 1.2–1.7 µs | `sim_delta_sweep.csv` edge_cpu_us_per_req_mean (pull) |
| Hybrid 20.27 vs 19.98 µs (+1.5%) | `token_verify.csv` O4/O1 warm N=2^16 |

### F. Controller
| Claim | Source |
|---|---|
| Table controller values | `controller_paired.csv`, `tables/tab5_controller.tex` |
| WC better by 4.93 / 4.41 ms; 1.0 ms worse at 20000 | `controller_paired.csv` policy=wc diff |
| Fixed Δ ≥ 3 s violates SLO in all bins | `sim_controller_summary.csv` slo column |

### G. Validation
| Claim | Source |
|---|---|
| 24/24, 4.4%, model 14.8% | `proto_validate.csv` |
| 0.05116 [0.05036, 0.05196] vs 0.05067 | `proto_validate.csv` pull/pull_staple V=10 Δ=1 λ=200 miss_per_token |
| 8/8 pull Δ ≤ 1: 76.9–78.5 vs 75.9 ms | `proto_validate.csv` metric miss_lat_mean_ms |
| Δ=10: 118–137 ms; ~4,400 tokens; first-request p50 136.8 vs 23.6 ms | `proto_validate.csv`; RESULTS_B §5 (`raw/proto/p3_req_*.csv.gz`) |
| Staple 0.074–0.086 vs 0.026 ms | `proto_validate.csv`; `sim_proto_mc.csv` |
| 36–45% under-prediction | `proto_validate.csv` rel_err_mc (0.36–0.446) |

### H. DoS
| Claim | Source |
|---|---|
| 9,270–9,636 fetches/s, 4,630 verifs/s, 0.48 core; 7,680 → 65; 10^4 verifs, 1.03 cores; 100/s, 0.027 | `dos.csv` attack_rate 10000 rows |

### Trust table
| Claim | Source |
|---|---|
| All values | `tables/tab6_trust.tex` (from `token_sizes.csv`, `native_*_agg.csv` run 2, `sim_dissem.csv`) |
| B5v hit 2.19 µs | `native_pathverify_agg.csv` op sha256 over 3.5 KB token (2,191 ns) |
| ~3× larger than HMAC | derived: 503/166 = 3.03 |

## Section VIII (discussion, limitations)
| Claim | Source |
|---|---|
| +341 B for n=32 at 2^16 | derived: 844 − 503 |
| B12 283 MB/s at E=500 | `sim_dissem.csv` B12 E=500 (283,521 kB/s) |
| Hypothesis table | the rows above; RESULTS_A §9, RESULTS_B §6 |
| P1 contended runs, utilisation 0.84–0.88 | `raw/proto/proto_capacity_contended.csv` runs 3–5; RESULTS_B §3.1 |
| Emulator 624 Mbit/s | RESULTS_B §4 |

## P1 (quiet rerun)
(filled in after the rerun; see below)
