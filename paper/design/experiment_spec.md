# EMBER experiment spec (for the Experimenter agent)

Read `design/design.md` first. This spec covers the engineering: modules, parameters, commands and CSV schemas. Every number in the paper must come from these scripts. **Do not `import oqs`.**

## 0. Environment
- Python: `VENV=/tmp/claude-0/-home-user-my-project/4a27d5c9-46a1-5d35-98ec-9a4e85dfb968/scratchpad/venv` (pqcrypto 1.0.0, cryptography 50.0.2, numpy, scipy, matplotlib; pandas if present, otherwise use csv/numpy). Record `pip freeze` to `results/env_pip_freeze.txt`. Record `lscpu`, `uname -a` and the OpenSSL version to `results/env.txt`.
- pqcrypto API: `from pqcrypto.sign import ml_dsa_44, ml_dsa_65, slh_dsa_sha2_128s, slh_dsa_sha2_128f`. Functions are `keygen() -> (pk, sk)`, `sign(sk, msg, context=None)` and `verify(pk, msg, sig, context=None)`; `verify` raises on failure. The object API is `SecretKey(sk).sign(...)`.
- Native backends:
  - (a) gcc + system OpenSSL 3.0 libcrypto (`-lcrypto`) for SHA-256 path verification and HMAC;
  - (b) Docker image `openquantumsafe/oqs-ossl3:latest` (OpenSSL 3.6.0, present locally; start dockerd with `nohup dockerd >/tmp/dockerd.log 2>&1 &` if needed). Use it for native ML-DSA/SLH-DSA/Ed25519/ECDSA/RSA sign and verify via `openssl speed` (see `experiments/probe/openssl_speed.sh`) and, ideally, a small C program linked against that image's libcrypto, using EVP_PKEY_sign/verify, built inside the container.
- Pinning: `taskset -c 2` for single-core benchmarks; the 4-process issuer run uses cores 0–3. Run `gc.disable()` during timed loops, use `time.perf_counter_ns()`, and warm up for 200 iterations.
- **Native primary (Critic):** OpenSSL 3.5.4 at `$SP/opt/ossl35` (already built; recipe in `scout/feasibility.md`). Set `LD_LIBRARY_PATH=$SP/opt/ossl35/lib` and `OPENSSL_CONF=$SP/opt/ossl35/ssl/openssl.cnf`, and compile with `-I$SP/opt/ossl35/include -L$SP/opt/ossl35/lib -lcrypto`. **All issuer-cost and edge-CPU claims use these numbers.** Docker oqs-ossl3 is a cross-check only.
- **Go:** `/usr/local/go/bin/go` 1.24.7, with module `github.com/cloudflare/circl v1.6.1` (fetch verified working through the proxy) for ML-DSA-44 and `golang.org/x/net/http2/hpack` for E3b.
- **Seeds.** Global `SEED=20261105`. Simulation replicate r uses `SEED + 1000*r`.
  - Use **≥ 5 replicates** everywhere, and 10 for the controller headline (`sim_controller_summary`).
  - Use **common random numbers**: the same seeds across policies and modes.
  - Report the mean and a **Student-t 95% CI** (t₄ = 2.776 for 5 reps, t₉ = 2.262 for 10). For every "A better than B" claim, also report the **paired-difference CI**.
- **Micro-benchmark statistics.** ≥ 5 independent process runs (fresh process per run, pinned core) × n_iter per run. Report the median of run-medians and a bootstrap CI over run-medians (2000 resamples), plus pooled p99. Record `/sys/devices/system/cpu/cpu*/cpufreq/scaling_governor` (if present) and `/proc/stat` steal time before and after each run in `results/env.txt`.

