# Set 3 — Network Layer (IPv4/IPv6 addressing, subnetting, routing, congestion control)

**68 questions** — High: 39, Medium: 29, Low: 0

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
The IP address 191.200.10.5 belongs to

(1) Class B  
(2) Class C  
(3) Class D  
(4) Class A  

<details><summary>Answer</summary>

**(1)** — Class B covers first octets 128–191.

</details>

**Q2.** `High`  
Match List I with List II.  
List I (Class): A. Class A  B. Class B  C. Class C  D. Class D  
List II (Leading bits of the address): I. 110  II. 1110  III. 0  IV. 10

(1) A-III, B-IV, C-I, D-II  
(2) A-III, B-I, C-IV, D-II  
(3) A-IV, B-III, C-I, D-II  
(4) A-III, B-IV, C-II, D-I  

<details><summary>Answer</summary>

**(1)** — A: 0, B: 10, C: 110, D: 1110, E: 1111.

</details>

**Q3.** `High`  
The number of usable host addresses in a subnet with prefix /26 is

(1) 30  
(2) 62  
(3) 64  
(4) 126  

<details><summary>Answer</summary>

**(2)** — 6 host bits give 2^6 − 2 = 62 usable addresses.

</details>

**Q4.** `High`  
A host has the IP address 192.168.10.130/26. The network address and the broadcast address of its subnet are

(1) 192.168.10.130 and 192.168.10.191  
(2) 192.168.10.128 and 192.168.10.255  
(3) 192.168.10.0 and 192.168.10.63  
(4) 192.168.10.128 and 192.168.10.191  

<details><summary>Answer</summary>

**(4)** — A /26 has blocks of 64; 130 lies in the block 128–191.

</details>

**Q5.** `High`  
What is the subnet (network) address of the host 172.16.45.14/20?

(1) 172.16.0.0  
(2) 172.16.32.0  
(3) 172.16.45.0  
(4) 172.16.40.0  

<details><summary>Answer</summary>

**(2)** — Mask 255.255.240.0; 45 AND 240 = 32, so the subnet is 172.16.32.0.

</details>

**Q6.** `High`  
The directed broadcast address of the subnet containing 172.16.45.14/20 is

(1) 172.16.47.255  
(2) 172.16.45.255  
(3) 172.16.63.255  
(4) 172.16.255.255  

<details><summary>Answer</summary>

**(1)** — The block is 172.16.32.0 – 172.16.47.255.

</details>

**Q7.** `High`  
A Class B network is subnetted with the mask 255.255.240.0. The number of subnets and the number of usable hosts per subnet are

(1) 16 and 4096  
(2) 16 and 4094  
(3) 240 and 4094  
(4) 4096 and 14  

<details><summary>Answer</summary>

**(2)** — 4 bits are borrowed (16 subnets), leaving 12 host bits: 2^12 − 2 = 4094.

</details>

**Q8.** `High`  
An organisation needs a block that supports at least 500 hosts. The longest prefix (smallest block) that suffices is

(1) /23  
(2) /22  
(3) /24  
(4) /25  

<details><summary>Answer</summary>

**(1)** — /23 gives 2^9 − 2 = 510 usable addresses; /24 gives only 254.

</details>

**Q9.** `High`  
A Class C network must be divided into 6 subnets. The subnet mask to be used and the number of usable hosts per subnet are

(1) 255.255.255.224 and 30  
(2) 255.255.255.224 and 32  
(3) 255.255.255.192 and 62  
(4) 255.255.255.240 and 14  

<details><summary>Answer</summary>

**(1)** — 3 bits are needed for 6 subnets (2^3 = 8), leaving 5 host bits: 30 hosts.

</details>

**Q10.** `High`  
For the address 200.10.11.144/27, the last usable host address of the subnet is

(1) 200.10.11.175  
(2) 200.10.11.159  
(3) 200.10.11.190  
(4) 200.10.11.158  

<details><summary>Answer</summary>

**(4)** — Blocks of 32: 128–159; the broadcast is .159, so the last host is .158.

</details>

**Q11.** `High`  
The four networks 192.168.0.0/24, 192.168.1.0/24, 192.168.2.0/24 and 192.168.3.0/24 can be aggregated into the single supernet

(1) 192.168.0.0/23  
(2) 192.168.0.0/16  
(3) 192.168.0.0/22  
(4) 192.168.0.0/21  

