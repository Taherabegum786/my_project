# Set 6 — Mobile Technology (cellular systems, GSM/GPRS/SMS, wireless LANs, MANETs, satellites, geolocation)

**54 questions** — High: 22, Medium: 31, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
In a cellular system with hexagonal cells, the cluster size N must satisfy N = i² + ij + j² for non-negative integers i and j. Which of the following is NOT a valid cluster size?

(1) 5  
(2) 3  
(3) 4  
(4) 7  

<details><summary>Answer</summary>

**(1)** — Valid values are 1, 3, 4, 7, 9, 12, 13 ...; 5 cannot be written in this form.

</details>

**Q2.** `High`  
A cellular system has 490 duplex channels and uses a cluster size of 7. The number of channels available per cell is

(1) 490  
(2) 98  
(3) 35  
(4) 70  

<details><summary>Answer</summary>

**(4)** — 490 / 7 = 70 channels per cell.

</details>

**Q3.** `High`  
For a cluster size of N = 7 and cell radius R, the co-channel reuse distance D is approximately

(1) 2.65 R  
(2) 7 R  
(3) 4.58 R  
(4) 3.46 R  

<details><summary>Answer</summary>

**(3)** — D = R × sqrt(3N) = R × sqrt(21) ≈ 4.58 R.

</details>

**Q4.** `High`  
Given below are two statements.  
Statement I: Decreasing the cluster size N increases the capacity of a cellular system.  
Statement II: Decreasing the cluster size N reduces co-channel interference.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — A smaller N gives more channels per cell but brings co-channel cells closer, increasing interference.

</details>

**Q5.** `High`  
The process of transferring an ongoing call from one base station to another as the mobile moves is called

(1) roaming  
(2) registration  
(3) paging  
(4) handoff (handover)  

<details><summary>Answer</summary>

**(4)** — Roaming refers to service in a network other than the home network.

</details>

**Q6.** `High`  
Given below are two statements.  
Statement I: In a hard handoff the mobile breaks the connection with the old base station before connecting to the new one.  
Statement II: Soft handoff, in which the mobile communicates with two base stations simultaneously, is a feature of CDMA systems.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Hard handoff is break-before-make; soft handoff is make-before-break.

</details>

**Q7.** `Medium`  
Which techniques are used to increase the capacity of a cellular system?  
A. Cell splitting  B. Sectoring  C. Increasing the cell radius  D. Microcell zone concept  
Choose the correct answer from the options given below:

(1) B, C and D only  
(2) A and C only  
(3) A, B, C and D  
(4) A, B and D only  

<details><summary>Answer</summary>

**(4)** — Larger cells reduce capacity per unit area; splitting, sectoring and microzones increase it.

</details>

**Q8.** `High`  
Match List I with List II.  
List I (Generation): A. 1G  B. 2G  C. 3G  D. 4G  
List II (Representative technology): I. LTE  II. UMTS / WCDMA  III. AMPS  IV. GSM

(1) A-III, B-II, C-IV, D-I  
(2) A-III, B-IV, C-I, D-II  
(3) A-IV, B-III, C-II, D-I  
(4) A-III, B-IV, C-II, D-I  

<details><summary>Answer</summary>

**(4)** — 1G analog AMPS, 2G digital GSM, 3G UMTS, 4G LTE.

</details>

**Q9.** `High`  
GSM uses which multiple access technique?

(1) CDMA  
(2) FDMA only  
(3) A combination of FDMA and TDMA  
(4) OFDMA  

<details><summary>Answer</summary>

**(3)** — Each 200 kHz carrier is divided into 8 time slots.

</details>

**Q10.** `Medium`  
In GSM, the carrier spacing and the number of time slots per TDMA frame are respectively

(1) 1.25 MHz and 64  
(2) 30 kHz and 6  
(3) 200 kHz and 8  
(4) 25 kHz and 3  

<details><summary>Answer</summary>

**(3)** — GSM carriers are 200 kHz wide with 8 full-rate slots.

</details>

**Q11.** `Medium`  
The modulation technique used in GSM is

(1) QPSK  
(2) BFSK  
(3) GMSK  
(4) 16-QAM  