## 1. Directory layout (`paper/experiments/`)
```
experiments/
  README.md                 # how to reproduce; maps every figure/table -> script -> CSV
  run_all.sh                # runs everything end-to-end (with QUICK=1 smoke mode)
  ember/
    __init__.py
    th.py                   # tweakable hash Th(tweak, data) w/ truncation n∈{16,32}; tweak packer
    merkle.py               # build_tree(e, leaves)->(root, levels); auth_path(levels,i); root_from_path(...)
    token.py                # Claims dataclass, canonical enc(), wire encode/decode (signed URL & cookie forms)
    signers.py              # uniform Signer interface for all root/per-token signers (see §2)
    issuer.py               # EmberIssuer: queue, close_epoch(), period bundles, revocation deltas
    edge.py                 # EmberEdge: RootCache (coalescing, negative cache), verify(token, now, url)
    controller.py           # FixedDelta, WorkConserving, Adaptive (D(Δ) model, constraints)
    model.py                # analytical formulas (size, throughput, latency, M(Δ), bandwidth)
  baselines/
    pertoken.py             # per-token token schemes B1..B9 sharing ember.token claim encoding
  bench/
    bench_primitives.py     # E1 (python backends)
    bench_tokens.py         # E2 sizes, verify, issuer throughput (python)
    fit_analysis.py         # E3
    native/
      pathverify.c          # SHA-256 Th + path verify + HMAC-SHA256, libcrypto; CLI prints CSV
      Makefile
      oqs_sigbench.c        # EVP sign/verify loop (built & run inside oqs-ossl3 container)
      evp_sigbench.c        # PRIMARY: EVP sign/verify/keygen + ML-KEM-768 encap/decap, OpenSSL 3.5.4 (scratchpad)
      run_native.sh         # builds & runs all, 5 runs each, writes results/native_*.csv
  sim/
    workload.py             # tenants, diurnal NHPP, edge shares, sessions, RTT samplers
    fleet_mc.py             # vectorised epoch-level Monte Carlo (E5 main)
    des.py                  # per-request discrete-event simulator (validation, E5v) using heapq
    dos.py                  # E7
    run_sim.py              # CLI: --exp {sweep_delta,controller,dissem,e2e,sens,validate,dos}
  proto/                    # E8 real prototype (Go module, circl v1.6.1, x/net)
    go.mod
    tokens/                 # Go port of token encode/verify for all schemes (must pass the shared test vectors)
    edge/main.go            # edge verifier: query/cookie token, V virtual edges, root cache + singleflight, neg cache, verify-LRU
    issuer/main.go          # issuer + root service: timer-Δ epochs, ML-DSA-44 (circl) root, per-token modes, /root/<kid>/<e>
    loadgen/main.go         # closed-loop (P1) and open-loop Poisson sessions (P2/P3); writes CSV
    hpackbytes/main.go      # E3b: per-session header bytes with hpack encoder
    net/                    # tapbridge.c + net3.sh (3 netns: cli, edge, origin; 2 tapbridge instances)
    run_proto.sh            # builds, sets up netns, runs P1-P3 x 5 runs, tears down
  plots/
    style.py                # common matplotlib style (IEEE column width 3.5in, 8pt fonts, colorblind palette)
    make_figures.py         # fig2..fig9 from CSVs -> results/figs/*.pdf
    make_tables.py          # LaTeX tables tab2..tab4 -> results/tables/*.tex
  tests/
    test_ember.py           # correctness + negative tests (pytest or plain asserts)
```
Outputs go to `paper/results/` (CSV), `paper/results/figs/` (PDF + PNG) and `paper/results/tables/` (.tex).

## 2. Core interfaces

