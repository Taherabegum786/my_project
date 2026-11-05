"""Simulation driver shared by all E5 experiments: generates the workload with common random numbers, applies
an epoch policy per tenant (or pooled shard), replays requests per dissemination mode with the numba kernel,
and accumulates constant-memory statistics."""
import math

import numpy as np

from ember.controller import Adaptive
from sim import fleet_mc as F
from sim import model as M
from sim.workload import DEFAULTS, SEED, lognorm_mean_s, nhpp, tenant_phases, tenant_rates, tokens, zipf_shares

BLOCK = 1 << 20
NB_TS = 288


class Acc:
    """Accumulator for one (policy, mode)."""

    def __init__(self, ts_bins=0, n_dec=10):
        self.hW = np.zeros(F.H_NB)
        self.hD = np.zeros(F.H_NB)
        self.hMiss = np.zeros(F.H_NB)   # waits of fetch-initiating requests
        self.hCoal = np.zeros(F.H_NB)   # waits of coalesced requests
        self.tokens = 0
        self.requests = 0.0
        self.sumW = self.sumD = 0.0
        self.cnt = np.zeros(8, np.int64)
        self.nver = 0
        self.tokens_missed = 0
        self.cpu_vals = {}   # cost (s) -> weight (requests)
        self.bytes_pull = 0.0
        self.bytes_push = 0.0
        self.bytes_staple = 0.0
        self.edge_verifs_push = 0.0
        self.epochs = 0
        self.periods = 0
        self.d_hist = np.zeros(64)
        self.refresh = 0.0
        self.dec_D = np.zeros(n_dec)
        self.dec_n = np.zeros(n_dec)
        self.dec_W99 = [np.zeros(F.H_NB) for _ in range(n_dec)]
        self.model_M = 0.0
        self.model_D = 0.0
        if ts_bins:
            self.ts_n = np.zeros(ts_bins)
            self.ts_D = np.zeros(ts_bins)
            self.ts_miss = np.zeros(ts_bins)
            self.ts_delta = np.zeros(ts_bins)
            self.ts_dmax = np.zeros(ts_bins)
            self.ts_hW = np.zeros((ts_bins, F.H_NB))
        self.ts_bins = ts_bins

    def add_cpu(self, vals, wts):
        u, inv = np.unique(vals, return_inverse=True)
        s = np.bincount(inv, weights=wts)
        for a, b in zip(u, s):
            self.cpu_vals[a] = self.cpu_vals.get(a, 0.0) + b

    def cpu_stats(self):
        v = np.array(sorted(self.cpu_vals))
        w = np.array([self.cpu_vals[x] for x in v])
        if w.sum() == 0:
            return float("nan"), float("nan")
        c = np.cumsum(w) / w.sum()
        return float((v * w).sum() / w.sum()), float(v[np.searchsorted(c, 0.99)])


