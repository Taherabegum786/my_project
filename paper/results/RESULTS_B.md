# RESULTS_B: E3b HPACK wire bytes and the E8 real prototype (Experimenter B)

All numbers below were produced by code in `paper/experiments/proto/` and read from the CSVs named next to them.
Confidence intervals (CI) are 95% Student-t intervals over 5 runs unless stated otherwise. Timings are labelled
by implementation: **go-1.24.7+circl-1.6.1** means the Go prototype, using the Go stdlib and cloudflare/circl
v1.6.1. These timings are not the OpenSSL 3.5.4 native numbers, which are Experimenter A's primary source.

**Testbed limitation (state it in the paper).** All processes run on **one 4-vCPU KVM guest** (Intel Xeon @ 2.10 GHz,
Linux 6.18). The client, edge and origin run in three network namespaces (`ember_cli`, `ember_edge`, `ember_origin`).
They are joined by two userspace link emulators (`netemu/tapbridge.c`, reused from the author's earlier artifact
`origin/claude/brave-meitner-l8yswp`, because netem is not compiled into this kernel). The links have 10 ms and 37.5 ms
one-way delay, 1 Gbit/s serialisation and MTU 1500. Traffic crosses these emulated links, but the namespaces still share
CPU, memory and the kernel. No physical NIC is involved.

Cores: load generator 0 (P1: 0, 2, 3; P2: 0, 3), edge 1 (`GOMAXPROCS=1`), both tapbridges 2, issuer 3.
Environment details are in `env.txt` (section "Experimenter B").

## 0. Reproduce

```bash
cd paper/experiments/proto
STAGES="test hpack rtt p1 p2 p3 gobench agg" RUNS=5 bash run_proto.sh   # full run, ~100 min (over the 60-min E8 cap)
STAGES="p1 agg" RUNS=5 bash run_proto.sh      # STANDALONE P1 RERUN on a quiet machine (~27 min); overwrites
                                              # proto_capacity.csv and re-aggregates proto_* from existing CSVs
```

- **Rerun command:** `STAGES="p1 agg" RUNS=5 bash run_proto.sh` is the command for the coordinator's planned quiet-machine
  P1 rerun. It recreates the namespaces when they are missing or stale (for example after a reboot). It logs
  `/proc/stat` steal ticks and load average at the start and end of every P1 run to `raw/proto/p1_steal.csv`, and the
  interference sampler writes to `raw/proto/interference.log`. I smoke-tested it standalone into a scratch results
  directory after a VM reboot.
- **Do not edit `run_proto.sh` while it runs.** Bash reads scripts incrementally. In the main run, a mid-run edit caused
  the `line 131: syntax error` at the very end of `raw/proto/run_proto.stdout`. All six stages had already finished, and
  the file on disk passes `bash -n`.
- **Correctness:** `go test ./tokens/` passes. It includes **128 cross-implementation checks against the Python
  reference's `tests/vectors.json`** (tweaks, Th, signed roots for ML-DSA-44, Ed25519 and hybrid, EMBER tokens at
  N = 1, 5, 1000 with n = 16 and 32, valid and tampered cases, and per-token B1, B2, B3, B5, B11, B12). See
  `raw/proto/go_test.log`.

## 1. E3b: request-header bytes per session (`wire_bytes.csv`, `hpackbytes/`)

Each session is 1 manifest request plus K = 150 segment requests on one connection. The other headers are a realistic
Chrome-like set of about 570 B in HTTP/1.1. The encoder is `golang.org/x/net/http2/hpack` v0.38.0 with a 4096-B dynamic
table and the encoder's default indexing policy. Two sensitivity variants are included: `h2-hpack-pathnoindex`
(`:path` never indexed) and `h2-hpack-t64k` (65536-B table). Signatures are real (circl / Go stdlib). The SLH-DSA
signatures (B7, B8, and the O3 staple) are real pqcrypto 1.0.0 signatures. EMBER tokens come from real trees.

