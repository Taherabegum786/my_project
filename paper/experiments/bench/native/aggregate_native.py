"""Aggregate native runs: median of run-medians + bootstrap 95% CI over run-medians (2000 resamples),
pooled p99 from raw samples.  Writes native_sig_agg.csv and native_pathverify_agg.csv."""
import os
import sys

import numpy as np
import pandas as pd

out = sys.argv[1]
rng = np.random.default_rng(20261105)


def boot(x, B=2000):
    x = np.asarray(x, float)
    if len(x) < 2:
        return x[0], x[0]
    m = np.median(x[rng.integers(0, len(x), (B, len(x)))], axis=1)
    return np.percentile(m, 2.5), np.percentile(m, 97.5)


df = pd.read_csv(os.path.join(out, "native_sig.csv"))
rows = []
for (s, op), g in df.groupby(["scheme", "op"], sort=False):
    lo, hi = boot(g.median_us)
    raw = []
    for r in g.run:
        f = os.path.join(out, "raw", "native_%s_%s_r%d.bin" % (s, op, r))
        if os.path.exists(f):
            raw.append(np.fromfile(f, dtype=np.float64))
    raw = np.concatenate(raw) if raw else np.array([np.nan])
    rows.append(dict(scheme=s, op=op, impl="openssl-3.5.4-native", runs=len(g), n_iter=int(g.n_iter.iloc[0]),
                     median_us=float(np.median(g.median_us)), ci95_lo_us=lo, ci95_hi_us=hi,
                     p99_us=float(np.percentile(raw, 99)), mean_us=float(np.mean(raw)),
                     sig_bytes=int(g.sig_bytes.iloc[0]), pk_bytes=int(g.pk_bytes.iloc[0])))
pd.DataFrame(rows).to_csv(os.path.join(out, "native_sig_agg.csv"), index=False, float_format="%.3f")

pv = pd.read_csv(os.path.join(out, "native_pathverify.csv"))
rows = []
for (impl, op, d, n), g in pv.groupby(["impl", "op", "d", "n"], sort=False):
    lo, hi = boot(g.ns_per_op_median)
    rows.append(dict(impl=impl, op=op, d=d, n=n, runs=len(g), iters_per_run=int(g.iters.iloc[0]),
                     ns_median=float(np.median(g.ns_per_op_median)), ci95_lo_ns=lo, ci95_hi_ns=hi,
                     ns_p99=float(np.max(g.ns_per_op_p99))))
pd.DataFrame(rows).to_csv(os.path.join(out, "native_pathverify_agg.csv"), index=False, float_format="%.2f")
print("aggregated native results")

f = os.path.join(out, "native_issuer.csv")
if os.path.exists(f):
    d = pd.read_csv(f)
    rows = []
    for (a, N, n), g in d.groupby(["root_alg", "N", "n"], sort=False):
        lo, hi = boot(g.tokens_per_s)
        r = dict(root_alg=a, N=N, n=n, runs=len(g), impl="openssl-3.5.4-native")
        for c in ("t_leaf_us", "t_tree_us", "t_sign_us", "t_encode_us", "t_epoch_us", "tokens_per_s"):
            r[c] = float(np.median(g[c]))
        r["tps_ci95_lo"], r["tps_ci95_hi"] = lo, hi
        rows.append(r)
    pd.DataFrame(rows).to_csv(os.path.join(out, "native_issuer_agg.csv"), index=False, float_format="%.3f")