<details><summary>Answer</summary>

**(3)** — Gaussian minimum shift keying gives a compact spectrum with constant envelope.

</details>

**Q12.** `High`  
Match List I with List II.  
List I (GSM entity): A. HLR  B. VLR  C. EIR  D. AuC  
List II (Function): I. Stores authentication and ciphering keys  II. Database of valid and stolen mobile equipment (IMEI)  III. Permanent database of subscribers of the home network  IV. Temporary database of subscribers currently in an MSC area

(1) A-IV, B-III, C-II, D-I  
(2) A-III, B-IV, C-II, D-I  
(3) A-III, B-IV, C-I, D-II  
(4) A-III, B-II, C-IV, D-I  

<details><summary>Answer</summary>

**(2)** — Home/visitor location registers, equipment identity register, authentication centre.

</details>

**Q13.** `Medium`  
Given below are two statements.  
Statement I: The IMSI identifies the subscriber and is stored in the SIM.  
Statement II: The IMEI identifies the mobile equipment.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — IMSI is tied to the subscription, IMEI to the handset.

</details>

**Q14.** `Medium`  
In GSM, the algorithms A3, A5 and A8 are used respectively for

(1) encryption, authentication and key generation  
(2) authentication, encryption and cipher key generation  
(3) authentication, key generation and encryption  
(4) key generation, authentication and encryption  

<details><summary>Answer</summary>

**(2)** — A3 authenticates, A8 derives the session key, A5 encrypts the radio link.

</details>

**Q15.** `Medium`  
Arrange the GSM network elements in the order in which a call from a mobile station passes through them.  
A. BSC  B. MSC  C. BTS

(1) C, B, A  
(2) B, A, C  
(3) A, C, B  
(4) C, A, B  

<details><summary>Answer</summary>

**(4)** — Mobile station, base transceiver station, base station controller, mobile switching centre.

</details>

**Q16.** `High`  
GPRS adds packet-switched data to GSM by introducing which two new network nodes?

(1) HLR and VLR  
(2) MSC and GMSC  
(3) SGSN and GGSN  
(4) BSC and BTS  

<details><summary>Answer</summary>

**(3)** — The serving and gateway GPRS support nodes route packets and connect to external data networks.

</details>

**Q17.** `Medium`  
GPRS and EDGE are commonly referred to respectively as

(1) 2.5G and 2.75G  
(2) 1G and 2G  
(3) 2G and 3G  
(4) 3G and 4G  

<details><summary>Answer</summary>

**(1)** — GPRS is 2.5G; EDGE, with 8-PSK modulation, is 2.75G.

</details>

**Q18.** `High`  
The maximum length of a single SMS message using the default 7-bit GSM alphabet is

(1) 256 characters  
(2) 140 characters  
(3) 160 characters  
(4) 70 characters  

<details><summary>Answer</summary>

**(3)** — 140 bytes of payload hold 160 seven-bit characters (70 in 16-bit UCS-2).

</details>

**Q19.** `Medium`  
SMS messages are delivered using

(1) GPRS tunnels only  
(2) Wi-Fi access points  
(3) signalling channels and a store-and-forward SMS centre  
(4) a dedicated traffic channel and circuit switching  

<details><summary>Answer</summary>

**(3)** — The SMSC stores the message and forwards it when the recipient is reachable.

</details>

**Q20.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: CDMA systems require tight power control.  
Reason R: Without it, a transmitter near the base station would drown out the signals of distant mobiles (the near-far problem).

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — All users share the same frequency, so received powers must be equalised.

</details>

**Q21.** `Medium`  
The multiple access technique used in the downlink of 4G LTE is

(1) CDMA  
(2) OFDMA  
(3) FDMA  
(4) TDMA  

<details><summary>Answer</summary>

**(2)** — LTE uses OFDMA on the downlink and SC-FDMA on the uplink.

</details>

**Q22.** `High`  
Match List I with List II.  
List I (Standard): A. IEEE 802.11a  B. IEEE 802.11b  C. IEEE 802.11g  D. IEEE 802.11n  
List II (Band and maximum data rate): I. 2.4 GHz, 54 Mbps  II. 2.4/5 GHz, up to 600 Mbps using MIMO  III. 5 GHz, 54 Mbps  IV. 2.4 GHz, 11 Mbps

