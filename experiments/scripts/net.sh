#!/bin/bash
# Two network namespaces joined by the userspace link emulator (tapbridge):
#   ns "srv" 10.77.0.1/24 (tap device taps)  <-- tapbridge -->  ns "cli" 10.77.0.2/24 (tapc)
# MTU 1500 and no segmentation offload, so TCP segments are real 1500-byte frames.
#   net.sh up <bridge_cpu> [rate_mbit]
#   net.sh rtt <ms>        set RTT (one-way delay = ms/2 each direction)
#   net.sh down
set -euo pipefail
BIN=$(cd "$(dirname "$0")/../bin" && pwd)
case ${1:-} in
up)
  CPU=${2:-3}; RATE=${3:-1000}
  echo 0 > /run/tapbridge.delay_us
  rm -f /run/tapbridge.ready
  taskset -c "$CPU" "$BIN/tapbridge" taps tapc 0 "$RATE" /run/tapbridge.ready &
  echo $! > /run/tapbridge.pid
  for i in $(seq 50); do [ -e /run/tapbridge.ready ] && break; sleep 0.1; done
  for ns in srv cli; do ip netns add $ns; done
  ip link set taps netns srv; ip link set tapc netns cli
  ip -n srv addr add 10.77.0.1/24 dev taps; ip -n cli addr add 10.77.0.2/24 dev tapc
  for ns in srv cli; do
    dev=$([ $ns = srv ] && echo taps || echo tapc)
    ip -n $ns link set $dev mtu 1500 up; ip -n $ns link set lo up
    ip netns exec $ns ethtool -K $dev tso off gso off gro off tx off rx off 2>/dev/null || true
    ip netns exec $ns sysctl -qw net.ipv4.ip_local_port_range="10000 65000"
    ip netns exec $ns sysctl -qw net.ipv4.tcp_tw_reuse=1
    ip netns exec $ns sysctl -qw net.core.somaxconn=4096
    ip netns exec $ns sysctl -qw net.ipv4.tcp_max_syn_backlog=8192
  done
  ip netns exec cli ping -c 2 -q 10.77.0.1 >/dev/null && echo "link up"
  ;;
rtt)
  echo $(( ${2} * 1000 / 2 )) > /run/tapbridge.delay_us
  kill -HUP "$(cat /run/tapbridge.pid)"
  ;;
down)
  kill "$(cat /run/tapbridge.pid)" 2>/dev/null || true
  ip netns del srv 2>/dev/null || true; ip netns del cli 2>/dev/null || true
  ;;
*) echo "usage: $0 up|rtt|down"; exit 2 ;;
esac
