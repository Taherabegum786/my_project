"""All figures (PDF vector + PNG 300 dpi) from the result CSVs.

python -m plots.make_figures --in ../results --out ../results/figures
Every figure is produced only from CSVs written by the experiment scripts.  Model curves are lines labelled
'model'; measured / simulated values are markers.  Figures that depend solely on Experimenter B's E8/E3b CSVs
(wire_bytes.csv, proto_capacity.csv, proto_latency.csv, proto_validate.csv) are skipped if those files are missing.
"""
import argparse
import math
import os
import sys
import traceback

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from plots.style import COL, DCOL, INK2, LINES, MARKERS, SERIES, save, setup  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

IN = OUT = None
LABEL = {"B1": "B1 HMAC", "B2": "B2 Ed25519", "B3": "B3 ECDSA", "B4": "B4 RSA-2048", "B5": "B5 ML-DSA-44",
         "B6": "B6 ML-DSA-65", "B7": "B7 SLH-128s", "B8": "B8 SLH-128f", "B9": "B9 Ed25519+ML-DSA-44",
         "B5c": "B5c ML-DSA-44 (2 cookies)", "B6c": "B6c ML-DSA-65 (2 cookies)", "B10k3": "B10 multi-MAC k=3",
         "B11": "B11 deleg. Ed25519", "B12": "B12 KEM-wrapped HMAC", "B13": "B13 MTL"}


def rd(name):
    p = os.path.join(IN, name)
    if not os.path.exists(p):
        raise FileNotFoundError(name)
    return pd.read_csv(p)


def tci(x):
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    n = len(x)
    if n < 2:
        return (x.mean() if n else np.nan), 0.0
    from scipy import stats
    return x.mean(), stats.t.ppf(0.975, n - 1) * x.std(ddof=1) / np.sqrt(n)


def limits(ax, horiz=False):
    for v, lab in ((2048, "2 KB URL (practice)"), (4096, "4 KB cookie"), (8000, "8000 B URL (RFC 9110)")):
        (ax.axvline if horiz else ax.axhline)(v, color=INK2, lw=0.8, ls=":")
        if horiz:
            ax.text(v, 1.0, " " + lab, rotation=90, va="top", ha="right", fontsize=7, color=INK2,
                    transform=ax.get_xaxis_transform())


# ------------------------------------------------------------------ Fig 2
def fig2():
    d = rd("token_sizes.csv")
    d = d[(d.url_path_len == 60) & (d.with_ip == 0)]
    rows = []
    for s in ["B1", "B10k3", "B12", "B11", "B2", "B3", "B4", "B5", "B9", "B6", "B7", "B8"]:
        r = d[d.scheme == s]
        if len(r):
            rows.append((LABEL.get(s, s), r.signed_url_bytes.iloc[0], r.cookie_bytes.iloc[0]))
    for s, lg in (("B5c", None), ("B6c", None)):
        r = d[d.scheme == s]
        if len(r):
            rows.append((LABEL[s] + " (max cookie)", r.signed_url_bytes.iloc[0], r.cookie_bytes.iloc[0]))
    r = d[(d.scheme == "B13") & (d.log2N == d[d.scheme == "B13"].log2N.max())]
    if len(r):
        rows.append(("B13 MTL, series 2^%d" % r.log2N.iloc[0], r.signed_url_bytes.iloc[0], r.cookie_bytes.iloc[0]))
    for o, lg in (("O1", 10), ("O1", 16), ("O1", 20), ("O2", 16), ("O3", 16), ("O4", 16)):
        r = d[(d.scheme == o) & (d.log2N == lg)]
        if len(r):
            nm = {"O1": "EMBER ML-DSA-44 n16", "O2": "EMBER ML-DSA-44 n32", "O3": "EMBER SLH-128s n16", "O4": "EMBER hybrid n16"}[o]
            rows.append(("%s, N=2^%d" % (nm, lg), r.signed_url_bytes.iloc[0], r.cookie_bytes.iloc[0]))
    fig, ax = plt.subplots(figsize=(COL, 3.9))
    y = np.arange(len(rows))
    ax.barh(y - 0.2, [r[1] for r in rows], height=0.38, color=SERIES[0], label="signed URL (bytes)")
    ax.barh(y + 0.2, [r[2] for r in rows], height=0.38, color=SERIES[1], label="Set-Cookie value (bytes)")
    ax.set_yticks(y, [r[0] for r in rows], fontsize=7)
    ax.invert_yaxis()
    ax.set_xscale("log")
    ax.set_xlabel("bytes (log)")
    limits(ax, horiz=True)
    ax.legend(loc="lower right", fontsize=7)
    ax.grid(axis="y", visible=False)
    save(fig, OUT, "fig2_token_sizes")