(1) A-III, B-IV, C-II, D-I  
(2) A-III, B-IV, C-I, D-II  
(3) A-IV, B-III, C-I, D-II  
(4) A-I, B-IV, C-III, D-II  

<details><summary>Answer</summary>

**(2)** — 802.11a: 5 GHz/54; b: 2.4 GHz/11; g: 2.4 GHz/54; n: MIMO up to 600 Mbps.

</details>

**Q23.** `Medium`  
An IEEE 802.11 network that operates without an access point is called

(1) an independent BSS (ad hoc network)  
(2) an extended service set  
(3) a distribution system  
(4) an infrastructure BSS  

<details><summary>Answer</summary>

**(1)** — In an IBSS the stations communicate directly with one another.

</details>

**Q24.** `Medium`  
Two or more basic service sets interconnected by a distribution system form

(1) an IBSS  
(2) a scatternet  
(3) a piconet  
(4) an ESS  

<details><summary>Answer</summary>

**(4)** — An extended service set lets stations roam between access points.

</details>

**Q25.** `Medium`  
In IEEE 802.11, the distributed coordination function (DCF) uses

(1) polling  
(2) CSMA/CA  
(3) token passing  
(4) CSMA/CD  

<details><summary>Answer</summary>

**(2)** — DCF is contention-based CSMA/CA; the optional PCF uses polling by the access point.

</details>

**Q26.** `High`  
Station A and station C are both within range of station B but cannot hear each other. If A and C transmit to B at the same time, the collision at B is an example of the

(1) hidden terminal problem  
(2) capture effect  
(3) near-far problem  
(4) exposed terminal problem  

<details><summary>Answer</summary>

**(1)** — Each sender is hidden from the other; RTS/CTS mitigates it.

</details>

**Q27.** `High`  
A Bluetooth piconet can have

(1) any number of masters  
(2) 2 masters and up to 6 active slaves  
(3) 1 master and up to 8 active slaves  
(4) 1 master and up to 7 active slaves  

<details><summary>Answer</summary>

**(4)** — 3-bit active member addresses allow 7 active slaves; more can be parked.

</details>

**Q28.** `Medium`  
Bluetooth operates in the 2.4 GHz ISM band and uses

(1) OFDM  
(2) DSSS  
(3) frequency hopping spread spectrum at 1600 hops per second  
(4) infrared  

<details><summary>Answer</summary>

**(3)** — Classic Bluetooth hops over 79 channels of 1 MHz.

</details>

**Q29.** `Medium`  
Two or more piconets linked by a device that participates in both form a

(1) scatternet  
(2) basic service set  
(3) cluster  
(4) mesh cell  

<details><summary>Answer</summary>

**(1)** — A bridge node may be a slave in one piconet and a master or slave in another.

</details>

**Q30.** `Medium`  
Match List I with List II.  
List I (Technology): A. Bluetooth  B. ZigBee  C. Wi-Fi  D. WiMAX  
List II (IEEE standard): I. 802.16  II. 802.11  III. 802.15.1  IV. 802.15.4

(1) A-IV, B-III, C-II, D-I  
(2) A-III, B-IV, C-I, D-II  
(3) A-III, B-II, C-IV, D-I  
(4) A-III, B-IV, C-II, D-I  

<details><summary>Answer</summary>

**(4)** — Bluetooth 802.15.1, ZigBee 802.15.4, Wi-Fi 802.11, WiMAX 802.16.

</details>

**Q31.** `High`  
In Mobile IP, the temporary address that a mobile node acquires in a foreign network is called the

(1) link-local address  
(2) anycast address  
(3) home address  
(4) care-of address  

<details><summary>Answer</summary>

**(4)** — The home agent tunnels packets to the care-of address.

</details>

**Q32.** `High`  
In Mobile IP, packets addressed to the mobile node's home address are intercepted by the

(1) correspondent node  
(2) foreign agent and tunnelled to the home agent  
(3) home agent and tunnelled to the care-of address  
(4) DNS server  

<details><summary>Answer</summary>

