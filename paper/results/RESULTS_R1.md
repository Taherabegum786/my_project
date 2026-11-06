# RESULTS_R1: data for the round-1 major revision

Revision Experimenter, 2026-11-06. This file answers `manuscript/review_round1.md` with new runs. Every number below
comes from code in `paper/experiments/` that was run in this round and is read from the CSV named next to it. The
complete console output of the analysis is in `results/r1_summary.txt`, produced by `python -m plots.make_r1 --in ../results`.

- Simulated values are labelled **sim**, measured values **meas**, and analytic values **analytic**.
- Simulation CIs are Student-t 95% over 5 seeds with common random numbers. Unless a CI is given, the half-width is below 1% of the mean.
- The manuscript was not edited, and NUMBERS_TRACE.md is the writer's job.

---

## 0. How the story changes (read this first)

1. **The reviewer is right about M1.** With per-tenant trees and Δ = 10 ms (the v1 recommendation), **71.5% of tokens sit in single-token trees** (λ̄ = 2000/s).
   - Even in the top tenant-rate decile, which carries 69% of tokens, 59% of tokens have N_e = 1.
   - The issuer then makes 1,646 root signatures/s for 2,000 tokens/s: 0.674 cores, against 0.818 for per-token ML-DSA. That is a **1.2× gain, not 522×**.
2. **The new M2 baseline (stapled per-token ML-DSA-44) matches or beats EMBER on everything except issuer CPU:**
   - bytes on the wire;
   - edge CPU, both simulated and in the Go prototype;
   - misses;
   - user-visible delay (M2 has no batching wait).
3. **EMBER's measurable advantage is issuer signing cost, and only when trees are pooled across tenants** (one tree per issuer key per Δ):
   - λ̄ = 2000/s: issuer 0.0425 vs 0.818 cores (19×).
   - λ̄ = 20000/s: issuer 0.057 vs 8.18 cores (144×).
   - Hottest edge: 151 vs 1,658 ML-DSA verifications/s.
   - The price: +5.4 ms mean issuance delay, a 268–332-B URL token instead of 148 B, and about 1.6–1.8× the fleet edge crypto CPU (all still µs per request).
4. **Corrected recommendation:** pool all tenants of one issuer key into one tree per 10 ms, and staple on every new edge contact. EMBER is worth it only where aggregate issuance per key is roughly ≥ 10³ tokens/s. Below that, M2 is simpler and at least as good.
   - The paper's headline numbers (503 B, 1.28 M tokens/s, 522×) apply only at N = 2^14–2^16. That needs λΔ ≥ 1.6·10⁴, which no simulated configuration reaches at Δ ≤ 0.1 s.
5. **HPACK (M3):** Chrome 153 adopts the edge's advertised 64 KiB table. A 3.3-KB ML-DSA cookie then costs **25.7 B/request** (measured), so in cookie form every PQ option costs about 11.7–12.0 KB per session. curl/nghttp2 and the Go client clamp the table to 4096 B.
6. **Stapling 0.049%** is purely the re-route assumption: 0 at p_move = 0 and 0.95% at p_move = 0.01. Stapling on every new edge contact removes the waits entirely, at +0.19 KB per session (p_move = 0.0005) up to +3.75 KB (p_move = 0.01).
7. **Stale numbers.** The DoS paragraph's 0.48 / 1.03 / 0.027 cores are the **run-2** values. The committed dos.csv (0.586 / 1.243 / 0.032) was a later **run-1** rerun. All simulations except the controller and DES-validation runs now use run 2 (§9).

---

## 1. Which crypto costs feed which result (review M7, checklist 9)

| result | costs | file |
|---|---|---|
| Tables of primitives | native run 2 (top-level `native_*_agg.csv`) | unchanged |
| sweep, dissem, e2e, sens, DoS | **now native run 2** (rerun 2026-11-06) | top-level `sim_delta_sweep.csv`, `sim_dissem.csv`, `sim_e2e_latency.csv`, `sim_sens*.csv`, `dos.csv` |
| R1 experiments: oprg, pmove | native run 2 | `sim_oprg*.csv`, `sim_pmove.csv` |
| v1 versions of the above (run 1) | native run 1 | snapshot in `results/sim_costs_run1/` (with README) |
| controller (Table V / Fig. 6), DES-vs-MC validate | **still run 1, not rerun** (time) | `sim_controller_*.csv`, `sim_validate.csv` |
| proto_mc / P3 validation | Go circl root verify (0.026 ms) | unchanged |