# ------------------------------------------------------------------ Fig 3
def fig3():
    d = rd("token_sizes.csv")
    d = d[(d.url_path_len == 60) & (d.with_ip == 0)]
    fig, (a, b) = plt.subplots(2, 1, figsize=(COL, 4.3))
    for k, (o, n) in enumerate((("O1", 16), ("O2", 32))):
        r = d[d.scheme == o].sort_values("log2N")
        a.plot(r.log2N, r.token_bytes, MARKERS[k], color=SERIES[k], label="measured, n=%d" % n)
        L = np.arange(0, 25)
        cb = r.claims_bytes.iloc[0]
        a.plot(L, [cb + 3 + math.ceil(4 * (30 + n * l) / 3) for l in L], LINES[k], color=SERIES[k], lw=1, label="model, n=%d" % n)
    b5 = d[d.scheme == "B5"].token_bytes.iloc[0]
    a.axhline(b5, color=INK2, ls=":", lw=0.8)
    a.text(0.3, b5 * 0.93, "B5 per-token ML-DSA-44 (%d B)" % b5, fontsize=7, color=INK2, va="top")
    a.set_ylabel("token bytes (b64url)")
    a.set_xlabel("log$_2$ N (tokens per epoch)")
    a.legend(fontsize=7, ncol=2, loc="center right")
    a.set_ylim(0, b5 * 1.08)
    ia = rd("native_issuer_agg.csv")
    for k, alg in enumerate(["ML-DSA-44", "SLH-DSA-SHA2-128s"]):
        r = ia[(ia.root_alg == alg) & (ia.n == 16)].sort_values("N")
        b.errorbar(r.N, r.tokens_per_s, yerr=[r.tokens_per_s - r.tps_ci95_lo, r.tps_ci95_hi - r.tokens_per_s],
                   fmt=MARKERS[k] + LINES[k], color=SERIES[k], lw=1, ms=3.5, capsize=1.5,
                   label="EMBER, %s root (native)" % alg.replace("SLH-DSA-SHA2-", "SLH-"))
    ns = rd("native_sig_agg.csv")
    for k, (s, lab) in enumerate((("ML-DSA-44", "per-token ML-DSA-44 sign"), ("SLH-DSA-SHA2-128s", "per-token SLH-128s sign"))):
        v = 1e6 / ns[(ns.scheme == s) & (ns.op == "sign")].median_us.iloc[0]
        b.axhline(v, color=SERIES[k], ls=":", lw=0.9, label=lab + " (native, %.3g/s)" % v)
    b.set_xscale("log", base=2)
    b.set_yscale("log")
    b.set_xlabel("N (tokens per epoch)")
    b.set_ylabel("issuer tokens/s per core")
    b.set_ylim(1, 2e10)
    b.legend(fontsize=7, loc="upper left", ncol=1, handlelength=1.6, borderaxespad=0.2)
    fig.tight_layout()
    save(fig, OUT, "fig3_size_vs_N")