<details><summary>Answer</summary>

**(3)** — Four contiguous /24 blocks share the first 22 bits.

</details>

**Q12.** `High`  
How many addresses are contained in the CIDR block 20.10.30.32/28 and what is its last address?

(1) 16 and 20.10.30.47  
(2) 16 and 20.10.30.48  
(3) 32 and 20.10.30.63  
(4) 14 and 20.10.30.46  

<details><summary>Answer</summary>

**(1)** — 32 − 28 = 4 host bits give 16 addresses: .32 to .47.

</details>

**Q13.** `High`  
Which of the following addresses belongs to the same subnet as 10.1.1.70/26?

(1) 10.1.1.60  
(2) 10.1.1.63  
(3) 10.1.1.130  
(4) 10.1.1.100  

<details><summary>Answer</summary>

**(4)** — The /26 block containing .70 is .64 to .127.

</details>

**Q14.** `High`  
Which of the following is NOT a private IPv4 address?

(1) 172.20.1.1  
(2) 192.168.100.1  
(3) 10.200.3.4  
(4) 172.32.1.1  

<details><summary>Answer</summary>

**(4)** — Private ranges: 10.0.0.0/8, 172.16.0.0/12 (172.16–172.31) and 192.168.0.0/16.

</details>

**Q15.** `Medium`  
The address 127.0.0.1 is used for

(1) multicasting  
(2) limited broadcast  
(3) loopback testing  
(4) automatic private addressing  

<details><summary>Answer</summary>

**(3)** — The 127.0.0.0/8 block is reserved for loopback.

</details>

**Q16.** `Medium`  
A host that fails to obtain an address from a DHCP server assigns itself an address in the range

(1) 169.254.0.0/16  
(2) 224.0.0.0/4  
(3) 127.0.0.0/8  
(4) 10.0.0.0/8  

<details><summary>Answer</summary>

**(1)** — 169.254.0.0/16 is the link-local (APIPA) block.

</details>

**Q17.** `Medium`  
The number of networks in Class B and the number of addresses in each Class A network are respectively

(1) 2^14 and 2^16  
(2) 2^16 and 2^24  
(3) 2^14 and 2^24  
(4) 2^21 and 2^8  

<details><summary>Answer</summary>

**(3)** — Class B has a 16-bit netid with 2 fixed bits (2^14 networks); Class A has 24 host bits.

</details>

**Q18.** `High`  
A router has the following routing table entries: 10.0.0.0/8 → interface A, 10.1.0.0/16 → interface B, 10.1.2.0/24 → interface C, default → interface D. A packet destined to 10.1.3.9 is forwarded on

(1) interface B  
(2) interface A  
(3) interface D  
(4) interface C  

<details><summary>Answer</summary>

**(1)** — Longest prefix match: /8 and /16 match, /24 does not; the /16 entry is chosen.

</details>

**Q19.** `High`  
The minimum and maximum sizes of an IPv4 header are

(1) 20 bytes and 40 bytes  
(2) 8 bytes and 60 bytes  
(3) 20 bytes and 60 bytes  
(4) 40 bytes and 60 bytes  

<details><summary>Answer</summary>

**(3)** — HLEN is 4 bits counted in 4-byte words: 5 × 4 = 20 to 15 × 4 = 60 bytes.

</details>

**Q20.** `High`  
An IPv4 datagram arrives with HLEN value 1000 (binary). The number of bytes of options carried is

(1) 32  
(2) 20  
(3) 8  
(4) 12  

<details><summary>Answer</summary>

**(4)** — HLEN = 8, so the header is 32 bytes; 32 − 20 = 12 bytes of options.

</details>

**Q21.** `High`  
An IPv4 datagram of total length 4000 bytes (20-byte header) has to pass through a link with an MTU of 1500 bytes. The number of fragments and the offset value of the last fragment are

(1) 3 and 2960  
(2) 2 and 185  
(3) 4 and 370  
(4) 3 and 370  

<details><summary>Answer</summary>

**(4)** — 3980 data bytes split as 1480 + 1480 + 1020; offsets are 0, 185 and 370 (in units of 8 bytes).

</details>

**Q22.** `High`  
A fragment arrives with a fragmentation offset value of 100, HLEN of 5 and total length of 100. The numbers of its first and last data bytes are

(1) 100 and 179  
(2) 100 and 199  
(3) 800 and 879  
(4) 800 and 899  