**Sensitivity, run 1 → run 2** (`r1_table6_agg.csv`, which holds both):
- Misses per token are bit-identical, because crypto cost does not enter the miss process.
- D changes by ≤ 0.1 ms. For example, pull at Δ = 0.01 goes from 96.17 to 96.08 ms.
- Simulated mean edge CPU per request falls by 15–16%. For example, pull at Δ = 0.01 goes from 1.195 to 1.012 µs, and its p99 from 0.725 to 0.639 µs.
- Because the controller's D is dominated by Δ/2 and RTTs, and the sweep moved D by ≤ 0.1 ms, the controller conclusions (all differences ≪ 10 ms) cannot change. Say so in the paper, or rerun it (`run_sim --exp controller`, about 60 min on 4 cores).

**Spread of primitives as min–max of run medians** (`native_sig_minmax.csv`; run-2 median [min–max of 5 run-2 run medians]; run-1 median):

| primitive | run 2 | run 1 |
|---|---|---|
| ML-DSA-44 sign | 408.8 [386.9–452.4] µs | 501.8 µs |
| ML-DSA-44 verify | 100.9 [100.2–120.4] µs | 122.3 µs |
| Ed25519 sign | 30.1 [30.1–30.4] µs | 35.8 µs |
| Ed25519 verify | 94.6 [93.8–96.2] µs | 114.1 µs |
| path d = 16 | 2,341 [2,334–2,455] ns | |
| path d = 0 | 235 [217–247] ns | |
| HMAC | 297 [296–303] ns | |

Recommendation: report a range "run 2 [min–max]; run 1", not a 5-point bootstrap CI.

---

## 2. Item 1 / M1: the operating region

**What I ran.**
- `python -m sim.run_sim --exp oprg --reps 5 --procs 4` produces `sim_oprg.csv` and `sim_oprg_deciles.csv`, aggregated in `r1_oprg_agg.csv` and `r1_oprg_deciles_agg.csv`.
- Table: `tables/tab_r1_oprg.tex`. Figure: `figures/fig13_operating_region`.
- Workload as in v1: E = 500, T = 1000 tenants with Zipf(1.0) rates, stationary, K = 150, p_move = 0.0005. Horizons: 3600 s for λ̄ = 200/2000, 1200 s for λ̄ = 20000.
- Simulator extensions (v1 outputs are unchanged and were checked bit-identical):
  - pooling policies: `tenant`; `shard8` (8 tenant shards ≈ trust domains); `global` (1 pool: all tenants of an issuer key); `region10` / `region50` (one tree per edge region; region = edge mod R; re-routes go anywhere);
  - policies: fixed Δ ∈ {0.01, 0.1, 1} s, work-conserving (WC), and `pertoken` = **M2**;
  - modes: pull, pull_staple (staple on first request), and the new `staple_always` (staple on every new edge contact).
- New metrics: N_e distribution per tenant-rate decile, issuer signatures/s and CPU, per-edge and hottest-edge verifications and CPU, staple installs per token.

**N_e distribution, per-tenant trees, Δ = 10 ms, λ̄ = 2000/s.** Decile 1 is the top 10% of tenants by rate and carries 69.3% of the tokens.
- Fraction of tokens in N_e = 1 trees, by decile: **59.4% (decile 1)**, 98.1%, 98.9%, 99.2%, 99.4%, 99.5%, 99.6%, 99.6%, 99.7%, 99.7%.
- All tokens: **71.5% in N_e = 1 trees**.
- Median tree-size bin is 2^0 in every decile. The mean is 1.22 tokens per tree.
- At λ̄ = 20000 per-tenant Δ = 10 ms, decile 1 is still 19% N_e = 1 (median 2^3), and deciles 2–10 are 83–97% N_e = 1.
- Per-tenant WC gives N_e = 1 for ≥ 99.7% of tokens at λ̄ ≤ 2000 (86.7% in decile 1 at λ̄ = 20000).

**Key operating points** (`r1_oprg_agg.csv`; mode staple_always unless stated):
- "tok B" uses the actual encoder size (`token_sizes_r1.csv`, 118-B claims).
- "fleet CPU" is the simulated edge crypto CPU summed over 500 edges, using native per-op costs, not full HTTP handling.
- "hot-edge verif/s" is ML-DSA verifications per second at the busiest edge.