**(3)** — The home agent encapsulates the packets (IP-in-IP) and forwards them to the foreign network.

</details>

**Q33.** `Medium`  
The inefficiency in Mobile IP in which packets from the correspondent node travel via the home agent even when the mobile node is nearby is called

(1) count to infinity  
(2) triangle routing  
(3) tunnel collapse  
(4) ping-pong handoff  

<details><summary>Answer</summary>

**(2)** — Route optimisation lets the correspondent node send directly to the care-of address.

</details>

**Q34.** `High`  
A mobile ad hoc network (MANET) is characterised by

(1) a fixed infrastructure of base stations  
(2) self-configuring mobile nodes that act as both hosts and routers without fixed infrastructure  
(3) a static topology  
(4) wired backbone links between nodes  

<details><summary>Answer</summary>

**(2)** — Topology changes dynamically and routing is multi-hop.

</details>

**Q35.** `High`  
Match List I with List II.  
List I (MANET routing protocol): A. DSDV  B. AODV  C. ZRP  
List II (Category): I. Hybrid  II. Proactive (table-driven)  III. Reactive (on-demand)

(1) A-I, B-III, C-II  
(2) A-II, B-III, C-I  
(3) A-II, B-I, C-III  
(4) A-III, B-II, C-I  

<details><summary>Answer</summary>

**(2)** — DSDV and OLSR are proactive, AODV and DSR are reactive, ZRP is hybrid.

</details>

**Q36.** `Medium`  
In the Dynamic Source Routing (DSR) protocol

(1) routes are computed by a central server  
(2) every node maintains a route to every other node at all times  
(3) link state packets are flooded periodically  
(4) the complete route is carried in the header of each data packet  

<details><summary>Answer</summary>

**(4)** — DSR is an on-demand source-routing protocol; AODV instead keeps next-hop entries at the nodes.

</details>

**Q37.** `Medium`  
In AODV, a route to a destination is discovered by

(1) flooding the data packets  
(2) broadcasting a route request (RREQ) and receiving a route reply (RREP)  
(3) consulting the home agent  
(4) periodic exchange of full routing tables  

<details><summary>Answer</summary>

**(2)** — Route discovery is triggered only when a route is needed.

</details>

**Q38.** `High`  
Match List I with List II.  
List I (Satellite orbit): A. LEO  B. MEO  C. GEO  
List II (Approximate altitude): I. 35,786 km  II. 500 to 2,000 km  III. 5,000 to 20,000 km

(1) A-II, B-III, C-I  
(2) A-I, B-III, C-II  
(3) A-II, B-I, C-III  
(4) A-III, B-II, C-I  

<details><summary>Answer</summary>

**(1)** — Low, medium and geostationary Earth orbits.

</details>

**Q39.** `Medium`  
The minimum number of geostationary satellites needed to cover almost the whole Earth (excluding the polar regions) is

(1) 24  
(2) 6  
(3) 3  
(4) 2  

<details><summary>Answer</summary>

**(3)** — Three satellites spaced 120 degrees apart suffice.

</details>

**Q40.** `Medium`  
The round-trip propagation delay (Earth station to satellite and back to Earth) of a geostationary satellite link is approximately

(1) 25 ms  
(2) 2.5 ms  
(3) 2.5 s  
(4) 250 ms  

<details><summary>Answer</summary>

**(4)** — About 36,000 km each way at 3 × 10^8 m/s gives 240 to 270 ms.

</details>

**Q41.** `Medium`  
Given below are two statements.  
Statement I: LEO satellites give lower propagation delay than GEO satellites.  
Statement II: A LEO system needs fewer satellites than a GEO system for global coverage.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — LEO footprints are small and the satellites move quickly, so many satellites and frequent handoffs are needed.

</details>

**Q42.** `Medium`  
The equipment on a satellite that receives the uplink signal, amplifies it, changes its frequency and retransmits it on the downlink is the

(1) multiplexer  
(2) duplexer  
(3) transponder  
(4) footprint  

<details><summary>Answer</summary>

**(3)** — The uplink frequency is higher than the downlink frequency to avoid interference.

</details>

**Q43.** `High`  
The Global Positioning System nominally consists of

