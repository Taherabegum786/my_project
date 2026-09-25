"""Generates Course_Plan_CNS_Lab.pdf — unit-wise course plan."""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, ListFlowable, ListItem, KeepTogether)

COURSE = "CRYPTOGRAPHY &amp; NETWORK SECURITY LAB"
FACULTY = "Dr. K. Venkata Ramana"
OUT = __file__.replace("build_course_plan.py", "Course_Plan_CNS_Lab.pdf")

R, BD = "Times-Roman", "Times-Bold"
def st(name, size, font=R, align=0, **kw):
    return ParagraphStyle(name, fontName=font, fontSize=size, leading=size * 1.25, alignment=align, **kw)

CELL, CELLC, HEAD = st("cell", 9), st("cellc", 9, align=TA_CENTER), st("head", 9, BD)
BODY = st("body", 9.5)
UNIT_H = st("unit", 11.5, BD, spaceBefore=6, spaceAfter=3, keepWithNext=1)

# (topic, hours, mode of teaching, learning activity)
UNITS = [
    ("I", "Bitwise Operations and Classical Ciphers", [
        ("Lab introduction and ethics of security testing; C programs to XOR each character of “Hello world” with 0, and to AND, OR and XOR each character with 127", 3, "Lecture / Demonstration", "Observe and explain the effect of each bitwise operation on the output"),
        ("Java programs for encryption and decryption using the Caesar cipher and the Substitution cipher", 3, "Demonstration / Guided Practice", "Encrypt and decrypt messages; attempt a brute-force attack on Caesar"),
        ("Java program for encryption and decryption using the Hill cipher", 3, "Worked Examples / Hands-on Practice", "Compute key-matrix inverse mod 26; verify decryption"),
    ]),
    ("II", "Symmetric Block and Stream Ciphers", [
        ("C/Java program to implement the DES algorithm logic", 3, "Demonstration / Guided Practice", "Trace key generation and one Feistel round"),
        ("C/Java program to implement the Blowfish algorithm logic", 3, "Guided Hands-on Practice", "Implement subkey generation and the F-function"),
        ("C/Java program to implement the Rijndael (AES) algorithm logic", 3, "Worked Examples / Hands-on Practice", "Implement SubBytes, ShiftRows, MixColumns and AddRoundKey"),
        ("RC4 logic in Java; encrypt “Hello world” with Blowfish using Java Cryptography and a key created with Java keytool", 3, "Demonstration / Hands-on Practice", "Generate a key with keytool; use javax.crypto for encryption"),
    ]),
    ("III", "Public-Key Cryptography and Message Digests", [
        ("Java program to implement the RSA algorithm", 3, "Worked Examples / Hands-on Practice", "Generate keys; encrypt and decrypt a message"),
        ("Diffie-Hellman key exchange mechanism using HTML and JavaScript", 3, "Demonstration / Hands-on Practice", "Build a web page showing both parties computing the shared key"),
        ("Message digest of a text using SHA-1 and MD5 in Java", 3, "Guided Hands-on Practice", "Compare digest lengths; observe the avalanche effect"),
    ]),
    ("IV", "Network Security", [
        ("Find the IP address and MAC address of your machine; find neighbouring machines in the network; check if a server is up and running", 3, "Demonstration / Guided Practice", "Use ipconfig/ifconfig, arp, ping and nmap"),
        ("Run the tcpdump / WinDump utility with at least 4 options", 3, "Guided Hands-on Practice", "Capture and filter traffic by host, port and protocol"),
        ("Capture packets using Wireshark and analyse one TCP packet in detail", 3, "Demonstration / Hands-on Practice", "Analyse TCP header fields and the three-way handshake"),
        ("Use Snort to detect intrusion packets; demonstrate ARP poisoning on an isolated lab network", 3, "Case Study / Hands-on Practice", "Write Snort rules and view alerts; observe poisoned ARP tables"),
    ]),
    ("V", "Revision and Assessment", [
        ("Revision, Record Evaluation and Internal Lab Examination", 3, "Viva-voce / Practical Test", "Program execution, record submission and viva"),
    ]),
]

GRID = [("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6E6E6")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]