| scheme / placement | token B | h2 session B | h2 B/req | HTTP/1.1 session B | h2 (64 KiB table) session B |
|---|---|---|---|---|---|
| no token (headers only) | 0 | 8,557 | 56.7 | 86,823 | 8,761 |
| B1 HMAC, URL | 127 | 26,706 | 176.9 | 107,057 | 24,918 |
| B11 delegated Ed25519, URL | 175 | 33,277 | 220.4 | 114,305 | 30,825 |
| B12 KEM-wrapped HMAC, URL | 132 | 27,660 | 183.2 | 107,812 | 25,540 |
| B5 ML-DSA-44, URL | 3,311 | 457,831 | 3,032.0 | 587,841 | 410,359 |
| B5 ML-DSA-44, cookie | 3,311 | 458,568 | 3,036.9 | 589,955 | **11,667** |
| B5c ML-DSA-44, 2 cookies | 3,311 | 460,984 | 3,052.9 | 592,522 | **11,933** |
| B6 ML-DSA-65, cookie | 4,496 | 551,251 | 3,650.7 | 768,890 | 12,603 |
| **O1 EMBER N=2^14, URL** | 421 | **66,344** | 439.4 | **151,451** | 60,605 |
| O1 N=2^14, URL, + stapled root on the first request | 421 | 69,298 | 458.9 | 154,749 | 63,149 |
| O1 N=2^14, cookie | 421 | 10,775 | 71.4 | 153,565 | 9,358 |
| O1 N=2^20, URL | 549 | 83,225 | 551.2 | 170,779 | 75,820 |
| O2 (n = 32) N=2^14, URL | 720 | 107,896 | 714.5 | 196,600 | 96,377 |
| O3 (SLH-DSA-128s root) + staple, URL | 421 | 74,682 | 494.6 | 161,997 | 68,683 |

Findings (cite the `wire_bytes.csv` rows):

- **URL form, EMBER vs B5c:** O1 is 66,344 / 460,984 = **0.144×** B5c per session in HTTP/2 and
  151,451 / 592,522 = **0.256×** in HTTP/1.1.
- **The 4096-B HPACK table does not rescue ML-DSA cookies.** A ~3.3 KB cookie is evicted by the per-request `:path`
  entries, so every request re-sends it: 3,036.9 B per request. With a 64 KiB table the cookie stays indexed (77.3 B
  per request), and the cookie gap to EMBER shrinks to 11,667 vs 9,358 B per session. Splitting into 2 cookies (B5c)
  does not help at 4096 B.
- **The stapled root adds 2,954 B per session** (69,298 − 66,344, h2, URL). For an SLH-DSA-128s root the first request
  is 9,147 B.

## 2. Go crypto costs (`proto_go_verify.csv` → `proto_go_verify_agg.csv`; `gobench/`)

Pinned to core 1, 5 fresh processes. Iterations per process: 2000; 500 for signing; 20 for epoch issue. Each row gives
the median of the run medians with a bootstrap 95% CI over run medians (2000 resamples), labelled `go-1.24.7+circl-1.6.1`.
The run started at 22:59:00 and ended at 22:59:58. The machine was quiet: load average 0.98 at the start. Experimenter A's
`sim sens` job started at about 23:01.

| op | median µs | 95% CI |
|---|---|---|
| verify token B1 HMAC | 0.853 | 0.843–0.914 |
| verify token B12 | 0.940 | 0.868–1.815 |
| **EMBER token verify (parse + path, N=2^14, warm root)** | **3.074** | 3.071–3.077 |
| verify token B5 ML-DSA-44 | 32.76 | 32.31–32.79 |
| verify token B6 ML-DSA-65 | 45.26 | 44.83–45.72 |
| verify token B2 Ed25519 | 45.43 | 45.35–46.81 |
| verify token B11 | 45.99 | 45.50–48.47 |
| verify token B3 ECDSA P-256 | 70.62 | 70.52–71.81 |
| verify token B9 hybrid | 78.31 | 78.19–78.47 |
| verify root ML-DSA-44 (unmarshal + verify) | 25.51 | 24.78–27.66 |
| verify root hybrid Ed25519 + ML-DSA-44 | 70.99 | 70.81–76.88 |
| sign root ML-DSA-44 | 121.2 | 112.6–136.5 |
| sign token B5 ML-DSA-44 | 123.9 | 118.1–134.4 |
| issue epoch N=1024 (leaves + tree + sign + encode) | 2,372 | 2,332–2,584 |
| issue epoch N=16384 | 41,850 | 39,610–43,680 |

**Sanity check.** circl's ML-DSA-44 verify (32.8 µs) is below the OpenSSL 3.5.4 figure (~120 µs in feasibility.md).
It falls in the "tens of µs" AVX2 range the design document anticipates, so it is not implausible. A should note the
cross-implementation gap in `notes_impl_xcheck.md`. In circl, ML-DSA-44 verify is cheaper than Ed25519 or ECDSA verify
in Go.

