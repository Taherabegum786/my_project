"""Row tagging shared by all CSV writers: machine, date, git commit."""
import datetime
import os
import socket
import subprocess


def tag():
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    try:
        commit = subprocess.check_output(["git", "-C", root, "rev-parse", "--short", "HEAD"],
                                         text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        commit = "unknown"
    return {"machine": os.environ.get("MACHINE_NAME") or socket.gethostname(),
            "date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "git_commit": commit}


def stats(samples_us):
    import numpy as np
    a = np.asarray(samples_us, dtype=float)
    return {"mean": a.mean(), "median": float(np.median(a)),
            "p95": float(np.percentile(a, 95)), "p99": float(np.percentile(a, 99)),
            "std": a.std(ddof=1) if len(a) > 1 else 0.0}