class Sim:
    def __init__(self, costs, **over):
        p = dict(DEFAULTS)
        p.update(over)
        self.p = p
        self.c = costs
        self.E = int(p["E"])
        self.S = max(1, int(round(self.E * p["shields_per_edge"])))
        rs = p.get("rtt_scale", 1.0)
        self.es = (p["rtt_es_ms"][0] * rs, p["rtt_es_ms"][1])
        self.sr = (p["rtt_sr_ms"][0] * rs, p["rtt_sr_ms"][1])
        self.pu = (p["push_ms"][0] * rs, p["push_ms"][1])

    def run(self, rep, policies, modes, t0=0.0, t1=None, pool=0, ts=False, decile=True, e2e_res=None):
        p, c = self.p, self.c
        t1 = p["horizon_s"] if t1 is None else t1
        rng0 = np.random.default_rng(SEED + 1000 * rep)
        w = zipf_shares(self.E, p["alpha_e"], rng0)
        cumw = np.cumsum(w)
        cumw[-1] = 1.0
        lam = tenant_rates(p["T"], p["alpha_t"], p["lam_bar"])
        phase = tenant_phases(p["T"], rng0)
        rank_dec = (np.arange(p["T"]) * 10) // p["T"]   # tenant index = rank (rates sorted descending)
        es_mean, sr_mean = lognorm_mean_s(self.es), lognorm_mean_s(self.sr)
        adapt = Adaptive(w, self.S, es_mean, sr_mean, c.t_tok, c.t_sign, slo=p["slo_s"], budget_B=p["budget_B"],
                         claims_bytes=p["claims_bytes"], n=p["n"],
                         grid=np.logspace(np.log10(p["grid_lo"]), np.log10(p["grid_hi"]), p["grid_n"]), alpha=p["ewma"])
        nmax = int(adapt.nmax)
        accs = {(pol, m): Acc(NB_TS if ts else 0) for pol in policies for m in modes}
        # tenant groups
        if pool:
            groups = [np.arange(g, p["T"], p["n_shards"]) for g in range(p["n_shards"])]
        else:
            groups = [np.array([t]) for t in range(p["T"])]
        P = p["P_s"]
        Mtab_x = None
        for gi, grp in enumerate(groups):
            arrs = []
            for tnt in grp:
                hrs = np.arange(math.floor(t0 / 3600), math.ceil(t1 / 3600))
                parts = []
                for h in hrs:
                    r = np.random.default_rng([SEED + 1000 * rep, int(tnt), int(h), 1])
                    a = nhpp(r, lam[tnt], p["diurnal_a"], phase[tnt], max(t0, h * 3600.0), min(t1, (h + 1) * 3600.0))
                    parts.append(a)
                arrs.append(np.concatenate(parts) if parts else np.zeros(0))
            if pool:
                tid = np.concatenate([np.full(a.size, t) for a, t in zip(arrs, grp)])
                arr = np.concatenate(arrs)
                o = np.argsort(arr, kind="stable")
                arr, tid = arr[o], tid[o]
            else:
                arr = arrs[0]
            n = arr.size
            if n == 0:
                continue
            lam_g = lam[grp].sum()
            dec = 0 if pool else rank_dec[grp[0]]
            # token-level randoms in blocks (CRN across policies and modes)
            blocks = {}

            def block(b):
                if b not in blocks:
                    r = np.random.default_rng([SEED + 1000 * rep, int(gi), int(b), 2 + pool])
                    lo, hi = b * BLOCK, min(n, (b + 1) * BLOCK)
                    blocks[b] = tokens(r, arr[lo:hi], cumw, p)
                return blocks[b]

            for pol in policies:
                if pol.startswith("fixed:"):
                    delta = float(pol.split(":")[1])
                    tok_ep, ep_close, ep_N = F.epochs_fixed(arr, delta, nmax)
                    ep_delta = np.full(ep_close.size, delta)
                elif pol == "wc":
                    tok_ep, ep_close, ep_N = F.epochs_wc(arr, c.t_tok, c.t_sign)
                    ep_delta = np.diff(np.concatenate([[arr[0]], ep_close]))
                elif pol == "adaptive":
                    tok_ep, ep_close, ep_N, ep_delta = adapt.epochs(arr, lam_g, t0)
                else:
                    raise ValueError(pol)
                ep_issue = F.issue_times(ep_close, ep_N, c.t_tok, c.t_sign)
                ep_d = np.ceil(np.log2(np.maximum(ep_N, 1))).astype(np.int64)
                ep_cost = c.path_cost(ep_d)
                ep_period = np.floor(ep_close / P).astype(np.int64)
                p0 = ep_period[0]
                ep_period_l = ep_period - p0
                nper = int(ep_period_l[-1]) + 1
                m_per = np.bincount(ep_period_l, minlength=nper)
                per_avail = (np.arange(nper) + p0 + 1) * P + c.t_sign
                nonempty_periods = int((m_per > 0).sum())
                mean_bundle = c.bundle_bytes(m_per[m_per > 0].mean())
                tok_issue_all = ep_issue[tok_ep]
                W_all = tok_issue_all - arr
                for m in modes:
                    A = accs[(pol, m)]
                    mid = F.MODE_ID[m]
                    A.epochs += ep_close.size
                    A.periods += nonempty_periods
                    if m == "push":
                        A.bytes_push += ep_close.size * (self.E + self.S) * c.sr_bytes
                        A.edge_verifs_push += ep_close.size * self.E
                    if m == "push_rollup":
                        A.bytes_push += ((m_per > 0) * c.bundle_bytes(m_per) * (self.E + self.S)).sum()
                        A.edge_verifs_push += nonempty_periods * self.E
                    # chunks aligned to epoch boundaries
                    i0 = 0
                    while i0 < n:
                        i1 = min(n, i0 + BLOCK)
                        if i1 < n:
                            k = tok_ep[i1]
                            i1 = int(np.searchsorted(tok_ep, k, side="left"))
                            if i1 <= i0:
                                i1 = int(np.searchsorted(tok_ep, k, side="right"))
                        b0, b1 = i0 // BLOCK, (i1 - 1) // BLOCK
                        ed, d0, K, mvt, mvo, mve = [], [], [], [], [], []
                        for b in range(b0, b1 + 1):
                            e_, d_, K_, mt_, mo_, me_ = block(b)
                            lo = b * BLOCK
                            s_, t_ = max(i0, lo) - lo, min(i1, lo + e_.size) - lo
                            ed.append(e_[s_:t_]); d0.append(d_[s_:t_]); K.append(K_[s_:t_])
                            sel = (mt_ >= s_) & (mt_ < t_)
                            mvt.append(mt_[sel] + lo - i0); mvo.append(mo_[sel]); mve.append(me_[sel])
                        ed = np.concatenate(ed); d0 = np.concatenate(d0); K = np.concatenate(K)
                        mvt = np.concatenate(mvt); mvo = np.concatenate(mvo); mve = np.concatenate(mve)
                        if mid in (0, 1, 2, 3, 4) and p["p_move"] == 0:
                            mvt = mvt[:0]; mvo = mvo[:0]; mve = mve[:0]
                        te = tok_ep[i0:i1]
                        salt = (SEED + 1000 * rep) * 7 + gi * 131 + 17
                        tw, nver, rw, rk, cnt = F.kernel(mid, te, tok_issue_all[i0:i1], ed, d0, mvt, mvo, mve,
                                                         ep_issue, ep_period_l, per_avail, self.S, salt,
                                                         self.es[0], self.es[1], self.sr[0], self.sr[1],
                                                         self.pu[0], self.pu[1])
                        W = W_all[i0:i1]
                        D = W + tw
                        A.tokens += W.size
                        req = (1.0 + K)
                        A.requests += req.sum()
                        A.sumW += W.sum(); A.sumD += D.sum()
                        F.hist_add(A.hW, W); F.hist_add(A.hD, D)
                        F.hist_add(A.hMiss, rw[rk == 1]); F.hist_add(A.hCoal, rw[rk == 2])
                        A.cnt += cnt
                        A.nver += int(nver.sum())
                        A.tokens_missed += int((tw > 0).sum())
                        A.bytes_pull += (cnt[0] + cnt[1]) * c.sr_bytes + (cnt[2] + cnt[3]) * mean_bundle
                        if m == "pull_staple":
                            A.bytes_staple += W.size * c.sr_bytes
                        cost = ep_cost[te]
                        A.add_cpu(np.concatenate([cost, cost + c.t_verify]),
                                  np.concatenate([req - nver, nver.astype(float)]))
                        dd = ep_d[te]
                        A.d_hist += np.bincount(dd, minlength=64)[:64]
                        A.refresh += np.floor(K * p["seg_interval_s"] / p["v_max_s"]).sum()
                        if decile:
                            dd_ = tid[i0:i1] if pool else None
                            if pool:
                                pass
                            else:
                                A.dec_D[dec] += D.sum(); A.dec_n[dec] += D.size
                                F.hist_add(A.dec_W99[dec], W)
                        if A.ts_bins:
                            bi = np.clip(((arr[i0:i1] - t0) / ((t1 - t0) / A.ts_bins)).astype(int), 0, A.ts_bins - 1)
                            A.ts_n += np.bincount(bi, minlength=A.ts_bins)
                            A.ts_D += np.bincount(bi, weights=D, minlength=A.ts_bins)
                            A.ts_miss += np.bincount(bi, weights=(nver > 0).astype(float), minlength=A.ts_bins)
                            A.ts_delta += np.bincount(bi, weights=ep_delta[te], minlength=A.ts_bins)
                            np.maximum.at(A.ts_dmax, bi, dd.astype(float))
                            np.add.at(A.ts_hW, (bi, F.hidx(W)), 1.0)
                        if e2e_res is not None and (pol, m) in e2e_res:
                            e2e_res[(pol, m)].append((rw.copy(), rk.copy(), req.sum(), cost, req, nver))
                        i0 = i1
                # model (pull, first-request misses only), token-weighted
                if not pol.startswith("fixed:"):
                    continue
                x = lam_g * delta
                Mx = M.miss_per_token(np.array([x]), w)[0]
                Fx = M.fetch_penalty(w, self.E, self.S, es_mean, sr_mean, x)
                for m in modes:
                    A = accs[(pol, m)]
                    A.model_M += n * Mx
                    A.model_D += n * (delta / 2 + x * c.t_tok + c.t_sign + Mx * Fx)
        self.horizon = t1 - t0
        return accs

    def summary(self, A):
        """Flat dict of the standard metrics for one accumulator."""
        p, c = self.p, self.c
        H = self.horizon
        cpu_mean, cpu_p99 = A.cpu_stats()
        miss = A.cnt[0] + A.cnt[2]
        d_nz = np.nonzero(A.d_hist)[0]
        served = A.requests * p["seg_bytes"]
        tb = [M.token_bytes(p["claims_bytes"], p["n"], int(d)) for d in d_nz]
        wts = A.d_hist[d_nz]
        cdf = np.cumsum(wts) / wts.sum()
        root_bw = (A.bytes_pull + A.bytes_push) / H
        return dict(
            issue_wait_mean_s=A.sumW / A.tokens, issue_wait_p99_s=F.hist_q(A.hW, 0.99),
            miss_per_token=miss / A.tokens, miss_per_mreq=miss / A.requests * 1e6,
            miss_latency_p99_ms=1000 * F.hist_q(A.hMiss + A.hCoal, 0.99) if (A.hMiss.sum() + A.hCoal.sum()) > 0 else 0.0,
            D_mean_s=A.sumD / A.tokens, root_bw_fleet_Bps=root_bw,
            root_bw_ratio=root_bw / (served / H), edge_cpu_us_per_req_mean=cpu_mean * 1e6,
            edge_cpu_us_per_req_p99=cpu_p99 * 1e6,
            sig_verifs_per_edge_per_s=(A.nver + A.edge_verifs_push) / self.E / H,
            tok_bytes_p50=tb[int(np.searchsorted(cdf, 0.5))], tok_bytes_max=max(tb),
            model_miss_per_token=A.model_M / A.tokens if A.model_M else "",
            model_D_s=A.model_D / A.tokens if A.model_D else "",
            refresh_per_session=A.refresh / A.tokens,
            frac_req_waiting=(A.hMiss.sum() + A.hCoal.sum()) / A.requests,
            staple_bytes_per_session=A.bytes_staple / A.tokens,
            tokens=A.tokens, requests=A.requests, epochs=A.epochs,
        )
