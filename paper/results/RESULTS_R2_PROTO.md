# RESULTS_R2_PROTO — prototype run of the recommended configurations

Run by the coordinator on 2026-11-06, 17:22–18:09 UTC, on an otherwise idle VM (load average 0.11 at start; nothing else was running). The code was implemented by Experimenter B; see `experiments/proto/README.md` and `run_r2.sh`.

```bash
cd paper/experiments/proto
STAGES="p1 p1tb p2 p4" RUNS=5 bash run_r2.sh     # ~47 min
python agg_r2.py                                  # writes proto_*_r2_agg.csv
```

All values are means of 5 runs with Student-t 95% CIs in brackets. The raw logs are in `raw/proto/r2_run.stdout`. Scheme labels:

| Label | Scheme |
|---|---|
| b1 | HMAC |
| b5s | **M2**: stapled per-token ML-DSA-44, using the 401 Staple-Required retry path |
| o1 | **pooled EMBER**, tree of 32 tokens, root stapled |
| b5 | per-token ML-DSA-44, unstapled |

The setup is the same as before: a Go 1.24.7 edge pinned to 1 core, three network namespaces and two tapbridge links. The limitation still holds that everything runs on one VM.

## P1: edge capacity, closed loop (`proto_capacity_r2_agg.csv`, edge namespace over loopback)

| scheme | req/s | edge CPU µs/req | ratio vs HMAC | edge util |
|---|---|---|---|---|
| b1 HMAC | 38,088 [36,787–39,390] | 25.90 [25.03–26.76] | 1 | 0.986 |
| b5s M2 | 38,849 [36,882–40,816] | 25.35 [24.01–26.70] | 1.02 [0.94–1.10] | 0.984 |
| o1 pooled EMBER | 36,174 [35,125–37,223] | 27.23 [26.50–27.96] | 0.95 [0.93–0.97] | 0.985 |
| b5 ML-DSA-44 | 12,733 [12,086–13,380] | 77.52 [73.79–81.25] | 0.33 [0.32–0.35] | 0.986 |

**P1 across the emulated link** (`proto_capacity_tb_r2_agg.csv`):
- **b1, b5s, o1:** each achieves about 24.4–24.7k req/s. The edge sits at 0.69–0.71 utilisation, so these runs are **link-bound**, and their req/s are lower bounds on capacity.
- **b5:** 12,226 req/s at 0.99 edge utilisation, so it is edge-bound.

**Finding.** With staple-once-per-connection, M2 is statistically indistinguishable from HMAC at the edge. Pooled EMBER is 5% below HMAC. These numbers come from the synthetic loadgen session pattern, where each connection carries many requests per token.

## P2: latency under open-loop load across the link (`proto_latency_r2_agg.csv`)

At 50% and 80% of each scheme's own P1 capacity, the added median latency vs HMAC is:

| scheme | 50% load | 80% load |
|---|---|---|
| M2 | +0.006 [−0.045, 0.057] ms | −0.052 [−0.20, 0.10] ms |
| pooled EMBER | −0.004 [−0.026, 0.017] ms | −0.106 [−0.26, 0.05] ms |
| b5 | **+0.81 [0.77, 0.84] ms** | **+1.55 [0.94, 2.16] ms** |

The p99 CIs are wide and overlap zero for every scheme except as noted in the CSV, so we make no p99 claims.

## P4: recovery (`proto_recovery_r2_agg.csv`, `proto_recovery_events_r2.csv`)

The workload averages 20.5–20.6 requests per token and 1.19 new connections per token, and about 1,160–1,170 client moves per run. The base RTT from client to edge is about 20.3 ms. Zero requests failed in any scenario.

| scenario | scheme | recoveries / 1k req | extra delay per recovery (mean / p99) | edge ML-DSA verifs / token |
|---|---|---|---|---|
| cold cache | M2 | 0 | — | 1.19 |
| cold cache | EMBER | 0 | — | 0.41 |
| flush mid-run (connections kept; 401→retry) | M2 | 6.08 [5.81–6.35] | 35.8 / 62.4 ms | 1.32 |
| flush mid-run | EMBER | 4.40 [4.15–4.66] | 35.8 / 61.9 ms | 0.50 |
| edge restart (all connections dropped) | M2 | 6.17 [5.92–6.43] (760 reconnects) | 262.9 [234.5–291.3] / 426.7 ms | 0.76 |
| edge restart | EMBER | 6.38 [5.92–6.85] (787 reconnects) | 257.7 [229.0–286.3] / 429.2 ms | 0.30 |
| cache capped at 64 entries | M2 | **551 [533–570]** (55% of requests) | 22.9 / 40.9 ms | 12.6 |
| cache capped at 64 entries | EMBER | 100 [87–113] (10% of requests) | 23.1 / 42.0 ms | 2.18 |
| cache capped at 256 entries | M2 | 0.04 | 22.7 ms | 1.19 |
| cache capped at 256 entries | EMBER | 0 | — | 0.41 |

Median request latency with a 64-entry cache is 41.7 ms for M2 against 20.4 ms for EMBER. The staple header bytes per token are 3,877 for M2 and 3,934 for EMBER on a cold cache. They rise to 40,699 for M2 and 10,693 for EMBER with a 64-entry cache.

## What this means for the paper's claims

1. **Edge CPU, prototype run (closes the gap).** "Stapling fixes the edge" is confirmed for the synthetic many-requests-per-connection workload: M2 runs at 1.02× HMAC and pooled EMBER at 0.95×. The paper should replace "recommended configuration not run on the prototype" in Limitations with these numbers.
2. **"Recovery costs one RTT" is only partly true.**
   - **Lost cache state, connection kept:** a retry costs about 35.8 ms on average, roughly 1.8× the 20.3 ms base RTT. That is about one extra round trip plus a re-verify and queueing; p99 is 62 ms.
   - **Edge restart:** this costs a reconnect, about 258–263 ms on average (p99 about 427 ms), roughly 13× the RTT. M2 and EMBER are statistically the same here, because the cost is the reconnect itself.
   - **Revise the claim:** say that recovery costs about one extra RTT when cache state is lost on a live connection, and a full reconnect after a restart. Recovery happened on about 6 of every 1,000 requests in our flush and restart scenarios.
3. **Cache sizing matters more for M2.** M2 needs one cache entry per token, while EMBER needs one per tree. With an undersized cache of 64 entries for about 6,000 tokens, M2 retries on 55% of requests against 10% for EMBER, and its median latency doubles. With 256 entries, neither retries. The paper's 24 B-per-entry memory estimate is unaffected, but it should warn about cache sizing.
4. **Edge ML-DSA verifications per token are about 3× lower for pooled EMBER** in every scenario (0.41 vs 1.19 on a cold cache), because one root covers many tokens. This is consistent with the trace finding that EMBER's edge advantage grows as requests per token shrink.
