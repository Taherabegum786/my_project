# Set 4 — Transport Layer, Application Layer Protocols and the World Wide Web

**58 questions** — High: 22, Medium: 35, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
The sizes of the UDP header and the minimum TCP header are respectively

(1) 20 bytes and 8 bytes  
(2) 8 bytes and 40 bytes  
(3) 20 bytes and 20 bytes  
(4) 8 bytes and 20 bytes  

<details><summary>Answer</summary>

**(4)** — UDP has a fixed 8-byte header; TCP's header is 20 to 60 bytes.

</details>

**Q2.** `High`  
Match List I with List II.  
List I (Protocol): A. FTP (control)  B. SMTP  C. DNS  D. HTTPS  
List II (Well-known port): I. 53  II. 443  III. 21  IV. 25

(1) A-III, B-I, C-IV, D-II  
(2) A-III, B-IV, C-I, D-II  
(3) A-III, B-IV, C-II, D-I  
(4) A-IV, B-III, C-I, D-II  

<details><summary>Answer</summary>

**(2)** — FTP control 21, SMTP 25, DNS 53, HTTPS 443.

</details>

**Q3.** `High`  
Match List I with List II.  
List I (Protocol): A. Telnet  B. SSH  C. POP3  D. IMAP  
List II (Well-known port): I. 143  II. 110  III. 22  IV. 23

(1) A-IV, B-III, C-II, D-I  
(2) A-II, B-III, C-IV, D-I  
(3) A-IV, B-III, C-I, D-II  
(4) A-III, B-IV, C-II, D-I  

<details><summary>Answer</summary>

**(1)** — Telnet 23, SSH 22, POP3 110, IMAP 143.

</details>

**Q4.** `High`  
Which of the following application layer protocols normally use UDP as the transport protocol?  
A. DNS  B. SMTP  C. TFTP  D. SNMP  E. HTTP/1.1  
Choose the correct answer from the options given below:

(1) B and E only  
(2) A, C, D and E only  
(3) A, C and D only  
(4) A, B and C only  

<details><summary>Answer</summary>

**(3)** — DNS, TFTP and SNMP run over UDP; SMTP and HTTP/1.1 use TCP.

</details>

**Q5.** `High`  
The range of well-known port numbers is

(1) 0 to 255  
(2) 1024 to 49151  
(3) 49152 to 65535  
(4) 0 to 1023  

<details><summary>Answer</summary>

**(4)** — Well-known 0–1023, registered 1024–49151, dynamic/ephemeral 49152–65535.

</details>

**Q6.** `High`  
Arrange the segments exchanged during TCP connection establishment in the correct order.  
A. ACK  B. SYN  C. SYN + ACK

(1) B, C, A  
(2) A, B, C  
(3) B, A, C  
(4) C, B, A  

<details><summary>Answer</summary>

**(1)** — Three-way handshake: SYN, SYN+ACK, ACK.

</details>

**Q7.** `High`  
A TCP receiver gets a segment with sequence number 5000 carrying 1000 bytes of data, and all earlier bytes have been received. The acknowledgement number it sends is

(1) 5000  
(2) 5999  
(3) 6001  
(4) 6000  

<details><summary>Answer</summary>

**(4)** — TCP acknowledges the next byte expected: 5000 + 1000 = 6000.

</details>

**Q8.** `High`  
A TCP connection starts in slow start with a congestion window of 1 MSS and a slow-start threshold of 8 MSS. If no loss occurs, the congestion window during the 6th transmission round is

(1) 16 MSS  
(2) 12 MSS  
(3) 32 MSS  
(4) 10 MSS  

<details><summary>Answer</summary>

**(4)** — Rounds: 1, 2, 4, 8 (threshold reached), then additive increase: 9, 10.

</details>

**Q9.** `High`  
A TCP Tahoe sender has a congestion window of 24 MSS when a timeout occurs. The new values of the slow-start threshold and the congestion window are

(1) 12 MSS and 1 MSS  
(2) 12 MSS and 12 MSS  
(3) 12 MSS and 15 MSS  
(4) 24 MSS and 1 MSS  

<details><summary>Answer</summary>

**(1)** — On timeout ssthresh becomes half the current window and cwnd restarts from 1 MSS.

</details>

**Q10.** `High`  
In TCP Reno, on receiving three duplicate acknowledgements the sender

(1) closes the connection  
(2) sets the congestion window to 1 MSS and enters slow start  
(3) halves the congestion window and continues with congestion avoidance (fast recovery)  
(4) doubles the congestion window  