## 3. P1: edge capacity (`proto_capacity.csv` → `proto_capacity_agg.csv`)

- **Setup:** edge on 1 core; closed loop over the edge namespace's loopback; 64 keep-alive connections; each token is
  used for 150 requests; 5 s warm-up + 20 s; 5 runs.
- **Metrics:** `edge_cpu_us_per_req` = edge CPU utilisation (from `/proc/<pid>/stat`) ÷ req/s. It is the robust metric
  when the edge is not fully saturated.

| scheme | token B | req/s mean [95% CI] | CV % | edge CPU µs/req [95% CI] | CV % | min edge util | p99 ms |
|---|---|---|---|---|---|---|---|
| B1 HMAC | 100 | 37,890 [29,750–46,030] | **17.3** | 24.80 [21.31–28.30] | 11.4 | 0.840 | 5.65 |
| B12 KEM-wrapped HMAC | 106 | 35,970 [31,690–40,250] | 9.6 | 25.33 [23.72–26.94] | 5.1 | 0.844 | 6.12 |
| O4 EMBER, hybrid root | 309 | 32,110 [26,730–37,490] | 13.5 | 28.81 [25.73–31.89] | 8.6 | 0.874 | 6.63 |
| O1a EMBER + root verify / 1000 req | 310 | 31,330 [26,710–35,960] | 11.9 | 29.42 [26.98–31.85] | 6.7 | 0.866 | 6.59 |
| O1 EMBER, warm | 309 | 30,830 [27,490–34,170] | 8.7 | 29.67 [27.83–31.50] | 5.0 | 0.864 | 6.90 |
| B5v ML-DSA-44 + verify cache | 3,285 | 20,550 [19,240–21,870] | 5.2 | 46.89 [45.02–48.76] | 3.2 | 0.943 | 7.73 |
| B5 ML-DSA-44 | 3,284 | 11,900 [11,390–12,410] | 3.5 | 83.14 [79.47–86.81] | 3.6 | 0.987 | 13.0 |
| B11 delegated Ed25519 | 149 | 11,030 [10,760–11,300] | 1.9 | 89.59 [87.18–92.01] | 2.2 | 0.983 | 14.9 |
| B2 Ed25519 | 143 | 10,830 [10,370–11,290] | 3.4 | 91.33 [87.68–94.97] | 3.2 | 0.982 | 15.3 |
| B6 ML-DSA-65 | 4,469 | 8,866 [8,218–9,514] | 5.9 | 111.7 [103.3–120.1] | 6.1 | 0.983 | 17.3 |
| B3 ECDSA P-256 | 152 | 8,088 [7,831–8,345] | 2.6 | 122.2 [118.5–126.0] | 2.5 | 0.987 | 18.5 |
| B9 hybrid per token | 3,369 | 6,543 [6,271–6,815] | 3.3 | 150.9 [144.8–157.0] | 3.3 | 0.983 | 22.9 |

### 3.1 P1 anomaly: run-to-run variance, and interference with Experimenter A
- **CV by scheme:** the expensive schemes keep the edge at 0.98–0.99 CPU and have req/s CV of 1.9–5.9%. The cheap
  schemes (B1, B12, O1, O1a, O4) have CV of 8.7–17.3%.
- **Cheap schemes stop saturating in runs 3–5.** In runs 1–2 their edge utilisation is 0.96–0.99. In runs 3–5 it drops
  to **0.84–0.88** (`proto_capacity.csv`). The edge then idles part of the time: the load generator, not the edge,
  became the limit. B1's req/s per run was 39,956 / 37,168 / 47,962 / 32,745 / 31,626. Run 3's high value came with
  utilisation 0.958, so the per-request CPU cost also moved between runs.
- **The drop coincides in time with Experimenter A's work.** A's note in `raw/proto/interference.log` says A ran
  `bench_primitives` **pinned to core 2**, one of the three P1 load-generator cores, from about 18:38 to 18:52. A also
  ran `sim validate` on core 0, which is also a load-generator core. P1 runs 3–5 ran from 18:40 to 18:55
  (`raw/proto/p1_*` file times), exactly the runs that lost saturation.