def unit_table(topics):
    data = [[Paragraph(h, HEAD) for h in ("S.No.", "Experiment / Topic", "Hrs", "Mode of Teaching", "Learning Activity")]]
    for i, (topic, hrs, mode, act) in enumerate(topics, 1):
        data.append([Paragraph(str(i), CELLC), Paragraph(topic, CELL), Paragraph(str(hrs), CELLC),
                     Paragraph(mode, CELL), Paragraph(act, CELL)])
    t = Table(data, colWidths=[12 * mm, 73 * mm, 11 * mm, 35 * mm, 55 * mm], repeatRows=1)
    t.setStyle(TableStyle(GRID))
    return t


story = [Spacer(1, 70 * mm)]
for text, size, font, gap in [("COURSE PLAN", 18, BD, 10), (COURSE, 22, BD, 40),
                              ("Prepared by", 12, R, 4), (FACULTY, 18, BD, 4),
                              ("Department of CSSE", 12, R, 2), ("Andhra University", 12, BD, 0)]:
    story += [Paragraph(text, st("c", size, font, TA_CENTER)), Spacer(1, gap * mm / 2 + 4)]
story.append(PageBreak())

story += [
    Paragraph("<u>UNIT-WISE COURSE PLAN</u>", st("t1", 15, BD, TA_CENTER, spaceAfter=6)),
    Paragraph(f"<u>{COURSE}</u>", st("t2", 11.5, BD, TA_CENTER, spaceAfter=6)),
    Paragraph(f"<b>Total Hours:</b> 45 (15 sessions × 3 hours)", BODY),
    Spacer(1, 3),
    Paragraph("<b>Software / Tools:</b> GCC, JDK (javax.crypto, keytool), web browser, Wireshark, "
              "tcpdump / WinDump, Nmap, Snort, arpspoof / Ettercap; Linux or Windows", BODY),
    Spacer(1, 3),
    Paragraph("<b>Reference Books:</b> (1) William Stallings, <i>Computer Security – Principles and Practices</i>, "
              "2/e, Pearson Education; (2) William Stallings, <i>Cryptography and Network Security</i>, "
              "Pearson Education Asia, New Delhi", BODY),
    Spacer(1, 4),
]

dist = []
for num, name, topics in UNITS:
    hrs = sum(t[1] for t in topics)
    dist.append((num, name, hrs))
    story += [Paragraph(f"UNIT {num}: {name} — {hrs} Hours", UNIT_H), unit_table(topics)]
total = sum(d[2] for d in dist)
assert total == 45, total

data = [[Paragraph(h, st("hc", 9, BD, TA_CENTER)) for h in ("Unit", "Unit Title", "Hours", "Percentage")]]
data += [[Paragraph(n, CELLC), Paragraph(t, CELL), Paragraph(str(h), CELLC),
          Paragraph(f"{h / total * 100:.2f}%", CELLC)] for n, t, h in dist]
data.append(["", Paragraph("<b>GRAND TOTAL</b>", CELL), Paragraph(f"<b>{total}</b>", CELLC),
             Paragraph("<b>100%</b>", CELLC)])
dt = Table(data, colWidths=[16 * mm, 110 * mm, 30 * mm, 30 * mm])
dt.setStyle(TableStyle(GRID))
story += [Paragraph("Overall Hour Distribution", UNIT_H), dt]

modes = [
    "Each laboratory session is of 3 hours: a short briefing/demonstration by the faculty, followed by individual hands-on implementation by students.",
    "Students prepare the algorithm/design before the session, and execute, test and debug the programs during the session.",
    "Cipher outputs are verified by hand on small inputs and against standard library implementations (javax.crypto, MessageDigest).",
    "Network security experiments are carried out only on the isolated lab network, with emphasis on ethical and legal use of the tools.",
    "Guided problem solving for complex experiments; additional exercises are given to fast learners.",
    "Continuous assessment through observation book, lab record, program output and viva-voce in every session.",
    "The final session is for revision, record evaluation and the internal laboratory examination.",
]
story.append(KeepTogether([
    Paragraph("General Modes of Teaching", UNIT_H),
    ListFlowable([ListItem(Paragraph(m, BODY), leftIndent=10) for m in modes],
                 bulletType="bullet", leftIndent=10, bulletFontSize=7),
]))

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=12 * mm, rightMargin=12 * mm,
                        topMargin=12 * mm, bottomMargin=12 * mm,
                        title="Cryptography & Network Security Lab – Course Plan", author=FACULTY)
doc.build(story)
print("wrote", OUT)
