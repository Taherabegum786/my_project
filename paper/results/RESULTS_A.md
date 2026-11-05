# RESULTS_A: EMBER library, benchmarks (E1, E1n, E2/E2+, E3), simulation (E5), DoS (E7)

Experimenter A, 2026-11-05. Every number below was produced by code in `paper/experiments/` and is read from the CSV
named next to it. Reproduction: `paper/experiments/README.md` and `run_all.sh`. Nothing is interpolated or projected.
Model values are labelled **model**. Simulated values are labelled **simulated**. Every timing names its implementation.

**Statistics.**
- Native microbenchmarks: 5 fresh processes pinned to core 2. Reported value = median of run medians, with a bootstrap 95% CI over run medians (2000 resamples) and pooled p99.
- Python microbenchmarks: one pinned process, with a bootstrap CI of the median.
- Simulations: Student-t 95% CI over seeds, using common random numbers (seed `20261105 + 1000·r`) across policies and modes, plus paired-difference CIs.

**Machine.** One 4-vCPU KVM guest (Xeon @ 2.1 GHz, SHA-NI/AVX-512), described in `env.txt`. The VM was rebooted between
the first and second halves of this work; see the anomalies section.

---

## 0. Correctness (prerequisite)

- `pytest -q tests/` gives **51 passed** (`tests/test_ember.py`). Coverage:
  - round trips at N ∈ {1, 2, 3, 5, 8, 1000, 1025} × n ∈ {16, 32}, plus all N ≤ 69 for the tree code;
  - rejection of single-bit flips in the claims (every byte), salt, path and index;
  - epoch swap, wrong-kid and relabelled-kid roots, cross-kid replay;
  - expiry, and the `Expires > T_start+Δ+V_max` bound;
  - clock skew: ±τ accepted, 2τ rejected, at both the expiry and the validity-bound boundaries;
  - revocation (including a tampered delta) and a tampered period-bundle list;
  - each half of the hybrid root;
  - cross-tenant replay in a pooled tree;
  - `idx ≥ N` rejected, and the epoch counter refusing to wrap;
  - negative cache, stapled root (valid and invalid), and pad-to-2^d;
  - valid/tampered/expired tokens for every per-token baseline: B1–B9, B5v/B6v with the cache respecting `Expires`, B10 per-domain tags for k = 1/3/10, B11 (expired delegated key and non-certified key rejected), B12 (wrong-epoch key rejected, wrap bound to its epoch and its edge), B13 MTL, B5c split.
- `tests/vectors.json` (from `python -m tests.gen_vectors`) is the shared test-vector file. B's Go port verifies it identically: 128 cross-implementation checks (RESULTS_B §0).
- **Spec deviation (documented in `ember/th.py`).** The tweak is **26 B**: the spec's 22 B plus a 4-B tenant id in leaf tweaks, so that pooled trees separate tenants (Critic D6).

## 1. E1n: native primitives (PRIMARY, OpenSSL 3.5.4)

Sources: `native_sig_agg.csv`, `native_pathverify_agg.csv`, `native_issuer_agg.csv`. Command: `CORE=2 bash bench/native/run_native.sh ../results`.
Implementation for all rows: `impl=openssl-3.5.4-native`. Values are µs, as median [95% CI]. This is **run 2** (after the reboot).

| op | ML-DSA-44 | ML-DSA-65 | ML-DSA-87 | SLH-128s | SLH-128f | Ed25519 | ECDSA-P256 | RSA-2048 |
|---|---|---|---|---|---|---|---|---|
| sign | 408.8 [386.9, 452.4] | 676.5 [673.5, 682.7] | 808.7 [796.3, 871.5] | 306,464 [300,201, 312,495] | 14,436 [14,294, 14,486] | 30.1 [30.1, 30.5] | 23.0 [22.9, 31.1] | 314.1 [309.4, 340.5] |
| verify | **100.9 [100.2, 120.4]** | 154.8 [154.6, 165.8] | 244.8 [243.5, 250.0] | 288.1 [282.4, 320.0] | 873.2 [862.3, 883.6] | 94.6 [93.8, 96.2] | 69.6 [69.5, 70.0] | 20.7 [18.8, 24.2] |

