# Set 2 — Network Models, Topologies, Data Link Layer, MAC and LANs

**65 questions** — High: 31, Medium: 33, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Match List I with List II.  
List I (OSI layer): A. Physical  B. Data link  C. Network  D. Transport  
List II (Protocol data unit): I. Segment  II. Bits  III. Packet  IV. Frame

(1) A-II, B-IV, C-I, D-III  
(2) A-II, B-IV, C-III, D-I  
(3) A-II, B-III, C-IV, D-I  
(4) A-IV, B-II, C-III, D-I  

<details><summary>Answer</summary>

**(2)** — Physical: bits, data link: frames, network: packets (datagrams), transport: segments.

</details>

**Q2.** `High`  
Match List I with List II.  
List I (Device): A. Repeater  B. Bridge  C. Router  D. Gateway  
List II (Highest OSI layer of operation): I. Network layer  II. All seven layers  III. Physical layer  IV. Data link layer

(1) A-III, B-I, C-IV, D-II  
(2) A-III, B-IV, C-I, D-II  
(3) A-IV, B-III, C-I, D-II  
(4) A-III, B-IV, C-II, D-I  

<details><summary>Answer</summary>

**(2)** — Repeaters/hubs are layer 1, bridges/switches layer 2, routers layer 3, gateways can work up to the application layer.

</details>

**Q3.** `High`  
How many point-to-point links are required to connect 10 devices in a fully connected mesh topology?

(1) 20  
(2) 90  
(3) 45  
(4) 10  

<details><summary>Answer</summary>

**(3)** — n(n − 1)/2 = 10 × 9 / 2 = 45 duplex links.

</details>

**Q4.** `Medium`  
In a fully connected mesh network of n devices, the number of I/O ports required on each device is

(1) 2n  
(2) n − 1  
(3) n  
(4) n(n − 1)/2  

<details><summary>Answer</summary>

**(2)** — Each device connects directly to the other n − 1 devices.

</details>

**Q5.** `High`  
Which layer of the OSI model is responsible for dialog control and synchronisation (check-pointing)?

(1) Transport layer  
(2) Data link layer  
(3) Presentation layer  
(4) Session layer  

<details><summary>Answer</summary>

**(4)** — The session layer establishes, manages and synchronises dialogs between applications.

</details>

**Q6.** `High`  
Data compression, encryption and translation between data formats are functions of the

(1) presentation layer  
(2) application layer  
(3) transport layer  
(4) session layer  

<details><summary>Answer</summary>

**(1)** — The presentation layer deals with the syntax and semantics of the information exchanged.

</details>

**Q7.** `High`  
Which of the following is the correct order of encapsulation as data moves down the layers of the sending host?

(1) Data, segment, packet, frame, bits  
(2) Data, packet, segment, frame, bits  
(3) Bits, frame, packet, segment, data  
(4) Data, frame, packet, segment, bits  

<details><summary>Answer</summary>

**(1)** — Application data is wrapped into a transport segment, a network packet, a data link frame and finally sent as bits.

</details>

**Q8.** `Medium`  
Which OSI layers are combined into the application layer of the TCP/IP protocol suite?

(1) Application and presentation only  
(2) Application, presentation and session  
(3) Session and transport  
(4) Presentation, session and transport  

<details><summary>Answer</summary>

**(2)** — TCP/IP has no separate session and presentation layers; their functions belong to the application layer.

</details>

**Q9.** `High`  
Match List I with List II.  
List I (Address): A. Port address  B. IPv4 address  C. MAC address  D. IPv6 address  
List II (Size): I. 48 bits  II. 128 bits  III. 16 bits  IV. 32 bits

(1) A-III, B-IV, C-II, D-I  
(2) A-III, B-IV, C-I, D-II  
(3) A-III, B-I, C-IV, D-II  
(4) A-IV, B-III, C-I, D-II  

<details><summary>Answer</summary>

**(2)** — Port 16 bits, IPv4 32 bits, MAC 48 bits, IPv6 128 bits.

</details>

**Q10.** `High`  
In a stop-and-wait protocol, the frame transmission time is 1 ms and the one-way propagation delay is 2 ms. Ignoring ACK size and processing time, the link utilisation is

(1) 20%  
(2) 33.3%  
(3) 25%  
(4) 50%  

<details><summary>Answer</summary>

