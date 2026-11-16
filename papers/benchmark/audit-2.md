# Code audit, loop 2: benchmark (HEAD 6ad24e7)

All file:line references are to HEAD 6ad24e7. The tree is committed and stable.

## Part 1: status of the loop-1 findings

| loop-1 id | status | evidence (file:line) |
|---|---|---|
| B1 delayed forger / reception-time model | **closed** | The prompt forger is now injected in the disclosure slot: `run_proto.py:237` (`g_f = m_ + d + 0`). Both reception stamps are modelled (`modes.py:598`, `:604-611`), plus a guard variant. The threshold sentence is now derived from the stamp model (`summarize.py:842-869`). Analytically, prompt+start is accepted from δ + 1 ms behind, prompt+end from 1.5 slots, delayed+end from 2.5 slots. These agree with the receiver rule at `modes.py` (time-safety line in `_resolve`: `t_arr + delta_eff + guard > t_rel + relax`). |
| M1 first-come candidate caps | **partly closed** | `bind_slot` (`modes.py:609`) stops application candidates from other slots. The chain tag cap is 32 (`:59`, `:846`). Still open: see N2 (cross-slot pre-filling through fields that are not bound) and N1 (the binding is an oracle). Same-slot pre-filling is disclosed (`summarize.py:828`). |
| M2 R4/R4c not mutation-sensitive | **closed** | R4/R4c now use the prompt forger (`negative_tests.py:182`). C4m1 (release time relaxed by one slot) and C4m2 (δ = 0) must accept the forgery (`:194`, `:196`). With stamp=start and offset -0.5, the rule has a 1 ms margin, so both mutations flip the outcome. |
| m1 hard-coded literals | **partly closed** | The assumptions table now uses the constants (`summarize.py:204`). Line 904 still hard-codes "3 candidate symbols", "8" and "Merkle 16" in prose. |
| m2 key stash displacement | **partly closed** | The stash now keeps 2 candidates per index (`modes.py:917`). Two bogus keys per index sent ahead of the honest one still displace it. The key field (ke, ki) is not bound to the delivery slot (see N2). |
| m3 stale blob kills object | **closed** | A stale blob now costs one try: `modes.py:682` (frag), `:797` (Merkle), `:870` (anchor). |
| m4 reception-time model undisclosed | **closed** | Rx docstring `modes.py:582-591`; assumptions table `summarize.py:205`. |

### Checks requested on the fixes

- **bind_slot vs multi-slot spans: honest traffic is not broken.** Every frame of slot g carries application message g (`build`: `S.frames[g] = (apps[g], auth)`; `make_app` packs seq = g, `modes.py:432-434`). Symbols of other objects ride in those frames, so binding never drops an honest frame. I confirmed this by re-running `lossless_invariant.py --quick` on HEAD with the default (hardened) receiver through `run_one`: 2394 cells replayed, 1026 real, 0 mismatches. Output: `/tmp/claude-0/-home-user-my-project/46dade12-34d7-5f2d-a590-dd3f35c40afe/scratchpad/li_quick2.csv`.
- **The hardened receiver is the one used in the main sweep, but the Q2 section does not say so.**
  - `run_one` builds `make_rx(...)` with the defaults (`bind_slot=True`, `pend_cap=32`) for the operating point, the minimum budget, the joiner, the invariant and UDP (`run_proto.py:71-72`; `udp_link.py:81`).
  - "hardened = the shipped receiver" is stated only in the attacker section (`summarize.py:756-757`). The Q2 operating-point and H5 sections do not say which receiver produced them (n3).
- **Per-slot-capacity layout.**
  - `Alloc.layout` / `lossless_set` are unchanged since loop 1. The EDF, augmenting-path placement, and the ≤255-symbols and capacity limits are sound as reported in loop 1.
  - The smoke data show bytes per slot ≤ the average slot capacity in every cell (max utilisation 1.000).
- **Lossless invariant: the "symbolic receiver" is not independent of `lossless_set`** (n1).
  - `replay()` decides "decoded" from the layout's own `L.slots`, not from the sender's frames.
  - Its frag, Merkle and chain rules are a transcription of `lossless_set`: the same `cap >= mand` frame test (`lossless_invariant.py:63`), the same key-slot rule (`:83`), and the same `d < 1 + DELTA` cut-off.
  - A shared conceptual error would pass both. The independent check is the REAL part: real sender bytes and real receivers. It covers all modes, profiles and budgets for 6 schemes in the full run, but only 3 in QUICK, and never SLH-DSA.

