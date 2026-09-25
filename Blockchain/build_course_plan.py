"""Generates Course_Plan_Blockchain_Technology.pdf — unit-wise course plan."""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, ListFlowable, ListItem, KeepTogether)

COURSE = "BLOCKCHAIN TECHNOLOGY"
SUBTITLE = "Open Elective"
FACULTY = "Dr. K. Venkata Ramana"
OUT = __file__.replace("build_course_plan.py", "Course_Plan_Blockchain_Technology.pdf")

R, BD = "Times-Roman", "Times-Bold"
def st(name, size, font=R, align=0, **kw):
    return ParagraphStyle(name, fontName=font, fontSize=size, leading=size * 1.25, alignment=align, **kw)

CELL, CELLC, HEAD = st("cell", 9), st("cellc", 9, align=TA_CENTER), st("head", 9, BD)
BODY = st("body", 9.5)
UNIT_H = st("unit", 11.5, BD, spaceBefore=6, spaceAfter=3, keepWithNext=1)

# (topic, hours, mode of teaching, learning activity)
UNITS = [
    ("I", "Block Chain and its History", [
        ("Course introduction; History of blockchain – from digital cash to Bitcoin; need for blockchain", 1, "Lecture / PPT", "Timeline of key milestones in blockchain history"),
        ("Types of blockchain – public, private, hybrid; comparison with traditional databases", 1, "Lecture / Board", "Compare blockchain types with real-world examples"),
        ("Blockchain Components – blocks, transactions, nodes, peer-to-peer network, ledger", 1, "Lecture / Board", "Label the components of a blockchain network"),
        ("Cryptographic primitives – hash functions, public-key cryptography, digital signatures", 2, "Lecture / Demonstration", "Compute SHA-256 hashes; sign and verify a message"),
        ("Permissioned Blockchain, Permissionless Blockchain and Consortium Blockchain", 2, "Lecture / Case Study", "Classify Hyperledger, Bitcoin, Ethereum and R3 Corda"),
        ("Basics of Consensus Algorithms – need for consensus, Byzantine Generals problem", 1, "Lecture / Think-Pair-Share", "Discuss fault tolerance in distributed agreement"),
        ("Architecture and Properties of Blockchain – immutability, transparency, decentralisation, security", 2, "Lecture / Worked Examples", "Draw layered blockchain architecture; quiz on Unit I"),
    ]),
    ("II", "Decentralization and Consensus Algorithms", [
        ("Decentralization using blockchain; Methods of decentralization – disintermediation, contest-driven", 2, "Lecture / Board", "Identify intermediaries removed by blockchain in given scenarios"),
        ("Routes to decentralization", 1, "Lecture / Discussion", "Map the steps to decentralize a given system"),
        ("Decentralized organizations – DOs, DAOs, DACs, DApps", 1, "Lecture / Case Study", "Study The DAO case and its lessons"),
        ("Distributed systems – CAP theorem, fault tolerance", 1, "Lecture / Worked Examples", "Apply the CAP theorem to example systems"),
        ("Distributed ledger – centralized vs. decentralized vs. distributed ledgers", 1, "Lecture / Board", "Compare ledger models"),
        ("Merkle tree – construction, Merkle root, Merkle proofs", 1, "Demonstration / Problem Solving", "Build a Merkle tree for a set of transactions"),
        ("Structure of a block – block header, nonce, timestamp, previous hash, genesis block", 1, "Demonstration", "Inspect real blocks using a block explorer"),
        ("Consensus Algorithms: Proof of Work – mining, difficulty adjustment, energy cost", 2, "Lecture / Demonstration", "Simulate mining with varying difficulty"),
        ("Proof of Stake and Proof of Burn", 1, "Lecture / Worked Examples", "Compare PoW, PoS and PoB on cost and security"),
        ("Proof of Elapsed Time and Proof of Activity", 1, "Lecture / Worked Examples", "Explain PoET with trusted execution environments"),
        ("Proof of Concept; comparison of consensus algorithms", 1, "Problem Solving / Quiz", "Tabulate consensus algorithms; quiz on Unit II"),
    ]),
    ("III", "Bitcoin and Alternative Coins", [
        ("Bitcoin – overview, keys and addresses, wallets", 1, "Lecture / Demonstration", "Create a test wallet and address"),
        ("Bitcoin Transactions – inputs, outputs, UTXO model, transaction scripts", 2, "Lecture / Demonstration", "Trace a transaction on a block explorer"),
        ("Bitcoin payments; Bitcoin properties", 1, "Lecture / Board", "List properties with supporting examples"),
        ("Transaction life cycle", 1, "Lecture / Worked Examples", "Draw the transaction life cycle"),
        ("Creation of coin – mining reward, halving; Sending payments", 1, "Lecture / Worked Examples", "Calculate block rewards across halving periods"),
        ("Double spending using blockchain", 1, "Lecture / Think-Pair-Share", "Analyse a double-spend attack scenario"),
        ("Bitcoin anonymity – pseudonymity, mixing, de-anonymisation", 1, "Lecture / Discussion", "Discuss privacy risks of public ledgers"),
        ("Ether – Ethercoin properties; comparison of Ether with Bitcoin", 1, "Lecture / Case Study", "Compare Bitcoin and Ether features"),
        ("Alternative Coins; Bitcoin limitations – scalability, energy, privacy", 1, "Lecture / Discussion", "Discuss Bitcoin limitations and solutions"),
        ("Namecoin and Litecoin", 1, "Lecture / Case Study", "Compare with Bitcoin by purpose and consensus"),
        ("Primecoin and Zcash", 1, "Lecture / Case Study", "Study proof-of-work on primes and zero-knowledge proofs"),
        ("Future currencies – CBDCs, stablecoins; creating own crypto token (ERC-20 overview)", 1, "Demonstration / Quiz", "Outline the design of a custom token; quiz on Unit III"),
    ]),
    ("IV", "Ethereum and Smart Contracts", [
        ("Ethereum Architecture – EVM, accounts, transactions", 2, "Lecture / PPT", "Explore accounts and transactions on a test network"),
        ("Ethereum gas, blocks, networks and clients", 1, "Lecture / Demonstration", "Estimate gas costs for sample transactions"),
        ("Solidity programming basics – data types, variables, functions, control structures", 2, "Demonstration / Hands-on", "Write simple Solidity programs in Remix IDE"),
        ("Solidity – mappings, structs, modifiers, events, inheritance", 1, "Demonstration / Hands-on", "Extend programs with modifiers and events"),
        ("Smart Contract – structure, life cycle, common security issues", 2, "Lecture / Worked Examples", "Write a simple storage and voting contract"),
        ("Deploying Smart Contracts – Remix, MetaMask and test networks", 2, "Demonstration / Hands-on", "Deploy a contract to a test network"),
        ("Deploying Smart Contracts with Ganache and Truffle", 1, "Demonstration / Hands-on", "Deploy and test a contract on a local blockchain"),
        ("Integration with UI – Web3.js / Ethers.js, building a simple DApp front end", 2, "Demonstration / Mini Project", "Connect a web page to a deployed contract; assignment"),
    ]),
    ("V", "Blockchain Applications", [
        ("Blockchain outside of currencies; Internet of Things", 1, "Lecture / Case Study", "Study blockchain for IoT device management"),
        ("Government", 1, "Lecture / Case Study", "Discuss e-governance and land records"),
        ("Health", 1, "Lecture / Case Study", "Study sharing of electronic health records"),
        ("Finance", 1, "Lecture / Case Study", "Study cross-border payments, trade finance and DeFi"),
        ("Media", 1, "Lecture / Discussion", "Discuss content ownership and royalties"),
        ("Secure Voting and Digital Identity", 1, "Lecture / Think-Pair-Share", "Design a blockchain-based voting system"),
        ("Real Estate", 1, "Lecture / Case Study", "Study property registration and tokenisation"),
        ("Education", 1, "Lecture / Case Study", "Study certificate verification; quiz on Unit V"),
    ]),
    ("VI", "Revision and Assessment", [
        ("Revision of Units I–III – blockchain basics, consensus, Bitcoin and altcoins", 1, "Tutorial / Discussion", "Solve previous question papers"),
        ("Revision of Units IV–V – Ethereum, smart contracts and applications", 1, "Tutorial / Discussion", "Solve previous question papers"),
        ("Assignment review, slip test and doubt clearance", 1, "Slip Test / Discussion", "Written test and feedback on assignments"),
    ]),
]

