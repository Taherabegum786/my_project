"""E5 experiments.  python -m sim.run_sim --exp {sweep_delta,controller,dissem,e2e,sens,validate} --reps R --out DIR
Common random numbers: replicate r uses seed SEED+1000r for every policy/mode.  Crypto costs: native OpenSSL 3.5.4
(primary, --backend native) or Python E1 (--backend python).  QUICK=1 shortens horizons."""
import argparse
import csv
import json
import os
import sys
import time
from multiprocessing import get_context

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sim import fleet_mc as F
from sim import model as Mo
from sim.engine import NB_TS, Sim
from sim.fleet_mc import MODES, Costs
from sim.workload import DEFAULTS, SEED, dump_params, lognorm

QUICK = os.environ.get("QUICK", "0") == "1"
FIX5 = [0.01, 0.1, 1.0, 10.0, 60.0]
FIX_ORACLE = [0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0]
T_CRIT = {2: 12.706, 3: 4.303, 4: 3.182, 5: 2.776, 6: 2.571, 7: 2.447, 8: 2.365, 9: 2.306, 10: 2.262}


def tci(x):
    x = np.asarray(x, float)
    n = len(x)
    m = float(x.mean())
    if n < 2:
        return m, m, m
    h = T_CRIT.get(n, 1.96) * x.std(ddof=1) / np.sqrt(n)
    return m, m - h, m + h


