# Paper 1 · Unit 8 — Information & Communication Technology (ICT)

**Expected questions: ~5 (10 marks) · Target: 5/5 — easiest unit for a CS candidate**

## Syllabus Checklist
- [ ] ICT: general abbreviations and terminology
- [ ] Basics of Internet, Intranet, E-mail, Audio and Video-conferencing
- [ ] Digital initiatives in higher education
- [ ] ICT and Governance

---

## 1. Computer Basics

```mermaid
flowchart LR
    I[Input<br/>keyboard, mouse, scanner] --> CPU
    subgraph CPU[Central Processing Unit]
        CU[Control Unit]
        ALU[Arithmetic Logic Unit]
        REG[Registers]
    end
    CPU <--> MEM[Primary memory<br/>RAM, ROM, Cache]
    CPU --> O[Output<br/>monitor, printer]
    MEM <--> SEC[Secondary storage<br/>HDD, SSD, Pen drive]
```

### Memory hierarchy (fast/costly at top)
```
          ┌──────────┐  Registers
          │          │
        ┌─┴──────────┴─┐  Cache (SRAM)
        │              │
      ┌─┴──────────────┴─┐  Main memory (DRAM)
      │                  │
    ┌─┴──────────────────┴─┐  SSD / HDD
    │                      │
  ┌─┴──────────────────────┴─┐  Optical / Tape
  └──────────────────────────┘  slowest, cheapest, largest
```

### Units
```
1 nibble = 4 bits     1 byte = 8 bits
1 KB = 2^10 B   1 MB = 2^20 B   1 GB = 2^30 B   1 TB = 2^40 B
1 PB = 2^50 B   1 EB = 2^60 B   1 ZB = 2^70 B   1 YB = 2^80 B
```

### Number Systems (frequent question!)
- Binary (2), Octal (8), Decimal (10), Hexadecimal (16).
- (25)₁₀ = (11001)₂ = (31)₈ = (19)₁₆
- (1010.101)₂ = 10.625
- Group 3 bits → octal, 4 bits → hex.

## 2. Abbreviations (must know)

| Abbr. | Full form |
|------|-----------|
| ALU | Arithmetic Logic Unit |
| BIOS | Basic Input Output System |
| CMOS | Complementary Metal Oxide Semiconductor |
| DNS | Domain Name System |
| DHCP | Dynamic Host Configuration Protocol |
| FTP | File Transfer Protocol |
| HTML | HyperText Markup Language |
| HTTP(S) | HyperText Transfer Protocol (Secure) |
| IMAP | Internet Message Access Protocol |
| ISP | Internet Service Provider |
| LAN/MAN/WAN | Local/Metropolitan/Wide Area Network |
| MODEM | Modulator–Demodulator |
| OCR / OMR / MICR | Optical Character / Optical Mark / Magnetic Ink Character Recognition |
| POP3 | Post Office Protocol v3 |
| SMTP | Simple Mail Transfer Protocol |
| TCP/IP | Transmission Control Protocol / Internet Protocol |
| URL | Uniform Resource Locator |
| VoIP | Voice over Internet Protocol |
| VPN | Virtual Private Network |
| Wi-Fi | Wireless Fidelity |
| GIF, JPEG, PNG | Graphics Interchange Format, Joint Photographic Experts Group, Portable Network Graphics |
| PDF | Portable Document Format |
| CC / BCC | Carbon Copy / Blind Carbon Copy |
| IoT | Internet of Things |
| LMS | Learning Management System (Moodle) |
| NIC | National Informatics Centre |
| CERT-In | Indian Computer Emergency Response Team |

## 3. Internet, Intranet, Extranet

```mermaid
flowchart LR
    subgraph Org[Organisation]
        IN[Intranet<br/>private, employees only]
    end
    EX[Extranet<br/>intranet + selected partners] --- IN
    IN --- FW[Firewall]
    FW --- NET((Internet<br/>public, global))
```

- **Internet** originated from **ARPANET (1969)**, US DoD. **WWW** invented by **Tim Berners-Lee (1989, CERN)**.
- India's first: **ERNET (1986)**; public internet by **VSNL on 15 Aug 1995**.
- IPv4 = 32 bits; IPv6 = 128 bits. Domain types: .com, .org, .edu, .gov, .ac.in, .nic.in.
- Browser = client software (Chrome, Firefox); Search engine = website (Google, Bing).
- **Cookies** = small data files stored by websites in the browser.

## 4. E-mail

```mermaid
sequenceDiagram
    participant A as Sender client
    participant S1 as Sender mail server
    participant S2 as Receiver mail server
    participant B as Receiver client
    A->>S1: SMTP (send)
    S1->>S2: SMTP (relay)
    B->>S2: POP3 / IMAP (retrieve)
```