## Part 2: areas not covered in loop 1

- **(a) Fair budget: sound.**
  - All modes of a (profile, scheme, budget) share one `Plan` (`run_proto.py:42-49`): `cap_reg = B - digest`, and `cap_cert = max(0, B - P - S)` with the certificate metadata counted as 0 B (a lower bound, TODO-RESULT).
  - `put()` asserts the per-slot cap. Symbol size is chosen by the same `choose_s` rule for every mode.
  - `chain_r2`'s rho = 2 is a stated variant, not a tuning difference.
  - Smoke data: `proto_alloc` caps are identical across modes; measured utilisation is ≤ 1.0 everywhere.
- **(b) CI and verdict logic: mostly sound.**
  - Pairing is by seed after averaging each arm over the class's conditions (`summarize.py:369-399`). The same seed means the same mask for every mode in a condition.
  - The t table `T975` (`:54-55`) matches t_0.975 for df 1-30, and df = n - 1.
  - Best-competitor selection on the same data matches `hypotheses.yaml`. The minimum effects come from the yaml.
  - Issues: N3 (H7 decision changed), n4 (NaN pairing), n5 ("decidable" includes "unclear"), n6 (H4 by construction).
  - `git log` shows `hypotheses.yaml` changed only in 96d1dc7 and 6ad24e7, and the 6ad24e7 diff adds attacker settings only.
- **(c) Mask independence: sound.**
  - `make_mask` seeds a `SeedSequence` with (seed, p, burst, `stream_id(profile, scheme, condition)`) (`lossform.py:120-130`).
  - Smoke data: exactly 1 mask per (profile, scheme, condition, seed) cell, shared by all modes, and distinct across schemes.
  - The joiner's rng is per (profile, scheme, seed), so it is paired across modes.
  - Attacker slot selection is not paired across modes, because `arng` consumption depends on field sizes. Harmless: retention is a within-mode ratio, and baseline and hardened share the same injection dict.
- **(d) Minimum budget reuses the operating-point masks: no directional bias for H5.**
  - Chain and fragmentation see identical masks at every budget (common random numbers), so the comparison stays paired.
  - The 1.0x grid point is literally the operating-point run (seeds 0-9).
  - Two consequences, disclosed only in part (n7):
    - H5 is not independent evidence from H1.
    - H5 has no uncertainty: a mean over 10 fixed masks against the target, and `minbps` takes the smallest passing grid point even if a larger budget fails.
  - Best-of-8 competitor selection on the same masks favours fragmentation, which is conservative for the chain, as the yaml states.

## Findings (new in loop 2)

