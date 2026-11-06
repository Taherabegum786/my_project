# Changes in R2 (author-requested improvement experiments)

Two new experiments were integrated: a replay of Meta's public CacheLib CDN traces (`results/RESULTS_R2_TRACE.md`) and the R2 prototype runs (`results/RESULTS_R2_PROTO.md`). Every new or changed number is listed under "R2 experiments" at the end of `NUMBERS_TRACE.md`.

## 1. Why the framing changed

The previous version had two headline claims: "stapling fixes the edge" and "pooled batching fixes the issuer".

- **The issuer claim survives, and the trace strengthens it.** At the full token rates implied by the trace, the pooled EMBER issuer needs 0.38–1.08 cores; per-token signing (M2) needs 177. The degenerate single-token trees from R1 appear only at low rates: on the sampled trace, 91.5% of tokens are alone in their tree; at the scaled rate, 0.02% are.
- **The edge claim holds only for long-lived tokens.** Assuming one signed-URL token per object per hour, a real token carries just K = 1.7–2.4 requests. M2 then costs 53.8 µs and 1,869 B per request, against 1.9 µs and 426 B for pooled EMBER. This contradicts "M2 ≥ EMBER at the edge" for that regime.
- **The decisive variable is K, the number of requests per token per verifier.** We derived the crossover from measured costs (arithmetic in `NUMBERS_TRACE.md`):
  - CPU: M2 is cheaper only above K\*_cpu = t_v/(path(d) − path(0)) ≈ 48–154 (d = 16…5).
  - Bytes: M2 is smaller only above K\*_bytes = 3242/(S_tok(d) − 148) ≈ 9–27.
  - The synthetic sessions (K = 150) sit near the CPU crossover for d = 5 (150 vs 154) and above it for deeper trees, and above the bytes crossover. The trace's per-object tokens sit far below both.
- **The trace cannot settle which regime is real.** It has no session or client IDs, so token granularity is an assumption. The paper now says so wherever the edge result appears.

## 2. Section-by-section changes

- **Title.** "Stapling Fixes the Edge, Pooled Batching Fixes the Issuer" became **"Pooled Batching Relieves the Issuer, Requests per Token Decide the Edge"**. The old edge claim is false in the per-object regime, and "fixes" overstated the issuer result, which needs a busy pool.
- **Abstract.** Rewritten around the two regimes and the crossover. It states the token-granularity assumption and includes the trace numbers and the prototype R2 results. The HPACK sentence moved out of the abstract for length; the finding stays in the introduction and §VI-E.
- **Introduction.**
  - Tokens are no longer assumed to carry hundreds of requests.
  - A paragraph introduces K and the trace.
  - Contributions 2 and 3 are rewritten as "pooled batching relieves the issuer" and "requests per token decide the edge".
  - The guidance contribution is now keyed to K, the per-key rate and who holds the issuer key.