- ML-KEM-768 encaps / decaps: 19.3 / 30.0 µs.
- ML-DSA-44 verify falls in the tens-to-hundreds-of-µs range required by the spec's sanity rule.
- **Edge per-request primitives** (`native_pathverify_agg.csv`, EVP with prefetched SHA-256, 5 runs × 2·10⁵ verifications, values in ns):
  - HMAC-SHA256 over the 200-B claims: 297.1 [296.1, 303.1].
  - EMBER path verification at n = 16 (leaf + d nodes + compare):
    - d = 4: 751.7
    - d = 8: 1,283.9
    - d = 11: 1,678.1
    - d = 16: **2,341.2 [2,334.1, 2,455.5]**
    - d = 20: 2,875.9
    - d = 24: 3,407.0
  - Measured for every d in 0..24; the simulator never interpolates.
  - One Th call: 125.9 ns on 64 B; 207.4 ns on 200 B.
  - SHA-256 of a 3.5 KB token (the B5v cache key): 2,191 ns.
  - The low-level `SHA256_*` variant (`impl=ll`) is 7–13% faster: d = 16 is 2,108.8 ns; HMAC with precomputed pads is 276.7 ns.
- **Native issuer** (`issuerbench.c`; leaf hashing + tree + one root signature + base64url encoding of N tokens; 5 processes, values in tokens/s per core [CI]):

  | root signer | N = 1 | N = 2⁸ | N = 2¹⁴ | N = 2¹⁸ |
  |---|---|---|---|---|
  | ML-DSA-44 | 1,579 | 469,254 [319,698, 729,692] | **1,275,990 [1,161,768, 1,282,009]** | 1,133,291 |
  | SLH-DSA-128s | 3.1 | 796 | 49,063 | 477,337 |
  | SLH-DSA-128f | — | — | 549,089 | 1,006,770 |

  For n = 32 (ML-DSA-44 root): 828,577 tokens/s at N = 2¹⁴.

**Cross-implementation check.** The Docker oqs-ossl3 probe (`probe_openssl_speed.csv`, single run) gives ML-DSA-44 sign/verify 675/123 µs. B's Go circl gives ML-DSA-44 root verify ≈ 25–28 µs (`proto_go_verify.csv`). All implementations are within the spec's 3× bound of OpenSSL 3.5.4 except circl verify, which is 3.6–4.0× faster than OpenSSL. That is consistent with circl's optimised NTT and is noted, not hidden. pqcrypto is examined under A1 below.

## 2. E1: Python primitives (secondary) and anomaly A1

Source: `micro_primitives.csv`, raw samples in `raw/micro_*.npy`. Command: `taskset -c 2 python -m bench.bench_primitives --out ../results`.

- **A1** (`notes_A1_mldsa_sign.md`). pqcrypto 1.0.0 ML-DSA-44 sign has a median of 6,312 µs. That is **15.4× native OpenSSL** sign, while pqcrypto verify is only 1.2× native and keygen 1.5×.
- The API path does not explain it: flat vs object API, context string, 32-B vs 200-B message, and pure vs HashML-DSA all fall within 1.1% of each other.
- The extension is the Rust crate `backbone-ml-dsa-0.2.0` with its portable `src/backends/soft.rs` backend, which inflates the NTT-heavy rejection loop of signing.
- **Consequence:** every issuer/sign claim uses native numbers. pqcrypto sign times appear only as "Python backend".

## 3. E2/E2+: tokens (sizes, edge verify, issuer)

**Sizes** (`token_sizes.csv`; 60-char path, no IP, 118-B canonical claims; actual generated tokens):

| scheme | token bytes | signed URL bytes | Set-Cookie value bytes |
|---|---|---|---|
| B1 HMAC | 166 | 256 | 177 |
| B10 multi-MAC, k = 1 / 3 / 10 | 145 / 187 / 337 | | |
| B12 | 171 | | |
| B11 | 214 | | |
| B2 Ed25519 / B3 ECDSA / B4 RSA | 209 / 217 / 465 | | |
| B5 ML-DSA-44 | **3,350** | 3,440 | |
| B6 ML-DSA-65 | 4,535 | | 4,546 |
| B9 hybrid | 3,435 | | |
| B7 SLH-128s | 10,598 | | |
| B8 SLH-128f | 22,907 | | |
| B5c / B6c, largest single cookie | | | 1,687 / 2,280 |