**(1)** — a = Tp/Tt = 2; efficiency = 1/(1 + 2a) = 1/5 = 20%.

</details>

**Q11.** `High`  
A stop-and-wait protocol sends 1000-bit frames over a 1 Mbps link whose one-way propagation delay is 4.5 ms. Ignoring acknowledgement transmission time, the throughput is

(1) 200 kbps  
(2) 100 kbps  
(3) 500 kbps  
(4) 1 Mbps  

<details><summary>Answer</summary>

**(2)** — One frame per Tt + 2Tp = 1 + 9 = 10 ms, so 1000 bits / 10 ms = 100 kbps.

</details>

**Q12.** `High`  
With a 3-bit sequence number field, the maximum sender window sizes in Go-Back-N and Selective Repeat are respectively

(1) 7 and 7  
(2) 8 and 8  
(3) 7 and 4  
(4) 8 and 4  

<details><summary>Answer</summary>

**(3)** — Go-Back-N: 2^m − 1 = 7; Selective Repeat: 2^(m−1) = 4.

</details>

**Q13.** `High`  
In the Selective Repeat ARQ protocol the sender window size is 32. The minimum number of bits needed for the sequence number field is

(1) 5  
(2) 4  
(3) 6  
(4) 7  

<details><summary>Answer</summary>

**(3)** — Window ≤ 2^(m−1), so 2^(m−1) ≥ 32 gives m = 6.

</details>

**Q14.** `High`  
The receiver window size in the Go-Back-N ARQ protocol is

(1) 2^m − 1  
(2) 2^m  
(3) 1  
(4) 2^(m−1)  

<details><summary>Answer</summary>

**(3)** — The Go-Back-N receiver accepts only the next in-order frame, so its window is 1.

</details>

**Q15.** `Medium`  
In a sliding window protocol, the optimal window size for maximum utilisation, where a = Tp/Tt, is

(1) 2a  
(2) 1 + a  
(3) 1 + 2a  
(4) a  

<details><summary>Answer</summary>

**(3)** — In one round-trip time the sender can transmit 1 + 2a frames.

</details>

**Q16.** `High`  
The maximum throughput of pure ALOHA and slotted ALOHA are respectively

(1) 50% and 100%  
(2) 18.4% and 50%  
(3) 36.8% and 18.4%  
(4) 18.4% and 36.8%  

<details><summary>Answer</summary>

**(4)** — Pure ALOHA: S = Ge^(−2G), max 1/(2e) at G = 0.5; slotted: S = Ge^(−G), max 1/e at G = 1.

</details>

**Q17.** `High`  
A pure ALOHA network transmits 200-bit frames on a shared 200 kbps channel. If the stations together produce 1000 frames per second, the throughput is approximately

(1) 184 frames per second  
(2) 500 frames per second  
(3) 368 frames per second  
(4) 135 frames per second  

<details><summary>Answer</summary>

**(4)** — Frame time is 1 ms, so G = 1; S = G e^(−2G) = 0.135, i.e. 135 frames per second.

</details>

**Q18.** `Medium`  
The vulnerable time in pure ALOHA, where Tfr is the frame transmission time, is

(1) Tfr / 2  
(2) 2 × Tfr  
(3) Tfr  
(4) 4 × Tfr  

<details><summary>Answer</summary>

**(2)** — A frame can collide with frames started one frame time before or after it; in slotted ALOHA it is Tfr.

</details>

**Q19.** `High`  
A CSMA/CD network runs at 10 Mbps over a cable of length 2500 m with a signal speed of 2 × 10^8 m/s. The minimum frame size is

(1) 250 bits  
(2) 125 bits  
(3) 512 bits  
(4) 500 bits  

<details><summary>Answer</summary>

**(1)** — Tt ≥ 2Tp = 2 × 12.5 µs = 25 µs; 25 µs × 10 Mbps = 250 bits.

</details>

**Q20.** `High`  
The minimum and maximum frame lengths (excluding preamble and SFD) in standard IEEE 802.3 Ethernet are

(1) 72 bytes and 1526 bytes  
(2) 64 bytes and 1518 bytes  
(3) 64 bytes and 1500 bytes  
(4) 46 bytes and 1500 bytes  

<details><summary>Answer</summary>

**(2)** — 46–1500 bytes of payload plus 18 bytes of header and trailer gives 64–1518 bytes.