<details><summary>Answer</summary>

**(3)** — First byte = 100 × 8 = 800; data length = 100 − 20 = 80 bytes, so the last byte is 879.

</details>

**Q23.** `High`  
In an IPv4 datagram the M (more fragments) bit is 0 and the fragmentation offset is non-zero. The datagram is

(1) the first fragment  
(2) the last fragment  
(3) not fragmented  
(4) a middle fragment  

<details><summary>Answer</summary>

**(2)** — M = 0 with offset ≠ 0 means last fragment; M = 0 with offset 0 means unfragmented.

</details>

**Q24.** `High`  
Match List I with List II.  
List I (Protocol): A. ICMP  B. TCP  C. UDP  D. OSPF  
List II (Value of the IPv4 protocol field): I. 17  II. 89  III. 1  IV. 6

(1) A-III, B-I, C-IV, D-II  
(2) A-IV, B-III, C-I, D-II  
(3) A-III, B-IV, C-II, D-I  
(4) A-III, B-IV, C-I, D-II  

<details><summary>Answer</summary>

**(4)** — ICMP 1, TCP 6, UDP 17, OSPF 89.

</details>

**Q25.** `Medium`  
The purpose of the time-to-live (TTL) field in the IPv4 header is to

(1) measure the round-trip time  
(2) indicate the age of the routing table  
(3) order the fragments  
(4) prevent a datagram from looping in the network forever  

<details><summary>Answer</summary>

**(4)** — Each router decrements TTL; the datagram is discarded when it reaches 0.

</details>

**Q26.** `Medium`  
The header checksum in an IPv4 datagram covers

(1) both header and data  
(2) the header only  
(3) the data only  
(4) the header and a pseudo-header  

<details><summary>Answer</summary>

**(2)** — IPv4 checks only its header, and the checksum is recomputed at every router because TTL changes.

</details>

**Q27.** `High`  
Which of the following fields of the IPv4 header is NOT present in the IPv6 base header?

(1) Version  
(2) Hop limit (TTL)  
(3) Source address  
(4) Header checksum  

<details><summary>Answer</summary>

**(4)** — IPv6 drops the header checksum, HLEN and the fragmentation fields from the base header.

</details>

**Q28.** `High`  
The size of an IPv6 address and of the IPv6 base header are respectively

(1) 64 bits and 40 bytes  
(2) 128 bits and 20 bytes  
(3) 128 bytes and 40 bits  
(4) 128 bits and 40 bytes  

<details><summary>Answer</summary>

**(4)** — 16-byte addresses and a fixed 40-byte base header.

</details>

**Q29.** `High`  
The IPv6 address 2001:0DB8:0000:0000:0000:FF00:0042:8329 can be abbreviated as

(1) 2001:DB8::FF::42:8329  
(2) 2001:DB8::FF00:42:8329  
(3) 2001:DB8:0:FF00:42:8329  
(4) 2001:DB8::FF:42:8329  

<details><summary>Answer</summary>

**(2)** — Leading zeros of each group are dropped and one run of all-zero groups is replaced by ::.

</details>

**Q30.** `High`  
Which of the following types of address is NOT defined in IPv6?

(1) Multicast  
(2) Broadcast  
(3) Unicast  
(4) Anycast  

<details><summary>Answer</summary>

**(2)** — IPv6 replaces broadcast with multicast and adds anycast.

</details>

**Q31.** `Medium`  
Given below are two statements.  
Statement I: In IPv6, fragmentation can be performed only by the source host and not by intermediate routers.  
Statement II: The IPv6 base header contains a 20-bit flow label field.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — IPv6 routers never fragment (a fragment extension header is used by the source), and the flow label is 20 bits.

</details>

**Q32.** `Medium`  
Match List I with List II.  
List I (IPv6 address/prefix): A. ::1  B. FE80::/10  C. FF00::/8  D. ::  
List II (Meaning): I. Multicast  II. Unspecified address  III. Loopback  IV. Link-local unicast

(1) A-IV, B-III, C-I, D-II  
(2) A-III, B-IV, C-I, D-II  
(3) A-III, B-I, C-IV, D-II  
(4) A-II, B-IV, C-I, D-III  

<details><summary>Answer</summary>

**(2)** — ::1 loopback, FE80::/10 link-local, FF00::/8 multicast, :: unspecified.

</details>

**Q33.** `High`  
Which protocol finds the physical (MAC) address corresponding to a known IP address?