- **EMBER O1 (n = 16), token bytes:**
  - N = 1: 161
  - N = 2¹⁰: 375
  - N = 2¹⁶: **503**
  - N = 2²⁰: 588
  - N = 2²⁴: 673
- O2 (n = 32): 844 at N = 2¹⁶ and 1,185 at N = 2²⁴.
- O3/O4 have the same sizes as O1; the root signer does not affect token size.
- B13 MTL condensed signature: 504 B for a series of 2¹⁶ and 589 B for 2²⁰. That is identical to EMBER at the same tree size; the difference is that the MTL series grows with λ·V_max, not λ·Δ.
- **Model check** (`model_check.csv`): the token-size formula `c_enc + 3 + ⌈4(30 + n·d)/3⌉` has a relative error of **0.000** at every measured point (26 rows).

**Edge verify, Python** (`token_verify.csv`; full parse + policy + crypto; 5000 distinct-token verifications; median µs [CI]):

| scheme | median µs [CI] | notes |
|---|---|---|
| B1 | 5.36 [5.36, 5.37] | |
| B12 | 5.59 | |
| B4 | 25.7 | |
| B3 | 75.7 | |
| B2 | 107.0 | |
| B11 | 107.6 | |
| B5 | 128.1 [127.8, 128.6] | |
| B6 | 211.8 | |
| B9 | 234.9 | |
| B7 | 295.5 | |
| B8 | 827.8 | |
| B5v | hit 3.04, miss 131.1 | amortised over K = 150: **3.89 µs/req** |
| EMBER O1, warm cache | N = 2⁸: 12.2; N = 2¹⁶: **19.98 [19.95, 20.02]**; N = 2²⁰: 23.8 | |
| EMBER O1, cold (includes root verify) | N = 2¹⁶: 143.6 | |
| O1 + vcache | | amortised **1.58 µs/req** |
| O4 hybrid, warm, N = 2¹⁶ | 20.27 | |
| B13, warm, 2¹⁶ | 17.4 | |

- **Model check, edge verify:** the Python-overhead model under-predicts the warm EMBER verify by 26–40% (`model_check.csv`, `edge_verify_us`). The model omits base64 and parse costs that grow with path length. The native numbers in §1 are the ones to cite.

**Issuer.**

`issuer_throughput.csv`: one core, Python hashing with a pqcrypto root signature.
- Per-token: B5 143.5 tokens/s, B7 3.7 tokens/s, B2 27.7k tokens/s.
- EMBER with an ML-DSA-44 root: 24.5k tokens/s at N = 2⁸ and 151.5k tokens/s at N = 2¹⁴.
- pad-to-2^d costs at most 12% (N = 1000: 54.5k → 47.7k tokens/s).

`issuer_throughput_mp.csv`: one shard per core, each worker pinned to its own core.
- B5: 154 → 606 tokens/s.
- EMBER at N = 2¹⁴: 137k → **565k tokens/s with 4 processes**.

B12 per-epoch wrap cost (Python ML-KEM + HKDF + AES-GCM; wrap = 1,136 B per edge):
- 37.6 ms for E = 500;
- 160.6 ms for E = 2000.

## 4. E3: fit (sanity check; `fit.csv`, `tables/tab3_fit.tex`)

URL path lengths are drawn from a lognormal with median 80 and σ = 0.5 (assumption), 10⁵ samples.
- **B5:** 0% of URLs fit in 2 KB; 100% fit in a 4 KB cookie. **B6:** 0% fit in a 4 KB cookie. **B7/B8:** 0% fit under any limit.
- **B5c/B6c:** 100% of cookies fit.
- **EMBER O1/O3:** 100% under every limit up to N = 2²⁴. At N = 2²⁴ the median signed URL is 810 B and p99 is 1,218 B.
- **EMBER O2:** 99.92% fit in a 2 KB URL at N = 2²⁴.

## 5. E5: fleet simulation (simulated; all crypto costs from native E1n **run 1**, `results/native_run1/`)