- **The 15-s CPU samples cannot separate the runs.** `p1_interference.py` gives `proto_p1_interference.csv` and
  `.txt`. Other processes averaged 95 / 87 / 87 / 93 / 98% of one core in runs 1–5. That is about one busy core
  throughout P1. Per-scheme correlations between other-process CPU and req/s (n = 5) range from −0.23 to +0.91 with no
  consistent sign. Pooled over the cheap schemes, corr(other CPU, edge utilisation) = −0.16 (n = 25).
- **Conclusion:** the noise is consistent with A's runs competing for load-generator cores (temporal coincidence at run
  level), but the coarse sampling does not show it statistically. Hypervisor steal was not logged per run in the main
  run; the rerun logs it.
- **Treat the cheap-scheme req/s values as lower bounds and prefer `edge_cpu_us_per_req`.** Its CV is ≤ 6.7% except
  B1 (11.4%) and O4 (8.6%). Rerun P1 on a quiet machine with `STAGES="p1 agg" RUNS=5`.

## 4. P2: latency under load over tapbridge A (`proto_latency_runs.csv` → `proto_latency.csv`, `proto_latency_agg.csv`)

- **Setup:** open loop (Poisson) at 50% and 80% of each scheme's own mean P1 req/s; 1024 connections; 3 s warm-up +
  15 s; 5 runs. Latency is measured from the scheduled send time.
- **Comparison caveat:** `added_*_vs_hmac` is paired by run against B1 at the same load fraction. Because the load is a
  fraction of each scheme's own capacity, the absolute rates differ between schemes. The base RTT is 20.98 ms.
- **Errors:** zero errors in all P2 runs.

| scheme | load | achieved req/s | p50 ms [CI] | p99 ms [CI] | added p50 vs HMAC ms [CI] |
|---|---|---|---|---|---|
| B1 | 0.5 | 18,947 | 25.41 [24.68–26.13] | 39.80 [35.95–43.65] | 0 |
| O1 | 0.5 | 15,409 | 25.34 [23.78–26.90] | 61.60 [7.79–115.4] | −0.07 [−1.17–1.03] |
| O1a | 0.5 | 15,666 | 25.38 [23.92–26.85] | 36.63 [34.11–39.15] | −0.03 [−0.87–0.82] |
| B5 | 0.5 | 5,937 | 25.87 [25.27–26.46] | 47.46 [32.87–62.05] | 0.46 [−0.67–1.59] |
| B5v | 0.5 | 10,266 | 25.74 [23.28–28.21] | 41.79 [38.05–45.52] | 0.34 [−2.77–3.44] |
| B1 | 0.8 | 30,329 | 30.87 [27.78–33.96] | 108.9 [50.0–167.8] | 0 |
| O1 | 0.8 | 24,676 | 27.63 [26.62–28.65] | 52.93 [38.58–67.27] | −3.24 [−6.82–0.34] |
| O1a | 0.8 | 25,075 | 28.51 [27.14–29.88] | 58.59 [42.88–74.31] | −2.36 [−5.95–1.22] |
| B5 | 0.8 | 9,511 | 42.34 [34.44–50.23] | 175.7 [81.0–270.4] | **11.47 [5.09–17.85]** |
| B5v | 0.8 | 16,444 | 80.05 [−26.4–186.5] | 240.3 [83.4–397.3] | 49.18 [−58.6–157.0] |

The full table, including B2, B3, B11 and B12, is in `proto_latency_agg.csv`. At 50% load, no scheme's added p50 is
distinguishable from zero except B2 (−1.25 ms) and B3 (−1.39 ms). Those two run at much lower absolute rates than HMAC.

Anomalies:
- **ML-DSA tokens at 80% load inflate latency.** B5 (+11.5 ms p50) and B5v (p50 80 ms, with a CI spanning zero
  because individual runs collapsed) are the only schemes whose latency rises at 80%. They are also the only ones
  sending 3.3 KB URLs at about 9.5k and 16.4k req/s: roughly 260 and 450 Mbit/s of request bytes through the single
  userspace tapbridge. A bulk TCP transfer measured about 624 Mbit/s through it. The likely cause is the link emulator
  and its queues, not edge CPU. I have not verified this.
- **One O1 run at 50% has a p99 outlier** (CI 7.8–115 ms).
- **Possible extra interference:** P2/P3 ran 18:56–19:25 while other processes used on average 234% CPU
  (`interference.log`), so P2 tails may contain interference as well.

## 5. P3: dissemination and simulator validation (`proto_p3_runs.csv`, `proto_validate.csv`, `proto_validate_replica.csv`)

