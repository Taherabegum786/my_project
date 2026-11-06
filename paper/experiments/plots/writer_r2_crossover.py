"""R2 writer: analytic requests-per-token crossover between M2 and pooled EMBER at the edge.

python -m plots.writer_r2_crossover --in ../results
Inputs (measured, native OpenSSL run 2): native_sig_agg.csv (ML-DSA-44 verify median),
native_pathverify_agg.csv (evp pathverify n=16 medians by depth d), token_sizes_r1.csv (M2 token,
M2 staple header line, EMBER encoder size formula checked against log2N 5/8/14).
Model (same as sim/trace.py, per verifier):
  M2    edge us/request = t_verify / K + path(0)          (one staple verification per token, then a hash)
  EMBER edge us/request = path(d)                          (root already held: amortised over the pool)
  M2    bytes/request   = 148 + 3242 / K                   (URL token + one HTTP/1.1 staple line per token)
  EMBER bytes/request   = S_tok(d)                         (Eq. size; root staple amortised over the pool)
  K*_cpu(d)   = t_verify / (path(d) - path(0));  K*_bytes(d) = 3242 / (S_tok(d) - 148)
K is the number of requests a token carries at one verifier. Outputs: r2_k_crossover.csv,
figures/fig18_k_crossover.{pdf,png}.
"""
import argparse
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402


def s_tok(d, c_enc=118):
    return c_enc + 3 + math.ceil(4 * (30 + 16 * d) / 3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default="../results")
    a = ap.parse_args()
    sig = pd.read_csv(os.path.join(a.inp, "native_sig_agg.csv"))
    tv = float(sig[(sig.scheme == "ML-DSA-44") & (sig.op == "verify")].median_us.iloc[0])
    pv = pd.read_csv(os.path.join(a.inp, "native_pathverify_agg.csv"))
    pv = pv[(pv.impl == "evp") & (pv.op == "pathverify") & (pv.n == 16)].set_index("d").ns_median / 1000.0
    ts = pd.read_csv(os.path.join(a.inp, "token_sizes_r1.csv"))
    m2 = ts[(ts.scheme == "M2-B5s") & (ts.url_path_len == 60) & (ts.with_ip == 0)].iloc[0]
    m2_tok, m2_staple = int(m2.token_bytes), int(m2.staple_header_http11_bytes)
    em = ts[(ts.scheme == "EMBER-O1") & (ts.url_path_len == 60) & (ts.with_ip == 0)]
    for _, r in em.iterrows():  # the formula must reproduce the encoder
        assert s_tok(int(r.log2N)) == int(r.token_bytes), (r.log2N, r.token_bytes)
    p0 = float(pv.loc[0])
    rows = []
    for d in (5, 8, 9, 12, 16, 20, 24):
        rows.append(dict(d=d, path_us=float(pv.loc[d]), token_B=s_tok(d),
                         Kstar_cpu=tv / (float(pv.loc[d]) - p0),
                         Kstar_bytes=m2_staple / (s_tok(d) - m2_tok)))
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(a.inp, "r2_k_crossover.csv"), index=False)
    print("t_verify %.3f us, path(0) %.3f us, M2 token %d B, staple line %d B" % (tv, p0, m2_tok, m2_staple))
    print(out.to_string(index=False, float_format=lambda x: "%.2f" % x))

    K = np.logspace(0, 3, 400)
    plt.rcParams.update({"font.size": 7.5, "axes.titlesize": 7.5, "legend.fontsize": 6.5})
    fig, ax = plt.subplots(1, 2, figsize=(3.5, 1.75))
    cols = {5: "#2a78d6", 12: "#e8663a", 16: "#1aab78"}
    for i in (0, 1):
        ax[i].axvspan(1.71, 2.36, color="0.85", lw=0)
        ax[i].axvline(150, color="0.4", ls=":", lw=0.8)
        ax[i].set_xscale("log")
        ax[i].set_xlabel("requests per token per verifier, $K$")
        ax[i].grid(alpha=0.3, lw=0.4)
    ax[0].plot(K, tv / K + p0, color="#c2185b", lw=1.3, label="M2")
    ax[1].plot(K, m2_tok + m2_staple / K, color="#c2185b", lw=1.3, label="M2")
    for d, c in cols.items():
        ax[0].axhline(float(pv.loc[d]), color=c, lw=1.0, ls="--", label="EMBER $d{=}%d$" % d)
        ax[1].axhline(s_tok(d), color=c, lw=1.0, ls="--", label="EMBER $d{=}%d$" % d)
    ax[0].set_yscale("log")
    ax[0].set_ylabel("edge crypto, $\\mu$s/request")
    ax[1].set_yscale("log")
    ax[1].set_ylabel("token + staple, B/request")
    ax[0].set_title("(a) edge CPU")
    ax[1].set_title("(b) bytes")
    ax[0].text(2.0, 0.3, "trace", ha="center", fontsize=6)
    ax[0].text(150, 60, "synthetic", ha="right", fontsize=6, rotation=90)
    ax[0].legend(loc="upper right", frameon=False, handlelength=1.6)
    fig.tight_layout(pad=0.3, w_pad=0.6)
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(a.inp, "figures", "fig18_k_crossover." + ext), dpi=300)


if __name__ == "__main__":
    main()