def write(path, rows, mode="w"):
    if not rows:
        return
    new = mode == "w" or not os.path.exists(path)
    with open(path, mode, newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        if new:
            w.writeheader()
        for r in rows:
            w.writerow({k: (("%.6g" % v) if isinstance(v, (float, np.floating)) else v) for k, v in r.items()})


def pmap(fn, tasks, procs):
    if procs <= 1:
        return [fn(t) for t in tasks]
    with get_context("fork").Pool(procs) as pool:
        return pool.map(fn, tasks, chunksize=1)


ARGS = None
COSTS = {}


def costs(backend="native", rs="ML-DSA-44", n=16):
    k = (backend, rs, n)
    if k not in COSTS:
        COSTS[k] = Costs(os.environ.get("EMBER_COSTS_DIR", ARGS.out), backend, rs, n)
    return COSTS[k]


# ============================================================ sweep_delta
def _sweep_task(t):
    lam, pool, rep, hor, backend = t
    pols = ["fixed:%g" % d for d in FIX5 if not (d == 0.01 and lam < 2000)] + ["wc", "adaptive"]
    s = Sim(costs(backend), lam_bar=lam, diurnal_a=0.0, horizon_s=hor)
    t0 = time.time()
    acc = s.run(rep, pols, MODES, pool=pool)
    rows = []
    for (pol, m), A in acc.items():
        r = s.summary(A)
        rows.append(dict(mode=m, policy=pol, delta_s=pol.split(":")[1] if ":" in pol else "", lambda_bar=lam, E=s.E,
                         alpha_e=s.p["alpha_e"], pool=pool, rep=rep, backend=backend, horizon_s=hor,
                         **{k: r[k] for k in ("issue_wait_mean_s", "issue_wait_p99_s", "miss_per_token", "miss_per_mreq",
                                              "miss_latency_p99_ms", "D_mean_s", "root_bw_fleet_Bps", "root_bw_ratio",
                                              "edge_cpu_us_per_req_mean", "edge_cpu_us_per_req_p99",
                                              "sig_verifs_per_edge_per_s", "tok_bytes_p50", "tok_bytes_max",
                                              "model_miss_per_token", "model_D_s", "frac_req_waiting")}))
    print("sweep lam=%g pool=%d rep=%d %s done in %.0f s" % (lam, pool, rep, backend, time.time() - t0), flush=True)
    return rows


def exp_sweep(a):
    hz = {200: 3600.0, 2000: 3600.0, 20000: a.hor20k}
    if QUICK:
        hz = {200: 600.0, 2000: 600.0, 20000: 120.0}
    tasks = [(lam, pool, r, hz[lam], "native") for lam in (200, 2000, 20000) for pool in (0, 1)
             for r in range(a.reps) if not (lam == 20000 and pool == 1)]
    tasks += [(2000, 0, r, hz[2000], "python") for r in range(a.reps)]  # second cost source (E1 python)
    tasks.sort(key=lambda t: -t[0] * t[3])
    rows = sum(pmap(_sweep_task, tasks, a.procs), [])
    write(os.path.join(a.out, "sim_delta_sweep.csv"), rows)
    return {"sweep_delta_horizon_s": hz}


# ============================================================ controller (24 h diurnal)
def _ctrl_task(t):
    lam, rep, t0, t1, ts = t
    pols = ["adaptive", "wc"] + ["fixed:%g" % d for d in FIX_ORACLE]
    s = Sim(costs(), lam_bar=lam, diurnal_a=DEFAULTS["diurnal_a"], horizon_s=t1)
    tt = time.time()
    acc = s.run(rep, pols, ["pull"], t0=t0, t1=t1, ts=ts)
    slo = s.p["slo_s"]
    dmax = Mo.d_max(s.p["budget_B"], s.p["claims_bytes"], s.p["n"])
    summ, tsrows, dec = [], [], {}
    for (pol, m), A in acc.items():
        r = s.summary(A)
        p99bins = np.array([F.hist_q(h, 0.99) if h.sum() else np.nan for h in A.ts_hW])
        valid = A.ts_n > 0
        slo_v = float(np.mean(p99bins[valid] > slo))
        bud_v = float(A.d_hist[dmax + 1:].sum() / A.d_hist.sum())
        summ.append(dict(policy=pol, mode=m, pool=0, rep=rep, lambda_bar=lam, horizon_s=t1 - t0, D_mean_s=r["D_mean_s"],
                         issue_wait_mean_s=r["issue_wait_mean_s"], issue_wait_p99_s=r["issue_wait_p99_s"],
                         slo_violation_frac=slo_v, budget_violation_frac=bud_v, miss_per_token=r["miss_per_token"],
                         root_bw_fleet_Bps=r["root_bw_fleet_Bps"], tokens=r["tokens"]))
        dec[pol] = (A.dec_D.copy(), A.dec_n.copy(), slo_v)
        if rep == 0 and pol in ("adaptive", "fixed:0.1", "fixed:1", "fixed:10", "wc"):
            bl = (t1 - t0) / NB_TS
            for b in range(NB_TS):
                if A.ts_n[b] == 0:
                    continue
                tsrows.append(dict(policy=pol, mode=m, lambda_bar=lam, t_bin_s=t0 + b * bl, lambda_hat=A.ts_n[b] / bl,
                                   delta_chosen_s=A.ts_delta[b] / A.ts_n[b], issue_wait_p99_s=p99bins[b],
                                   miss_per_token=A.ts_miss[b] / A.ts_n[b], D_mean_s=A.ts_D[b] / A.ts_n[b],
                                   tok_bytes_max=Mo.token_bytes(s.p["claims_bytes"], s.p["n"], int(A.ts_dmax[b])),
                                   slo_violation=int(p99bins[b] > slo)))
    # oracles from the fixed grid at the same seeds (hindsight)
    fx = [p for p in dec if p.startswith("fixed:")]
    tot_n = dec[fx[0]][1].sum()
    for name, cand in (("oracle_fixed", fx), ("oracle_fixed_slo", [p for p in fx if dec[p][2] == 0.0])):
        if not cand:
            continue
        best_single = min(cand, key=lambda p: dec[p][0].sum() / dec[p][1].sum())
        Dd = sum(min(dec[p][0][k] / max(dec[p][1][k], 1) for p in cand) * dec[fx[0]][1][k] for k in range(10))
        choice = [min(cand, key=lambda p: dec[p][0][k] / max(dec[p][1][k], 1)) for k in range(10)]
        summ.append(dict(policy=name, mode="pull", pool=0, rep=rep, lambda_bar=lam, horizon_s=t1 - t0, D_mean_s=Dd / tot_n,
                         issue_wait_mean_s="", issue_wait_p99_s="", slo_violation_frac="", budget_violation_frac="",
                         miss_per_token="", root_bw_fleet_Bps="", tokens=tot_n,
                         ))
        summ[-1]["oracle_choice"] = "|".join(c.split(":")[1] for c in choice)
        summ.append(dict(summ[-1], policy=name.replace("oracle_fixed", "best_single_fixed"),
                         D_mean_s=dec[best_single][0].sum() / dec[best_single][1].sum(), oracle_choice=best_single.split(":")[1]))
    for r in summ:
        r.setdefault("oracle_choice", "")
    print("controller lam=%g rep=%d done in %.0f s" % (lam, rep, time.time() - tt), flush=True)
    return summ, tsrows


def exp_controller(a):
    H = 3600.0 if QUICK else a.ctrl_hours * 3600.0
    reps = a.reps if QUICK else max(a.reps, 10)
    tasks = [(lam, r, 0.0, H, True) for lam in (200, 2000) for r in range(reps)]
    tasks += [(20000, r, 10800.0, 10800.0 + (600.0 if QUICK else 3600.0), True) for r in range(min(5, reps))]
    tasks.sort(key=lambda t: -t[0] * (t[3] - t[2]))
    res = pmap(_ctrl_task, tasks, a.procs)
    write(os.path.join(a.out, "sim_controller_summary.csv"), sum([r[0] for r in res], []))
    write(os.path.join(a.out, "sim_controller_ts.csv"), sum([r[1] for r in res], []))
    return {"controller_horizon_s": {"200": H, "2000": H, "20000": "1 h peak window [10800, 14400] s"},
            "controller_reps": reps}


# ============================================================ dissemination (+ B11/B12)
def _dissem_task(t):
    E, delta, P, rep, hor = t
    s = Sim(costs(), E=E, lam_bar=2000.0, diurnal_a=0.0, horizon_s=hor, P_s=P)
    acc = s.run(rep, ["fixed:%g" % delta], MODES)
    rows = []
    c = s.c
    for (pol, m), A in acc.items():
        r = s.summary(A)
        vmax = s.p["v_max_s"]
        epochs_rate = A.epochs / s.horizon
        # per-edge root state upper bound: every epoch root of every tenant within V_max
        if m in ("pull_rollup", "push_rollup"):
            state = epochs_rate * vmax * (c.n + 20)              # verified roots kept as (meta, n-byte root)
        else:
            state = epochs_rate * vmax * (c.n + 20 + c.sig_bytes)  # signed roots kept
        rows.append(dict(scheme="EMBER-O1", mode=m, E=E, delta_s=delta, P_s=P, rep=rep,
                         root_bw_fleet_Bps=r["root_bw_fleet_Bps"], root_bw_per_edge_Bps=r["root_bw_fleet_Bps"] / E,
                         miss_per_mreq=r["miss_per_mreq"], miss_per_token=r["miss_per_token"],
                         edge_root_state_bytes=state,
                         staple_bytes_per_session=r["staple_bytes_per_session"],
                         refresh_per_session=r["refresh_per_session"],
                         revocation_propagation_s=_revocation(m, P, s, rep),
                         frac_req_waiting=r["frac_req_waiting"], root_bw_ratio=r["root_bw_ratio"]))
    # B11 (delegated Ed25519): one ML-DSA-44-signed cert per kid per V_max, same pull path; per tenant
    # B12 (KEM-wrapped HMAC): push-only, per epoch Delta, E wraps of (1088 + 48) B, per tenant with traffic
    T = s.p["T"]
    cert_bytes = 48 + 2420 + 40
    tenants_active = T
    rows.append(dict(scheme="B11", mode="pull", E=E, delta_s=s.p["v_max_s"], P_s=P, rep=rep,
                     root_bw_fleet_Bps=(E + s.S) * tenants_active * cert_bytes / s.p["v_max_s"],
                     root_bw_per_edge_Bps=tenants_active * cert_bytes / s.p["v_max_s"], miss_per_mreq="",
                     miss_per_token="", edge_root_state_bytes=2 * tenants_active * (32 + 8),
                     staple_bytes_per_session=0, refresh_per_session="", revocation_propagation_s="",
                     frac_req_waiting="", root_bw_ratio=""))
    wrap = 1088 + 48
    A0 = acc[("fixed:%g" % delta, "pull")]
    rows.append(dict(scheme="B12", mode="push", E=E, delta_s=delta, P_s=P, rep=rep,
                     root_bw_fleet_Bps=E * wrap * A0.epochs / s.horizon, root_bw_per_edge_Bps=wrap * A0.epochs / s.horizon,
                     miss_per_mreq="", miss_per_token="", edge_root_state_bytes=(A0.epochs / s.horizon) * s.p["v_max_s"] * 36,
                     staple_bytes_per_session=0, refresh_per_session="", revocation_propagation_s="",
                     frac_req_waiting="", root_bw_ratio=""))
    print("dissem E=%d delta=%g P=%g rep=%d" % (E, delta, P, rep), flush=True)
    return rows


def _revocation(mode, P, s, rep):
    """Mean time for a revocation published at a uniform random time to reach an edge (simulated by sampling):
    pull modes: edges refresh the signed revocation delta with each period close (uniform residual of P) + fetch RTT;
    push modes: push propagation delay."""
    r = np.random.default_rng(SEED + 1000 * rep + 99)
    n = 20000
    if mode.startswith("push"):
        v = lognorm(r, s.pu, n)
    else:
        v = r.uniform(0, P, n) + lognorm(r, s.es, n) + lognorm(r, s.sr, n)
    return float(v.mean())


def exp_dissem(a):
    hor = 600.0 if QUICK else 1800.0
    tasks = [(E, d, 300.0, r, hor) for E in (100, 500, 2000) for d in (0.1, 1.0, 10.0) for r in range(a.reps)]
    rows = sum(pmap(_dissem_task, tasks, a.procs), [])
    write(os.path.join(a.out, "sim_dissem.csv"), rows)
    return {"dissem_horizon_s": hor}


# ============================================================ end-to-end latency CDF
def _e2e_task(t):
    rep, hor, delta = t
    s = Sim(costs(), lam_bar=2000.0, diurnal_a=0.0, horizon_s=hor)
    res = {("fixed:%g" % delta, m): [] for m in MODES}
    s.run(rep, ["fixed:%g" % delta], MODES, e2e_res=res)
    rng = np.random.default_rng(SEED + 1000 * rep + 5)
    out = []
    c = s.c
    per = 20000
    for (pol, m), chunks in res.items():
        rw = np.concatenate([x[0] for x in chunks]); rk = np.concatenate([x[1] for x in chunks])
        dd = np.concatenate([x[2] for x in chunks]); req = np.concatenate([x[3] for x in chunks])
        nver = np.concatenate([x[4] for x in chunks])
        R = req.sum()
        # sample requests uniformly: pick a token with prob ~ requests, then whether it is a verifying request
        tk = rng.choice(req.size, per, p=req / R)
        isv = rng.uniform(0, 1, per) < nver[tk] / req[tk]
        cpu = c.path_cost(dd[tk]) + isv * c.t_verify
        wait = np.zeros(per)
        # waiting requests: fraction len(rw)/R of all requests; draw their waits from rw
        iw = rng.uniform(0, 1, per) < rw.size / R
        wait[iw] = rng.choice(rw, iw.sum()) if rw.size else 0.0
        for v in (wait + cpu):
            out.append(dict(scheme="EMBER-O1", mode=m, rep=rep, sample_ms=v * 1000))
    # per-token baselines: no root misses; CPU per request from native verify costs
    nat = c
    import pandas as pd
    cdir = os.environ.get("EMBER_COSTS_DIR", ARGS.out)
    ns = pd.read_csv(os.path.join(cdir, "native_sig_agg.csv"))
    pv = pd.read_csv(os.path.join(cdir, "native_pathverify_agg.csv"))

    def n_(s_, op):
        return float(ns[(ns.scheme == s_) & (ns.op == op)].median_us.iloc[0]) * 1e-3

    def p_(op):
        return float(pv[(pv.impl == "evp") & (pv.op == op)].ns_median.iloc[0]) * 1e-6
    K = rng.geometric(1 / 150, per) + 1.0
    first = rng.uniform(0, 1, per) < 1.0 / K   # the request is the first one of its session at this edge
    base = {"B1-HMAC": np.full(per, p_("hmac_sha256_200B")), "B2-Ed25519": np.full(per, n_("ED25519", "verify")),
            "B3-ECDSA": np.full(per, n_("ECDSA-P256", "verify")), "B5-ML-DSA-44": np.full(per, n_("ML-DSA-44", "verify")),
            "B5v-ML-DSA-44+vcache": np.where(first, n_("ML-DSA-44", "verify") + p_("sha256_3500B"), p_("sha256_3500B")),
            "B11-DelegEd25519": np.full(per, n_("ED25519", "verify")), "B12-KEM-HMAC": np.full(per, p_("hmac_sha256_200B"))}
    for k, v in base.items():
        for x in v:
            out.append(dict(scheme=k, mode="none", rep=rep, sample_ms=x))
    print("e2e rep=%d" % rep, flush=True)
    return out


def exp_e2e(a):
    hor = 600.0 if QUICK else 1800.0
    rows = sum(pmap(_e2e_task, [(r, hor, 1.0) for r in range(a.reps)], a.procs), [])
    write(os.path.join(a.out, "sim_e2e_latency.csv"), rows)
    return {"e2e": "lam_bar=2000, Delta=1 s, horizon %g s, 20000 samples per (scheme, mode, rep)" % hor}


# ============================================================ sensitivity
SENS = [("rtt_scale", [0.5, 1.0, 2.0]), ("alpha_e", [0.0, 0.8, 1.2]), ("alpha_t", [0.8, 1.0, 1.2]),
        ("P_s", [60.0, 300.0, 1800.0]), ("seg_bytes", [0.5e6, 1.5e6, 4e6]), ("p_move", [0.0, 0.0005, 0.005]),
        ("v_max_s", [300.0, 3600.0, 86400.0]), ("n", [16, 32]), ("root_signer", ["ML-DSA-44", "ML-DSA-65", "SLH-DSA-128s", "Hybrid-Ed25519+ML-DSA-44"]),
        ("E", [100, 500, 2000])]


def _sens_task(t):
    param, val, rep, hor = t
    kw = {param: val} if param not in ("root_signer", "n") else {}
    cs = costs("native", val if param == "root_signer" else "ML-DSA-44", val if param == "n" else 16)
    s = Sim(cs, lam_bar=2000.0, diurnal_a=0.0, horizon_s=hor, **kw)
    if param == "n":
        s.p["n"] = val
    pols = ["fixed:1", "adaptive"] + (["fixed:%g" % d for d in (0.01, 0.1, 10.0, 60.0)] if param == "E" else [])
    acc = s.run(rep, pols, ["pull", "pull_staple", "pull_rollup"])
    rows = []
    for (pol, m), A in acc.items():
        r = s.summary(A)
        for met in ("miss_per_token", "D_mean_s", "root_bw_ratio", "edge_cpu_us_per_req_mean", "edge_cpu_us_per_req_p99",
                    "root_bw_fleet_Bps", "tok_bytes_max", "refresh_per_session", "issue_wait_mean_s"):
            rows.append(dict(param=param, value=val, policy=pol, mode=m, rep=rep, metric=met, v=r[met]))
    print("sens %s=%s rep=%d" % (param, val, rep), flush=True)
    return rows


def exp_sens(a):
    hor = 300.0 if QUICK else 1800.0
    tasks = [(p, v, r, hor) for p, vals in SENS for v in vals for r in range(a.reps)]
    raw = sum(pmap(_sens_task, tasks, a.procs), [])
    write(os.path.join(a.out, "sim_sens_raw.csv"), raw)
    import pandas as pd
    d = pd.DataFrame(raw)
    d["v"] = pd.to_numeric(d["v"], errors="coerce")
    rows = []
    for (p, v, pol, m, met), g in d.groupby(["param", "value", "policy", "mode", "metric"], sort=False):
        mm, lo, hi = tci(g.v.values)
        rows.append(dict(param=p, value=v, policy=pol, mode=m, metric=met, mean=mm, ci_lo=lo, ci_hi=hi, reps=len(g)))
    write(os.path.join(a.out, "sim_sens.csv"), rows)
    return {"sens_horizon_s": hor}


# ============================================================ validate (DES vs MC: internal consistency)
def exp_validate(a):
    from sim.des import run_des
    rows = []
    hor = 600.0 if QUICK else 3600.0
    for m in MODES:
        for d in (0.1, 1.0, 10.0):
            dv, mv = {"miss_per_token": [], "issue_wait_mean_s": [], "D_mean_s": []}, {"miss_per_token": [], "issue_wait_mean_s": [], "D_mean_s": []}
            for r in range(a.reps):
                s = Sim(costs(), lam_bar=200.0, E=100, T=50, diurnal_a=0.0, horizon_s=hor)
                A = s.run(r, ["fixed:%g" % d], [m])[("fixed:%g" % d, m)]
                sm = s.summary(A)
                de = run_des(s, r, d, m, 0.0, hor)
                for k in dv:
                    dv[k].append(de[k]); mv[k].append(sm[k])
            for k in dv:
                dm, dlo, dhi = tci(dv[k]); mm, mlo, mhi = tci(mv[k])
                diff = np.array(dv[k]) - np.array(mv[k])
                pm, plo, phi = tci(diff)
                rows.append(dict(mode=m, delta=d, metric=k, des_value=dm, des_ci_lo=dlo, des_ci_hi=dhi, mc_value=mm,
                                 mc_ci_lo=mlo, mc_ci_hi=mhi, rel_diff=(dm - mm) / mm if mm else 0.0,
                                 paired_diff_ci_lo=plo, paired_diff_ci_hi=phi, label="internal_consistency"))
            print("validate", m, d, flush=True)
    write(os.path.join(a.out, "sim_validate.csv"), rows)
    return {"validate_horizon_s": hor}


# ============================================================ R1: operating region (reviewer M1/M2, checklist 1-2)
R1_POOLS = {"tenant": (0, {}), "shard8": (1, {"n_shards": 8}), "global": (1, {"n_shards": 1}),
            "region10": (2, {"regions": 10}), "region50": (2, {"regions": 50})}
R1_MODES = ["pull", "pull_staple", "staple_always"]
R1_KEYS = ("frac_tok_N1", "frac_tok_N_le4", "d_p50", "d_p99", "tok_bytes_p50", "tok_bytes_p99", "mean_tokens_per_tree",
           "issuer_sigs_per_s", "issuer_cpu_cores", "issuer_cpu_us_per_token", "issue_wait_mean_s", "issue_wait_p99_s",
           "miss_per_token", "frac_req_waiting", "miss_latency_p99_ms", "D_mean_s", "staple_installs_per_token",
           "moves_per_token", "staple_bytes_per_session", "edge_cpu_us_per_req_mean", "edge_cpu_us_per_req_p99",
           "sig_verifs_per_edge_per_s", "req_per_sig_verify", "busiest_edge_req_per_s", "busiest_edge_verifs_per_s",
           "busiest_edge_cpu_frac", "max_edge_cpu_frac", "fleet_edge_cpu_cores", "root_bw_fleet_Bps", "root_bw_ratio")


def _oprg_task(t):
    lam, pname, rep, hor, pols, extra = t
    pool, kw = R1_POOLS[pname]
    s = Sim(costs(), lam_bar=lam, diurnal_a=0.0, horizon_s=hor, **kw, **extra)
    t0 = time.time()
    acc = s.run(rep, pols, R1_MODES, pool=pool)
    rows, drows = [], []
    for (pol, m), A in acc.items():
        r = s.summary(A)
        base = dict(lambda_bar=lam, pooling=pname, policy=pol, mode=m, rep=rep, horizon_s=hor,
                    **{k: v for k, v in extra.items()})
        rows.append(dict(base, **{k: r[k] for k in R1_KEYS}))
        if m == "pull":
            for k in range(10):
                if ("dec%d_tokens" % k) in r:
                    drows.append(dict(base, mode="any", decile=k, tokens=r["dec%d_tokens" % k],
                                      frac_tok_N1=r["dec%d_frac_N1" % k], d_p50=r["dec%d_d_p50" % k]))
    print("oprg lam=%g %s rep=%d %s done in %.0f s" % (lam, pname, rep, extra, time.time() - t0), flush=True)
    return rows, drows


def exp_oprg(a):
    hz = {200: 3600.0, 2000: 3600.0, 20000: a.hor20k}
    if QUICK:
        hz = {200: 300.0, 2000: 300.0, 20000: 60.0}
    pols = ["fixed:0.01", "fixed:0.1", "fixed:1", "wc"]
    tasks = []
    for lam in (200, 2000, 20000):
        for pname in R1_POOLS:
            for r in range(a.reps):
                tasks.append((lam, pname, r, hz[lam], pols + (["pertoken"] if pname == "tenant" else []), {}))
    tasks.sort(key=lambda t: -t[0] * t[3] * (2 if t[1].startswith("region") else 1))
    res = pmap(_oprg_task, tasks, a.procs)
    write(os.path.join(a.out, "sim_oprg.csv"), sum([r[0] for r in res], []))
    write(os.path.join(a.out, "sim_oprg_deciles.csv"), sum([r[1] for r in res], []))
    return {"oprg_horizon_s": hz, "oprg_note": "R1 operating-region sweep; pooling tenant/shard8/global/region10/region50"}


def exp_pmove(a):
    """R1 (reviewer M4, checklist 5): stapling sensitivity to the per-segment re-route probability."""
    hor = 300.0 if QUICK else 1800.0
    tasks = []
    for pm in (0.0, 1e-4, 2e-4, 5e-4, 1e-3, 2e-3, 5e-3, 1e-2):
        for pname, pols in (("tenant", ["fixed:0.01", "fixed:1", "pertoken"]), ("global", ["fixed:0.01", "wc"])):
            for r in range(a.reps):
                tasks.append((2000.0, pname, r, hor, pols, {"p_move": pm}))
    res = pmap(_oprg_task, tasks, a.procs)
    write(os.path.join(a.out, "sim_pmove.csv"), sum([r[0] for r in res], []))
    return {"pmove_horizon_s": hor}


def main():
    global ARGS
    ap = argparse.ArgumentParser()
    ap.add_argument("--exp", required=True)
    ap.add_argument("--reps", type=int, default=5)
    ap.add_argument("--out", default="../results")
    ap.add_argument("--procs", type=int, default=3)
    ap.add_argument("--hor20k", type=float, default=1200.0)
    ap.add_argument("--ctrl_hours", type=float, default=24.0)
    ARGS = a = ap.parse_args()
    t0 = time.time()
    info = {"exp_sweep": exp_sweep, "sweep_delta": exp_sweep, "controller": exp_controller, "dissem": exp_dissem,
            "e2e": exp_e2e, "sens": exp_sens, "validate": exp_validate,
            "oprg": exp_oprg, "pmove": exp_pmove}[a.exp](a)
    info = info or {}
    info["%s_wall_s" % a.exp] = round(time.time() - t0, 1)
    info["%s_costs_dir" % a.exp] = os.environ.get("EMBER_COSTS_DIR", a.out)
    pj = os.path.join(a.out, "sim_params.json")
    prev = {}
    if os.path.exists(pj):
        with open(pj) as f:
            prev = json.load(f)
    prev.update(info)
    dump_params(pj, prev)
    print("%s done in %.0f s" % (a.exp, time.time() - t0))


if __name__ == "__main__":
    main()