- **Configuration** (`proto_p3_config.json`):
  - Modes pull and pull_staple, λ ∈ {20, 200} tokens/s. The four (mode, λ) pipelines run concurrently, each with its
    own kid and its own virtual edges.
  - V ∈ {10, 50} virtual edges with Zipf(0.8) shares; Δ ∈ {0.1, 1, 10} s.
  - 60 s issuance window per run, then drain. This deviates from the 5 min in the spec, to fit the time budget.
  - K ~ geometric with mean 20 segments, 200 ms apart; token receipt to first request is lognormal (median 120 ms,
    σ = 0.5).
  - 5 runs with common seeds (`SEED + 1000·run`).
  - The edge keeps 64 pre-warmed keep-alive connections to the root service.
- **Measured RTTs** (`proto_rtt.csv`, keep-alive HTTP, 1000 samples per path): edge→origin mean 76.10 ms (p50 75.88,
  p99 80.62); client→edge mean 20.98 ms (p50 20.74, p99 23.57). ICMP gave 20.6 / 75.5 / 95.9 ms (`raw/proto/net_check.txt`).
- **Correctness:** 0 rejects and 0 errors across all 120 pipeline-runs.
- **Issuance wait:** the mean is 152–155 ms at Δ = 0.1 s, 620–630 ms at Δ = 1 s and 5.22–5.44 s at Δ = 10 s. This is
  the client→origin RTT (about 95 ms) plus Δ/2 (`issue_wait_mean_ms`).
- **Stapling** adds 3,298 B upstream per session (the `X-EMBER-Root` header). Requests with a stapled-root miss wait a
  mean of 0.074–0.086 ms, against 76.9–78.5 ms for a pull miss at Δ ≤ 1 s. Request p99 at Δ ≤ 1 s is 39–47 ms with
  stapling vs 75–103 ms with pull.

**Validation (H8).** The MC column comes from **Experimenter A's `fleet_mc`** (`sim_proto_mc.csv`, `fleet_mc-kernel`,
50 reps, fed the measured RTT distribution and the Go root-verify cost of 0.0259 ms). The model column is the analytic
steady-state formula Σ_v(1−e^{−λΔw_v})/(λΔ). As an independent cross-check, `validate.py --replica` gives
`proto_validate_replica.csv`; the replica agrees with fleet_mc to within 2.1% on every metric.

| metric | configurations passing (\|rel. err\| ≤ 15% or MC inside the prototype CI) | max \|rel. err\| MC | max \|rel. err\| model |
|---|---|---|---|
| misses / token | **24 / 24** | 0.044 | 0.148 |
| root bytes / token | **24 / 24** | 0.044 | 0.149 |
| mean miss-added latency, pull, Δ ≤ 1 s | **8 / 8** | 0.033 | 0.030 |
| mean miss-added latency, pull, Δ = 10 s | **0 / 4** | 0.446 | 0.445 |
| mean miss-added latency, pull_staple | **0 / 12** | 0.698 | 0.703 |

- **Misses/token, examples (prototype mean [CI] vs fleet_mc):**
  - V=10, Δ=1, λ=200: 0.05116 [0.05036–0.05196] vs 0.05067.
  - V=50, Δ=0.1, λ=20: 0.9543 [0.9516–0.9570] vs 0.9528.
  - V=50, Δ=10, λ=200: 0.02817 [0.02788–0.02846] vs 0.02880.
- **The analytic model's 9–15% error at Δ = 10 s is a finite-window effect.** A 60-s window holds only about 6 epochs,
  so partly filled boundary epochs add misses. The model is steady-state; fleet_mc simulates the same finite window.
- **Pull at Δ = 10 s: the prototype measures 118–137 ms against fleet_mc's 75.9 ms** (−36% to −45%).
  - **Cause:** the four concurrent pipelines share Δ and start their timers together. Each epoch close therefore
    releases about 4,400 tokens at once, and their first requests, each on a new TCP connection, hit the one-core edge
    within about 200 ms.
  - **Evidence:** first-request latency p50 is 136.8 ms at Δ = 10 s vs 23.6 ms at Δ = 1 s (run 1, V = 10,
    `raw/proto/p3_req_*.csv.gz`). Pull-fetch waits have p90 209.7 ms vs 82.5 ms.
  - **Why the simulator misses it:** the root fetch shares the congested edge core and link. fleet_mc and the model
    contain no edge-CPU or link queueing.
  - This is a real effect of timer-aligned epochs (synchronised flash crowds), amplified here by the concurrent
    pipelines. The run-to-run CIs are wide (79.6–157.2 ms).