Defaults are in `sim_params.json` and `tables/tab4_simparams.tex`:
- E = 500 edges, Zipf(0.8) edge share, 50 shields;
- T = 1000 tenants, Zipf(1.0);
- K ~ geometric(150) requests per session, 4 s apart;
- edge re-route probability per segment 0.0005 (my mobility assumption: about 7% of sessions switch edge once);
- lognormal RTTs: edge→shield 15 ms, shield→root 60 ms, push 150 ms, token receipt → first request 120 ms.

Engine: `sim/engine.py` with a numba kernel in `sim/fleet_mc.py`, replaying every first request and every re-route request against per-edge and per-shield caches (with coalescing). Commands are `python -m sim.run_sim --exp X --reps 5 --procs 3`. The controller uses 10 seeds.

Horizons:
- sweep: 1 h stationary (λ̄ = 20000: **1200 s**, a recorded cut);
- controller: 24 h diurnal at λ̄ = 200 and 2000; 1 h peak window at 20000;
- dissem/e2e/sens: 1800 s.

**Model vs simulation.**
- With no re-routes (QUICK check), simulated first-request misses per token equal the analytic M(Δ) to 3–4 digits.
- In the full sweep (`sim_delta_sweep.csv`, column `model_miss_per_token`), the model under-predicts by the re-route misses. Pull mode, λ̄ = 2000, Δ = 1: simulated **0.921**, model 0.862 (Fig 5).
- **Internal consistency, DES vs MC** (`sim_validate.csv`, `tab7_validate.tex`; independent heapq DES; λ̄ = 200, E = 100, T = 50, 1 h, 5 seeds):
  - maximum |relative difference|: misses per token 0.56%, D 0.09%, issuance wait 0.08%;
  - paired-difference CI contains 0 in 43 of 45 rows (the two exceptions differ by 0.12% and 0.49%).

**Key operating points** (λ̄ = 2000, per-tenant trees, means over 5 seeds; CI half-widths below 1% of the mean; `sim_delta_sweep.csv`):

| mode | Δ | misses/token | D (ms) | requests waiting | root bytes / served bytes | edge CPU/req (mean / p99, µs) |
|---|---|---|---|---|---|---|
| pull | 0.01 s | 1.069 | 96.2 | 0.71% | 2.4e-5 | 1.19 / 0.72 |
| pull | 1 s | 0.921 | 575.4 | | | |
| pull_staple | 0.01 s | **0.073** (re-routes only) | **11.7** | **0.049%** | 1.6e-6 | |
| pull_staple | 1 s | 0.058 | | | | |
| push | 0.01 s | 0.622 | 19.8 | | **5.0e-3** | |
| push_rollup | 0.01 s | 0.997 | | 0.67% | 5.3e-5 | |

- push at Δ = 0.01 needs **2.27 GB/s** of root pushes. Push is slower than the client, because the 150 ms push delay exceeds the 120 ms receipt → first-request delay.
- Pooling 8 shards cuts misses only for Δ ≥ 1 s: pull at Δ = 10 drops from 0.676 to 0.178.

**Dissemination** (`sim_dissem.csv`, Fig 7; Δ = 1 s; λ̄ = 2000):
- Fleet root bytes/s at E = 100 / 500 / 2000:

  | scheme / mode | E = 100 | E = 500 | E = 2000 |
  |---|---|---|---|
  | EMBER pull | 6.8 MB/s | 8.4 MB/s | 9.5 MB/s |
  | EMBER pull_staple | 0.46 MB/s | 0.58 MB/s | 0.65 MB/s |
  | EMBER push | 140 MB/s | 689 MB/s | 2.75 GB/s |
  | EMBER push_rollup | 9.4 MB/s | 22.8 MB/s | 68 MB/s |
  | B12 (push of KEM wraps) | 57 MB/s | 283 MB/s | 1.13 GB/s |
  | B11 (certificates) | 0.08 MB/s | 0.38 MB/s | 1.5 MB/s |

- Misses per 10⁶ requests at E = 500: pull 6,098; pull_rollup 6,011; push 3,653; **pull_staple 387**.
- Revocation propagation (mean): pull modes 150 s (P/2 + RTT), push 0.17 s.
- The `edge_root_state_bytes` column is an **all-tenants upper bound** (4.4 GB per edge without roll-up, 65 MB with). From the simulated fetch rate (8.41 MB/s ÷ 2,501 B ÷ 500 edges × 3,600 s), an edge actually holds about 24k roots: ≈ 59 MB if it keeps signatures and ≈ 0.9 MB as 36-B verified entries. This is arithmetic on simulated values.

