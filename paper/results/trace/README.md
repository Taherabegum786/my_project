# Trace provenance (R2)

**Dataset.** Meta CacheLib public workload traces, `cdn/202303`, from the S3 bucket `cachelib-workload-sharing`
(read without credentials).
- Content: 3 Meta CDN edge clusters (eag, nha, prn), 7 days each, 15–22 Mar 2023.
- Licence: per the CacheLib documentation, "licensed under the same license as CacheLib", which is Apache-2.0.
- Source of that statement: `website/docs/Cache_Library_User_Guides/Cachebench_FB_HW_eval.md` in github.com/facebook/CacheLib (main branch, read 2026-11-06).
- Cite: that documentation page and Berg et al., "The CacheLib Caching Engine: Design and Experiences at Scale", USENIX OSDI 2020.

**Files used.** Byte ranges were taken from the start of each file, which is time-ordered. A truncated last row is dropped by `prep.py`.

| object (`https://cachelib-workload-sharing.s3.amazonaws.com/pub/cdn/…`) | S3 ETag / size | byte range used | SHA-256 of the bytes received | rows kept |
|---|---|---|---|---|
| `reag0c01_20230315_20230322_0.2000.csv` | `c84bc4074bd7fbf25a95b6dcc013f7bb-457` / 7,659,801,374 | 0–3,299,999,999 | `02d5a1c4c551c3b2aca25f1328ce4ec584eb4ecf04fe4659e8e77828465da5c4` | 21,519,687 |
| `rnha0c01_20230315_20230322_0.8000.csv` | `252b46cbde0228ba3396f30958265c40-1004` / 16,842,373,731 | 0–7,199,999,999 | `f0f4336f8b626562fb170116515a68a0dd456a3dc98ee34683120624c0244395` | 44,085,387 |
| `rprn0c01_20230315_20230322_0.2000.csv` | `6de5773a02e85f96f3e40a4c994e4f62-917` / 15,370,742,189 | 0–6,599,999,999 | `59c4641828881bc6058d7ae0a034ba27bc00c26d62cd1519e8a47eba0c499c49` | 41,159,261 |

- All three objects have Last-Modified 2023-04-03 23:04:20 GMT.
- `cdn_trace_reag0c01_20230315_20230322.json` here is the bucket's cachebench config for eag (3.6 KB, copied verbatim).

**Commands.** The raw trace (about 17 GB) is not committed. The files here are `fetch.sh` and `prep.py`, copied from the scratchpad.

```bash
# untrusted data: streamed straight into the parser (python -I), never executed
fetch.sh reag reag0c01_20230315_20230322_0.2000.csv 0-3299999999
fetch.sh rnha rnha0c01_20230315_20230322_0.8000.csv 0-7199999999
fetch.sh rprn rprn0c01_20230315_20230322_0.2000.csv 0-6599999999
#   = curl -r <range> <url> | tee >(sha256sum) | python -I prep.py <npzdir>   -> chunk*.npz (t_ms, key64 = pandas hash of cacheKey, ...)
cd paper/experiments
python -m sim.trace --npz <npzroot> --out ../results --clusters <c> --tag <c>          # per cluster, V = 3600 s
python -m sim.trace --npz <npzroot> --out ../results --clusters rnha --V 600   --tag rnha
python -m sim.trace --npz <npzroot> --out ../results --clusters rnha --V 86400 --tag rnha
# per-cluster outputs concatenated into results/trace_{oprg,rates,replicates}[_V*].csv
python -m plots.make_trace --in ../results
```

Use only the first 3 full 24-h windows of each cluster. These replicates cover 15–18 Mar 2023 for every cluster.
