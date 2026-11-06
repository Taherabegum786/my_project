# RESULTS_R2_TRACE: EMBER's operating region on a real public CDN trace

Revision Experimenter, 2026-11-06. Every number below comes from code in `paper/experiments/` and the CSV named next to it.
- Statistics: mean [Student-t 95% CI] over **9 replicates = 3 Meta CDN clusters × 3 days**, unless stated otherwise.
- Full console output: `results/r2_trace_summary.txt`, from `python -m plots.make_trace --in ../results`.
- Provenance, licence, byte ranges and SHA-256: `results/trace/README.md`. The raw trace is not committed.
- Values are labelled **trace-exact** (replay of the published sampled trace), **trace-scaled** (rates × 1/SamplingRate, Poisson within each minute) or **analytic**.

## 0. Summary: what changes

1. **The R1 "per-tenant trees degenerate to N_e = 1" finding holds only at low token rates.**
   - It holds at the synthetic λ̄ ≤ 20,000/s and on the published sampled trace (about 66 tokens/s): 91.5% of tokens in N_e = 1 trees.
   - At the full cluster rate implied by the trace (2.3–7.7·10⁵ tokens/s per cluster under the per-URL token mapping), per-content-type trees at Δ = 10 ms have a median N_e of 547 and 0.02% singletons.
   - EMBER's issuer then costs **1.08 cores vs 177 cores for M2** (per type) and **0.38 vs 177** (one pool per cluster).
2. **The R1 conclusion "M2 matches or beats EMBER on edge CPU and bytes" is contradicted on real traffic.**
   - Real tokens carry K ≈ 1.7–2.4 requests (78–84% are requested once), not the synthetic K̄ = 150.
   - So M2 pays an ML-DSA verification about every 2 requests: **53.8 µs/request vs 1.9 µs for pooled EMBER** with a shared verifier, and 1,869 vs 426 B/request.
   - EMBER wins in every verifier model.
3. **Stapling/re-route rates cannot be measured from any trace reachable here.** This trace has no client IDs, and keys are anonymised per cluster. The 0.049% stays model-dependent (RESULTS_R1 §6).
   - What the trace does give is verifier contacts per request: M2 0.53–0.86, EMBER pooled 0.0002–0.16.
4. The synthetic workload's λ̄ = 2,000 tokens/s for a whole CDN is **100–400× below one real cluster's** per-URL token rate. Rates, not tree mechanics, decide the R1 verdict.

## 1. Trace and mapping (assumptions)

**Trace.** Meta CacheLib public CDN traces `cdn/202303`, Apache-2.0, published in S3 bucket `cachelib-workload-sharing`.
- Clusters: eag (`reag`), nha (`rnha`), prn (`rprn`), 15–22 Mar 2023.
- Columns used: ms timestamp, anonymised cacheKey, content-type id, VIP type, SamplingRate (1e-4 for eag and prn, 4e-4 for nha).
- Reachability: analytics.wikimedia.org, zenodo, figshare, archive.org, kaggle, SNIA and lrb.cs.princeton.edu were all blocked by the egress policy (HTTP 403). This is the only CDN trace that was downloadable.
- Replicates: the first 3 full 24-h windows of each cluster (`trace_replicates.csv`).

**Mapping** (`sim/trace.py` header; each item is an assumption):

| model element | mapping |
|---|---|
| edge | the trace cluster (one site; thousands of hosts per the CacheLib docs) |
| token | **one signed-URL token per (object key, 1-h bucket)**, issued at that bucket's first request; K = requests of the key in the bucket |
| token validity V | 1 h; sensitivity V = 10 min and 24 h on nha (`trace_oprg_V600.csv`, `trace_oprg_V86400.csv`) |
| tenant | `cdn_content_type_id` (23–24 classes) |
| trust-domain pool | `vip_type` (10–12 classes) |
| global pool | all tokens of a cluster |

- **Rates (trace-scaled).** Per-(pool, minute) token counts × 1/SamplingRate, with Poisson arrivals within each minute. This assumes key-hash sampling, which is consistent with 71% of sampled requests hitting keys seen ≥ 2 times within 5 h.
- **Check of the scaling model at the sampled rate** (exact replay vs the Poisson model):
  - signatures/s agree within 0.07–0.69%;
  - the N_e = 1 fraction agrees within 0.010;
  - EMBER edge CPU agrees within 0.6%.

  Burstiness inside a minute beyond Poisson is therefore not material at the sampled rate. It cannot be checked at the full rate.
- **Verifier models** (the trace has no host field):

  | model | meaning |
  |---|---|
  | shared | cluster-wide verified-root/token cache |
  | keyshard:1000 | each token's requests go to one of 1000 hosts by key hash |
  | reqspread:1000 | each request goes to a random host out of 1000 |

- **Costs:** native OpenSSL run 2 (ML-DSA-44 sign 408.8 µs, verify 100.9 µs; path cost by d; M2 hash 207 ns). Sizes: M2 URL token 148 B; EMBER 118-B claims + path; staple header 3,242 / 3,298 B (HTTP/1.1).

## 2. Trace characteristics (`trace_replicates.csv`, `trace_rates.csv`)