**End-to-end added latency per request** (`sim_e2e_latency.csv`, Fig 8; 5 × 20,000 samples per scheme/mode; native CPU):

| scheme / mode | p99 | share of requests > 1 ms | p99.9 |
|---|---|---|---|
| EMBER pull | 0.123 ms | 0.65% | 112 ms |
| EMBER pull_staple | **0.0017 ms** | **0.05%** | 0.12 ms |
| EMBER push | 0.0017 ms | 0.36% | |
| EMBER push_rollup | 0.123 ms | 0.58% | |
| B5 | 0.122 ms on every request | | |
| B5v | 0.125 ms | | |
| B1 | 0.0004 ms | | |

**Sensitivity** (`sim_sens.csv`, Fig 9; Δ = 1 s; 5 seeds):
- Misses in pull_staple come only from re-routes: 0 at p_move = 0, 0.058 at 0.0005, 0.56 at 0.005.
- An SLH-128s root raises D by ≈ 352 ms: 0.927 vs 0.575 s in pull, because its 306–352 ms signature sits in the issuance path.
- RTT ×0.5/×2 moves pull_staple D by −2.5/+4.9 ms.
- V_max, P and segment size do not change misses in this workload.
- The Δ × E heatmap is in Fig 9.

**Second cost source.** The same sweep run with Python E1 costs (`backend=python` rows) leaves misses unchanged. D rises by 7 ms because pqcrypto sign takes 6.3 ms, and mean edge CPU is 7.9 µs instead of 1.2 µs per request.

## 6. Controller (H5; `sim_controller_summary.csv`, `controller_paired.csv`, `tab5_controller.tex`, Fig 6)

24 h diurnal workload, pull mode, D in ms [t-CI], paired differences as adaptive − policy:

| λ̄ (seeds) | adaptive D | oracle best fixed Δ (per-decile, in hindsight; = best single = SLO-feasible) | paired (adaptive − oracle) | WC D |
|---|---|---|---|---|
| 200 (10) | 96.61 [96.59, 96.63] | 96.61, Δ = 0.01 in all deciles | **−0.001 ms [−0.004, +0.002]** | 91.68; WC is **4.93 ms better** than adaptive |
| 2000 (10) | 96.08 | 96.08, Δ = 0.01 | **+0.005 ms [+0.001, +0.010]** | 91.68; 4.41 ms better |
| 20000 (5, 1 h peak window) | 90.40 [90.03, 90.76] | 91.23, Δ = 0.01 | **−0.83 ms [−0.91, −0.75] (−0.9%)** | 91.45 |

- SLO and budget violations are 0 for the adaptive policy and for every Δ ≤ 1 s. Fixed Δ ≥ 3 s violates the SLO in 100% of 5-min bins.
- The adaptive controller selects the grid floor, Δ = 10 ms, essentially all day (Fig 6). In this workload, root misses barely fall with Δ until λ_τΔ ≫ E, so the interior optimum predicted in design §4.4 does not occur for any tenant at λ̄ ≤ 2000.

## 7. E7: DoS (`dos.csv`; one edge, 60 s, 5 seeds, native costs)

| variant | key space | fake tokens/s | root fetches/s | verifies/s | one-core CPU |
|---|---|---|---|---|---|
| naive or coalesce+neg | all tenants | 10⁴ | 9,270–9,636 | 4,630 | **0.48** |
| naive | lowest-rate tenant | 10⁴ | 7,680 | | |
| coalesce+neg | lowest-rate tenant | 10⁴ | **65** | | (key-space bound) |
| either | top tenant | 10⁴ | ≤ 79 | | |
| stapled-root flood | | 10⁴ | | 10⁴ | **1.03** |
| stapled-root flood + 1/s per-client limit (100 clients) | | 10⁴ | | 100 | 0.027 |

- With fake tokens spread over all tenants, coalescing and negative caching do **not** help, because keys rarely repeat.
- Conclusion: per-client fetch/staple rate limits are required; coalescing and negative caching only bound single-tenant floods.

