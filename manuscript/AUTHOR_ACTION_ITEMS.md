# What the authors still have to do before resubmitting

The revised `main.tex` covers every reviewer comment that can be fixed by
rewriting. Some comments need **new experiments or facts that only you have**.
Those places are marked in red in the PDF as **[AUTHOR INPUT: …]**. There are
23 of them in `main.pdf`. **Do not submit until they are all resolved.** No
numbers were invented for these gaps.

## A. Problems found in your own data (please check against the raw measurements)

1. **The latency saving cannot come from PQ arithmetic.** PQ verification takes
   0.08–0.14 ms (your Table 2), but DAPV saves 14–21 ms. Reviewers will notice
   this. The paper now says so openly (Sec. 6.2). Please profile the
   synchronous path (perf / VTune / ETW) to find the real cause.
2. **Windows timer resolution is a likely suspect.** The default Windows timer
   period is 15.6 ms. That is close to both the saving and the 14–21 ms
   "thread dispatch" part of Δt. Creating a thread normally takes tens of µs.
   Re-measure on the Linux testbed, or on Windows with `timeBeginPeriod(1)`.
3. **The FN-DSA saving is not constant across RTT.** It is 14.3 ms at 0 ms RTT
   and 20.0 ms at 150 ms RTT (48.5→34.2 and 199→179). The old text claimed
   "variation below 0.2 ms", which is not true for FN-DSA.
4. **The standard-deviation claim contradicts Table 2.** The old text said the
   SD was below 4% of the mean "in all cases". But the Δt CI [18.6, 23.8] with
   n = 30 implies SD ≈ 7 ms (about 33%). The text now limits the 4% claim to
   latency and throughput.
5. **Some numbers in the old Comparison table were wrong.**
   - "+52% latency @150 ms" for this work (sync) is really +25% (206 vs 165).
   - "55% throughput loss" (sync) vs "20%" (DAPV) mixed two concurrency
     levels: 55% is at 1000 clients, 20% is at 500 clients. At 500 clients the
     figures are 39% vs 20%.
   - The prior-work numbers (Paquin, Sikeridis, Montenegro, Sosnowski) could
     not be verified. That table is now qualitative.
6. **The old risk figure contradicted its own text.** Fig. 11 showed about 0.8%
   risk at 1 Gbps / 20 ms, but the text said "approaches 10%" (that value is
   for 10 Gbps). β was never calibrated, so the model was removed.
7. **The old leakage table mixed units** (MiB vs MB). It has been recomputed in
   decimal units from the measured Δt values.
8. **Fig. 9's "2.5×" is measured against the idle 95th percentile** (23.8 ms),
   not the idle median as the old text said.
9. **The old Fig. 10 labelled 2420 B (the ML-DSA-44 signature alone) as
   "public key + signature".** It was replaced by Table 1 with standard sizes.
10. **The old "fragmentation adds round trips when a message exceeds the MTU"
    model was wrong.** An extra round trip happens only when the server flight
    exceeds TCP's initial congestion window (about 14.6 KB). Your own curves
    have equal slopes, so δk = 0 in your setup.

## B. Facts to supply (quick)

- Target journal (`\journal{}`).
- Whether client and server ran on the same host, and any CPU pinning.
- Which testbed (Windows or Linux) produced each figure and table.
- Key-exchange group (X25519 or X25519MLKEM768?) (Reviewer 4, detailed comment 4).
- Number of certificates in the chain, and whether the leaf was self-signed.
- Whether PQ chain signatures were also deferred, or only CertificateVerify.
- liboqs and oqs-provider versions, the load-generator tool, handshakes per run,
  and whether sessions were resumed.
- The netem interface (loopback?) and how delay was split between directions.
- Whether latency at RTT 20/50/100 ms was **measured** (Fig. 3 shows points
  there, but the old Table 4 said they were interpolated) (Reviewer 5,
  comment 8).
- How the prototype reports a PQ failure to the main thread. Whether the
  bounded pool, the ticket handling and the `SSL_get_dapv_state` API are
  implemented or only proposed.
- **A public code repository and archive DOI** (Reviewer 4, weakness 3). This
  was a stated reason for rejection.

## C. New experiments the reviewers asked for (strongly recommended)

1. Put the client and server on **separate hosts** over a real NIC, or at least
   on disjoint pinned cores / veth namespaces. Report server-only throughput.
2. Use a **2–3-certificate chain** with hybrid certificates. This is also where
   DAPV has the most to defer.
3. Test **X25519MLKEM768** key exchange for the hybrid configurations.
4. Use **≥1000 handshakes** for the Δt distribution, so the percentiles mean
   something.
5. Implement and measure the **bounded pool**, so the "Δt < 1 ms" claim is
   measured instead of projected.
6. Optionally: a **three-algorithm hybrid**, or SLH-DSA. Here parallel workers
   give a real benefit (Reviewer 4, weakness 6).

## D. References

- Removed/replaced: the old `Cremers2016` pointed to a non-existent draft.
  It is now the IEEE S&P 2016 paper. `Cheval2022` could not be verified and
  was replaced by Cremers et al., CCS 2017.
- Unused entries were dropped: Gamma1994, Fowler2014, Goldsmith2022,
  Keshav2019, Butin2017, Blanchet2024, Alnahawi2023practical. Please
  double-check Goldsmith2022 and Keshav2019 in particular: they could not be
  located and should not be cited anywhere.
- New entries were checked against publisher / IETF / ePrint listings.
  Still verify FIPS 206's current status and the HybridSpectrums author list.

## Files

- `main.tex` / `main.pdf`: revised manuscript (the sequence diagram is now
  TikZ, inside `main.tex`).
- `response_to_reviewers.tex` / `.pdf`: point-by-point response to
  Reviewers #4 and #5.
- `references.bib`
- `figures/`: figures still used are fig01, fig02, fig04, fig05 and fig09.
- `previous_submission/`: the R2 sources you uploaded, unchanged.
