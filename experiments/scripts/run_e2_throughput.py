#!/usr/bin/env python3
"""E2: completed-handshake rate under a closed-loop load.

Placements (link emulator always on CPU 3):
  separate   server on CPU 0; client on CPUs 1-2 (disjoint cores and
             separate network namespaces: the "separate machines" setting)
  colocated  server and client share CPUs 0-1 (the original paper's setting)

Output: results/e2/summary.csv and per-run latency/job files.
"""
import csv, os, subprocess, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIN = os.path.join(ROOT, "bin")
CERTS = os.environ.get("CERTS", "/opt/dapv_certs")
OUT = os.path.join(ROOT, "results", "e2")
GROUP = "X25519MLKEM768"
PLACEMENTS = {"separate": ("0", "1,2"), "colocated": ("0,1", "0,1")}
CONFIGS = [("p256", "none"), ("p256_mldsa44", "none"),
           ("p256_mldsa44", "thread"), ("p256_mldsa44", "pool:2")]
CONNS = [int(x) for x in os.environ.get("CONNS", "100,500").split(",")]
RTTS = [int(x) for x in os.environ.get("RTTS", "0,50").split(",")]
REPS = int(os.environ.get("REPS", 3))
WARM, MEAS = float(os.environ.get("WARM", 3)), float(os.environ.get("MEAS", 10))
TCK = os.sysconf("SC_CLK_TCK")


def cpu_seconds(pid):
    with open(f"/proc/{pid}/stat") as f:
        v = f.read().rsplit(")", 1)[1].split()
    return (int(v[11]) + int(v[12])) / TCK


def main():
    os.makedirs(OUT, exist_ok=True)
    summ = open(os.path.join(OUT, "summary.csv"), "w", newline="")
    w = csv.writer(summ)
    w.writerow(["placement", "rtt_ms", "conns", "alg", "worker", "rep", "rate",
                "mean_hs_ms", "errors", "client_cpu_cores", "server_cpu_cores",
                "pq_jobs", "pq_failures"])
    port = 6000
    for pl, (scpu, ccpu) in PLACEMENTS.items():
        for rtt in RTTS:
            subprocess.run([os.path.join(ROOT, "scripts", "net.sh"), "rtt", str(rtt)], check=True)
            for conns in CONNS:
                for rep in range(REPS):
                    for alg, wm in CONFIGS:
                        port += 1
                        d = os.path.join(CERTS, alg)
                        srv = subprocess.Popen(
                            ["ip", "netns", "exec", "srv", "taskset", "-c", scpu,
                             os.path.join(BIN, "tlsserver"), str(port), "512",
                             os.path.join(d, "chain.pem"), os.path.join(d, "leaf.key"), GROUP],
                            stderr=subprocess.DEVNULL)
                        time.sleep(0.8)
                        name = f"{pl}__rtt{rtt}__c{conns}__{alg}__{wm.replace(':', '')}__r{rep}"
                        # Two client processes (each conns/2 connections) so that the
                        # single-threaded event loop of one client is not the bottleneck.
                        clis = [subprocess.Popen(
                            ["ip", "netns", "exec", "cli", "taskset", "-c", ccpu,
                             os.path.join(BIN, "tlsclient"), "10.77.0.1", str(port),
                             os.path.join(d, "root.pem"), GROUP, wm,
                             os.path.join(OUT, f"{name}_p{k}"), "load", str(conns // 2),
                             str(WARM), str(MEAS)],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            for k in range(2)]
                        time.sleep(WARM)
                        s0 = cpu_seconds(srv.pid)
                        time.sleep(MEAS)
                        s1 = cpu_seconds(srv.pid)
                        kvs = [dict(x.split("=") for x in c.communicate()[0].split()) for c in clis]
                        hs_n = sum(int(k["handshakes"]) for k in kvs)
                        kv = {"rate": f"{sum(float(k['rate']) for k in kvs):.1f}",
                              "mean_hs_ms": f"{sum(float(k['mean_hs_ms']) * int(k['handshakes']) for k in kvs) / max(hs_n, 1):.3f}",
                              "errors": str(sum(int(k["errors"]) for k in kvs)),
                              "client_cpu_cores": f"{sum(float(k['client_cpu_cores']) for k in kvs):.3f}",
                              "pq_jobs": str(sum(int(k["pq_jobs"]) for k in kvs)),
                              "pq_failures": str(sum(int(k["pq_failures"]) for k in kvs))}
                        srv.kill(); srv.wait()
                        w.writerow([pl, rtt, conns, alg, wm, rep, kv["rate"], kv["mean_hs_ms"],
                                    kv["errors"], kv["client_cpu_cores"],
                                    f"{(s1 - s0) / MEAS:.3f}", kv["pq_jobs"], kv["pq_failures"]])
                        summ.flush()
                        print(name, kv["rate"], kv["errors"], flush=True)
    subprocess.run([os.path.join(ROOT, "scripts", "net.sh"), "rtt", "0"])


if __name__ == "__main__":
    main()