## 8. H8 support: fleet_mc at the E8 P3 configuration (B's prototype is the ground truth)

- Command: `python -m sim.fleet_mc --proto-p3 ../results 50` writes `sim_proto_mc.csv` (50 seeds). Inputs: E = V, unpermuted Zipf(0.8), no shield tier, RTT lognormal fitted to `proto_rtt.csv` (median 75.88 ms, σ = 0.017), plus the Go root-verify median of 0.026 ms. B's `proto/validate.py` then writes `proto_validate.csv` (Fig 12).
- **misses/token:** 24/24 configurations pass (within 15% or inside the prototype CI). Maximum |relative error| is **4.4%**. The analytic model's maximum is 14.8%.
- **mean miss latency:** 8/24 pass.
  - **pull, Δ = 0.1 and 1 s (8/8 pass):** prototype 76.9–78.5 ms vs 75.9 ms simulated.
  - **pull, Δ = 10 s (fails):** prototype 118–137 ms with wide CIs (e.g. [79.6, 157.2]). The simulator predicts 75.9 ms. This is a prototype-side effect that the simulator does not model; B should explain it.
  - **pull_staple (12/12 fail):** prototype 0.074–0.086 ms vs 0.026 ms simulated. The simulator charges only the microbenchmarked verify, not decoding of the ≈ 3.3 KB `X-EMBER-Root` header. The absolute gap is ≈ 0.05 ms.

## 9. Hypotheses

