"""Workload model (assumptions; every value appears in Table IV via results/sim_params.json)."""
import json

import numpy as np

SEED = 20261105

DEFAULTS = dict(
    E=500,                 # edges
    alpha_e=0.8,           # Zipf exponent of edge traffic share
    T=1000,                # tenants
    alpha_t=1.0,           # Zipf exponent of tenant rate share
    lam_bar=2000.0,        # aggregate mean token (session) rate, tokens/s
    diurnal_a=0.6,         # diurnal amplitude
    horizon_s=86400.0,
    K_mean=150.0,          # segments per session (geometric)
    seg_interval_s=4.0,
    p_move=0.01,           # per-segment probability that a request lands on a different edge (anycast/failover)
    v_max_s=3600.0,
    P_s=300.0,             # period (roll-up) length in seconds
    rtt_ce_ms=(20.0, 0.6),     # client->edge RTT lognormal (median, sigma)
    rtt_es_ms=(15.0, 0.5),     # edge->shield
    rtt_sr_ms=(60.0, 0.5),     # shield->root service
    push_ms=(150.0, 0.5),      # push propagation delay
    first_req_ms=(120.0, 0.5),  # token receipt -> first request
    shields_per_edge=0.1,  # shields = E/10
    seg_bytes=1.5e6,       # mean segment size (bandwidth ratio only)
    n=16,
    root_signer="ML-DSA-44",
    claims_bytes=104,      # canonical claims bytes (60-char path, no IP; token_sizes.csv)
    slo_s=2.0,             # controller L_SLO on p99 issuance wait
    budget_B=1024,         # controller token budget (bytes)
    ewma=0.2,
    grid_n=25, grid_lo=0.01, grid_hi=60.0,
    n_shards=8,            # pooling shards
)


def zipf_shares(k, alpha, rng=None, permute=True):
    w = 1.0 / np.arange(1, k + 1) ** alpha
    w /= w.sum()
    if permute and rng is not None:
        w = w[rng.permutation(k)]
    return w


def tenant_rates(T, alpha_t, lam_bar):
    return lam_bar * zipf_shares(T, alpha_t, permute=False)


def tenant_phases(T, rng):
    return rng.uniform(0, np.pi / 2, T)


def nhpp(rng, lam, a, phase, t0, t1):
    """Arrival times on [t0, t1) for lam(t) = lam(1 + a sin(2 pi t / 86400 + phase)), by thinning."""
    lmax = lam * (1 + a)
    n = rng.poisson(lmax * (t1 - t0))
    t = np.sort(rng.uniform(t0, t1, n))
    if a > 0:
        keep = rng.uniform(0, 1, n) * (1 + a) < 1 + a * np.sin(2 * np.pi * t / 86400.0 + phase)
        t = t[keep]
    return t


def lognorm(rng, med_sigma, size):
    m, s = med_sigma
    return m / 1000.0 * np.exp(s * rng.standard_normal(size))


def lognorm_mean_s(med_sigma):
    m, s = med_sigma
    return m / 1000.0 * np.exp(s * s / 2)


def tokens(rng, arr, cumw, p):
    """Per-token random draws (common random numbers across policies)."""
    n = arr.size
    edge = np.searchsorted(cumw, rng.uniform(0, 1, n), side="right").astype(np.int64)
    edge = np.minimum(edge, cumw.size - 1)
    d0 = lognorm(rng, p["first_req_ms"], n)
    K = rng.geometric(1.0 / p["K_mean"], n).astype(np.int64)
    nm = rng.binomial(K, p["p_move"]).astype(np.int64)
    m = int(nm.sum())
    mv_tok = np.repeat(np.arange(n, dtype=np.int64), nm)
    mv_off = (np.floor(rng.uniform(0, 1, m) * K[mv_tok]) + 1) * p["seg_interval_s"]
    mv_edge = np.minimum(np.searchsorted(cumw, rng.uniform(0, 1, m), side="right"), cumw.size - 1).astype(np.int64)
    return edge, d0, K, mv_tok, mv_off, mv_edge


def dump_params(path, extra=None):
    d = dict(DEFAULTS)
    d["seed"] = SEED
    d["seed_rule"] = "replicate r uses SEED + 1000*r; per (tenant, chunk) SeedSequence([SEED+1000r, tenant, chunk])"
    if extra:
        d.update(extra)
    with open(path, "w") as f:
        json.dump(d, f, indent=1)