</details>

**Q21.** `High`  
In the binary exponential backoff algorithm of CSMA/CD, after the 3rd collision a station waits a random number of slot times chosen from

(1) 0 to 8  
(2) 1 to 8  
(3) 0 to 7  
(4) 0 to 3  

<details><summary>Answer</summary>

**(3)** — After the n-th collision K is chosen uniformly from 0 to 2^n − 1.

</details>

**Q22.** `Medium`  
In standard Ethernet a station gives up transmitting a frame after how many unsuccessful attempts?

(1) 16  
(2) 32  
(3) 10  
(4) 15  

<details><summary>Answer</summary>

**(1)** — The backoff exponent is capped at 10 and the frame is aborted after 16 attempts.

</details>

**Q23.** `High`  
Match List I with List II.  
List I (IEEE standard): A. 802.3  B. 802.5  C. 802.11  D. 802.15  
List II (Technology): I. Wireless LAN  II. Token ring  III. Bluetooth / wireless PAN  IV. CSMA/CD Ethernet

(1) A-IV, B-I, C-II, D-III  
(2) A-IV, B-II, C-III, D-I  
(3) A-IV, B-II, C-I, D-III  
(4) A-II, B-IV, C-I, D-III  

<details><summary>Answer</summary>

**(3)** — 802.3 Ethernet, 802.5 token ring, 802.11 WLAN, 802.15 WPAN.

</details>

**Q24.** `Medium`  
Match List I with List II.  
List I (IEEE standard): A. 802.1Q  B. 802.2  C. 802.4  D. 802.16  
List II (Technology): I. Token bus  II. WiMAX  III. VLAN tagging  IV. Logical link control

(1) A-I, B-IV, C-III, D-II  
(2) A-IV, B-III, C-I, D-II  
(3) A-III, B-IV, C-II, D-I  
(4) A-III, B-IV, C-I, D-II  

<details><summary>Answer</summary>

**(4)** — 802.1Q VLAN, 802.2 LLC, 802.4 token bus, 802.16 WiMAX.

</details>

**Q25.** `High`  
Which multiple access method is used by IEEE 802.11 wireless LANs?

(1) CSMA/CA  
(2) CSMA/CD  
(3) Token passing  
(4) Pure ALOHA  

<details><summary>Answer</summary>

**(1)** — Collisions cannot be detected reliably on a wireless medium, so 802.11 uses collision avoidance.

</details>

**Q26.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: CSMA/CD is not used in wireless LANs.  
Reason R: A wireless station cannot reliably detect a collision while transmitting, because its own signal is much stronger than any received signal and stations may be hidden from one another.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Both the signal-strength problem and the hidden-station problem make collision detection impractical.

</details>

**Q27.** `High`  
The RTS/CTS handshake in IEEE 802.11 is used to solve the

(1) silly window syndrome  
(2) count-to-infinity problem  
(3) exposed terminal problem only  
(4) hidden terminal problem  

<details><summary>Answer</summary>

**(4)** — RTS/CTS reserves the channel so that stations hidden from the sender hear the CTS and defer.

</details>

**Q28.** `High`  
In the designation 10Base-T, the terms 10, Base and T stand for

(1) 10 Mbps, broadband, twisted pair  
(2) 10 MHz, baseband, thick coax  
(3) 10 Mbps, baseband, twisted pair  
(4) 10 m, baseband, terminator  

<details><summary>Answer</summary>

**(3)** — Data rate in Mbps, baseband signalling, and twisted-pair medium.

</details>

**Q29.** `Medium`  
The maximum segment length of 10Base5 (thick Ethernet) is

(1) 185 m  
(2) 500 m  
(3) 2000 m  
(4) 100 m  

<details><summary>Answer</summary>

**(2)** — 10Base5: 500 m; 10Base2: 185 m; 10Base-T: 100 m.

</details>

**Q30.** `High`  
An Ethernet MAC address is

(1) 128 bits long and written in hexadecimal  
(2) 32 bits long and written in dotted decimal  
(3) 48 bits long and written in hexadecimal  
(4) 64 bits long and written in hexadecimal  

<details><summary>Answer</summary>

**(3)** — A MAC address has 6 bytes (48 bits), usually written as 12 hexadecimal digits.

</details>