| H | Outcome | Evidence |
|---|---|---|
| H1 size | **Partly supported.** <512 B holds up to N = 2¹⁶ (503 B) but not 2²⁰ (588 B). Bytes per session (B's E3b): EMBER/B5c = 0.144× in HTTP/2 URL form (supported) and 0.256× in HTTP/1.1 (just misses 0.25). In cookie form with a 64 KiB HPACK table the gap almost vanishes (9,358 vs 11,667 B). B11/B12 tokens are smaller than EMBER (214/171 B). | `token_sizes.csv`, `wire_bytes.csv` (RESULTS_B) |
| H2 edge CPU | **Partly supported.** Native warm path at d = 16 is 2.34 µs = **7.9× HMAC**, so ≤5× is **not** met (it holds only for d ≤ 8: 4.3×). It is **43× cheaper than uncached ML-DSA-44 verify** (≥10× supported). Against B5v the advantage shrinks to amortised per-request cost: Python 1.58 (O1v) vs 3.89 µs (B5v). Simulated EMBER pull is 1.2–1.7 µs per request including root verifies. Go P1 req/s is in RESULTS_B. | `native_pathverify_agg.csv`, `native_sig_agg.csv`, `token_verify.csv` |
| H3 issuer (Python) | **Supported.** At N = 2⁸, 24.5k vs 143.5 tokens/s (171×); 1,055× at 2¹⁴. With an SLH-128s root, the native issuer reaches 49k tokens/s at N = 2¹⁴. | `issuer_throughput.csv`, `native_issuer_agg.csv` |
| H4 dissemination | **Partly supported.** Root/served bytes < 0.1% for pull, staple and push_rollup at every Δ (max 5.3e-5), but **not** for per-tenant push at Δ ≤ 1 s (0.15–0.50%). Roll-up ≥ 5× miss reduction: **not supported**. Pull_rollup reduces aggregate misses by only ≈1.4–2.2% (6,098 → 6,011 per 10⁶ requests at Δ = 1; 1.069 → 1.045 misses/token at Δ = 0.01), because first requests arrive about 120 ms after issuance, before any period closes. Low-rate tenants were not separately reported. | `sim_delta_sweep.csv`, `sim_dissem.csv` |
| H5 controller | **Not supported → C4 is demoted to a guideline** under the pre-registered rule. Adaptive vs the oracle best fixed Δ: −0.001 / +0.005 / −0.83 ms (all ≪ 10 ms and ≪ 10%). Plain work-conserving beats adaptive by 4.4–4.9 ms at λ̄ ≤ 2000. | `controller_paired.csv` |
| H6 end-to-end | **Supported** for pull_staple (0.049% of requests wait) and push_rollup (0.67%). Edge CPU p99 is ≤ 2.6 µs, ≪ 1 ms. Plain pull: 0.71% wait, with p99.9 of 112 ms. | `sim_delta_sweep.csv`, `sim_e2e_latency.csv` |
| H7 hybrid | **Not supported in the default workload.** Warm per-request cost is unchanged (20.27 vs 19.98 µs Python, +1.5%), but with per-tenant trees each (edge, epoch) root serves about one session. The extra Ed25519 root verify therefore raises simulated mean edge CPU per request by **41.6%** (2.37 vs 1.67 µs; still µs-level). | `token_verify.csv`, `sim_sens_raw.csv` |
| H8 validation | **Partial** (B owns the verdict). The simulator matches prototype misses/token in 24/24 configurations (≤ 4.4%) and miss latency in 8/24 (see §8). | `proto_validate.csv` |
| H9 issuer (native) | **Supported for EMBER vs B5:** native EMBER is 469k tokens/s (N = 2⁸) and 1.28M (2¹⁴), vs 1/408.8 µs = 2,446 tokens/s for per-token ML-DSA-44 sign (192× / 522×). "B11/B12 comparable": **not supported** as stated. Native per-token Ed25519 sign (B11) is 30.1 µs, i.e. about 33k tokens/s, so EMBER is ≥14× faster. B12 tokens are HMAC-cheap, but each epoch costs E wraps (37.6 ms Python at E = 500). | `native_issuer_agg.csv`, `native_sig_agg.csv` |

## 10. Anomalies and deviations (please carry into the paper's methodology/limitations)

1. **Two native E1n runs differ by ~15–20%.** Run 1 (18:10–18:40, before a VM reboot, preserved in `results/native_run1/`): ML-DSA-44 sign/verify 501.8/122.3 µs; d = 16 path 2,846.9 ns. Run 2 (22:59–23:08, after the reboot, top-level CSVs): 408.8/100.9 µs and 2,341 ns. Same scripts and pinning, so this is host-level variation; ratios are stable. **All simulations** (sweep, controller, validate, dissem, e2e, sens, DoS) consistently use run 1. Sweep, controller and validate ran before the reboot, when the top-level CSVs held run 1. Dissem, e2e, sens and DoS were rerun with `EMBER_COSTS_DIR=../results/native_run1` (recorded as `*_costs_dir` in `sim_params.json`). Tables and figures of primitives use run 2.
2. **Concurrency with Experimenter B.** Native run 1 overlapped the start of B's E8 runs. My Python benchmarks were stopped and rerun after B finished. During B's runs, simulations ran under SCHED_IDLE. After the reboot, my rerun sims (cores 0, 1, 3) overlapped B's 1-min Go microbenchmark on core 1. All of this is logged in `raw/proto/interference.log`.
3. **Mobility assumption.** About 7% of sessions are re-routed to another edge once. This produces nearly all misses under stapling and the gap between the simulated and model M(Δ). It is swept from 0 to 0.005.
4. The multi-process issuer rows first ran under a single-core `taskset` and were invalid. They were removed and remeasured, unpinned and one worker per core, into `issuer_throughput_mp.csv`.
5. Path length in the simulator is ⌈log₂ N⌉, an upper bound for promote-trees.
6. Push mode includes pull fallback; its misses are dominated by push delay exceeding the client's first-request delay.
7. A stray 71-B file `/sim_validate.log` (a failed launch message) sits at the filesystem root. I could not delete it (safety check); it contains no data.
8. Spec deviations: the tweak is 26 B (tenant id added); figures are in `results/figures/` (the spec said `figs/`); the λ̄ = 20000 sweep horizon was cut to 1200 s; `procs = 3` for simulations.

## 11. Outputs

- Figures, each as PDF + PNG in `results/figures/`:
  - fig2_token_sizes, fig3_size_vs_N, fig4_verify_cost, fig5_delta_tradeoff, fig6_controller_24h, fig7_dissemination, fig8_e2e_cdf, fig9_sens_heatmap;
  - from B's data: fig10_wire_bytes, fig11_proto_capacity, fig12_proto_validation.
- Tables in `results/tables/`: tab2_primitives, tab3_fit, tab4_simparams, tab5_controller, tab6_trust, tab7_validate.
- The figure/table → script → CSV mapping is in `experiments/README.md`.