- **SMTP** = sending (port 25/587); **POP3** = download & delete (110); **IMAP** = sync, mail stays on server (143).
- First email: **Ray Tomlinson (1971)**, introduced `@`.
- **BCC** recipients are hidden from others. **Spam** = unsolicited mail. **Phishing** = fraudulent mail to steal data.
- Attachments: MIME (Multipurpose Internet Mail Extensions).

## 5. Audio & Video Conferencing
- Real-time communication over IP: Zoom, Google Meet, Microsoft Teams, Webex; government: **JioMeet, Bharat VC (NIC's)**.
- Protocols: **H.323**, **SIP** (Session Initiation Protocol), RTP. Codecs compress audio/video.
- Synchronous (live) vs asynchronous (recorded, forums, email) learning.
- Webinar = web seminar; Podcast = audio episodes; Vodcast = video podcast.

## 6. Digital Initiatives in Higher Education

| Initiative | Purpose |
|-----------|---------|
| SWAYAM | MOOCs (2017) |
| SWAYAM PRABHA | DTH educational TV channels |
| NDL India | National Digital Library (IIT Kharagpur) |
| e-PG Pathshala | PG e-content (UGC/INFLIBNET) |
| Shodhganga / Shodhgangotri | Theses / synopses repository |
| e-ShodhSindhu | E-journal consortium (merged UGC-INFONET, N-LIST, INDEST) |
| **ONOS (One Nation One Subscription)** | Nation-wide access to scholarly journals (2024/25) |
| NAD / DigiLocker | National Academic Depository — digital certificates |
| **ABC** | Academic Bank of Credits (NEP 2020) |
| **NIRF** | National Institutional Ranking Framework (2015) |
| AISHE | All India Survey on Higher Education |
| Virtual Labs, Spoken Tutorial, e-Yantra, FOSSEE | Lab/skill initiatives |
| SAMARTH | e-Governance suite for universities |
| VIDWAN | Database of experts (INFLIBNET) |
| PM e-VIDYA | Multi-mode access to digital education (2020) |
| NEAT | National Educational Alliance for Technology (AICTE, AI-based adaptive learning) |
| DIKSHA | Teachers' platform |

## 7. ICT & Governance

```mermaid
flowchart LR
    G2C[Government to Citizen<br/>UMANG, DigiLocker, passport seva]
    G2B[Government to Business<br/>GeM, GSTN, MCA21]
    G2G[Government to Government<br/>e-Office, PFMS]
    G2E[Government to Employee<br/>e-HRMS]
```
- **Digital India** (1 July 2015) — 9 pillars incl. broadband highways, e-Kranti, Information for All.
- Key platforms: **UMANG** (unified app), **DigiLocker**, **GeM** (Government e-Marketplace), **BHIM-UPI** (NPCI), **CoWIN**, **MyGov**, **e-Hospital**, **Bhashini** (language AI).
- **IT Act 2000** (amended 2008) — legal recognition of e-records & digital signatures; Sec 66A struck down (Shreya Singhal, 2015). **DPDP Act 2023**.
- Cyber security: firewall, antivirus, encryption, 2FA. Malware: virus (needs host), worm (self-replicating), Trojan (disguised), ransomware, spyware.

---

## Previous Year Questions (PYQ pattern)

1. (1011)₂ + (0111)₂ = ? → **(10010)₂**
2. (237)₈ in decimal = 2×64+3×8+7 = **159**
3. 1 TB equals: **1024 GB**
4. Which protocol is used to send e-mail? **SMTP**
5. Which protocol keeps mail on the server and syncs folders? **IMAP**
6. BCC stands for: **Blind Carbon Copy**
7. Which is NOT an input device? (a) scanner (b) light pen (c) plotter (d) OMR — **Ans: (c)**
8. WWW was invented by: **Tim Berners-Lee**
9. The internet originated from: **ARPANET**
10. Private network inside an organisation using internet technology: **Intranet**
11. URL stands for: **Uniform Resource Locator**
12. Which is a volatile memory? **RAM**
13. Which converts domain names to IP addresses? **DNS**
14. IPv6 address length: **128 bits**
15. "Academic Bank of Credits" is an initiative under: **NEP 2020**
16. The portal providing Indian theses: **Shodhganga**
17. The national ranking framework for HEIs: **NIRF**
18. Which is a G2B service? **GeM / GSTN**
19. Malware that replicates itself without a host program: **Worm**
20. Fraudulent attempt to obtain credentials via email: **Phishing**
21. Video conferencing protocol: **H.323 / SIP**
22. The Information Technology Act was passed in: **2000**
23. Arrange in increasing order of capacity: **KB < MB < GB < TB < PB**

## Quick Revision Box
- SMTP send · POP3 download · IMAP sync
- ARPANET 1969 · WWW 1989 (Berners-Lee) · India public internet 1995 (VSNL)
- IT Act 2000 · Digital India 2015 · DPDP Act 2023
