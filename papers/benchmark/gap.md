# Gap: benchmark (cross-domain PQ signatures vs budget profiles)

Evidence: 31 notes. [A] = abstract-only note (weak evidence).

## 1. Landscape

| Approach | Keys | Achieves | Leaves open |
|---|---|---|---|
| Single-domain size fit | junquera2023assessment, chen2025hybrid, abrar2026deployment, twardokus2024when | Which NIST signatures fit one budget | No common method across domains |
| Single-domain reviews / multi-algorithm | mamun2026post, yoshizawa2026a, nabasirye2026security [A] | ITS review (13 gaps); ZK-proof compression of V2X sigs, 40-95% smaller; GOOSE benchmark rig | ITS-only or grid-only |
| PQ sig anchoring HMAC chain | darzi2026a | 324 B, one SIB1 vs 13-34 fragments | 5G SIB only; time sync |
| Symmetric broadcast auth | veara2025tbrd, hussain2026a | 68 B Remote ID auth; fast SV MAC | No PQ signature comparison |
| Fragmentation / multi-frame | goertzen2022post, rawat2024post [A], wiethuechter2024drip | PQ sigs over 1232 B DNS; FEC over 25 B frames | Request-response or classical-only |
| Few-time hash-based | sedghighadikolaei2024fast, sedghighadikolaei2024signer | Fast sign/verify | Stateful, finite capacity |
| MCU benchmarks | chhetri2026benchmarking, gringiani2023mayo [A], bauer2026mayo [A], aardal2024optimized [A], pornin2025falcon [A], halmans2026flying [A], nist2024pqm4 [A] | Cycles, RAM, tails | Not mapped to message budgets |
| Hybrid design / SoK | bindel2026hybrid, fall2025sok [A], devevey2025compact [A] | Hybrid property vocabulary; TLS/QUIC hybrid SoK; compact non-separable hybrid | No broadcast budgets; single signer/verifier |
| Handshake feasibility envelopes | hyoung2026post [A], sikeridis2020post [A] | Algorithms mapped to channel conditions | Handshake, not broadcast |

## 2. Gap

The six new notes do not overturn the gap, but they narrow it. None compares PQ signatures across more than one broadcast domain. mamun2026post and yoshizawa2026a are explicitly ITS/V2X-only. nabasirye2026security [A] is grid-only. fall2025sok [A] is about hybrids in TLS/QUIC. Multi-algorithm comparison inside one domain is now taken: yoshizawa2026a covers NIST and additional-round candidates for V2X CAMs, and mamun2026post reviews ITS. So the novelty must rest on scoring one set of modes against several handshake-free profiles, not on breadth of algorithms. The modes are full signature, fragmented, PQ-anchored chain (darzi2026a), hybrid (bindel2026hybrid) and ZK compression (yoshizawa2026a). The nearest work is still hyoung2026post [A], which builds a size-latency envelope but for a ROS2/DDS handshake. A broader broadcast SoK cannot be excluded, because fall2025sok was read as abstract only.

## 3. Questions

1. Which (scheme, mode) pairs fit each profile? Profiles: C-V2X 437 B (twardokus2024when), Remote ID 25 B frames / 255 B auth (wiethuechter2024drip), OSNMA 16 DSM blocks (junquera2023assessment), SIB1 372 B (darzi2026a), DNS 1232 B (goertzen2022post). Metric: auth bytes per message, share of budget, frames per message.
2. At 0-30% loss, does a PQ-anchored chain beat fragmented signatures? Metrics: expected bytes per verified message, p95 time-to-authenticate, share of messages verified (darzi2026a gives a 10% point).
3. Is size or the timing tail binding? Metric: deadline-miss rate from p99 sign/verify against 3 ms (hussain2026a, nabasirye2026security [A]) and 100 ms (chen2026pseudonym, mamun2026post). Tail data comes from chhetri2026benchmarking. MCU figures are cited, not measured (x86 only).

## 4. Baselines

- darzi2026a: reproduce 34 / 13 SIB1 fragments (ML-DSA / FN-DSA) and the 324 B overhead.
- junquera2023assessment: reproduce 67 / 71 DSM blocks (Falcon signature / key). 666 B over 104-bit blocks gives about 52, so check against the full text.
- yoshizawa2026a: reproduce size reduction per algorithm (liboqs+Bulletproofs, i7 16 GB machine).
- chen2025hybrid, junquera2023assessment: check size tables against liboqs.
- goertzen2022post: reproduce transfer bytes if BIND+liboqs fits in 8 GB; otherwise cite.
- veara2025tbrd: 68 B / 4-page TESLA reference.
- chhetri2026benchmarking: cite only (RP2040).

## 5. Thin spots

- hyoung2026post [A] (closest competitor) and fall2025sok [A] (possible overlapping SoK): need full text.
- nabasirye2026security [A]: no GOOSE numbers.
- devevey2025compact [A]: no Silithium sizes.
- MAYO/SQIsign (gringiani2023mayo, bauer2026mayo, aardal2024optimized) and Falcon M4/pqm4 (pornin2025falcon, halmans2026flying, nist2024pqm4) are [A].
- Missing: ETSI ITS profiles; ADS-B/AIS/LoRaWAN; LMS/XMSS sizes; x86 liboqs baselines; hybrid downgrade in broadcast.
