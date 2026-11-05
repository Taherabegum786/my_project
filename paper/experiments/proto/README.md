# E8 prototype and E3b HPACK measurement (Experimenter B)

Go module `emberproto` (Go 1.24.7, `GOTOOLCHAIN=local`; `github.com/cloudflare/circl v1.6.1` for ML-DSA-44/65,
Go stdlib for Ed25519 / ECDSA P-256 / HMAC / ML-KEM-768 / AES-GCM, `golang.org/x/net v0.38.0` for HPACK).

| Path | What |
|---|---|
| `tokens/` | Go port of the EMBER token format and baselines B1-B3, B5/B5v, B6, B9, B10, B11, B12. `go test ./tokens/` runs round-trip/negative tests **and the shared Python test vectors** (`../tests/vectors.json`, 128 checks). |
| `edge/` | HTTP edge verifier: token from `?Token=` or `Edge-Token` cookie; per-virtual-edge root cache (`X-VEdge`), singleflight coalescing, negative cache, pull-on-miss `GET <origin>/root/<kid>/<e>`, stapled root (`X-EMBER-Root`), B5v verify cache, `o1a` = one root-signature verification per 1000 requests. |
| `issuer/` | Issuer + root service: timer-Δ epochs per kid, ML-DSA-44 (or hybrid) root, `/issue` blocks until the epoch closes. |
| `loadgen/` | `p1` closed loop, `p2` open-loop Poisson (latency from the scheduled send time), `p3` token sessions, `rtt` probe. Raw HTTP/1.1 keep-alive client. |
| `hpackbytes/` | E3b: per-session request-header bytes with the real HPACK encoder; `gen_slh.py` adds real SLH-DSA signatures (pqcrypto) since circl 1.6.1 has no SLH-DSA. |
| `gobench/` | Go crypto per-op costs (verify/sign/issue) → `results/proto_go_verify.csv`. |
| `netemu/` | `tapbridge.c` (copied from `git show origin/claude/brave-meitner-l8yswp:experiments/src/tapbridge.c`, the author's earlier artifact, plus a per-instance control-file patch) and `net3.sh` (3 netns, 2 tapbridges). `net.sh.orig` is the unmodified prior script. |
| `run_proto.sh` | Builds and runs everything: `STAGES="test hpack rtt p1 p2 p3 gobench agg" RUNS=5 bash run_proto.sh`. |
| `proto_agg.py` | P1/P2 aggregation (Student-t 95% CI over runs; P2 added latency vs HMAC paired by run). |
| `validate.py` | H8: prototype vs MC vs analytic model → `results/proto_validate.csv`. Uses `results/sim_proto_mc.csv` from Experimenter A's `fleet_mc` if present, else its own epoch-level replica of the fleet_mc pull/staple algorithm. |

## Topology (all on ONE 4-vCPU VM: a stated limitation)

```
ember_cli 10.71.0.2 --[tapbridge A: 10 ms one-way, 1 Gbit/s, MTU 1500]-- 10.71.0.1 ember_edge 10.72.0.1
          --[tapbridge B: 37.5 ms one-way]-- 10.72.0.2 ember_origin      (ember_edge forwards cli<->origin)
cores: loadgen 0 | edge 1 (GOMAXPROCS=1) | both tapbridges 2 | issuer 3
```
netem is not available in this kernel, so delay and serialisation come from the userspace tapbridge.
Processes in different namespaces still share the host CPU, memory bus and kernel: traffic crosses the
emulated links, but this is not a multi-host testbed.

## Experiments
- **P1 capacity** (edge ns loopback, so no tapbridge; measures edge CPU): closed loop, 64 keep-alive connections,
  each connection uses one token for K = 150 requests (a session), 5 s warm-up + 20 s, 5 runs, edge on 1 core.
  Loadgen on cores 0, 2, 3 so that the edge (not the generator) saturates; `cpu_util_edge` (from
  `/proc/<pid>/stat`) is reported for every run to show this.
- **P2 latency under load** over tapbridge A: open loop Poisson at 50% / 80% of each scheme's mean P1 capacity,
  1024 connections, 3 s warm-up + 15 s, 5 runs.
- **P3 dissemination validation**: pull and pull_staple, λ ∈ {20, 200} tokens/s (the four (mode, λ) pipelines run
  concurrently, each with its own kid and its own V virtual edges), V ∈ {10, 50}, Δ ∈ {0.1, 1, 10} s, 60 s issuance
  window per run (+ drain), segment interval 200 ms, K ~ geometric(mean 20), token-receipt-to-first-request
  lognormal(median 120 ms, σ 0.5), Zipf(0.8) edge choice, 5 runs. The edge keeps 64 pre-warmed keep-alive
  connections to the root service (as a CDN edge keeps persistent connections to its parent).
