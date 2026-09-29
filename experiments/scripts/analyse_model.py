#!/usr/bin/env python3
"""Analysis of E3-E6 and validation of the latency model.

Model (Section 4.7 of the paper):
    L(RTT) = L0 + (1 + dk) * RTT
    dk = min n >= 0 such that IW * MSS * (2^(n+1) - 1) >= F      (slow start)
where F is the server's first flight in bytes (measured), IW the initial
congestion window in segments and MSS = 1448 bytes.  L0 is taken from the
RTT = 0 measurement of the same configuration, so the model has no fitted
parameters at non-zero RTT.

DAPV benefit under verification-cost scaling (E6):
    dL(k) = L_sync(k) - L_dapv(k) ~= a * k - b
a = critical-path verification cost per unit of k, b = dispatch overhead;
the break-even point is k* = b / a.
"""
import csv, glob, json, os, random, statistics as st
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "results")
FIG = os.path.join(ROOT, "figures")
MSS = 1448
random.seed(2)
C = {"none": "#2a78d6", "pool2": "#eb6834", "classical": "#6b6a66", "a4": "#1baf7a"}
ALGNAME = {"p256": "P-256", "p256_mldsa44": "P-256+ML-DSA-44",
           "p256_falcon512": "P-256+FN-DSA-512", "p384_mldsa65": "P-384+ML-DSA-65",
           "p256_sphincssha2128fsimple": "P-256+SLH-DSA-128f"}
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": "#e6e5e1", "grid.linewidth": 0.6,
                     "axes.edgecolor": "#8a8984", "axes.axisbelow": True})