| id | severity | file:line | what is wrong | how confirmed | suggested fix |
|---|---|---|---|---|---|
| N1 | major | `modes.py:604-611`; `negative_tests.py:198`; `summarize.py:206`, `:836` | **Slot binding uses an oracle.** `deliver()` compares the message seq with the harness's true slot index g, which is unaffected by `clock_ms`. A real receiver gets g either from its own clock (then binding drops all honest frames once the offset exceeds a slot) or from an unauthenticated link-layer counter (SFN or slot number) that the attacker can influence. A receiver that knows the exact slot index also contradicts the clock-offset model being swept. The binding also needs the application to carry a 32-bit slot number in its first 4 bytes; that is true of `make_app`, not of real SIB1/BSM payloads, and those bytes are not charged. So R4d ("the forgery is dropped at any clock offset") and "with it on, the forgery is dropped at every offset" (`summarize.py:836`) overstate a real-world defence. R4d is counted as a reject test. H6 itself is measured with binding off and is unaffected. | Code reading: `self.t` uses `clock_ms`, the bind test uses the raw `g`. | Derive g from the receiver clock (`floor((t + clock_ms)/T)`), or state the counter as an authenticated or trusted input. Drop "at any clock offset". Move R4d to a documented assumption-dependent test. Charge the slot-number bytes, or state them. |
| N2 | major | `modes.py:825`, `:843-847` (chain (e,i) unchecked against g); frag symbol `age` within the span; Merkle path frames for any leaf of batch b; key (ke, ki) (`:917`); `run_proto.py:186-225` | **Cross-slot pre-filling survives binding** (residual of loop-1 M1). Binding only checks the application seq. A bogus frame in slot g can carry g's own honest application while it claims a future chain (e', i') and fills its 32 tag candidates. It can also fill symbol candidates (3 per index) of a frag object still inside its span, path candidates (3) of a Merkle leaf, or key-stash candidates (2). `summarize.py:828` ("slot binding removes candidates that arrive in a slot other than the message's own") is therefore false for every field except the application. The harness's "early" order cannot detect this: `bogus(S, g, ...)` puts the target slot's seq into slot g-1, so binding drops it trivially. The hardened "early" retention therefore measures nothing. | Code reading of the unpacking and caps; the `bogus()` construction. | Reject chain frames with (e, i) ≠ (g // E, g % E + 1). Bind symbol age, path leaf and key index to what slot g may legitimately carry. Add an "early" variant that uses the attacking slot's own application. Correct line 828. |
| N3 | major | `summarize.py:770-796`, `:139`; `hypotheses.yaml:61` | **H7 is now decided under the strong pre-filling attacker.** The pre-registered criterion says "the pre-registered criteria H7 / H8 use 1 (bogus frame per attacked slot)" (yaml line 61, still present). The process note (`:139`) says "without changing any criterion". The change is in the conservative direction, but it is a change in the decision rule after results, and it is presented as none. | Diff 96d1dc7..HEAD plus the verdict code. | Report the pre-registered H7 (weak attacker, hardened and baseline) as the verdict and the strong attacker as descriptive, or declare the rule change explicitly with its reason. |
| n1 | minor | `lossless_invariant.py:10`, `:40-89` | The "symbolic receiver" is not independent of `lossless_set`: same rules, and it reads the layout's own slot lists. | Code comparison. | Rephrase the docstring and summary. Derive "decoded" from the sender's actual frames, which `build` already exposes. |
| n2 | minor | `results/raw/*quick-smoke*.csv` | All smoke CSVs are tagged 64485a3 with dirty=1, not HEAD 6ad24e7. Which receiver produced them cannot be established. | `git_commit` columns. | Re-run (QUICK) at a clean HEAD before `summary.md` is used. |
| n3 | minor | `summarize.py:310-330`, `:636-660` | The Q2 operating-point and H5 sections do not state that the hardened receiver (bind_slot on, 32 tag candidates) produced them. | Grep. | State it in the Q2 header and the assumptions table. |
| n4 | minor | `summarize.py:369` (`PER = ...mean()`) | Per-seed averaging skips NaN per arm. For `air_bytes_per_auth` (NaN when nothing is authenticated) the chain and the competitor can be averaged over different condition sets, which breaks the pairing for H2. | Code reading. | Average only over conditions where both arms are defined, or treat the metric as a ratio of sums. |
| n5 | minor | `summarize.py:402-411` | The denominator of the verdict rule includes "unclear" groups. "Fraction of decidable groups" (yaml) more naturally excludes them. | Code vs yaml. | State the rule, or exclude "unclear". |
| n6 | minor | `summarize.py:479-505` | H4 is refuted by construction for the chain. The C-V2X need is 1 slot (100 ms // 100 ms), and the chain's minimum delay is d + 1 = 3 slots (printed, but still treated as a tested verdict). | Arithmetic. | Present H4 as a design consequence, as round-3 Major 2 asked for H2c. |
| n7 | minor | `summarize.py:644-646`; `run_proto.py:291-296` | H5 has no uncertainty (mean of 10 shared masks against the target). `minbps` takes the smallest passing budget even when a larger one fails. The 1.0x point duplicates the operating-point runs. | Code reading. | Require monotone success (smallest B from which all larger grid points pass). Report a seed bootstrap. Say H5 is not independent of H1. |
| n8 | minor | `modes.py:843-847` | `pend` grows without bound: any frame can create lists for arbitrary 16-bit epochs and indices. This is memory and CPU growth under injection, and it is not reflected in H8. | Code reading. | Accept only (e, i) bound to the slot (N2), or bound the open epochs. |

## Checked and found sound (loop 2)

- Prompt forger, stamp models and guard variant; the analytic thresholds match the rule.
- Mutation controls C4m1 and C4m2.
- Stale blobs cost one try.
- Honest traffic under bind_slot: invariant 0 mismatches at HEAD.
- Equal per-slot budget and identical tuning rule for all modes.
- t quantiles and seed pairing.
- Mask independence across (profile, scheme, condition), with paired masks within a cell.
- Minimum-budget reuse of masks does not favour the chain.