(1) DHCP  
(2) ICMP  
(3) RARP  
(4) ARP  

<details><summary>Answer</summary>

**(4)** — ARP maps a logical address to a physical address; RARP does the reverse.

</details>

**Q34.** `High`  
Given below are two statements.  
Statement I: An ARP request is broadcast on the local network.  
Statement II: An ARP reply is also broadcast on the local network.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — The reply is unicast directly to the requester, whose MAC address is in the request.

</details>

**Q35.** `High`  
Arrange the DHCP messages in the order in which they are exchanged when a host obtains an address.  
A. DHCPREQUEST  B. DHCPOFFER  C. DHCPACK  D. DHCPDISCOVER

(1) D, A, B, C  
(2) B, D, A, C  
(3) D, B, C, A  
(4) D, B, A, C  

<details><summary>Answer</summary>

**(4)** — Discover, Offer, Request, Acknowledge (DORA).

</details>

**Q36.** `High`  
Which protocol is used by the ping and traceroute utilities?

(1) ARP  
(2) IGMP  
(3) SNMP  
(4) ICMP  

<details><summary>Answer</summary>

**(4)** — Ping uses ICMP echo request/reply; traceroute relies on ICMP time-exceeded messages.

</details>

**Q37.** `Medium`  
The traceroute program discovers the routers along a path by sending packets with

(1) the record-route option only  
(2) increasing TTL values and collecting ICMP time-exceeded messages  
(3) decreasing TTL values and collecting ICMP echo replies  
(4) TCP SYN segments to every router  

<details><summary>Answer</summary>

**(2)** — Each successive probe has a TTL one larger, so each router in turn discards it and reports back.

</details>

**Q38.** `Medium`  
Network address translation (NAT) is mainly used to

(1) allow many hosts with private addresses to share one or a few public addresses  
(2) map IP addresses to MAC addresses  
(3) translate domain names to IP addresses  
(4) encrypt IP datagrams  

<details><summary>Answer</summary>

**(1)** — NAT rewrites addresses (and ports) at the border router, conserving public IPv4 addresses.

</details>

**Q39.** `High`  
Match List I with List II.  
List I (Routing protocol): A. RIP  B. OSPF  C. BGP  
List II (Algorithm): I. Path vector  II. Distance vector  III. Link state

(1) A-II, B-I, C-III  
(2) A-III, B-II, C-I  
(3) A-I, B-III, C-II  
(4) A-II, B-III, C-I  

<details><summary>Answer</summary>

**(4)** — RIP is distance vector, OSPF is link state, BGP is path vector.

</details>

**Q40.** `High`  
Match List I with List II.  
List I (Routing protocol): A. RIP  B. OSPF  C. BGP  
List II (Carried in): I. TCP port 179  II. IP directly, protocol number 89  III. UDP port 520

(1) A-III, B-I, C-II  
(2) A-III, B-II, C-I  
(3) A-I, B-II, C-III  
(4) A-II, B-III, C-I  

<details><summary>Answer</summary>

**(2)** — RIP uses UDP 520, OSPF runs directly over IP (89), BGP uses TCP 179.

</details>

**Q41.** `High`  
In RIP, a hop count of 16 denotes

(1) a directly connected network  
(2) an unreachable destination (infinity)  
(3) the default route  
(4) the maximum allowed path  

<details><summary>Answer</summary>

**(2)** — RIP limits paths to 15 hops; 16 means infinity.

</details>

**Q42.** `High`  
The count-to-infinity problem is associated with

(1) distance vector routing  
(2) link state routing  
(3) flooding  
(4) path vector routing  

<details><summary>Answer</summary>

**(1)** — Bad news propagates slowly in distance vector routing; split horizon and poison reverse reduce the problem.

</details>

**Q43.** `High`  
Distance vector routing and link state routing are based respectively on the

(1) Bellman-Ford and Dijkstra algorithms  
(2) Dijkstra and Bellman-Ford algorithms  
(3) Bellman-Ford and Floyd-Warshall algorithms  
(4) Prim and Kruskal algorithms  

<details><summary>Answer</summary>

**(1)** — Distance vector uses the Bellman-Ford equation; link state runs Dijkstra on the full topology.

</details>

**Q44.** `Medium`  
Given below are two statements.  
Statement I: In distance vector routing each router shares its knowledge of the entire network only with its neighbours.  
Statement II: In link state routing each router shares knowledge of its neighbourhood with every router in the area by flooding.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — This is the classic contrast between the two approaches.

