# Scout A: CDN × Post-Quantum Cryptography, literature map and candidate problems

Compiled 2026-11-05 by Scout A. Verification method: each reference below was checked with web search against at least one primary or bibliographic record (publisher/DOI page, IACR ePrint, IETF archive, RFC Editor, vendor blog URL, dblp/researchr, university repository). WebFetch was blocked in this session (arxiv.org and datatracker.ietf.org did not resolve), so some arXiv and blog details come from search-index snippets rather than the full text. Those are marked **[snippet-verified]**. Anything I could not confirm is marked **UNVERIFIED** and left out of `refs_A.bib`.

Local tooling check, relevant to feasibility: the scratchpad venv's `pqcrypto` 1.0.0 provides **ML-KEM-512/768/1024, ML-DSA-44/65/87, SLH-DSA (SHA2/SHAKE, 128–256, s/f), HQC-128/192/256, Classic McEliece, sntrup**. It does **not** provide Falcon/FN-DSA. `cryptography` 50.0.2 provides X25519, Ed25519, ECDSA, RSA, HMAC and AES-GCM. System OpenSSL is 3.0.13, which has no ML-KEM, so it can't run real PQ TLS handshakes without an oqs-provider build or Go ≥1.24 in Docker. `import oqs` (liboqs-python) hung, apparently trying to fetch or build liboqs, so it should be avoided or built explicitly.

---

## 1. Literature map (53 entries: 47 verified, 6 UNVERIFIED)

