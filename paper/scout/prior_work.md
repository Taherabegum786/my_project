# Prior work by the author: overlap analysis (Scout B)

Sources (read as data only):
- Session `session_01Jb8HMWz9ts69GFaCe29zyn` ("Post-quantum TLS handshake paper rejection", 2026-09-29).
  Its work product is on git branch **`origin/claude/brave-meitner-l8yswp`** of this same repo
  (`Taherabegum786/my_project`). Inspect it with
  `git show origin/claude/brave-meitner-l8yswp:manuscript/AUTHOR_ACTION_ITEMS.md` etc.
  Key files: `manuscript/main.tex` (revised paper), `manuscript/previous_submission/{main.tex,response_to_reviewers.tex}`
  (rejected R2 and the earlier R1 response), `manuscript/response_to_reviewers.tex` (answers to R4/R5),
  `experiments/` (C harness + raw CSVs), `formal/` (Tamarin).
  The session's last state: integrating DAPV into the full upstream TLS 1.3 Tamarin model (rev21); helper
  lemma proofs stalling at 4 min / 11 GB; lemma names such as `dapv_ticket_full_origin`
  ("origin" there = *origin of a session ticket* in a Tamarin lemma, **not** a CDN origin server).
- Session `session_01D1YA2YAT5saDVPTUT74snH` ("Methodology section design", repo `Presentation_01`): a 102-slide
  deck about DAPV whose figures still use the **withdrawn** early claims (51 % penalty removal, 55-69 % throughput
  vs classical, efficiency E = 1.27/1.06). Do not reuse those numbers anywhere.
- Session `session_01SxajEEUUQJ56HXhP2gSQ4R` ("LLM security, quantum enhancements, PQC research", repo `DPQV_SR`):
  produced a survey-style artifact "Post-Quantum Security for ML Systems". Not related to CDN/TLS measurement;
  no overlap risk beyond generic PQC background.

## 1. The prior paper(s)