| λ̄ | config | % tok N_e=1 | median N_e | tok B (URL) | issuer sig/s | issuer cores | µs/token | edge µs/req | fleet CPU (cores) | hot-edge verif/s | D (ms) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2000 | **M2 per-token** | 100 | 1 | **148** | 2,000 | 0.818 | 408.8 | **0.953** | **0.288** | 165.8 | **0.41** |
| 2000 | per-tenant Δ=10 ms (v1 rec.) | 71.5 | 1 | 161 | 1,646 | 0.674 | 337.2 | 1.012 | 0.306 | 162.4 | 5.41 |
| 2000 | per-tenant WC | 99.8 | 1 | 161 | 1,998 | 0.818 | 409.2 | 0.953 | 0.288 | 165.8 | 0.41 |
| 2000 | 8 shards Δ=10 ms | 8.8 | 2^2 | 204 | 718 | 0.295 | 147.5 | 1.200 | 0.362 | 150.1 | 5.41 |
| 2000 | 50 regions Δ=10 ms | 59.1 | 1 | 161 | 1,534 | 0.629 | 314.4 | 0.956 | 0.289 | 89.5 | 5.41 |
| 2000 | **1 pool Δ=10 ms** | 0 | 2^5 (20/tree) | **268** | **100** | **0.0425** | **21.2** | 1.509 | 0.456 | **88.1** | **5.43** |
| 2000 | 1 pool WC | 63.6 | 1 | 161 | 1,587 | 0.650 | 325.2 | 1.014 | 0.306 | 162.6 | 0.54 |
| 2000 | 1 pool Δ=100 ms | 0 | 2^8 | 332 | 10 | 0.0057 | 2.8 | 1.715 | 0.518 | 15.2 | 50.6 |
| 20000 | **M2 per-token** | 100 | 1 | 148 | 19,999 | **8.18** | 408.8 | 0.953 | 2.88 | 1,658 | 0.41 |
| 20000 | per-tenant Δ=10 ms | 41.0 | 2^1 | 183 | 10,794 | 4.43 | 221.4 | 1.168 | 3.53 | 1,420 | 5.41 |
| 20000 | 8 shards Δ=10 ms | 0 | 2^5 | 268 | 800 | 0.343 | 17.1 | 1.540 | 4.65 | 756 | 5.43 |
| 20000 | 50 regions Δ=10 ms | 3.6 | 2^3 | 225 | 4,699 | 1.94 | 96.9 | 1.064 | 3.21 | 206 | 5.41 |
| 20000 | **1 pool Δ=10 ms** | 0 | 2^8 (200/tree) | **332** | **100** | **0.057** | **2.83** | 1.714 | 5.18 | **151** | 5.57 |
| 20000 | 1 pool WC | 0 | 2^4 (8.3/tree) | 247 | 2,407 | 1.000 | 50.0 | 1.382 | 4.17 | 1,244 | 0.62 |
| 200 | M2 per-token | 100 | 1 | 148 | 200 | 0.082 | 408.8 | 0.953 | 0.029 | 16.6 | 0.41 |
| 200 | 1 pool Δ=10 ms | 13.6 | 2^2 | 204 | 86.5 | 0.0355 | 177.6 | 1.156 | 0.035 | 15.4 | 5.41 |

- Token-size note: the simulator's `tok_bytes_*` columns use `claims_bytes = 104` and are therefore **14 B smaller** than the real encoder: the sim gives 147 B at d = 0 where the encoder gives 161 B. Use `token_sizes_r1.csv` for sizes (161 / 268 / 332 / 460 B at N = 1 / 2^5 / 2^8 / 2^14). The 147 B quoted by the reviewer is the simulator's value.
- Misses and waiting (pull_staple; `r1_oprg_agg.csv`):
  - λ̄ = 2000: requests waiting are 0.0489% (M2), 0.0486% (per-tenant 10 ms) and 0.040% (1 pool 10 ms).
  - Pure pull at 10 ms: misses/token 1.074 (M2), 1.070 (per-tenant) and 0.957 (1 pool).
  - The tree buys almost no miss reduction at 10 ms. At 1 pool Δ = 100 ms pull it is 0.644 (`sim_oprg.csv`).
- **Where EMBER wins:**
  - Issuer CPU once pooled: 19× at λ̄ = 2000, 144× at λ̄ = 20000. Issuer signatures are capped at 1/Δ per pool, independent of λ.
  - Verifications at hot edges: capped at about 1/Δ per pool, versus sessions/s for M2.
