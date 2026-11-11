# Post-Quantum Cryptography for Intelligent Transportation Systems: An Implementation-Focused Review (arXiv 2026)
url: https://arxiv.org/abs/2601.01068
read: full
problem: Readiness of vehicular communication and security standards for PQC; implementation constraints in in-vehicle networks, V2X, and embedded hardware (side-channel/fault attacks).
method: Literature review of ITS PQC work; identifies research gaps and a phased migration roadmap.
numbers: thirteen research gaps (RG1-RG13); 18 studies classified under D2 (Vehicular Standards); BSM 10 Hz, 100 ms authentication budget; cited result (ref [130], Jetson AGX Xavier OBU): 3.9 ms ECDSA-P256 vs 12.7 ms Falcon (Level 1) over 300 WAVE payloads; cited ~35-40% payload growth estimate; cited hybrid handshake result up to 73.2% faster at 5% packet loss (V2C).
limits: Secondary review, no new measurements. Does NOT compare PQ signatures across more than one broadcast domain: scope is ITS only (in-vehicle, V2X, V2C), no drone or grid broadcast. Does NOT cover handshake-free broadcast as a distinct topic; broadcast authentication (BSM) is discussed only within V2X alongside handshake-based V2C sessions, and mostly via hybrid ECDSA+PQC.
use-for: v2x