GRID = [("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6E6E6")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]


def unit_table(topics):
    data = [[Paragraph(h, HEAD) for h in ("S.No.", "Topic", "Hrs", "Mode of Teaching", "Learning Activity")]]
    for i, (topic, hrs, mode, act) in enumerate(topics, 1):
        data.append([Paragraph(str(i), CELLC), Paragraph(topic, CELL), Paragraph(str(hrs), CELLC),
                     Paragraph(mode, CELL), Paragraph(act, CELL)])
    t = Table(data, colWidths=[12 * mm, 73 * mm, 11 * mm, 35 * mm, 55 * mm], repeatRows=1)
    t.setStyle(TableStyle(GRID))
    return t


story = [Spacer(1, 70 * mm)]
for text, size, font, gap in [("COURSE PLAN", 18, BD, 10), (COURSE, 22, BD, 8), (SUBTITLE, 12, R, 40),
                              ("Prepared by", 12, R, 4), (FACULTY, 18, BD, 4),
                              ("Department of CSSE", 12, R, 2), ("Andhra University", 12, BD, 0)]:
    story += [Paragraph(text, st("c", size, font, TA_CENTER)), Spacer(1, gap * mm / 2 + 4)]
story.append(PageBreak())

story += [
    Paragraph("<u>UNIT-WISE COURSE PLAN</u>", st("t1", 15, BD, TA_CENTER, spaceAfter=6)),
    Paragraph(f"<u>{COURSE}</u>", st("t2", 11.5, BD, TA_CENTER, spaceAfter=6)),
    Paragraph(f"<b>Course Type:</b> {SUBTITLE} &nbsp; | &nbsp; <b>Total Hours:</b> 60 (15 weeks × 4 hours)", BODY),
    Spacer(1, 3),
    Paragraph("<b>Software / Tools:</b> Block explorer, Remix IDE, MetaMask, Ganache / Truffle, "
              "Node.js with Web3.js / Ethers.js", BODY),
    Spacer(1, 3),
    Paragraph("<b>Text Books:</b> (1) Imran Bashir, <i>Mastering Blockchain</i>, 2/e, Packt, 2017; "
              "(2) Narayanan, Bonneau, Felten, Miller, Goldfeder, <i>Bitcoin and Cryptocurrency Technologies</i>, "
              "Princeton University, 2016; (3) Subramanian, George, Abhilash, Karthikeyan, "
              "<i>Blockchain Technology</i>, University Press, 2021", BODY),
    Spacer(1, 4),
]