**Q31.** `Medium`  
An Ethernet destination address in which the least significant bit of the first byte is 1 is a

(1) multicast address  
(2) loopback address  
(3) private address  
(4) unicast address  

<details><summary>Answer</summary>

**(1)** — LSB of the first byte 0 = unicast, 1 = multicast; all 1s is the broadcast address.

</details>

**Q32.** `Medium`  
The preamble and start frame delimiter of an IEEE 802.3 frame together occupy

(1) 12 bytes  
(2) 8 bytes  
(3) 7 bytes  
(4) 4 bytes  

<details><summary>Answer</summary>

**(2)** — 7 bytes of preamble (alternating 1s and 0s) plus 1 byte of SFD (10101011).

</details>

**Q33.** `High`  
A network has four hosts connected to a hub, the hub connected to a switch port, and three more hosts connected directly to other ports of the same switch. The number of collision domains and broadcast domains are respectively

(1) 1 and 1  
(2) 7 and 1  
(3) 4 and 1  
(4) 4 and 4  

<details><summary>Answer</summary>

**(3)** — Each switch port is a collision domain (1 for the hub segment + 3 for the hosts); a switch does not divide the broadcast domain.

</details>

**Q34.** `High`  
Which device breaks up both collision domains and broadcast domains?

(1) Router  
(2) Bridge  
(3) Layer-2 switch  
(4) Hub  

<details><summary>Answer</summary>

**(1)** — Routers do not forward layer-2 broadcasts; switches and bridges split only collision domains.

</details>

**Q35.** `High`  
A transparent (learning) bridge builds its forwarding table by examining the

(1) destination MAC address of incoming frames  
(2) source MAC address of incoming frames  
(3) destination IP address of incoming packets  
(4) source IP address of incoming packets  

<details><summary>Answer</summary>

**(2)** — The bridge learns which port a station is on from the source address; it forwards using the destination address.

</details>

**Q36.** `Medium`  
The spanning tree protocol is used in a switched LAN to

(1) find the shortest path between two hosts  
(2) assign IP addresses to switches  
(3) create VLANs  
(4) prevent loops when redundant bridges are present  

<details><summary>Answer</summary>

**(4)** — STP blocks redundant ports to build a loop-free logical topology.

</details>

**Q37.** `High`  
Which of the following is NOT a type of HDLC frame?

(1) Acknowledgement frame  
(2) Unnumbered frame  
(3) Supervisory frame  
(4) Information frame  

<details><summary>Answer</summary>

**(1)** — HDLC defines I-frames, S-frames and U-frames; acknowledgements are carried in I- and S-frames.

</details>

**Q38.** `Medium`  
The flag field that delimits an HDLC frame is

(1) 01111110  
(2) 10101010  
(3) 10101011  
(4) 11111111  

<details><summary>Answer</summary>

**(1)** — The flag 01111110 marks both the start and the end of a frame; bit stuffing keeps it unique.

</details>

**Q39.** `Medium`  
Which of the following statements about the Point-to-Point Protocol (PPP) is correct?

(1) PPP provides flow control using a sliding window  
(2) PPP is a bit-oriented protocol using bit stuffing  
(3) PPP can be used only on multipoint links  
(4) PPP uses LCP to establish the link and NCP to configure the network layer  

<details><summary>Answer</summary>

**(4)** — PPP is byte-oriented, uses byte stuffing, and has no flow control; LCP and NCP are its control protocols.

</details>

**Q40.** `Medium`  
The technique of temporarily delaying an acknowledgement so that it can be attached to the next outgoing data frame is called

(1) bit stuffing  
(2) piggybacking  
(3) multiplexing  
(4) pipelining  

<details><summary>Answer</summary>

**(2)** — Piggybacking saves bandwidth by carrying the ACK in the header of a data frame.

</details>

**Q41.** `Medium`  
Match List I with List II.  
List I (Access method category): A. Random access  B. Controlled access  C. Channelization  
List II (Protocols): I. FDMA, TDMA, CDMA  II. ALOHA, CSMA/CD, CSMA/CA  III. Reservation, polling, token passing

(1) A-I, B-III, C-II  
(2) A-III, B-II, C-I  
(3) A-II, B-I, C-III  
(4) A-II, B-III, C-I  

<details><summary>Answer</summary>

**(4)** — Standard classification of multiple access protocols.

</details>