<details><summary>Answer</summary>

**(3)** — Reno performs fast retransmit followed by fast recovery instead of slow start.

</details>

**Q11.** `High`  
TCP's congestion control in the congestion avoidance phase follows

(1) multiplicative increase, additive decrease  
(2) multiplicative increase, multiplicative decrease  
(3) additive increase, additive decrease  
(4) additive increase, multiplicative decrease  

<details><summary>Answer</summary>

**(4)** — AIMD: the window grows by 1 MSS per RTT and is halved on loss.

</details>

**Q12.** `High`  
The actual size of the TCP sender's window is

(1) the maximum of the congestion window and the receiver's advertised window  
(2) the receiver's advertised window  
(3) the minimum of the congestion window and the receiver's advertised window  
(4) the congestion window  

<details><summary>Answer</summary>

**(3)** — The sender must respect both flow control (rwnd) and congestion control (cwnd).

</details>

**Q13.** `Medium`  
The estimated RTT of a TCP connection is 100 ms. A new RTT sample of 140 ms is measured. With α = 0.125, the new estimated RTT is

(1) 135 ms  
(2) 105 ms  
(3) 110 ms  
(4) 120 ms  

<details><summary>Answer</summary>

**(2)** — EstimatedRTT = 0.875 × 100 + 0.125 × 140 = 105 ms.

</details>

**Q14.** `Medium`  
Match List I with List II.  
List I (Algorithm): A. Nagle's algorithm  B. Clark's solution  C. Karn's algorithm  
List II (Purpose): I. Receiver-side remedy for silly window syndrome  II. Excludes retransmitted segments from RTT estimation  III. Sender-side remedy for silly window syndrome

(1) A-II, B-I, C-III  
(2) A-III, B-II, C-I  
(3) A-I, B-III, C-II  
(4) A-III, B-I, C-II  

<details><summary>Answer</summary>

**(4)** — Nagle acts at the sender, Clark at the receiver; Karn's algorithm handles the retransmission ambiguity.

</details>

**Q15.** `Medium`  
The sizes of the sequence number field and the window size field in the TCP header are

(1) 16 bits and 16 bits  
(2) 16 bits and 32 bits  
(3) 32 bits and 32 bits  
(4) 32 bits and 16 bits  

<details><summary>Answer</summary>

**(4)** — Sequence and acknowledgement numbers are 32 bits; the advertised window is 16 bits.

</details>

**Q16.** `Medium`  
Which TCP flag is used to abort a connection abruptly?

(1) PSH  
(2) URG  
(3) RST  
(4) FIN  

<details><summary>Answer</summary>

**(3)** — RST resets the connection; FIN performs a graceful close.

</details>

**Q17.** `Medium`  
A socket address is the combination of

(1) a port number and a protocol number  
(2) a MAC address and an IP address  
(3) a MAC address and a port number  
(4) an IP address and a port number  

<details><summary>Answer</summary>

**(4)** — IP address identifies the host and the port identifies the process.

</details>

**Q18.** `Medium`  
Given below are two statements.  
Statement I: TCP is a byte-stream-oriented protocol that numbers every byte it transmits.  
Statement II: UDP provides flow control and congestion control but no error control.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — UDP offers no flow or congestion control; it has only an optional checksum.

</details>

**Q19.** `Medium`  
The pseudo-header used in the computation of the TCP and UDP checksums contains

(1) the source and destination port numbers  
(2) the source and destination IP addresses, the protocol number and the segment length  
(3) the sequence and acknowledgement numbers  
(4) the MAC addresses of sender and receiver  

<details><summary>Answer</summary>

**(2)** — The pseudo-header guards against misdelivered datagrams.

</details>

**Q20.** `Medium`  
A SYN flooding attack exploits

(1) the fragmentation mechanism of IP  
(2) the three-way handshake of TCP  
(3) the checksum of UDP  
(4) the four-way connection termination of TCP  

<details><summary>Answer</summary>

**(2)** — The attacker sends many SYNs with spoofed addresses, exhausting the server's half-open connection table.

</details>

**Q21.** `Medium`  
Which of the following features is provided by SCTP but not by TCP?

(1) Reliable delivery  
(2) Multihoming and multiple streams per association  
(3) Connection-oriented service  
(4) Congestion control  

<details><summary>Answer</summary>

**(2)** — SCTP is message-oriented and supports multistreaming and multihoming.