- **pull_staple: the prototype measures 0.074–0.086 ms against a modelled 0.026 ms.** The model counts only the
  ML-DSA-44 verify. The prototype also base64-decodes and parses the 3.3 KB header, takes a lock, and runs on a loaded
  core. X-Root-Wait has 1 µs resolution. The absolute gap is about 0.05 ms, which does not matter for latency but
  fails the relative criterion.

**H8 outcome: partially supported.** fleet_mc predicts misses/token and root bytes within 4.4% on all 24
configurations. It predicts pull miss latency within 3.3% when epochs are small (Δ ≤ 1 s). It **fails** for miss
latency at Δ = 10 s (36–45% under-prediction, from burst queueing it does not model) and for staple latency (sub-0.1 ms
parse overhead). The simulator's latency claims should be scoped to non-bursty edges, or edge queueing should be added.

## 6. Hypothesis outcomes (B's evidence)

- **H1 (bytes per session): supported for HTTP/2, marginally refuted for HTTP/1.1.** In URL form, EMBER uses 0.144×
  B5c's bytes in HTTP/2 and 0.256× in HTTP/1.1, against a threshold of ≤ 0.25. In HTTP/1.1 about 87 KB per session is
  token-independent header bytes. In cookie form under HTTP/2 the gap depends on the HPACK table size: 458,568 vs
  10,775 B at 4096 B, and 11,667 vs 9,358 B at 64 KiB.
- **H2 (edge CPU, Go): supported.**
  - **Per-token microbenchmark:** EMBER verify takes 3.074 µs, which is 3.6× HMAC (0.853 µs; threshold ≤ 5×) and
    10.7× cheaper than uncached ML-DSA-44 (32.76 µs; threshold ≥ 10×).
  - **Whole HTTP request (P1 edge CPU):** O1 29.67 µs vs B1 24.80 µs (1.20×) vs B5 83.14 µs (2.8×).
  - **Requests per core:** O1 30,830 vs B5 11,900 vs B5v 20,550 req/s. B5v amortises verification per session, but its
    3.3 KB tokens still cost 46.89 µs per request to parse and hash.
- **H7 (hybrid root): no detectable per-request difference at this noise level.** O4 is 28.81 [25.73–31.89] µs/req and
  O1 is 29.67 [27.83–31.50] µs/req; the CIs overlap. A < 1% difference cannot be resolved here. The hybrid root verify
  costs 70.99 µs vs 25.51 µs, but only once per (edge, epoch). O1a, with one root verify per 1000 requests, is
  29.42 µs/req, indistinguishable from O1.
- **H8: partially supported** (§5).
- **H3/H9 (issuer), Go cross-check only. A's OpenSSL numbers are the primary source.** Go epoch issue at N = 1024 is
  2.372 ms, about 432k tokens/s per core, which is 53× Go per-token ML-DSA-44 signing (123.9 µs, about 8.07k/s). At
  N = 16384 it is 41.85 ms, about 392k tokens/s, which is 48×. The cost at large N is dominated by leaf hashing,
  `crypto/rand` salts and base64 encoding.

## 7. Deviations and anomalies (summary)
1. **E8 wall time** was about 100 min, against a 60-min cap.
   - P2 runs were 15 s instead of 30 s.
   - P3 used a 60-s window instead of 5 min, with the four (mode, λ) pipelines run concurrently.
   - The P1 load generator used 3 cores so the generator would not be the bottleneck. In runs 3–5 it still was for the
     cheap schemes (§3.1).
2. **Experimenter A ran benchmarks during P1 runs 2–5** (core 2 and core 0) and during P2/P3 (§3.1, §4). P1 should be
   rerun on a quiet machine with `STAGES="p1 agg" RUNS=5`.
3. **The tapbridge is userspace and single-threaded.** Throughput is high-latency-tolerant but limited (~624 Mbit/s for
   a bulk transfer; MTU-sized frames of 1513 B average). It is the likely source of the B5/B5v tail at 80% load.
4. **TLS is not in the prototype.** Connections are plain HTTP/1.1 keep-alive, as in the design's limitation 3. The
   response body is 64 B, so P1 measures verification cost, not content delivery.
5. **The VM rebooted between the main run (finished ~19:25) and the gobench/agg stages (22:59).** The emulated network
   was rebuilt by the rerun smoke test and torn down afterwards.