- **Where EMBER does not win:**
  - per-tenant trees at Δ ≤ 0.1 s for any tenant below about 10³ tokens/s;
  - per-request bytes (path grows with log N);
  - per-request edge CPU (+0.55–0.76 µs/req of path hashing, which exceeds the amortised staple verify at K = 150);
  - delay (+Δ/2).
- Region pooling helps edge verifications (89.5 vs 165.8 verifications/s at the hot edge, λ̄ = 2000) but not the issuer, because each region's rate is small.
- WC pooling self-limits issuer CPU to ≤ 1 core per pool at sub-ms delay. At λ̄ = 20000 that is 1.000 core and N ≈ 8.

**Edge CPU crossover (analytic from native costs).** M2 pays t_verify/K per request, and EMBER pays path(d) − path(0). EMBER is cheaper at the edge only if sessions per edge are short: K < 100.9 µs / (path(d) − path(0)).
- d = 5: path 0.89 µs → K < 155.
- d = 8: path 1.28 µs → K < 97.
- The simulated workload has K̄ = 150.

**Corrected recommended configuration** (all metrics above at the same point): **1 pool per issuer key, Δ = 10 ms, staple on every new edge contact, pull fallback.**

| metric | λ̄ = 2000 | λ̄ = 20000 |
|---|---|---|
| median N_e | 20 | 200 |
| token (encoder) | 268 B | 332 B |
| issuer | 0.0425 cores (21.2 µs/token) | 0.057 cores (2.83 µs/token) |
| mean D | 5.43 ms | 5.57 ms |
| requests waiting | 0 | 0 |
| simulated edge crypto | 1.51 µs/req | 1.71 µs/req |
| staple upstream | 2,688 B/session (`sim_pmove.csv`, p_move = 0.0005) | |

This presumes that a shared issuer may mint tokens for all tenants of a trust domain. With per-tenant issuers (each customer signs its own tokens), use M2.

**Headline numbers.** The 1.28 M tokens/s (N = 2^14) is a per-epoch microbenchmark rate. The native issuer at the pooled sizes (`native_issuer_agg.csv`) is:
- N = 16: 41,774 tokens/s;
- N = 64: 104,633 tokens/s;
- N = 256: 469,254 tokens/s;
- per-token ML-DSA-44: 1/408.8 µs = 2,446 tokens/s.

## 3. Item 2 / M2: stapled per-token ML-DSA baseline (B5s)

**Implementation.**
- Python: `experiments/baselines/stapled.py`, with test `tests/test_ember.py::test_stapled_pertoken_m2`; the suite gives **52 passed**.
- Go: `proto/tokens/stapled.go` (+ test), with an edge `b5s` case, a P1 load generator that staples on each session's first request, and hpackbytes rows.
- Simulator: policy `pertoken`.
- URL token = claims ‖ `:S=` b64url(kid ‖ 16-B nonce). The staple is the 2,420-B ML-DSA-44 signature in `x-token-sig`, sent once per edge connection. The edge caches H(ref ‖ claims).

**Bytes** (`token_sizes_r1.csv`, 60-char path, 118-B claims):
- M2 URL token **148 B** (signed URL 238 B) vs EMBER N = 1 / 2^5 / 2^8 / 2^14: 161 / 268 / 332 / 460 B.
- Staple: raw M2 2,420 B vs EMBER signed root 2,461 B.
- HTTP/1.1 header line: 3,242 vs 3,298 B.
- Per session (`wire_bytes_r1.csv`) for M2, EMBER 2^5 + staple and EMBER 2^14 + staple:

  | placement | M2 | EMBER 2^5 + staple | EMBER 2^14 + staple |
  |---|---|---|---|
  | URL, HTTP/2, 4 KiB | **27,048** | 43,401 | 69,161 |
  | URL, HTTP/2, 64 KiB | 25,273 | 39,966 | 63,012 |
  | cookie, HTTP/2, 4 KiB | 12,114 | 13,165 | 14,090 |
  | cookie, HTTP/2, 64 KiB | 11,711 | 11,853 | 12,008 |

