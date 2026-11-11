# Environment

Pinned (see run.sh): liboqs tag `0.12.0` (LIBOQS_TAG variable; verify the tag exists and enables the desired algorithms, edit if not),
Ubuntu 22.04/24.04, gcc, cmake, ninja, OpenSSL dev headers, Python 3.10+.
Python packages: numpy, pandas, pyyaml, matplotlib, tabulate, cryptography (installed in a venv by run.sh).

Cloud smoke environment (this session): Linux 6.18, Python 3.13.18, gcc, cmake, ninja, numpy 2.5.3, pandas 3.0.5,
PyYAML 6.0.3, cryptography 50.0.1, matplotlib 3.11.2, 4 cores / 15 GB. liboqs NOT built: github.com returned HTTP 403.
The C benchmark (`lib/pqsig/oqs_bench.c`) was only syntax-checked against a stub header, never run against real liboqs.
MAYO/UOV/SNOVA/CROSS availability depends on the liboqs tag; run.sh passes the enable flags and the benchmark skips any not compiled in.
