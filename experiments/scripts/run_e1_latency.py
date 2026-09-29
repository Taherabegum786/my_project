#!/usr/bin/env python3
"""E1: sequential-handshake latency and provisional window (Delta t).

Server: namespace srv, CPU 0.  Client: namespace cli, CPUs 1-2.
Link emulator: CPU 3.  Configurations are interleaved in rounds so that slow
drift of the host affects all of them equally.

Output: results/e1/<rtt>/<config>__r<round>_{hs,jobs}.csv
"""
import itertools, os, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIN = os.path.join(ROOT, "bin")
CERTS = os.environ.get("CERTS", "/opt/dapv_certs")
OUT = os.path.join(ROOT, "results", "e1")
SRV_CPU, CLI_CPU = "0", "1,2"
MLKEM, X25519 = "X25519MLKEM768", "X25519"

# (alg, chain, group, worker models)
CONFIGS = [
    ("p256", "chain3", MLKEM, ["none"]),
    ("p256_mldsa44", "chain3", MLKEM, ["none", "thread", "pool:2"]),
    ("p256_mldsa44", "single", MLKEM, ["none", "pool:2"]),
    ("p256_mldsa44", "chain3", X25519, ["none", "pool:2"]),
    ("p256_falcon512", "chain3", MLKEM, ["none", "pool:2"]),
    ("p384_mldsa65", "chain3", MLKEM, ["none", "pool:2"]),
    ("p256_sphincssha2128fsimple", "chain3", MLKEM, ["none", "pool:2"]),
]
RTTS = [int(x) for x in os.environ.get("RTTS", "0,20,50,100,150").split(",")]
N_RTT0 = int(os.environ.get("N_RTT0", 1000))
N_RTT = int(os.environ.get("N_RTT", 200))
ROUNDS = int(os.environ.get("ROUNDS", 10))


def files(alg, chain):
    d = os.path.join(CERTS, alg)
    if chain == "single":
        return (os.path.join(d, "single.pem"), os.path.join(d, "single.key"),
                os.path.join(d, "single.pem"))
    return (os.path.join(d, "chain.pem"), os.path.join(d, "leaf.key"),
            os.path.join(d, "root.pem"))


def main():
    servers, port = {}, 5000
    procs = []
    for alg, chain, group, _ in CONFIGS:
        port += 1
        cert, key, _ca = files(alg, chain)
        servers[(alg, chain, group)] = port
        procs.append(subprocess.Popen(
            ["ip", "netns", "exec", "srv", "taskset", "-c", SRV_CPU,
             os.path.join(BIN, "tlsserver"), str(port), "4", cert, key, group],
            stderr=subprocess.DEVNULL))
    time.sleep(1.0)
    runs = [(alg, chain, group, wm) for alg, chain, group, wms in CONFIGS for wm in wms]
    try:
        for rtt in RTTS:
            subprocess.run([os.path.join(ROOT, "scripts", "net.sh"), "rtt", str(rtt)], check=True)
            time.sleep(0.5)
            n = N_RTT0 if rtt == 0 else N_RTT
            per_round = n // ROUNDS
            d = os.path.join(OUT, f"rtt{rtt}")
            os.makedirs(d, exist_ok=True)
            t0 = time.time()
            for r in range(ROUNDS):
                for alg, chain, group, wm in runs:
                    _, _, ca = files(alg, chain)
                    name = f"{alg}__{chain}__{group}__{wm.replace(':', '')}__r{r}"
                    cmd = ["ip", "netns", "exec", "cli", "taskset", "-c", CLI_CPU,
                           os.path.join(BIN, "tlsclient"), "10.77.0.1",
                           str(servers[(alg, chain, group)]), ca, group, wm,
                           os.path.join(d, name), "seq", str(per_round)]
                    res = subprocess.run(cmd, capture_output=True, text=True)
                    if res.returncode != 0:
                        print("FAILED", name, res.stderr[-500:], flush=True)
            print(f"rtt={rtt} done in {time.time() - t0:.0f}s", flush=True)
    finally:
        for p in procs:
            p.kill()
        subprocess.run([os.path.join(ROOT, "scripts", "net.sh"), "rtt", "0"])


if __name__ == "__main__":
    main()