</details>

**Q45.** `Medium`  
Which of the following is an inter-domain (exterior gateway) routing protocol?

(1) IS-IS  
(2) BGP  
(3) OSPF  
(4) RIP  

<details><summary>Answer</summary>

**(2)** — BGP routes between autonomous systems; the others are intra-domain protocols.

</details>

**Q46.** `Medium`  
RIP routers send periodic updates to their neighbours every

(1) 90 seconds  
(2) 10 seconds  
(3) 180 seconds  
(4) 30 seconds  

<details><summary>Answer</summary>

**(4)** — The RIP periodic timer is about 30 s; the expiration timer is 180 s.

</details>

**Q47.** `Medium`  
Which of the following routing techniques does not require any network information and always finds the shortest path, at the cost of generating many duplicate packets?

(1) Flooding  
(2) Link state routing  
(3) Hierarchical routing  
(4) Distance vector routing  

<details><summary>Answer</summary>

**(1)** — Flooding sends every packet on every outgoing line, so one copy necessarily takes the shortest path.

</details>

**Q48.** `High`  
A token bucket has a capacity of 8 megabits and tokens arrive at 6 Mbps. If the maximum output rate is 10 Mbps and the bucket is initially full, for how long can the host transmit at the maximum rate?

(1) 2 s  
(2) 1.33 s  
(3) 0.8 s  
(4) 4 s  

<details><summary>Answer</summary>

**(1)** — S = C / (M − ρ) = 8 / (10 − 6) = 2 s.

</details>

**Q49.** `High`  
Given below are two statements.  
Statement I: The leaky bucket algorithm produces output at a constant rate regardless of the burstiness of the input.  
Statement II: The token bucket algorithm allows an idle host to save up permission to send bursts later.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Leaky bucket smooths traffic rigidly; token bucket permits bounded bursts.

</details>

**Q50.** `Medium`  
Which of the following is an open-loop congestion control technique?

(1) Implicit signalling  
(2) Backpressure  
(3) Choke packet  
(4) Admission/retransmission policy  

<details><summary>Answer</summary>

**(4)** — Open-loop methods prevent congestion through policies; choke packets, backpressure and signalling are closed-loop.

</details>

**Q51.** `Medium`  
A choke packet is

(1) a packet with TTL equal to zero  
(2) a packet sent by a congested router to the source asking it to reduce its rate  
(3) a packet dropped by the router  
(4) a corrupted packet  

<details><summary>Answer</summary>

**(2)** — It is an explicit closed-loop congestion signal directed at the source.

</details>

**Q52.** `Medium`  
IGMP is used for

(1) managing multicast group membership  
(2) configuring hosts automatically  
(3) resolving addresses  
(4) reporting errors to the source  

<details><summary>Answer</summary>

**(1)** — Hosts use IGMP to inform local routers of the multicast groups they wish to join.

</details>

**Q53.** `Medium`  
Match List I with List II.  
List I (ICMP message): A. Echo request  B. Destination unreachable  C. Time exceeded  D. Echo reply  
List II (Type value): I. 0  II. 3  III. 11  IV. 8

(1) A-IV, B-II, C-I, D-III  
(2) A-IV, B-II, C-III, D-I  
(3) A-I, B-II, C-III, D-IV  
(4) A-IV, B-III, C-II, D-I  

<details><summary>Answer</summary>

**(2)** — Echo reply 0, destination unreachable 3, echo request 8, time exceeded 11.

</details>

**Q54.** `Medium`  
The address 255.255.255.255 is

(1) a directed broadcast address  
(2) a multicast address  
(3) the limited broadcast address  
(4) the loopback address  

<details><summary>Answer</summary>

**(3)** — It reaches all hosts on the local network only; routers never forward it.

</details>

**Q55.** `Medium`  
Which strategies allow the coexistence of IPv4 and IPv6 during the transition?  
A. Dual stack  B. Tunnelling  C. Header translation  D. Supernetting  
Choose the correct answer from the options given below:

(1) A, B and C only  
(2) A, B, C and D  
(3) A and D only  
(4) B, C and D only  

<details><summary>Answer</summary>

**(1)** — Supernetting is an IPv4 address aggregation technique, not a transition strategy.

</details>

**Q56.** `Medium`  
In classful addressing, the default mask of a Class B address is

