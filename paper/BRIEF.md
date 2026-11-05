# Research brief (shared by all agents)

Goal: a medium-level, submittable research paper (IEEE conference / mid-tier journal, e.g. IEEE Access,
Computer Networks, Computers & Security, IEEE ICC/Globecom workshops) at the intersection of
**Content Delivery Networks (CDN)** and **Post-Quantum Cryptography (PQC) security**.

## Pipeline
1. Scout   -> paper/scout/      : literature map + ranked candidate novel problem statements
2. Design  -> paper/design/     : chosen problem, threat model, novel methodology, experiment plan
3. Experim -> paper/experiments/ (code) + paper/results/ (CSV, figures): real measurements
4. Writer  -> paper/manuscript/ : LaTeX (IEEEtran) paper + references.bib

## Hard rules
- Every number in the paper must come from code in this repo that was actually run. Never invent results,
  citations, DOIs, or venues. Only cite papers you verified exist (title/authors/year/venue).
- Must be feasible on this machine: 4 CPU, 15 GB RAM, no GPU, Python 3.13 (venv with pqcrypto, numpy,
  pandas, scipy, matplotlib at the scratchpad venv), gcc/cmake/docker available, outbound internet via proxy.
  Linux `tc`/netem may not be available; simulation + real crypto microbenchmarks is acceptable.
- Must NOT duplicate the author's earlier rejected paper (Tamarin formal verification of PQ TLS 1.3
  handshake / resumption tickets with origin ("DAPV"), session session_01Jb8HMWz9ts69GFaCe29zyn).
- Today is 2026-11-05. NIST FIPS 203/204/205 (ML-KEM, ML-DSA, SLH-DSA) are final; FN-DSA/HQC in progress.