**Q42.** `Medium`  
In which CSMA persistence method does a station that finds the channel idle transmit immediately with probability 1?

(1) 0-persistent  
(2) 1-persistent  
(3) p-persistent  
(4) Non-persistent  

<details><summary>Answer</summary>

**(2)** — 1-persistent CSMA sends as soon as the line is idle, giving the highest chance of collision.

</details>

**Q43.** `Medium`  
Given below are two statements.  
Statement I: In a datagram network every packet carries the full destination address and packets of the same message may follow different paths.  
Statement II: In a virtual-circuit network resources are necessarily reserved for the entire duration of the connection, as in circuit switching.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — A virtual circuit fixes the route and uses a VC identifier, but resource reservation is optional and may be on demand.

</details>

**Q44.** `Medium`  
An ATM cell consists of

(1) 5 bytes of header and 53 bytes of payload  
(2) 8 bytes of header and 53 bytes of payload  
(3) 48 bytes of header and 5 bytes of payload  
(4) 5 bytes of header and 48 bytes of payload  

<details><summary>Answer</summary>

**(4)** — An ATM cell is a fixed 53 bytes: 5-byte header plus 48-byte payload.

</details>

**Q45.** `Medium`  
Which line coding is used by IEEE 802.5 token ring?

(1) Differential Manchester  
(2) NRZ-L  
(3) Manchester  
(4) AMI  

<details><summary>Answer</summary>

**(1)** — Token ring uses differential Manchester; 10 Mbps Ethernet uses Manchester.

</details>

**Q46.** `Medium`  
Which of the following topologies requires a terminator at each end of the cable?

(1) Star  
(2) Bus  
(3) Mesh  
(4) Ring  

<details><summary>Answer</summary>

**(2)** — Terminators absorb the signal at the ends of the bus backbone to prevent reflection.

</details>

**Q47.** `Medium`  
Given below are two statements.  
Statement I: In a star topology the failure of the central hub brings down the whole network.  
Statement II: In a star topology the failure of one link affects all the other stations.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — The hub is a single point of failure, but a broken link isolates only the station on that link.

</details>

**Q48.** `High`  
Arrange the layers of the OSI model from top to bottom.  
A. Session  B. Network  C. Presentation  D. Transport  E. Data link

(1) C, A, D, B, E  
(2) A, C, D, B, E  
(3) C, A, B, D, E  
(4) C, D, A, B, E  

<details><summary>Answer</summary>

**(1)** — Application, Presentation, Session, Transport, Network, Data link, Physical.

</details>

**Q49.** `High`  
Which of the following are functions of the data link layer?  
A. Framing  B. Flow control  C. Routing  D. Error control  E. Media access control  
Choose the correct answer from the options given below:

(1) A, B, D and E only  
(2) A, B and C only  
(3) B, C and D only  
(4) A, C, D and E only  

<details><summary>Answer</summary>

**(1)** — Routing is a network layer function; the others belong to the data link layer.

</details>

**Q50.** `Medium`  
In Go-Back-N ARQ, if frames 0 to 6 have been sent and the timer for frame 3 expires, the sender retransmits

(1) frames 3, 4, 5 and 6  
(2) frames 4, 5 and 6  
(3) frame 3 only  
(4) frames 0 to 6  

<details><summary>Answer</summary>

**(1)** — Go-Back-N resends the lost frame and every frame sent after it.

</details>

**Q51.** `Medium`  
In Selective Repeat ARQ a negative acknowledgement NAK n means

(1) all frames from n onward are to be retransmitted  
(2) all frames up to n are received  
(3) the receiver window is full  
(4) only frame n is to be retransmitted  

<details><summary>Answer</summary>

**(4)** — Selective Repeat retransmits only the damaged or lost frame.

</details>

**Q52.** `High`  
The link utilisation of Go-Back-N with window size N, when N < 1 + 2a, is

(1) N / (1 + a)  
(2) N / (1 + 2a)  
(3) 1 / (1 + 2a)  
(4) 1  

<details><summary>Answer</summary>

**(2)** — N frames are delivered in each cycle of duration (1 + 2a) frame times.

</details>

**Q53.** `Medium`  
A LAN technology known as Fast Ethernet operates at

(1) 10 Gbps  
(2) 1 Gbps  
(3) 100 Mbps  
(4) 10 Mbps  

