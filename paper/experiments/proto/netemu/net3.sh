#!/bin/bash
# Three network namespaces joined by two userspace link emulators (tapbridge), adapted from the
# author's earlier artifact (git show origin/claude/brave-meitner-l8yswp:experiments/scripts/net.sh).
#
#   ember_cli 10.71.0.2 (tAc) <-tapbridge A, 10 ms one-way-> (tAe) 10.71.0.1 ember_edge
#   ember_edge 10.72.0.1 (tBe) <-tapbridge B, 37.5 ms one-way-> (tBo) 10.72.0.2 ember_origin
#   ember_edge forwards between the two links (cli->origin traffic, i.e. token issuance, crosses both).
# MTU 1500, 1000 Mbit/s serialisation in each tapbridge; TAP devices are created without
# offloads (no TUNSETOFFLOAD), so every frame is <= 1514 B.
#
#   net3.sh up [bridge_cpu] [delayA_us] [delayB_us] [rate_mbit]
#   net3.sh down
#   net3.sh check        (ping + one-way-delay sanity)
#
# NOTE: all namespaces share one physical 4-vCPU host; traffic crosses the emulated links but
# not a physical NIC (limitation, stated in RESULTS_B.md).
set -euo pipefail
BIN=$(cd "$(dirname "$0")/../bin" && pwd)
RUN=/run/ember_net
case ${1:-} in
up)
  CPU=${2:-2}; DA=${3:-10000}; DB=${4:-37500}; RATE=${5:-1000}
  mkdir -p $RUN
  for L in A B; do echo 0 > $RUN/tb$L.loss_ppm; rm -f $RUN/tb$L.ready; done
  echo $DA > $RUN/tbA.delay_us; echo $DB > $RUN/tbB.delay_us
  taskset -c "$CPU" "$BIN/tapbridge" tAc tAe "$DA" "$RATE" $RUN/tbA.ready $RUN/tbA > $RUN/tbA.log 2>&1 &
  echo $! > $RUN/tbA.pid
  taskset -c "$CPU" "$BIN/tapbridge" tBe tBo "$DB" "$RATE" $RUN/tbB.ready $RUN/tbB > $RUN/tbB.log 2>&1 &
  echo $! > $RUN/tbB.pid
  for i in $(seq 50); do [ -e $RUN/tbA.ready ] && [ -e $RUN/tbB.ready ] && break; sleep 0.1; done
  for ns in ember_cli ember_edge ember_origin; do ip netns add $ns; ip -n $ns link set lo up; done
  ip link set tAc netns ember_cli; ip link set tAe netns ember_edge
  ip link set tBe netns ember_edge; ip link set tBo netns ember_origin
  ip -n ember_cli addr add 10.71.0.2/24 dev tAc
  ip -n ember_edge addr add 10.71.0.1/24 dev tAe
  ip -n ember_edge addr add 10.72.0.1/24 dev tBe
  ip -n ember_origin addr add 10.72.0.2/24 dev tBo
  for pair in ember_cli:tAc ember_edge:tAe ember_edge:tBe ember_origin:tBo; do
    ns=${pair%%:*}; dev=${pair##*:}
    ip -n $ns link set $dev mtu 1500 up
  done
  ip -n ember_cli route add default via 10.71.0.1
  ip -n ember_origin route add default via 10.72.0.1
  ip netns exec ember_edge sysctl -qw net.ipv4.ip_forward=1
  for ns in ember_cli ember_edge ember_origin; do
    ip netns exec $ns sysctl -qw net.ipv4.ip_local_port_range="10000 65000"
    ip netns exec $ns sysctl -qw net.ipv4.tcp_tw_reuse=1
    ip netns exec $ns sysctl -qw net.core.somaxconn=8192
    ip netns exec $ns sysctl -qw net.ipv4.tcp_max_syn_backlog=16384
  done
  ip netns exec ember_cli ping -c 2 -q 10.71.0.1 >/dev/null && ip netns exec ember_cli ping -c 2 -q 10.72.0.2 >/dev/null && echo "links up"
  ;;
check)
  ip netns exec ember_cli ping -c 10 -i 0.2 10.71.0.1 | tail -1
  ip netns exec ember_edge ping -c 10 -i 0.2 10.72.0.2 | tail -1
  ip netns exec ember_cli ping -c 10 -i 0.2 10.72.0.2 | tail -1
  for ns in ember_cli ember_edge ember_origin; do echo "== $ns"; ip -n $ns -br addr; done
  ;;
down)
  for L in A B; do kill "$(cat $RUN/tb$L.pid 2>/dev/null)" 2>/dev/null || true; done
  for ns in ember_cli ember_edge ember_origin; do ip netns del $ns 2>/dev/null || true; done
  ;;
*) echo "usage: $0 up|check|down"; exit 2 ;;
esac
