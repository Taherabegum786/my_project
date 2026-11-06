# Final check, R2 (independent checker, 2026-11-06)

Scope: every number that is new or changed in R2 (abstract, introduction, §IV-A recovery, §V trace and P4 setup, §VI-B R2 prototype, §VI-D trace and crossover, §VII-A rules 2–4, §VII-B Limitations, conclusion). I checked each one against `NUMBERS_TRACE.md` and the underlying file: `r2_trace_summary.txt`, `trace_replicates.csv`, `r2_k_crossover.csv`, `proto_capacity_r2_agg.csv`, `proto_capacity_tb_r2_agg.csv`, `proto_latency_r2_agg.csv`, `proto_recovery_r2_agg.csv`, `proto_capacity_r1_agg.csv`, `experiments/proto/run_r2.sh` and `edge/r2.go`.

## Issues found and fixed

1. **§IV-A, recovery rate overstated for EMBER.**
   - Before: "One flush or restart per 30-s run caused about 6 recoveries per 1,000 requests."
   - Data: EMBER flush is 4.40 per 1,000 (M2 flush 6.08, M2 restart 6.17, EMBER restart 6.38).
   - Fix: changed to "4.4–6.4 recoveries per 1,000 requests".
2. **§IV-A, outdated description of the prototype's retry signal.**
   - Before: "implements the hint as a 403 with X-Reject: staple required".
   - Code: R2 runs with `-staple-status` defaulting to 401 and send a `Staple-Required` header (`edge/r2.go`; `run_r2.sh` sets `-ember-miss 401`). The 403 was the R1 behaviour.
   - Fix: "The R2 prototype implements it as a 401 with a Staple-Required header (the R1 prototype used a 403)."
3. **§V, P4 setup missing EMBER's epoch length.** P4 ran EMBER with Δ = 100 ms (`run_r2.sh`: issuer `-kids 12:100`), not the 10 ms used elsewhere. Added "(EMBER with Δ = 100 ms)".
4. **Abstract too long.** It was 281 rendered words (pdftotext); the IEEE Access limit is 250. Trimmed to 244 rendered words (≈ counted as a separate word).
   - All key numbers are kept: 19–144×, 0.38–1.08 vs 177 cores, K = 1.7–2.4, 53.8 vs 1.9 µs, 1,869 vs 426 B, K\* 48–154 (CPU) and 9–27 (bytes), 36 ms, 258–263 ms, 55%.
   - The K-crossover message is kept.
   - The R1 P1 pair (22.33 vs 22.80 µs) was dropped from the abstract. It remains in Table III and §VI-B, and the abstract still says "two prototype campaigns".
5. **Table IX (`tab:hyp`) was never referenced.** Added "(Table IX)" next to the Appendix B reference in §V.

## Verified with no change needed

- **Crossover arithmetic.** I recomputed it with t_v = 100.939 µs, path(0) = 0.23501 µs and S_tok(d) = 118 + 3 + ⌈4(30+16d)/3⌉:
  - K\*_cpu = 154.3 (d = 5), 96.2 (d = 8), 64.1 (d = 12), 47.9 (d = 16);
  - K\*_bytes = 27.0 (d = 5), 12.1 (d = 12), 9.1 (d = 16).
  - These match `r2_k_crossover.csv` and the text.
  - Check against the trace: 100.939 × 0.5308 + 0.207 = 53.78 µs, against 53.79 in the trace.
  - K = 150 sits just below K\*_cpu at d = 5 and above it for deeper trees, which matches "near or above".
- **Fig. 3 (`fig18_k_crossover.pdf`)** is identical to `results/figures/`, and its curves match the CSV.
- **Trace numbers** all match `r2_trace_summary.txt` and `trace_replicates.csv`:
  - Table V, all rows;
  - K per cluster, 78–84% of tokens with K = 1, request-weighted median K 2–4;
  - 2.3–7.7·10⁵ tokens/s, 100–400× the synthetic rate;
  - 547 / 2,164 / 4,369 tokens per tree;
  - 1.08 [0.91, 1.26] / 0.38 [0.23, 0.54] vs 176.7 cores;
  - 0.76 µs/token and 0.33 cores;
  - 1,021 tokens/s threshold and 99.5–99.9%;
  - 54,780 and 477 B at Δ = 1 s, 312 and 245 for the V sensitivity;
  - 16.7–17.6 vs 53.8–87.3 µs, contacts 0.53–0.86 and 0.0002–0.16;
  - 51.4 vs 53.8 µs (sampled);
  - Poisson check within 0.7% and 0.6%;
  - dates 15–18 Mar 2023;
  - 390–2,200 hosts, from the doc's traffic factors 1/13.4, 1/6.37, 1/4.58, re-read from the CacheLib documentation page.
- **Prototype R2 numbers** all match the `proto_*_r2_agg.csv` files:
  - P1: 25.90, 25.35, 27.23, 77.52 µs; ratio 1.02 [0.94, 1.10]; +5%;
  - across the link: 24.4–24.7k req/s, B5 12,226/s;
  - P2: −0.11 … +0.01 ms, B5 +0.81 [0.77, 0.84] and +1.55 [0.94, 2.16] ms;
  - P4: 35.8 ms (p99 62), 20.3 ms RTT, ×1.8; 262.9 ms (p99 427) and 257.7 ms, ×13; 0 failures; 55% vs 10% at 64 entries; 41.7 ms median; about 6,000 tokens; 256 entries with no retries; about 20 requests per token.
  - Limitations: 26% spread (20.54 / 22.80 / 25.90 µs) and the 0.98 ratio, from the R1 and R2 aggregates.
- **Internal consistency.** No remaining text says "stapling fixes the edge", "recovery costs one RTT", "not run on the prototype" or uses the old title. The §VI-B session-token result says explicitly that it reverses for small K, and the threat model's generic K is consistent with this.
- **References and figures.** Every `\ref`/`\eqref` resolves. All 6 figures and 9 tables are referenced. All 5 included figure files exist in `figures/`. Every `\cite` key exists in `references.bib`.
- **Citations.**
  - `berg2020cachelib`: web search confirms the title, all 11 authors in order, OSDI 2020 (14th USENIX OSDI), pp. 753–768 (USENIX listing) and USENIX Association. NSF PAR lists 769–786, which looks like a metadata error; I kept the publisher's pages.
  - `cachelib-traces`: re-fetched the page. The title "Evaluating SSD hardware for Facebook workloads", `cdn/202303` (3 clusters, 7 days, Mar 2023), bucket `cachelib-workload-sharing` and "licensed under the same license as CacheLib" (Apache-2.0) all match.
  - No bib changes were needed.
- **Header and placeholders.** The running header reads "Manuscript submitted for review". The author block, Data Availability, AI declaration and Acknowledgment are still marked [Editable].

## Build

- `latexmk -pdf`: no errors, no undefined references or citations; only font-shape warnings.
- **13 pages.** I checked every page visually. `main.pdf` was copied to `main_final.pdf`.
- **`pqcdn_tokens_latex.zip`:**
  - Rebuilt in a fresh scratchpad directory with the same layout: 24 entries, 5 figures, `IEEEtran.cls` from texlive.
  - Extracted into a new empty directory, removed `main.pdf` and `main.bbl`, and test-compiled: 13 pages, no undefined references.
- Additions to `NUMBERS_TRACE.md`: a "Final check R2 (corrections)" table that records the changes above.