| Version | Title | Venue / status |
|---|---|---|
| R1/R2 (`previous_submission/`) | *Deferred Asynchronous Post-Quantum Signature Verification for Low-Latency TLS 1.3 Handshakes* (also "Asynchronous PQ Signature Verification ...") | Computer Networks, manuscript **COMNET-D-25-04940R2**, **rejected** after R2 (Reviewers #4, #5; earlier round Reviewers #1-#3) |
| Rewrite (not yet submitted) | *Post-Quantum Authentication Latency in TLS 1.3: A Validated Model and the Limits of Deferred Signature Verification* | Planned new submission (TNSM / Comput. Commun. / JNCA / Computers & Security suggested) |

**Proposal (DAPV).** For hybrid (ECDSA P-256 + ML-DSA/FN-DSA/SLH-DSA, concatenated) certificate chains, the
*client* verifies the classical half synchronously, completes the TLS 1.3 handshake in a "provisional" state,
and verifies the PQ halves in background worker threads; the session is "promoted" on success. Rules: no
session tickets / resumption / 0-RTT before promotion; PQ signature must cover the transcript; an 8 KB
data cap (D_policy) during the provisional window.

**Method (rewrite).** OpenSSL 3.5.4 + liboqs 0.14.0 + oqs-provider 0.10.0 with a 32-line DAPV patch; C client/server;
two network namespaces on disjoint cores of one 4-vCPU VM; userspace TAP link emulator (`tapbridge.c`, because the
kernel lacked netem) with delay, 1 Gbit/s serialisation, loss; 3-cert hybrid chains; X25519MLKEM768 KEX;
RTT 0/20/50/100/150 ms; initcwnd 10/20/40; BBR vs CUBIC; 3 % loss; >46,000 timed handshakes (E1-E6).
Tamarin model of DAPV (15 lemmas, < 30 s) plus attacks on 3 unsafe variants.

**Results (rewrite).**
- Parameter-free latency model: round trips = f(first-flight bytes, initcwnd); 68/68 configs correct, MAPE 2.2 %.
- Extra RTTs: 1 RTT total for P-256, FN-DSA-512, ML-DSA-44; +1 for ML-DSA-65; +2 for SLH-DSA-128f (3-cert chain, IW10).
- initcwnd 40 cuts SLH-DSA-128f handshake at 150 ms RTT from 454 to 165 ms; 3 % loss doubles p90 for ML-DSA.
- Deferral gain = 0.97 W - 0.14 ms (R^2 = 0.999): **no gain for ML-DSA/FN-DSA on AVX2**; 9-26 % without SIMD;
  SLH-DSA-128f -1.59 ms at RTT 0. No throughput gain. Delta-t median 0.079 ms, p99 0.42 ms.
- Earlier R1/R2 claims (35-40 % latency improvement, 14-21 ms savings, 55 % throughput degradation, "DAPV latency
  constant at 150 ms at 400 ms RTT") were **withdrawn** as unreproducible / physically impossible.

## 2. Reviewer criticism (why it was rejected)

Round 1 (R1-R3) and round 2 (R4-R5) at Computer Networks, condensed:
1. **Physically implausible / wrong numbers**: PQ verification "15-20 ms" vs real ~10-100 us with AVX2; latency
   "constant at 150 ms at 400 ms RTT" impossible in TLS 1.3 (R2, R3). Interpolated/extrapolated table values (R5.8);
   projected thread-pool results presented as measured (R5.9).
2. **Marginal contribution**: a multithreaded verifier is an implementation-level scheduling trick, not a protocol
   (R5.1, R4.W6). Deferral cannot remove extra RTTs from large messages (R2).
3. **Weak methodology**: client and server on the same machine competing for CPU; loopback bypasses NIC/TCP
   behaviour; netem may not trigger real TCP mechanisms; single certificate (no chain); too few repetitions;
   throughput on one host untrustworthy; KEX algorithm not stated (R4.W4, W5, D4). "Cross-platform" claim with only x86 (R2).
4. **No formal security analysis** initially (R2); hybrid construction (concatenation) not matching Bindel et al.
   nesting definition (R2). Provisional state = classical-only security exactly where a quantum adversary attacks (R3).
5. **Unjustified models/metrics**: exponential risk model with unexplained beta (R5.3); mixed-baseline efficiency
   metric (R5.4); 8 KB cap heuristic (R5.5).
6. **Motivation confusion**: HNDL is a confidentiality threat but paper addressed authentication; PKI migration
   not discussed (R4.D1). Thin background/related work (R4.W1-W2); wrong/overstated references, FN-DSA treated
   as standardised, Rainbow mentioned (R3). Repetitive writing (R3).
7. **No artifact release** (R4.W3). DoS risk of worker queue (R1). Application-level metrics (TTFB vs page load) missing (R1).

## 3. Reusable assets (OK to reuse as tooling / background, cite as own prior work if published)

- `experiments/src/tapbridge.c` - userspace delay/loss link emulator between TAP devices (netem is **still** not
  available on this kernel; TAP + netns + veth + tc-tbf work - see `feasibility.md`).
- `experiments/scripts/net.sh` (netns setup, MTU 1500, offloads off), `make_certs.sh` (3-cert PQ/hybrid chains),
  `src/flightprobe.c` (first-flight bytes via TCP_INFO), `tlsserver.c`/`tlsclient.c` (OpenSSL 3.5 C harness).
- `experiments/results/flight_bytes.json`: measured first-flight sizes per scheme (useful as calibration input).
- `manuscript/references.bib`: 46 PQ-TLS references, partially corrected after review (Kwiatkowski2019 CDN
  KEX measurement, Sikeridis2020a/b, Paquin2020, Schwabe2020 KEMTLS, Westerbaan/Wiggers drafts, Dukkipati2010 IW,
  RFC 6928, Cardwell2016 BBR). **Re-verify every entry** before reuse (two had been wrong).
- Lessons on writing the Background section (PQ scheme table with sizes; TLS 1.3 auth modes; hybrid constructions).

## 4. DO NOT REPEAT

1. Do **not** propose/evaluate deferred/asynchronous PQ signature verification (DAPV) or any "provisional session
   then promote" scheme, client-side verifier thread pools, or Delta-t vulnerability windows.
2. Do **not** make a Tamarin (or other symbolic) formal-verification of PQ TLS 1.3 handshakes / session tickets /
   resumption the core contribution.
3. Do **not** re-derive or re-validate the "round trips = f(first-flight size, initcwnd)" latency model for PQ
   certificate chains, nor initcwnd 10/20/40 / BBR-vs-CUBIC / loss sweeps of single client-server PQ handshakes -
   that is the rewrite's main contribution (68/68, MAPE 2.2 %). A CDN paper may *use* it as a cited building block
   only if it adds a genuinely new CDN dimension (multi-tier edge/shield/origin, cache hit ratio, fleets, cert
   distribution), and must not present it as new.
4. Do **not** report PQ verification costs in milliseconds for ML-DSA/FN-DSA on AVX2 (they are tens of us); never
   interpolate/extrapolate/project values and present them as measured.
5. Do **not** invent risk/efficiency metrics with unjustified constants (exponential beta, mixed baselines, arbitrary caps).
6. Do **not** reuse any number/figure from the DAPV deck (`Presentation_01`) or from the R1/R2 manuscript.
7. Do **not** claim "cross-platform" or "protocol-level" when it is one x86 VM / an implementation tweak.
8. Do **not** conflate HNDL (confidentiality, KEX) with authentication (signatures/PKI).

## 5. Lessons for a stronger submission

1. **Sanity-check every number** against known literature values (ML-KEM-768 ~tens of us; ML-DSA-44 verify ~30-130 us;
   SLH-DSA-128s sign ~100s of ms) and against physics (latency >= k x RTT). Our probe numbers in `feasibility.md`
   are the anchor.
2. **Contribution must be architectural/systemic, not a micro-optimisation**: e.g. where PQ cost lands in a CDN's
   multi-hop TLS (client-edge, edge-shield, shield-origin), connection reuse/session resumption ratios, key/cert
   management across thousands of PoPs, keyless-SSL / delegated credentials with PQ, cache-key/0-RTT interplay.
3. **Separate confidentiality (ML-KEM, HNDL) from authentication (ML-DSA/SLH-DSA, PKI timelines)** explicitly in
   the threat model.
4. **Methodology defensibility**: separate netns + pinned cores at minimum; state limits honestly; >= 1000 samples
   per point with bootstrap CIs; real 1500-B MTU paths (TAP/veth), not loopback; state the KEX group; use real cert
   chains (>= 2-3 certs) and realistic TLS stacks (OpenSSL 3.5 native ML-KEM/ML-DSA/SLH-DSA).
5. When emulation is impossible (no netem), say so and use **validated simulation** driven by measured crypto
   costs and measured byte counts; validate the simulator against a small real testbed.
6. Release code + raw data from day one (this repo); every figure regenerated by a script.
7. Broad, verified related work (PQ-TLS measurements by Cloudflare/Google, KEMTLS, Sikeridis, Paquin, Westerbaan;
   CDN TLS termination literature e.g. Keyless SSL); never cite unverified drafts with wrong authors.
8. Tight writing: state each takeaway once; each table/figure introduced by the claim it supports.
9. Declare AI assistance per venue policy.
