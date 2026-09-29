# Before you submit: what changed and what is left

## 1. What the paper is now

**New title:** *Post-Quantum Authentication Latency in TLS 1.3: A Validated
Model and the Limits of Deferred Signature Verification*

The paper has been reframed from "DAPV makes TLS faster" into a
**measurement-and-model paper**. The earlier framing was not supported by the
new data. Its contributions, all backed by data in `experiments/`:

1. **A parameter-free latency model** for PQ authentication in TLS 1.3.
   - Predicts the number of round trips in **68/68** configurations.
   - Mean absolute latency error **2.2%**.
   - Covers 5 schemes, RTT 20–150 ms, initial window 10/20/40, BBR and CUBIC.
2. **The break-even point of deferred verification.**
   - Gain = 0.97 × verification work − 0.14 ms, with R² = 0.999.
   - It gains nothing for ML-DSA/FN-DSA on AVX2 CPUs.
   - It gains 9–26% without vector instructions and up to 65% for slow
     verifiers.
3. **Network findings.**
   - An initial window of 40 cuts SLH-DSA handshakes from 454 to 165 ms at
     150 ms RTT.
   - BBR pacing keeps part of the cost.
   - 3% loss doubles the 90th-percentile latency of ML-DSA handshakes but not
     of classical ones.
4. **DAPV specification, security analysis and open implementation.**
5. **Deployment guidance** (Section 9).

**Scale of the evaluation:** more than 46,000 individually timed handshakes
across six experiments (E1–E6), plus the throughput runs.

## 2. Remaining red markers in the PDF (2)

- `\journal{}`: the target journal (see section 4).
- **Repository URL and DOI** (Section 6.2 and the response letter).
  - Put `experiments/` (code, patch, raw data) in a public GitHub repository.
  - Archive it on Zenodo to get a DOI.

## 3. Things you must do yourself

- **Understand and check the results.** Read `experiments/README.md`, re-run
  at least one experiment, and make sure you can explain every number. You
  will have to defend them to reviewers.
- **Disclose AI assistance.** Elsevier and most publishers require authors to
  declare the use of generative-AI tools in writing and in research (for
  example in a "Declaration of generative AI and AI-assisted technologies"
  section). The rewriting, implementation, experiments and analysis in this
  revision were done with an AI assistant. Check your target journal's
  policy and disclose accordingly. AI tools cannot be listed as authors.
- **Physical-host validation (strongly recommended).**
  - Everything ran on one 4-vCPU cloud VM, with network namespaces and
    disjoint cores standing in for separate machines. This is stated
    honestly in Section 7.7.
  - Re-running E1 and E3 on two physical machines would remove the most
    likely reviewer objection. The drivers only need the IP address and CPU
    pinning changed.
- **Optional, and high value:** measure one real ARM device (for example a
  Raspberry Pi) as the client. That places a real device on the break-even
  curve (Figure 4).
- **Check the references.** Confirm FIPS 206's current status and the author
  list of the "Hybrid Signature Spectrums" draft.

## 4. Where to submit

Rejection by Computer Networks usually means a new submission elsewhere.
If you want to go back to Computer Networks, check its policy on
resubmitting a substantially new manuscript. Good fits for a
measurement-plus-model paper, roughly from most to least selective:

- *IEEE Transactions on Network and Service Management*
- *Computer Networks* (Elsevier), as a new submission if the policy allows
- *Computer Communications* (Elsevier)
- *Journal of Network and Computer Applications* (Elsevier)
- *Computers & Security* (Elsevier), if you emphasise the provisional-state
  security analysis

A shorter version would also suit venues such as the PQCrypto conference
or measurement-focused workshops.

No revision can guarantee acceptance. The honest version is the one most
likely to survive expert review, because reviewers of PQ-TLS papers know
the field's numbers well.

## 5. Files

- `main.tex` / `main.pdf`: the revised paper.
- `response_to_reviewers.tex` / `.pdf`: point-by-point answers to the
  Computer Networks reviews. Useful as a cover letter ("previously reviewed
  at…"), or to adapt.
- `figures/`: the paper's figures.
- `previous_submission/`: your original R2 sources.
- `../experiments/`: everything needed to reproduce the results.