</details>

**Q22.** `High`  
Which of the following statements about HTTP is correct?

(1) HTTP is a stateful protocol that uses UDP  
(2) HTTP is a push protocol  
(3) HTTP uses two parallel TCP connections for control and data  
(4) HTTP is a stateless protocol that uses TCP port 80  

<details><summary>Answer</summary>

**(4)** — HTTP itself keeps no client state; cookies are used to add state.

</details>

**Q23.** `High`  
A web page consists of a base HTML file and 10 embedded images on the same server. Using non-persistent HTTP without parallel connections, how many TCP connections are needed?

(1) 1  
(2) 2  
(3) 10  
(4) 11  

<details><summary>Answer</summary>

**(4)** — Non-persistent HTTP opens a separate connection for each of the 11 objects.

</details>

**Q24.** `High`  
In non-persistent HTTP, the time needed to fetch one small object (ignoring transmission time), where RTT is the round-trip time, is approximately

(1) 2 RTT  
(2) 3 RTT  
(3) 4 RTT  
(4) 1 RTT  

<details><summary>Answer</summary>

**(1)** — One RTT to set up the TCP connection and one RTT for the request and response.

</details>

**Q25.** `High`  
Match List I with List II.  
List I (HTTP status code): A. 200  B. 301  C. 404  D. 500  
List II (Meaning): I. Not found  II. Internal server error  III. OK  IV. Moved permanently

(1) A-IV, B-III, C-I, D-II  
(2) A-III, B-IV, C-I, D-II  
(3) A-III, B-I, C-IV, D-II  
(4) A-III, B-IV, C-II, D-I  

<details><summary>Answer</summary>

**(2)** — 2xx success, 3xx redirection, 4xx client error, 5xx server error.

</details>

**Q26.** `Medium`  
Which HTTP method retrieves only the headers of a resource, without the body?

(1) PUT  
(2) HEAD  
(3) GET  
(4) POST  

<details><summary>Answer</summary>

**(2)** — HEAD is identical to GET except that the server does not return a message body.

</details>

**Q27.** `Medium`  
Which mechanism lets a web server recognise a returning user even though HTTP is stateless?

(1) Three-way handshake  
(2) DNS caching  
(3) MIME  
(4) Cookies  

<details><summary>Answer</summary>

**(4)** — A cookie stored by the browser is sent back with each later request to the same server.

</details>

**Q28.** `High`  
Which of the following statements about FTP is correct?

(1) FTP uses a single connection for both control and data  
(2) FTP runs over UDP port 69  
(3) FTP uses TCP port 21 for control and TCP port 20 for data  
(4) FTP is a stateless protocol  

<details><summary>Answer</summary>

**(3)** — FTP sends control information out-of-band on a separate connection and maintains user state.

</details>

**Q29.** `High`  
Given below are two statements.  
Statement I: SMTP is a push protocol used to transfer mail from the sender's mail server to the receiver's mail server.  
Statement II: POP3 and IMAP are pull protocols used by a user agent to retrieve mail from the mail server.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — SMTP pushes mail; message access agents pull it.

</details>

**Q30.** `Medium`  
Which protocol allows non-ASCII data such as images and audio to be sent through e-mail?

(1) ICMP  
(2) SNMP  
(3) POP3  
(4) MIME  

<details><summary>Answer</summary>

**(4)** — MIME converts non-ASCII data to 7-bit ASCII (e.g. Base64) for SMTP.

</details>

**Q31.** `High`  
Match List I with List II.  
List I (DNS resource record): A. A  B. AAAA  C. MX  D. CNAME  
List II (Meaning): I. Mail exchanger for the domain  II. Alias (canonical name) mapping  III. IPv4 address of a host  IV. IPv6 address of a host

(1) A-IV, B-III, C-I, D-II  
(2) A-III, B-IV, C-I, D-II  
(3) A-I, B-IV, C-III, D-II  
(4) A-III, B-IV, C-II, D-I  

<details><summary>Answer</summary>

**(2)** — A: IPv4, AAAA: IPv6, MX: mail server, CNAME: alias.

</details>

**Q32.** `High`  
The Domain Name System normally uses

(1) UDP port 67  
(2) TCP port 53 for all messages  
(3) TCP port 80  
(4) UDP port 53 for queries and TCP port 53 for zone transfers and large responses  

<details><summary>Answer</summary>

**(4)** — Ordinary queries use UDP; responses that do not fit and zone transfers use TCP.