- **§V Methodology.** A new "Trace replay" paragraph covers:
  - the dataset, replicates and the Poisson-scaling check;
  - the three verifier models;
  - the bold assumption "one signed-URL token per object key per hour";
  - a host-count sanity check (about 390–2,200 hosts per cluster, from the trace documentation's traffic factors), which brackets the 1000-host models.
- **§VI-B.** Renamed "Stapling at the Edge with Session Tokens". It states K = 150, writes the crossover as K\*_cpu, and flags that the result reverses for short-lived tokens.
- **§VI-C.** Renamed "Batching Relieves the Issuer, Only When the Pool Is Busy". The content is unchanged.
- **New §VI-D "Real CDN Trace: Requests per Token Decide the Edge".**
  - Table `tab:trace`: per-cluster K and rates, M2 vs EMBER pools at Δ = 10 ms (scaled), and the sampled replay.
  - New Fig. 18 (`fig18_k_crossover`): analytic edge CPU and bytes against K, from measured costs. It is produced by `experiments/plots/writer_r2_crossover.py`, which writes `results/r2_k_crossover.csv`.
  - The section covers the issuer, edge and crossover paragraphs, plus V sensitivity.
  - `fig16` and `fig17` were not included: their content is in the table, and the page budget is tight.
- **§VII-A Deployment guidance.** Rules 2–4 are rewritten:
  - Rule 2: measure K first.
  - Rule 3: large K → staple (M2); add pooled EMBER if the key's rate exceeds about 10³/s.
  - Rule 4: small K → pooled EMBER, if the pool is busy and shares a key.
  - The B11 and operational rules are renumbered 5 and 6.
- **§VII-B Limitations.**
  - New "Trace mapping" bullet: one operator, three days, no session/client/host IDs, the assumed granularity, key-hash sampling, Poisson within each minute, and re-routes still unobservable.
  - The "Recommended configurations not prototyped" bullet is replaced with the R2 prototype results (see §3 below).
  - The bullets were tightened.
- **§IV-C.** Added the analytic limit of Eq. (miss): when λΔw_v ≫ 1, M ≈ E/(λΔ), so pull rarely misses at trace-scale pool rates.
- **Length.** The paper is 13 pages, including appendices and references.
  - To fit, these were condensed without changing any number: the HPACK, B11, validation, "Other results", microbenchmark and controller paragraphs, the intro contributions and the abstract.
  - Fig. 13 was scaled to 0.88 textwidth, and Figs. 14/12 to 0.62/0.58.
  - The validation figure was moved earlier in the source, so it no longer floats past the \FloatBarrier.
- **Conclusion.** Rewritten for the two variables: per-key rate at the issuer, K at the edge.
- **References.** Added `berg2020cachelib` (Berg et al., "The CacheLib Caching Engine: Design and Experiences at Scale", USENIX OSDI 2020, pp. 753–768; verified by web search on the USENIX listing, dblp and Crossref) and `cachelib-traces` (CacheLib documentation page "Evaluating SSD hardware for Facebook workloads", which describes the `cdn/202303` traces, the S3 bucket and the licence; fetched from github.com/facebook/CacheLib on 2026-11-06).

## 3. Prototype R2

Source: `results/RESULTS_R2_PROTO.md` and the `proto_*_r2_agg.csv` files. All runs used an idle VM, 5 runs each, mean [95% CI].

- **The Limitations claim "recommended configuration not run on the prototype" is removed.** It is replaced by a "Prototype coverage" bullet that states what R2 covered and what remains simulated: issuer cores, dissemination, shield tier, real K, and production flush/restart rates.
- **Table P1 (Table III) now has two columns.** R1 is the earlier campaign; R2 is the new run of the recommended configurations. In R2, M2 costs 25.35 µs/request against 25.90 for HMAC (throughput ratio 1.02 [0.94, 1.10]); pooled EMBER with a 2^5 tree costs 27.23 µs, 5% more than HMAC.
- **§VI-B adds the R2 link and latency results.**
  - Across the emulated link, B1, M2 and EMBER are link-bound at 24.4–24.7k requests/s.
  - P2 latency: M2 and pooled EMBER add −0.11 to +0.01 ms to median latency relative to HMAC, and every CI includes 0. B5 adds 0.81 and 1.55 ms.
  - The old P2 (R1) appendix paragraph is marked superseded and shortened.
- **The recovery claim in §IV-A was corrected, because the data contradict "a recovery costs one client–edge round trip".**
  - A cache flush on a live connection costs about one extra round trip: 35.8 ms mean (p99 62 ms) against a 20.3 ms base RTT.
  - An edge restart costs a reconnect: 263 ms mean (p99 427 ms), about 13 RTTs. M2 and EMBER pay the same here.
  - A single event caused about 6 recoveries per 1,000 requests, and no request failed.
  - With a 64-entry cache, M2 retries on 55% of requests against 10% for pooled EMBER. With 256 entries, neither retries.
  - "We did not measure how often recovery occurs" was removed. The production frequency of flushes and restarts is still stated as unknown.
- **The P4 results appear in the abstract, rule 3 (cache sizing) and the conclusion.** The P4 setup is described in §V.
- **The smoke values from the coordinator's message are not cited.** The full run measured a 263 ms restart cost, not ~355 ms, and 551 retries per 1,000 requests with a 64-entry cache, not 469.
- **Limitations updated.** P1's absolute values differ by up to 26% across campaigns (B1: 20.54, 22.80 and 25.90 µs), while M2/HMAC stays at 0.98.

## 4. What did not change

- The trust comparison, primitives, HPACK, dissemination, B11, validation and the hypothesis table are unchanged. H1–H9 were fixed before the experiments and are not re-scored against the trace.
- The running header still reads "Manuscript submitted for review". The author block and the Data Availability, AI and Acknowledgment placeholders remain marked [Editable].
