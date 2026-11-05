"""E3: fraction of tokens fitting URL / cookie / header limits under a URL-path-length distribution.

python -m bench.fit_analysis --out ../results     (needs token_sizes.csv)
Path length L ~ lognormal(median 80 chars, sigma 0.5) [assumption, Table IV], 1e5 samples, clipped to [10, 4000].
Token bytes for a sample = measured auth part (token_bytes - claims_bytes at url_path_len=60, no IP, from
token_sizes.csv) + exact canonical claims length for that L (computed with ember.token.enc).
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ember.token import Claims, enc

HOST = "https://cdn.example.com"
LIMITS = {"url2k": 2048, "url8k": 8000, "cookie4k": 4096, "hdr8k": 8192}
OTHER_HDR = 600


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="../results")
    ap.add_argument("--samples", type=int, default=100000)
    a = ap.parse_args()
    rng = np.random.default_rng(20261105)
    L = np.clip(np.round(rng.lognormal(np.log(80), 0.5, a.samples)), 10, 4000).astype(int)
    uniq = np.unique(L)
    clen = {l: len(enc(Claims("/" + "x" * (l - 1), 1800001800, 7))) for l in uniq}
    claims_len = np.array([clen[l] for l in L])
    ts = pd.read_csv(os.path.join(a.out, "token_sizes.csv"))
    base = ts[(ts.url_path_len == 60) & (ts.with_ip == 0)]
    rows = []
    for _, r in base.iterrows():
        auth = r.token_bytes - r.claims_bytes
        tok = claims_len + auth
        url = len(HOST) + L + len("?Token=") + tok
        ncook = int(r.n_cookies)
        if ncook == 1:
            cookie_max = len("Edge-Token=") + tok
            cookie_tot = cookie_max
        else:  # split across ncook cookies named Edge-Token<j>
            per = -(-tok // ncook)
            cookie_max = len("Edge-Token0=") + per
            cookie_tot = ncook * len("Edge-Token0=") + tok + 2 * (ncook - 1)  # "; " separators
        hdr = OTHER_HDR + len("Cookie: ") + cookie_tot
        vals = {"url2k": url, "url8k": url, "cookie4k": cookie_max, "hdr8k": hdr}
        for lim, cap in LIMITS.items():
            v = vals[lim]
            rows.append(dict(scheme=r.scheme, root_signer=r.root_signer if isinstance(r.root_signer, str) else "",
                             n=int(r.n) if not pd.isna(r.n) else "", log2N=int(r.log2N) if not pd.isna(r.log2N) else "",
                             limit=lim, fraction_fit=float(np.mean(v <= cap)), median_bytes=float(np.median(v)),
                             p99_bytes=float(np.percentile(v, 99))))
    pd.DataFrame(rows).to_csv(os.path.join(a.out, "fit.csv"), index=False, float_format="%.4f")
    print("wrote fit.csv with", len(rows), "rows")


if __name__ == "__main__":
    main()