</details>

**Q33.** `Medium`  
In a recursive DNS query

(1) the queried server takes responsibility for resolving the name completely and returns the final answer  
(2) the client contacts each name server in turn  
(3) no caching is done  
(4) only root servers are contacted  

<details><summary>Answer</summary>

**(1)** — In an iterative query the server instead returns a referral to another server.

</details>

**Q34.** `Medium`  
Which DNS record type is used for reverse lookup, i.e. mapping an IP address to a name?

(1) NS  
(2) SOA  
(3) PTR  
(4) TXT  

<details><summary>Answer</summary>

**(3)** — PTR records in the in-addr.arpa domain support inverse resolution.

</details>

**Q35.** `Medium`  
In SNMP, the collection of managed objects maintained by an agent is called the

(1) ASN  
(2) SMI  
(3) PDU  
(4) MIB  

<details><summary>Answer</summary>

**(4)** — The Management Information Base is the agent's virtual database; SMI defines the rules for naming objects.

</details>

**Q36.** `Medium`  
SNMP agents listen on UDP port 161, and managers receive trap messages on UDP port

(1) 160  
(2) 514  
(3) 163  
(4) 162  

<details><summary>Answer</summary>

**(4)** — Port 161 for requests to agents, 162 for traps sent to the manager.

</details>

**Q37.** `Medium`  
Which of the following provides secure remote login and has replaced Telnet?

(1) FTP  
(2) SNMP  
(3) SSH  
(4) TFTP  

<details><summary>Answer</summary>

**(3)** — SSH encrypts the session; Telnet sends everything, including passwords, in plain text.

</details>

**Q38.** `High`  
Arrange the following system calls in the order in which a TCP server invokes them.  
A. listen()  B. socket()  C. accept()  D. bind()

(1) B, A, D, C  
(2) B, D, C, A  
(3) B, D, A, C  
(4) D, B, A, C  

<details><summary>Answer</summary>

**(3)** — socket, bind, listen, accept.

</details>

**Q39.** `Medium`  
The World Wide Web was invented by

(1) Vint Cerf at DARPA  
(2) Tim Berners-Lee at CERN  
(3) Robert Metcalfe at Xerox PARC  
(4) Ray Tomlinson at BBN  

<details><summary>Answer</summary>

**(2)** — Berners-Lee proposed the Web at CERN in 1989.

</details>

**Q40.** `Medium`  
In the URL http://www.example.org:8080/docs/index.html, the component 8080 is the

(1) host  
(2) protocol  
(3) port number  
(4) path  

<details><summary>Answer</summary>

**(3)** — A URL has the form protocol://host:port/path.

</details>

**Q41.** `Medium`  
Match List I with List II.  
List I (Type of web document): A. Static document  B. Dynamic document  C. Active document  
List II (Description): I. A program run at the client site, e.g. a Java applet or script  II. Fixed-content file stored on the server  III. Created by the server on each request, e.g. using CGI

(1) A-II, B-I, C-III  
(2) A-II, B-III, C-I  
(3) A-III, B-II, C-I  
(4) A-I, B-III, C-II  

<details><summary>Answer</summary>

**(2)** — Static: fixed; dynamic: generated at the server; active: executed at the client.

</details>

**Q42.** `Medium`  
A proxy server (web cache) improves performance by

(1) compressing the TCP headers  
(2) keeping copies of recently requested objects and serving them locally  
(3) assigning IP addresses dynamically  
(4) encrypting the HTTP messages  

<details><summary>Answer</summary>

**(2)** — A cache hit avoids contacting the origin server, reducing response time and traffic.

</details>

**Q43.** `Medium`  
Which HTTP request header and status code are used by a cache to verify that its stored copy is still up to date?

(1) Range and 404 Not Found  
(2) Host and 200 OK  
(3) Cookie and 401 Unauthorized  
(4) If-Modified-Since and 304 Not Modified  

<details><summary>Answer</summary>

**(4)** — A conditional GET returns 304 with no body if the object is unchanged.

</details>

**Q44.** `Medium`  
Given below are two statements.  
Statement I: HTTP/1.1 uses persistent connections by default.  
Statement II: HTTPS is HTTP running over TLS/SSL and uses port 443 by default.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Both statements are true.

</details>

**Q45.** `Medium`  
Which protocol is used to synchronise the clocks of computers over a network?

(1) RTP  
(2) NTP  
(3) SNMP  
(4) NNTP  

<details><summary>Answer</summary>