**Edge CPU.**
- Native per request (analytic from measured ops): M2 hit = SHA-256 over about 138 B ≤ th_200B = 207 ns, vs EMBER path d = 0 / 5 / 8 = 235 / 892 / 1,284 ns. Add one ML-DSA-44 verify (100.9 µs) per (token, edge) for M2, and per (root, edge) for EMBER.
- Simulated per request: see §2. M2 0.953 µs vs EMBER 1-pool 1.509 µs at λ̄ = 2000.
- **Go prototype P1** (`proto_capacity_r1.csv` → `proto_capacity_r1_agg.csv`; quiet machine; same session for all five schemes; edge on 1 core; 64 conns; K = 150; 5 runs; mean [t-CI], min–max):

| scheme | req/s | edge CPU µs/req |
|---|---|---|
| B1 HMAC | 43,392 [42,182, 44,602] (42,654–45,074) | 22.80 [22.23, 23.36] |
| **M2 b5s** (1 staple verify per 150 req) | **44,254 [42,856, 45,652]** (42,465–45,520) | **22.33 [21.60, 23.05]** |
| O1 EMBER warm (N = 1024 tree, roots pre-installed) | 37,786 [36,770, 38,802] | 26.16 [25.51, 26.82] |
| B5v | 23,232 | 42.53 |
| B5 | 13,079 | 75.58 |

- The edge's own counter confirms 7,419 staple verifications for 1,108,422 requests (`raw/proto_r1/p1_stats_b5s_1.json`).
- **M2 is indistinguishable from HMAC and about 15% cheaper per request than EMBER in Go.**
- Python (secondary; `token_verify_r1.csv`): M2 cache hit 4.70 µs, M2 staple verify 130.5 µs, EMBER warm d = 0 6.25 µs, d = 5 11.14 µs.