# ------------------------------------------------------------------ Fig 4
def fig4():
    tv = rd("token_verify.csv")
    fig, (a, b) = plt.subplots(1, 2, figsize=(DCOL, 3.1))
    sel = [("B1", "none"), ("B10k3", "none"), ("B12", "none"), ("B2", "none"), ("B3", "none"), ("B4", "none"),
           ("B11", "none"), ("B5", "none"), ("B6", "none"), ("B9", "none"), ("B7", "none"), ("B8", "none"),
           ("B5v", "hit"), ("B5v", "miss")]
    rows = []
    for s, c in sel:
        r = tv[(tv.scheme == s) & (tv.cache == c)]
        if len(r):
            rows.append(("%s%s" % (LABEL.get(s, s) if s != "B5v" else "B5v ML-DSA-44+vcache", "" if c == "none" else " (%s)" % c),
                         r.median_us.iloc[0], r.p99_us.iloc[0], 0))
    for o, lg, c in (("O1", 8, "warm"), ("O1", 16, "warm"), ("O1", 20, "warm"), ("O1", 16, "cold"), ("O4", 16, "warm"),
                     ("O1v", 16, "hit"), ("B13", 16, "warm")):
        r = tv[(tv.scheme == o) & (tv.log2N == lg) & (tv.cache == c)]
        if len(r):
            nm = {"O1": "EMBER O1", "O4": "EMBER O4 hybrid", "O1v": "EMBER O1+vcache", "B13": "B13 MTL"}[o]
            rows.append(("%s N=2^%d (%s)" % (nm, lg, c), r.median_us.iloc[0], r.p99_us.iloc[0], 1))
    _bars(a, rows, "Python backends: full verify()")
    ns = rd("native_sig_agg.csv")
    pv = rd("native_pathverify_agg.csv")
    nrows = []
    g = pv[(pv.impl == "evp")]
    hm = g[g.op == "hmac_sha256_200B"]
    nrows.append(("HMAC-SHA256 (200 B)", hm.ns_median.iloc[0] / 1e3, hm.ns_p99.iloc[0] / 1e3, 0))
    for s, lab in (("ED25519", "Ed25519 verify"), ("ECDSA-P256", "ECDSA-P256 verify"), ("RSA-2048", "RSA-2048 verify"),
                   ("ML-DSA-44", "ML-DSA-44 verify"), ("ML-DSA-65", "ML-DSA-65 verify"),
                   ("SLH-DSA-SHA2-128s", "SLH-128s verify"), ("SLH-DSA-SHA2-128f", "SLH-128f verify")):
        r = ns[(ns.scheme == s) & (ns.op == "verify")]
        nrows.append((lab, r.median_us.iloc[0], r.p99_us.iloc[0], 0))
    for dd in (8, 12, 16, 20):
        r = g[(g.op == "pathverify") & (g.d == dd) & (g.n == 16)]
        nrows.append(("EMBER path verify d=%d" % dd, r.ns_median.iloc[0] / 1e3, r.ns_p99.iloc[0] / 1e3, 1))
    r = g[g.op == "sha256_3500B"]
    if len(r):
        nrows.append(("vcache key SHA-256 (3.5 KB token)", r.ns_median.iloc[0] / 1e3, r.ns_p99.iloc[0] / 1e3, 0))
    _bars(b, nrows, "Native OpenSSL 3.5.4 (C, EVP)")
    fig.tight_layout()
    fig.legend(handles=fig._ember_handles, loc="lower center", ncol=2, fontsize=7, bbox_to_anchor=(0.5, -0.04))
    save(fig, OUT, "fig4_verify_cost")


def _bars(ax, rows, title):
    y = np.arange(len(rows))
    med = np.array([r[1] for r in rows])
    p99 = np.array([r[2] for r in rows])
    col = [SERIES[1] if r[3] else SERIES[0] for r in rows]
    ax.barh(y, med, color=col, height=0.7)
    ax.errorbar(p99, y, fmt="|", color="#0b0b0b", ms=5, mew=1, label="p99")
    ax.set_yticks(y, [r[0] for r in rows], fontsize=7)
    ax.invert_yaxis()
    ax.set_xscale("log")
    ax.set_xlabel("microseconds per verification (log); bar = median, | = p99")
    ax.set_title(title, fontsize=7)
    ax.grid(axis="y", visible=False)
    from matplotlib.patches import Patch
    ax.figure._ember_handles = [Patch(color=SERIES[0], label="baseline / primitive"),
                                Patch(color=SERIES[1], label="EMBER / Merkle path")]