dist = []
for num, name, topics in UNITS:
    hrs = sum(t[1] for t in topics)
    dist.append((num, name, hrs))
    story += [Paragraph(f"UNIT {num}: {name} — {hrs} Hours", UNIT_H), unit_table(topics)]
total = sum(d[2] for d in dist)
assert total == 60, total

data = [[Paragraph(h, st("hc", 9, BD, TA_CENTER)) for h in ("Unit", "Unit Title", "Hours", "Percentage")]]
data += [[Paragraph(n, CELLC), Paragraph(t, CELL), Paragraph(str(h), CELLC),
          Paragraph(f"{h / total * 100:.2f}%", CELLC)] for n, t, h in dist]
data.append(["", Paragraph("<b>GRAND TOTAL</b>", CELL), Paragraph(f"<b>{total}</b>", CELLC),
             Paragraph("<b>100%</b>", CELLC)])
dt = Table(data, colWidths=[16 * mm, 110 * mm, 30 * mm, 30 * mm])
dt.setStyle(TableStyle(GRID))
story += [Paragraph("Overall Hour Distribution", UNIT_H), dt]

modes = [
    "Each session is a 1-hour lecture: concepts are introduced on the board or through PPT, followed by examples and discussion.",
    "Live demonstrations with block explorers, hashing tools, Remix IDE and MetaMask make abstract concepts concrete.",
    "Hands-on sessions on Solidity programming and smart-contract deployment on Ethereum test networks.",
    "Case studies on The DAO, altcoins and blockchain in government, health, finance and education connect theory with practice.",
    "Active-learning techniques such as Think-Pair-Share and short quizzes check understanding at the end of each unit.",
    "Continuous assessment through assignments, quizzes, a mini project (simple DApp), slip test and mid-semester examinations.",
    "Additional reading and exercises are given to fast learners, and remedial sessions are held for slow learners.",
    "The final three hours are for revision, solving previous question papers and the slip test.",
]
story.append(KeepTogether([
    Paragraph("General Modes of Teaching", UNIT_H),
    ListFlowable([ListItem(Paragraph(m, BODY), leftIndent=10) for m in modes],
                 bulletType="bullet", leftIndent=10, bulletFontSize=7),
]))

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=12 * mm, rightMargin=12 * mm,
                        topMargin=12 * mm, bottomMargin=12 * mm,
                        title="Blockchain Technology – Course Plan", author=FACULTY)
doc.build(story)
print("wrote", OUT)