**(2)** — The Network Time Protocol runs on UDP port 123.

</details>

**Q46.** `Medium`  
Real-time Transport Protocol (RTP), used for audio and video streaming, normally runs over

(1) UDP  
(2) ICMP  
(3) ARP  
(4) TCP  

<details><summary>Answer</summary>

**(1)** — Timeliness matters more than reliability for real-time media, so RTP uses UDP.

</details>

**Q47.** `Medium`  
TFTP differs from FTP in that TFTP

(1) uses UDP port 69 and provides no authentication  
(2) supports directory listing  
(3) uses two connections  
(4) uses TCP port 21  

<details><summary>Answer</summary>

**(1)** — TFTP is a minimal file transfer protocol over UDP.

</details>

**Q48.** `Medium`  
Which of the following correctly orders the steps taken when a user types a URL into a browser for the first time?  
A. TCP connection establishment  B. DNS lookup of the host name  C. HTTP request  D. HTTP response

(1) C, B, A, D  
(2) A, B, C, D  
(3) B, A, C, D  
(4) B, C, A, D  

<details><summary>Answer</summary>

**(3)** — The name is resolved first, then the connection is set up, then request and response.

</details>

**Q49.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: DNS uses UDP for ordinary name queries.  
Reason R: A query and its response are short, and avoiding connection set-up reduces the delay.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — The low overhead of UDP suits short request-response exchanges.

</details>

**Q50.** `Medium`  
In TCP, each of the SYN and FIN segments

(1) consumes one sequence number  
(2) consumes as many sequence numbers as the window size  
(3) consumes no sequence number  
(4) cannot carry an acknowledgement  

<details><summary>Answer</summary>

**(1)** — SYN and FIN each consume one sequence number even though they carry no data.

</details>

**Q51.** `Medium`  
The maximum size of a TCP receive window without the window scaling option is

(1) 1024 bytes  
(2) 4 GB  
(3) 1 MB  
(4) 65,535 bytes  

<details><summary>Answer</summary>

**(4)** — The window field is 16 bits wide.

</details>

**Q52.** `Medium`  
Which transport-layer function allows several application processes on one host to share the network using port numbers?

(1) Multiplexing and demultiplexing  
(2) Flow control  
(3) Congestion control  
(4) Segmentation  

<details><summary>Answer</summary>

**(1)** — Ports let the transport layer multiplex at the sender and demultiplex at the receiver.

</details>

**Q53.** `Medium`  
In IMAP, unlike POP3

(1) mail is sent from client to server  
(2) mail is always deleted from the server after download  
(3) UDP is used  
(4) a user can organise mail in folders on the server and download only headers  

<details><summary>Answer</summary>

**(4)** — IMAP keeps mail on the server and supports folders and partial fetch.

</details>

**Q54.** `Medium`  
Which of the following is a markup language used to describe the structure and transport of data rather than its presentation?

(1) CSS  
(2) JavaScript  
(3) XML  
(4) HTML  

<details><summary>Answer</summary>

**(3)** — XML defines user-defined tags for describing data; HTML describes how to display it.

</details>

**Q55.** `Medium`  
The HTTP status code 403 indicates

(1) Service unavailable  
(2) Forbidden  
(3) Unauthorized  
(4) Bad request  

<details><summary>Answer</summary>

**(2)** — 400 Bad Request, 401 Unauthorized, 403 Forbidden, 503 Service Unavailable.

</details>

**Q56.** `Low`  
HTTP/3 runs over which transport protocol?

(1) QUIC over UDP  
(2) SCTP  
(3) DCCP  
(4) TCP  

<details><summary>Answer</summary>

**(1)** — HTTP/3 replaces TCP with QUIC, which is built on UDP.

</details>

**Q57.** `Medium`  
Which of the following is a peer-to-peer file sharing protocol in which a file is divided into chunks exchanged among a swarm of peers?

(1) SMTP  
(2) BitTorrent  
(3) NFS  
(4) FTP  

<details><summary>Answer</summary>

**(2)** — BitTorrent peers trade chunks using a tit-for-tat strategy, coordinated by a tracker or DHT.

</details>

**Q58.** `Medium`  
Which of the following is NOT a service provided by TCP?

(1) Full-duplex communication  
(2) Guaranteed minimum bandwidth  
(3) Flow control  
(4) Reliable in-order delivery  

<details><summary>Answer</summary>

**(2)** — TCP offers no timing or bandwidth guarantees.

</details>
