"""Aggregate the R2 prototype CSVs (Student-t 95% CI over runs).

  python agg_r2.py [results_dir]
in : proto_capacity_r2.csv, proto_capacity_tb_r2.csv, proto_latency_runs_r2.csv, proto_recovery_r2.csv,
     raw/proto_r2/p4_req_<scenario>_r<run>.csv.gz
out: proto_capacity_r2_agg.csv, proto_capacity_tb_r2_agg.csv, proto_latency_r2.csv, proto_latency_r2_agg.csv,
     proto_recovery_r2_agg.csv, proto_recovery_events_r2.csv
"""
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats


def tci(x):
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    if len(x) == 0:
        return np.nan, np.nan, np.nan
    m = x.mean()
    if len(x) < 2:
        return m, np.nan, np.nan
    h = stats.t.ppf(0.975, len(x) - 1) * x.std(ddof=1) / np.sqrt(len(x))
    return m, m - h, m + h


def agg(df, keys, cols):
    rows = []
    for k, g in df.groupby(keys, sort=False):
        d = dict(zip(keys, k if isinstance(k, tuple) else (k,)))
        d["n_runs"] = len(g)
        for c in cols:
            d[c + "_mean"], d[c + "_ci_lo"], d[c + "_ci_hi"] = tci(g[c])
        rows.append(d)
    return pd.DataFrame(rows)


def cap(res, name):
    p = os.path.join(res, name + ".csv")
    if not os.path.exists(p):
        return None
    d = pd.read_csv(p)
    d["edge_cpu_us_per_req"] = d.cpu_util_edge / d.req_per_s * 1e6
    b1 = d[d.scheme == "b1"].set_index("run").req_per_s
    b1us = d[d.scheme == "b1"].set_index("run").edge_cpu_us_per_req
    d["ratio_vs_b1"] = d.req_per_s / d.run.map(b1)
    d["us_diff_vs_b1"] = d.edge_cpu_us_per_req - d.run.map(b1us)
    a = agg(d, ["scheme"], ["req_per_s", "edge_cpu_us_per_req", "cpu_util_edge", "p50_ms", "p99_ms", "ratio_vs_b1",
                            "us_diff_vs_b1", "retries"])
    g = d.groupby("scheme")
    a["cv_req_per_s_pct"] = a.scheme.map(g.req_per_s.std() / g.req_per_s.mean() * 100)
    a["cv_us_per_req_pct"] = a.scheme.map(g.edge_cpu_us_per_req.std() / g.edge_cpu_us_per_req.mean() * 100)
    a["cpu_util_min"] = a.scheme.map(g.cpu_util_edge.min())
    a["token_bytes"] = a.scheme.map(g.token_bytes.first())
    a["tree"] = a.scheme.map(g.tree.first())
    a.to_csv(os.path.join(res, name + "_agg.csv"), index=False, float_format="%.5g")
    return a


def main(res):
    cap(res, "proto_capacity_r2")
    cap(res, "proto_capacity_tb_r2")
    p = os.path.join(res, "proto_latency_runs_r2.csv")
    if os.path.exists(p):
        l = pd.read_csv(p)
        for col in ("p50_ms", "p99_ms"):
            base = l[l.scheme == "b1"].set_index(["load_frac", "run"])[col]
            l["added_" + col + "_vs_hmac"] = [r[col] - base.get((r.load_frac, r.run), np.nan) for _, r in l.iterrows()]
        l.to_csv(os.path.join(res, "proto_latency_r2.csv"), index=False, float_format="%.5g")
        a = agg(l, ["scheme", "load_frac"], ["rate_target", "rate_achieved", "p50_ms", "p99_ms", "added_p50_ms_vs_hmac",
                                             "added_p99_ms_vs_hmac", "errors", "retries"])
        a.to_csv(os.path.join(res, "proto_latency_r2_agg.csv"), index=False, float_format="%.5g")
    p = os.path.join(res, "proto_recovery_r2.csv")
    if os.path.exists(p):
        r = pd.read_csv(p)
        r["requests_per_token"] = r.requests / r.tokens
        r["edge_verifs_per_token"] = r.edge_verifs / r.tokens
        r["new_conns_per_token"] = r.new_conns / r.tokens
        r["recoveries_per_1k_req"] = 1000 * (r.retries + r.reconnects) / r.requests
        cols = ["tokens", "requests_per_token", "moves", "new_conns_per_token", "staple_hdr_bytes_per_token", "retries",
                "retries_per_1k_req", "retry_extra_mean_ms", "retry_extra_p99_ms", "reconnects", "reconnect_extra_mean_ms",
                "reconnect_extra_p99_ms", "recoveries_per_1k_req", "fails", "affected_frac", "req_lat_p50_ms",
                "req_lat_p99_ms", "retried_req_lat_mean_ms", "edge_verifs_per_token", "edge_m2_evictions",
                "edge_root_evictions", "issue_errors"]
        a = agg(r, ["scenario", "scheme"], cols)
        a.to_csv(os.path.join(res, "proto_recovery_r2_agg.csv"), index=False, float_format="%.5g")
        # event-level: recoveries after the flush/restart event (t = 15 s) and their timing
        ev = []
        raw = os.path.join(res, "raw", "proto_r2")
        for sc in r.scenario.unique():
            for run in sorted(r.run.unique()):
                f = os.path.join(raw, f"p4_req_{sc}_r{run}.csv.gz")
                if not os.path.exists(f):
                    continue
                q = pd.read_csv(f)
                for sch, g in q.groupby("pipe"):
                    rec = g[g.kind.isin(["retry", "reconnect"])]
                    after = rec[rec.t_off_ms >= 15000]
                    # sessions with an open connection at the event: a request in [14.6 s, 15 s) and another after 15 s
                    open_ = g[(g.t_off_ms >= 14600) & (g.t_off_ms < 15000)].tok.nunique()
                    ev.append(dict(scenario=sc, scheme=sch, run=run, recoveries=len(rec), recoveries_after_15s=len(after),
                                   recov_window_ms=(after.t_off_ms.max() - 15000) if len(after) else np.nan,
                                   sessions_active_at_event=open_, extra_mean_ms=rec.extra_ms.mean() if len(rec) else np.nan,
                                   extra_p50_ms=rec.extra_ms.median() if len(rec) else np.nan,
                                   staple_req_frac=g.stapled.mean(), fail=int((g.kind == "fail").sum())))
        if ev:
            e = pd.DataFrame(ev)
            e.to_csv(os.path.join(res, "proto_recovery_events_r2.csv"), index=False, float_format="%.5g")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "results"))
