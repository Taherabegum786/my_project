# A Lightweight Post-Quantum Authentication Framework for 5G Base Station Bootstrapping (arXiv 2606.30542 2026)
url: https://arxiv.org/abs/2606.30542
read: full
problem: 5G SIB broadcasts are unauthenticated (fake BS, MITM, spoofed alerts); NIST PQ signatures do not fit SIB packet limits.
method: EMULSION: TESLA-style timed, loss-tolerant HMAC chain anchored by one compact PQ signature (MAYO) per epoch; uses fixed SIB windows, GNSS/time sync, eSIM/USIM credentials. Single packet, no certificates, extends to SIB1-SIB21. Security proof; open-source; srsRAN/Open5GS/USRP B210 over-the-air testbed.
numbers: ML-DSA needs 34 SIB1 fragments, up to 5,282 ms E2E; FN-DSA 13 fragments, up to 1,920 ms. EMULSION: 160.07 ms E2E, 324 bytes crypto overhead, single SIB1 (372 B max, SIB1 every 160 ms). At 10% loss: ~41 bytes retransmission overhead vs ~1,971 bytes FN-DSA. Abstract: 33x lower delay and 31x less overhead than ML-DSA; 12x and 5.4x vs FN-DSA. MAC tags truncated to 16 bytes.
limits: Bootstrapping only; orthogonal to and does not replace 5G-AKA. Needs loose time synchronization (TESLA-style) and a long-lived MAYO public key provisioned in USIM/eSIM. Evaluated for 5G/6G BS, not grid or V2X.
use-for: framework
