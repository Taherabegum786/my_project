"""Real-UDP mode: sender and receiver as separate processes (same machine or two machines on a LAN).

Datagram = '>IH' (slot number, app length) | app | auth;   END datagram = slot 0xFFFFFFFF | '>I' number of frame datagrams sent.
Loss is injected AT THE RECEIVER from the seeded mask (lossform.make_mask(G, seed, p, burst)) indexed by slot number, so a UDP run
with the same --seed/--loss/--build-seed gives the same authentication outcome as the in-process run; genuine network loss shows up as
`udp_missing` (frames the sender sent but the receiver never got), and the run is then not comparable with the in-process one.
The receiver needs the sender's public key (provisioned out of band in the real systems): the sender writes --keyfile
(PQ pk and Ed25519 pk); copy it to the receiver machine before starting the receiver.
Example (two machines):  receiver: run_proto.py udp --role receiver --udp 0.0.0.0:9000 --keyfile k.bin ...
                         sender:   run_proto.py udp --role sender   --udp RECEIVER_IP:9000 --keyfile k.bin ...  (same --profile/--pq/--mode/--M/--seed)
Datagrams up to 2.5 kB (C-V2X J3161 ceiling) are fragmented by IP on a 1500 B-MTU LAN; that is transport detail, not part of the model.
"""
import socket
import struct
import time

import numpy as np

END = 0xFFFFFFFF


def add_args(u):
    u.add_argument("--role", required=True, choices=["sender", "receiver"])
    u.add_argument("--udp", required=True, help="HOST:PORT (sender: destination, receiver: bind address)")
    u.add_argument("--profile", required=True); u.add_argument("--pq", required=True); u.add_argument("--mode", required=True)
    u.add_argument("--M", type=int, default=10)
    u.add_argument("--loss", default="iid:0.0", help="iid:P or ge:P:BURST (applied at the receiver)")
    u.add_argument("--seed", type=int, default=0); u.add_argument("--build-seed", type=int, default=0)
    u.add_argument("--speed", type=float, default=1.0, help="time compression: slot period / speed (1 = real time)")
    u.add_argument("--keyfile", required=True); u.add_argument("--out", help="receiver: append the result row to this CSV")
    u.add_argument("--machine"); u.add_argument("--check", action="store_true", help="receiver: compare with the in-process run")
    u.add_argument("--start-delay", type=float, default=3.0, help="sender: seconds between writing the keyfile and sending (raise it on a LAN to leave time to copy the keyfile)"); u.add_argument("--timeout", type=float, default=30.0)


def parse_loss(s):
    parts = s.split(":")
    return (parts[0], float(parts[1]), int(parts[2]) if len(parts) > 2 else 0)


