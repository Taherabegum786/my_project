"""Row tagging shared by all CSV writers: machine, date, git commit."""
import datetime
import os
import socket
import subprocess


def _git(root, *args):
    return subprocess.check_output(["git", "-C", root, *args], text=True, stderr=subprocess.DEVNULL).strip()


def code_state():
    """(full commit id, dirty flag). Dirty = tracked or untracked changes under lib/ or papers/*/experiments/ (build/, results/ and __pycache__ excluded)."""
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    try:
        commit = _git(root, "rev-parse", "HEAD")
        dirty = bool(_git(root, "status", "--porcelain", "--", "lib", "papers/benchmark/experiments",
                          ":(exclude)papers/benchmark/experiments/build", ":(exclude,glob)**/__pycache__/**"))
    except Exception:
        commit, dirty = "unknown", True
    return commit, dirty


def tag():
    commit, dirty = code_state()
    return {"machine": os.environ.get("MACHINE_NAME") or socket.gethostname(),
            "date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "git_commit": commit, "git_dirty": int(dirty)}


def stats(samples_us):
    import numpy as np
    a = np.asarray(samples_us, dtype=float)
    return {"mean": a.mean(), "median": float(np.median(a)),
            "p95": float(np.percentile(a, 95)), "p99": float(np.percentile(a, 99)),
            "std": a.std(ddof=1) if len(a) > 1 else 0.0}
