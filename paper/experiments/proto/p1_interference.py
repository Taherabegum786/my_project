"""P1 interference analysis: CPU of other processes (results/raw/proto/interference.log, 15-s samples of
processes >5% CPU) during each P1 run vs req/s and edge utilisation -> results/proto_p1_interference.csv.
usage: python p1_interference.py <results_dir>"""
import numpy as np, pandas as pd, os, datetime, sys
res=sys.argv[1]
samples=[]; cur=None
for line in open(f"{res}/raw/proto/interference.log"):
    if line.startswith("=="):
        if cur: samples.append(cur)
        h,m,s=map(int,line.split()[1].split(":")); cur=[h*3600+m*60+s,0.0]
    else:
        f=line.split()
        try: v=float(f[0])
        except Exception: continue
        if cur and f[2]!="claude": cur[1]+=v
if cur: samples.append(cur)
S=np.array(samples)
def ts(p):
    t=datetime.datetime.fromtimestamp(os.path.getmtime(p)); return t.hour*3600+t.minute*60+t.second
d=pd.read_csv(f"{res}/proto_capacity.csv")
rows=[]
for r in sorted(d.run.unique()):
    for s in d.scheme.unique():
        end=ts(f"{res}/raw/proto/p1_stats_{s}_{r}.json"); start=end-21
        sel=S[(S[:,0]>=start)&(S[:,0]<=end+15)]
        rows.append((s,r,sel[:,1].mean() if len(sel) else np.nan, len(sel)))
x=pd.DataFrame(rows,columns=["scheme","run","other_cpu_pct","n_samples"]).merge(d[["scheme","run","req_per_s","cpu_util_edge"]],on=["scheme","run"])
x.to_csv(f"{res}/proto_p1_interference.csv",index=False,float_format="%.3f")
print(x.groupby("run").other_cpu_pct.mean().round(0).to_string())
for s in sorted(d.scheme.unique()):
    y=x[x.scheme==s]; print(s, "corr(other_cpu,req/s)=%+.2f corr(other_cpu,edge_util)=%+.2f"%(np.corrcoef(y.other_cpu_pct,y.req_per_s)[0,1],np.corrcoef(y.other_cpu_pct,y.cpu_util_edge)[0,1]))
cheap=x[x.scheme.isin(["b1","b12","o1","o1a","o4"])]
print("pooled cheap schemes: corr(other_cpu, edge_util)=%.2f n=%d"%(np.corrcoef(cheap.other_cpu_pct,cheap.cpu_util_edge)[0,1],len(cheap)))
w=S[(S[:,0]>18*3600+56*60)&(S[:,0]<19*3600+25*60)]
print("P2/P3 window (18:56-19:25) mean other-process CPU %%: %.0f (n=%d samples)"%(w[:,1].mean(),len(w)))