<details><summary>Answer</summary>

**(3)** — Fast Ethernet (802.3u) is 100 Mbps; Gigabit Ethernet (802.3z/ab) is 1000 Mbps.

</details>

**Q54.** `Medium`  
Which of the following networks covers the smallest geographical area?

(1) PAN  
(2) LAN  
(3) MAN  
(4) WAN  

<details><summary>Answer</summary>

**(1)** — A personal area network spans a few metres around one person.

</details>

**Q55.** `Medium`  
The data link layer is divided by the IEEE 802 project into which two sublayers?

(1) HDLC and PPP  
(2) LLC and PHY  
(3) MAC and PHY  
(4) LLC and MAC  

<details><summary>Answer</summary>

**(4)** — Logical link control (802.2) sits above the technology-specific media access control sublayer.

</details>

**Q56.** `Medium`  
In the byte-stuffing (character-stuffing) method of framing, a special byte is added to the data section when

(1) five consecutive 1s occur  
(2) a parity error occurs  
(3) the data contains a byte with the same pattern as the flag or the escape character  
(4) the frame is too short  

<details><summary>Answer</summary>

**(3)** — An ESC byte is inserted before any flag or ESC pattern that appears in the data.

</details>

**Q57.** `Medium`  
Which of the following is a connection-oriented, packet-switched WAN technology that uses a 10-bit DLCI to identify virtual circuits?

(1) Frame Relay  
(2) Ethernet  
(3) FDDI  
(4) Token ring  

<details><summary>Answer</summary>

**(1)** — Frame Relay identifies virtual circuits by the data link connection identifier.

</details>

**Q58.** `Medium`  
In IEEE 802.11, which interframe space gives the highest priority to frames such as ACK and CTS?

(1) EIFS  
(2) PIFS  
(3) SIFS  
(4) DIFS  

<details><summary>Answer</summary>

**(3)** — SIFS is the shortest interframe space, so frames waiting only SIFS get the medium first: SIFS < PIFS < DIFS.

</details>

**Q59.** `Medium`  
FDDI uses which of the following access methods and media?

(1) CSMA/CA over radio  
(2) Polling over twisted pair  
(3) Token passing over a dual fibre ring  
(4) CSMA/CD over coaxial cable  

<details><summary>Answer</summary>

**(3)** — FDDI is a 100 Mbps token-passing network built as dual counter-rotating fibre rings.

</details>

**Q60.** `Medium`  
Given below are two statements.  
Statement I: A VLAN divides a single switched network into multiple broadcast domains.  
Statement II: Communication between hosts in different VLANs requires a layer-3 device.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Each VLAN is its own broadcast domain, and inter-VLAN traffic must be routed.

</details>

**Q61.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Standard Ethernet specifies a minimum frame length of 64 bytes.  
Reason R: A station must still be transmitting when a collision from the farthest station is detected, so the frame transmission time must be at least twice the maximum propagation time.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — The minimum frame size comes directly from the CSMA/CD requirement Tt ≥ 2Tp.

</details>

**Q62.** `Medium`  
A group of computers and devices that share a common communication line in which control alternates between a primary station and secondary stations uses

(1) reservation  
(2) CSMA  
(3) token passing  
(4) polling  

<details><summary>Answer</summary>

**(4)** — In polling the primary station selects and polls the secondaries.

</details>

**Q63.** `Low`  
Which of the following is a set of rules that governs data communication?

(1) Topology  
(2) Interface  
(3) Protocol  
(4) Standard  

<details><summary>Answer</summary>

**(3)** — A protocol defines the syntax, semantics and timing of communication.

</details>

**Q64.** `Medium`  
The three key elements of a protocol are

(1) speed, cost and security  
(2) sender, receiver and medium  
(3) syntax, semantics and timing  
(4) framing, routing and addressing  

<details><summary>Answer</summary>

**(3)** — Syntax (format), semantics (meaning) and timing (when and how fast).

</details>

**Q65.** `Medium`  
Which of the following Ethernet standards uses optical fibre?

(1) 1000Base-T  
(2) 100Base-TX  
(3) 1000Base-SX  
(4) 10Base-T  

<details><summary>Answer</summary>

**(3)** — 1000Base-SX is short-wavelength Gigabit Ethernet over multimode fibre; the others use twisted pair.

</details>
