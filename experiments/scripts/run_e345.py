#!/usr/bin/env python3
"""E3-E5: network and platform sensitivity (sequential handshakes).

E3  initial congestion window: server initcwnd (and client initrwnd) of 10, 20
    and 40 segments at RTT 50 and 150 ms; synchronous verification.
E4  packet loss: 0, 1 and 3 % independent frame loss per direction at
    RTT 50 ms; synchronous verification.
E6  verification-cost scaling (see e6()).
E5  client without vector instructions: the client (and the provider it
    loads) uses a portable C build of liboqs (no AVX2); the server keeps the
    AVX2 build.  Synchronous vs DAPV pool at RTT 0 and 50 ms.

Same placement as E1 (server CPU 0, client CPUs 1-2, emulator CPU 3), same
three-certificate chains and X25519MLKEM768.  Output:
results/<exp>/<condition>/<alg>__chain3__X25519MLKEM768__<worker>__r<k>_{hs,jobs}.csv
"""
import os, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIN = os.path.join(ROOT, "bin")
NET = os.path.join(ROOT, "scripts", "net.sh")
CERTS = os.environ.get("CERTS", "/opt/dapv_certs")
GROUP = "X25519MLKEM768"
GENERIC_LIB = "/opt/ossl/lib:/opt/liboqs-generic/lib"


def net(*a):
    subprocess.run([NET, *map(str, a)], check=True)


def servers(algs, base):
    procs, ports = [], {}
    for i, alg in enumerate(algs):
        d = os.path.join(CERTS, alg)
        ports[alg] = base + i
        procs.append(subprocess.Popen(
            ["ip", "netns", "exec", "srv", "taskset", "-c", "0",
             os.path.join(BIN, "tlsserver"), str(base + i), "4",
             os.path.join(d, "chain.pem"), os.path.join(d, "leaf.key"), GROUP],
            stderr=subprocess.DEVNULL))
    time.sleep(1.0)
    return procs, ports


def run(outdir, runs, ports, n, rounds, env=None):
    os.makedirs(outdir, exist_ok=True)
    per = max(1, n // rounds)
    for r in range(rounds):
        for alg, wm in runs:
            name = f"{alg}__chain3__{GROUP}__{wm.replace(':', '')}__r{r}"
            cmd = ["ip", "netns", "exec", "cli"]
            if env:
                cmd += ["env", *[f"{k}={v}" for k, v in env.items()]]
            cmd += ["taskset", "-c", "1,2", os.path.join(BIN, "tlsclient"), "10.77.0.1",
                    str(ports[alg]), os.path.join(CERTS, alg, "root.pem"), GROUP, wm,
                    os.path.join(outdir, name), "seq", str(per)]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode != 0:
                print("FAILED", outdir, name, res.stderr[-300:], flush=True)


def e3():
    algs = ["p256", "p256_mldsa44", "p384_mldsa65", "p256_sphincssha2128fsimple"]
    procs, ports = servers(algs, 7100)
    try:
        for rtt in (50, 150):
            net("rtt", rtt)
            for cw in (10, 20, 40):
                net("initcwnd", cw)
                time.sleep(0.3)
                t = time.time()
                run(os.path.join(ROOT, "results", "e3", f"cw{cw}_rtt{rtt}"),
                    [(a, "none") for a in algs], ports, 100, 5)
                print(f"e3 cw={cw} rtt={rtt} {time.time() - t:.0f}s", flush=True)
    finally:
        net("initcwnd", 10); net("rtt", 0)
        for p in procs: p.kill()


def e4():
    algs = ["p256", "p256_falcon512", "p256_mldsa44", "p384_mldsa65"]
    procs, ports = servers(algs, 7200)
    try:
        net("rtt", 50)
        for loss in (0, 1, 3):
            net("loss", loss)
            time.sleep(0.3)
            t = time.time()
            run(os.path.join(ROOT, "results", "e4", f"loss{loss}_rtt50"),
                [(a, "none") for a in algs], ports, 400, 8)
            print(f"e4 loss={loss} {time.time() - t:.0f}s", flush=True)
    finally:
        net("loss", 0); net("rtt", 0)
        for p in procs: p.kill()


def e5():
    algs = ["p256_falcon512", "p256_mldsa44", "p384_mldsa65", "p256_sphincssha2128fsimple"]
    procs, ports = servers(algs, 7300)
    try:
        for rtt, n in ((0, 1000), (50, 200)):
            net("rtt", rtt)
            time.sleep(0.3)
            t = time.time()
            run(os.path.join(ROOT, "results", "e5", f"generic_rtt{rtt}"),
                [(a, w) for a in algs for w in ("none", "pool:2")], ports, n, 10,
                env={"LD_LIBRARY_PATH": GENERIC_LIB})
            print(f"e5 rtt={rtt} {time.time() - t:.0f}s", flush=True)
    finally:
        net("rtt", 0)
        for p in procs: p.kill()


def e6():
    """Verification-cost scaling: each PQ verification is performed k times
    (synchronous and deferred paths alike) to emulate a k-times slower
    verifier; P-256+ML-DSA-44."""
    procs, ports = servers(["p256_mldsa44"], 7500)
    try:
        for rtt, n in ((0, 300), (50, 100)):
            net("rtt", rtt)
            time.sleep(0.3)
            for k in (1, 2, 4, 8, 16, 32, 64):
                t = time.time()
                run(os.path.join(ROOT, "results", "e6", f"k{k}_rtt{rtt}"),
                    [("p256_mldsa44", w) for w in ("none", "pool:2")], ports, n, 5,
                    env={"DAPV_VERIFY_REPEAT": k})
                print(f"e6 k={k} rtt={rtt} {time.time() - t:.0f}s", flush=True)
    finally:
        net("rtt", 0)
        for p in procs: p.kill()


if __name__ == "__main__":
    for e in (sys.argv[1:] or ["e3", "e4", "e5", "e6"]):
        globals()[e]()
