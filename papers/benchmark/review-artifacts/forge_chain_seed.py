# FROZEN review artifact: runs against the pass-3 code (commit 694ba76 / c95c6e3) only. It is superseded by experiments/negative_tests.py
# (R8: the same forgery against the new secret-keyed chain is rejected; control C8: it still succeeds against the legacy derivation).
import sys, struct, hashlib
sys.path.insert(0, "/home/user/my_project/papers/benchmark/experiments"); sys.path.insert(0, "/home/user/my_project/lib")
import run_proto as RP
from pqsig.proto import modes as MO
from pqsig.proto.oqs import PQ, Counters
pq="Falcon-512"; pl=RP.plan_for("sib1",pq,10,N=32,E=8)
key=PQ(pq).keypair()
S=MO.build(pq,"chain",pl,0,key=key)
A=S.alloc; M=pl.M; D=14; e,i=D//8, D%8+1; w=pl.off+D
# attacker recomputes the chain from the public build seed only
K=[None]*9; K[8]=MO.H(b"seed",struct.pack(">II",0,e))[:16]
for j in range(8,0,-1): K[j-1]=MO.Fchain(K[j])
app_f=bytearray(S.truth[D]); app_f[20]^=1; app_f=bytes(app_f)
tag_f=MO.mac_tag(K[i],e,i,app_f,b"")
lay=S.layout; fr=list(S.frames)
for g in range(w*M,(w+1)*M):
    if fr[g] and fr[g][1]:
        au=fr[g][1]; fr[g]=(app_f, au[:lay["tag"][0]]+tag_f+au[lay["tag"][1]:])   # in-time forged frames
rx=MO.make_rx(A,S.pk,0,Counters())
for g,f in enumerate(fr):
    if f: rx.deliver(g,*f)
print("forged message accepted:", rx.app.get(D)==app_f, " honest copy:", rx.app.get(D)==S.truth[D])
