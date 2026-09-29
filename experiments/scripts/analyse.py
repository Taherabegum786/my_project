#!/usr/bin/env python3
"""Summarise E1/E2 results into CSV tables and paper figures.

Statistics: mean with 95% CI of the mean (normal approximation over all
handshakes, which are pooled over interleaved rounds), median and tail
percentiles.  The DAPV-minus-synchronous latency difference is reported with
a 95% bootstrap CI (2000 resamples) of the difference in medians.
"""
import csv, glob, os, random, statistics as st
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "results")
FIG = os.path.join(ROOT, "figures")
os.makedirs(FIG, exist_ok=True)
random.seed(1)

# Reference categorical palette (slots 1-4) + neutral for the classical baseline.
C = {"none": "#2a78d6", "pool2": "#eb6834", "thread": "#1baf7a", "classical": "#6b6a66"}
LABEL = {"none": "synchronous", "pool2": "DAPV, pool (M=2)", "thread": "DAPV, thread/job"}
ALGNAME = {"p256": "P-256", "p256_mldsa44": "P-256+ML-DSA-44",
           "p256_falcon512": "P-256+FN-DSA-512", "p384_mldsa65": "P-384+ML-DSA-65",
           "p256_sphincssha2128fsimple": "P-256+SLH-DSA-128f"}
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": "#e6e5e1", "grid.linewidth": 0.6,
                     "axes.edgecolor": "#8a8984", "axes.axisbelow": True})