(1) 3 geostationary satellites  
(2) 24 satellites in 6 orbital planes  
(3) 12 satellites in 3 orbital planes  
(4) 66 satellites in 6 orbital planes  

<details><summary>Answer</summary>

**(2)** — GPS satellites are in MEO at about 20,200 km.

</details>

**Q44.** `High`  
The minimum number of GPS satellites that a receiver needs in order to compute its three-dimensional position and correct its clock is

(1) 6  
(2) 2  
(3) 4  
(4) 3  

<details><summary>Answer</summary>

**(3)** — Three ranges give position (trilateration); the fourth resolves the receiver clock error.

</details>

**Q45.** `Medium`  
GPS determines the position of a receiver by

(1) measuring signal strength of cell towers  
(2) trilateration using distances derived from signal travel times  
(3) Doppler shift only  
(4) triangulation using angles of arrival  

<details><summary>Answer</summary>

**(2)** — Each range is the travel time multiplied by the speed of light.

</details>

**Q46.** `Medium`  
Which of the following is a network-based wireless geolocation technique used in cellular systems?

(1) Frequency reuse  
(2) Slow start  
(3) Time difference of arrival (TDOA)  
(4) Bit stuffing  

<details><summary>Answer</summary>

**(3)** — TDOA, angle of arrival and cell-ID are common network-based positioning methods.

</details>

**Q47.** `Medium`  
Which of the following has the shortest range?

(1) WiMAX  
(2) Wi-Fi  
(3) Bluetooth  
(4) NFC  

<details><summary>Answer</summary>

**(4)** — Near-field communication works over about 4 cm or less.

</details>

**Q48.** `Medium`  
WAP (Wireless Application Protocol) uses which markup language for content on small-screen devices?

(1) HTML  
(2) SGML  
(3) WML  
(4) XAML  

<details><summary>Answer</summary>

**(3)** — Wireless Markup Language organises content into decks and cards.

</details>

**Q49.** `Medium`  
In first-generation analog cellular systems such as AMPS, the multiple access technique used was

(1) TDMA  
(2) CDMA  
(3) FDMA  
(4) OFDMA  

<details><summary>Answer</summary>

**(3)** — Each call was given its own 30 kHz frequency channel.

</details>

**Q50.** `Medium`  
Why are cells in a cellular network modelled as hexagons?

(1) A hexagon approximates a circle and tiles a plane without gaps or overlaps  
(2) Antennas radiate in a hexagonal pattern  
(3) Hexagons need the least transmission power  
(4) It is required by the GSM standard  

<details><summary>Answer</summary>

**(1)** — Among shapes that tessellate, the hexagon covers the largest area for a given radius.

</details>

**Q51.** `Medium`  
Interference between cells that use the same set of frequencies is called

(1) adjacent-channel interference  
(2) crosstalk  
(3) intersymbol interference  
(4) co-channel interference  

<details><summary>Answer</summary>

**(4)** — It is controlled by the reuse distance, not by raising transmit power.

</details>

**Q52.** `Medium`  
Which of the following is a feature of 5G networks?  
A. Millimetre-wave bands  B. Massive MIMO  C. Network slicing  D. Circuit-switched voice core  
Choose the correct answer from the options given below:

(1) B, C and D only  
(2) A, B and C only  
(3) A and D only  
(4) A, B, C and D  

<details><summary>Answer</summary>

**(2)** — 4G and 5G cores are all-IP and packet-switched.

</details>

**Q53.** `Low`  
The 2.4 GHz band used by Wi-Fi and Bluetooth is part of the

(1) licensed cellular band  
(2) C band  
(3) Ku band  
(4) ISM (industrial, scientific and medical) band  

<details><summary>Answer</summary>

**(4)** — ISM bands are unlicensed.

</details>

**Q54.** `Medium`  
In IEEE 802.11, a station that hears an RTS or CTS frame sets its ____ and defers access for the indicated duration.

(1) backoff counter to zero  
(2) beacon interval  
(3) network allocation vector (NAV)  
(4) contention window  

<details><summary>Answer</summary>

**(3)** — The NAV implements virtual carrier sensing.

</details>