def run_udp(a):
    import os
    import run_proto as RP
    from pqsig import lossform as LF
    from pqsig.proto import modes as MO
    from pqsig.proto.oqs import PQ, Counters, Ed
    if a.machine:
        os.environ["MACHINE_NAME"] = a.machine
    host, port = a.udp.rsplit(":", 1); port = int(port)
    plan = RP.plan_for(a.profile, a.pq, a.M)
    if a.role == "sender":
        pq = PQ(a.pq); pk, sk = pq.keypair(); ed = Ed()
        with open(a.keyfile + ".tmp", "wb") as f:
            f.write(struct.pack(">II", len(pk), len(ed.pk)) + pk + ed.pk)
        os.replace(a.keyfile + ".tmp", a.keyfile)
        print(f"sender: keys written to {a.keyfile}; copy it to the receiver, which waits for it; sending starts in {a.start_delay}s", flush=True)
        S = MO.build(a.pq, a.mode, plan, build_seed=a.build_seed, key=(pk, sk), ed=ed)
        if not S.alloc.feasible:
            print("infeasible allocation: nothing to send"); return
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        time.sleep(a.start_delay)
        t0 = time.perf_counter(); sent = 0; dt = plan.T / a.speed
        for g, f in enumerate(S.frames):
            if f is None:
                continue
            while time.perf_counter() - t0 < g * dt:
                pass
            sock.sendto(struct.pack(">IH", g, len(f[0])) + f[0] + f[1], (host, port)); sent += 1
        for _ in range(5):
            sock.sendto(struct.pack(">II", END, sent), (host, port)); time.sleep(0.01)
        print(f"sender: {sent} frames, {time.perf_counter() - t0:.1f}s wall, {S.air_bytes} auth bytes on air")
        return
    # receiver
    t_wait = time.time()
    while not os.path.exists(a.keyfile):
        if time.time() - t_wait > a.timeout:
            raise SystemExit("receiver: keyfile never appeared")
        time.sleep(0.1)
    with open(a.keyfile, "rb") as f:
        n1, n2 = struct.unpack(">II", f.read(8)); pk = f.read(n1); edpk = f.read(n2)
    model, p, burst = parse_loss(a.loss)
    mask = LF.make_mask(plan.G, a.seed, p, burst or None)
    A = MO.Alloc(a.pq, a.mode, plan, PQ(a.pq).sig_len)
    rng = np.random.default_rng(np.random.SeedSequence([a.seed, 77]))
    join = plan.off * plan.M + int(rng.integers(0, plan.E * plan.M))
    rctr = Counters(); rx = MO.make_rx(A, pk, 0, rctr, edpk); rj = MO.make_rx(A, pk, join, Counters(), edpk)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 16 << 20)
    sock.bind((host, port)); sock.settimeout(a.timeout)   # bound after the keyfile exists: the sender starts --start-delay s after writing it
    got = 0; sent = None; cpu = 0; jdone = False; first = None
    print(f"receiver listening on {host}:{port}", flush=True)
    while True:
        try:
            d = sock.recv(70000)
        except socket.timeout:
            print("receiver: timeout"); break
        g, la = struct.unpack(">IH", d[:6])
        if g == END:
            sent = struct.unpack(">I", d[4:8])[0]; break
        got += 1
        if mask[g]:
            continue
        app = d[6:6 + la]; auth = d[6 + la:]
        t0 = time.thread_time_ns(); rx.deliver(g, app, auth); cpu += time.thread_time_ns() - t0
        if not jdone and g >= join:
            rj.deliver(g, app, auth)
            if rj.auth:
                jdone = True; first = min(rj.auth.values())
    dl = RP.delays_ms(rx, plan); na = len(rx.auth)
    row = dict(RP.tag(), profile=a.profile, pq=a.pq, mode=a.mode, M=a.M, loss_model=model, loss_p=p, burst_len=burst, seed=a.seed,
               build_id=a.build_seed, transport="udp", authenticated=na, share=na / plan.N, rejected=rx.rejected,
               delay_median_ms=float(np.median(dl)) if dl else "", delay_p95_ms=float(np.percentile(dl, 95)) if dl else "",
               ttfa_ms=((first + 1 - join) * plan.T * 1000.0 if first is not None else ""), ttfa_censored=int(first is None),
               rx_cpu_us_per_msg=cpu / 1e3 / plan.N, udp_frames_received=got, udp_frames_sent=sent if sent is not None else "",
               udp_missing=(sent - got) if sent is not None else "")
    print({k: row[k] for k in ("authenticated", "share", "rejected", "delay_median_ms", "ttfa_ms", "udp_frames_received", "udp_missing")})
    if a.check:
        import statistics
        # reference run: own keys (signature bytes differ, authentication outcome must not)
        ref_ed = Ed()
        S = MO.build(a.pq, a.mode, plan, build_seed=a.build_seed, ed=ref_ed)
        r2 = MO.make_rx(S.alloc, S.pk, 0, Counters(), ref_ed.pk); rj2 = MO.make_rx(S.alloc, S.pk, join, Counters(), ref_ed.pk)
        RP.one_run(S, r2, rj2, mask, join)
        same = (set(r2.auth) == set(rx.auth)) and {k: v for k, v in r2.auth.items()} == {k: v for k, v in rx.auth.items()}
        row["inproc_same_outcome"] = int(same); row["inproc_authenticated"] = len(r2.auth)
        print("check vs in-process:", "IDENTICAL (same messages, same slots)" if same else "DIFFERENT", f"(udp_missing={row['udp_missing']})")
    if a.out:
        new = not os.path.exists(a.out)
        import csv
        with open(a.out, "a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(row)); 
            if new:
                w.writeheader()
            w.writerow(row)
