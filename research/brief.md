# Research brief (fixed decisions — do not re-derive)

**Thesis:** A post-quantum (PQ) broadcast authentication technology for systems where each
message has a tight size/latency budget, receivers have no prior relationship with the
sender, and there is no handshake. Vehicles (V2X) are the first application, not the only one.

**Core idea:** each target system is a *budget profile* (bytes per message, latency deadline,
message rate, loss rate, privacy requirement). The technology offers authentication modes
(full PQ signature + certificate; fragmented certificate; periodic PQ signature anchoring a
hash chain; classical+PQ hybrid) and selects/tunes one per profile.

**Papers (one directory each under `papers/`):**
| id | Paper | Distinct problem |
|---|---|---|
| benchmark | Cross-domain benchmark / systematisation | PQ signatures vs budget profiles |
| v2x | Vehicles | size budget at 10 msg/s; baseline: Twardokus et al., NDSS 2024 |
| drones | Drone Remote ID | frames smaller than any PQ signature |
| grid | Substation GOOSE (optional) | 3-4 ms deadline; speed, not size |
| framework | General framework + formal model (last) | the above as instances of one scheme |

Order: benchmark -> v2x -> drones -> (grid) -> framework. Each paper needs domain-specific
novelty; reuse code, never text.

**Resources:** CS background, no lab. Three CPU-only PCs (i7/16 GB, Ryzen 7/8 GB, Ubuntu
i5/8 GB). Everything must run in software: liboqs, ns-3 or OMNeT++/Veins/SUMO, Tamarin,
libiec61850. Keep experiments within 8 GB RAM, or flag that the 16 GB machine is needed.

**Research questions:**
1. Minimum per-message overhead for PQ broadcast authentication at a given deadline/loss rate?
2. Can one parameterised design cover size-, latency- and privacy-bound domains?
3. Is it secure through the hybrid transition (downgrade attacks)?
4. Can pseudonym privacy be kept at practical cost with PQ credentials?