```python
# ember/th.py
CTX = b"EMBERv1\0"
TYPE_LEAF, TYPE_NODE, TYPE_ROOT, TYPE_PERIOD = 0, 1, 2, 3
def tweak(kid:int, epoch:int, typ:int, level:int, index:int) -> bytes  # 8+4+4+1+1+4 = 22 B, big-endian
def Th(tw:bytes, data:bytes, n:int) -> bytes    # hashlib.sha256(tw+data).digest()[:n]

# ember/merkle.py  (RFC 9162-style: split at largest power of two < N; or simple pairwise w/ promote-odd — pick pairwise-promote, document it)
def build_tree(kid, epoch, leaves:list[bytes], n) -> (root:bytes, levels:list[list[bytes]])
def auth_path(levels, i) -> list[bytes]            # promoted (unpaired) nodes contribute no sibling
def root_from_path(kid, epoch, i, N, leaf, path, n) -> bytes   # needs N to know promotions

# ember/token.py
@dataclass
class Claims:
    url_prefix: str
    expires: int
    tenant: int
    ip: str|None
def enc(c) -> bytes                                # canonical: "URLPrefix=<b64url>:Expires=<int>:Tenant=<int>[:IP=<cidr>]"
def encode_ember(c, kid, epoch, idx, r, path, n, alg) -> str   # claims + ":E=" + b64url(ver|alg|kid|epoch|idx|r|path)
def encode_pertoken(c, scheme, sig) -> str          # claims + ":Sig=" + b64url(sig)  (hybrid: sig = ed||mldsa)
def to_signed_url(base_url, token) -> str           # base_url + "?Token=" + token  (len counted in bytes)
def to_cookie(token) -> str                         # "Edge-Token=" + token  (Set-Cookie value size)

# ember/signers.py
class Signer:  name; keygen(); sign(msg)->bytes; verify(msg, sig)->bool; sig_len; pk_len
# implementations: HMACSHA256, Ed25519, ECDSAP256 (DER, SHA-256), RSA2048 (PKCS1v15, SHA-256),
# MLDSA44, MLDSA65, SLHDSA128s, SLHDSA128f (pqcrypto, context=b"EMBER-root" for roots / b"CDN-token" per-token),
# HybridEd25519MLDSA44 (both must verify)
# Critic baselines:
#   MultiMAC(k)            -> k truncated 16-B HMAC tags, independent keys (B10)
#   DelegatedEd25519       -> ML-DSA-44-signed epoch cert {kid, ed_pk, not_after}; token = claims+Ed25519 sig+cert id (B11)
#   KemWrappedHMAC         -> per-epoch k_e; wrap = ML-KEM-768 encaps to each edge pk + AES-GCM/HKDF of k_e; token = HMAC_k_e (B12)
#   MTLMode                -> single growing Merkle series per key; ladder re-signed every Δ; condensed sig = idx|rung_id|path (B13)
# VerifyCache wrapper: LRU(SHA-256(token)) -> accept until Expires; applies to any scheme (B5v/B6v and ablation for EMBER)

# ember/issuer.py
class EmberIssuer:
    def __init__(self, signer, kid, n=16, period_m=300, rng=None, pad_pow2=False)
    def submit(self, claims) -> int                # returns ticket
    def close_epoch(self, t_now) -> (SignedRoot, dict[ticket->token_str], timings)
    def close_period(self) -> PeriodBundle
    def revoke(self, epoch, idx)
# ember/edge.py
class EmberEdge:
    def __init__(self, pk_signer, kid, n, v_max, fetch_fn, negative_ttl)
    def verify(self, token_str, now, url, stapled:bytes|None=None) -> (ok:bool, reason:str, needed_fetch:bool)
```

**Test requirements (`tests/test_ember.py`).** All of these must pass before any benchmark runs.
- Round-trip at N ∈ {1, 2, 3, 5, 8, 1000, 1025} and n ∈ {16, 32}.
- Each of the following must be rejected:
  - one flipped bit in the claims, salt, path or index;
  - the epoch id swapped to another valid epoch;
  - a root signed under a different kid;
  - an expired token, and Expires > T_start + Δ + V_max;
  - a revoked (e, i);
  - a period-bundle root with a tampered list;
  - for the hybrid, either half's signature corrupted.
- Every per-token baseline: valid accepted, tampered rejected.
- (Critic) Cross-tenant: a leaf from tenant A replayed with Tenant = B in a pooled tree is rejected; the tenant id is in the leaf tweak.
- (Critic) Cross-kid replay is rejected. An edge clock skewed by +τ_skew/−τ_skew accepts; one skewed by 2τ_skew rejects at the boundary.
- (Critic) idx ≥ N_e is rejected. The epoch counter refuses to wrap.
- (Critic) B11: an expired delegated key is rejected; Ed25519 under a non-certified key is rejected. B12: a wrong-epoch key is rejected.
- (Critic) Shared JSON test vectors (`tests/vectors.json`) generated by Python must verify identically in the Go `proto/tokens` package.

## 3. Experiments, parameters, CSV schemas

### E1. `bench/bench_primitives.py` → `results/micro_primitives.csv`
- Schemes: HMAC-SHA256, Ed25519, ECDSA-P256, RSA-2048, ML-DSA-44, ML-DSA-65, ML-DSA-87, SLH-DSA-SHA2-128s, SLH-DSA-SHA2-128f, Hybrid(Ed25519+ML-DSA-44), plus Th at n = 16/32 on 64-byte and 200-byte inputs.
- Operations: keygen, sign, verify (Th: hash).
- Message: a 200-byte claim string.
- Repetitions: n_iter = 2000 for everything except keygen/sign of SLH-DSA-128s (30) and SLH-DSA-128f sign (200).
- Columns:
  `scheme,op,backend,n_iter,median_us,p99_us,mean_us,ci95_lo_us,ci95_hi_us,sig_bytes,pk_bytes`
  - CIs: bootstrap of the median, 2000 resamples.
  - backend ∈ {pqcrypto-1.0.0, cryptography-50.0.2, hashlib}.