# ------------------------------------------------------------------ Fig 5
def fig5():
    d = rd("sim_delta_sweep.csv")
    d = d[(d["mode"] == "pull") & (d.pool == 0) & (d.backend == "native") & d.policy.str.startswith("fixed")]
    d["delta_s"] = d.delta_s.astype(float)
    fig, axs = plt.subplots(3, 1, figsize=(COL, 4.6), sharex=True)
    for k, lam in enumerate(sorted(d.lambda_bar.unique())):
        g = d[d.lambda_bar == lam]
        st = g.groupby("delta_s").agg(list)
        x = st.index.values
        for ax, col, mcol in ((axs[0], "issue_wait_mean_s", None), (axs[1], "miss_per_token", "model_miss_per_token"),
                              (axs[2], "D_mean_s", "model_D_s")):
            m = np.array([tci(v)[0] for v in st[col]])
            h = np.array([tci(v)[1] for v in st[col]])
            ax.errorbar(x, m, yerr=h, fmt=MARKERS[k], color=SERIES[k], ms=3.5, capsize=1.5,
                        label="simulated, $\\bar\\lambda$=%g/s" % lam)
            if mcol:
                mv = np.array([np.mean(v) for v in st[mcol]])
                ax.plot(x, mv, LINES[k], color=SERIES[k], lw=1, label="model, $\\bar\\lambda$=%g/s" % lam)
    xx = np.logspace(-2, np.log10(60), 50)
    axs[0].plot(xx, xx / 2, ls="-", color=INK2, lw=0.8, label="model $\\Delta$/2")
    axs[0].set_ylabel("mean issuance\nwait (s)")
    axs[1].set_ylabel("root misses\nper token")
    axs[2].set_ylabel("D($\\Delta$) (s)")
    for ax in axs:
        ax.set_xscale("log")
    axs[0].set_yscale("log")
    axs[2].set_yscale("log")
    axs[2].set_xlabel("epoch length $\\Delta$ (s), pull mode, per-tenant trees")
    from matplotlib.lines import Line2D
    axs[1].legend(handles=[Line2D([], [], color=INK2, lw=1, label="model (line)"),
                           Line2D([], [], color=INK2, marker="o", ls="none", ms=3.5, label="simulated (marker)")],
                  fontsize=7, loc="lower left")
    axs[0].legend(fontsize=7)
    fig.tight_layout()
    save(fig, OUT, "fig5_delta_tradeoff")


# ------------------------------------------------------------------ Fig 6
def fig6():
    d = rd("sim_controller_ts.csv")
    lam = 2000 if (d.lambda_bar == 2000).any() else d.lambda_bar.max()
    d = d[d.lambda_bar == lam]
    fig, axs = plt.subplots(3, 1, figsize=(DCOL, 4.2), sharex=True)
    a = d[d.policy == "adaptive"].sort_values("t_bin_s")
    axs[0].plot(a.t_bin_s / 3600, a.lambda_hat, color=SERIES[0])
    axs[0].set_ylabel("token rate (1/s)")
    pols = [("adaptive", 0), ("wc", 4), ("fixed:0.1", 1), ("fixed:1", 2), ("fixed:10", 3)]
    for p, k in pols:
        g = d[d.policy == p].sort_values("t_bin_s")
        if not len(g):
            continue
        axs[1].plot(g.t_bin_s / 3600, g.delta_chosen_s, ls=LINES[k], color=SERIES[k], lw=1.2, label=p)
        axs[2].plot(g.t_bin_s / 3600, g.D_mean_s, ls=LINES[k], color=SERIES[k], lw=1.2, label=p)
    axs[1].set_yscale("log")
    axs[1].set_ylabel("token-weighted\nmean $\\Delta$ (s)")
    axs[2].set_yscale("log")
    axs[2].set_ylabel("mean D per token (s)")
    axs[2].set_xlabel("time of day (h), simulated, $\\bar\\lambda$=%g tokens/s, pull mode" % lam)
    axs[2].legend(ncol=5, fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.45))
    fig.tight_layout()
    save(fig, OUT, "fig6_controller_24h")


