# Gap: benchmark (cross-domain PQ signatures vs budget profiles)

Evidence: all 25 notes. [A] = abstract-only note (weak evidence).

## 1. Landscape

| Approach | Keys | Achieves | Leaves open |
|---|---|---|---|
| Single-domain size fit | junquera2023assessment, chen2025hybrid, abrar2026deployment, twardokus2024when | Which NIST signatures fit one budget | No common method across domains |
| PQ sig anchoring HMAC chain | darzi2026a | 324 B, one SIB1 vs 13-34 fragments | 5G SIB only; time sync |
| Symmetric broadcast auth | veara2025tbrd, hussain2026a | 68 B Remote ID auth; fast SV MAC | No PQ signature comparison |
| Fragmentation / multi-frame | goertzen2022post, rawat2024post [A], wiethuechter2024drip | PQ sigs over 1232 B DNS; FEC over 25 B frames | Request-response or classical-only |
| Few-time hash-based | sedghighadikolaei2024fast, sedghighadikolaei2024signer | Fast sign/verify | Stateful, finite capacity |
| MCU benchmarks | chhetri2026benchmarking, gringiani2023mayo [A], bauer2026mayo [A], aardal2024optimized [A], pornin2025falcon [A], halmans2026flying [A], nist2024pqm4 [A] | Cycles, RAM, timing tails | Not mapped to message budgets |
| Handshake feasibility envelopes | hyoung2026post [A], sikeridis2020post [A] | Algorithms mapped to channel conditions | Handshake, not handshake-free broadcast |

## 2. Gap

Each full-text size-fit study checks one domain against its own limit (junquera2023assessment, chen2025hybrid, abrar2026deployment, twardokus2024when, darzi2026a). Mode comparisons use only each paper's own baselines: darzi2026a against ML-DSA/FN-DSA fragmentation, veara2025tbrd against ECC only. Constrained-hardware timing is not tied to deadlines or message rates (chhetri2026benchmarking; the other MCU notes are [A]). The nearest work, hyoung2026post, builds a size-latency feasibility envelope, but it covers a ROS2/DDS handshake and our evidence is the abstract only (hyoung2026post [A]). So the gap is one benchmark that scores the same signature-based modes against several handshake-free broadcast profiles. The notes cannot rule out an existing SoK, because no survey was scouted.

## 3. Questions

1. Which (scheme, mode) pairs fit each profile? Profiles: C-V2X 437 B (twardokus2024when), Remote ID 25 B frames / 255 B auth (wiethuechter2024drip), OSNMA 16 DSM blocks (junquera2023assessment), SIB1 372 B (darzi2026a), DNS 1232 B (goertzen2022post). Metric: auth bytes per message, share of budget, frames per authenticated message.
2. At 0-30% loss, does a PQ-anchored chain beat fragmented signatures? Metrics: expected bytes per verified message, p95 time-to-authenticate, share of messages verified (darzi2026a gives one 10%-loss point).
3. Is size or the timing tail the binding constraint? Metric: deadline-miss rate, comparing p99 sign/verify with 3 ms (hussain2026a) and 100 ms (chen2026pseudonym). Tail data comes from chhetri2026benchmarking. We have only x86 machines, so MCU figures are cited, not measured.

## 4. Baselines

- darzi2026a: reproduce analytically 34 (ML-DSA) / 13 (FN-DSA) SIB1 fragments and the 324 B overhead.
- junquera2023assessment: reproduce 67 DSM blocks per Falcon signature and 71 per key. 666 B over 104-bit blocks gives about 52, so check the accounting against the full text.
- chen2025hybrid, junquera2023assessment: check the size tables against liboqs.
- goertzen2022post: reproduce the transfer bytes (Falcon-512 3,112; Dilithium2 8,623; SPHINCS+ 26,073) if BIND+liboqs fits in 8 GB; otherwise cite them.
- veara2025tbrd: the 68 B / 4-page TESLA layout as the symmetric reference.
- chhetri2026benchmarking: cite only (needs an RP2040).

## 5. Thin spots

- hyoung2026post [A] (PDF 403) is the closest competitor. Top priority.
- MAYO and SQIsign sizes/RAM (gringiani2023mayo, bauer2026mayo, aardal2024optimized) are [A].
- Falcon M4 cycles (pornin2025falcon, halmans2026flying) and pqm4 tables (nist2024pqm4) are [A].
- rawat2024post, sikeridis2020post, strenzke2026scaling and eaton2024provably are [A].
- Missing: any PQ broadcast-auth SoK/survey; GOOSE PQ signatures; ETSI ITS profiles; other broadcast domains (ADS-B, AIS, LoRaWAN); LMS/XMSS sizes; x86 liboqs baselines; hybrid downgrade attacks.
