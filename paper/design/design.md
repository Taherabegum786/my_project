# Design: EMBER, post-quantum CDN access tokens with epoch-Merkle batching

**EMBER** = **E**poch-**M**erkle **B**atched, **E**dge-verifiable, **R**oot-signed tokens.

Designer agent, 2026-11-05. Inputs: `BRIEF.md`, `scout/scout_A.md`, `scout/refs_A.bib`, `scout/prior_work.md`. `scout/feasibility.md` did not exist when I finished; the anchors I measured are recorded in §6.0.

Status markers: **[V]** means I verified it with web search this session (title/venue/URL seen). **[bib]** means it is already in `refs_A.bib`. **[TODO-verify]** means the Writer must verify it before citing.

---

## 1. Novelty check

### 1.1 Searches run on 2026-11-05 (9 queries)

| # | Query (abridged) | What exists |
|---|---|---|
| Q1 | post-quantum signed URL CDN token ML-DSA Merkle | **Nothing on PQ CDN signed URLs or cookies.** Only hits: an ML-DSA token SDK on PyPI (vendor, no CDN, no batching) and the Verisign *ML-DSA-MTL for DNSSEC* draft (draft-kaizer-dnsop-ml-dsa-mtl-dnssec). |
| Q2 | JOSE/COSE ML-DSA JWT | **RFC 9964, "ML-DSA for JOSE and COSE", May 2026 [V]**. It defines ML-DSA-44/65/87 JWS/COSE algorithms, notes that base64url makes signatures even larger, and warns ML-DSA "might not be the best choice" where small signatures are required. It has no batching and nothing on tokens or size. |
| Q3 | Merkle batch signing JWT tokens | **Aguilar-Melchor, Albrecht, Bailleux, Bindel, Howe, Hülsing, Joseph, Manzano, "Batch Signatures, Revisited", CT-RSA 2024, LNCS 14643, pp. 163–186, doi:10.1007/978-3-031-58868-6_7 (ePrint 2023/492) [V]**. It formalizes Merkle batch signatures with EUF-CMA and privacy proofs, but in its model every signature carries the root signature and it is evaluated on TLS. Also found: draft-joseph-tls-batch-signatures-00 (2023, expired) [V]. |
| Q4 | MTL mode | **draft-harvey-cfrg-mtl-mode-08/-09 (Verisign; -09 Mar 2026) [V]**. MTL signs "ladders" over a growing message series, and messages are authenticated by a path to a rung. The draft says it is most useful when verifiers check a subset of a large evolving series. Its CT-RSA 2023 paper is Fregly et al. [bib]. DNSSEC profiles: SLH-DSA-MTL [bib] and ML-DSA-MTL [V]. |
| Q5 | Media CDN / CloudFront signed URL algorithms | Google Media CDN signs URLs and cookies with **Ed25519** [V, cloud.google.com/media-cdn/docs/generate-signatures]. AWS CloudFront key groups accept **RSA-2048 and ECDSA-256** public keys [V, AWS API reference PublicKeyConfig]. Akamai Token Auth (EdgeAuth) is **HMAC** per Scout A [TODO-verify vendor doc]. No vendor announces a PQ signed-URL option. |
| Q6 | draft-burls-mtac (Merkle Tree Agent Certificates) | **draft-burls-mtac-00, Jul 2026 (individual, Aelethion) [V]**. It batches AI-agent identity credentials under an ML-DSA-65 signed tree head (RFC 9162 tree) with logarithmic inclusion proofs. It explicitly claims no novelty in Merkle trees and **specifies no runtime authorization**. It is the closest token-like credential work, but it is identity, not CDN access control, and it has no epoch control, edge cache or size budget. |
| Q7 | Privacy Pass PQ | Policharla, Westerbaan, Faz-Hernández, Wood, PQ Privacy Pass via zkDilithium (ePrint 2023/414) [V]: 85–175 KB tokens, anonymity-focused. Chu, Do, Hanzlik, rate-limited Privacy Pass (ePrint 2023/1805) [V]. These address a different problem (unlinkable anonymous tokens) and are orders of magnitude larger. |
| Q8 | PQ access tokens / OAuth / JWT Merkle batch | MAGIQ (arXiv 2605.06933) [V title]: PQ multi-agent AI governance, UC proofs, not CDN. draft-coetzee-oauth-spt-txn-tokens is a lead only [unverified, do not cite]. |
| Q9 | Batch Signatures Revisited bibliographic check | Confirmed CT-RSA 2024 (see Q3). |

Already in `refs_A.bib`: MTC (draft-ietf-plants-merkle-tree-certs; Cloudflare blog), TLS batch signing (draft-ietf-tls-batch-signing), MTL CT-RSA 2023, SLH-DSA-MTL DNSSEC.

### 1.2 What exists vs. our delta

