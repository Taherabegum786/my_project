#!/usr/bin/env python3
"""Part C. run_loss.py SIZES_DECLARED.csv PROFILES.yaml OUTDIR [SEEDS] [NMSG]
Writes loss_params.csv, loss_closed.csv (closed forms), loss_simcheck.csv (iid simulation vs closed form), loss_ge.csv (Gilbert-Elliott)."""
import itertools, os, sys
import numpy as np, pandas as pd, yaml
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
from pqsig import lossform as L
from pqsig.common import tag

sizes, prof, outdir = sys.argv[1:4]
seeds = int(sys.argv[4]) if len(sys.argv) > 4 else 20
nmsg = int(sys.argv[5]) if len(sys.argv) > 5 else 4000
Y = yaml.safe_load(open(prof)); sib = Y["profiles"]["sib1"]; ch = Y["common"]["chain"]
C = sib["auth_budget"]["bytes"]; SLOT_S = sib["message_period_s"]
d = pd.read_csv(sizes).set_index("scheme")
SIGS = ["MAYO-2", "MAYO-1", "Falcon-padded-512", "Falcon-512", "ML-DSA-44"]
MS = (3, 6, 12, 24, 48); PS = (0, .05, .10, .15, .20, .25, .30)
E, RA, W, N8 = 20, 2, 2, 8
T = tag()

params = [
    ("slot capacity C (auth bytes/slot)", C, "darzi2026a via profiles.yaml sib1.auth_budget (293 B)"),
    ("slot period", SLOT_S, "darzi2026a (SIB1 every 160 ms), stated"),
    ("fragment header", 0, "TODO-RESULT in evidence; 0 used (lower bound on fragment count)"),
    ("slots per message window M", "3,6,12,24,48", "assumed grid (equal for every scheme)"),
    ("signature bytes S", "declared liboqs length_signature", "sizes_declared.csv"),
    ("anchor = S + commit + ts", f"S+{ch['commit']}+{ch['ts']}", "commit 16 B and ts 4 B assumed"),
    ("tag / disclosed key", f"{ch['tag']} / {ch['key']}", "tag 16 B darzi2026a; key 16 B assumed (does not enter the slot count: one slot carries it)"),
    ("epoch length E (messages)", E, "assumed"), ("minimum anchor repetitions", RA, "assumed; actual r_a = floor(E*a_s/k_a) uses all reserved slots"),
    ("key windows w (d=1 message delay)", W, "assumed"), ("Merkle batch n", "4,8,16 (8 main)", "assumed"),
    ("merkle signature redundancy", "2 repetitions' worth of slots", "assumed"),
    ("loss", "i.i.d. p in 0..0.30; Gilbert-Elliott loss_G=0, loss_B=1, mean burst 2/5/10 slots, stationary loss p", "task spec; burst lengths assumed"),
    ("seeds / messages", f"{seeds} / {nmsg}", "simulation only (cross-check and GE)"),
]
pd.DataFrame([{**T, "parameter": a, "value": b, "source": c} for a, b, c in params]).to_csv(os.path.join(outdir, "loss_params.csv"), index=False)

rows = []
for sig, M, n in itertools.product(SIGS, MS, (4, 8, 16)):
    S = int(d.loc[sig, "sig_declared"]); a = L.params(S, C, M, ch["commit"], ch["ts"], E, RA, W, n)
    for p in PS:
        for s in L.SCHEMES:
            if s.startswith("merkle") is False and n != 8: continue
            rows.append({**T, "sig": sig, "S": S, "k": a["k"], "ka": a["ka"], "M": M, "n": n if s.startswith("merkle") else "", "loss": p, "scheme": s,
                         "P_verified": L.P_closed(s, p, a), "tta95_slots": L.tta95(s, p, a) if p > 0 or True else 0})
pd.DataFrame(rows).to_csv(os.path.join(outdir, "loss_closed.csv"), index=False)

chk = []
for sig, M, p, s in itertools.product(SIGS[:3] + ["ML-DSA-44"], (6, 12, 24), (.05, .10, .20, .30), L.SCHEMES):
    S = int(d.loc[sig, "sig_declared"]); a = L.params(S, C, M, ch["commit"], ch["ts"], E, RA, W, N8)
    v = np.array([L.sim(s, p, a, nmsg, np.random.default_rng(1000 * sd + int(p * 100) + M)) for sd in range(seeds)])
    cf = L.P_closed(s, p, a)
    chk.append({**T, "sig": sig, "M": M, "loss": p, "scheme": s, "closed": cf, "sim_mean": v.mean(), "sim_sd": v.std(ddof=1),
                "abs_diff": abs(v.mean() - cf), "se": v.std(ddof=1) / np.sqrt(seeds), "seeds": seeds, "n_msgs": nmsg})
pd.DataFrame(chk).to_csv(os.path.join(outdir, "loss_simcheck.csv"), index=False)

ge = []
for sig, M, p, bl, s in itertools.product(["MAYO-2", "Falcon-padded-512", "ML-DSA-44"], (12, 24), (.05, .10, .20, .30), (2, 5, 10), L.SCHEMES):
    S = int(d.loc[sig, "sig_declared"]); a = L.params(S, C, M, ch["commit"], ch["ts"], E, RA, W, N8)
    v = np.array([L.sim(s, p, a, nmsg, np.random.default_rng(7000 * sd + int(p * 100) + M + bl), burst_len=bl) for sd in range(seeds)])
    ge.append({**T, "sig": sig, "M": M, "loss": p, "burst_len": bl, "scheme": s, "iid_closed": L.P_closed(s, p, a),
               "ge_mean": v.mean(), "ge_sd": v.std(ddof=1), "seeds": seeds, "n_msgs": nmsg})
pd.DataFrame(ge).to_csv(os.path.join(outdir, "loss_ge.csv"), index=False)
print(len(rows), len(chk), len(ge))