- Also save the raw samples: `results/raw/micro_<scheme>_<op>.npy`, used for the CDFs and as simulator input.
- **A1 investigation.** Time ML-DSA-44 sign via the flat `sign` and the object API, and via `hash_algorithm=None` vs a pre-hash variant if available. Write the findings to `results/notes_A1_mldsa_sign.md`.

### E1n. `bench/native/run_native.sh` → `results/native_pathverify.csv`, `results/native_sig.csv` (PRIMARY timing source)
- **`evp_sigbench.c` against OpenSSL 3.5.4 (scratchpad).**
  - Ops: keygen/sign/verify for ML-DSA-44/65/87, SLH-DSA-SHA2-128s/128f, Ed25519, ECDSA-P256, RSA-2048; ML-KEM-768 keygen/encaps/decaps.
  - Repetitions: 5 runs × 2000 iterations (SLH-DSA-128s sign 5 × 10; SLH-DSA-128f sign 5 × 100). Fresh process per run, `taskset -c 2`, warm-up 200 iterations.
  - Columns: `scheme,op,impl,run,n_iter,median_us,p99_us,mean_us`. Write the aggregate to `native_sig_agg.csv` with `ci95_lo_us,ci95_hi_us` (bootstrap over run-medians), `impl=openssl-3.5.4-native`.
- `pathverify.c` is also linked against OpenSSL 3.5.4, and also runs 5 runs.
- `pathverify.c` (libcrypto SHA-256; also try SHA-NI if OpenSSL uses it automatically):
  - for d ∈ {4, 8, 10, 12, 14, 16, 18, 20, 24} and n ∈ {16, 32}, time 10⁶ path verifications; also time HMAC-SHA256 over the 200 B claims, 10⁶ times;
  - columns: `op,d,n,iters,ns_per_op_median,ns_per_op_p99`. Use batches of 1000 and per-batch timing to obtain the distribution.
- `oqs_sigbench.c` or `openssl speed` in the container, for ML-DSA-44/65, SLH-DSA-128s/f, Ed25519, ECDSA-P256, RSA-2048:
  - columns: `scheme,op,backend,us_per_op,ops_per_s`, with backend = "openssl-3.6.0+oqsprovider (docker, 1 core)".
  - If only `openssl speed` works, reuse the parser from `experiments/probe/`.

### E2. `bench/bench_tokens.py`
- **Sizes** → `results/token_sizes.csv`.
  - Each scheme B1–B9 and O1–O4, plus EMBER at log2N ∈ {0, 2, 4, …, 24}.
  - Claims variants: url_path_len ∈ {40, 60, 120, 250}, with_ip ∈ {0, 1}.
  - Columns: `scheme,root_signer,n,log2N,url_path_len,with_ip,claims_bytes,auth_bytes_raw,token_bytes,signed_url_bytes,cookie_bytes`.
  - EMBER rows use measured lengths of actually generated tokens; the analytic values go only to `model_check.csv`.
- **Edge verify** → `results/token_verify.csv`.
  - Per scheme, 5000 verifications of distinct tokens, measuring the full `verify()`: parse + policy + crypto.
  - EMBER with warm cache at log2N ∈ {4, 8, 12, 16, 20}, plus a cold-cache variant: verify includes root-signature verification (fetch_fn returns instantly) to show the amortisation cost.
  - Columns: `scheme,root_signer,n,log2N,cache,iters,median_us,p99_us,mean_us,ci95_lo_us,ci95_hi_us`.
- **Issuer throughput** → `results/issuer_throughput.csv`.
  - Per-token schemes: tokens/s over a 10 s window, or 30 tokens for SLH-128s.
  - EMBER: N ∈ {1, 4, 16, 64, 256, 1024, 4096, 16384, 65536, 262144} × root signers {ML-DSA-44, ML-DSA-65, SLH-DSA-128s, SLH-DSA-128f, Hybrid}. Time `close_epoch` end to end (leaf hashing + tree + sign + token encoding) and report the components.
  - Columns: `scheme,root_signer,n,N,procs,t_leaf_us,t_tree_us,t_sign_us,t_encode_us,t_epoch_us,tokens_per_s`.
  - Also run procs = 4 (multiprocessing, one issuer shard per core) for O1 and for B5.
- **Model check** → `results/model_check.csv`: `quantity,scheme,param,predicted,measured,rel_err`.