def pct(xs, p):
    xs = sorted(xs)
    k = (len(xs) - 1) * p
    lo = int(k); hi = min(lo + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def load(exp):
    """-> {(cond, alg, worker): [hs rows]}, {(cond, alg, worker): [job rows]}"""
    hs, jobs = defaultdict(list), defaultdict(list)
    for f in glob.glob(os.path.join(RES, exp, "*", "*_hs.csv")):
        cond = os.path.basename(os.path.dirname(f))
        alg, _chain, _grp, wm, _r = os.path.basename(f)[:-7].split("__")
        jf = f.replace("_hs.csv", "_jobs.csv")
        if not os.path.exists(jf):
            continue
        hs[(cond, alg, wm)] += list(csv.DictReader(open(f)))
        jobs[(cond, alg, wm)] += list(csv.DictReader(open(jf)))
    return hs, jobs


def med(rows, col="hs_ms"):
    return st.median(float(r[col]) for r in rows)


def dk_pred(F, iw):
    n = 0
    while iw * MSS * (2 ** (n + 1) - 1) < F:
        n += 1
    return n


def main():
    flights = json.load(open(os.path.join(RES, "flight_bytes.json")))
    out = {}

    # ---------- model validation on E1 (IW 10) and E3 (IW 10/20/40)
    e1 = {}
    for r in csv.DictReader(open(os.path.join(RES, "e1_summary.csv"))):
        if r["chain"] == "chain3" and r["group"] == "X25519MLKEM768" and r["worker"] == "none":
            e1[(r["alg"], int(r["rtt_ms"]))] = float(r["hs_median"])
    rows = []
    for (alg, rtt), m in sorted(e1.items()):
        if rtt == 0 or alg not in flights:
            continue
        dk = dk_pred(flights[alg], 10)
        pred = e1[(alg, 0)] + (1 + dk) * rtt
        rows.append(dict(src="E1", alg=alg, iw=10, rtt=rtt, flight=flights[alg], dk_pred=dk,
                         measured=round(m, 2), predicted=round(pred, 2),
                         err_pct=round(100 * (pred - m) / m, 2)))
    hs3 = {}
    for tag in ("e3", "e3_cubic"):
        h, _ = load(tag)
        hs3.update({(tag,) + k: v for k, v in h.items()})
    for (tag, cond, alg, wm), v in sorted(hs3.items()):
        iw = int(cond.split("_")[0][2:]); rtt = int(cond.split("_")[1][3:])
        dk = dk_pred(flights[alg], iw)
        pred = e1[(alg, 0)] + (1 + dk) * rtt
        m = med(v)
        rows.append(dict(src="E3-" + ("cubic" if tag.endswith("cubic") else "bbr"), alg=alg, iw=iw, rtt=rtt, flight=flights[alg], dk_pred=dk,
                         measured=round(m, 2), predicted=round(pred, 2),
                         err_pct=round(100 * (pred - m) / m, 2),
                         p95=round(pct([float(r["hs_ms"]) for r in v], .95), 2), n=len(v)))
    with open(os.path.join(RES, "model_validation.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=sorted({k for r in rows for k in r}))
        w.writeheader(); w.writerows(rows)
    for name, sel in (("all", lambda r: True), ("bbr", lambda r: r["src"] != "E3-cubic"),
                      ("cubic", lambda r: r["src"] == "E3-cubic"),
                      ("iw10", lambda r: r["iw"] == 10)):
        rr = [r for r in rows if sel(r)]
        if not rr:
            continue
        errs = [abs(r["err_pct"]) for r in rr]
        out[f"model_{name}"] = dict(points=len(rr), mape_pct=round(st.mean(errs), 2),
                                    max_abs_err_pct=round(max(errs), 2),
                                    dk_correct=sum(1 for r in rr if abs(r["measured"] - r["predicted"]) < 0.5 * r["rtt"]))

    # Figure: E3 latency vs initcwnd at RTT 150
    fig, ax = plt.subplots(figsize=(4.6, 2.8))
    for alg, col in (("p256_mldsa44", C["none"]), ("p384_mldsa65", C["pool2"]),
                     ("p256_sphincssha2128fsimple", C["a4"]), ("p256", C["classical"])):
        pts = sorted((r["iw"], r["measured"], r["predicted"]) for r in rows
                     if r["src"] == "E3-cubic" and r["alg"] == alg and r["rtt"] == 150)
        if not pts:
            continue
        ax.plot([p[0] for p in pts], [p[1] for p in pts], "-o", color=col, lw=2, ms=4, label=ALGNAME[alg])
        ax.plot([p[0] for p in pts], [p[2] for p in pts], "x", color=col, ms=7, mew=1.5)
    ax.set_xscale("log", base=2); ax.set_xticks([10, 20, 40]); ax.set_xticklabels(["10", "20", "40"])
    ax.set_xlabel("server initial congestion window (segments)")
    ax.set_ylabel("median handshake latency (ms)")
    ax.set_title("RTT 150 ms, CUBIC; o measured, x model prediction", fontsize=8)
    ax.legend(frameon=False, fontsize=7)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "e3_initcwnd.pdf")); fig.savefig(os.path.join(FIG, "e3_initcwnd.png"), dpi=200); plt.close(fig)

    # ---------- E4 loss
    hs4, _ = load("e4")
    lrows = []
    for (cond, alg, wm), v in sorted(hs4.items()):
        loss = float(cond.split("_")[0][4:])
        x = [float(r["hs_ms"]) for r in v]
        t = [float(r["tcp_ms"]) + float(r["hs_ms"]) for r in v]
        lrows.append(dict(alg=alg, loss_pct=loss, n=len(x), hs_median=round(st.median(x), 2),
                          hs_p90=round(pct(x, .9), 2), hs_p99=round(pct(x, .99), 2),
                          hs_mean=round(st.mean(x), 2), frac_over_2rtt=round(sum(1 for y in x if y > 100) / len(x), 4),
                          conn_hs_median=round(st.median(t), 2), conn_hs_p99=round(pct(t, .99), 2)))
    # tail model: a handshake is delayed if any of its data segments is lost;
    # segments = server first flight + ClientHello (one segment).
    segs = json.load(open(os.path.join(RES, "flight_segments.json")))
    base = {r["alg"]: r["hs_median"] for r in lrows if r["loss_pct"] == 0}
    for r in lrows:
        x = [float(q["hs_ms"]) for q in hs4[(f"loss{int(r['loss_pct'])}_rtt50", r["alg"], "none")]]
        r["frac_delayed"] = round(sum(1 for y in x if y > base[r["alg"]] + 25) / len(x), 4)
        p = r["loss_pct"] / 100
        r["frac_delayed_model"] = round(1 - (1 - p) ** (segs[r["alg"]] + 1), 4)
    with open(os.path.join(RES, "e4_loss.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(lrows[0])); w.writeheader(); w.writerows(lrows)
    fig, ax = plt.subplots(figsize=(4.6, 2.8))
    for alg, col in (("p256", C["classical"]), ("p256_falcon512", C["a4"]),
                     ("p256_mldsa44", C["none"]), ("p384_mldsa65", C["pool2"])):
        pts = sorted((r["loss_pct"], r["hs_mean"]) for r in lrows if r["alg"] == alg)
        ax.plot([p[0] for p in pts], [p[1] for p in pts], "-o", color=col, lw=2, ms=4, label=ALGNAME[alg])
    ax.set_xlabel("frame loss per direction (%)"); ax.set_ylabel("mean handshake latency (ms)")
    ax.set_xticks([0, 1, 3]); ax.set_title("RTT 50 ms", fontsize=8)
    ax.legend(frameon=False, fontsize=7)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "e4_loss.pdf")); fig.savefig(os.path.join(FIG, "e4_loss.png"), dpi=200); plt.close(fig)

    # ---------- E5 portable liboqs client
    hs5, jobs5 = load("e5")
    r5 = []
    for (cond, alg, wm), v in sorted(hs5.items()):
        if wm != "none":
            continue
        rtt = int(cond.split("rtt")[1])
        b = [float(r["hs_ms"]) for r in v]
        a = [float(r["hs_ms"]) for r in hs5[(cond, alg, "pool2")]]
        d = []
        for _ in range(1000):
            d.append(st.median(random.choice(a) for _ in a) - st.median(random.choice(b) for _ in b))
        j = jobs5[(cond, alg, "pool2")]
        dt = [float(x["dt_us"]) / 1000 for x in j]
        r5.append(dict(alg=alg, rtt=rtt, sync=round(st.median(b), 3), dapv=round(st.median(a), 3),
                       diff=round(st.median(a) - st.median(b), 3), lo=round(pct(d, .025), 3), hi=round(pct(d, .975), 3),
                       pct=round(100 * (st.median(a) - st.median(b)) / st.median(b), 2),
                       verify_ms=round(st.median(float(x["crypto_us"]) / 1000 for x in j), 4),
                       dt_median=round(st.median(dt), 3), dt_p99=round(pct(dt, .99), 3)))
    with open(os.path.join(RES, "e5_generic.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(r5[0])); w.writeheader(); w.writerows(r5)

    # ---------- E6 verification-cost scaling
    hs6, jobs6 = load("e6")
    r6 = []
    for (cond, alg, wm), v in sorted(hs6.items()):
        if wm != "none":
            continue
        k = int(cond.split("_")[0][1:]); rtt = int(cond.split("rtt")[1])
        b = [float(r["hs_ms"]) for r in v]
        a = [float(r["hs_ms"]) for r in hs6[(cond, alg, "pool2")]]
        fa = [float(r["full_ms"]) for r in hs6[(cond, alg, "pool2")]]
        d = []
        for _ in range(1000):
            d.append(st.median(random.choice(a) for _ in a) - st.median(random.choice(b) for _ in b))
        j = jobs6[(cond, alg, "pool2")]
        dt = [float(x["dt_us"]) / 1000 for x in j]
        r6.append(dict(k=k, rtt=rtt, sync=round(st.median(b), 3), dapv=round(st.median(a), 3),
                       gain=round(st.median(b) - st.median(a), 3), gain_lo=round(-pct(d, .975), 3),
                       gain_hi=round(-pct(d, .025), 3),
                       gain_pct=round(100 * (st.median(b) - st.median(a)) / st.median(b), 2),
                       full_auth=round(st.median(fa), 3),
                       verify_ms=round(st.median(float(x["crypto_us"]) / 1000 for x in j), 4),
                       dt_median=round(st.median(dt), 3), dt_p99=round(pct(dt, .99), 3)))
    r6.sort(key=lambda r: (r["rtt"], r["k"]))
    with open(os.path.join(RES, "e6_scaling.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(r6[0])); w.writeheader(); w.writerows(r6)
    # linear fit of gain vs per-handshake verification work (3 jobs * verify_ms)
    for rtt in (0, 50):
        pts = [(3 * r["verify_ms"], r["gain"]) for r in r6 if r["rtt"] == rtt]
        if len(pts) < 3:
            continue
        xs, ys = zip(*pts); mx, my = st.mean(xs), st.mean(ys)
        a = sum((x - mx) * (y - my) for x, y in pts) / sum((x - mx) ** 2 for x in xs)
        b = my - a * mx
        ss_res = sum((y - (a * x + b)) ** 2 for x, y in pts); ss_tot = sum((y - my) ** 2 for y in ys)
        out[f"e6_fit_rtt{rtt}"] = dict(slope=round(a, 3), intercept_ms=round(b, 3),
                                       r2=round(1 - ss_res / ss_tot, 4),
                                       breakeven_work_ms=round(-b / a, 3) if a else None)
    fig, ax = plt.subplots(figsize=(4.6, 2.8))
    lim = max(3 * r["verify_ms"] for r in r6) * 1.05 if r6 else 1
    ax.plot([0, lim], [0, lim], ":", color="#8a8984", lw=1, label="gain = work")
    for rtt, col in ((0, C["pool2"]), (50, C["none"])):
        pts = [(3 * r["verify_ms"], r["gain"], r["gain_lo"], r["gain_hi"]) for r in r6 if r["rtt"] == rtt]
        if not pts:
            continue
        ax.errorbar([p[0] for p in pts], [p[1] for p in pts],
                    yerr=[[p[1] - p[2] for p in pts], [p[3] - p[1] for p in pts]],
                    fmt="o", color=col, ms=4, capsize=2, label=f"measured, RTT {rtt} ms")
        f = out.get(f"e6_fit_rtt{rtt}")
        if f:
            ax.plot([0, lim], [f["intercept_ms"], f["slope"] * lim + f["intercept_ms"]], "-", color=col, lw=1.5,
                    label=f"fit: {f['slope']:.2f} W {f['intercept_ms']:+.2f} ms")
    ax.axhline(0, color="#52514e", lw=0.8)
    ax.set_xlim(0, lim)
    ax.set_xlabel("PQ verification work per handshake W (ms)")
    ax.set_ylabel("DAPV latency gain (ms)")
    ax.legend(frameon=False, fontsize=7)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "e6_scaling.pdf")); fig.savefig(os.path.join(FIG, "e6_scaling.png"), dpi=200); plt.close(fig)

    json.dump(out, open(os.path.join(RES, "model_summary.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
