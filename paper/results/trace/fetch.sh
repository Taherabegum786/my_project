#!/bin/bash
# usage: fetch.sh <name> <s3 file> <byte range or 'full'>
set -o pipefail
n=$1; f=$2; r=$3
RANGE=""; [ "$r" != full ] && RANGE="-r $r"
cd /
curl -sS --retry 5 $RANGE https://cachelib-workload-sharing.s3.amazonaws.com/pub/cdn/$f | tee >(sha256sum > /tmp/claude-0/-home-user-my-project/4a27d5c9-46a1-5d35-98ec-9a4e85dfb968/scratchpad/trace_npz/$n.sha256) | nice -n 10 /tmp/claude-0/-home-user-my-project/4a27d5c9-46a1-5d35-98ec-9a4e85dfb968/scratchpad/venv/bin/python -I /tmp/claude-0/-home-user-my-project/4a27d5c9-46a1-5d35-98ec-9a4e85dfb968/scratchpad/trace_tools/prep.py /tmp/claude-0/-home-user-my-project/4a27d5c9-46a1-5d35-98ec-9a4e85dfb968/scratchpad/trace_npz/$n > /tmp/claude-0/-home-user-my-project/4a27d5c9-46a1-5d35-98ec-9a4e85dfb968/scratchpad/trace_npz/$n.log 2>&1
echo "EXIT $?" >> /tmp/claude-0/-home-user-my-project/4a27d5c9-46a1-5d35-98ec-9a4e85dfb968/scratchpad/trace_npz/$n.log
