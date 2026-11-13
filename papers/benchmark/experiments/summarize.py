#!/usr/bin/env python3
"""Build results/summary.md, figures (PDF) and derived CSVs from results/raw/*.csv.  Every number in summary.md is computed here; every
threshold and decision rule is read from hypotheses.yaml (fixed before the results were seen)."""
import glob
import math
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "results"); RAW = os.path.join(RES, "raw")
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "lib")); sys.path.insert(0, HERE)
import pqsig.accounting as acc                      # noqa: E402
import pqsig.proto.modes as MO                      # noqa: E402
from pqsig.common import code_state                 # noqa: E402
from pqsig.schemes import lowest_level              # noqa: E402

L = []


def w(s=""): L.append(s)
def md(df, fmt=".4g"): return df.to_markdown(index=False, floatfmt=fmt)
def rd(n): return pd.read_csv(os.path.join(RAW, n))
def opt(n):
    p = os.path.join(RAW, n)
    return pd.read_csv(p) if os.path.exists(p) else None


MN = os.environ.get("MACHINE_NAME", "cloud-smoke")
Y = yaml.safe_load(open(os.path.join(HERE, "profiles.yaml"))); PROF = Y["profiles"]; COM = Y["common"]
HY = yaml.safe_load(open(os.path.join(HERE, "hypotheses.yaml")))
sizes = rd("sizes_declared.csv"); pq = sizes[sizes.family_kind == "pq"]
timing = rd(f"oqs_timing_{MN}.csv"); classical = rd(f"classical_timing_{MN}.csv"); sc = rd("scoring_all_levels.csv")
res = rd(f"proto_results_{MN}.csv"); minb = rd(f"minbudget_{MN}.csv"); att = rd(f"attack_{MN}.csv"); alloc = rd(f"proto_alloc_{MN}.csv")
xchk = rd(f"loss_crosscheck_{MN}.csv"); neg = rd(f"negative_tests_{MN}.csv")
udp = opt(f"udp_smoke_{MN}.csv"); phases = opt(f"run_phases_{MN}.csv"); rt = opt(f"proto_runtime_{MN}.csv"); ptime = opt(f"proto_pairtime_{MN}.csv")
PNAMES = list(PROF)
SIGPROF = [p for p in PNAMES if PROF[p].get("role", "signature") == "signature"]
PROTO_P = sorted(res.profile.unique(), key=lambda p: PNAMES.index(p))
LAB = {p: p + (" [ceiling-based]" if PROF[p]["basis"] == "ceiling-based" else "") + (" [key space]" if PROF[p].get("role") == "public-key-space" else "") for p in PNAMES}
PQS = [q for q in MO.PQ_IDS if q in set(res.pq)]
CH = HY["contrast"]["chain_mode"]; COMP = HY["contrast"]["competitor_modes"]
CLASSES = HY["contrast"]["loss_classes"]; CI = HY["contrast"]["ci_level"]; EFF = HY["effects"]; VR = HY["verdict_rule"]
D_AN = HY["deadlines"]["analysis_periods"]
SLOT_MS = {p: int(round(PROF[p]["proto"]["slot_period_s"] * 1000)) for p in PROTO_P}
NEED = {p: (HY["deadlines"]["need_ms"].get(p) if isinstance(HY["deadlines"]["need_ms"].get(p), dict) else None) for p in PROTO_P}
T975 = [12.706, 4.303, 3.182, 2.776, 2.571, 2.447, 2.365, 2.306, 2.262, 2.228, 2.201, 2.179, 2.160, 2.145, 2.131, 2.120, 2.110, 2.101, 2.093, 2.086,
        2.080, 2.074, 2.069, 2.064, 2.060, 2.056, 2.052, 2.048, 2.045, 2.042]


def tcrit(df):
    """two-sided 95% Student t critical value (table for df <= 30, 1.96 beyond; the CI level is fixed at 0.95 in hypotheses.yaml)"""
    return T975[df - 1] if 1 <= df <= 30 else 1.96


assert abs(HY["contrast"]["ci_level"] - 0.95) < 1e-9
LAGC = [f"lag_{j}" for j in range(1, 21)]

# ---------------------------------------------------------------- derived tables (Part A / Q1)
reps = pq[pq.is_rep]; main_cls = lowest_level(reps)
sc["lowest"] = sc.class_id.isin(set(main_cls.class_id))
main = sc[sc.lowest & (sc.family_kind == "pq")]; stf = sc[sc.family_kind == "stateful"]
main_all = pd.concat([main, stf])
main_all.to_csv(os.path.join(RES, "main_table_lowest_level.csv"), index=False)
sc.to_csv(os.path.join(RES, "appendix_all_levels.csv"), index=False)

# ---------------------------------------------------------------- unconditional delay metrics (per run)
def within(df, D):
    D = np.asarray(D) if not np.isscalar(D) else np.full(len(df), D)
    cs = np.cumsum(df[LAGC].values, axis=1)
    idx = np.clip(D, 1, 20) - 1
    return cs[np.arange(len(df)), idx] / df.received.values