### E2+ (Critic baselines) in `bench_tokens.py`
- Add B5v, B6v, B5c, B6c, B10 (k = 1, 3, 10), B11, B12 and B13 to `token_sizes.csv` and `token_verify.csv`.
- For the `+vcache` variants, report `cache=hit` and `cache=miss` rows, plus `amortised_us_per_req` for K = 150 segments at one edge.
- B12 issuer cost per epoch = E × ML-KEM-768 encaps (native) + E × AES-GCM; add it to `issuer_throughput.csv` with E ∈ {100, 500, 2000}.
- Also add EMBER `pad_pow2=1` rows (issuer cost).

### E3b. `proto/hpackbytes` → `results/wire_bytes.csv`
- Build each scheme's real token (via the shared Python test-vector generator, or the Go port).
- For a session of 1 manifest + K = 150 segment requests with realistic headers (`:method,:scheme,:authority,:path,user-agent,accept`, ~600 B total), encode with `hpack.NewEncoder` (4096-B table). Placements:
  - `url`: token in the query, so `:path` differs per segment;
  - `cookie`: same value every request;
  - `cookie2`: split across 2 cookie headers for B5c/B6c.
- HTTP/1.1 = raw byte length.
- EMBER: with and without `X-EMBER-Root` on the first request.
- Columns: `scheme,placement,proto,K,first_req_bytes,session_bytes,bytes_per_req_mean`.

### E3. `bench/fit_analysis.py` → `results/fit.csv`
- URL path length L ~ lognormal(median = 80 chars, σ = 0.5) (assumption, stated in Table IV), with 10⁵ samples; base URL host = "https://cdn.example.com".
- Limits:
  - `url2k` = 2048 B (practice);
  - `url8k` = 8000 B (RFC 9110 recommendation);
  - `cookie4k` = 4096 B (RFC 6265 minimum, name+value);
  - `hdr8k` = 8192 B total request headers (assumed default), counting the cookie plus 600 B of other headers.
- Columns: `scheme,root_signer,n,log2N,limit,fraction_fit,median_bytes,p99_bytes`.

### E5. Simulation (`sim/`)
**Workload (`workload.py`), defaults:**
| Parameter | Default | Sweep |
|---|---|---|
| Edges E | 500 | 100, 500, 2000 |
| Edge share w | Zipf α_e = 0.8 over edges | 0, 0.8, 1.2 |
| Tenants T | 1000 | — |
| Tenant rate share | Zipf α_t = 1.0 | 0.8, 1.2 |
| Aggregate mean λ̄ | 2000 tokens/s | 200, 2000, 20000 |
| Diurnal | λ(t) = λ̄_τ(1+0.6 sin(2πt/86400)) (per-tenant phase φ ~ U(0, π/2)) | a ∈ {0, 0.6} |
| Duration | 24 h | QUICK = 1 h |
| Segments per session K | geometric, mean 150 | — |
| Segment interval | 4 s | — |
| V_max | 3600 s | 300, 3600, 86400 |
| Period m | 300 epochs (or P = 300 s when Δ varies: use P fixed in seconds) | P ∈ {60, 300, 1800} s |
| RTT client→edge | lognormal median 20 ms, σ = 0.6 | ×0.5, ×2 |
| RTT edge→shield | lognormal median 15 ms, σ = 0.5 | ×0.5, ×2 |
| RTT shield→root service | lognormal median 60 ms, σ = 0.5 | ×0.5, ×2 |
| Push propagation delay | lognormal median 150 ms, σ = 0.5 | ×0.5, ×2 |
| Token receipt → first request | lognormal median 120 ms, σ = 0.5 | — |
| Crypto costs | resampled from E1 raw .npy (python) **and** a second run using E1n native medians | — |
| Mean segment bytes (bandwidth ratio only) | 1.5 MB (assumption) | 0.5, 4 MB |

**Modes:** `pull`, `push`, `pull_staple`, `pull_rollup`, `push_rollup`.
**Policies:** `fixed:<Δ>` for Δ ∈ {0.01, 0.1, 1, 10, 60}, `wc`, `adaptive` (L_SLO = 2 s p99, token budget B = 1024 B, n = 16, grid of 25 log-spaced values in [0.01, 60] s, EWMA α = 0.2). Pooling: `pool=0` (per-tenant tree) or `pool=1` (tenants hashed into 8 shared issuer shards).

**`fleet_mc.py` algorithm** (per tenant, per epoch):
1. Draw N ~ Poisson(∫λ dt over the epoch).
2. Draw edge counts ~ Multinomial(N, w).
3. Draw first-request arrival offsets per token.
4. For each edge with count > 0, find the earliest arrival.
5. Decide whether a miss occurs:
   - **pull:** the root is not in that edge's cache, i.e. this is the first (edge, epoch) occurrence. With roll-up and a closed period, the first (edge, period) occurrence instead.
   - **push:** the arrival precedes push-delivery time.
   - **staple:** the miss costs 0 RTT but adds stapled bytes and one signature verification.
