# What the authors still have to do before resubmitting

## 1. Read this first: the new experiments overturn the original claims

The experiments the reviewers asked for have now been run (see
`experiments/README.md`). The setup was:

- three-certificate hybrid chains;
- X25519MLKEM768 key exchange;
- client and server in separate network namespaces on disjoint cores, joined
  by an emulated 1500-byte-MTU link;
- 1000 handshakes per configuration;
- a measured bounded worker pool.

**Results:**

| Claim in the previous version | New measurement |
|---|---|
| DAPV saves ≈20 ms of handshake latency | **No measurable saving** for ML-DSA-44, ML-DSA-65 or FN-DSA-512: median change within ±0.2 ms, with CIs spanning 0. A thread per job is **0.15 ms slower**. Only SLH-DSA-128f benefits: −1.59 ms (−13.5%) at RTT 0. |
| Server throughput +31–36% | **No gain** in either CPU placement. DAPV is −7% to +4% vs synchronous, within run-to-run noise. |
| Δt = 14–21 ms, dominated by thread overhead | Δt = **0.079 ms median, 0.42 ms p99** (ML-DSA-44, bounded pool); 0.114 / 0.99 ms with a thread per job. |
| "Δt < 1 ms with a thread pool" (projection) | Now measured, and well below 1 ms. |

The manuscript has been rewritten around the new data:
- abstract;
- contributions;
- Sections 5–6 (entirely new);
- the leakage table;
- conclusion.

The old Windows measurements are no longer reported. Section 6.2 says that
they could not be reproduced, and that timer-quantised waiting on Windows is
the most plausible cause.

**This is your decision.** If you believe the Windows prototype measured
something real, you would have to show why a different implementation gives
the opposite result. In my assessment, the honest paper is the one now in
`main.tex`: a careful measurement study showing *when* deferral helps
(expensive verification) and when it does not (lattice schemes on
vector-capable CPUs). A measurement-focused venue, or a short paper, may suit
it better than Computer Networks' full-paper track.

## 2. Remaining red markers in `main.pdf` (2)

- `\journal{}`: the target journal.
- **Repository URL and archive DOI** (Section 5.2). Push `experiments/`
  (code, patch, raw data) to a public repository and archive it on Zenodo.
  Missing code was one of the stated reasons for the rejection.

Also fill the one marker in `response_to_reviewers.tex` (the same URL/DOI).

## 3. Honest limitations to be aware of (all stated in Section 6.4)

- **Separate *namespaces and cores*, not separate *physical machines*.**
  Everything ran on one 4-vCPU cloud VM. That removes CPU competition and
  loopback, which were the reviewers' concrete concerns, but the two sides
  still share cache, memory bandwidth and the hypervisor. If you can, repeat
  E1/E2 on two physical hosts: the drivers only need the IP address and CPU
  pinning changed.
- **The link is emulated** by a userspace bridge (`netem` was unavailable):
  fixed delay, 1 Gbit/s, no loss.
- **One CPU type** (Intel Xeon 2.1 GHz with AVX2). Devices without vector
  units, where deferral should help most, are still unmeasured. This is the
  most valuable next experiment if you want a positive result for DAPV.
- **The hardware changed.** The experiments ran on a cloud VM, not your
  i7-11800H / Xeon 4310 testbeds. The paper describes the actual testbed.

## 4. References

- Replaced: the old `Cremers2016` pointed to a non-existent draft and is now
  the IEEE S&P 2016 paper. `Cheval2022` could not be verified and was
  replaced by Cremers et al., CCS 2017.
- Still to verify: FIPS 206's current status, and the HybridSpectrums author
  list.

## Files

- `main.tex` / `main.pdf`: revised manuscript with the new evaluation.
- `response_to_reviewers.tex` / `.pdf`: point-by-point response.
- `figures/`: new figures `e1_*.pdf` and `e2_*.pdf`. The old fig01–fig11
  are no longer used.
- `previous_submission/`: the R2 sources as uploaded.
- `../experiments/`: code, patch, raw data, analysis.
