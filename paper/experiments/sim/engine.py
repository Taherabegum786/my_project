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
        self.cpu_d = np.zeros(64)      # requests by path length d without a signature verification
        self.cpu_dv = np.zeros(64)     # requests by d that also verified a root/bundle/staple signature
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
        # R1 additions
        self.dec_dhist = np.zeros((n_dec, 64))   # tokens by (tenant-rate decile, d = ceil(log2 N_e))
        self.issuer_cpu_s = 0.0                  # leaf/tree/encode + root (or per-token) signatures
        self.moves = 0
        self.edge_ver = None                     # per-edge signature verifications (first-edge attribution)
        self.edge_req = None
        self.edge_path_s = None
        if ts_bins:
            self.ts_n = np.zeros(ts_bins)
            self.ts_D = np.zeros(ts_bins)
            self.ts_miss = np.zeros(ts_bins)
            self.ts_delta = np.zeros(ts_bins)
            self.ts_dmax = np.zeros(ts_bins)
            self.ts_hW = np.zeros((ts_bins, F.H_NB))
        self.ts_bins = ts_bins

    def cpu_stats(self, costs):
        d = np.arange(64)
        ok = (self.cpu_d + self.cpu_dv) > 0
        base = costs.path_cost(d[ok])
        v = np.concatenate([base, base + costs.t_verify])
        w = np.concatenate([self.cpu_d[ok], self.cpu_dv[ok]])
        o = np.argsort(v)
        v, w = v[o], w[o]
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

    def _groups(self, rep, pool, lam, phase, w, t0, t1):
        p = self.p

        def tenant_arr(tnt):
            parts = []
            for h in np.arange(math.floor(t0 / 3600), math.ceil(t1 / 3600)):
                r = np.random.default_rng([SEED + 1000 * rep, int(tnt), int(h), 1])
                parts.append(nhpp(r, lam[tnt], p["diurnal_a"], phase[tnt], max(t0, h * 3600.0), min(t1, (h + 1) * 3600.0)))
            return np.concatenate(parts) if parts else np.zeros(0)

        def merge(grp):
            arrs = [tenant_arr(t) for t in grp]
            tid = np.concatenate([np.full(a.size, t) for a, t in zip(arrs, grp)])
            arr = np.concatenate(arrs)
            o = np.argsort(arr, kind="stable")
            return arr[o], tid[o]

        if pool == 2:
            # R1 region pooling: region of edge e = e % R.  Each token's region is drawn with the region's traffic
            # share; its first edge is drawn inside the region (re-routes may go to any edge).
            R = int(p["regions"])
            reg = np.arange(self.E) % R
            share = np.bincount(reg, weights=w, minlength=R)
            arr_all, tid_all = merge(np.arange(p["T"]))
            rr = np.random.default_rng([SEED + 1000 * rep, 77])
            cs = np.cumsum(share)
            cs[-1] = 1.0
            reg_all = np.minimum(np.searchsorted(cs, rr.uniform(0, 1, arr_all.size), side="right"), R - 1)

            def gen(gi, g):
                sel = reg_all == g
                cw = np.cumsum(w * (reg == g)) / share[g]
                cw[-1] = 1.0
                return arr_all[sel], tid_all[sel], lam.sum() * share[g], cw
            return list(range(R)), gen
        if pool:
            groups = [np.arange(g, p["T"], p["n_shards"]) for g in range(p["n_shards"])]

            def gen(gi, grp):
                arr, tid = merge(grp)
                return arr, tid, lam[grp].sum(), None
            return groups, gen

        def gen(gi, grp):
            return tenant_arr(grp[0]), None, lam[grp].sum(), None
        return [np.array([t]) for t in range(p["T"])], gen

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
        # tenant groups (pool 0: per tenant; pool 1: n_shards interleaved tenant shards (n_shards=1: one pool
        # for all tenants of the issuer key); pool 2 (R1): one pool per edge region, all tenants)
        P = p["P_s"]
        Mtab_x = None
        groups, gen = self._groups(rep, pool, lam, phase, w, t0, t1)
        for gi, grp in enumerate(groups):
            arr, tid, lam_g, cumw_g = gen(gi, grp)
            n = arr.size
            if n == 0:
                continue
            dec = 0 if pool else rank_dec[grp[0]]
            # token-level randoms in blocks (CRN across policies and modes)
            blocks = {}

            def block(b):
                if b not in blocks:
                    r = np.random.default_rng([SEED + 1000 * rep, int(gi), int(b), 2 + pool])
                    lo, hi = b * BLOCK, min(n, (b + 1) * BLOCK)
                    blocks[b] = tokens(r, arr[lo:hi], cumw if cumw_g is None else cumw_g, p, cumw_mv=cumw)
                return blocks[b]

            for pol in policies:
                if pol.startswith("fixed:"):
                    delta = float(pol.split(":")[1])
                    tok_ep, ep_close, ep_N = F.epochs_fixed(arr, delta, nmax)
                    ep_delta = np.full(ep_close.size, delta)
                elif pol == "pertoken":
                    # R1 baseline M2/B5s: one ML-DSA signature per token (a "tree" of N = 1), issued at once
                    tok_ep = np.arange(n, dtype=np.int64)
                    ep_close = arr.copy()
                    ep_N = np.ones(n, np.int64)
                    ep_delta = np.zeros(n)
                elif pol == "wc":
                    tok_ep, ep_close, ep_N = F.epochs_wc(arr, c.t_tok, c.t_sign)
                    ep_delta = np.diff(np.concatenate([[arr[0]], ep_close]))
                elif pol == "adaptive":
                    tok_ep, ep_close, ep_N, ep_delta = adapt.epochs(arr, lam_g, t0)
                else:
                    raise ValueError(pol)
                if pol == "pertoken":
                    # enough signer cores (issuer cores are reported); no queueing between tokens
                    ep_issue = ep_close + c.t_sign
                    iss_cpu = n * c.t_sign
                else:
                    ep_issue = F.issue_times(ep_close, ep_N, c.t_tok, c.t_sign)
                    iss_cpu = ep_close.size * c.t_sign + n * c.t_tok
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
                    A.issuer_cpu_s += iss_cpu
                    if A.edge_ver is None:
                        A.edge_ver = np.zeros(self.E); A.edge_req = np.zeros(self.E); A.edge_path_s = np.zeros(self.E)
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
                        if m == "staple_always":
                            A.bytes_staple += (W.size + mvt.size) * c.sr_bytes
                        A.moves += mvt.size
                        dd = ep_d[te]
                        A.cpu_d += np.bincount(dd, weights=req - nver, minlength=64)[:64]
                        A.cpu_dv += np.bincount(dd, weights=nver.astype(float), minlength=64)[:64]
                        A.d_hist += np.bincount(dd, minlength=64)[:64]
                        decs = rank_dec[tid[i0:i1]] if tid is not None else np.full(dd.size, dec)
                        A.dec_dhist += np.bincount(decs * 64 + np.minimum(dd, 63), minlength=640)[:640].reshape(10, 64)
                        A.edge_ver += np.bincount(ed, weights=nver.astype(float), minlength=self.E)
                        A.edge_req += np.bincount(ed, weights=req, minlength=self.E)
                        A.edge_path_s += np.bincount(ed, weights=req * ep_cost[te], minlength=self.E)
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
                            A.ts_hW += np.bincount(bi * F.H_NB + F.hidx(W), minlength=A.ts_bins * F.H_NB).reshape(A.ts_bins, F.H_NB)
                        if e2e_res is not None and (pol, m) in e2e_res:
                            e2e_res[(pol, m)].append((rw.copy(), rk.copy(), dd.copy(), req.copy(), nver.copy()))
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
        cpu_mean, cpu_p99 = A.cpu_stats(c)
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
            **self.r1_summary(A),
        )

    def r1_summary(self, A):
        """R1 metrics: tree-size distribution, issuer cost, busiest-edge CPU, staple installs, amortisation."""
        p, c = self.p, self.c
        H = self.horizon
        dh = A.d_hist
        cdf = np.cumsum(dh) / dh.sum()
        tb = lambda d: M.token_bytes(p["claims_bytes"], p["n"], int(d))
        verifs = A.nver + A.edge_verifs_push
        ev = A.edge_ver + A.edge_verifs_push / self.E
        cpu_edge = (ev * c.t_verify + A.edge_path_s) / H
        top = int(np.argmax(A.edge_req))
        out = dict(
            frac_tok_N1=dh[0] / dh.sum(),
            frac_tok_N_le4=dh[:3].sum() / dh.sum(),
            d_p50=int(np.searchsorted(cdf, 0.5)), d_p99=int(np.searchsorted(cdf, 0.99)),
            tok_bytes_p99=tb(int(np.searchsorted(cdf, 0.99))),
            mean_tokens_per_tree=A.tokens / A.epochs,
            issuer_sigs_per_s=A.epochs / H,
            issuer_cpu_cores=A.issuer_cpu_s / H,
            issuer_cpu_us_per_token=A.issuer_cpu_s / A.tokens * 1e6,
            staple_installs_per_token=A.cnt[4] / A.tokens,
            moves_per_token=A.moves / A.tokens,
            req_per_sig_verify=A.requests / verifs if verifs else float("inf"),
            edge_verifs_total_per_s=verifs / H,
            busiest_edge_req_per_s=A.edge_req[top] / H,
            busiest_edge_verifs_per_s=ev[top] / H,
            busiest_edge_cpu_frac=cpu_edge[top],
            max_edge_cpu_frac=float(cpu_edge.max()),
            fleet_edge_cpu_cores=float(cpu_edge.sum()),
        )
        for k in range(10):
            dk = A.dec_dhist[k]
            if dk.sum() > 0:
                ck = np.cumsum(dk) / dk.sum()
                out["dec%d_frac_N1" % k] = dk[0] / dk.sum()
                out["dec%d_d_p50" % k] = int(np.searchsorted(ck, 0.5))
                out["dec%d_tokens" % k] = dk.sum()
        return out