# ------------------------------------------------------------------ Fig 7
def fig7():
    d = rd("sim_dissem.csv")
    dd = d[(d.delta_s.astype(float) == 1.0) | (d.scheme == "B11")]
    fig, (a, b) = plt.subplots(1, 2, figsize=(DCOL, 2.4))
    modes = ["pull", "push", "pull_staple", "pull_rollup", "push_rollup"]
    for k, m in enumerate(modes):
        g = dd[(dd.scheme == "EMBER-O1") & (dd["mode"] == m)].groupby("E")
        x = np.array(sorted(g.groups))
        bw = [tci(g.get_group(e).root_bw_fleet_Bps)[0] for e in x]
        bh = [tci(g.get_group(e).root_bw_fleet_Bps)[1] for e in x]
        a.errorbar(x, bw, yerr=bh, fmt=MARKERS[k], ls=LINES[k], color=SERIES[k], ms=3.5, lw=1, label="EMBER " + m)
        mm = [tci(g.get_group(e).miss_per_mreq)[0] for e in x]
        mh = [tci(g.get_group(e).miss_per_mreq)[1] for e in x]
        b.errorbar(x, mm, yerr=mh, fmt=MARKERS[k], ls=LINES[k], color=SERIES[k], ms=3.5, lw=1, label="EMBER " + m)
    for k, s in ((5, "B11"), (6, "B12")):
        g = dd[dd.scheme == s].groupby("E")
        x = np.array(sorted(g.groups))
        a.plot(x, [g.get_group(e).root_bw_fleet_Bps.astype(float).mean() for e in x], MARKERS[k], ls=LINES[k],
               color=SERIES[k], ms=3.5, lw=1, label=LABEL[s] + (" (push)" if s == "B12" else " (certs)"))
    a.set_xscale("log"); a.set_yscale("log")
    a.set_xlabel("edges E"); a.set_ylabel("fleet root/key bytes/s (simulated)")
    b.set_xscale("log"); b.set_yscale("log")
    b.set_xlabel("edges E"); b.set_ylabel("root misses per $10^6$ requests")
    h, l = a.get_legend_handles_labels()
    fig.legend(h, l, fontsize=7, ncol=4, loc="lower center", bbox_to_anchor=(0.5, -0.12))
    a.set_title("(a) dissemination bandwidth, $\\Delta$=1 s", fontsize=7)
    b.set_title("(b) misses, $\\Delta$=1 s", fontsize=7)
    fig.tight_layout()
    save(fig, OUT, "fig7_dissemination")


# ------------------------------------------------------------------ Fig 8
def fig8():
    d = rd("sim_e2e_latency.csv")
    fig, ax = plt.subplots(figsize=(COL * 0.62, 2.6))
    series = [("EMBER-O1", "pull"), ("EMBER-O1", "pull_staple"), ("EMBER-O1", "push"), ("EMBER-O1", "push_rollup"),
              ("B1-HMAC", "none"), ("B5-ML-DSA-44", "none"), ("B5v-ML-DSA-44+vcache", "none"), ("B11-DelegEd25519", "none")]
    for k, (s, m) in enumerate(series):
        v = np.sort(d[(d.scheme == s) & (d["mode"] == m)].sample_ms.values)
        if not v.size:
            continue
        y = np.arange(1, v.size + 1) / v.size
        ax.plot(np.maximum(v, 1e-4), y, ls=LINES[k], color=SERIES[k], lw=1.2,
                label=(s.replace("EMBER-O1", "EMBER") + ("" if m == "none" else " " + m)))
    ax.set_xscale("log")
    ax.set_xlabel("added latency per request (ms)")
    ax.set_ylabel("CDF (simulated)")
    ax.set_ylim(0.9, 1.0005)
    ax.legend(fontsize=7, loc="upper left", bbox_to_anchor=(1.01, 1.0), handlelength=2.2)
    save(fig, OUT, "fig8_e2e_cdf")