def add_metrics(df):
    df = df.copy()
    rc = df.received.replace(0, np.nan)
    df["within_an"] = within(df, D_AN)
    cs = np.cumsum(df[LAGC].values, axis=1)
    j = np.arange(1, 21)
    auth_le = cs[:, D_AN - 1]
    num = (df[LAGC].values[:, :D_AN] * j[:D_AN]).sum(axis=1) + D_AN * (df.received.values - auth_le)
    df["rmst_ms"] = num / rc.values * df.slot_period_ms.values          # restricted mean time to authentication, unauthenticated censored at the deadline
    need_slots = df.profile.map(lambda p: int(NEED[p]["ms"] // SLOT_MS[p]) if NEED.get(p) else 0)
    df["need_slots"] = need_slots
    ws = np.array([cs[i, n - 1] / df.received.values[i] if n > 0 else np.nan for i, n in enumerate(need_slots)])
    df["within_need"] = ws
    df["air_bytes_per_auth"] = pd.to_numeric(df.air_bytes_per_auth, errors="coerce")
    df["bytes_per_s_air"] = df.air_bytes / (df.N_meas * df.slot_period_ms / 1000.0)
    return df


res = add_metrics(res); minb = add_metrics(minb)

# ---------------------------------------------------------------- header, provenance
commit_now, dirty_now = code_state()
tags = pd.concat([d[["machine", "date", "git_commit", "git_dirty"]] for d in (sizes, timing, classical, sc, res, minb, att, alloc, xchk, neg)
                  if "git_dirty" in d]).drop_duplicates()
tags["date"] = tags.date.str[:10]
tags = tags.drop_duplicates(["machine", "date", "git_commit", "git_dirty"])
smoke = (tags.machine == "cloud-smoke").all()
w("# benchmark: results summary, experiments pass 4 (generated by experiments/summarize.py from results/raw/*.csv)")
w()
w(f"**Code commit (git rev-parse HEAD at summarisation): `{commit_now}`; working tree {'DIRTY (uncommitted code changes under lib/ or experiments/)' if dirty_now else 'clean'}.** "
  "Every CSV row carries `machine`, `date`, `git_commit` and `git_dirty`; the distinct tags found in the CSVs are:")
w(); w(md(tags)); w()
if smoke:
    w("**All runs in this summary are smoke tests (`machine: cloud-smoke`, a shared cloud VM, QUICK settings unless the run table says otherwise). No publication numbers. All verdicts below are PROVISIONAL. See 'Runs still needed'.**")
else:
    w(f"Machines in this summary: {', '.join(sorted(tags.machine.unique()))}. Rows tagged `cloud-smoke` (if any) are smoke tests.")
w()
if (tags.git_dirty == 1).any():
    w("Rows with `git_dirty = 1` were produced from an uncommitted tree: they are not traceable to a commit and must be regenerated from a clean commit before use.")
    w()
nseeds_o = int(res.groupby(["profile", "pq", "mode", "cond"]).seed.nunique().min()); nseeds_m = int(minb.groupby(["profile", "pq", "mode", "cond", "B_mult"]).seed.nunique().min())
nseeds_a = int(att.groupby(["profile", "pq", "mode", "attack", "param"]).seed.nunique().min())
w(f"Protocol experiments: operating point {len(res)} rows (seeds per cell >= {nseeds_o}), minimum-budget sweep {len(minb)} rows (seeds >= {nseeds_m}), active attacker {len(att)} rows (seeds >= {nseeds_a}).")
w()
w("**Standard-error rule.** Across seeds the spread is the sample standard deviation; the uncertainty of a mean over n seeds is SE = sd / sqrt(n) and confidence intervals are Student-t 95% intervals over seeds "
  "(`ci_method` in `hypotheses.yaml`). Seeds are independent loss masks (below). The closed-form cross-check uses z = diff / max(SE over seeds, binomial SE) and excludes lossless cells.")
w()

# ---------------------------------------------------------------- hypotheses (restated, criteria from hypotheses.yaml)
w("## Questions and hypotheses (criteria fixed in `experiments/hypotheses.yaml` before looking at results)")
w()
w("- **Q1 (fit).** Which (scheme, mode) pairs fit one message of each profile's authentication budget? (unchanged, Part A/Q1)")
w("- **Q2 (native-rate protocols).** With real cryptography and byte framing, ONE application message per slot at the channel's native rate (no repetition), loss that is independent per (profile, scheme, condition): how does a PQ-anchored TESLA-style chain compare with the best per-message fragmentation mode, and with Merkle batches, in share, bytes, unconditional delay, minimum budget, and under an active attacker?")
w("- **Q3 (size vs time).** Is signature size or timing tail binding (unchanged, Part Q3).")
w()
hy = pd.DataFrame([{"id": k, "metric": v.get("metric"), "statement": v["text"]} for k, v in HY["hypotheses"].items()])
w(md(hy)); w()
w("Process note: the criteria and thresholds below were written before the first smoke run and have not been changed since. After the first smoke run the following were ADDED (no criterion changed): iid 0.2 in the QUICK operating conditions (needed to pair burst and i.i.d. loss), a second injection intensity (4 bogus frames per attacked slot, descriptive only), and the late single-frame replay test R5b / control C5b, which was added because the first smoke run showed Merkle receivers accepting stale leaves after a batch root had been verified (a freshness bug in the receiver, fixed in `modes.py`; the first run's H6 verdict was REFUTED because of it).")
w()
w(f"Decision rule (from `hypotheses.yaml`): groups are (profile, scheme, loss class), the chain variant is `{CH}`, the competitor is the best of {len(COMP)} fragmentation modes ({', '.join(COMP)}) "
  f"selected per group on the same data (conservative for the chain). Group outcome: {VR['group_outcome']}. Hypothesis verdict: supported if >= {VR['supported_fraction']:.0%} of decidable groups are 'chain better' and <= {VR['worse_tolerance']:.0%} are 'chain worse'; "
  f"refuted if >= {VR['refuted_fraction']:.0%} are 'chain worse'; otherwise inconclusive. {VR['combine_classes']}. {VR['competitor_infeasible']}. "
  f"Minimum effects: share {EFF['share_abs']}, bytes {EFF['bytes_rel']:.0%}, delay {EFF['delay_rel']:.0%}, budget ratio {EFF['budget_ratio_low']} / {EFF['budget_ratio_high']}.")
w()

# ---------------------------------------------------------------- traffic model + assumptions
w("## Traffic model (one table)")
w()
tm_rows = []
for p in PROTO_P:
    pr = PROF[p]["proto"]; B = PROF[p]["auth_budget"]["bytes"]
    pl = MO.Plan(pr["slot_period_s"], B, pr["digest_bytes"], pr["app_bytes"], pr["cert_every"], 0, COM["protocol"]["epoch_windows_E"], COM["protocol"]["measured_epochs"], COM["protocol"]["key_delay_slots_d"], COM["protocol"]["tail_slots"])
    tm_rows.append({"profile": LAB[p], "native message rate": f"1 per {int(pr['slot_period_s'] * 1000)} ms ({1 / pr['slot_period_s']:.2f} Hz)", "application message B (not charged)": pr["app_bytes"],
                    "digest B in slot": pr["digest_bytes"], "auth budget B per slot": B, "channel budget B/s": round(B / pr["slot_period_s"], 1),
                    "certificate slot": (f"every {pr['cert_every']}th slot, auth capacity max(0, B - P - S)" if pr["cert_every"] else "none"),
                    "repetition of the message": "none (sent once in its own slot)", "measured messages per run": pl.N, "warm-up / tail slots": f"{pl.W0} / {COM['protocol']['tail_slots']}",
                    "source": pr["app_source"]})
w(md(pd.DataFrame(tm_rows))); w()
w("A message whose own slot is lost cannot be authenticated by any mode, so every share below is relative to RECEIVED messages (`received`); the fraction of messages delivered at all is in the CSV (`delivered_frac`). "
  "The pass-3 'repeat the message in all M slots' assumption is gone: a mode that cannot carry its authentication data within the slot budget at the native rate is reported as infeasible (below), not helped by repetition.")
w()
w("## Assumptions and design choices that drive the results (one table)")
w()
A_ = HY["attack"]
ass = [("tag length (chain MAC)", f"{MO.TAG_B} B (HMAC-SHA-256 truncated), key {MO.KEY_B} B, commitment {MO.COMMIT_B} B, Merkle node hash {MO.NODE_B} B", "128-bit symmetric strength is acceptable for NIST level 1; ML-DSA-44 is level 2, Falcon/MAYO/OV/SNOVA/SLH-DSA-128s level 1"),
       ("anchor allocation", "the anchor uses ALL bytes left in the slots of its epoch after tag, key (and commitment): n = min(255, free bytes / symbol); chain_r2 caps the anchor at 2x the source symbols (rho = 2)", "driver of chain bytes and anchor share; the minimum-budget sweep removes the dependence"),
       ("disclosure delay d", f"{COM['protocol']['key_delay_slots_d']} slots (key of message i released at the start of slot i + d); receiver sync bound {MO.DELTA_SLOTS} slot", "d = 2 leaves one slot of slack; chain delay >= (d + 1) slots by construction"),
       ("epoch length E", f"{COM['protocol']['epoch_windows_E']} slots", "assumed"),
       ("anchor fresh / lead", "chain: anchor of epoch e inside epoch e; chain_lead(_cont): inside epoch e-1; epoch 0 has no anchor in the lead modes (warm-up, excluded)", "design of the variants"),
       ("fragmentation spans", "W = 1, 2, 4, 8 slots (frag_rep/frag_mds), W = 1, 4 (hybrids); the best frag mode per group is the competitor", "W is a delay/robustness trade-off chosen by the best-of selection"),
       ("symbol size rule", "s maximises the design-point reliability P[>= k of n symbols] at slot loss 0.2 (MDS assumption), then larger s; same rule for every mode", "design choice"),
       ("Merkle", "path hashes 16 B, each path sent in 2 slots, batch signature MDS-coded over the n slots after the batch", "design choice"),
       ("freshness (bytes charged)", f"frag/hyb: seq {MO.SEQ_B} B + timestamp {MO.TS_B} B inside the signed blob; Merkle: batch id {MO.SEQ_B} B + timestamp {MO.TS_B} B per batch; chain anchor: epoch id {MO.SEQ_B} B + epoch-start timestamp {MO.TS_B} B + schedule {MO.SCHED_B} B", f"added bytes are inside the blobs and therefore inside the accounting: frag/hyb +{MO.SEQ_B + MO.TS_B} B per message; Merkle +{MO.SEQ_B + MO.TS_B} B per batch = " + ", ".join(f"{(MO.SEQ_B + MO.TS_B) / n_:.2f} B/msg (n={n_})" for n_ in (4, 8, 16)) + f"; chain anchor +{MO.SEQ_B + MO.TS_B - 4 + MO.SCHED_B} B per epoch vs pass 3 = {(MO.SEQ_B + MO.TS_B - 4 + MO.SCHED_B) / COM['protocol']['epoch_windows_E']:.2f} B/msg"),
       ("replay / staleness", f"timestamps older than {MO.FRESH_SLOTS} slots or from the future (> {MO.DELTA_SLOTS} slot) are rejected; replay window {MO.RW} messages", "receiver policy"),
       ("pollution handling", f"up to {3} candidate symbols per index, decode-and-verify over subsets; at most {MO.A_MAX} failed signature verifications per object (Merkle {2 * MO.A_MAX}); {16} subset decodes", "no extra bytes; bound stated in the attacker section"),
       ("chain keys", "os.urandom(32) secret per build; never derived from a seed", "regression-tested (R8)"),
       ("loss", "i.i.d. per slot; Gilbert-Elliott (0 in Good, 1 in Bad, mean burst 3 / 5 / 10 slots, same stationary loss); independent mask stream per (profile, scheme, condition), paired across modes inside the cell", "assumed channel, collision-free"),
       ("burst lengths run", ", ".join(str(int(b)) for b in sorted(res[res.loss_model == "ge"].burst_len.unique())), "generated from the data"),
       ("deadlines", f"analysis deadline {D_AN} message periods for every profile (ASSUMED); stated latency need: " + "; ".join(f"{p}: " + (f"{NEED[p]['ms']} ms ({NEED[p]['source']})" if NEED[p] else "TODO-RESULT") for p in PROTO_P), "no source states a deadline for SIB1"),
       ("builds / seeds", f"{int(res.build_id.nunique())} builds per (profile, scheme, mode) ({int(res.groupby(['profile', 'pq']).build_id.nunique().min())} for slow signers); seeds vary the loss mask only (and the join slot), not the signatures", "stated limitation"),
       ("late joiner", "one join per seed at a uniformly random slot of epoch 1; time to first authenticated message", "operating-point rows only"),
       ("hybrid", "Ed25519 + PQ signature, both verified; hybrids are reported separately and are not in the 'best fragmentation' set", "design choice"),
       ("certificate", "PQ issuer = same scheme, metadata TODO-RESULT (0 B, lower bound); capacity of the certificate slot = max(0, B - P - S)", "profiles.yaml")]
w(md(pd.DataFrame(ass, columns=["choice", "value", "note"]))); w()
# ---------------------------------------------------------------- Part A
w("## Part A: sizes and timings (C, liboqs and OpenSSL)")
w()
nl = len(timing)
w(f"Sources: `raw/sizes_declared.csv`, `raw/oqs_timing_{MN}.csv` ({nl} schemes; default list = lowest-level class of each family plus all levels of ML-DSA, Falcon, MAYO, UOV, SNOVA and the pure SLH-DSA sets), "
  f"`raw/classical_timing_{MN}.csv` (Ed25519 and ECDSA P-256 measured in C through OpenSSL, backend `{classical.backend.iloc[0]}`). The Python classical timings are gone.")
w()
n_raw = len(pq); n_cls = pq.class_id.nunique(); n_main = main_cls.class_id.nunique()
w(f"liboqs {pq.liboqs_version.iloc[0]}: {n_raw} signature parameter sets enabled, {n_cls} distinct (family, level, pk size, signature size) classes, {n_main} at the lowest level of their family (used in the main tables).")
w()
tm = timing.drop(columns="family").merge(pq[["scheme", "class_id", "claimed_nist_level", "family", "sig_declared", "length_public_key"]], on="scheme")
tm_main = tm[tm.scheme.isin(set(main_cls.scheme)) | tm.scheme.isin(MO.PQ_IDS)]
cols = ["scheme", "claimed_nist_level", "iterations", "length_public_key", "sig_declared", "sign_median_us", "sign_p95_us", "verify_median_us", "verify_p95_us"]
w("Timing of the lowest-level class representatives and the protocol-experiment schemes (x86 VM; rows with iterations < 100 have no usable p95/p99):"); w()
w(md(tm_main[cols].sort_values(["claimed_nist_level", "scheme"]))); w()
cl = classical[["scheme", "backend", "iterations", "pk_bytes", "sig_bytes_max", "sign_median_us", "sign_p95_us", "verify_median_us", "verify_p95_us"]]
w("Classical baselines (OpenSSL, C):"); w(); w(md(cl)); w()

# ---------------------------------------------------------------- Q1
w("## Q1: which (scheme, mode) pairs fit each profile")
w()
w("Sources: `raw/scoring_all_levels.csv` (all classes; appendix), `results/main_table_lowest_level.csv` (lowest level per family), `experiments/profiles.yaml`. "
  "**Headers marked [ceiling-based] have no authentication-only budget in their source: budget = payload ceiling minus the stated overheads (one rule for both C-V2X ceilings), so the verdict is conditional on that derivation.**")
w()
w("Byte-accounting formulas (`lib/pqsig/accounting.py`):"); w(); w("```"); w(acc.__doc__.strip()); w("```"); w()
w("**OSNMA (fixed).** Signatures are scored only against the DSM-KROOT signature space (`osnma_kroot158`, 158 B derived). Public keys are scored only against the DSM-PKR key space (`osnma_pkr_keys`, 76 B derived = (1632-1024) bit / 8). The former 'PKR as signature budget' column is removed.")
w()
rows = []
for (f, m), g in main_all[main_all["mode"].isin(["full", "hybrid", "full_cert_pq", "full_cert_cl", "full_cert_pk"])].groupby(["family", "mode"]):
    r = {"family": f, "mode": m}
    for p in SIGPROF:
        gg = g[g.profile == p]
        r[LAB[p]] = f"{int(gg.fits.sum())}/{len(gg)}" if len(gg) else "n/a"
    rows.append(r)
w("**Fit counts (classes fitting one message / classes in the family; lowest level per family; LMS/XMSS literature rows included).** `full_cert_pq` = PQ issuer (metadata TODO-RESULT, 0 used = most favourable); `full_cert_cl` = the source's classical-issuer case, shown separately; `full_cert_pk` = bare key (Remote ID endorsement, DNSKEY). Chain is not in this table (see the join-time table).")
w(); w(md(pd.DataFrame(rows))); w()
tot = main[main["mode"].isin(["full", "hybrid", "full_cert_pq", "full_cert_cl", "full_cert_pk"])].groupby(["profile", "mode"]).fits.agg(["sum", "count"]).reset_index()
tot["fit"] = tot["sum"].astype(int).astype(str) + "/" + tot["count"].astype(str)
w("Totals over the lowest-level liboqs classes (LMS/XMSS excluded):"); w()
w(md(tot.pivot(index="mode", columns="profile", values="fit").reset_index()[["mode"] + [p for p in SIGPROF if p in set(tot.profile)]].rename(columns=LAB))); w()
cert = main[main["mode"] == "full_cert_pq"]
if len(cert):
    cc = cert.groupby("profile").agg(classes=("fits", "size"), fit_meta0=("fits", "sum"), fit_meta41=("fits_meta41", "sum"), fit_meta73=("fits_meta73", "sum")).reset_index()
    cc["profile"] = cc.profile.map(LAB)
    w("PQ-issuer certificate fits (full_cert_pq), recounted, with the metadata sensitivity (metadata is TODO-RESULT; columns are the counts at 0, 41 and 73 B):"); w(); w(md(cc)); w()
    clz = main[main["mode"] == "full_cert_cl"].groupby("profile").agg(classes=("fits", "size"), fit=("fits", "sum")).reset_index()
    clz["profile"] = clz.profile.map(LAB)
    w("The source's classical-issuer case (full_cert_cl, certificate = P + 105 B), separately labelled:"); w(); w(md(clz)); w()
    ex = main[(main.profile == "cv2x_j3161") & main["mode"].isin(["full_cert_pq", "full_cert_cl"]) & main.scheme.isin(MO.PQ_IDS)]
    w("Margins B - x (bytes; negative = over budget) for the protocol schemes on the J3161 ceiling, certificate cases:"); w()
    w(md(ex.pivot_table(index="scheme", columns="mode", values="margin_bytes").reset_index())); w()
kd = main[main["mode"] == "key_delivery"]
w(f"**OSNMA key delivery (public key vs the {PROF['osnma_pkr_keys']['auth_budget']['bytes']} B DSM-PKR key space):** {int(kd.fits.sum())}/{len(kd)} lowest-level classes fit: " + (", ".join(sorted(kd[kd.fits].scheme)) or "none") + ".")
w()
fl = main[(main["mode"] == "full") & (main.profile.isin(SIGPROF))]
tab = fl.assign(cell=lambda d: d.msgs_needed.astype(str) + " msg / " + d.frames_per_msg.astype(str) + " fr / " + d.ttfa_s.map(lambda v: "n/a" if pd.isna(v) else f"{v:.3g} s") + " / margin " + d.margin_bytes.astype(int).astype(str) + " B")
tab = tab.pivot_table(index=["family", "scheme", "sig_declared", "pk_bytes"], columns="profile", values="cell", aggfunc="first").reset_index()[["family", "scheme", "sig_declared", "pk_bytes"] + SIGPROF].rename(columns=LAB)
w("**Full signature: messages needed / frames / time to the last fragment (no loss) / margin B - x.**"); w(); w(md(tab)); w()
w("**Chain: judged by join time against an assumed per-profile deadline, not by a fit count** (its 32 B steady cost always fits, so a fit count carries no information). Static join time = time to receive (profiles without a stated message rate, i.e. dns, are n/a) the fragmented anchor + d x period; the measured join times (with loss and anchor wait) are in Q2.")
w()
cj = main[(main["mode"] == "chain") & main.profile.isin(SIGPROF) & main.ttfa_s.notna()].copy()   # dns has no message rate (TODO-RESULT): n/a
cj["deadline_s"] = cj.profile.map(Y["join_deadline_s"]); cj["meets"] = cj.ttfa_s <= cj.deadline_s
cjs = cj.groupby("profile").agg(classes=("meets", "size"), meet_deadline=("meets", "sum"), join_s_min=("ttfa_s", "min"), join_s_median=("ttfa_s", "median"), join_s_max=("ttfa_s", "max"), deadline_s=("deadline_s", "first")).reset_index()
cjs["profile"] = cjs.profile.map(LAB)
w(md(cjs)); w()
st = sizes[sizes.family_kind == "stateful"]
w(f"LMS/XMSS: {len(st)} literature size-only rows (no timings; sizes flagged `derived`/`tabulated`/`not stated`; stateful, bounded signatures per key). They are in `main_table_lowest_level.csv`; only an LMS H=5 row exists (32 signatures per key = 3.2 s of 10 Hz BSMs), so 'LMS fits J3161' is operationally empty. H = 15/20 rows are TODO-RESULT.")
w()
# sensitivity: 437 strict
sens = PROF["cv2x_437"]["auth_budget"]["sensitivity_bytes"]
fm = main[(main["mode"] == "full") & (main.profile == "cv2x_437")]
w(f"Sensitivity of cv2x_437 to the 40 B frame overhead: full signatures fitting {PROF['cv2x_437']['auth_budget']['bytes']} B: {int(fm.fits.sum())}/{len(fm)}; fitting {sens} B (overhead inside 437): {int((fm.sig_declared <= sens).sum())}/{len(fm)}.")
w()
tc = {p: int(fl[(fl.profile == p) & fl.fits].shape[0]) for p in SIGPROF}
fl_cv = main[(main["mode"] == "full") & (main.profile == "cv2x_j3161")]
w(f"**Verdict Q1: answered (descriptive, supported as a table).** Full signatures fitting one message, of {n_main} lowest-level classes: " + "; ".join(f"{LAB[p]} {tc[p]}" for p in SIGPROF) +
  ". Certificate handling on J3161 (peak message = signature + full certificate): "
  + (f"{int(cert[cert.profile=='cv2x_j3161'].fits.sum())}/{len(cert[cert.profile=='cv2x_j3161'])} classes fit with a PQ issuer at metadata 0 versus {int(main[(main['mode']=='full_cert_cl')&(main.profile=='cv2x_j3161')].fits.sum())} with the source's classical issuer." if len(cert) else ""))
w()
fig, ax = plt.subplots(figsize=(9, 4)); fams = list(fl.family.unique())
for i, f in enumerate(fams):
    g = fl[fl.family == f]
    ax.scatter([SIGPROF.index(p) + (i - len(fams) / 2) * 0.08 for p in g.profile], g.share_of_budget, s=14, label=f)
ax.set_xticks(range(len(SIGPROF))); ax.set_xticklabels([LAB[p] for p in SIGPROF], rotation=20, fontsize=7)
ax.axhline(1, color="k", ls="--"); ax.set_yscale("log"); ax.set_ylabel("full signature / auth budget"); ax.legend(fontsize=6, ncol=2); fig.tight_layout()
fig.savefig(os.path.join(RES, "fig_q1_share.pdf")); plt.close(fig)
w("Figure `fig_q1_share.pdf` (source `raw/scoring_all_levels.csv`, lowest-level classes, full mode; headers marked [ceiling-based]).")
w()
bd = Y["baselines"]; dz = bd["darzi2026a_table3"]; jq = bd["junquera2023_falcon"]
w("Consistency checks of stated numbers (not reproductions from liboqs sizes; they divide the sources' own byte totals):"); w()
w(md(pd.DataFrame([
    {"check": "darzi2026a FN-DSA 2-level chain bytes / 293 B", "computed": math.ceil(dz["fn_dsa_2level_crypto_bytes"] / dz["auth_bytes_per_packet"]), "reported": dz["reported_packets"]["fn_dsa"]},
    {"check": "darzi2026a ML-DSA 2-level chain bytes / 293 B", "computed": math.ceil(dz["ml_dsa_2level_crypto_bytes"] / dz["auth_bytes_per_packet"]), "reported": dz["reported_packets"]["ml_dsa"]},
    {"check": "junquera2023assessment Falcon bits / 79 bit", "computed": math.ceil(jq["falcon_sig_bits"] / jq["bits_per_block_for_ds"]), "reported": jq["reported_blocks"]}]))); w()

# ================================================================ Q2 (native rate)
def condcls(m): return "iid" if m == "iid" else "burst"


res["cls"] = res.loss_model.map(condcls); minb["cls"] = minb.loss_model.map(condcls)
CONDS = list(dict.fromkeys(res.sort_values(["loss_model", "loss_p", "burst_len"]).cond))
w("## Q2: real protocols at the native message rate")
w()
w(f"Sources: `raw/proto_results_{MN}.csv` (operating point: the profile's real budget), `raw/minbudget_{MN}.csv` (budget sweep), `raw/attack_{MN}.csv` (active attacker), `raw/proto_alloc_{MN}.csv` (allocation), "
  "`lib/pqsig/proto/modes.py` (senders / receivers, docstring = traffic model, allocation rule and security rules), `lib/pqsig/proto/attacks.py`. "
  "A message counts as authenticated only if the receiver verified the received bytes (PQ signature / Merkle-root signature / anchor signature plus MAC-chain check, plus Ed25519 for hybrids) "
  f"and the freshness / replay checks passed. `false_accepts` (accepted bytes different from the sent bytes) over all operating-point rows: {int(res.false_accepts.sum())}; stale acceptances: {int(res.stale_accepted.sum())}.")
w()
w("**Modes** (names in the CSV): `frag_rep_wW` / `frag_mds_wW` (the message signature fragmented and sent over W slots starting at the message's slot, plain repetition or Reed-Solomon coded), "
  "`hyb_*` (Ed25519 + PQ signature), `merkle4/8/16` (batch signature, per-message authentication path sent in two slots after the batch, signature MDS-coded over the n slots after the batch), "
  "`chain` (TESLA-style chain: 16 B tag in the message's own slot, key released d slots later, anchor = commitment + signed schedule + timestamp, MDS-coded over the epoch), `chain_r2` (same, anchor redundancy bounded to 2x), "
  "`chain_lead` (anchor sent one epoch ahead), `chain_lead_cont` (as chain_lead plus continuity: the next commitment travels inside the MAC input, so an authenticated epoch bootstraps the next without its anchor).")
w()

# ---- independence
w("### Independent randomness")
w()
res["stream"] = res.mask_id.str.split("-").str[0]
n_ids = res.mask_id.nunique(); n_streams = res.stream.nunique()
shared = int(res.groupby("mask_id")[["profile", "pq"]].apply(lambda g: len(g.drop_duplicates())).max())
modes_per_mask = res.groupby("mask_id")["mode"].nunique()
w(f"Loss masks are drawn per (profile, scheme, loss condition, seed) from independent streams (`lossform.stream_id`). In `raw/proto_results_{MN}.csv` there are **{n_streams} independent (profile, scheme, condition) streams and {n_ids} distinct masks (stream x seed)**; "
  f"the maximum number of different (profile, scheme) pairs that share one mask is {shared} (pass 3: every profile and every PQ scheme shared the mask of a given seed, condition and M, which collapsed the 462 comparison cells to about 66 groups). "
  f"Each mask is shared by {int(modes_per_mask.min())}-{int(modes_per_mask.max())} modes (paired comparison inside the cell only). The effective number of independent groups for the per-scheme comparisons below is therefore "
  f"{res.groupby(['profile', 'pq', 'cls']).ngroups} (profile, scheme, loss class) groups x {nseeds_o} independent seeds. The minimum-budget and attacker runs reuse the same stream names (same cell = same mask), so they are not independent of the operating-point runs.")
w()

# ---- feasibility at native rate
A1 = alloc[alloc.B_mult == 1.0].copy()
A1["family"] = A1["mode"].map(lambda m: "best frag" if m in COMP else "hybrid" if m.startswith("hyb") else m)
fe = A1[A1.family.isin(["best frag", "hybrid", "merkle4", "merkle8", "merkle16", "chain", "chain_r2", "chain_lead", "chain_lead_cont"])].groupby(["profile", "pq", "family"]).feasible_frac.max().unstack()
fe = fe[[c for c in ["best frag", "hybrid", "merkle4", "merkle8", "merkle16", "chain", "chain_r2", "chain_lead", "chain_lead_cont"] if c in fe]].reset_index()
fe["profile"] = pd.Categorical(fe.profile, PROTO_P); fe["pq"] = pd.Categorical(fe.pq, PQS); fe = fe.sort_values(["profile", "pq"])
w("### Native-rate feasibility (a result)")
w()
w(f"Fraction of objects of the mode that can be carried at the profile's real budget (`feasible_frac` in `raw/proto_alloc_{MN}.csv`, B_mult = 1; maximum over the modes of the family; 0 = the scheme cannot keep up at the native rate, 1 = every object fits). "
  "Without the pass-3 repetition assumption a signature that is larger than the free bytes per slot cannot be sent per message at all.")
w(); w(md(fe, ".2f")); w()
npairs = len(fe)
no_frag = int((fe["best frag"] == 0).sum()); no_chain = int((fe["chain"] == 0).sum()); no_merk = int((fe["merkle8"] == 0).sum())
part = A1[A1["mode"].isin(MO.MODES) & (A1.feasible_frac > 0) & (A1.feasible_frac < 1)]
w(f"Of {npairs} (profile, scheme) pairs, **no per-message fragmentation mode is feasible in {no_frag}**, the Merkle-8 batch mode is infeasible in {no_merk} and the chain in {no_chain}. "
  f"Individual modes are only partially feasible (0 < fraction < 1) in {len(part)} (profile, scheme, mode) configurations: on C-V2X the certificate-bearing slot has capacity max(0, B - P - S), which is 0 for most schemes at these budgets, so a mode that needs the message's own slot (W = 1, the chain tag) cannot authenticate the message in that slot; "
  "the best-of selection over spans W > 1 covers those messages in the fragmentation family, the chain has no such alternative (its tag travels with the message).")
w()
rtt = res[(res.cond == "iid 0") & (res.feasible == 1)].groupby(["profile", "pq", "mode"]).tx_realtime_ratio.mean().reset_index()
slowtx = rtt[rtt.tx_realtime_ratio > 1]
w(f"Sender real-time check (CPU per message / slot period, this machine; > 1 = the sender cannot keep up): {len(slowtx)} of {len(rtt)} (profile, scheme, mode) configurations" + (": " + ", ".join(sorted({f"{r.pq}/{r['mode']}@{r.profile}" for _, r in slowtx.iterrows()})[:10]) if len(slowtx) else "") + ".")
w()

# ---- paired machinery
MET = ["share", "within_an", "rmst_ms", "air_bytes_per_auth", "bytes_per_s_air", "within_need"]
PER = res[res.loss_p > 0].groupby(["profile", "pq", "cls", "mode", "seed"])[MET].mean()


def ser(profile, pqn, cls, mode, metric):
    try:
        return PER.loc[(profile, pqn, cls, mode)][metric]
    except KeyError:
        return pd.Series(dtype=float)


def paired(profile, pqn, cls, metric, better, rel, chain_mode=CH, comp_modes=COMP, thr=None):
    c = ser(profile, pqn, cls, chain_mode, metric)
    cand = {m: ser(profile, pqn, cls, m, metric) for m in comp_modes}
    cs = {m: v.mean() for m, v in cand.items() if len(v) and not np.isnan(v.mean())}
    comp_alive = max([ser(profile, pqn, cls, m, "within_an").mean() for m in comp_modes] + [0.0])
    row = dict(profile=profile, pq=pqn, cls=cls, competitor_infeasible=int(comp_alive <= 1e-9))
    if not cs or c.isna().all():
        return dict(row, best="", chain=np.nan, comp=np.nan, diff=np.nan, lo=np.nan, hi=np.nan, n=0, outcome="no data")
    bm = (max if better == "higher" else min)(cs, key=cs.get)
    d = (c - cand[bm]).dropna()
    n = len(d)
    if n < 2:
        return dict(row, best=bm, chain=c.mean(), comp=cs[bm], diff=np.nan, lo=np.nan, hi=np.nan, n=n, outcome="no data")
    ref = cs[bm] if rel else 1.0
    if rel and abs(ref) < 1e-12:
        return dict(row, best=bm, chain=c.mean(), comp=cs[bm], diff=np.nan, lo=np.nan, hi=np.nan, n=n, outcome="no data")
    m_ = d.mean() / ref; h = tcrit(n - 1) * d.std(ddof=1) / math.sqrt(n) / abs(ref)
    lo, hi = m_ - h, m_ + h
    t = thr if thr is not None else (EFF["bytes_rel"] if metric.startswith("air") or metric.startswith("bytes") else EFF["delay_rel"]) if rel else EFF["share_abs"]
    fav_lo, fav_hi = (lo, hi) if better == "higher" else (-hi, -lo)           # favourable direction = positive
    out = "chain better" if fav_lo > t else "chain worse" if fav_hi < -t else "equivalent" if (lo > -t and hi < t) else "unclear"
    return dict(row, best=bm, chain=c.mean(), comp=cs[bm], diff=m_, lo=lo, hi=hi, n=n, outcome=out)


def verdict_of(df):
    d = df[(df.competitor_infeasible == 0) & (df.outcome != "no data")]
    n = len(d)
    if n == 0:
        return dict(n=0, better=0, worse=0, equivalent=0, unclear=0, verdict="no data")
    fb = (d.outcome == "chain better").mean(); fw = (d.outcome == "chain worse").mean()
    v = "supported" if fb >= VR["supported_fraction"] and fw <= VR["worse_tolerance"] else "refuted" if fw >= VR["refuted_fraction"] else "inconclusive"
    return dict(n=n, better=int((d.outcome == "chain better").sum()), worse=int((d.outcome == "chain worse").sum()), equivalent=int((d.outcome == "equivalent").sum()),
                unclear=int((d.outcome == "unclear").sum()), verdict=v)


def combine(vi, vb):
    if vi["verdict"] == vb["verdict"] and vi["verdict"] in ("supported", "refuted"):
        return vi["verdict"]
    return "inconclusive" if "no data" not in (vi["verdict"], vb["verdict"]) else "no data"


def run_h(metric, better, rel):
    rows = [paired(p, q, c, metric, better, rel) for p in PROTO_P for q in PQS for c in ("iid", "burst")]
    return pd.DataFrame(rows)


def fmt_ci(r):
    if np.isnan(r["diff"]):
        return "n/a"
    return f"{r['diff']:+.3f} [{r['lo']:+.3f}, {r['hi']:+.3f}]"


VERD = []
PD_ALL = []


def show_h(hid, title, metric, better, rel, unit):
    df = run_h(metric, better, rel); df["hypothesis"] = hid; PD_ALL.append(df)
    vs = {c: verdict_of(df[df.cls == c]) for c in ("iid", "burst")}
    vv = combine(vs["iid"], vs["burst"])
    VERD.append(dict(hypothesis=hid, claim=HY["hypotheses"][hid]["text"], iid=vs["iid"]["verdict"], burst=vs["burst"]["verdict"], verdict=vv, n_iid=vs["iid"]["n"], n_burst=vs["burst"]["n"]))
    w(f"### {hid}: {title}")
    w()
    w(f"Source: `raw/proto_results_{MN}.csv` (loss > 0; per-seed values averaged over the conditions of the class, then chain minus best fragmentation mode, Student-t 95% CI over {nseeds_o} independent seeds). "
      f"Difference {'relative to the competitor' if rel else 'absolute'} ({unit}); chain variant `{CH}`. Competitor = best of the fragmentation modes of the group.")
    w()
    t = df.copy()
    t["profile"] = pd.Categorical(t.profile, PROTO_P); t["pq"] = pd.Categorical(t.pq, PQS)
    tt = pd.DataFrame({"profile": t.profile, "scheme": t.pq, "loss class": t.cls, "best frag mode": np.where(t.competitor_infeasible == 1, "-", t.best), "chain": t.chain.round(3), "best frag": t.comp.round(3),
                       "chain - frag [95% CI]": t.apply(fmt_ci, axis=1), "outcome": np.where(t.competitor_infeasible == 1, "competitor infeasible", t.outcome)})
    w(md(tt.sort_values(["profile", "scheme", "loss class"]))); w()
    cnt = pd.DataFrame([{"loss class": c, "decidable groups": vs[c]["n"], "chain better": vs[c]["better"], "chain worse": vs[c]["worse"], "equivalent (tie)": vs[c]["equivalent"],
                         "unclear": vs[c]["unclear"], "competitor infeasible (excluded)": int(df[df.cls == c].competitor_infeasible.sum()), "class verdict": vs[c]["verdict"]} for c in ("iid", "burst")])
    w("Secondary table, tie-aware group counts (each group counted once; ties = CI inside the minimum effect):"); w(); w(md(cnt)); w()
    w(f"**Verdict {hid}: {vv.upper()}** (i.i.d. class {vs['iid']['verdict']}, burst class {vs['burst']['verdict']}). PROVISIONAL (smoke run)." if smoke else f"**Verdict {hid}: {vv.upper()}** (i.i.d. class {vs['iid']['verdict']}, burst class {vs['burst']['verdict']}).")
    w()
    return df


h1 = show_h("H1", "share of received messages authenticated within the analysis deadline", "within_an", "higher", False, f"fraction; deadline {D_AN} message periods")
h2 = show_h("H2", "bytes on air per authenticated message", "air_bytes_per_auth", "lower", True, "relative; bytes in the measured slots / authenticated messages")
h3 = show_h("H3", "unconditional delay (restricted mean time to authentication, unauthenticated censored at the deadline)", "rmst_ms", "lower", True, f"relative; ms, censored at {D_AN} message periods")

# variants and Merkle against the same competitor
var_rows = []
for v in ("chain_r2", "chain_lead", "chain_lead_cont", "merkle4", "merkle8", "merkle16"):
    for metric, better, rel, nm in (("within_an", "higher", False, "H1 share"), ("air_bytes_per_auth", "lower", True, "H2 bytes"), ("rmst_ms", "lower", True, "H3 delay")):
        d = pd.DataFrame([paired(p, q, c, metric, better, rel, chain_mode=v) for p in PROTO_P for q in PQS for c in ("iid", "burst")])
        for c in ("iid", "burst"):
            vv = verdict_of(d[d.cls == c]); var_rows.append({"variant": v, "metric": nm, "loss class": c, "decidable": vv["n"], "better": vv["better"], "worse": vv["worse"], "tie": vv["equivalent"], "unclear": vv["unclear"], "verdict": vv["verdict"]})
w("### Other chain variants and Merkle against the same best fragmentation mode")
w()
w(f"Same rule and data as H1-H3 with the variant in place of `{CH}`:"); w(); w(md(pd.DataFrame(var_rows))); w()

# competitor infeasible cells (separate)
w("### Cells where the fragmentation competitor is infeasible at the native rate")
w()
inf = h1[h1.competitor_infeasible == 1]
tb = inf.groupby(["profile", "cls"]).agg(schemes=("pq", lambda x: ", ".join(sorted(set(x)))), chain_share_within_deadline_mean=("chain", "mean")).reset_index()
w("No fragmentation mode authenticates any message; the chain's share within the deadline is shown for information only (not a contest):"); w(); w(md(tb)); w()

# ---- H4 stated latency need
w("### H4: the stated latency need (C-V2X 100 ms)")
w()
h4 = []
for p in PROTO_P:
    if not NEED[p]:
        continue
    for q in PQS:
        sub = res[(res.profile == p) & (res.pq == q) & (res.cond == "iid 0")]
        if sub.empty:
            continue
        r = {"profile": p, "scheme": q, "need ms": NEED[p]["ms"], "need slots": int(NEED[p]["ms"] // SLOT_MS[p])}
        for m in [CH] + COMP:
            v = sub[sub["mode"] == m].within_need
            r[m] = v.mean() if len(v) else np.nan
        best = max(COMP, key=lambda m: -1 if np.isnan(r[m]) else r[m])
        r["chain_within_need"] = r[CH]; r["best frag mode"] = best; r["best frag within_need"] = r[best]
        r["min chain delay ms"] = (COM["protocol"]["key_delay_slots_d"] + 1) * SLOT_MS[p]
        h4.append(r)
h4 = pd.DataFrame(h4)
H4V = "no data"
if len(h4):
    hh = HY["hypotheses"]["H4"]
    h4["chain verdict"] = np.where(h4.chain_within_need >= hh["supported_at_least"], "supported", np.where(h4.chain_within_need < hh["refuted_below"], "refuted", "inconclusive"))
    fs = (h4["chain verdict"] == "supported").mean(); fr = (h4["chain verdict"] == "refuted").mean()
    H4V = "supported" if fs >= VR["supported_fraction"] else "refuted" if fr >= VR["refuted_fraction"] else "inconclusive"
    w(f"Source: `raw/proto_results_{MN}.csv`, lossless condition (`iid 0`, the best case). `chain_within_need` = fraction of received messages authenticated within the need ({NEED[PROTO_P[1]]['source'] if NEED.get(PROTO_P[1]) else ''}); the chain cannot authenticate before its key is released: minimum delay = (d + 1) slots.")
    w()
    w(md(h4[["profile", "scheme", "need ms", "need slots", "chain_within_need", "best frag mode", "best frag within_need", "min chain delay ms", "chain verdict"]].round(3))); w()
    w(f"SIB1: latency need is TODO-RESULT (darzi2026a states no hard deadline), so H4 is not evaluated for it. For reference the chain's minimum delay on SIB1 is {(COM['protocol']['key_delay_slots_d'] + 1) * SLOT_MS['sib1']} ms.")
    w()
    w(f"**Verdict H4: {H4V.upper()}** ({int((h4['chain verdict'] == 'supported').sum())} of {len(h4)} (profile, scheme) pairs supported, {int((h4['chain verdict'] == 'refuted').sum())} refuted)." + (" PROVISIONAL (smoke run)." if smoke else ""))
    w()
VERD.append(dict(hypothesis="H4", claim=HY["hypotheses"]["H4"]["text"], iid=H4V, burst="n/a (lossless)", verdict=H4V, n_iid=len(h4), n_burst=0))

# ---- delay distribution
w("### Unconditional delay distribution at i.i.d. loss 0.1 (all received messages, unauthenticated = censored)")
w()


def pooled(df):
    rc = df.received.sum(); h = df[LAGC].sum().values
    return rc, np.cumsum(h) / rc if rc else np.full(20, np.nan)


rows = []
for p in PROTO_P:
    for q in PQS:
        sub = res[(res.profile == p) & (res.pq == q) & (res.cond == "iid 0.1")]
        if sub.empty:
            continue
        means = sub.groupby("mode").within_an.mean()
        bf = max(COMP, key=lambda m: means.get(m, -1)); mk = [m for m in ("merkle4", "merkle8", "merkle16")]
        bm = max(mk, key=lambda m: means.get(m, -1))
        for lab, m in (("chain", CH), ("best frag", bf), ("best merkle", bm)):
            s_ = sub[sub["mode"] == m]
            if s_.empty or means.get(m, 0) == 0:
                rows.append({"profile": p, "scheme": q, "family": lab, "mode": m, "authenticated within 1 slot": 0.0, "within 3": 0.0, "within 10": 0.0, "within 20": 0.0, "median ms": ">20 slots / none", "p90 ms": ">20 slots / none"})
                continue
            rc, cdf = pooled(s_)
            qs = lambda qq: (f"{(int(np.argmax(cdf >= qq)) + 1) * SLOT_MS[p]}" if (cdf >= qq).any() else ">20 slots")     # noqa: E731
            rows.append({"profile": p, "scheme": q, "family": lab, "mode": m, "authenticated within 1 slot": cdf[0], "within 3": cdf[2], "within 10": cdf[9], "within 20": cdf[19],
                         "median ms": qs(0.5), "p90 ms": qs(0.9)})
dd = pd.DataFrame(rows)
dd.to_csv(os.path.join(RES, "delay_distribution_iid0.1.csv"), index=False)
w(f"Source: `raw/proto_results_{MN}.csv` (lag histograms pooled over seeds; the fractions are of all RECEIVED messages, so a mode that authenticates few messages is not favoured). Full table: `results/delay_distribution_iid0.1.csv`. Showing J3161 and SIB1 rows:")
w(); w(md(dd[dd.profile.isin(["sib1", "cv2x_j3161"])].round(3))); w()
fig, axs = plt.subplots(1, len(PROTO_P), figsize=(5 * len(PROTO_P), 3.6), squeeze=False)
for ax, p in zip(axs[0], PROTO_P):
    for lab, c in (("chain", "C3"), ("best frag", "C0"), ("best merkle", "C2")):
        g = dd[(dd.profile == p) & (dd.family == lab)]
        if len(g):
            ax.plot(np.arange(1, 21) * SLOT_MS[p], [0] * 20, alpha=0)
    for q in PQS:
        sub = res[(res.profile == p) & (res.pq == q) & (res.cond == "iid 0.1")]
        for lab, m, c in (("chain", CH, "C3"), ("best frag", None, "C0"), ("merkle8", "merkle8", "C2")):
            if m is None:
                means = sub.groupby("mode").within_an.mean(); m = max(COMP, key=lambda x: means.get(x, -1))
            s_ = sub[sub["mode"] == m]
            if s_.empty:
                continue
            rc, cdf = pooled(s_)
            ax.step(np.arange(1, 21) * SLOT_MS[p], cdf, where="post", color=c, alpha=0.5, lw=1, label=lab if q == PQS[0] else None)
    if NEED[p]:
        ax.axvline(NEED[p]["ms"], color="k", ls="--", lw=0.8)
    ax.set_title(LAB[p], fontsize=8); ax.set_xlabel("time since message slot start (ms)"); ax.set_ylabel("fraction of received messages authenticated"); ax.set_ylim(0, 1.02)
axs[0, 0].legend(fontsize=6); fig.tight_layout(); fig.savefig(os.path.join(RES, "fig_delay_cdf.pdf")); plt.close(fig)
w(f"Figure `fig_delay_cdf.pdf` (source `raw/proto_results_{MN}.csv`; one line per scheme; dashed = stated latency need).")
w()

# ---- forest plot for H1
fig, axs = plt.subplots(1, 2, figsize=(11, 0.28 * len(PROTO_P) * len(PQS) + 1.5), sharey=True)
for ax, c in zip(axs, ("iid", "burst")):
    d = h1[(h1.cls == c) & (h1.competitor_infeasible == 0)].copy()
    d["lab"] = d.profile + " / " + d.pq
    d = d.iloc[::-1]
    ax.errorbar(d["diff"], range(len(d)), xerr=[d["diff"] - d.lo, d.hi - d["diff"]], fmt="o", ms=3, capsize=2)
    ax.axvline(0, color="k", lw=0.7); ax.axvline(EFF["share_abs"], color="g", ls=":", lw=0.7); ax.axvline(-EFF["share_abs"], color="r", ls=":", lw=0.7)
    ax.set_yticks(range(len(d))); ax.set_yticklabels(d.lab, fontsize=6); ax.set_title(f"{c} loss", fontsize=8); ax.set_xlabel("chain - best frag, share within deadline")
fig.tight_layout(); fig.savefig(os.path.join(RES, "fig_h1_share_diff.pdf")); plt.close(fig)
w(f"Figure `fig_h1_share_diff.pdf` (source: the H1 table, `results/paired_differences.csv`; dotted lines = minimum effect).")
w()

# ---- bytes at the operating point
w("### Bytes on air at the operating point (i.i.d. loss 0.1)")
w()
rows = []
for p in PROTO_P:
    for q in PQS:
        sub = res[(res.profile == p) & (res.pq == q) & (res.cond == "iid 0.1")]
        if sub.empty:
            continue
        means = sub.groupby("mode").within_an.mean(); bf = max(COMP, key=lambda m: means.get(m, -1))
        r = {"profile": p, "scheme": q, "allocated B/slot": int(sub.B_slot.iloc[0])}
        for lab, m in (("chain", CH), ("chain_r2", "chain_r2"), ("best frag", bf), ("merkle8", "merkle8")):
            s_ = sub[sub["mode"] == m]
            r[f"{lab} B per auth msg"] = s_.air_bytes_per_auth.mean() if s_.air_bytes_per_auth.notna().any() else np.nan
        rows.append(r)
bt = pd.DataFrame(rows)
w(f"Source: `raw/proto_results_{MN}.csv`. Bytes of authentication fields in the measured slots divided by the number of authenticated messages (steady state: no prelude, warm-up or tail slots are charged to or credited to any mode). NaN = the mode authenticates nothing.")
w(); w(md(bt.round(0))); w()
chb = bt.dropna(subset=["chain B per auth msg", "best frag B per auth msg"])
if len(chb):
    rr = chb["chain B per auth msg"] / chb["best frag B per auth msg"]
    w(f"chain / best-frag bytes per authenticated message: median {rr.median():.2f}, range {rr.min():.2f}-{rr.max():.2f} over {len(rr)} pairs where both authenticate; chain_r2 / best frag: median {(chb['chain_r2 B per auth msg'] / chb['best frag B per auth msg']).median():.2f}.")
    w()

# ---- ">= 0.95" claims over all conditions, burst effects
w("### Share claims over ALL loss conditions (worst case stated)")
w()
cell = res[res.loss_p > 0].groupby(["profile", "pq", "mode", "cond"]).agg(within_an=("within_an", "mean"), feas=("feasible", "first")).reset_index()
bestf = cell[cell["mode"].isin(COMP)].groupby(["profile", "pq", "cond"]).agg(within_an=("within_an", "max"), feas=("feas", "max")).reset_index()
chn = cell[cell["mode"] == CH][["profile", "pq", "cond", "within_an", "feas"]]
cr = chn.merge(bestf, on=["profile", "pq", "cond"], suffixes=("_chain", "_frag"))
cr["cls"] = np.where(cr.cond.str.startswith("iid"), "iid", "burst")
rows = []
for c in ("iid", "burst", "all"):
    d = cr if c == "all" else cr[cr.cls == c]
    dc = d[d.feas_chain == 1]; df_ = d[d.feas_frag == 1]
    wc = dc.loc[dc.within_an_chain.idxmin()]; wf = df_.loc[df_.within_an_frag.idxmin()]
    rows.append({"loss class": c, "cells (profile, scheme, condition)": len(d), "chain feasible cells": len(dc), "chain share >= 0.95": int((dc.within_an_chain >= 0.95).sum()),
                 "chain worst feasible cell": f"{wc.within_an_chain:.3f} ({wc.profile}/{wc.pq}/{wc.cond})", "frag feasible cells": len(df_), "best frag share >= 0.95": int((df_.within_an_frag >= 0.95).sum()),
                 "best frag worst feasible cell": f"{wf.within_an_frag:.3f} ({wf.profile}/{wf.pq}/{wf.cond})"})
w(f"Source: `raw/proto_results_{MN}.csv`; share = fraction of received messages authenticated within {D_AN} message periods, per cell mean over seeds; the count of cells >= 0.95 is over cells where the mode is feasible at the native rate, and the worst case is the minimum over those cells. Conditions present: {', '.join(CONDS)}.")
w(); w(md(pd.DataFrame(rows))); w()
w("Burst effect: share within the deadline under Gilbert-Elliott loss minus i.i.d. loss at the same stationary loss p (mean over profiles and schemes where the mode is feasible; `n neg` = (profile, scheme) pairs with a negative delta, because the sign differs per scheme):")
w()
iidm = res[res.loss_model == "iid"].groupby(["profile", "pq", "mode", "loss_p"]).within_an.mean()
ge = res[res.loss_model == "ge"].groupby(["profile", "pq", "mode", "loss_p", "burst_len"]).within_an.mean().reset_index()
ge["iid"] = [iidm.get((r.profile, r.pq, r["mode"], r.loss_p), np.nan) for _, r in ge.iterrows()]
ge["delta"] = ge.within_an - ge.iid
ge["family"] = np.where(ge["mode"] == CH, CH, np.where(ge["mode"].isin(COMP), "frag (all W/coder)", np.where(ge["mode"].str.startswith("merkle"), "merkle", "other")))
ge = ge[ge["mode"].isin([CH] + COMP + ["merkle4", "merkle8", "merkle16"])]
ge = ge.dropna(subset=["delta"])
gt = ge.groupby(["family", "burst_len"]).agg(mean_delta=("delta", "mean"), n_neg=("delta", lambda x: int((x < -1e-9).sum())), n=("delta", "size")).reset_index()
w(md(gt.round(3))); w()

# ---------------------------------------------------------------- H5 minimum budget
w("### H5: minimum channel budget to reach a target share within the deadline")
w()
MB = HY["minbudget"]; TG = MB["targets"]
mbm = minb.groupby(["profile", "pq", "mode", "cond", "cls", "B_mult"]).agg(within_an=("within_an", "mean"), within_need=("within_need", "mean"), bps=("bytes_per_s", "first"), B_slot=("B_slot", "first"), feas=("feasible", "first")).reset_index()
mbm.to_csv(os.path.join(RES, "minbudget_cells.csv"), index=False)


def minbps(sub, col, t):
    ok = sub[sub[col] >= t]
    return float(ok.bps.min()) if len(ok) else np.inf


rows = []
for (p, q, cnd), g in mbm.groupby(["profile", "pq", "cond"]):
    for dl, col in (("analysis", "within_an"), ("need", "within_need")):
        if dl == "need" and (not NEED[p] or g[col].isna().all()):
            continue
        for t in TG:
            r = {"profile": p, "scheme": q, "cond": cnd, "cls": g.cls.iloc[0], "deadline": dl, "target": t}
            vals = {m: minbps(g[g["mode"] == m], col, t) for m in MO.MODES}
            r["chain"] = vals[CH]; r["chain_r2"] = vals["chain_r2"]; r["chain_lead_cont"] = vals["chain_lead_cont"]
            bc = min(COMP, key=lambda m: vals[m]); r["best frag mode"] = bc if np.isfinite(vals[bc]) else ""; r["best frag"] = vals[bc]
            bm = min(["merkle4", "merkle8", "merkle16"], key=lambda m: vals[m]); r["best merkle"] = vals[bm]
            r["best hybrid"] = min(vals[m] for m in MO.MODES if m.startswith("hyb"))
            c, f = r["chain"], r["best frag"]
            r["outcome"] = ("neither reaches" if not np.isfinite(c) and not np.isfinite(f) else "chain only" if np.isfinite(c) and not np.isfinite(f)
                            else "frag only" if not np.isfinite(c) else "chain cheaper" if c / f <= EFF["budget_ratio_low"] else "chain dearer" if c / f >= EFF["budget_ratio_high"] else "similar")
            r["ratio chain/frag"] = (c / f) if np.isfinite(c) and np.isfinite(f) else np.nan
            rows.append(r)
mbt = pd.DataFrame(rows)
mbt.to_csv(os.path.join(RES, "minbudget_table.csv"), index=False)
w(f"Source: `raw/minbudget_{MN}.csv` ({', '.join(str(x) for x in MB['multipliers']['quick' if smoke else 'full'])} x the profile's budget per slot as listed in `hypotheses.yaml`; the quick grid is used in QUICK runs). A cell's value is the smallest budget in bytes per second "
  "(budget per slot / slot period) whose mean share of received messages authenticated within the deadline (over seeds) reaches the target; `inf` = not reached on the grid (right-censored at the largest budget). "
  "This replaces the pass-3 allocation rule (anchor symbol in every slot): each mode gets every grid budget, and the chain is shown with full anchor redundancy (`chain`) and with bounded anchor redundancy (`chain_r2`, rho = 2). "
  "Full table: `results/minbudget_table.csv`; per-cell shares: `results/minbudget_cells.csv`. Deadlines: `analysis` = " + f"{D_AN} message periods; `need` = the source-stated latency need (C-V2X 100 ms).")
w()
hdl = mbt[(mbt.deadline == "analysis") & (mbt.target == TG[0])]
w(f"Headline view (analysis deadline, target {TG[0]}), bytes per second:"); w()
w(md(hdl[["profile", "scheme", "cond", "chain", "chain_r2", "chain_lead_cont", "best frag mode", "best frag", "best merkle", "best hybrid", "outcome"]].round(0))); w()
vt = []
mb_verd = {}
for dl in ("analysis", "need"):
    for t in TG:
        d = mbt[(mbt.deadline == dl) & (mbt.target == t)]
        if d.empty:
            continue
        per = {}
        for c in ("iid", "burst"):
            x = d[(d.cls == c) & (d.outcome != "neither reaches")]; n = len(x)
            if n == 0:
                per[c] = ("no data", 0, 0, 0, 0); continue
            fb = x.outcome.isin(["chain cheaper", "chain only"]).mean(); fw = x.outcome.isin(["chain dearer", "frag only"]).mean()
            v = "supported" if fb >= VR["supported_fraction"] and fw <= VR["worse_tolerance"] else "refuted" if fw >= VR["refuted_fraction"] else "inconclusive"
            per[c] = (v, n, int(x.outcome.isin(["chain cheaper", "chain only"]).sum()), int(x.outcome.isin(["chain dearer", "frag only"]).sum()), int((x.outcome == "similar").sum()))
        vv = combine(dict(verdict=per["iid"][0]), dict(verdict=per["burst"][0]))
        mb_verd[(dl, t)] = vv
        vt.append({"deadline": dl, "target": t, "iid: decidable / chain cheaper or only / dearer or frag-only / similar": "/".join(str(v) for v in per["iid"][1:]), "iid verdict": per["iid"][0],
                   "burst: decidable / cheaper / dearer / similar": "/".join(str(v) for v in per["burst"][1:]), "burst verdict": per["burst"][0], "combined": vv,
                   "neither reaches (excluded)": int((d.outcome == "neither reaches").sum())})
w("Counts of cells by outcome and the H5 verdict per deadline and target (ties = 'similar'; cells in which neither side reaches the target on the grid are excluded and counted):"); w(); w(md(pd.DataFrame(vt))); w()
head5 = mb_verd.get(("analysis", TG[0]), "no data")
VERD.append(dict(hypothesis="H5", claim=HY["hypotheses"]["H5"]["text"], iid=[v["iid verdict"] for v in vt if v["deadline"] == "analysis" and v["target"] == TG[0]][0] if vt else "no data",
                 burst=[v["burst verdict"] for v in vt if v["deadline"] == "analysis" and v["target"] == TG[0]][0] if vt else "no data", verdict=head5, n_iid=0, n_burst=0))
w(f"**Verdict H5 (headline: analysis deadline, target {TG[0]}): {head5.upper()}.** Other deadline / target combinations are in the table above." + (" PROVISIONAL (smoke run)." if smoke else ""))
w()
w("Reading: the pass-3 'chain needs 200x redundant anchor symbols' effect is removed because the anchor redundancy is no longer fixed by the allocation rule: compare `chain` (all free bytes used) with `chain_r2` (bounded) and with the budget at which each reaches the target.")
w()
fig, axs = plt.subplots(1, len(PROTO_P), figsize=(5 * len(PROTO_P), 3.8), squeeze=False)
for ax, p in zip(axs[0], PROTO_P):
    d = mbt[(mbt.profile == p) & (mbt.deadline == "analysis") & (mbt.target == TG[0])]
    xs = np.arange(len(d)); lab = (d.scheme + " " + d.cond).values
    for col, c, off in (("chain", "C3", -0.25), ("chain_r2", "C1", 0.0), ("best frag", "C0", 0.25)):
        v = d[col].replace(np.inf, np.nan).values
        ax.scatter(xs + off, v, s=14, c=c, label=col)
        cens = d[col].values == np.inf
        ax.scatter((xs + off)[cens], np.full(cens.sum(), np.nanmax(d[["chain", "chain_r2", "best frag"]].replace(np.inf, np.nan).values) * 1.5 if np.isfinite(d[["chain", "chain_r2", "best frag"]].replace(np.inf, np.nan).values).any() else 1), marker="^", c=c, s=14)
    ax.set_yscale("log"); ax.set_xticks(xs[::max(1, len(xs) // 12)]); ax.set_xticklabels(lab[::max(1, len(xs) // 12)], rotation=70, fontsize=5)
    ax.set_title(LAB[p], fontsize=8); ax.set_ylabel(f"min budget for share >= {TG[0]} (B/s); triangles = not reached")
axs[0, 0].legend(fontsize=6); fig.tight_layout(); fig.savefig(os.path.join(RES, "fig_minbudget.pdf")); plt.close(fig)
w(f"Figure `fig_minbudget.pdf` (source `results/minbudget_table.csv` from `raw/minbudget_{MN}.csv`).")
w()

# ---------------------------------------------------------------- active attacker
w("## Active attacker (same harness)")
w()
AH = HY["attack"]
w(f"Source: `raw/attack_{MN}.csv`. Attacker model (`lib/pqsig/proto/attacks.py`): hears all frames, knows formats, schedule and the public key, has neither the PQ secret key nor the chain secret; learns a chain key only through disclosure. "
  f"Background channel: i.i.d. loss {AH['background_loss']}. (i) **Injection**: in a fraction r of the slots the attacker adds one frame that copies a genuine frame (same headers, same indices, the genuine application message) with random payload bytes in every symbol / tag / key / path / commitment field (at most one bogus frame per slot; a stronger attacker that sends several per slot is not modelled). "
  "(ii) **Clock offset**: the receiver's clock is shifted by the given number of slots (negative = behind) while the attacker jams every 5th measured message and re-sends a forged version of it after its key was disclosed (the classic TESLA attack; for the other modes the forgery re-uses the genuine authenticator). "
  "(iii) **Replay**: the receiver is offline for epoch 1 while the attacker records the frames; the recorded frames are replayed 4 epochs later (older than the freshness bound). The control receiver has no freshness / time-safety checks. "
  f"Pairs run (feasible fragmentation at the native rate): {', '.join(f'{p}/{q}' for p, q in AH['pairs'])}. Metrics: forged messages accepted (must be 0), share of honest (not jammed) received messages still authenticated, extra receiver CPU.")
w()
att["family"] = att["mode"].map(lambda m: CH if m == CH else m if m.startswith("chain") else "frag/hyb" if m.startswith(("frag", "hyb")) else "merkle")
inj_all = att[att.attack.isin(["none", "inject", "inject_x4"])]
inj = att[att.attack.isin(["none", "inject"])]
inj4 = att[att.attack.isin(["none", "inject_x4"])]
ij = inj.groupby(["profile", "pq", "mode", "param"]).agg(share=("share", "mean"), cpu=("rx_cpu_us_per_msg", "mean"), fa=("false_accepts", "sum")).reset_index()
w("### (i) Symbol / fragment injection")
w()
rates = sorted(ij.param.unique())
sh = ij.pivot_table(index=["profile", "pq", "mode"], columns="param", values="share").reset_index()
sh.columns = [f"share @ {c:g}" if not isinstance(c, str) else c for c in sh.columns]
w("Share of received honest messages authenticated within the run (mean over seeds) by injection rate (0 = no attack):"); w()
w(md(sh.round(3))); w()
tot_fa_inj = int(inj_all.false_accepts.sum()); tot_st_inj = int(inj_all.stale_accepted.sum())
w(f"**Forged messages accepted under injection: {tot_fa_inj}; stale acceptances: {tot_st_inj}** (over {len(inj_all)} runs with 1 or 4 bogus frames per attacked slot, all modes).")
w()
ra = HY["hypotheses"]["H7"]["at_rate"]
rows = []
for (p, q, m), g in ij.groupby(["profile", "pq", "mode"]):
    b = g[g.param == 0]; a = g[np.isclose(g.param, ra)]
    if b.empty or a.empty or b.share.iloc[0] <= 0:
        continue
    rows.append({"profile": p, "pq": q, "mode": m, "family": "chain" if m.startswith("chain") else "merkle" if m.startswith("merkle") else "hybrid" if m.startswith("hyb") else "frag",
                 "retention": a.share.iloc[0] / b.share.iloc[0], "cpu_ratio": a.cpu.iloc[0] / b.cpu.iloc[0] if b.cpu.iloc[0] > 0 else np.nan})
rt_ = pd.DataFrame(rows)
H7V = H8V = "no data"
if len(rt_):
    thr7 = HY["hypotheses"]["H7"]["retention"]; thr8 = HY["hypotheses"]["H8"]["factor"]
    f7 = (rt_.retention >= thr7).mean(); f7w = (rt_.retention < thr7).mean()
    H7V = "supported" if f7 >= HY["hypotheses"]["H7"]["supported_fraction"] else "refuted" if f7w >= VR["refuted_fraction"] else "inconclusive"
    f8 = (rt_.cpu_ratio <= thr8).mean(); f8w = (rt_.cpu_ratio > thr8).mean()
    H8V = "supported" if f8 >= VR["supported_fraction"] else "refuted" if f8w >= VR["refuted_fraction"] else "inconclusive"
    fam = rt_.groupby("family").agg(cells=("retention", "size"), retention_mean=("retention", "mean"), retention_min=("retention", "min"), cells_ge_threshold=("retention", lambda x: int((x >= thr7).sum())),
                                    cpu_ratio_mean=("cpu_ratio", "mean"), cpu_ratio_max=("cpu_ratio", "max")).reset_index()
    w(f"Retention = share at {ra:.0%} injection / share without attack; extra CPU = receiver CPU per message ratio. By mode family ({len(rt_)} (pair, mode) cells where the mode works without attack):"); w()
    w(md(fam.round(3))); w()
    worst = rt_.loc[rt_.retention.idxmin()]
    w(f"Worst case: {worst['mode']} on {worst.profile}/{worst.pq}: retention {worst.retention:.3f}. **Verdict H7 (retention >= {thr7:.0%} at {ra:.0%} injection in >= {HY['hypotheses']['H7']['supported_fraction']:.0%} of cells): {H7V.upper()}** ({int((rt_.retention >= thr7).sum())}/{len(rt_)} cells)." + (" PROVISIONAL." if smoke else ""))
    w(f"**Verdict H8 (receiver CPU <= {thr8:g}x at {ra:.0%} injection): {H8V.upper()}** ({int((rt_.cpu_ratio <= thr8).sum())}/{len(rt_)} cells; worst ratio {rt_.cpu_ratio.max():.2f})." + (" PROVISIONAL." if smoke else ""))
    w()
ij4 = inj4.groupby(["profile", "pq", "mode", "param"]).agg(share=("share", "mean")).reset_index()
rows4 = []
for (p_, q_, m_), g in ij4.groupby(["profile", "pq", "mode"]):
    b = g[g.param == 0]; a = g[np.isclose(g.param, ra)]
    if b.empty or a.empty or b.share.iloc[0] <= 0:
        continue
    rows4.append({"mode": m_, "family": "chain" if m_.startswith("chain") else "merkle" if m_.startswith("merkle") else "hybrid" if m_.startswith("hyb") else "frag", "profile": p_, "pq": q_, "retention": a.share.iloc[0] / b.share.iloc[0]})
if rows4:
    r4 = pd.DataFrame(rows4)
    f4 = r4.groupby("family").agg(cells=("retention", "size"), retention_mean=("retention", "mean"), retention_min=("retention", "min"), cells_ge_threshold=("retention", lambda x: int((x >= HY["hypotheses"]["H7"]["retention"]).sum()))).reset_index()
    w(f"Descriptive (no pre-registered criterion): the same retention at {ra:.0%} of slots when the attacker sends 4 bogus frames per attacked slot (more than the 3 candidate symbols kept per index):"); w(); w(md(f4.round(3))); w()
    w4 = r4.loc[r4.retention.idxmin()]
    w(f"Worst case with 4 bogus frames: {w4['mode']} on {w4.profile}/{w4.pq}: retention {w4.retention:.3f}.")
    w()
VERD.append(dict(hypothesis="H7", claim=HY["hypotheses"]["H7"]["text"], iid="n/a", burst="n/a", verdict=H7V, n_iid=len(rt_), n_burst=0))
VERD.append(dict(hypothesis="H8", claim=HY["hypotheses"]["H8"]["text"], iid="n/a", burst="n/a", verdict=H8V, n_iid=len(rt_), n_burst=0))
fig, ax = plt.subplots(figsize=(7, 4))
for fam_, c in (("frag/hyb", "C0"), ("merkle", "C2"), (CH, "C3"), ("chain_lead_cont", "C1")):
    d = inj[inj.family == fam_].groupby("param").share.mean()
    if len(d):
        ax.plot(d.index * 100, d.values, marker="o", ms=3, color=c, label=fam_)
for fam_, c in (("frag/hyb", "C0"), ("merkle", "C2"), (CH, "C3"), ("chain_lead_cont", "C1")):
    d = inj4[inj4.family == fam_].groupby("param").share.mean()
    if len(d):
        ax.plot(d.index * 100, d.values, marker="x", ms=3, ls="--", color=c, alpha=0.7)
ax.set_xlabel("injection rate (% of slots); solid: 1 bogus frame per attacked slot, dashed: 4"); ax.set_ylabel("share of honest messages authenticated"); ax.legend(fontsize=7); ax.set_ylim(0, 1.02)
fig.tight_layout(); fig.savefig(os.path.join(RES, "fig_attack_inject.pdf")); plt.close(fig)
w(f"Figure `fig_attack_inject.pdf` (source `raw/attack_{MN}.csv`; mean over pairs, seeds and modes of the family).")
w()

w("### (ii) Receiver clock offset with the delayed-forgery attacker")
w()
ck = att[att.attack == "clock"]
cf = ck.groupby(["family", "param"]).agg(forged_accepted=("false_accepts", "sum"), honest_share=("share", "mean"), runs=("share", "size")).reset_index()
w(f"Forged messages accepted and honest share by clock offset (offset in slots, negative = receiver behind; configured sync bound {AH['sync_bound_slots']} slot). Targets forged per run: every 5th measured message.")
w(); w(md(cf.pivot_table(index="family", columns="param", values="forged_accepted", aggfunc="sum").reset_index().rename_axis(None, axis=1))); w()
w(md(cf.pivot_table(index="family", columns="param", values="honest_share").reset_index().rename_axis(None, axis=1).round(3))); w()
within_b = ck[ck.param.abs() <= AH["sync_bound_slots"]]
beyond = ck[ck.param.abs() > AH["sync_bound_slots"]]
fa_in = int(within_b.false_accepts.sum()); fa_out = beyond.groupby("family").false_accepts.sum()
thr_c = 2 + MO.DELTA_SLOTS
w(f"Forged accepted for |offset| <= {AH['sync_bound_slots']} slot: **{fa_in}** (over {len(within_b)} runs). Beyond the bound: " + ", ".join(f"{k}: {int(v)}" for k, v in fa_out.items()) +
  f". Analysis from the schedule: the attacker hears the key at the end of slot m + d and sends the forgery in the next slot, i.e. at (m + d + 2) T; the receiver accepts a tag only if its (shifted) arrival time plus its sync bound ({MO.DELTA_SLOTS} slot) is before the release time (m + d) T, "
  f"so forgeries become possible when the receiver clock is behind by at least {thr_c:g} slots; offsets in this run at which forged messages were accepted: {sorted(float(x) for x in beyond[beyond.false_accepts > 0].param.unique())}. "
  "Positive offsets (receiver ahead) only lose honest messages.")
w()
fig, axs = plt.subplots(1, 2, figsize=(10, 3.6))
for fam_ in sorted(ck.family.unique()):
    d = cf[cf.family == fam_]
    axs[0].plot(d.param, d.forged_accepted, marker="o", ms=3, label=fam_); axs[1].plot(d.param, d.honest_share, marker="o", ms=3, label=fam_)
axs[0].set_xlabel("receiver clock offset (slots)"); axs[0].set_ylabel("forged messages accepted (sum over runs)"); axs[1].set_xlabel("receiver clock offset (slots)"); axs[1].set_ylabel("honest share")
axs[0].legend(fontsize=6); fig.tight_layout(); fig.savefig(os.path.join(RES, "fig_attack_clock.pdf")); plt.close(fig)
w(f"Figure `fig_attack_clock.pdf` (source `raw/attack_{MN}.csv`).")
w()
w("### (iii) Replay of old epochs")
w()
rp = att[att.attack == "replay"]
rpt = rp.groupby("family").agg(runs=("share", "size"), replay_accepted=("replay_accepted", "sum"), stale_accepted=("stale_accepted", "sum"), control_replay_accepted=("ctrl_replay_accepted", "sum"),
                               honest_share=("share", "mean")).reset_index()
w(f"Messages of the replayed epoch authenticated (must be 0) and, as a control, the same count for a receiver without freshness / time-safety checks (> 0 shows the replay bites):"); w(); w(md(rpt.round(3))); w()
fa_rep = int(rp.replay_accepted.sum()) + int(rp.stale_accepted.sum()) + int(rp.false_accepts.sum())
# H6
h6_total = tot_fa_inj + tot_st_inj + fa_in + fa_rep
H6V = "supported" if h6_total == 0 else "refuted"
w(f"**Verdict H6: {H6V.upper()}.** Forged / stale acceptances: injection {tot_fa_inj + tot_st_inj}, replay {fa_rep}, clock offset within the bound {fa_in}; total {h6_total}. The control receiver accepted {int(rp.ctrl_replay_accepted.sum())} replayed messages." + (" PROVISIONAL." if smoke else ""))
w()
VERD.append(dict(hypothesis="H6", claim=HY["hypotheses"]["H6"]["text"], iid="n/a", burst="n/a", verdict=H6V, n_iid=len(inj) + len(rp) + len(within_b), n_burst=0))

w("**What decode-and-verify does and does not protect (pollution).** The receivers keep up to 3 candidate symbols per index and verify subsets (at most 8 failed signature verifications per object; Merkle 16): no extra bytes are sent, the extra work per object is bounded by those verifications. "
  "It does NOT make a signature's own symbols individually authenticable: a symbol hash list or Merkle root over the symbols of a signature would have to be signed by something other than that signature (circular), so there is no per-symbol authentication for frag / Merkle signatures. "
  "What remains unprotected: an attacker that injects enough bad candidates per index (more than 3 per index, or more bad symbols than the subset search can avoid when k is large) still blocks an object; the attacker section above measures how far one bogus frame per slot gets. "
  "`chain_lead_cont` is protected differently: once an epoch is authenticated its successor's commitment travels inside the MACs, so anchor pollution only affects joiners and recovery, not steady state.")
w()

# ---------------------------------------------------------------- negative tests
w("## Negative tests (receivers must reject) and positive controls")
w()
w(f"Source: `raw/negative_tests_{MN}.csv`. SIB1 slot timing and message size, generous budget (32x) so every mode is feasible, E = 8, no channel loss. A **reject test** passes when the receiver's authenticated set equals the stated expected set (the untouched run's set minus the messages the attacker may deny), with zero false accepts and zero stale acceptances. "
  "A **control** passes when its stated positive outcome occurs (an ablated receiver accepts the forgery / the replay; the untouched stream authenticates); controls prove that the reject tests bite and are not counted as tests.")
w()
nt = neg[neg.passed.isin([0, 1])]
rej = nt[nt.kind == "reject"]; ctl = nt[nt.kind == "control"]
w(f"**{int(rej.passed.sum())}/{len(rej)} reject tests passed; {int(ctl.passed.sum())}/{len(ctl)} positive controls passed** (reported separately), over {rej.pq.nunique()} PQ schemes x {rej['mode'].nunique()} modes ({neg[neg.kind == 'n/a'].shape[0]} configurations infeasible at the test budget are listed as n/a).")
w()
gtab = nt.assign(family=nt.test.str.split(" ").str[0]).groupby(["kind", "test"]).agg(runs=("passed", "size"), passed=("passed", "sum"), false_accepts=("false_accepts", "sum")).reset_index()
w(md(gtab)); w()
if (nt.passed == 0).any():
    w("FAILED:"); w(); w(md(nt[nt.passed == 0][["kind", "pq", "mode", "test", "got", "expected", "false_accepts"]])); w()
w("Coverage: tampered payload (R1), tampered signature symbols / Merkle path / batch symbols / MAC tag / disclosed key (R2), wrong signer alone and interleaved with the genuine stream, with the attacker holding its own PQ key and its own random chain secret (R3), "
  "forged message with a disclosed key and receiver clock offsets inside the bound (R4), **replay of an old epoch for every mode** (R5), corrupted anchor and **anchor fields modified after signing: timestamp, disclosure delay, E, epoch id, commitment** (R6, R9), "
  "validly signed but policy-violating schedules (R9), hybrid with invalid Ed25519 half (R7), **symbol injection** (R10), **chain-key derivability regression: the forgery of `review-artifacts/forge_chain_seed.py` against the legacy derivation is rejected (R8) while the same forgery succeeds against the OLD derivation (control C8)**, "
  "and a **forged next-epoch commitment by an attacker without chain keys (R11)**.")
w()

# ---------------------------------------------------------------- cross-check
w("## Closed-form cross-check")
w()
w(f"Source: `raw/loss_crosscheck_{MN}.csv`. The sender's symbol placement is recomputed without cryptography and the probability that an MDS-coded fragmentation object decodes given its own slot arrived is computed exactly (`crosscheck_loss.py`). "
  "z = (measured mean - closed form) / SE with SE = max(SE over seeds, binomial SE sqrt(c(1-c)/(seeds x mean received))); the binomial term only matters where all seeds agree. **Lossless (p = 0) cells are excluded.** Only MDS fragmentation / hybrid modes have an independent closed form in this pass; repetition, Merkle, chain and Gilbert-Elliott loss are not compared.")
w()
nb3 = int(xchk.beyond_3se.sum())
w(f"{len(xchk)} cells compared; **{nb3} differ by more than 3 standard errors** (about {len(xchk) * 0.0027:.1f} expected by chance); max |difference| = {xchk['diff'].abs().max():.4f}; cells with zero seed SE and a non-zero difference: {int(xchk.zero_seed_se_nonzero_diff.sum())}.")
w()
if nb3:
    w(md(xchk[xchk.beyond_3se][["profile", "pq", "mode", "loss_p", "closed", "impl_mean", "impl_sd", "z"]])); w()

# ---------------------------------------------------------------- UDP
w("## Real-UDP mode")
w()
if udp is not None and len(udp):
    w(f"Source: `raw/udp_smoke_{MN}.csv`. Sender and receiver ran as separate processes over loopback (`run_proto.py udp ...`); loss was injected at the receiver from the same seeded mask. `inproc_same_outcome = 1` means the same messages were authenticated in the same slots as an in-process reference run (own keys).")
    w()
    cols = [c for c in ["profile", "pq", "mode", "loss_model", "loss_p", "burst_len", "seed", "authenticated", "N_meas", "udp_frames_sent", "udp_missing", "inproc_same_outcome"] if c in udp]
    w(md(udp[cols])); w()
    w(f"Loopback runs identical to in-process: {int((udp.inproc_same_outcome == 1).sum())}/{len(udp)}. **Not yet run across two machines**: see below.")
else:
    w("No UDP smoke result found.")
w()
# ---------------------------------------------------------------- Q3
w("## Q3: size or timing tail binding")
w()
w(f"Sources: `raw/oqs_timing_{MN}.csv`, `raw/scoring_all_levels.csv`, `results/proto_summary.csv`. x86 VM only; MCU timings are not measured.")
w()
w("Method. Pairs = (lowest-level size class that was benchmarked, signature profile with a stated message rate; dns and the key-space profile excluded). Size-bound: the full signature exceeds the auth budget. "
  "Deadline = packet period (frame period if > 0, else message period). Timing-bound: max(p99 sign, p99 verify) of the class exceeds the deadline; classes with < 100 iterations have no usable tail, and are timing-bound only if the median alone exceeds the deadline, else `insufficient`. "
  "Family is size-bound if size-only pairs exceed timing-only pairs, timing-bound if the reverse, otherwise not distinguishing. Second look from the protocol runs: `tx_realtime_ratio > 1` (sender cannot keep up).")
w()
tt3 = timing.set_index("scheme"); members = pq.groupby("class_id").scheme.apply(list)


def cls_timing(cid):
    ms = [m for m in members[cid] if m in tt3.index]
    if not ms:
        return None
    d = tt3.loc[ms]
    full_n = (d.iterations >= 100).all()
    return full_n, (float(d[["sign_p99_us", "verify_p99_us"]].max(axis=1).max()) if full_n else float("nan")), float(d[["sign_median_us", "verify_median_us"]].max(axis=1).max())


ct = {cid: cls_timing(cid) for cid in main_cls.class_id}
rows = []
for _, r in fl[~fl.profile.isin(["dns"])].iterrows():
    if ct.get(r.class_id) is None:
        continue
    Pf = PROF[r.profile]; D = (Pf["frame_period_s"] or Pf["message_period_s"]) * 1e6
    ok, tail, med = ct[r.class_id]
    tim = ("miss" if tail > D else "ok") if ok else ("miss" if med > D else "insufficient")
    sb = not r.fits
    cl_ = "both" if sb and tim == "miss" else "size-only" if sb else "timing-only" if tim == "miss" else "insufficient" if tim == "insufficient" else "neither"
    rows.append({"family": r.family, "pair_class": cl_})
q3 = pd.DataFrame(rows)
cnt = q3.groupby(["family", "pair_class"]).size().unstack(fill_value=0)
for c_ in ("size-only", "timing-only", "both", "neither", "insufficient"):
    if c_ not in cnt: cnt[c_] = 0
cnt = cnt[["size-only", "timing-only", "both", "neither", "insufficient"]].reset_index()
cnt["pairs"] = cnt[["size-only", "timing-only", "both", "neither", "insufficient"]].sum(axis=1)
cnt["family_binding"] = np.where(cnt["size-only"] > cnt["timing-only"], "size", np.where(cnt["timing-only"] > cnt["size-only"], "timing", "not distinguishing"))
w(md(cnt)); w()
fig, ax = plt.subplots(figsize=(8, 3.5)); bottom = np.zeros(len(cnt))
for c_ in ("size-only", "both", "timing-only", "neither", "insufficient"):
    ax.bar(cnt.family, cnt[c_], bottom=bottom, label=c_); bottom += cnt[c_].values
ax.set_ylabel("(class, profile) pairs"); ax.legend(fontsize=7); plt.xticks(rotation=25, fontsize=7); fig.tight_layout()
fig.savefig(os.path.join(RES, "fig_q3_size_vs_tail.pdf")); plt.close(fig)
w(f"Figure `fig_q3_size_vs_tail.pdf` (source `raw/oqs_timing_{MN}.csv`, `raw/scoring_all_levels.csv`).")
w()

slow = rtt[rtt.tx_realtime_ratio > 1]
nsz = int((cnt.family_binding == "size").sum()); ntm = int((cnt.family_binding == "timing").sum()); nnd = int((cnt.family_binding == "not distinguishing").sum())
w(f"Sender real-time check (protocol runs at the native rate): {len(slow)}/{len(rtt)} (profile, scheme, mode) configurations have a sender slower than the slot period on this machine (details in the Q2 section).")
w()
w(f"**Verdict Q3: size is binding in {nsz} of {len(cnt)} families, timing in {ntm}, not distinguishing in {nnd}** (rule above). Supported for x86 under this rule; inconclusive for constrained devices (no MCU data). Q3 is close to tautological because the deadlines are packet periods much longer than x86 operation times.")
w()

# ---------------------------------------------------------------- verdict table
V = pd.DataFrame(VERD).sort_values("hypothesis", key=lambda c: c.str[1:].astype(int)).reset_index(drop=True)
V.to_csv(os.path.join(RES, "verdicts.csv"), index=False)
pd.concat(PD_ALL).to_csv(os.path.join(RES, "paired_differences.csv"), index=False)
agg = res.groupby(["profile", "pq", "mode", "cond"]).agg(seeds=("seed", "nunique"), feasible=("feasible", "first"), share=("share", "mean"), share_sd=("share", "std"), within_an=("within_an", "mean"),
                                                         rmst_ms=("rmst_ms", "mean"), air_bytes_per_auth=("air_bytes_per_auth", "mean"), rx_cpu_us=("rx_cpu_us_per_msg", "mean"), tx_cpu_us=("tx_cpu_us_per_msg", "mean"),
                                                         ttfa_ms=("ttfa_ms", lambda x: pd.to_numeric(x, errors="coerce").mean()), ttfa_censored=("ttfa_censored", "mean"), false_accepts=("false_accepts", "sum")).reset_index()
agg.to_csv(os.path.join(RES, "proto_summary.csv"), index=False)
w("## Verdicts (all hypotheses)")
w()
w(f"Source: `results/verdicts.csv`, computed above with the rules of `hypotheses.yaml`. " + ("**All PROVISIONAL: smoke run (`cloud-smoke`).**" if smoke else ""))
w()
w(md(V[["hypothesis", "iid", "burst", "verdict", "claim"]])); w()
jt = agg[(agg.cond == "iid 0.1") & (agg.feasible == 1)].groupby("mode").ttfa_ms.mean().reindex(MO.MODES)
jc = agg[(agg.cond == "iid 0.1") & (agg.feasible == 1)].groupby("mode").ttfa_censored.mean().reindex(MO.MODES)
w("Late-joiner time to first authenticated message at iid 0.1 (ms, mean over the feasible (profile, scheme) pairs and seeds where it exists; fraction censored = no authentication before the end of the run):"); w()
w(md(pd.DataFrame({"mode": MO.MODES, "join_ms": jt.values, "censored": jc.values}).round(1))); w()

# ---------------------------------------------------------------- statements
w("## Properties and limits (statements, not measurements)")
w()
w("- **The chain provides no non-repudiation.** Any receiver holding the disclosed key can compute valid tags; only the per-message signature and Merkle-batch modes give transferable evidence.")
w("- **The chain needs loose time synchronisation and fails open beyond it**: with the receiver clock behind by more than the slack the delayed-forgery attacker succeeds (attacker section, (ii)); a receiver ahead of the sender only loses honest messages.")
w("- **Anchor and schedule are signed**: the receiver takes epoch start, slot period, E, disclosure delay, tag / key length and the continuity flag from a verified anchor and applies a local policy (`D_MIN`..`D_MAX`, slot period, E); an anchor older than its epoch plus the freshness bound is rejected. Epoch ids in frame headers are 16 bit (wrap after 36 h at E = 20, 100 ms); the full 32-bit id is inside the signed anchor and the freshness check prevents aliasing.")
w("- **Chain keys are secret per stream** (os.urandom); tags and keys are not reused across schemes or variants. The pass-3 forgery is a regression test.")
w("- **Freshness for fragment and Merkle modes** uses a signed timestamp (6 B, Unix ms: the 32-bit ms timestamp of pass 3 would wrap after 49.7 days) and a replay window; the added bytes are counted inside the blobs.")
w("- **Python receivers and ctypes**: CPU numbers are for Python receivers on a cloud VM and are not MCU or OBU numbers.")
w("- Hybrid: both signatures must verify (R7); stripping the classical half is rejected; downgrade resistance beyond this is not analysed.")
w("- Not modelled: collisions / congestion, a stronger pollution attacker (several bogus frames per slot, tampered key chain disclosure order), selective jamming beyond the delayed-forgery pattern, per-symbol authentication of signature symbols (circular, see attacker section), mixed PQ-CA certificate chains, ZK-compressed signatures.")
w()

# ---------------------------------------------------------------- runs needed / timing
w("## Runs still needed (on the user's own machines)")
w()
w("- `MACHINE_NAME=<name> ./run.sh` (full run: 20 seeds operating point, 10 seeds minimum budget and attacker, full loss grid, full budget grid) on every target machine; numbers here are `cloud-smoke` QUICK numbers (6 loss conditions, 2 budget-sweep conditions, coarser grids) unless the tags above say otherwise. Publication numbers need a clean git tree (`git_dirty = 0`).")
w("- Statistics that are only meaningful from the full run: the per-scheme confidence intervals (H1-H3), the minimum-budget cells (H5; the QUICK grid has 2 conditions and 6 budgets), the burst-length table (QUICK uses one stationary loss for bursts 3 / 5 / 10) and the attacker pairs at the full set of injection rates and clock offsets.")
w("- Two-machine UDP run on a LAN: receiver `run_proto.py udp --role receiver --udp 0.0.0.0:9000 --keyfile K ...`, sender `--role sender --udp RECEIVER:9000 --start-delay 60 ...` with identical `--profile --pq --mode --seed`; copy the sender's keyfile to the receiver during the delay (see `udp_link.py`).")
w("- MCU timings (Cortex-M) for the non-standardised families; measured loss traces of the real channels; C-V2X PC5 Mode 4 scheduling, congestion and PDR (not modelled: slots are collision-free).")
w("- TODO-RESULT inputs: certificate metadata size, SIB1 latency need, BSM size for 437 B, LMS H=15/20 rows, remote_id/dns message rates, a primary source for the 100 ms C-V2X authentication budget (currently the survey mamun2026post).")
w("- Not done in this pass: per-symbol authentication of signature symbols (impossible without a second signature, see above); a stronger multi-frame pollution attacker; Remote ID and DNS in the real-protocol experiments.")
w()
if phases is not None and rt is not None:
    w("## Run time of this run")
    w()
    w(md(phases)); w()
    if ptime is not None:
        w(f"Slowest (profile, scheme) tasks of the protocol sweep (`raw/proto_pairtime_{MN}.csv`):"); w(); w(md(ptime.sort_values("secs", ascending=False).head(6)[["profile", "pq", "secs", "build_s", "n_builds", "rows_oper", "rows_minb", "rows_attack"]])); w()
    from estimate_duration import estimate
    e = estimate(RAW, MN)
    if e:
        parts, procs = e
        w(f"Estimated duration of the FULL run (`./run.sh` without QUICK) on {procs} cores, scaled from this QUICK run (`estimate_duration.py`; +-40%):"); w()
        w(md(pd.DataFrame([{"phase": k, "minutes": v / 60} for k, v in parts.items()] + [{"phase": "TOTAL", "minutes": sum(parts.values()) / 60}]), ".1f")); w()
open(os.path.join(RES, "summary.md"), "w").write("\n".join(L) + "\n")
print("summary.md written:", len(L), "lines")
