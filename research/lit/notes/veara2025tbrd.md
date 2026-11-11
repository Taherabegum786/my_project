# TBRD: TESLA Authenticated UAS Broadcast Remote ID (arXiv preprint 2025)
url: https://arxiv.org/abs/2510.11343
read: full
problem: ASTM Remote ID leaves authentication unspecified, enabling spoofing, relay and replay; per-message signatures are too heavy for UAS hardware.
method: TESLA delayed-key-disclosure MAC (SHA-256 HMAC) scoped to a mission, using mobile device TEEs for bootstrapping and a verification mechanism; carried in ASTM Open Drone ID Authentication messages inside a Message Pack. Evaluated with an ESP32-S3 proof of concept and a simulated 4-drone swarm mission.
numbers: Authentication message 68 bytes (interval index + HMAC 32 bytes + disclosed key); first 17 bytes in page 0, remaining 51 bytes over further pages, 4 authentication pages total; Message Pack sent once per second; authentication payload 104 bytes. Standard limit: 255 bytes of authentication/signature data. ESP32-S3: SHA-256 HMAC 10 ms, 129 mW; ECC signature (512-bit key, 100-byte payload) 1.2 seconds, 216 mW, 139-byte signature; ESP32-S3 could not sign once per second. Abstract claims 50% less authentication overhead and 100x less computation time than signatures. Galileo TESLA uses 40-bit truncated HMAC.
limits: Symmetric TESLA, not post-quantum in itself; requires loose time sync and mission-start info; key compromise affects current mission only; no PQ signature comparison.
use-for: drones, benchmark