**Issuer CPU:** see the table in §2 (M2 = 408.8 µs/token, which is EMBER's only clear loss).

## 4. Item 3: DoS numbers (M6)

`dos.csv` was rerun with run-2 costs (`python -m sim.dos --out ../results`). At 10⁴ fake tokens/s, one edge, 60 s, 5 seeds:

| variant | edge CPU (cores) | other |
|---|---|---|
| naive, all tenants | **0.484** | 9,636 fetches/s, 4,630 verifications/s |
| coalesce+neg, all tenants | 0.484 | 9,270 fetches/s |
| staple flood | **1.026** | |
| staple flood + 1/s per-client limit | **0.0269** | |
| coalesce+neg, low tenant | 0.0183 | 65 fetches/s |

- With run-1 costs (`sim_costs_run1/dos.csv`) the same rows are 0.586 / 1.243 / 0.032.
- **The PDF's 0.48 / 1.03 / 0.027 are therefore correct run-2 values.** The CSV the reviewer checked held a later run-1 rerun.
- Fix: cite the current dos.csv and state "run-2 costs".

## 5. Item 4: Table VI with one configuration

`tables/tab_r1_table6.tex` (from `r1_table6_agg.csv`) has per-tenant (T) and 8-shard pooled (P8) columns side by side, with every cell filled. Values are run 2, λ̄ = 2000, Δ = 10 ms.

| mode | misses/token (T / P8) | D ms (T / P8) | wait % (T) | root/served (T / P8) | CPU µs mean/p99 (T) |
|---|---|---|---|---|---|
| pull | 1.069 / 1.054 | 96.1 / 94.3 | 0.710 | 2.4e-5 | 1.01/0.64 |
| pull_staple | 0.073 / 0.071 | 11.6 / 11.5 | 0.049 | 1.6e-6 | 1.01/0.64 |
| push | 0.622 / 0.616 | 19.7 / 19.7 | 0.41 | 5.0e-3 / 2.2e-3 | 0.71/0.64 |
| pull_rollup | 1.045 / 1.003 | 93.2 / 89.9 | 0.69 | 4.5e-5 / 5.1e-5 | 1.00/0.64 |
| push_rollup | **1.012** / 0.997 | 91.3 / 89.7 | **0.672** | **1.04e-4** / 5.3e-5 | 0.97/0.64 |

- **H4 must use per-tenant push_rollup = 1.04e-4.** The claim "root bytes < 0.1% of served bytes" still holds.
- Δ = 1 s rows are in the .tex as well. For example, pull per-tenant is 0.921 misses/token, D 575.3 ms.
- H6's p99 CPU < 1 ms holds everywhere: maximum simulated edge CPU p99 is 1.71 µs in `r1_oprg_agg.csv` (1 pool, Δ = 100 ms) and 1.42 µs in the sweep (Δ = 1 s).

## 6. Item 5 / M4: re-route sensitivity of stapling

**What I ran.** `run_sim --exp pmove --reps 5` → `sim_pmove.csv`, aggregated in `r1_pmove_agg.csv`. Figure: `figures/fig14_pmove_sensitivity`. λ̄ = 2000, 1800 s, p_move ∈ {0, 1e-4, 2e-4, 5e-4, 1e-3, 2e-3, 5e-3, 1e-2}.

Re-routes per token are 0.0751 at p_move = 5e-4 and 0.75 at 5e-3.

**Requests that wait, per-tenant Δ = 10 ms, staple on the first request** (the v1 mechanism):

| p_move | requests waiting |
|---|---|
| 0 | **0.000%** |
| 5e-4 | 0.0486% [0.0485, 0.0487] |
| 5e-3 | 0.481% |
| 1e-2 | **0.951%** |

M2 behaves the same: 0.0489% at 5e-4.

- **Range to put in the abstract: 0–0.48% for p_move ∈ [0, 0.005] (0–0.95% up to 0.01). Label it model-dependent.**
- **staple_always** (staple on every new edge contact): 0% waiting at every p_move. The cost is upstream staple bytes per session: 2,501 → 2,689 (5e-4) → 4,377 (5e-3) → 6,254 B (1e-2), as raw signed roots.
- **Consistent miss definition** (P3 counts staple installs as misses). In the fleet simulator, staple installs per token are 0.996 (per-tenant 10 ms) and 0.897 (1 pool 10 ms) at p_move = 0, so "installs + fetches" per token ≈ 1.07 at 5e-4. That is P3's definition: compare it with P3 pull_staple (0.05–0.95) only at matching V and Δ.
- Unchanged and still true: P3 has no re-routes and no shield tier, and its 24 rows are 12 configurations × 2 metrics.
- `sim_sens.csv` (run 2, Δ = 1 s): pull_staple misses/token 0.0585 (5e-4) and 0.562 (5e-3). The v1 sentence "0.56 at p = 0.005" is the Δ = 1 s value. At Δ = 0.01 it is 0.726 (`sim_pmove.csv`; reviewer m8).

## 7. Item 6 / M3: HPACK like-for-like and real client encoders

**Like-for-like table:** `tables/tab_r1_hpack.tex` (from `wire_bytes_r1.csv`; hpackbytes rerun with the M2 and N = 1 / 2^5 / 2^8 rows). Session bytes, HTTP/2:

| scheme | URL 4 KiB | URL 64 KiB | cookie 4 KiB | cookie 64 KiB |
|---|---|---|---|---|
| B5 ML-DSA-44 (single) | 457,831 | 410,359 | 458,568 | **11,667** |
| B5c (2 cookies) | – | – | 460,833 | 11,932 |
| M2 + staple | 27,048 | 25,273 | 12,114 | 11,711 |
| EMBER 2^5 + staple | 43,401 | 39,966 | 13,165 | 11,853 |
| EMBER 2^14 + staple | 69,161 | 63,012 | 14,090 | 12,008 |
| B1 | 26,706 | 24,918 | 9,148 | 9,121 |

- The existing rows reproduce v1 within Huffman noise of fresh random signatures: o1 2^14 URL is 66,193 vs 66,344.
- **Fair abstract statement:**
  - In URL form, EMBER (2^5, stapled) uses 0.095× B5's bytes at 4 KiB.
  - In cookie form with a 64 KiB table, B5 (11,667 B) is *smaller* than stapled EMBER (11,853 B).
  - M2 is smallest among the PQ options in every placement.

**Real encoders** (`proto/h2probe`, written for this round; `hpack_clients.csv` and `raw/hpack_clients_raw.csv`). A raw-frame HTTP/2 server advertises SETTINGS_HEADER_TABLE_SIZE and records each request's HPACK block length. The test is a 3,311-B cookie value with 150 sequential fetches on one connection.

| client | advertised 64 KiB | advertised 4 KiB |
|---|---|---|
| **Chrome 153 (headless, "for Testing" build), 3 runs** | emits a table-size update to **65536**; steady **25.7 B/request**; 6,536 B total for 150 requests | 2,993–3,000 B/request; 448,608–449,638 B total |
| curl 8.5.0 / nghttp2 1.59.0 | emits an update to **4096**; 2,670.7 B/request | 2,675.7 B/request |
| Go x/net v0.38.0 Transport (default) | clamps to **4096** (update [4096]); 228.4 B/request | 228.5 B/request |

The Go figure is low because its small header set lets the 3.3-KB cookie fit alone in the 4 KiB table.

Firefox and Safari were not available on this machine and were not tested.

**Semantics, with verifiable sources only:**
- RFC 7541 §4.2: the decoder's maximum is signalled by the protocol, and the encoder may use less, signalling via a Dynamic Table Size Update (RFC 7541 §6.3).
- RFC 9113 §6.5.2: SETTINGS_HEADER_TABLE_SIZE informs the remote endpoint of the maximum header-compression table size used to decode field blocks.
- For requests, the edge is the decoder, so it advertises. The client's encoder decides.
- Go source evidence: x/net v0.38.0 `http2/config.go:98` defaults MaxEncoderHeaderTableSize to 4096; `transport.go:876` and `transport.go:2889` clamp the peer's SETTINGS value to that limit.

## 8. Item 8 / M9: when EMBER beats B11 (delegated Ed25519)

**What I ran.** Analytic from native run-2 costs plus the simulator's B11 dissemination formula. Output: `r1_b11_tradeoff.csv` and `figures/fig15_b11_tradeoff`.

**Exposure model.** A delegated Ed25519 public key is exposed from certificate publication until the last token signed under it expires. The window is L + V_max (V_max = 1 h in the workload). B11 is quantum-safe only if t_break > L + V_max. So, independent of L:
- **if t_break < V_max (1 h), no L makes B11 safe, and EMBER or M2 is preferable**;
- if t_break ≫ hours, B11 with L ≤ t_break − V_max is safe.

With V_max = 10 min the threshold drops to 10 min.

**Cost of short L** (T = 1000 tenants, E = 500, S = 50, cert = 2,508 B):

| L | cert fetches per edge | edge CPU | fleet cert bandwidth | issuer cert signing |
|---|---|---|---|---|
| 10 s | 100/s | 1.0% of a core | 138 MB/s | 0.041 cores |
| 60 s | 16.7/s | 0.17% | 23 MB/s | |
| 300 s | 3.3/s | | 4.6 MB/s | |
| 3600 s | 0.28/s | | 0.38 MB/s | |

**Edge-compromise exposure.** EMBER, M2 and B11 hold no minting secret at the edge, so their exposure is 0. B1 and B12 expose MAC keys for their key or epoch lifetime.

**Issuer CPU.** B11 costs 30.1 µs/token (Ed25519 sign), which is:
- below M2 (408.8) and per-tenant EMBER at 10 ms (337.2);
- above 1-pool EMBER at λ̄ = 2000 (21.2 µs/token) and λ̄ = 20000 (2.83 µs/token).

**Crossover statement for the paper:** prefer EMBER or M2 over B11 when the assumed time to break one Ed25519 key is below L + V_max (≥ 1 h with this workload's V_max). Otherwise B11 is cheaper in bytes (214 B) and dissemination, at negligible cost even for L = 60 s.

**Reference (verified to exist; use its numbers only after reading the paper):** D. Litinski, "How to compute a 256-bit elliptic curve private key with only 50 million Toffoli gates," arXiv:2306.08585 (2023). Its abstract reports one key per 38 h for a strictly 2D-local device. arXiv:2603.28846 (2026, secp256k1 resource estimates) also appeared in the search; it is unverified beyond its title.

## 9. Other checklist items with data

- **Item 10, P2** (`proto_latency_r1.csv`; relabelled, not rerun). Achieved rate divided by the *quiet* P1 capacity: nominal "50%" is 0.35–0.40 actual utilisation and nominal "80%" is 0.57–0.64.
  - Per-run medians [min, max] of added p50 vs B1 at the higher load:
    - B5 +12.14 [3.17, 16.52] ms;
    - B5v +11.75 [2.61, 203.82] ms (one collapsed run);
    - O1 −2.60 [−6.29, 0.55] ms.
  - Report as "≈ 0.6 utilisation" and use these nonparametric ranges.
- **Item 11, staple header size** (`wire_bytes_r1.csv`, `token_sizes_r1.csv`):

  | form | EMBER root | M2 signature |
  |---|---|---|
  | raw | 2,461 B | 2,420 B |
  | base64 | 3,282 chars | |
  | HTTP/1.1 header line | **3,298 B** | 3,242 B |
  | HPACK first-request increment | 2,636 B | 2,589 B |
  | HPACK session increment (4 KiB) | 2,968 B (v1: 2,954) | 2,921 B |

  "2.4 KB" is only the raw signature.
- **Item 14 / m4, padding.** Analytic from the native per-token components at N = 2^14 (leaf 0.174, node 0.130, encode 0.457 µs; sign 331 µs). Worst case is N = 2^k + 1:

  | N | slowdown |
  |---|---|
  | 2^4 + 1 | +1.3% |
  | 2^8 + 1 | +14.7% |
  | 2^14 + 1 | **+38.9%** (tends to about +40% for large N) |

  The measured +12.45% (Python, N = 1000) is not a bound.
- **m13, end-to-end means** (`sim_e2e_latency.csv`, run 2, Δ = 1 s):

  | scheme | mean | p99 |
  |---|---|---|
  | EMBER pull_staple | 0.0503 ms | 0.0014 ms |
  | B5v | **0.0049 ms** (10× lower mean than EMBER-staple) | 0.103 ms |
  | B5 | 0.1009 ms | |
  | EMBER pull | 0.486 ms | p99.9 112.0 ms |

  Fig. 8 now prints the means in its legend.
- **m14, amortisation.** In the simulator (λ̄ = 2000, pull), there are 141 requests per signature verification with per-tenant 10 ms trees, and 158 with 1 pool at 10 ms. In P1, O4 used 150 per root.
- **H7, hybrid** (run 2, `sim_sens.csv`): mean edge CPU 1.982 vs 1.405 µs/req, i.e. **+41.1%** (v1, run 1: +41.6%).
- **SLH-128s root:** D 0.881 vs 0.575 s.
- **Dissemination** (`sim_dissem.csv`, run 2; unchanged by costs): EMBER pull 8.41 MB/s, B11 0.383 MB/s, B12 283.5 MB/s at E = 500.
- **Figures:**
  - m12: `fig12_proto_validation` now uses log axes on both panels.
  - All `make_figures` / `make_tables` outputs were regenerated from the run-2 CSVs. Fig. 6 and Table V (controller) are still run 1.

## 10. Commands (from `paper/experiments`, venv python)

```bash
python -m pytest -q tests/                                   # 52 passed
python -m sim.run_sim --exp sweep_delta --reps 5 --procs 3   # run-2 rerun (802 s)
python -m sim.dos --out ../results
python -m sim.run_sim --exp dissem --reps 5; python -m sim.run_sim --exp e2e --reps 5
python -m sim.run_sim --exp oprg  --reps 5 --procs 4         # 968 s
python -m sim.run_sim --exp pmove --reps 5 --procs 4         # 304 s
python -m sim.run_sim --exp sens  --reps 5 --procs 4         # 409 s
taskset -c 2 python -m bench.bench_r1 --out ../results       # M2 sizes + Python verify
(cd proto && ./bin/hpackbytes -slh ../../results/raw/proto/slh_out.json -out ../../results/wire_bytes_r1.csv -K 150)
(cd proto && RES=<scratch> STAGES=p1 RUNS=5 P1_SCHEMES="b1 b5s o1 b5v b5" bash run_proto.sh)  # -> proto_capacity_r1.csv
proto/bin/h2probe -table {65536,4096} [-h2c] [-goclient]     # + headless Chrome / curl clients -> hpack_clients.csv
python -m plots.make_figures --in ../results --out ../results/figures
python -m plots.make_tables  --in ../results --out ../results/tables
python -m plots.make_r1 --in ../results                      # all R1 tables/figures + r1_summary.txt
```

**Code changed in this round:**
- `sim/engine.py`: group generator, region pooling, `pertoken` policy, R1 metrics.
- `sim/fleet_mc.py`: mode 5 `staple_always`.
- `sim/workload.py`: re-route edge CDF.
- `sim/run_sim.py`: exp `oprg` and `pmove`.
- `baselines/stapled.py` and `bench/bench_r1.py`.
- `plots/make_r1.py`; `plots/make_figures.py` (m12, m13).
- `proto/tokens/stapled.go`; `proto/edge/main.go`, `proto/loadgen/main.go` and `proto/hpackbytes/main.go` (b5s); `proto/h2probe/` (new).
- v1 simulator outputs are bit-identical for the old policies and modes (regression check against the original engine: 0 differing metrics).

**Not done:**
- Controller and DES-validation reruns with run-2 costs (justified in §1).
- P3 with re-routes and a shield tier.
- P2 rerun (relabelled instead).
- Firefox and Safari HPACK tests.