| cluster | requests/s (sampled) | tokens/s (sampled) | **tokens/s (scaled)** | K mean | tokens with K = 1 | request-weighted median K | requests on tokens with K < 97 |
|---|---|---|---|---|---|---|---|
| eag | 71.3 [63.3, 79.4] | 30.3 | **302,631 [296,257, 309,005]** | 2.36 [2.14, 2.57] | 78.4% | 4 | 69.3% |
| nha | 154.4 [130.9, 177.9] | 90.5 | **226,150 [223,365, 228,934]** | 1.71 [1.47, 1.95] | 81.2% | 2 | 88.6% |
| prn | 132.3 [127.8, 136.8] | 76.8 | **768,027 [727,234, 808,821]** | 1.72 [1.69, 1.76] | 84.1% | 2 | 84.9% |

- **Per-content-type pool rates, scaled** (median over types / maximum):
  - eag: 4,535 / 52,785 tokens/s;
  - nha: 3,455 / 40,125 tokens/s;
  - prn: 11,480 / 139,859 tokens/s.
- 99.5–99.9% of tokens are in types whose rate is ≥ 1,000/s.
- Per-minute rates of type pools, p10 / p50 / p90: eag 389 / 11,000 / 44,500; nha 83 / 5,889 / 35,361; prn 722 / 17,722 / 115,778 tokens/s.

## 3. Item 1: tokens per tree and issuer cores (`trace_agg.csv`, `cluster = all`, shared-verifier rows; `tab_r2_trace.tex`; `fig16_trace_operating_region`)

| rates | pool | Δ | tokens in N_e = 1 | median N_e | token B (request-weighted) | issuer sig/s | issuer cores EMBER | issuer cores M2 |
|---|---|---|---|---|---|---|---|---|
| trace-exact (66 tok/s) | type | 10 ms | **91.5% [88.7, 94.4]** | 1 | 163 | 62.5 | 0.0256 [0.0177, 0.0335] | 0.027 |
| trace-exact | VIP | 10 ms | 74.1% [65.2, 83.1] | 1 | 167 | 55.1 | 0.0226 | 0.027 |
| trace-exact | cluster | 10 ms | 52.8% [40.9, 64.7] | 2 | 175 | 46.0 | 0.0188 | 0.027 |
| trace-exact | type | 1 s | 5.4% [2.4, 8.4] | 9 | 221 | 11.8 | 0.0049 | 0.027 |
| trace-exact | type | WC | 99.0% | 1 | 161 | 65.4 | 0.0268 | 0.027 |
| **trace-scaled** (432,269 tok/s) | **type** | **10 ms** | **0.02% [0.01, 0.04]** | **547** | **335** | 1,811 | **1.08 [0.91, 1.26]** | **176.7 [96.9, 256.6]** |
| trace-scaled | VIP | 10 ms | 0.02% | 2,164 | 390 | 939 | 0.73 [0.52, 0.93] | 176.7 |
| trace-scaled | cluster | 10 ms | 0 | 4,369 | 425 | 100 | **0.38 [0.23, 0.54]** | 176.7 |
| trace-scaled | type | 1 s | 0 | 54,780 | 477 | 18.7 | 0.35 [0.19, 0.50] | 176.7 |
| trace-scaled | cluster | 1 s | 0 | 437,030 | 567 | 1.0 | 0.34 [0.19, 0.50] | 176.7 |

- At the scaled rate, EMBER's issuer cost is dominated by per-token leaf/encode work (0.761 µs/token × 4.3·10⁵/s ≈ 0.33 cores), not by signatures.
- **V sensitivity** (nha, scaled, per type at 10 ms):
  - V = 10 min: N_e = 1 for 0.04%, median 312, issuer 0.91 vs 99.4 cores;
  - V = 24 h: 0.06%, median 245, 0.84 vs 75.5 cores.

## 4. Item 2: M2 vs EMBER, bytes / edge CPU / delay with real K (`trace_agg.csv`, trace-scaled, Δ = 10 ms)

| verifier model | edge µs/request M2 | EMBER per type | EMBER cluster pool | contacts/request M2 | contacts/request EMBER (cluster) | B/request M2 | B/request EMBER (cluster) |
|---|---|---|---|---|---|---|---|
| shared | **53.8 [47.4, 60.1]** | 1.59 [1.48, 1.71] | **1.88 [1.80, 1.96]** | 0.531 | 0.0002 | 1,869 | 426 |
| keyshard:1000 | 53.8 [47.4, 60.1] | 43.8 [38.2, 49.5] | 16.7 [11.4, 21.9] | 0.531 | 0.147 | 1,869 | 909 |
| reqspread:1000 | 87.3 [80.6, 94.0] | 61.8 [52.5, 71.1] | 17.6 [11.6, 23.5] | 0.863 | 0.155 | 2,945 | 938 |

- At Δ = 1 s, EMBER is 2.2–4.7 µs/request in every model.
- **Delay** (analytic from costs): mean issuance wait is 5.41 ms for EMBER at Δ = 10 ms vs 0.41 ms for M2. The trace has no per-request latency, so wait at the edge cannot be measured.
- The R1 crossover (EMBER cheaper at the edge if K < 97–155) applies to **69–89% of trace requests**, versus none in the synthetic workload (K̄ = 150).