def pct(xs, p):
    xs = sorted(xs)
    k = (len(xs) - 1) * p
    lo = int(k)
    hi = min(lo + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def ci(xs):
    m = st.mean(xs)
    h = 1.96 * st.stdev(xs) / len(xs) ** 0.5 if len(xs) > 1 else 0
    return m, h


def boot_median_diff(a, b, n=2000):
    d = []
    for _ in range(n):
        ra = [random.choice(a) for _ in a]
        rb = [random.choice(b) for _ in b]
        d.append(st.median(ra) - st.median(rb))
    return st.median(a) - st.median(b), pct(d, 0.025), pct(d, 0.975)


# ---------------------------------------------------------------- E1
def load_e1():
    hs, jobs = defaultdict(list), defaultdict(list)
    for f in glob.glob(os.path.join(RES, "e1", "rtt*", "*_hs.csv")):
        rtt = int(os.path.basename(os.path.dirname(f))[3:])
        alg, chain, group, wm, _r = os.path.basename(f)[:-7].split("__")
        key = (rtt, alg, chain, group, wm)
        jf = f.replace("_hs.csv", "_jobs.csv")
        if not os.path.exists(jf):  # run still in progress
            continue
        with open(f) as fh:
            hs[key] += list(csv.DictReader(fh))
        with open(jf) as fh:
            jobs[key] += list(csv.DictReader(fh))
    return hs, jobs


def e1():
    hs, jobs = load_e1()
    if not hs:
        return
    rows = []
    for key in sorted(hs):
        rtt, alg, chain, group, wm = key
        h = [float(r["hs_ms"]) for r in hs[key]]
        full = [float(r["full_ms"]) for r in hs[key]]
        j = jobs[key]
        dt = [float(r["dt_us"]) / 1000 for r in j]
        cr = [float(r["crypto_us"]) / 1000 for r in j]
        q = [float(r["queue_us"]) / 1000 for r in j]
        m, hci = ci(h)
        rows.append(dict(
            rtt_ms=rtt, alg=alg, chain=chain, group=group, worker=wm, n=len(h),
            hs_mean=round(m, 4), hs_ci95=round(hci, 4), hs_median=round(st.median(h), 4),
            hs_p95=round(pct(h, .95), 4), full_median=round(st.median(full), 4),
            full_p95=round(pct(full, .95), 4),
            pq_jobs_per_hs=round(len(j) / len(h), 2) if h else 0,
            pq_fail=sum(1 for r in j if r["ok"] != "1"),
            crypto_median=round(st.median(cr), 4) if cr else "",
            queue_median=round(st.median(q), 4) if q else "",
            dt_n=len(dt), dt_median=round(st.median(dt), 4) if dt else "",
            dt_p95=round(pct(dt, .95), 4) if dt else "", dt_p99=round(pct(dt, .99), 4) if dt else "",
            dt_max=round(max(dt), 4) if dt else ""))
    with open(os.path.join(RES, "e1_summary.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    # DAPV - sync difference in median handshake latency, per config and RTT
    diffs = []
    for key in sorted(hs):
        rtt, alg, chain, group, wm = key
        if wm == "none":
            continue
        base = (rtt, alg, chain, group, "none")
        if base not in hs:
            continue
        a = [float(r["hs_ms"]) for r in hs[key]]
        b = [float(r["hs_ms"]) for r in hs[base]]
        d, lo, hi = boot_median_diff(a, b, 1000)
        diffs.append(dict(rtt_ms=rtt, alg=alg, chain=chain, group=group, worker=wm,
                          sync_median=round(st.median(b), 4), dapv_median=round(st.median(a), 4),
                          diff_ms=round(d, 4), diff_lo=round(lo, 4), diff_hi=round(hi, 4),
                          diff_pct=round(100 * d / st.median(b), 2)))
    with open(os.path.join(RES, "e1_dapv_minus_sync.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(diffs[0]))
        w.writeheader()
        w.writerows(diffs)

    # Figure A: latency vs RTT, ML-DSA-44 3-cert chain, X25519MLKEM768
    fig, ax = plt.subplots(figsize=(4.6, 3.0))
    series = [("p256", "none", "classical", "P-256 (classical)"),
              ("p256_mldsa44", "none", "none", "hybrid, synchronous"),
              ("p256_mldsa44", "pool:2", "pool2", "hybrid, DAPV pool")]
    for alg, wm, col, lab in series:
        pts = sorted((k[0], st.median([float(r["hs_ms"]) for r in v])) for k, v in hs.items()
                     if k[1] == alg and k[2] == "chain3" and k[3] == "X25519MLKEM768" and k[4] == wm.replace(":", ""))
        if not pts:
            continue
        ax.plot([p[0] for p in pts], [p[1] for p in pts], "-o", color=C[col], lw=2, ms=4, label=lab)
    ax.set_xlabel("RTT (ms)")
    ax.set_ylabel("median handshake latency (ms)")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "e1_latency_vs_rtt.pdf"))
    fig.savefig(os.path.join(FIG, "e1_latency_vs_rtt.png"), dpi=200)
    plt.close(fig)

    # Figure B: DAPV - sync at RTT 0, per algorithm (pool), with bootstrap CI
    sel = [d for d in diffs if d["rtt_ms"] == 0 and d["worker"] == "pool2" and d["chain"] == "chain3"
           and d["group"] == "X25519MLKEM768"]
    order = ["p256_falcon512", "p256_mldsa44", "p384_mldsa65", "p256_sphincssha2128fsimple"]
    sel = sorted(sel, key=lambda d: order.index(d["alg"]) if d["alg"] in order else 9)
    if sel:
        fig, ax = plt.subplots(figsize=(4.6, 2.6))
        y = range(len(sel))
        ax.barh(list(y), [d["diff_ms"] for d in sel], color=C["pool2"], height=0.5)
        ax.errorbar([d["diff_ms"] for d in sel], list(y),
                    xerr=[[d["diff_ms"] - d["diff_lo"] for d in sel], [d["diff_hi"] - d["diff_ms"] for d in sel]],
                    fmt="none", ecolor="#0b0b0b", lw=1, capsize=3)
        ax.set_yticks(list(y))
        ax.set_yticklabels([ALGNAME[d["alg"]] for d in sel])
        ax.axvline(0, color="#52514e", lw=1)
        ax.set_xlabel("DAPV − synchronous, median latency (ms)")
        fig.tight_layout()
        fig.savefig(os.path.join(FIG, "e1_dapv_gain_by_alg.pdf"))
        fig.savefig(os.path.join(FIG, "e1_dapv_gain_by_alg.png"), dpi=200)
        plt.close(fig)

    # Figure C: Delta t CDF, thread vs pool (ML-DSA-44, RTT 0)
    fig, ax = plt.subplots(figsize=(4.6, 2.8))
    for wm, col in (("thread", C["thread"]), ("pool2", C["pool2"])):
        k = (0, "p256_mldsa44", "chain3", "X25519MLKEM768", wm)
        if k not in jobs:
            continue
        dt = sorted(float(r["dt_us"]) / 1000 for r in jobs[k])
        ax.plot(dt, [(i + 1) / len(dt) for i in range(len(dt))], color=col, lw=2,
                label=f"{LABEL[wm]} (n={len(dt)})")
    ax.set_xscale("log")
    ax.set_xlabel("Δt per PQ verification job (ms, log scale)")
    ax.set_ylabel("CDF")
    ax.legend(frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "e1_dt_cdf.pdf"))
    fig.savefig(os.path.join(FIG, "e1_dt_cdf.png"), dpi=200)
    plt.close(fig)


# ---------------------------------------------------------------- E2
def e2():
    f = os.path.join(RES, "e2", "summary.csv")
    if not os.path.exists(f):
        return
    rows = list(csv.DictReader(open(f)))
    g = defaultdict(list)
    for r in rows:
        g[(r["placement"], int(r["rtt_ms"]), int(r["conns"]), r["alg"], r["worker"])].append(r)
    out = []
    for k, v in sorted(g.items()):
        rate = [float(r["rate"]) for r in v]
        m = st.mean(rate)
        sd = st.stdev(rate) if len(rate) > 1 else 0
        out.append(dict(placement=k[0], rtt_ms=k[1], conns=k[2], alg=k[3], worker=k[4], reps=len(v),
                        rate_mean=round(m, 1), rate_sd=round(sd, 1),
                        hs_ms_mean=round(st.mean(float(r["mean_hs_ms"]) for r in v), 3),
                        client_cpu=round(st.mean(float(r["client_cpu_cores"]) for r in v), 3),
                        server_cpu=round(st.mean(float(r["server_cpu_cores"]) for r in v), 3),
                        errors=sum(int(r["errors"]) for r in v),
                        pq_failures=sum(int(r["pq_failures"]) for r in v)))
    with open(os.path.join(RES, "e2_summary_agg.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)

    # Figure D: rate by placement, RTT 0, 500 conns
    for rtt in sorted({o["rtt_ms"] for o in out}):
        conns = max(o["conns"] for o in out)
        fig, axes = plt.subplots(1, 2, figsize=(6.4, 2.6), sharey=True)
        for ax, pl in zip(axes, ("separate", "colocated")):
            sel = [o for o in out if o["placement"] == pl and o["rtt_ms"] == rtt and o["conns"] == conns]
            labs, vals, errs, cols = [], [], [], []
            for alg, wm, col in (("p256", "none", C["classical"]), ("p256_mldsa44", "none", C["none"]),
                                 ("p256_mldsa44", "thread", C["thread"]), ("p256_mldsa44", "pool:2", C["pool2"])):
                o = next((o for o in sel if o["alg"] == alg and o["worker"] == wm), None)
                if not o:
                    continue
                labs.append("P-256" if alg == "p256" else {"none": "sync", "thread": "DAPV\nthread", "pool:2": "DAPV\npool"}[wm])
                vals.append(o["rate_mean"]); errs.append(o["rate_sd"]); cols.append(col)
            ax.bar(range(len(vals)), vals, yerr=errs, color=cols, width=0.6, capsize=3,
                   error_kw={"elinewidth": 1})
            for i, v in enumerate(vals):
                ax.text(i, v, f"{v:.0f}", ha="center", va="bottom", fontsize=8, color="#0b0b0b")
            ax.set_xticks(range(len(labs)))
            ax.set_xticklabels(labs, fontsize=8)
            ax.set_title({"separate": "server and client on disjoint cores",
                          "colocated": "server and client share cores"}[pl], fontsize=9)
        axes[0].set_ylabel("completed handshakes / s")
        fig.tight_layout()
        fig.savefig(os.path.join(FIG, f"e2_rate_rtt{rtt}.pdf"))
        fig.savefig(os.path.join(FIG, f"e2_rate_rtt{rtt}.png"), dpi=200)
        plt.close(fig)


if __name__ == "__main__":
    e1()
    e2()