# ------------------------------------------------------------------ Fig 9
def fig9():
    d = rd("sim_sens.csv")
    g = d[(d.param == "E") & (d.metric == "miss_per_token") & (d["mode"] == "pull") & d.policy.str.startswith("fixed")]
    Es = sorted(g.value.astype(float).unique())
    Ds = sorted(g.policy.str.split(":").str[1].astype(float).unique())
    M = np.full((len(Es), len(Ds)), np.nan)
    for i, e in enumerate(Es):
        for j, dl in enumerate(Ds):
            r = g[(g.value.astype(float) == e) & (g.policy == "fixed:%g" % dl)]
            if len(r):
                M[i, j] = r["mean"].iloc[0]
    from matplotlib.colors import LinearSegmentedColormap
    cm = LinearSegmentedColormap.from_list("blue", ["#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"])
    fig, ax = plt.subplots(figsize=(COL, 1.9))
    im = ax.imshow(M, cmap=cm, aspect="auto", vmin=0, vmax=max(1.0, np.nanmax(M)))
    ax.set_xticks(range(len(Ds)), ["%g" % x for x in Ds])
    ax.set_yticks(range(len(Es)), ["%d" % x for x in Es])
    ax.set_xlabel("$\\Delta$ (s)")
    ax.set_ylabel("edges E")
    ax.grid(False)
    for i in range(len(Es)):
        for j in range(len(Ds)):
            if not np.isnan(M[i, j]):
                ax.text(j, i, "%.2f" % M[i, j], ha="center", va="center", fontsize=7,
                        color="#0b0b0b" if M[i, j] < 0.5 else "#fcfcfb")
    fig.colorbar(im, ax=ax, label="misses/token (pull, simulated)")
    save(fig, OUT, "fig9_sens_heatmap")


# ------------------------------------------------------------------ E8 / E3b (Experimenter B data)
def fig_wire():
    d = rd("wire_bytes.csv")
    keep = d[d.proto.isin(["h2-hpack", "http1.1"])]
    pls = [(p, pr) for pr in ("h2-hpack", "http1.1") for p in sorted(keep[keep.proto == pr].placement.unique())]
    schemes = [s for s in keep.scheme.unique() if s != "none"]
    fig, ax = plt.subplots(figsize=(DCOL, 2.6))
    w = 0.8 / max(1, len(pls))
    x = np.arange(len(schemes))
    for k, (p, pr) in enumerate(pls):
        vals = [keep[(keep.scheme == s) & (keep.placement == p) & (keep.proto == pr)].session_bytes for s in schemes]
        v = [x_.iloc[0] if len(x_) else np.nan for x_ in vals]
        ax.bar(x + (k - len(pls) / 2 + 0.5) * w, v, width=w * 0.92, color=SERIES[k % 8], label="%s, %s" % (pr, p))
    ax.set_xticks(x, schemes, rotation=45, ha="right", fontsize=7)
    ax.set_yscale("log")
    ax.set_ylabel("upstream header bytes per session\n(1 manifest + K=150 segments, measured)")
    ax.legend(fontsize=7, ncol=3)
    ax.grid(axis="x", visible=False)
    save(fig, OUT, "fig10_wire_bytes")