(1) 255.0.0.0  
(2) 255.255.255.0  
(3) 255.255.0.0  
(4) 255.255.255.255  

<details><summary>Answer</summary>

**(3)** — Class B has a 16-bit network part.

</details>

**Q57.** `Medium`  
The identification, flags and fragmentation offset fields of the IPv4 header have sizes (in bits) of

(1) 32, 3 and 13  
(2) 8, 3 and 13  
(3) 16, 4 and 12  
(4) 16, 3 and 13  

<details><summary>Answer</summary>

**(4)** — Together they make up one 32-bit word of the header.

</details>

**Q58.** `High`  
An ISP is granted the block 16.12.64.0/20. The total number of addresses in the block is

(1) 4096  
(2) 2048  
(3) 8192  
(4) 1024  

<details><summary>Answer</summary>

**(1)** — 2^(32 − 20) = 4096 addresses.

</details>

**Q59.** `High`  
The subnet mask 255.255.255.248 in a Class C network provides

(1) 16 subnets with 14 hosts each  
(2) 32 subnets with 6 hosts each  
(3) 32 subnets with 8 hosts each  
(4) 8 subnets with 30 hosts each  

<details><summary>Answer</summary>

**(2)** — 248 = 11111000: 5 subnet bits (32 subnets) and 3 host bits (6 hosts).

</details>

**Q60.** `Medium`  
Which of the following services is provided by the IPv4 protocol?

(1) Reliable, connection-oriented delivery  
(2) Flow-controlled delivery  
(3) Unreliable, connectionless best-effort delivery  
(4) Reliable, connectionless delivery  

<details><summary>Answer</summary>

**(3)** — IP is a best-effort datagram protocol; reliability is left to upper layers.

</details>

**Q61.** `Medium`  
In OSPF, an autonomous system is divided into areas, all of which must be connected to

(1) a transit AS  
(2) area 1  
(3) the backbone area (area 0)  
(4) the stub area  

<details><summary>Answer</summary>

**(3)** — All OSPF areas attach to the backbone, area 0, through area border routers.

</details>

**Q62.** `Medium`  
Which of the following protocols supports quality of service by reserving resources along a path for a flow?

(1) RIP  
(2) ICMP  
(3) RSVP  
(4) ARP  

<details><summary>Answer</summary>

**(3)** — RSVP is the signalling protocol of Integrated Services.

</details>

**Q63.** `Medium`  
Split horizon is a technique in which a router

(1) sends the full table to all neighbours  
(2) uses two metrics for each route  
(3) does not advertise a route back on the interface from which it was learned  
(4) floods link state packets  

<details><summary>Answer</summary>

**(3)** — It helps avoid two-node routing loops in distance vector protocols.

</details>

**Q64.** `Medium`  
Which of the following is a multicast (Class D) address?

(1) 240.0.0.1  
(2) 192.0.2.1  
(3) 172.16.0.1  
(4) 224.0.0.5  

<details><summary>Answer</summary>

**(4)** — Class D spans 224.0.0.0 to 239.255.255.255; 240 and above is Class E.

</details>

**Q65.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: The IPv4 header checksum must be recalculated at every router.  
Reason R: The TTL field of the header changes at every hop.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Any change in the header (TTL, and possibly fragmentation fields) invalidates the previous checksum.

</details>

**Q66.** `Medium`  
The maximum total length of an IPv4 datagram is

(1) 1500 bytes  
(2) 4,294,967,295 bytes  
(3) 65,535 bytes  
(4) 65,536 bytes  

<details><summary>Answer</summary>

**(3)** — The total length field is 16 bits, so the maximum is 2^16 − 1 bytes.

</details>

**Q67.** `Medium`  
Which of the following addresses can be assigned to a host on the subnet 192.168.5.32/27?

(1) 192.168.5.63  
(2) 192.168.5.50  
(3) 192.168.5.64  
(4) 192.168.5.32  

<details><summary>Answer</summary>

**(2)** — .32 is the network address and .63 the broadcast address; hosts are .33 to .62.

</details>

**Q68.** `Medium`  
A router performs the bitwise AND of a destination address with the subnet mask in order to obtain the

(1) subnetwork address  
(2) broadcast address  
(3) next-hop MAC address  
(4) host address  

<details><summary>Answer</summary>

**(1)** — Masking extracts the network/subnet prefix used for the routing table lookup.

</details>