## 5. Item 3: rate threshold (analytic; native run 2, `r2_trace_summary.txt`)

**EMBER issuer ≥ x× cheaper than M2 when the pool's token rate exceeds:**

| Δ | 2× | 10× | 100× |
|---|---|---|---|
| 10 ms | 161 /s | **1,021 /s** | 12,340 /s |
| 1 s | 1.6 /s | 10.2 /s | 123 /s |

- M2 needs more than 1 issuer core above 2,446 tokens/s.
- **On the trace:**
  - scaled per-type pools: medians 3,455–11,480/s;
  - per-minute p10 rates: 83–722/s;
  - share of tokens in pools above the Δ = 10 ms 10× threshold: 99.5–99.9%.
- The published sampled trace (66 tokens/s) sits below the 2× threshold. At that rate EMBER and M2 tie (0.0256 vs 0.027 cores), which reproduces R1.

## 6. Item 4: stapling with real reuse

- **Not measurable from this trace:** there is no client or connection ID, and keys are anonymised per cluster (0 shared keys among the 2.4–6.9·10⁵ keys of the three clusters' overlapping first 2.6 h, from a one-off exploration of 200-MB file heads with scratchpad `trace_tools/explore.py`; not part of the committed outputs). Re-routes (p_move) can therefore neither be observed nor validated.
- What the trace does fix is how often a verifier first meets a token or root. These are the requests that must carry a staple or would miss in pull mode:
  - M2: 0.53 (shared) to 0.86 (reqspread) per request;
  - EMBER cluster pool: 0.0002 / 0.147 / 0.155;
  - EMBER per type: 0.0028 / 0.42 / 0.60.
- These are lower bounds on staple bytes, assuming a client staples exactly at verifier contacts.

## 7. Paper claims the trace contradicts or qualifies

| claim (manuscript v1 / RESULTS_R1) | trace verdict |
|---|---|
| R1: "at Δ ≈ 10 ms per-tenant trees, N_e ≈ 1; EMBER ≈ per-token ML-DSA" | **Rate-dependent.** True on the sampled trace (91.5% N_e = 1). False at the full-cluster rate (0.02%, median N_e 547). |
| R1: "M2 is at least as good as EMBER on edge CPU, bytes, misses" | **Contradicted** on real per-URL tokens: M2 53.8 vs EMBER 1.9 µs/request (shared verifier) and 1,869 vs 426 B/request. It holds only for long sessions (K̄ = 150, synthetic). |
| v1: 503 B tokens / "< 512 B" | Holds for Δ = 10 ms pools (request-weighted 335–425 B). Exceeded at Δ = 1 s (477–567 B). |
| v1: 1.28 M tokens/s/core issuer (N ≥ 2¹⁴) | That tree size is reached at Δ = 1 s (median N_e 54,780 per type) but **not at 10 ms** (547–4,369). Issuer cost at 10 ms is 0.38–1.08 cores for 4.3·10⁵ tokens/s, about 0.9–2.5 µs/token. |
| v1/R1: λ̄ = 2,000 tokens/s CDN-wide workload | **Unrealistically low:** 100–400× below one cluster's per-URL token rate. Even at 1/V-hour issuance the trace gives 1.8–7.7·10⁵ tokens/s. |
| Stapling 0.049% wait | **Untestable** with this trace; remains model-dependent. |
| Recommended configuration (R1: pooled, Δ = 10 ms, staple every new edge) | **Supported**, with stronger gains than synthetic: 462× issuer, and 28× (shared verifier) or 3.2–5.0× (1,000 hosts) edge CPU vs M2. |

**Main caveat.** Everything at scale depends on the mapping "one token per URL per hour". If tokens are per viewing session (as in the synthetic model), token rates and K differ, and this trace cannot identify sessions.

## 8. Outputs and commands

**CSVs** (`results/`):
- `trace_oprg.csv` (per replicate × pool × Δ × rate mode × verifier model);
- `trace_rates.csv`, `trace_replicates.csv`;
- `trace_*_V600.csv`, `trace_*_V86400.csv`;
- `trace_agg.csv` (aggregated with CIs);
- `r2_trace_summary.txt`.

**Tables and figures:**
- `tables/tab_r2_trace.tex`;
- `figures/fig16_trace_operating_region.{pdf,png}`: (a) N_e = 1 share, (b) issuer cores, (c) edge CPU by verifier model;
- `figures/fig17_trace_rates.{pdf,png}`: daily scaled token rate per cluster vs thresholds.

**Code:** `sim/trace.py` (new), `plots/make_trace.py` (new). Download and preprocessing scripts are in `results/trace/` (`fetch.sh`, `prep.py`), and the exact commands are in `results/trace/README.md`.

**Wall time.** About 25 min of downloads at about 8 MB/s, plus about 6 min of analysis on 2 cores.
- The downloads were pinned to one idle core while PROTO_RUNNING.txt existed.
- No simulation ran while it existed.