### A. Foundations and standards
| # | Reference | Takeaway |
|---|---|---|
| A1 | NIST, **FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism Standard**, Aug 2024. https://doi.org/10.6028/NIST.FIPS.203 | Defines ML-KEM, the basis of every CDN hybrid key exchange deployed today. |
| A2 | NIST, **FIPS 204: Module-Lattice-Based Digital Signature Standard**, Aug 2024. https://doi.org/10.6028/NIST.FIPS.204 | Defines ML-DSA. Signatures are 2420, 3309 or 4627 B, about 38× larger than ECDSA P-256. |
| A3 | NIST, **FIPS 205: Stateless Hash-Based Digital Signature Standard**, Aug 2024. https://doi.org/10.6028/NIST.FIPS.205 | Defines SLH-DSA, a conservative hash-based option with large or slow signatures. Candidate for roots and long-lived anchors. |
| A4 | Kwiatkowski, Kampanakis, Westerbaan, Stebila, **draft-ietf-tls-ecdhe-mlkem** (Post-quantum hybrid ECDHE-MLKEM key agreement for TLS 1.3), IETF TLS WG, -05 May 2026. https://www.ietf.org/archive/id/draft-ietf-tls-ecdhe-mlkem-05.html | Specifies X25519MLKEM768, SecP256r1MLKEM768 and SecP384r1MLKEM1024. The client share is 1216 B. |
| A5 | Barnes, Iyengar, Sullivan, Rescorla, **RFC 9345: Delegated Credentials for TLS and DTLS**, July 2023. https://www.rfc-editor.org/rfc/rfc9345 | Short-lived, operator-signed credentials. This is the CDN mechanism used to deploy KEMTLS/PQ keys without CA involvement. |
| A6 | Ghedini, Vasiliev, **RFC 8879: TLS Certificate Compression**, Dec 2020. https://www.rfc-editor.org/rfc/rfc8879 | Generic compression barely helps with high-entropy PQ keys and signatures. It is the baseline for abridged certificates and MTC. |
| A7 | Kampanakis, Lepoint, **Vision Paper: Do We Need to Change Some Things? Open Questions Posed by the Upcoming Post-Quantum Migration to Existing Standards and Deployments**, SSR 2023 (Springer LNCS), doi:10.1007/978-3-031-30731-7_4 | Lists open migration questions. Several of them (resumption, caching, tokens) map onto CDN pain points. *(The SSR venue is inferred from the DOI's LNCS volume. Title, authors and DOI are verified.)* |
| A8 | Alnahawi, Müller, Oupický, Wiesmaier, **A Comprehensive Survey on Post-Quantum TLS**, IACR Communications in Cryptology 1(2), 2024, doi:10.62056/ahee0iuc | Classifies PQ-TLS approaches and runs benchmarks. Use it as the related-work backbone. |

### B. PQ TLS performance (handshake, TTLB, web)
| # | Reference | Takeaway |
|---|---|---|
| B1 | Sikeridis, Kampanakis, Devetsikiotis, **Post-Quantum Authentication in TLS 1.3: A Performance Study**, NDSS 2020. https://www.ndss-symposium.org/ndss-paper/post-quantum-authentication-in-tls-1-3-a-performance-study/ | Dilithium/Falcon are viable for TLS authentication. Chain size drives slowdowns through TCP congestion window effects. (Pre-2023 seminal work.) |
| B2 | Paquin, Stebila, Tamvada, **Benchmarking Post-Quantum Cryptography in TLS**, PQCrypto 2020, LNCS 12100, pp. 72–91 | Network emulation shows latency masks compute cost, while packet loss hurts large multi-packet handshakes. (Pre-2023 baseline.) |
| B3 | Sosnowski, Wiedner, Hauser, Steger, Schoinianakis, Gallenmüller, Carle, **The Performance of Post-Quantum TLS 1.3**, CoNEXT Companion 2023, pp. 19–27, doi:10.1145/3624354.3630585 | Hybrid key exchange adds no measurable slowdown, and PQC beats classical at high security levels. Large keys can add RTTs. |
| B4 | Kampanakis, Childs-Klein, **The impact of data-heavy, post-quantum TLS 1.3 on the Time-To-Last-Byte of real-world connections**, NDSS MADWeb 2024; IACR ePrint 2024/176. https://eprint.iacr.org/2024/176 | Time-to-last-byte (TTLB) rises less than 5% on stable high-bandwidth links. Measuring the handshake alone overstates the impact. Lossy links are worse. |
| B5 | Rios, Montenegro, Muñoz, Ferraris, **Toward the Quantum-Safe Web: Benchmarking Post-Quantum TLS**, IEEE Network 39(5):247–253, 2025, doi:10.1109/MNET.2025.3531116 | PQ-TLS compute is comparable to classical. Bytes on the wire are the binding constraint. |
| B6 | Parsom (advisor Y. Kim), **Integrating Post-Quantum Cryptography Into a CDN-Style PKI: TLS and QUIC Performance Across PQC Suites**, M.S. thesis, UNLV, Dec 2025, doi:10.34917/40245762 | The **closest CDN-specific prior work**: an emulated CDN testbed with RSA vs ML-DSA plus hybrid KEM. It finds CPU concentrated at the edge and chains "within routine CDN limits". It is a thesis, not peer-reviewed. |
| B7 | **UNVERIFIED** (title only): "Signature Placement in Post-Quantum TLS Certificate Hierarchies: An Experimental Study of ML-DSA and SLH-DSA in TLS 1.3 Authentication", arXiv:2604.06100 (2026) | Search snippets say SLH-DSA at the leaf costs about 1.4 s, while all-ML-DSA chains stay under 1 ms. Authors not confirmed, so it is not in the bib. |

### C. Certificate-size mitigation: suppression, compression, MTC, trust negotiation
| # | Reference | Takeaway |
|---|---|---|
| C1 | Sikeridis, Huntley, Ott, Devetsikiotis, **Intermediate Certificate Suppression in Post-Quantum TLS: An Approximate Membership Querying Approach**, CoNEXT 2022, doi:10.1145/3555050.3569127 | AMQ filters advertise cached intermediates, cutting intermediate-certificate bytes by about 70%. |
| C2 | Kampanakis, Kallitsis, **Faster post-quantum TLS handshakes without intermediate CA certificates**, Amazon Science, 2022. https://www.amazon.science/publications/faster-post-quantum-tls-handshakes-without-intermediate-ca-certificates | Suppressing intermediate CA certificates (ICA suppression) via cached intermediates. Venue (CSCML 2022?) **UNVERIFIED**, so the bib uses @misc. |
| C3 | Jackson, **draft-ietf-tls-cert-abridge** (Abridged Compression for WebPKI Certificates), IETF TLS WG, -02 Sep 2024. https://www.ietf.org/archive/id/draft-ietf-tls-cert-abridge-02.html | A dictionary of CCADB intermediates and roots gives about 75% reduction on today's chains, but cannot compress PQ signatures. |
| C4 | Beck, Benjamin, O'Brien, Nekritz, **draft-ietf-tls-trust-anchor-ids** (TLS Trust Anchor Identifiers), IETF TLS WG, -06 Sep 2026. https://www.ietf.org/archive/id/draft-ietf-tls-trust-anchor-ids-06.html | Lets a server choose between multiple chains, such as classical and PQ, per client. This matters for CDNs serving heterogeneous clients. |
| C5 | Benjamin, O'Brien, Westerbaan, Valenta, Valsorda, **draft-ietf-plants-merkle-tree-certs** (Merkle Tree Certificates), IETF PLANTS WG, -02 Mar 2026 (-05 exists). https://www.ietf.org/archive/id/draft-ietf-plants-merkle-tree-certs-02.html | Batch-issued certificates authenticated by inclusion proofs against landmarks clients already hold. This makes PQ authentication nearly size-neutral, but issuance is batched and delayed. |
| C6 | Valenta, Patton, Gonçalves, Westerbaan, **Keeping the Internet fast and secure: introducing Merkle Tree Certificates**, Cloudflare Blog, 28 Oct 2025. https://blog.cloudflare.com/bootstrap-mtc/ | Live Cloudflare and Chrome MTC experiment, with each MTC bootstrapped from an X.509 certificate. |
| C7 | Benjamin, **draft-ietf-tls-batch-signing** (Batch Signing for TLS), IETF TLS WG, -00 Jan 2020. https://datatracker.ietf.org/doc/html/draft-ietf-tls-batch-signing | The server signs a Merkle root over many handshake transcripts. Amortizes signing cost, which matters for key servers. |
| C8 | Fregly, Harvey, Kaliski, Sheth, **Merkle Tree Ladder Mode: Reducing the Size Impact of NIST PQC Signature Algorithms in Practice**, CT-RSA 2023, LNCS, doi:10.1007/978-3-031-30872-7_16 | Condensed signatures of a few hundred bytes over a signed "ladder". A general primitive for amortizing PQ signatures over many messages. |
| C9 | Paul, Kuzovkova, Lahr, Niederhagen, **Mixed Certificate Chains for the Transition to Post-Quantum Authentication in TLS 1.3**, AsiaCCS 2022, doi:10.1145/3488932.3497755 | Hash-based roots combined with lattice-based or ECDSA leaves are practical, which supports heterogeneous chains. (Pre-2023.) |

### D. KEM-based authentication (KEMTLS)
| # | Reference | Takeaway |
|---|---|---|
| D1 | Schwabe, Stebila, Wiggers, **Post-Quantum TLS Without Handshake Signatures**, ACM CCS 2020; ePrint 2020/534 | KEMTLS replaces handshake signatures with KEMs, using less than half the bandwidth and about 90% less server CPU. |
| D2 | Schwabe, Stebila, Wiggers, **More Efficient Post-Quantum KEMTLS with Pre-Distributed Public Keys**, ESORICS 2021; ePrint 2021/779 | KEMTLS-PDK: cached server keys cut round trips. A natural fit for CDN repeat visitors. |
| D3 | Celi, Faz-Hernández, Sullivan, Tamvada, Valenta, Wiggers, Westerbaan, Wood, **Implementing and Measuring KEMTLS**, LATINCRYPT 2021, LNCS 12912, pp. 88–107 | Go implementation of KEMTLS using delegated credentials, measured on Cloudflare-like infrastructure. |

### E. QUIC / HTTP/3
| # | Reference | Takeaway |
|---|---|---|
| E1 | Nawrocki, Fotouhi Tehrani, Hiesgen, Mücke, Schmidt, Wählisch, **On the Interplay between TLS Certificates and QUIC Performance**, CoNEXT 2022, doi:10.1145/3555050.3569123 | About 35% of certificate chains already exceed QUIC's 3× anti-amplification limit and force multi-RTT handshakes. Cloudflare accounts for 96% of amplification cases. PQ chains make this much worse. |
| E2 | Kempf, Gauder, Jaeger, Zirngibl, Carle, **A Quantum of QUIC: Dissecting Cryptography with Post-Quantum Insights**, IFIP Networking 2024, pp. 195–203; arXiv:2405.09264 | Kyber, Dilithium and Falcon add little to QUIC handshakes. SPHINCS+ adds a lot. |
| E3 | Raavi, Wuthier, Chandramouli, Zhou, Chang, **QUIC Protocol with Post-quantum Authentication**, ISC 2022, LNCS 13640, pp. 84–91 | Falcon-512 handshakes over QUIC are faster than RSA-3072. (Pre-2023.) |

### F. Industry deployment reports (CDN and browser)
| # | Reference | Takeaway |
|---|---|---|
| F1 | Cloudflare (Westerbaan et al.), **Cloudflare now uses post-quantum cryptography to talk to your origin server**, Cloudflare Blog, 29 Sep 2023. https://blog.cloudflare.com/post-quantum-to-origins/ | Edge-to-origin hybrid key exchange with Off, Supported and Preferred modes. The HelloRetryRequest (HRR) cost is the design tension. *(Individual authors are UNVERIFIED, so the bib credits the organization.)* |
| F2 | Cloudflare, **Post-quantum authentication to origins is now supported**, Cloudflare Blog / changelog 17 Jun 2026. https://blog.cloudflare.com/post-quantum-authentication-to-origins/ | ML-DSA-44/65/87 in Authenticated Origin Pulls (mTLS) and Custom Origin Trust Store. Warns about downgrade if classical certificates are still accepted. **[snippet-verified]** |
| F3 | Westerbaan, **State of the post-quantum Internet in 2025**, Cloudflare Blog, 28 Oct 2025. https://blog.cloudflare.com/pq-2025/ | Most human traffic to Cloudflare is PQ key-exchanged. Signatures are the remaining hard part. |
| F4 | Westerbaan, **Cloudflare targets 2029 for full post-quantum security**, Cloudflare Blog, 7 Apr 2026. https://blog.cloudflare.com/post-quantum-roadmap | Roadmap: PQ authentication to origins by mid-2026, users by 2027, everything by 2029. Over 65% of human traffic is PQ-encrypted. **[snippet-verified]** |
| F5 | Westerbaan, **Sizing Up Post-Quantum Signatures**, Cloudflare Blog, 8 Nov 2021. https://blog.cloudflare.com/sizing-up-post-quantum-signatures/ | Dilithium2 as a drop-in replacement gives a 60% tail slowdown, caused by about 10 KB of extra handshake bytes and congestion-window effects. (Pre-2023, but the reference point for size budgets.) |
| F6 | Cloudflare, **1.1.1.1 now supports post-quantum DNSSEC, all 2,420 bytes of it**, Cloudflare Blog, Sep 2026. https://blog.cloudflare.com/post-quantum-dnssec-1111/ | ML-DSA-44 validation (DNSSEC algorithm 18), requiring a PQ validation path to resist downgrade. **[snippet-verified]** |
| F7 | Akamai, **Akamai Enables Post-Quantum Cryptography on the Edge**, Akamai Blog, Sep 2025. https://www.akamai.com/blog/security/2025/aug/akamai-enables-post-quantum-cryptography-edge | X25519MLKEM768 client-to-edge. PQ to origin introduced 30 Jun 2025. Default-on planned for Enhanced TLS. |
| F8 | Akamai, **Future-proofing the Internet: Akamai achieves end-to-end PQC**, Akamai Blog, Aug 2026. https://www.akamai.com/blog/security/2026/aug/future-proofing-internet-akamai-achieves-end-to-end-pqc | End-to-end PQC GA on 12 Aug 2026. Edge-to-origin is opt-in. **[snippet-verified]** |
| F9 | Burgess (Fastly), **Future-Proofing TLS Encryption Against Quantum Threats**, Fastly Blog, 2025. https://www.fastly.com/blog/future-proofing-tls-encryption-against-quantum-threats | ML-KEM on by default for TLS 1.3. About 5% of TLS 1.3 clients used it at launch. Motivated by harvest-now-decrypt-later (HNDL). |
| F10 | AWS, **AWS PQ readiness – confidentiality**. https://aws.amazon.com/security/post-quantum-cryptography/aws-pq-readiness-confidentiality/ | CloudFront viewer-to-POP prefers hybrid PQ key exchange transparently. Origin side is not stated. |
| F11 | Google Security Blog (O'Brien, Benjamin et al.), **A new path for Kyber on the web**, 13 Sep 2024. https://security.googleblog.com/2024/09/a-new-path-for-kyber-on-web.html | Chrome 131 moves from Kyber (0x6399) to X25519MLKEM768 (0x11EC). *(Individual authors are UNVERIFIED, so the bib credits Google.)* |
| F12 | Cloudflare, **Cloudflare announces public certificate authority for the post-quantum web** (press release), 29 Sep 2026; covered by Help Net Security 30 Sep 2026. https://www.helpnetsecurity.com/2026/09/30/cloudflare-certificate-authority/ | A CDN becomes a CA issuing X.509 and MTCs via ACME. Production MTC issuance is planned for Q1 2027. **[snippet-verified]** |

### G. Measurement of PQ deployment
| # | Reference | Takeaway |
|---|---|---|
| G1 | Dubey, Varshney, **Measurement Study of Post-Quantum Readiness of Internet: 2026**, arXiv:2606.16473, Jun 2026 | 32,011 domains. PQ readiness varies by CDN provider. **[snippet-verified]** Novelty risk for any CDN-readiness scan. |
| G2 | **UNVERIFIED authors**: "Mind the Gap: Policy vs Reality in Post-Quantum TLS Deployment", arXiv:2607.29005, 2026 | Three rounds (Jul 2025 to Mar 2026) over about 1M endpoints from 11 vantage points. Hybrid PQ default rose from about 31% to 49% of domains. Speaker A. Shaghaghi (UNSW). Not in the bib. |
| G3 | **UNVERIFIED** (authors from snippet: Loizou, Ghadafi): "Measuring Post-Quantum TLS Deployment Across UK Internet Sectors", arXiv:2608.02147, 2026 | 44% of HTTPS services vs 6.4% of SMTP support PQ key exchange. Not in the bib. |

### H. DNSSEC and naming
| # | Reference | Takeaway |
|---|---|---|
| H1 | Goertzen, Stebila, **Post-Quantum Signatures in DNSSEC via Request-Based Fragmentation**, PQCrypto 2023, LNCS 14154, pp. 535–564 | ARRF: application-layer fragmentation of large PQ DNSSEC responses. Beats TCP fallback. |
| H2 | Lee, Hoque, Aydeger, Zeydan, **Quantum-Resistant Domain Name System: A Comprehensive System-Level Study**, arXiv:2506.19943, 2025 | System-level evaluation of PQ in DNS, DNSSEC and encrypted DNS. |
| H3 | Fregly et al., **draft-fregly-dnsop-slh-dsa-mtl-dnssec** (SLH-DSA-MTL for DNSSEC), IETF, -05 Sep 2025. https://www.ietf.org/archive/id/draft-fregly-dnsop-slh-dsa-mtl-dnssec-05.html | Applies MTL mode to make SLH-DSA DNSSEC responses fit. |

### I. Resumption, forward secrecy, CDN key sharing
| # | Reference | Takeaway |
|---|---|---|
| I1 | Springall, Durumeric, Halderman, **Measuring the Security Harm of TLS Crypto Shortcuts**, IMC 2016, pp. 33–47 | Session ticket encryption keys (STEKs) and cache state are shared across domains and PoPs (Fastly example). One stolen secret can expose tens of thousands of sites. This is the classical analogue of HNDL exposure of resumption. (Pre-2023, essential.) |
| I2 | **UNVERIFIED (not peer-reviewed)**: "HQRT" hybrid quantum-safe resumption tickets, Preprints.org 202604.0557, Apr 2026 | Claims a dedicated PQ 0-RTT resumption design is absent from the literature. Only a novelty-risk marker. |
| I3 | **UNVERIFIED (patent)**: US 12192184 / US 12732488, "Secure session resumption using post-quantum cryptography" | Industry patents on PQ resumption. Novelty risk. |
| I4 | Stebila, Sullivan, **An Analysis of TLS Handshake Proxying**, IEEE TrustCom 2015 | Formal treatment of Keyless SSL (remote private-key operations). **Not re-verified this session; drawn from memory, so treat as UNVERIFIED and leave out of the bib until checked.** |

### J. Policy and certificate lifecycle
| # | Reference | Takeaway |
|---|---|---|
| J1 | CA/Browser Forum, **Ballot SC-081v3** (reduce TLS certificate validity to 200, then 100, then 47 days by 15 Mar 2029), passed Apr 2025. https://cabforum.org/ | Shrinking validity multiplies issuance and Certificate Transparency (CT) volume. Combined with PQ sizes, this is a CDN-scale cost. **[snippet-verified via secondary sources; official ballot page not fetched]** |

Count: 53 entries (A1–J1). 47 are verified (title, authors or organization, year, venue/URL) and go in `refs_A.bib`. C2 is in the bib as @misc because its venue is unverified. 6 are UNVERIFIED and excluded from the bib: B7, G2, G3, I2, I3, I4. The pre-2023 entries (B1, B2, C1, C9, D1–D3, E1, E3, F5, I1, A6) are kept as seminal baselines; the rest are 2023–2026.

### Gaps visible across the map
1. **Almost no PQ work on CDN application-layer crypto**: signed URLs and cookies, token auth, signed manifests, HTTP Message Signatures, DRM license flows. Searches for each returned nothing. Today's CDN schemes are HMAC (Akamai), RSA (CloudFront key groups) or Ed25519 (Media CDN) per vendor docs, so the asymmetric ones are quantum-vulnerable.
2. **Edge-specific PQ authentication architecture is unstudied**: Keyless SSL/remote signing, delegated credentials, batch signing at key servers. Deployment only uses KEMTLS + delegated credentials (D3).
3. **Origin-edge PQ authentication** shipped (F2, F8) with no published analysis of amortization across tiered caches, connection pools or mTLS.
4. **Certificate lifecycle at CDN scale** (multi-tenant SAN certificates, 47-day validity, CT growth, MTC batch delay vs custom-hostname onboarding SLA) has no quantitative study.
5. **HNDL exposure of resumption chains** across anycast PoPs during the hybrid transition: classical-born tickets, STEK sharing, psk_ke vs psk_dhe_ke. Only patents and a preprint exist.

---

## 2. Candidate novel problem statements

Hard-rule reminders: every candidate below uses **real PQC microbenchmarks** (pqcrypto ML-KEM/ML-DSA/SLH-DSA plus `cryptography` for X25519/Ed25519/ECDSA/HMAC/AES-GCM) **plus simulation**. None uses Tamarin or formal verification of TLS/resumption, to stay clear of the rejected DAPV paper.

### Candidate 1: Post-quantum CDN access tokens (signed URLs and cookies) with epoch-batched Merkle authentication ("PQ-Tokens")
- **Gap.** CDN token auth (signed URLs and cookies for HLS/DASH segments and downloads) uses RSA or Ed25519 in some major CDNs and has no PQ literature. Size-amortization primitives exist only for TLS handshakes (batch signing C7), certificates (MTC C5/C6) and DNSSEC (MTL C8/H3). Nobody has fitted them to the token setting. That setting has its own constraints: a URL or cookie budget (about 4 KB per cookie, practical URL limits), very high verification rates at the edge, issuance bursts from the origin or auth service, revocation by expiry, and per-segment request fan-out (C8 and F5 give the size issue; none treats tokens).
- **Why it matters.** Raw ML-DSA-44 tokens are about 3.3 KB base64 and ML-DSA-65 about 4.4 KB, which breaks cookie limits and bloats every segment request. A forged token after a cryptographically relevant quantum computer (CRQC) exists means content theft or paywall bypass. Symmetric HMAC is PQ-safe but needs the signing key shared with every PoP, which is a key-distribution and insider risk that asymmetric schemes avoid.
- **Method sketch.** The issuer accumulates the tokens issued in an epoch (for example 1 s to 60 s) into a Merkle tree. It signs the root once with ML-DSA-65 or SLH-DSA-128s, published as an "epoch root" that edges fetch once and cache like an object. Each token carries {claims, epoch id, leaf index, authentication path} at about 32·log2(N) B. The design adds three things:
  1. An adaptive epoch length that trades issuance latency against token size and edge root-fetch rate.
  2. A hybrid mode: an HMAC fast path plus PQ-root auditability.
  3. A comparison against raw ML-DSA, SLH-DSA, HMAC with per-PoP derived keys, and Ed25519.
- **Experiments (4 CPU).** Microbenchmark sign/verify for ML-DSA-44/65/87, SLH-DSA-128s/f, Ed25519, ECDSA-P256 and HMAC-SHA256, plus SHA-256 path verification. Run a discrete-event simulation of an edge fleet with Zipf viewers, segment request streams, issuance bursts and root-cache misses. Metrics are token bytes, edge CPU per verification, p99 issuance delay, root-fetch overhead and the fraction of tokens fitting the cookie/URL budget, over epoch lengths and batch sizes. Optionally add a real HTTP prototype (Python aiohttp or Go in Docker) measuring requests per second.
- **Expected contributions.** (i) The first threat model and requirements for PQ CDN token auth. (ii) An epoch-batched Merkle token scheme with an analytic size/latency model. (iii) Measured results showing tokens 10–20× smaller than raw ML-DSA with roughly HMAC-level edge verification cost.
- **Novelty risk.** Low to medium. MTL mode (C8) and MTC (C5) are the same family of idea, applied elsewhere. Vendors may have unpublished plans. Searches for "post-quantum signed URL CDN" returned no literature.
- **Feasibility: 5/5.**

### Candidate 2: PQ certificate lifecycle at CDN scale under 47-day validity: X.509 ML-DSA vs composite vs MTC ("CertOps-PQ")
- **Gap.** MTC (C5/C6) and the Cloudflare CA (F12) aim at handshake bytes. SC-081 (J1) shortens validity. No study quantifies the **operational** cost for a multi-tenant CDN when the two are combined: CA signing load, CT log storage and bandwidth growth from PQ precertificates, ACME renewal storms, and especially **MTC batch-issuance delay vs custom-hostname onboarding SLAs** (a new hostname can't serve an MTC until its batch lands and the landmark reaches clients, so an X.509 fallback is needed). Existing work (B1–B6, C1–C4) measures per-handshake cost only.
- **Why it matters.** CDNs hold millions of hostnames. Going from 398-day to 47-day validity is about 8.5× more issuance, and PQ certificates are about 5–17 KB more each. This affects CA HSM capacity, CT logs and the onboarding UX.
- **Method sketch.** A parameterized lifecycle simulator covering hostname arrival and churn, SAN packing policy, renewal jitter, issuance mode {ECDSA, ML-DSA-44/65, composite ML-DSA+ECDSA, SLH-DSA root, MTC with batch interval B and landmark interval L}, and client mix (MTC-capable vs not, via trust-anchor-ids C4). The novel element is an **optimizer for SAN packing and batch interval** that minimizes expected bytes per handshake plus CA/CT cost, subject to an onboarding-latency SLA.
- **Experiments.** Real keygen, sign and verify costs from pqcrypto, plus real DER certificate sizes generated with `cryptography`. ML-DSA certificates need hand-built TBS bytes and a pqcrypto signature, or approximation by known field sizes. The simulation covers 10^5–10^6 hostnames over 2026–2030 policy phases. Outputs are CA CPU-hours, CT GB/year, handshake bytes, and SLA violation rate.
- **Expected contributions.** The first quantitative CDN-scale PQ certificate lifecycle model, a Pareto analysis of MTC batch intervals vs onboarding latency, and a SAN-packing policy recommendation.
- **Novelty risk.** Medium. The MTC authors (Cloudflare/Google) surely have internal numbers, and the MTC draft discusses batch sizes, but no peer-reviewed lifecycle model exists.
- **Feasibility: 4/5.** Generating ML-DSA X.509 certificates in Python takes some manual DER work.

### Candidate 3: PQ Keyless SSL: remote signing, delegated credentials, and batch signing at the key server ("KeylessPQ")
- **Gap.** Keyless SSL (I4, unverified this session) and delegated credentials (A5) are how CDNs terminate TLS without holding customer keys. PQ studies (B1–B6, D1–D3) assume the signer is co-located with TLS termination. Batch signing (C7) was proposed for RSA. Nobody has quantified PQ remote-signing trade-offs: per-handshake ML-DSA or SLH-DSA RPC vs batch signing over a Merkle tree of transcripts (which adds about 32·log N B per handshake) vs PQ delegated credentials (which add about 2.4–4.6 KB of signature plus 1.3–2.6 KB of key and extend the compromise window) vs KEMTLS-style remote decapsulation.
- **Why it matters.** Banks and regulated customers use keyless setups precisely because of compliance, and they will need PQ authentication first (F4 roadmap). SLH-DSA signing takes milliseconds to hundreds of milliseconds, so the key server becomes the bottleneck.
- **Method sketch.** Model each variant as {bytes on wire, key-server CPU, added RTT, key-compromise exposure window}. Propose **adaptive batch signing**: the key server batches pending sign requests within a Δ-ms window, and Δ is tuned against arrival rate by queueing analysis (M/G/1 with batch service). Account for QUIC's 3× amplification budget (E1).
- **Experiments.** Real sign costs (ML-DSA-44/65/87, SLH-DSA-128f/s, Ed25519, ECDSA). A discrete-event queueing simulation of the key server at 10^3–10^5 handshakes/s per customer, with RTT to the key server drawn from distributions. Measures p50/p99 handshake latency, key-server cores needed, bytes and amplification-limit violations.
- **Expected contributions.** A taxonomy and cost model for PQ delegated TLS termination, an adaptive batch-signing policy with closed-form plus simulated latency bounds, and deployment guidance on when delegated credentials beat remote signing.
- **Novelty risk.** Medium. Cloudflare may have internal data, and the batch-signing draft exists, but no published PQ evaluation was found.
- **Feasibility: 4/5.**

### Candidate 4: HNDL exposure accounting for TLS resumption lineages across anycast PoPs during hybrid rollout ("Resumption Debt")
- **Gap.** PQ key exchange is now default on many CDNs (F3, F7, F9), but resumption PSKs inherit the key-exchange strength of the **original** handshake. psk_ke resumption never refreshes it, and STEKs are shared across PoPs and domains (I1). Nobody quantifies how much traffic stays HNDL-exposed through resumption chains born from classical handshakes, or what ML-KEM psk_dhe_ke costs at the edge. Only patents (I3) and a non-peer-reviewed preprint (I2) touch this.
- **Why it matters.** The headline "50%+ of traffic is PQ" (F3) may overstate HNDL protection if classical-born tickets keep resuming.
- **Method sketch.** Define an exposure metric (bytes × remaining-secret-lifetime with classical lineage). Propose a **lineage-tagged ticket policy**: tickets record their origin key exchange group, classical-born tickets are refused or forced to hybrid psk_dhe_ke, and ticket lifetime is optimized against CPU.
- **Experiments.** Microbenchmarks for X25519, ML-KEM-768 encapsulation/decapsulation and AES-GCM ticket sealing. Trace-driven simulation of client revisit processes and PQ-capable client share growth.
- **Contribution.** An exposure metric, a policy, and cost/benefit curves.
- **Novelty risk.** Medium (patents). **DAPV caution:** the topic neighbors the rejected Tamarin PQ-resumption paper. The method here is quantitative, not formal, but reviewers or the author may see overlap.
- **Feasibility: 5/5.**

### Candidate 5: PQ authentication cost amortization on origin-edge paths in tiered caches ("Shield-PQ")
- **Gap.** Cloudflare (F2) and Akamai (F8) shipped PQ to origin, including ML-DSA mTLS, with no published analysis. Client-side TTLB studies (B4) do not model tiered caches, connection pooling, origin shields or downgrade-resistant pinning.
- **Method.** An analytic plus trace-driven model of per-request PQ overhead as a function of hit ratio per tier, pool reuse, ticket reuse and chain choice. Plus an optimizer for the placement of the "PQ-strict" tier.
- **Experiments.** Microbenchmarks plus a cache simulator over synthetic Zipf or public CDN-like traces.
- **Novelty risk.** Low to medium, but it risks being seen as incremental.
- **Feasibility: 5/5.**

### Candidate 6: QUIC amplification budget for PQ chains on multi-tenant CDN certificates
- **Gap.** E1 measured classical chains. E2/E3 measured PQ QUIC in the lab without the 3× limit or CDN SAN packing. MTC (C5), abridged certificates (C3) and suppression (C1/C2) were never compared on the round-trip count under the amplification limit for CDN-style certificates.
- **Method.** An RTT-count simulator, plus a proposal for **address-validation-token-aware chain selection**: send the full PQ chain only to validated clients and otherwise send a compact MTC/ECDSA chain via trust-anchor-ids.
- **Novelty risk: high.** The MTC and Cloudflare team covers this.
- **Feasibility: 3/5.** It needs a certificate corpus, and CT access may be blocked.

### Candidate 7: PQ DNSSEC for CDN onboarding chains (CNAME, HTTPS RR, ECH config)
- **Gap.** H1–H3 and F6 treat single zones. CDN onboarding adds CNAME chains across zones (customer to CDN) plus HTTPS/SVCB records, which multiplies RRSIGs.
- **Method.** A response-size and truncation simulator, plus a CDN-side MTL batching proposal.
- **Novelty risk: medium-high.** DNSSEC PQ is a crowded area.
- **Feasibility: 4/5.**

### Ranking
| Rank | Candidate | Novelty | Feasibility | Impact |
|---|---|---|---|---|
| 1 | C1 PQ-Tokens | high | 5 | high (clear CDN gap) |
| 2 | C2 CertOps-PQ | med-high | 4 | high (timely: SC-081, MTC, Cloudflare CA) |
| 3 | C3 KeylessPQ | medium | 4 | medium-high |
| 4 | C4 Resumption Debt | medium (DAPV-adjacent) | 5 | high |
| 5 | C5 Shield-PQ | low-med | 5 | medium |
| 6 | C7 PQ-DNSSEC-CDN | med-low | 4 | medium |
| 7 | C6 QUIC-amp | low | 3 | medium |
