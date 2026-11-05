# EMBER experiments: how to reproduce

Python venv: `$SP/venv` (pqcrypto 1.0.0, cryptography 50.0.2, numpy, scipy, pandas, matplotlib, numba 0.68.1, pytest);
native: OpenSSL 3.5.4 built in `$SP/opt/ossl35` (recipe: `paper/scout/feasibility.md`). `oqs` is never imported.
`SP=/tmp/claude-0/-home-user-my-project/4a27d5c9-46a1-5d35-98ec-9a4e85dfb968/scratchpad`.

```bash
cd paper/experiments
QUICK=1 OUT=$SP/qres bash run_all.sh      # smoke run into a scratch directory
bash run_all.sh                            # full run: tests native bench sims figs (or name stages)
```
Simulations run at idle priority (`chrt -i 0`): they are timing-insensitive. Timing benchmarks are pinned to core 2.

## Code map
| Path | What |
|---|---|
| `ember/th.py` | tweakable hash; 26-B tweak `ctx|kid|epoch|type|level|index|tenant` (tenant added to the spec's 22 B for pooled trees) |
| `ember/merkle.py` | pairwise tree with promotion of unpaired nodes; auth paths; streaming treehash for large N |
| `ember/token.py` | canonical claims, EMBER / per-token wire formats, signed URL / cookie |
| `ember/signers.py` | all signers (B1-B9 roots and per-token), B10 MultiMAC, B11 DelegatedEd25519, B12 KemWrappedHMAC, B13 MTLMode, VerifyCache |
| `ember/issuer.py`, `ember/edge.py` | issuer (epochs, period bundles, revocation deltas, pad-to-2^d) and edge verifier (root cache, negative cache, staple, bundles, skew) |
| `ember/controller.py` | fixed / work-conserving / adaptive epoch policies (kernels in `sim/fleet_mc.py`) |
| `baselines/pertoken.py` | per-token scheme wrapper and factory for B1-B12, B5v/B6v, B5c/B6c |
| `tests/test_ember.py` | 51 correctness / forgery-rejection tests; `tests/gen_vectors.py` -> `tests/vectors.json` (shared with the Go port) |
| `bench/bench_primitives.py` | E1 (Python), A1 note |
| `bench/native/{evp_sigbench,pathverify,issuerbench}.c`, `run_native.sh`, `aggregate_native.py` | E1n primary native timings |
| `bench/bench_tokens.py` | E2/E2+ sizes, verify, issuer throughput, model check |
| `bench/fit_analysis.py` | E3 |
| `sim/workload.py`, `sim/model.py`, `sim/fleet_mc.py`, `sim/engine.py`, `sim/run_sim.py` | E5 fleet Monte Carlo (numba kernel) and experiments |
| `sim/des.py` | event-driven DES for the internal-consistency check |
| `sim/dos.py` | E7 |
| `sim/proto_mc.py` | fleet_mc kernel at the E8 P3 configuration -> `sim_proto_mc.csv` (consumed by `proto/validate.py`) |
| `plots/make_figures.py`, `plots/make_tables.py` | all figures / tables |

## Figure / table -> script -> CSV
| Output (`results/figures`, `results/tables`) | Script | CSV |
|---|---|---|
| fig2_token_sizes | make_figures.fig2 | token_sizes.csv (bench_tokens) |
| fig3_size_vs_N | fig3 | token_sizes.csv, native_issuer_agg.csv, native_sig_agg.csv |
| fig4_verify_cost | fig4 | token_verify.csv, native_sig_agg.csv, native_pathverify_agg.csv |
| fig5_delta_tradeoff | fig5 | sim_delta_sweep.csv |
| fig6_controller_24h | fig6 | sim_controller_ts.csv |
| fig7_dissemination | fig7 | sim_dissem.csv |
| fig8_e2e_cdf | fig8 | sim_e2e_latency.csv |
| fig9_sens_heatmap | fig9 | sim_sens.csv |
| fig10_wire_bytes / fig11_proto_capacity / fig12_proto_validation | fig_wire / fig_proto / fig_proto_validate | wire_bytes.csv / proto_capacity.csv / proto_validate.csv (Experimenter B; skipped if absent) |
| tab2_primitives | make_tables.tab2 | micro_primitives.csv, native_sig_agg.csv, native_pathverify_agg.csv |
| tab3_fit | tab3 | fit.csv |
| tab4_simparams | tab4 | sim_params.json |
| tab5_controller | tab5 | sim_controller_summary.csv (-> controller_paired.csv) |
| tab6_trust | tab6 | token_sizes.csv, native_*_agg.csv, sim_dissem.csv |
| tab7_validate | tab7 | sim_validate.csv |
