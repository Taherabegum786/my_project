"""Stream a CacheLib CDN trace CSV from stdin into compact per-chunk .npz files (untrusted input: parse only).
Columns kept: t_ms int64, key64 uint64 (pandas hash of the anonymized cacheKey string), ctype int16, vip int16,
handler int16, resp int64, hdr int32, is_range int8, samp float32. A truncated final line (byte-range downloads) is dropped."""
import sys, os, numpy as np, pandas as pd
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
cols = ["timestamp", "cacheKey", "responseSize", "responseHeaderSize", "rangeStart", "SamplingRate", "RequestHandler",
        "cdn_content_type_id", "vip_type"]
it = pd.read_csv(sys.stdin, usecols=cols, dtype={"cacheKey": str, "cdn_content_type_id": str}, chunksize=2_000_000,
                 on_bad_lines="skip", engine="c")
n = bad = 0
for i, d in enumerate(it):
    d = d.dropna(subset=["timestamp", "cacheKey", "RequestHandler", "vip_type"])
    ok = pd.to_numeric(d.timestamp, errors="coerce").notna()
    bad += int((~ok).sum()); d = d[ok]
    ct = pd.to_numeric(d.cdn_content_type_id, errors="coerce").fillna(-1)
    np.savez(f"{out}/chunk{i:04d}.npz", t_ms=d.timestamp.astype(np.int64).values,
             key64=pd.util.hash_pandas_object(d.cacheKey, index=False).values,
             ctype=ct.astype(np.int16).values, vip=d.vip_type.astype(np.int16).values,
             handler=d.RequestHandler.astype(np.int16).values, resp=d.responseSize.astype(np.int64).values,
             hdr=d.responseHeaderSize.astype(np.int32).values, is_range=(d.rangeStart.values >= 0).astype(np.int8),
             samp=d.SamplingRate.astype(np.float32).values)
    n += len(d)
    print("chunk", i, "rows", n, "last_t", int(d.timestamp.iloc[-1]), flush=True)
print("DONE rows", n, "dropped", bad)