PROTO_LABEL = {"b1": "B1 HMAC", "b12": "B12 KEM-wrapped HMAC", "o4": "EMBER O4 (hybrid root)",
               "o1a": "EMBER O1 + root/1000 req", "o1": "EMBER O1 (warm)", "b5v": "B5v ML-DSA-44 + vcache",
               "b5": "B5 ML-DSA-44", "b11": "B11 deleg. Ed25519", "b2": "B2 Ed25519", "b6": "B6 ML-DSA-65",
               "b3": "B3 ECDSA P-256", "b9": "B9 Ed25519+ML-DSA-44"}


def fig_proto():
    """P1 edge capacity. Primary metric: edge CPU time per request (edge CPU utilisation / req/s), which stays
    valid when the load generator rather than the edge limits throughput; req/s shown as secondary panel."""
    d = rd("proto_capacity.csv").copy()
    d["us_per_req"] = d.cpu_util_edge / d.req_per_s * 1e6
    g = d.groupby("scheme")
    s = sorted(g.groups, key=lambda k: g.get_group(k).us_per_req.mean())
    fig, (a, b) = plt.subplots(1, 2, figsize=(COL, 3.0), sharey=True, gridspec_kw={"width_ratios": [1.15, 1]})
    y = np.arange(len(s))
    for ax, col, scale, lab in ((a, "us_per_req", 1.0, "edge CPU, $\\mu$s/req"),
                                (b, "req_per_s", 1e-3, "req/s ($10^3$)")):
        m = [tci(g.get_group(k)[col])[0] * scale for k in s]
        h = [tci(g.get_group(k)[col])[1] * scale for k in s]
        cols = [SERIES[1] if k.startswith("o") else SERIES[0] for k in s]
        ax.barh(y, m, xerr=h, color=cols, height=0.7, capsize=1.5, error_kw={"lw": 0.8})
        ax.set_xlabel(lab)
        ax.grid(axis="y", visible=False)
    a.set_yticks(y, [PROTO_LABEL.get(k, k) for k in s], fontsize=7)
    a.invert_yaxis()
    fig.tight_layout(w_pad=1.2)
    save(fig, OUT, "fig11_proto_capacity")


def fig_proto_validate():
    d = rd("proto_validate.csv")
    fig, axs = plt.subplots(1, 2, figsize=(DCOL, 2.4))
    for ax, met, lab in ((axs[0], "miss_per_token", "misses per token"), (axs[1], "miss_lat_mean_ms", "mean miss latency (ms)")):
        g = d[d.metric == met]
        for k, mode in enumerate(sorted(g["mode"].unique())):
            r = g[g["mode"] == mode]
            ax.errorbar(r.proto_mean, r.mc_mean, xerr=[r.proto_mean - r.proto_ci_lo, r.proto_ci_hi - r.proto_mean],
                        fmt=MARKERS[k], color=SERIES[k], ms=3.5, capsize=1.5, ls="none", label=mode)
        lo = min(g.proto_mean.min(), g.mc_mean.min()) * 0.8
        hi = max(g.proto_mean.max(), g.mc_mean.max()) * 1.2
        xx = np.array([max(lo, 1e-4), hi])
        ax.plot(xx, xx, color=INK2, lw=0.8)
        ax.fill_between(xx, xx * 0.85, xx * 1.15, color="#e4e3df", lw=0, label="$\\pm$15%")
        if met == "miss_per_token":
            ax.set_xscale("log"); ax.set_yscale("log")
        ax.set_xlabel("prototype (measured) " + lab)
        ax.set_ylabel("fleet_mc (simulated) " + lab)
        ax.legend(fontsize=7)
    fig.tight_layout()
    save(fig, OUT, "fig12_proto_validation")


def main():
    global IN, OUT
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default="../results")
    ap.add_argument("--out", default="../results/figures")
    a = ap.parse_args()
    IN, OUT = a.inp, a.out
    setup()
    for f in (fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig_wire, fig_proto, fig_proto_validate):
        try:
            f()
        except FileNotFoundError as e:
            print("SKIP %s: missing %s" % (f.__name__, e))
        except Exception:
            print("FAILED %s" % f.__name__)
            traceback.print_exc()


if __name__ == "__main__":
    main()