6. Miss latency = edge→shield RTT; plus shield→root RTT if the shield also lacks it (track the shield cache likewise; shields = E/10, edges map to shields).
7. Coalesced waiters (other tokens arriving at that edge before the fetch completes) also wait the residual time.

Track per-edge root caches as sets keyed by (tenant, epoch) or (tenant, period), with expiry at V_max + P. Accumulate:
- issuance waits (exact, from arrival times within the epoch);
- root misses; requests (N·(1+K));
- bytes (push, pull, staple);
- edge CPU (requests × path-verify cost sampled + signature verifications × t_v).

**`des.py` (validation).** Per-request event simulation for 1 h, λ̄ = 200, E = 100, T = 50, all modes and fixed Δ ∈ {0.1, 1, 10}. It must match fleet_mc on misses/token and mean issuance wait within the CIs. Write `results/sim_validate.csv`: `mode,delta,metric,des_value,mc_value,rel_diff`.

**CSV outputs:**
- `results/sim_delta_sweep.csv`: `mode,policy,delta_s,lambda_bar,E,alpha_e,pool,rep,issue_wait_mean_s,issue_wait_p99_s,miss_per_token,miss_per_mreq,miss_latency_p99_ms,D_mean_s,root_bw_fleet_Bps,root_bw_ratio,edge_cpu_us_per_req_mean,edge_cpu_us_per_req_p99,sig_verifs_per_edge_per_s,tok_bytes_p50,tok_bytes_max,model_miss_per_token,model_D_s`
- `results/sim_controller_ts.csv` (5-min bins over 24 h): `policy,mode,t_bin_s,lambda_hat,delta_chosen_s,issue_wait_p99_s,miss_per_token,D_mean_s,tok_bytes_max,slo_violation`
- `results/sim_controller_summary.csv`: `policy,mode,pool,rep,D_mean_s,issue_wait_p99_s,slo_violation_frac,budget_violation_frac,miss_per_token,root_bw_fleet_Bps`
- `results/sim_dissem.csv`: `mode,E,delta_s,P_s,rep,root_bw_fleet_Bps,root_bw_per_edge_Bps,miss_per_mreq,edge_root_state_bytes,staple_bytes_per_session`
- `results/sim_e2e_latency.csv`: per-request added-latency samples, reservoir 10⁵ per (scheme, mode). Columns `scheme,mode,sample_ms`. Per-token baselines have zero miss latency but higher CPU.
- `results/sim_sens.csv`: `param,value,metric,mean,ci_lo,ci_hi`

**Critic additions to the simulation:**
- Policies also include `oracle_fixed`: per tenant-rate decile, the fixed Δ with the lowest D in hindsight, chosen from the `sweep_delta` results at the same seeds.
- Add baselines B11 and B12 to `sim_dissem.csv` (they share the per-epoch push/pull path; B12 is push-only at E·1120 B/epoch).
- Add columns `refresh_per_session` and `revocation_propagation_s`.
- `des.py` remains, but its CSV is labelled `internal_consistency`. The **validation** is E8 P3 (below).