The core primitive is **not new**: sign one Merkle root, give each message an authentication path. Batch signatures (CT-RSA'24), MTL mode, MTC and MTAC all do this. We say so plainly in the paper. **We found no publication or draft that applies it to CDN access tokens** (signed URLs, signed cookies, token auth). We also found no publication that addresses the constraints specific to that setting:

| Aspect | Batch sig (CT-RSA'24) | MTL mode | MTC / MTAC | **EMBER (this work)** |
|---|---|---|---|---|
| Signature/root carried per message | yes (full root sig each time) | condensed + separately fetched ladder | landmark/tree head pre-distributed | **path only; signed epoch root disseminated through the CDN itself (push / pull-on-miss / stapled)** |
| Verifier population | one TLS client | DNS resolvers | browsers / RPs | **thousands of edges, sticky sessions, request fan-out (100s of segment requests per token)** |
| Hard size budget | none | DNS UDP | TLS flight | **URL (RFC 9110: ≥8000 octets recommended; ~2 KB legacy practice), cookie (RFC 6265: ≥4096 B per cookie)** |
| Batch-window control | fixed | n/a (growing series) | fixed batch interval, hours | **adaptive Δ chosen by a single-unit delay model (issuance wait vs. edge root-miss RTT) per tenant, under diurnal and heavy-tailed multi-tenant load** |
| Old-root handling | n/a | ladder rungs | landmarks | **two-timescale epoch/period roll-up: one signature per period over all epoch roots** |
| Validity / revocation | n/a | n/a | cert lifetime | **epoch-bounded validity (Expires ≤ T_epoch + V_max), which also bounds the forgery window; per-(epoch, index) revocation** |
| Evaluation | TLS handshakes | DNSSEC sizes | handshake bytes | **CDN fleet simulation + measured crypto: % fitting URL/cookie, edge CPU, issuance latency, root bandwidth, root-miss latency** |

**Exact-idea check.** Neither MTAC nor any other work in our searches applies Merkle batching to CDN signed URLs or cookies. If the Writer finds such a paper during final verification, the fallback is the closest unexploited variant: keep the batching primitive as background and make the **adaptive dissemination/epoch control under multi-tenant CDN load** (C3–C4 below) the headline contribution. That part was absent from everything we found.

**Claimed contributions (paper)** (revised by the Critic: see the changes log, D1). C2 is explicitly a *profile* of Merkle batch signatures (CT-RSA'24) and MTL mode, not a new primitive. The headline contributions are the CDN-systems ones (C3, C4, C6) and the head-to-head with the *strong* baselines (B10–B15).
- **C1.** A threat model and requirement set for PQ CDN access tokens (do not claim "first"). It is honest about HMAC (already PQ-secure) and argues that the case for asymmetric tokens rests on trust distribution, not on quantum hardness.
- **C2.** EMBER, a token format and protocol: tweak-domain-separated Merkle tree with issuer-salted leaves; one ML-DSA / SLH-DSA (optionally hybrid Ed25519+ML-DSA) signature per epoch; epoch-bounded validity; revocation. Includes a **proof sketch** reducing token unforgeability to EUF-CMA of the root signer plus (second-preimage-type) security of the tweakable hash, and a **truncated-node analysis** (n = 16 B vs 32 B).
- **C3.** Root dissemination for a CDN fleet: push, pull-on-miss with request coalescing, **root stapling** on the first request, and **two-timescale period roll-up**, with closed-form bandwidth and miss models.
- **C4.** An **adaptive epoch controller** that minimises user-visible added delay in a single unit (seconds): issuance wait + expected root-miss RTT. It is subject to hard constraints on token size and signer capacity, uses no arbitrary weights, and runs per tenant.
- **C5.** Measured microbenchmarks. The primary numbers are native: OpenSSL 3.5.4 C/EVP built in the scratchpad, and Go/circl. Python pqcrypto is secondary and labelled. Wire bytes per session are measured with a real HPACK encoder. The comparison covers 15 baselines, including the strong ones: multi-MAC, delegated short-lived Ed25519 keys, KEM-wrapped epoch MAC keys, ML-DSA with a verified-token cache, multi-cookie ML-DSA, and MTL mode.
- **C6.** A **real Go prototype** (edge verifier, issuer + root service, open-loop load generator) in separate network namespaces joined by the userspace link emulator `tapbridge` (netem is unavailable). It measures edge req/s per core, added latency under load, and real root-miss behaviour. The fleet simulator is **validated against this prototype**, not only against a second simulator (E8).

---

## 2. Problem statement and motivation (honest version)

**CDN access tokens.** An origin or auth service (the *issuer*) authorises a client to fetch protected cached content (paywalled video, HLS/DASH segments, software downloads) by handing it a token. The token is carried in a query string (signed URL), a cookie (signed cookie), or a header. Any edge PoP verifies it before serving from cache, without contacting the origin. Current mechanisms:
- **HMAC** with a key shared with every edge (Akamai-style token auth).
- **RSA-2048 / ECDSA-P256** (CloudFront key groups [V]).
- **Ed25519** (Google Media CDN [V]).

**Why HMAC is not enough, even though it is PQ-secure.** We must not overclaim that "HMAC is quantum-broken". HMAC-SHA256 is fine against quantum adversaries. Its problems are about trust distribution:
1. **Key exposure surface.** The minting key sits on every edge, often thousands of machines in hundreds of PoPs, possibly third-party or partner hardware. Compromising one edge (memory disclosure, insider, misconfiguration) lets the attacker mint unlimited tokens for every edge and every path that key covers. With signatures, compromising an edge yields only public keys.
2. **Multi-CDN and third-party verifiers.** Content owners increasingly use several CDNs. HMAC means sharing the minting secret with every vendor, each of which can mint tokens valid on the others. With public-key tokens, each CDN gets only the public key.
3. **Accountability.** With HMAC any verifier could have minted a token, so there is no evidence of who issued it. Signatures provide issuer accountability for audit and disputes.
4. **Delegation.** A public-key issuer can delegate scoped issuing rights (a separate key per tenant or product) without re-keying edges. This is out of scope for evaluation and is mentioned only.
**Caveat on point 1 (Critic, D5).** A compromised edge can already serve anything it caches without checking any token. Asymmetric tokens only remove *lateral* minting: tokens usable at other edges, other CDNs, or for other tenants and paths. The benefit is therefore a smaller blast radius, quantified in Table V, not "edge compromise is harmless".
Some vendors offer public-key token options (CloudFront, Media CDN); we do not speculate about their motives. Those deployments use RSA/ECDSA/Ed25519 and are therefore quantum-vulnerable.

**Why PQ, and why now.** Authentication has **no harvest-now-decrypt-later (HNDL) problem**, and the paper must state this (lesson 8 from the prior rejection). Short-lived tokens issued today cannot be forged retroactively in any useful way. The real risks are:
- (a) Once a CRQC exists, an attacker recovers the long-lived issuer private key from the **public** key (Shor) and mints arbitrary tokens. Public keys are configured in CDN dashboards and edge configs for years.
- (b) Migration lead time. Configuration formats, SDKs, edge verifiers and URL/cookie size assumptions must change before that day. Industry roadmaps target PQ authentication by about 2029 (Cloudflare roadmap [bib cf2026roadmap]), and NSA CNSA 2.0 lists transition deadlines [TODO-verify exact dates and wording before citing].
- (c) Compliance pressure.
So the motivation is "readiness before a CRQC, under hard size constraints", not urgency from HNDL.

**Why naive PQ fails** (to be measured, §6). ML-DSA-44 signatures are 2420 B, which becomes 3227 B in base64url. ML-DSA-65 is 3309 B (4412 B b64), SLH-DSA-128s is 7856 B (10475 B b64), and SLH-DSA-128f is 17088 B (22784 B b64). Adding claims:
- ML-DSA-44 tokens exceed 2 KB URL practice and come close to a 4 KB cookie.
- ML-DSA-65 tokens exceed the cookie limit.
- SLH-DSA tokens exceed everything except large headers.
Every segment request also carries the token (header bloat over hundreds of requests per session), and per-request ML-DSA verification costs about 10²× an HMAC at the edge.

**Problem.** Design a public-key, PQ-secure CDN token scheme that:
- (R1) fits URL and cookie budgets with margin;
- (R2) has per-request edge verification cost close to HMAC;
- (R3) does not need the minting secret at edges;
- (R4) has bounded issuance latency;
- (R5) supports revocation;
- (R6) adds negligible fleet-wide bandwidth and keeps root-miss latency rare;
- (R7) has a clear security reduction.

---

## 3. System and threat model

**Entities.**
- **Issuer I.** The tenant's auth service, or a CDN-hosted issuer-as-a-service. It holds the signing key sk (ML-DSA-44/65, SLH-DSA-128s/f, or hybrid Ed25519‖ML-DSA-44), and may be sharded over k signer cores.
- **Root service.** A publication endpoint for signed epoch roots and period bundles. It is itself a cacheable origin object, fetched through the CDN tier hierarchy.
- **Edges E₁..E_E.** They hold pk (configured), a root cache, and optionally a revocation bitmap. A tier (shield) layer sits between edges and the root service.
- **Client.** It obtains a token from I after authentication (paywall, session), then makes requests carrying the token: one manifest plus many segments, sticky to one edge with high probability.

**Adversary 𝒜 capabilities.**
1. Full network control between clients and edges for observation and replay of observed tokens. Bearer-token theft is **out of scope** beyond the status quo (IP/ASN binding claims, short validity), and we state this.
2. **Compromise of any subset of edges and shields**: all their state (pk, cached roots, revocation lists) and the ability to inject roots into their own caches.
3. Chosen-claims issuance oracle: 𝒜 can be a legitimate client of any tenant and obtain arbitrarily many tokens for claims of its choice. Leaf salts stay issuer-chosen.
4. **Quantum adversary**: may run Shor against any public key, and Grover/BHT against hash functions within its time budget.
5. 𝒜 does **not** compromise the issuer's sk. Issuer compromise is handled by key rotation and kid, and is out of the security game.

**Security goals.**
- **G1 Unforgeability.** No PPT/QPT 𝒜 can make an honest edge accept claims c* that I never issued (or that were revoked), even with all edges compromised.
- **G2 Edge non-minting.** Compromising an edge gives no minting capability (structurally true: edges hold no secret).
- **G3 Bounded validity.** An edge rejects any token whose Expires exceeds T_epoch + V_max, even if the claims are authentic.
- **G4 Sibling privacy.** An authentication path reveals nothing about other clients' claims (hiding via 128-bit salts).
- **G5 Availability.** An edge that cannot get a root fails closed by default. The policy knob is discussed, not evaluated as secure.

**Additional threats the analysis must cover (Critic, D7/D8):**
- **Replay classes.**
  - Same-edge and cross-edge replay of a stolen bearer token: as in the status quo.
  - Cross-epoch replay: prevented by the epoch in the tweak; tested.
  - Cross-tenant replay in pooled trees: prevented by Tenant in the claims and the tenant id in the leaf tweak; tested.
  - Cross-kid replay: tested.
- **Binding options.** IP/ASN claims. An optional DPoP-style `cnf` = H(client public key) claim (+32 B; costs one client signature per request, so it is discussed, not evaluated). TLS-exporter binding is future work.
- **Clock skew.** Edges apply a tolerance τ_skew (default 5 s) to both the Expires and the T_start + Δ + V_max checks. There is a test with a ±τ_skew clock.
- **Volume privacy.** N_e in the public root leaks per-tenant issuance volume. Mitigations: pad-to-2^d or bucketed N, dummy leaves, pooling, and stapling/push-only distribution.
- **Linkability.** (e, i) is a per-token identifier visible on every request. This is the same as a per-token signature in the status quo, but say so.
- **Side channel.** Root-fetch timing at an edge reveals whether a token for (tenant, e) was recently used there (cache probing). The impact is low; mitigations are push or stapling.
- **Pooling changes the trust model.** One CDN-held key mints for all pooled tenants. Pooling is only valid when the tenant already delegates issuance to the CDN (D6).

Non-goals: client anonymity or unlinkability (Privacy Pass solves that at 85+ KB, ePrint 2023/414); confidentiality of claims; issuer-key compromise recovery beyond rotation.

---

## 4. The method: EMBER

### 4.1 Primitives and notation
- Hash: SHA-256 (default) or SHAKE256, output truncated to **n bytes**, n ∈ {16, 32}.
- **Tweakable hash** Th(T, x) = trunc_n(SHA-256(T ‖ x)), where the tweak T is fixed-length:
  `T = ctx(8B "EMBERv1\0") ‖ kid(4) ‖ epoch(4) ‖ type(1) ‖ level(1) ‖ index(4)`.
  `type` ∈ {LEAF, NODE, ROOT, PERIOD}. This follows the SPHINCS+ / SLH-DSA address-based domain-separation idea, so every node position in every epoch is a distinct hash instance and multi-target attacks do not apply.
- **Leaf:** L_i = Th(T_leaf(e,i), r_i ‖ enc(c_i)), where r_i ← {0,1}^128 is issuer-chosen and returned inside the token, and c_i is the canonical claims encoding.
- **Node:** N = Th(T_node(e, ℓ, j), left ‖ right). Trees are RFC 9162-style, unbalanced when N is not a power of two (path length ⌈log₂N⌉ or ⌊log₂N⌋). An optional pad-to-2^d mode hides the batch size.
- **Signed epoch root** SR_e = (kid, e, T_start(e), Δ_e, N_e, R_e, σ_e), where σ_e = Sign(sk, "EMBER-root" ‖ kid ‖ e ‖ T_start ‖ Δ_e ‖ N_e ‖ R_e). Uses the FIPS 204/205 context string "EMBER-root".
- **Hybrid option:** σ_e = σ_Ed25519 ‖ σ_ML-DSA-44, both over the same message, and both must verify. Because it is amortised per epoch, the classical half adds nothing per token. This is a contribution worth stating.

### 4.2 Token format (wire)
Media-CDN-like textual claims plus one base64url blob:

```
<claims>:E=<b64url( ver(1) | alg(1) | kid(4) | epoch(4) | idx(4) | r(16) | path(n*d) )>
claims = URLPrefix=<b64url(prefix)>:Expires=<unix>:Tenant=<id>[:IP=<cidr>]
```

Raw blob = 30 + n·d bytes. Encoded = ⌈4(30+n·d)/3⌉ (no padding).
- Example with n = 16, d = 14 (N ≈ 10⁴): 254 B raw, **339 B encoded**.
- Same tree with n = 32: 478 B raw, 638 B encoded.

### 4.3 Algorithms (pseudocode)

```
Issue(c):                         # called by client-facing API; enqueues
  r ← rand(16); req ← (c, r, future); Q_open.append(req); return await future

CloseEpoch():                     # triggered by controller (timer / count / signer-free)
  B ← Q_open; Q_open ← []; e ← next_epoch_id(); N ← |B|
  leaves ← [Th(T_leaf(e,i), B[i].r ‖ enc(B[i].c)) for i in 0..N-1]
  (R, levels) ← BuildTree(e, leaves)                  # 2N-1 hashes total
  σ ← Sign(sk, "EMBER-root" ‖ kid ‖ e ‖ T_start ‖ Δ ‖ N ‖ R)
  PublishRoot(SR_e = (kid,e,T_start,Δ,N,R,σ))
  for i: B[i].future.set( Token(B[i].c, kid, e, i, B[i].r, AuthPath(levels,i)) )

PublishRoot(SR_e):
  store SR_e at root service under immutable key /ember/<kid>/<e>  (Cache-Control: immutable, max-age=V_max+P)
  if mode ∈ {PUSH, PUSH+ROLLUP}: fan out SR_e to edges (via tier tree)
  append R_e to current period list; if period p closes (every m epochs):
     PB_p = (kid, p, e_first, m, [R_e...], σ_p = Sign(sk, "EMBER-period" ‖ kid ‖ p ‖ e_first ‖ m ‖ MTH([R_e...])))
     publish PB_p at /ember/<kid>/period/<p>

Verify_edge(token, now):          # per request
  parse claims c, blob → (kid,e,i,r,path); reject on malformed / unknown kid
  if now > c.Expires or c.Expires > T_start(e) + Δ_e + V_max: reject      # epoch-bounded validity
  if c.URLPrefix not prefix of request URL (and IP binding fails): reject
  if Revoked(e,i): reject
  R ← RootCache.get(kid,e)
  if R = ⊥:
     if stapled header X-EMBER-Root present: SR ← parse; verify σ; RootCache.put; R ← SR.R
     elif e in closed period p and PB_p fetchable: fetch PB_p (coalesced); verify σ_p over MTH; insert all m epoch roots
     else: fetch SR_e (coalesced, via tier); verify σ_e; insert
     on timeout: fail closed (503/403 per policy)
  x ← Th(T_leaf(e,i), r ‖ enc(c)); for ℓ, sib in path: x ← Th(T_node(e,ℓ,⌊i/2^{ℓ+1}⌋), order(x,sib,i,ℓ))
  accept iff x = R   (constant-time compare)
```

**Root stapling (optional).** The issuer API also returns SR_e. The client sends it once, in header `X-EMBER-Root`, on its first request to an edge (a one-time 2.4–3.3 KB header, outside URL/cookie budgets). The edge verifies it and caches the root. This removes the pull RTT on cold edges. The idea is analogous to OCSP stapling and MTL "full vs condensed" signatures, and we cite MTL.

**Period roll-up (two timescales).** Each epoch root is signed individually for fast availability. Every m epochs (period P = mΔ) the issuer also signs one bundle containing all m epoch roots: m·n + |σ| bytes, e.g. m = 300, n = 16 gives 4.8 KB + 2.4 KB. An edge that misses on any epoch in a closed period fetches one bundle and learns all m roots with one signature verification. Tokens are **unchanged**, so there are no token upgrades. The roll-up reduces cold-edge misses and pull bandwidth for sparse-traffic edges and tenants by up to a factor m, and it bounds edge root-cache state to V_max/P bundles.

**Revocation.**
1. Short V_max (default 1 h; sweep 5 min–24 h).
2. Per-token revocation: the issuer publishes a signed delta {(e, i)} (bitmap per epoch, or a sorted list) that edges pull with the period bundle. Edges check a hash set, O(1).
3. Whole-epoch revocation (kill R_e), e.g. after an issuer bug.
4. Key rotation via kid.
Compared with HMAC, revocation is no worse. Compared with per-token signatures, it is identical in expressiveness, but (e, i) gives a compact revocation identifier (8 B).

### 4.4 Adaptive epoch controller (contribution C4)

Every tenant/issuer shard τ maintains an EWMA estimate λ̂_τ of the issuance rate. The controller also uses an edge-traffic share vector ŵ (from edge root-miss telemetry, or geo priors). At each epoch close it chooses the next Δ ∈ grid G = {Δ_min, …, Δ_max} (log-spaced) as follows.

**Objective, in a single physical unit (seconds of user-visible added delay per token/session):**

D(Δ) = W_issue(Δ) + M(Δ) · F_miss

- **W_issue(Δ) = Δ/2 + t_build(λΔ) + t_sign + t_pub.** This is the mean wait for Poisson arrivals in timer mode; the p99 is ≈ 0.99Δ + t_build + t_sign.
- **M(Δ) = expected root misses per token** (first request of a session at an edge with no root for its epoch). For pull-only with per-epoch roots and Poisson tokens spread over edges by w:
  M(Δ) = (1/(λΔ)) · Σ_e [1 − exp(−λΔ w_e)]. For uniform w with λΔ ≫ E, M ≈ E/(λΔ) → 0. With λΔ ≪ E, M → 1 (every token misses).
  The model ignores time-ordering effects (the first-arriving token pays the miss), which the simulator captures exactly.
- **F_miss = expected miss penalty:** fetch RTT to the root service via tier (pull), or 0 with stapling (then the cost is bytes, reported separately), plus t_verify(σ).
- With roll-up, misses on closed periods use M_P computed with λP in place of λΔ.

**Hard constraints (no weights):**
- (i) Size: ⌈log₂(λΔ)⌉ ≤ d_max(B) = ⌊(3B/4 − 30 − c_enc)/n⌋. B is the token budget, e.g. 1024 B so that URL + claims ≤ 2 KB. Enforced by a count trigger N_max = 2^{d_max}: the epoch closes early when N reaches it.
- (ii) Signer capacity: t_build(λΔ) + t_sign ≤ k·Δ. This matters for SLH-DSA-128s with t_sign ≈ 0.3 s on this machine (measured in pqcrypto; to be re-measured).
- (iii) Latency SLO: p99 W_issue ≤ L_SLO.
- (iv) Optional push-bandwidth cap: E·|SR|/Δ ≤ BW_max.

Policy:

```
Controller.step():
  λ̂ ← EWMA(arrivals); feasible ← {Δ∈G : (i)-(iv) hold}
  if feasible = ∅: Δ ← Δ_min; raise alarm (shard tenant: k←k+1)
  else Δ ← argmin_{Δ∈feasible} D̂(Δ)       # D̂ uses λ̂, ŵ, measured t_sign, t_h, F̂_miss
  arm timer Δ; count trigger N_max
```

**Insight (to be tested).** In pull mode the optimum is interior. Approximately, dW/dΔ = 1/2 balances −dM/dΔ·F_miss. So high-rate tenants get small Δ (milliseconds to ~1 s), while the long tail of low-rate tenants gets larger Δ or benefits from **pooling tenants into one shared tree** (CDN issuer-as-a-service). Pooling raises λ without changing size by more than ⌈log₂ pool⌉. With push or stapling, F_miss → 0 and the optimum is Δ_min subject to (ii)/(iv). The paper reports which regime real parameters fall into rather than assuming one.

**Work-conserving variant (WC).** The epoch closes as soon as the signer is idle and ≥1 request is pending, so effectively Δ ≈ t_build + t_sign. Included as a baseline policy (it minimises W_issue but maximises root count).

### 4.5 Analytical cost model (validated against measurements and the simulator)

Symbols: n node bytes, d = ⌈log₂N⌉, N = λΔ, t_h one tweakable-hash call (measured, ~64–100 B input), t_s / t_v root sign/verify (measured), c_enc encoded claims bytes, E edges, Q_e request rate at edge e, ρ_e distinct-roots-needed rate at edge e.

| Quantity | Formula |
|---|---|
| Token size (encoded) | S_tok = c_enc + 3 + ⌈4(30 + n·d)/3⌉ |
| Issuer CPU per epoch | t_epoch = N·t_leaf + (N−1)·t_h + t_s + N·t_ser |
| Issuer throughput per core | Θ = N / t_epoch → 1/(2t_h + t_ser) as N→∞ (per-token ML-DSA: 1/t_s) |
| Issuance latency | mean Δ/2 + t_epoch; max Δ + t_epoch (timer); WC ≈ t_epoch + queueing |
| Edge verify per request | t_req = t_parse + (d+1)·t_h + t_lookup + (ρ_e/Q_e)·t_v(+t_vP·m-hash for bundles) |
| Root push bandwidth (fleet) | BW_push = E·(|σ| + 40)/Δ  [+ E·(m·n+|σ|)/P with roll-up] |
| Root pull bandwidth | BW_pull = Σ_e ρ_e·(|σ|+40); with roll-up ≤ Σ_e (V_max/P)·(m·n+|σ|)/V_max-ish (sim) |
| Edge root state | (V_max/Δ)·(n+|σ|) without roll-up (signed roots kept) vs (V_max/P)·m·n + open-period roots with roll-up (verified roots stored as n-byte hashes; signatures discarded after verify) |

### 4.6 Security argument (proof sketch, C2)

**Game EUF-CMA-TOK.** 𝒜 gets pk, the public root/bundle stream, and the state of all edges. It may query Issue(c) adaptively and have epochs closed. It wins if Verify_edge accepts (c*, e*, i*, r*, path*) such that (c*, e*, i*) was never issued (equivalently, (c*, e*) ∉ issued set).

**Theorem (informal).** Adv^{tok}(𝒜) ≤ Adv^{EUF-CMA}_{Sig}(ℬ₁) + Adv^{SM-TCR/2nd-pre}_{Th}(ℬ₂) (+ Adv_{Sig} of the period signature when roll-up is used). Here SM-TCR is single-function multi-target target-collision resistance with distinct tweaks, as used for SLH-DSA.

Critic additions (D9):
- **Parameters.** State q_h (hash queries) and the target count t ≤ Σ_e (2N_e − 1). The bound is ≈ q_h/2^{8n} classically and O(q_h²/2^{8n}) for a quantum adversary (Grover), with no factor t because the tweaks are distinct. Cite the SPHINCS+ tweakable-hash framework (Bernstein et al., CCS 2019 [TODO-verify]) for SM-TCR/SM-DSPR.
- **Ordering.** The issuer samples r *after* 𝒜 fixes c in the chosen-claims oracle, so 𝒜 cannot precompute a colliding (c, c′) pair for its own leaf.
- **Wrap-around.** epoch and idx must never wrap: rotate kid before 2^32 epochs.
- **Hybrid.** The hybrid root is an AND-combiner (both signatures verify over the same message), with its unforgeability as the max of the components. Cite Bindel et al. hybrid signature definitions [TODO-verify], because the prior paper was criticised on exactly this point.

**Sketch.** Let R* be the root the edge used for e*.
- **Case 1: R* was never output by the issuer for (kid, e*).** Then the (σ, message) pair the edge verified is a forgery for Sig: either directly on SR, or on PB_p, in which case R* ∈ PB_p means either the period message is forged or there is a collision inside the period tree, which falls under Case 2-type reasoning. This gives ℬ₁.
- **Case 2: R* = R_{e*}, the honest root.** Recompute both the honest path from leaf i* and 𝒜's path. Because c* differs from the honest c_{i*} (or i* ≥ N_{e*}, which is rejected by the N bound in SR), the two hash chains start from different inputs and end at the same root. So at some position (e*, ℓ, j) they have different inputs and equal outputs under the same tweak. The honest input at that position contains issuer randomness r unknown to 𝒜 before issuance, so 𝒜 could not have pre-selected a colliding pair. It must hit a fixed honest target after seeing it, which is a target-collision / second-preimage event at a unique tweak.
- With ≤ 2N_e·#epochs targets but distinct tweaks per target, there is no multi-target degradation (as in the SPHINCS+ tweakable-hash framework). The salt also gives **G4 hiding**: siblings are Th outputs over inputs containing 128 bits of fresh randomness.
- Plain collision resistance is a simpler but stronger assumption. It also suffices when n = 32, matching Aguilar-Melchor et al.'s proof structure for batch signatures, which the paper cites as the formal basis. We do not claim a new full proof.

**Truncation (n = 16 vs 32).**
- Classical second preimage at a given tweak costs ~2^{128} for n = 16. Quantum (Grover) costs ~2^{64} sequential queries, the same generic bound under which SLH-DSA-128s/f, which also uses n = 16 tweakable hashes, is placed in NIST category 1.
- Collision attacks (BHT 2^{n/3} ≈ 2^{43} for n = 16) would be catastrophic **only if 𝒜 controlled both inputs**. Issuer salting and tweaking prevent that, which is exactly why salting is mandatory, not optional, for n = 16.
- **Epoch-bounded validity** (G3) further confines a useful forgery to the window [T_epoch, T_epoch + V_max]. A second preimage found after that window yields claims that edges reject. We present this as defence in depth, not as part of the bound.
- Recommendation: n = 16 with SHA-256 truncation for category-1 deployments (paired with ML-DSA-44 / SLH-DSA-128), and n = 32 for conservative / CNSA-style deployments (paired with ML-DSA-65/87). The paper shows token size for both.

**Other properties.**
- G2 holds structurally.
- Replay of stolen tokens is unchanged from the status quo, mitigated by IP/ASN claims and short V_max.
- **Downgrade:** edges configured with an EMBER kid must not also accept classical tokens for the same tenant after the cut-over date. This mirrors the downgrade warning in Cloudflare PQ-to-origin [bib cf2026pqauthorigins].
- **DoS:** a garbage token with an unknown epoch could force root fetches. Mitigations:
  - an edge only fetches for e within [now − V_max − P, now] and for configured kids;
  - fetches are coalesced (one in flight per (kid, e));
  - fetches are negatively cached;
  - stapled roots cost one signature verification (bounded by a rate limit per client).
  The simulator quantifies worst-case verification CPU under a flood of distinct fake epochs.

---

## 5. Baselines

All baselines use the same claim string; only the authenticator differs.

| ID | Scheme | Role |
|---|---|---|
| B1 | HMAC-SHA256 (32 B tag) | Classical CDN status quo (Akamai-style); PQ-secure but shared-secret |
| B2 | Ed25519 | Media CDN status quo |
| B3 | ECDSA P-256 | CloudFront option |
| B4 | RSA-2048 PKCS#1 v1.5 | CloudFront option; security reference |
| B5 | ML-DSA-44 per token | Naive PQ (RFC 9964-style) |
| B6 | ML-DSA-65 per token | Naive PQ, cat 3 |
| B7 | SLH-DSA-SHA2-128s per token | Conservative hash-based |
| B8 | SLH-DSA-SHA2-128f per token | Conservative hash-based, fast sign |
| B9 | Hybrid Ed25519 + ML-DSA-44 per token | Transitional hybrid |
| O1 | EMBER, root = ML-DSA-44, n = 16 | Ours (default) |
| O2 | EMBER, root = ML-DSA-44, n = 32 | Ours, conservative node |
| O3 | EMBER, root = SLH-DSA-128s, n = 16 | Ours, hash-only assumptions end to end |
| O4 | EMBER, root = hybrid Ed25519+ML-DSA-44, n = 16 | Ours, hybrid at zero per-token cost |
| (abl.) | O1 w/o salt, w/o tweak, w/o roll-up, w/o stapling | Ablations for dissemination/latency; the salt and tweak ablations change security, not cost, so they are reported for cost only, with a note |

**Strong baselines added by the Critic (D2). These are mandatory; reviewers will ask for them.**

| ID | Scheme | What it tests | Evaluated in |
|---|---|---|---|
| B5v / B6v | ML-DSA-44/65 per token **+ edge verified-token cache** (LRU keyed by SHA-256(token), TTL = Expires) | Per-request crypto paid once per (session, edge). This is the strongest per-token competitor on CPU. | E2, E8, sim |
| B5c / B6c | ML-DSA-44/65 per token **split across 2 cookies** | Removes the 4 KB cookie objection. The remaining cost is bytes per request. | E3, E3b |
| B10 | **Multi-MAC**: one 16-B truncated HMAC per verifier domain (k ∈ {1, 3, 10} CDNs/regions) with independent keys | Answers the multi-CDN argument with symmetric crypto. Edge compromise still mints for its own domain. | E2, E3, Table V |
| B11 | **Delegated short-lived Ed25519**: an ML-DSA-44-signed epoch certificate over an Ed25519 key valid for V_max; token = claims + Ed25519 sig + key id | Same dissemination as EMBER, ~90-B tokens. PQ security rests on "no CRQC breaks Ed25519 within V_max". | E2, E3, E8, sim (same root-dissemination path) |
| B12 | **KEM-wrapped epoch HMAC keys**: per epoch the issuer generates k_e and wraps it with ML-KEM-768 to each edge (or to each PoP key); the token is an HMAC under k_e | PQ, tiny tokens. Edge compromise mints only within the live epoch(s), but for all edges. Costs push bandwidth of E·1120 B per epoch. | E2, E3, sim (push bandwidth), Table V |
| B13 | **MTL mode** (draft-harvey-cfrg-mtl-mode): one growing series per key, ladder re-signed every Δ, condensed signature = path to a rung | The nearest prior construction. Delta vs EMBER: path length grows with series length, not with epoch batch size; ladder fetch vs per-epoch root; state bounded by V_max. | E2 sizes (implemented tree, analytic ladder), sim dissemination |
| B14 | Macaroons (HMAC chain) | Attenuation, but HMAC trust. | Qualitative, Table V only |
| B15 | TLS/mTLS-bound or DPoP tokens; PQ-KEM token *encryption* (JWE with ML-KEM) | Orthogonal: binding and confidentiality, not unforgeability. | Qualitative only, explained |

Per-PoP derived HMAC keys (anycast/multi-CDN routing means the issuer does not know the serving PoP) are subsumed by B10 with k = #regions.

**Ablations (D2/D4):**
- salt off / tweak off (cost only);
- n = 16 vs 32;
- roll-up off;
- stapling off;
- pooling off;
- pad-to-2^d on;
- adaptive vs **oracle best fixed Δ** vs WC;
- verify cache on/off (for all schemes, including EMBER).

**Trust comparison (Table V, now mandatory).** Columns:
- secret at edge? (lifetime);
- one edge compromised: who can it mint for?;
- PQ assumption (unconditional / time-bounded classical);
- accountability;
- token bytes;
- per-request verify (native);
- dissemination bytes/s.

---

## 6. Experiment plan

### 6.0 Anchors measured by the Designer (sanity only; NOT paper numbers)
On this VM (Intel Xeon 2.1 GHz; AVX2/AVX-512/SHA-NI flags present), a one-off pqcrypto 1.0.0 probe gave:

| Scheme | pk (B) | sig (B) | sign | verify |
|---|---|---|---|---|
| ML-DSA-44 | 1312 | 2420 | ≈7.5 ms | ≈154 µs |
| ML-DSA-65 | 1952 | 3309 | ≈10.5 ms | ≈217 µs |
| SLH-DSA-128s | 32 | 7856 | ≈309 ms | ≈331 µs |
| SLH-DSA-128f | 32 | 17088 | ≈15 ms | ≈948 µs |

SHA-256 on 65 B from Python hashlib took ≈0.4 µs per call, dominated by interpreter overhead.

**Anomaly A1.** ML-DSA-44 sign at ≈7.5 ms is ~50× its verify and ~46× its keygen (163 µs). That is far slower than published reference figures (hundreds of µs) and suggests a slow path in the binding (for example per-call key expansion from the seed, or the RNG). The Experimenter **must**:
1. investigate this;
2. cross-check with a native build: liboqs `speed_sig`/`test_sig` via cmake, or PQClean/mldsa-native ref + AVX2, compiled with gcc;
3. report native (AVX2) and pqcrypto numbers separately and label them.
Scout B's probe (`results/probe_openssl_speed.csv`) confirms this: in the `openquantumsafe/oqs-ossl3` Docker image (OpenSSL 3.6.0 + oqsprovider, 1 core), ML-DSA-44 sign is ≈675 µs and verify ≈123 µs. So the pqcrypto sign path is ~11× slower than native and **must not** be presented as "ML-DSA signing cost"; use the native column for issuer-side claims. **Never** present ms-level ML-DSA *verify* figures. Per the prior-rejection lessons, verify must be in tens to hundreds of µs.

### 6.1 Experiments

**E1. Primitive microbenchmarks (real).**
- Schemes: keygen/sign/verify for B1–B9 plus root signers, and SHA-256 Th calls at n = 16/32.
- Samples: ≥2000 per op (≥30 for SLH-DSA-128s sign).
- Method: pinned to one core (`taskset -c 2`), GC disabled, warm-up 200, `perf_counter_ns`.
- Report median, p99, and 95% bootstrap CI.
- **Primary (Critic, D10).** A native C/EVP benchmark against **OpenSSL 3.5.4** (scratchpad build at `$SP/opt/ossl35`). It covers ML-DSA-44/65/87, SLH-DSA-128s/f, Ed25519, ECDSA-P256, RSA-2048, ML-KEM-768 (for B12), HMAC-SHA256, and EMBER path verify (d = 4..24, n = 16/32).
- **Statistics.** ≥ 5 independent process runs × ≥ 2000 iterations (SLH-DSA-128s sign: 5 × 10). Report the median of run-medians with a bootstrap 95% CI over runs, plus the pooled p99.
- **Cross-checks.** Docker OpenSSL 3.6 + oqsprovider `openssl speed`, and Go/circl (used by the E8 prototype). Each must be within 3× of OpenSSL 3.5.4, otherwise investigate.
- Python pqcrypto numbers are secondary and labelled.

**E2. Token-level benchmarks (real).**
- Build actual tokens for each scheme with realistic claims: URLPrefix ≈ 60-char path, Expires, Tenant, with and without IP.
- Measure encoded size in signed-URL and cookie forms.
- Edge verify per token: full parse + checks + crypto, for EMBER with warm root cache at N ∈ {2^4 … 2^20}.
- Issuer throughput (tokens/s per core): per-token schemes vs EMBER at N ∈ {2^0 … 2^20}, plus a 4-process run.

**E3. Fit analysis.**
- Fraction of tokens fitting the limits for a URL-length distribution: real-like path lengths. Use a lognormal with parameters stated as assumptions and swept, plus fixed 60/120/250-char cases.
- Limits:
  - 2048 B URL (legacy practice; label as practice, not a standard);
  - 8000 B URL (RFC 9110 recommendation);
  - 4096 B cookie (RFC 6265 minimum);
  - an 8 KB request-header total, as a common server default [TODO-verify, or present as an assumption].

**E4. Analytical model validation.**
- Compare predicted S_tok, issuer Θ, and edge t_req against E2 measurements: report error.
- Compare M(Δ) against the simulator: report MAPE, without overclaiming.

**E5. Fleet simulation (vectorised epoch-level Monte Carlo + event-driven root cache), driven by measured E1 costs.**
- **Edges:** E ∈ {100, 500, 2000}. Traffic share w ~ Zipf(α_pop = 0.8) over PoPs (assumption, swept 0–1.2).
- **Tenants:**
  - T = 1000;
  - session-start rates Zipf(1.0) across tenants;
  - aggregate peak λ ∈ {200, 2000, 20000} tokens/s;
  - diurnal NHPP λ(t) = λ̄(1 + a·sin(2πt/86400 + φ)) with a = 0.6;
  - 24 h simulated with epoch-level aggregation.
- **Sessions:**
  - 1 token per session;
  - sticky edge sampled by w;
  - requests: 1 manifest + K segments, K ~ geometric(mean 150, i.e. ~10 min at 4 s segments);
  - segment interval 4 s;
  - content popularity Zipf(0.9) over 10⁵ objects, used for cache hit/miss in end-to-end latency only.
- **Network** (lognormal, stated assumptions, swept ×0.5/×2):
  - client→edge RTT median 20 ms (σ = 0.6);
  - edge→shield median 15 ms;
  - shield→root-service median 60 ms;
  - push propagation median 150 ms;
  - client token-receipt→first request median 120 ms.
- **Modes:** pull, push, pull+stapling, pull+roll-up, push+roll-up.
- **Epoch policies:** fixed Δ ∈ {0.01, 0.1, 1, 10, 60} s; WC; adaptive controller. Tenant pooling on/off.
- **Metrics:** issuance latency (mean/p99), root misses per token and per request, request-latency overhead CDF (verify CPU + miss RTT), root bandwidth (fleet and per edge), edge CPU per request (p50/p99, including amortised root verify), issuer CPU, token size distribution.
- **Validation:** a full per-request discrete-event simulation (heapq) for 1 h at λ̄ = 200/s, E = 100, cross-checked against the vectorised simulator on the same seeds. Report the difference.

**E6. Sensitivity:** Δ × E heatmap of misses/token; V_max; m (period length); n; root signer; RTT scale; Zipf α.

**E3b. Wire bytes per session (real encoder).**
- Encode the request headers of a session (manifest + K = 150 segment requests) with Go `golang.org/x/net/http2/hpack`, default 4096-B dynamic table.
- Token placement: in the URL query (`:path` changes every segment, so the token is not indexed) or in a cookie (indexable only if the entry is ≤ table size).
- Report upstream header bytes per session for every scheme, including B5c/B6c and EMBER with/without the stapled root on the first request.
- Also report HTTP/1.1 (no compression).
- This replaces "% fit" as the main size metric. % fit is kept as a sanity check, since it holds for EMBER by construction.

**E8. Real prototype (Go, netns + tapbridge). This is the non-circular validation (D3).**
- Components (Go 1.24.7, stdlib + `cloudflare/circl` v1.6.1 for ML-DSA):
  - **edge**: net/http; verify from query or cookie; serves a fixed in-memory 64 KB object; root cache with singleflight coalescing and a negative cache; optional verified-token LRU; hosts V virtual edges (separate root caches, selected by a header) to emulate E > 1.
  - **issuer + root service**: timer-Δ batching; ML-DSA-44 root via circl; per-token modes.
  - **loadgen**: open-loop Poisson sessions; each fetches a token and then K segments at a time-compressed interval.
- Topology: three namespaces, `cli`, `edge` and `origin`, joined by two `tapbridge` instances (reused tooling from the author's prior work, branch `origin/claude/brave-meitner-l8yswp`, `experiments/src/tapbridge.c`, `scripts/net.sh`), with MTU 1500 and offloads off.
  - cli↔edge one-way delay 10 ms (RTT 20 ms);
  - edge↔origin one-way delay 37.5 ms (RTT 75 ms ≈ shield + root service).
- Cores: loadgen 0, edge 1 (GOMAXPROCS = 1), both tapbridges 2, issuer/root 3.
- **We do not sweep initcwnd, congestion control or loss, and we do not re-derive any handshake round-trip model.** That is the author's prior work (DO-NOT-REPEAT #3). Connections are kept alive, so TLS is omitted and stated as a limitation.
- Experiments:
  - **P1 capacity**: closed-loop max req/s at the edge per scheme (B1, B2, B3, B5, B5v, B11, B12, O1 warm, O1 cold-per-epoch). Run on the loopback within the `edge` ns (no tapbridge) to measure CPU, not the link.
  - **P2 latency under load**: open loop at 50% and 80% of each scheme's P1 capacity over tapbridge; added latency p50/p99 vs HMAC.
  - **P3 dissemination validation**: pull and pull_staple modes, V ∈ {10, 50} virtual edges, Δ ∈ {0.1, 1, 10} s, λ ∈ {20, 200} tokens/s, 5 min each. Measure misses/token, miss latency, and root bytes. Run **fleet_mc and the analytic model with the identical configuration and the measured RTTs**, then report rel. error with CIs. This is the validation the paper uses.
- 5 independent runs per point; Student-t 95% CI over runs.
- Limitation stated: one VM, so processes share the host; tapbridge is a userspace emulator; edge scale-out beyond one core is simulated.

**E7. DoS stress:** a flood of tokens with random valid-range epoch ids to one edge, with and without coalescing and negative caching. Measures root fetches/s and signature verifications/s.

### 6.2 Hypotheses (outcomes are whatever the code produces; report refutations)
- **H1 (size).** EMBER/n16 tokens stay < 512 B encoded for N ≤ 2^20. Fit is by construction, so the claim is about *bytes per session* (E3b): EMBER ≤ 0.25× B5c upstream header bytes per session in URL form. In cookie form under HPACK the gap may be small; report whatever is measured. B11 and B12 are smaller than EMBER; this is expected and is to be discussed via Table V, not hidden.
- **H2 (edge CPU).** With a warm root cache, EMBER per-request verify (native/Go) is within ≤5× of HMAC-SHA256 and ≥10× cheaper than *uncached* per-token ML-DSA-44 verify. Against **B5v** (verify cache), report per-session amortised CPU; EMBER's advantage is expected to shrink to the first request per (session, edge). Report P1 req/s per core.
- **H3 (issuer).** EMBER issuer throughput is hash-bound and ≥100× per-token ML-DSA-44 signing per core at N ≥ 2^8. SLH-DSA-128s becomes a usable root signer: only ≤ k/t_sign roots/s are needed.
- **H4 (dissemination).** Root bandwidth is < 0.1% of the edges' served bytes for Δ ≥ 0.1 s, under a stated per-segment-size assumption. Roll-up reduces pull misses for low-rate tenants by ≥ 5×.
- **H5 (controller).** Under diurnal multi-tenant load the adaptive controller achieves lower mean D than the **oracle best single fixed Δ** (paired CI over ≥ 10 seeds), while respecting the budget and SLO. **Pre-registered demotion rule:** if the improvement is < 10 ms or < 10% (CI including these), C4 becomes a guideline and the paper says so.
- **H6 (end-to-end).** With pull + stapling or push + roll-up, < 1% of requests incur a root-miss RTT, and the p99 request-latency overhead is < 1 ms of CPU.
- **H7 (hybrid).** A hybrid root (Ed25519 + ML-DSA-44) changes per-request edge cost by < 1% versus an ML-DSA-only root.
- **H8 (validation, E8).** fleet_mc predicts the prototype's misses/token and mean miss-added latency within 15% (or within the CI) on all P3 configurations. A failure is reported, and the simulator is corrected or its scope narrowed.
- **H9 (issuer, native).** With OpenSSL 3.5.4 native timings, EMBER issuer tokens/s per core at N ≥ 2^8 is ≥ 50× per-token ML-DSA-44 native signing, and B11/B12 issuance is comparable to EMBER.

### 6.3 Figures (8) and tables (4)
- **Fig 1.** Architecture and message flow: issuer → epoch tree → signed root → tier/edges; client token; stapling and roll-up. A TikZ diagram, no data.
- **Fig 2.** Encoded token size per scheme (bars, log y) with horizontal lines for 2 KB URL, 4 KB cookie, 8 KB URL. EMBER at N = 2^10/2^16/2^20.
- **Fig 3.** EMBER token size vs log₂N for n = 16/32: model line + measured markers. Secondary axis: issuer tokens/s per core vs N.
- **Fig 4.** Edge per-request verify time (median and p99, log scale) per scheme. Python and native panels.
- **Fig 5.** Issuance latency vs Δ and misses per token vs Δ for 3 tenant rates (pull mode): the interior optimum of D(Δ), model vs simulation.
- **Fig 6.** 24 h diurnal time series: Δ chosen by the controller, p99 issuance latency, and miss rate, vs fixed-Δ policies.
- **Fig 7.** Root-distribution bandwidth and misses per 10⁶ requests for push/pull/stapling/roll-up vs E (2 panels).
- **Fig 8.** CDF of the added request latency per scheme/mode (end to end, including tails from root misses).
- (Optional Fig 9.) Sensitivity heatmap, Δ × E → misses/token.
- **Table I.** Related work comparison (§1.2 table, condensed).
- **Table II.** Measured primitive costs and sizes (E1), with CIs.
- **Table III.** % tokens fitting each limit per scheme (E3).
- **Table IV.** Simulation parameters and assumptions (with sweep ranges).
- (Optional Table V.) Security property comparison: edge-compromise forgery, PQ, accountability, revocation granularity, per-request cost class.

---

## 7. Paper outline (IEEEtran conference, 8–10 pages)

1. **Introduction** (1 p). CDN token auth, the trust problem with HMAC, PQ migration of RSA/ECDSA/Ed25519 tokens, and why naive ML-DSA/SLH-DSA tokens break URL/cookie limits. Contributions C1–C5. Honest framing: there is no HNDL for signatures.
2. **Background** (1 p). Signed URLs and cookies (vendor schemes); FIPS 204/205 sizes; RFC 9964; Merkle trees; batch signatures (CT-RSA'24); MTL; MTC/MTAC.
3. **System and threat model; requirements R1–R7** (0.75 p).
4. **EMBER design** (2 p). Format, tweakable hash, Issue/Publish/Verify, stapling, roll-up, revocation, and multi-tenant pooling.
5. **Epoch control** (0.75 p). The D(Δ) model, constraints, and controller.
6. **Security analysis** (1 p). Game, theorem sketch, truncation, DoS, downgrade, privacy.
7. **Implementation and methodology** (0.5 p). Code, machine, pinning, Python vs native, simulator and its validation, assumptions table.
8. **Evaluation** (2.5 p). Size and fit (Fig 2/3, Tab III); CPU (Fig 4, Tab II); issuer (Fig 3); latency/control (Fig 5/6); dissemination (Fig 7); end to end (Fig 8); sensitivity and DoS.
9. **Discussion and limitations.** No real CDN deployment; simulated network; Python overhead; bearer replay unchanged; issuer key compromise; deployment path (CloudFront/Media CDN config changes, JOSE/COSE encoding via RFC 9964 for root signatures).
10. **Related work** (if not merged into §2) and **Conclusion**; artifact availability.
Also: AI-assistance declaration per venue policy.

**Defences against each prior-rejection reason (Critic, per coordinator):**
- *Implausible numbers*: every timing is sanity-checked against `feasibility.md` anchors (ML-DSA-44 verify ~120 µs in OpenSSL; tens of µs on AVX2 implementations). Never ms-level ML-DSA verify.
- *Interpolated or projected results*: none. Model curves are drawn as lines and labelled "model"; only run points are markers; sims are labelled "simulated".
- *Marginal implementation-level contribution*: the contribution is a protocol/token format plus fleet dissemination and epoch control, evaluated against strong baselines; the batching primitive is credited to prior work.
- *Client and server on one host over loopback*: separate netns + tapbridge + pinned cores; the residual single-VM limitation is stated.
- *Unjustified metrics*: D(Δ) is in seconds; there are no weights or composite scores.
- *HNDL confusion*: §2 states there is no HNDL for authentication.
- *Issuer cost*: from native OpenSSL 3.5.4 (scratchpad build), with ≥ 5 runs and 95% CIs.

**Do-not list (from prior rejection):**
- No DAPV-like "accept provisionally, verify later". EMBER never accepts before the root is verified; stapling and pull are synchronous.
- No invented risk metrics; D(Δ) is in seconds, from first principles.
- No projected numbers presented as measured.
- No ms-level ML-DSA verify claims.
- No "cross-platform" claim.


---

## 8. Limitations (to appear in the paper, Critic D17)
1. No production CDN deployment or trace. Workload parameters (Zipf exponents, RTTs, segment sizes, URL lengths) are assumptions, swept and listed in Table IV.
2. The prototype runs on one 4-vCPU VM. Netns + userspace `tapbridge` stands in for netem (unavailable). Edge scale-out (E ≥ 100) is simulated; the simulator is validated only at small scale (E8 P3), so extrapolation to E = 2000 is model-based.
3. TLS is not included in the prototype (kept-alive connections). It is orthogonal to token verification, and handshake-level PQ costs are the author's separate prior work.
4. Security is a proof sketch reducing to standard assumptions, not a new machine-checked proof.
5. Bearer-token replay is unchanged from the status quo. Binding options are discussed, not evaluated.
6. B11 (short-lived Ed25519) and B12 (KEM-wrapped MAC) may beat EMBER on size. EMBER's advantage is a combination of trust properties (Table V), not dominance on every metric.
7. Tenant pooling requires the tenant to trust the CDN-held issuer key.
8. Epoch-bounded validity forces token refresh for long sessions.
9. The implementations measured (OpenSSL 3.5.4, circl, pqcrypto) are not the fastest AVX2 implementations. Absolute numbers are implementation-specific; ratios are the robust result.
10. The root stream leaks issuance volume unless padding or bucketing is used.

## 9. Critic changes log (2026-11-05)
Details and severity are in `design/critique.md`.
- **D1** Reframed C2 as a profile of batch signatures and MTL. Removed "first". Added C6 (real prototype). MTL mode added as baseline B13.
- **D2** Added strong baselines: B5v/B6v (verify cache), B5c/B6c (multi-cookie), B10 multi-MAC, B11 delegated short-lived Ed25519, B12 ML-KEM-wrapped epoch HMAC keys, B13 MTL, B14/B15 qualitative. Expanded ablations. Table V (trust comparison) is mandatory.
- **D3** Added E8: a real Go prototype in netns + tapbridge. Simulator validation now against real measurements (H8). DES-vs-MC is relabelled an internal consistency check.
- **D4** Controller evaluated against the oracle best fixed Δ, with a pre-registered demotion rule (H5).
- **D5** G2 benefit restated as lateral blast radius.
- **D6** Pooling trust caveat; tenant id in the tweak.
- **D7** Privacy and side channels: volume leak via N_e, linkability, cache-probe timing; mitigations.
- **D8** Replay classes, binding options, clock-skew tolerance, and new negative tests.
- **D9** Proof sketch tightened: q_h, targets, salt ordering, no wrap, AND-combiner hybrid with citation.
- **D10** Native OpenSSL 3.5.4 is the primary timing source. ≥ 5 runs × ≥ 2000 iterations, bootstrap CI over runs, implementation labels, cross-implementation sanity bound.
- **D11** Sim statistics: ≥ 5 seeds (10 for the controller headline), Student-t CIs, common random numbers, paired-difference CIs.
- **D12** Compute budget and horizon cuts (spec §5.1).
- **D13** E3b: bytes per session with a real HPACK encoder. % fit demoted to a sanity check.
- **D14** Removed speculation about vendor motives.
- **D15** Token-refresh metric for long sessions.
- **D16** Bandwidth reported in absolute terms; ratio over the segment-size sweep.
- **D17** Limitations list (§8).
- **D18** Revocation propagation metric.
- Added an explicit mapping of the prior-rejection reasons to defences (§7).