### E8. Real prototype → `results/proto_capacity.csv`, `results/proto_latency.csv`, `results/proto_validate.csv`
- **Network.** `proto/net/net3.sh` builds netns `cli`, `edge`, `origin` with two `tapbridge` instances, adapted from `git show origin/claude/brave-meitner-l8yswp:experiments/src/tapbridge.c` and `.../scripts/net.sh` (copy; reused tooling, cite as the author's prior artifact):
  - cli↔edge one-way delay 10 ms;
  - edge↔origin one-way delay 37.5 ms;
  - 1000 Mbit/s, MTU 1500, offloads off.
  - Cores: loadgen 0, edge 1 (`GOMAXPROCS=1`), both tapbridges 2, issuer 3.
  - If netns/TAP setup fails, fall back to loopback, record `net=loopback` in every CSV row, and state it in the limitations. Never silently.
- **P1 capacity** (inside the `edge` ns, loadgen over that ns's loopback, so no tapbridge, measuring CPU):
  - closed loop with 64 connections, keep-alive, 20 s per run after 5 s warm-up, 5 runs;
  - schemes B1, B2, B3, B5, B5v (hit ratio set by K = 150), B11, B12, O1-warm, O1 with root verify every N_req = 1000 (amortised);
  - columns: `scheme,run,req_per_s,cpu_util_edge,p50_ms,p99_ms`.
- **P2 latency under load** (over tapbridge): open loop at 50% and 80% of each scheme's P1 capacity, 30 s × 5 runs. Columns: `scheme,load_frac,run,p50_ms,p99_ms,added_p50_ms_vs_hmac`.
- **P3 validation**:
  - modes `pull`, `pull_staple`; V ∈ {10, 50} virtual edges with Zipf(0.8) shares; Δ ∈ {0.1, 1, 10} s; λ ∈ {20, 200} tokens/s;
  - segment interval compressed to 200 ms and K ~ geometric(mean 20) to keep runs at 5 min; 5 runs each;
  - measured: misses/token, mean and p99 miss-added latency, root bytes;
  - then run `fleet_mc` and `model.py` with **the same parameters and the RTT distribution measured in the prototype** (ping-style probe through tapbridge, recorded);
  - columns: `mode,V,delta_s,lambda,metric,proto_mean,proto_ci_lo,proto_ci_hi,mc_mean,model_value,rel_err_mc,rel_err_model`.
- Wall-time cap for E8: ≤ 60 min. If it is exceeded, drop V = 50 first, then λ = 20.

### E7. `sim/dos.py` → `results/dos.csv`
- One edge; attack rate ∈ {10², 10³, 10⁴} fake tokens/s with random epochs within the acceptance window; 60 s.
- Variants: coalescing + negative cache on/off; stapled-root flood (each fake token carries a stapled root with an invalid signature).
- Columns: `variant,attack_rate,root_fetches_per_s,sig_verifs_per_s,edge_cpu_frac_1core`. CPU fraction comes from measured verify costs.

## 4. Figures and tables (`plots/make_figures.py`, `make_tables.py`)
| ID | File | Source CSV | Content |
|---|---|---|---|
| Fig 1 | (Writer, TikZ) | — | Architecture |
| Fig 2 | `figs/fig2_token_sizes.pdf` | token_sizes.csv | Bars of signed_url_bytes and cookie_bytes per scheme (url_path_len = 60, no IP), log y, limit lines 2048/4096/8000 |
| Fig 3 | `figs/fig3_size_vs_N.pdf` | token_sizes.csv, issuer_throughput.csv, model_check.csv | EMBER size vs log2N (n = 16/32, measured markers + model line); right axis tokens/s per core |
| Fig 4 | `figs/fig4_verify_cost.pdf` | token_verify.csv, native_*.csv | Median + p99 per scheme, log y; two panels: Python, native |
| Fig 5 | `figs/fig5_delta_tradeoff.pdf` | sim_delta_sweep.csv | x = Δ (log); y1 = issue_wait_mean, y2 = miss_per_token, D(Δ) model vs sim; 3 λ̄ curves; pull mode |
| Fig 6 | `figs/fig6_controller_24h.pdf` | sim_controller_ts.csv | 3 stacked panels: λ̂, Δ chosen, D / p99 wait; adaptive vs fixed 0.1/1/10 s |
| Fig 7 | `figs/fig7_dissemination.pdf` | sim_dissem.csv | (a) fleet root bandwidth vs E per mode (log), (b) misses per 10⁶ requests vs E |
| Fig 8 | `figs/fig8_e2e_cdf.pdf` | sim_e2e_latency.csv | CDF of added latency per request (log x), schemes × modes |
| Fig 9 (opt.) | `figs/fig9_sens_heatmap.pdf` | sim_sens.csv / delta sweep | Δ × E → miss/token |
| Tab II | `tables/tab2_primitives.tex` | micro_primitives.csv, native_sig.csv | sizes, sign/verify median [CI], python & native |
| Tab III | `tables/tab3_fit.tex` | fit.csv | % fit per limit per scheme |
| Tab IV | `tables/tab4_simparams.tex` | (from workload.py defaults dump `results/sim_params.json`) | parameters + sweep ranges |
| Tab V (opt.) | `tables/tab5_controller.tex` | sim_controller_summary.csv | D, SLO/budget violations per policy |

Style: IEEE single-column width 3.5 in (Fig 6 may be double-column, 7.16 in), 8 pt font, a colorblind-safe palette, every figure saved as PDF + PNG at 300 dpi, no titles (captions are written in LaTeX).

## 5. Run commands
```bash
cd /home/user/my_project/paper/experiments
PY=$VENV/bin/python
$PY -m tests.test_ember                                   # must pass
taskset -c 2 $PY -m bench.bench_primitives --out ../results
bash bench/native/run_native.sh ../results
taskset -c 2 $PY -m bench.bench_tokens --out ../results
$PY -m bench.fit_analysis --out ../results
$PY -m sim.run_sim --exp validate --out ../results
$PY -m sim.run_sim --exp sweep_delta --reps 5 --out ../results
$PY -m sim.run_sim --exp controller --reps 5 --out ../results
$PY -m sim.run_sim --exp dissem --reps 5 --out ../results
$PY -m sim.run_sim --exp e2e --reps 5 --out ../results
$PY -m sim.run_sim --exp sens --reps 3 --out ../results
$PY -m sim.dos --out ../results
$PY -m plots.make_figures --in ../results --out ../results/figs
$PY -m plots.make_tables  --in ../results --out ../results/tables
# or: QUICK=1 bash run_all.sh  (1 h sim, fewer iters) then bash run_all.sh
```
### 5.1 Compute budget (Critic D12; mandatory)
| Block | Cap | How |
|---|---|---|
| E1 + E1n | 30 min | 5 runs; SLH-128s sign limited to 10 iters/run |
| E2/E2+/E3/E3b | 25 min | the issuer N = 262144 point only for O1 and O3 |
| sweep_delta | 30 min | **1 h stationary horizon** (no diurnal), λ̄ ∈ {200, 2000, 20000}, 5 reps; Δ = 0.01 only at λ̄ ≥ 2000 |
| controller | 40 min | 24 h at λ̄ = 200 and 2000 (10 reps); λ̄ = 20000 runs a 1 h peak window only (5 reps) |
| dissem/e2e/sens | 30 min | sens 3 reps → **raised to 5** but only for 1 h horizons |
| E8 prototype | 60 min | see the E8 caps |
| total | ≤ 3.5 h | run `QUICK=1` first. If any block's extrapolated time exceeds its cap, shorten its horizon, record this in `results/sim_params.json`, and footnote it in Table IV |

The simulator must **never materialise empty tenant-epochs**. Generate per-tenant arrival times (NHPP by thinning), assign epochs with `np.searchsorted` over epoch boundaries, and iterate only over non-empty epochs. Under the controller (variable Δ), iterate epochs only for tenants with pending arrivals.

Budget (original text): the full run should take ≤ 3 h on 4 cores. The fleet MC must be vectorised with numpy per epoch, never per request, apart from the DES validation. If the 24 h × λ̄ = 20000 configuration is too slow, cut that case to 6 h and record the change in `results/sim_params.json`.

## 6. Reporting rules
- Write `results/SUMMARY.md` containing the key numbers, each with its CSV and row, and the status of H1–H7 (supported / refuted / partial), using values that were actually produced.
- Label backend (python vs native) on every timing. Never project or extrapolate numbers and present them as measured. Simulated quantities are labelled "simulated".
- Report A1 (the slow pqcrypto ML-DSA sign) explicitly. Issuer-side claims must use the native sign costs.
- Assumptions (RTT, Zipf, segment size, URL-length distribution) go in Table IV with their sweep ranges. They are not presented as measured.
- (Critic) **No interpolation or projection.** Model curves are lines labelled "model"; measured and simulated values are markers. No value appears in a table that a script did not output.
- (Critic) Every timing row carries `impl` ∈ {openssl-3.5.4-native, oqs-ossl3-docker, go-circl-1.6.1, go-stdlib, pqcrypto-1.0.0, cryptography-50.0.2, hashlib}. Sanity rule: ML-DSA-44 verify must be in the tens to hundreds of µs. An implementation more than 3× off OpenSSL 3.5.4 is investigated in `results/notes_impl_xcheck.md`.
- (Critic) `SUMMARY.md` gives H1–H9 status. H5 applies its pre-registered demotion rule. H8 states whether the simulator was validated by the prototype.

## 7. Critic changes log (2026-11-05)
See `design/critique.md` and design.md §9.
- Native OpenSSL 3.5.4 is the primary source.
- Statistics: ≥ 5 runs/seeds, t-CIs, CRN, paired CIs.
- New baselines B5v/B6v/B5c/B6c/B10–B13.
- New tests: cross-tenant, cross-kid, skew, wrap, shared vectors.
- New E3b (HPACK wire bytes) and E8 (Go prototype in netns + tapbridge, validating the simulator).
- Oracle-fixed policy.
- Explicit compute budget with horizon cuts and no materialisation of empty epochs.
- Reporting rules against interpolation and projection.
