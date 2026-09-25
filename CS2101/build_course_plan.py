"""Generates Course_Plan_CS2101.pdf — unit-wise course plan for CS2101."""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, ListFlowable, ListItem, KeepTogether)

COURSE = "DISCRETE MATHEMATICAL STRUCTURES (CS2101)"
CLASS = "II Year – I Semester"
FACULTY = "Dr. K. Venkata Ramana"
OUT = __file__.replace("build_course_plan.py", "Course_Plan_CS2101.pdf")

R, BD = "Times-Roman", "Times-Bold"
def st(name, size, font=R, align=0, **kw):
    return ParagraphStyle(name, fontName=font, fontSize=size, leading=size * 1.25, alignment=align, **kw)

CELL, CELLC, HEAD = st("cell", 9), st("cellc", 9, align=TA_CENTER), st("head", 9, BD)
BODY = st("body", 9.5)
UNIT_H = st("unit", 11.5, BD, spaceBefore=6, spaceAfter=3, keepWithNext=1)

# (topic, hours, mode of teaching, learning activity)
UNITS = [
    ("I", "The Foundations – Logic, Proofs and Basic Structures", [
        ("Propositional Logic – propositions, connectives, conditional and biconditional statements, truth tables", 1, "Lecture / Board", "Translate English sentences into logical expressions; build truth tables"),
        ("Propositional Equivalences – tautology, contradiction, logical equivalence laws, normal forms (DNF/CNF)", 1, "Lecture / Worked Examples", "Prove equivalences using laws and truth tables"),
        ("Predicates and Quantifiers – universal and existential quantifiers, negation of quantified statements", 1, "Lecture / Worked Examples", "Express statements using predicates and quantifiers"),
        ("Nested Quantifiers", 1, "Problem Solving", "Translate and negate nested quantified statements"),
        ("Rules of Inference – valid arguments, inference rules for propositions and quantified statements", 2, "Lecture / Guided Problem Solving", "Check validity of arguments step by step"),
        ("Introduction to Proofs; Proof Methods and Strategy – direct, contraposition, contradiction, cases, existence and uniqueness proofs", 2, "Worked Examples / Think-Pair-Share", "Write proofs of simple number-theoretic statements"),
        ("Sets and Set Operations – Venn diagrams, set identities, power set, Cartesian product", 1, "Lecture / Board", "Prove set identities; solve Venn-diagram problems"),
        ("Functions – one-to-one, onto, bijection, inverse, composition, floor and ceiling functions", 1, "Lecture / Worked Examples", "Classify functions; find inverses and compositions"),
        ("Sequences and Summations – arithmetic and geometric progressions, summation formulae", 1, "Problem Solving / Quiz", "Evaluate summations; short quiz on Unit I"),
    ]),
    ("II", "Algorithms, Integers and Matrices; Induction and Recursion", [
        ("Algorithms; Growth of Functions – Big-O, Big-Omega and Big-Theta notations", 1, "Lecture / Board", "Find Big-O estimates of given functions"),
        ("Complexity of Algorithms – time complexity of searching and sorting algorithms", 1, "Lecture / Worked Examples", "Analyse linear search, binary search and bubble sort"),
        ("The Integers and Division; Primes and Greatest Common Divisors", 1, "Lecture / Worked Examples", "Apply division algorithm, prime factorisation and GCD/LCM"),
        ("Integers and Algorithms – base-b expansions, Euclidean algorithm, modular exponentiation", 1, "Demonstration / Problem Solving", "Trace the Euclidean algorithm and fast modular exponentiation"),
        ("Applications of Number Theory – linear congruences, Chinese Remainder Theorem, RSA cryptosystem", 1, "Case Study / Worked Examples", "Encrypt and decrypt a small message with RSA"),
        ("Matrices – matrix arithmetic, transpose, zero–one matrices and Boolean product", 1, "Lecture / Problem Solving", "Compute Boolean products of zero–one matrices"),
        ("Mathematical Induction", 1, "Worked Examples / Guided Practice", "Prove summation formulae and inequalities by induction"),
        ("Strong Induction and Well-Ordering", 1, "Lecture / Problem Solving", "Prove results needing strong induction (e.g. postage problems)"),
        ("Recursive Definitions and Structural Induction", 1, "Lecture / Worked Examples", "Define sets and functions recursively; prove properties by structural induction"),
        ("Recursive Algorithms and Program Correctness – partial correctness, loop invariants", 1, "Problem Solving / Assignment", "Write recursive algorithms; verify a loop using invariants"),
    ]),
    ("III", "Counting and Advanced Counting Techniques", [
        ("The Basics of Counting – sum, product, subtraction and division rules, tree diagrams", 1, "Lecture / Board", "Solve counting problems on strings, passwords and licence plates"),
        ("The Pigeonhole Principle – basic and generalised forms", 1, "Worked Examples", "Apply the pigeonhole principle to existence problems"),
        ("Permutations and Combinations", 1, "Lecture / Problem Solving", "Solve arrangement and selection problems"),
        ("Binomial Coefficients – Binomial Theorem, Pascal's identity and triangle, Vandermonde's identity", 1, "Lecture / Worked Examples", "Expand binomials; prove combinatorial identities"),
        ("Generalized Permutations and Combinations; Generating Permutations and Combinations", 1, "Problem Solving / Demonstration", "Count with repetition; generate next permutation in lexicographic order"),
        ("Recurrence Relations – modelling with recurrences (Fibonacci, Towers of Hanoi, bit strings)", 1, "Lecture / Worked Examples", "Set up recurrence relations for counting problems"),
        ("Solving Linear Recurrence Relations – homogeneous and non-homogeneous with constant coefficients", 2, "Worked Examples / Guided Problem Solving", "Solve recurrences using characteristic roots and particular solutions"),
        ("Divide-and-Conquer Algorithms and Recurrence Relations – Master Theorem", 1, "Lecture / Problem Solving", "Derive recurrences for binary search and merge sort"),
        ("Generating Functions – solving counting problems and recurrences", 1, "Lecture / Worked Examples", "Find coefficients of generating functions for counting problems"),
        ("Inclusion–Exclusion and Applications of Inclusion–Exclusion – onto functions, derangements, sieve of Eratosthenes", 1, "Problem Solving / Quiz", "Count derangements and onto functions; quiz on Unit III"),
    ]),
    ("IV", "Relations", [
        ("Relations and their Properties – reflexive, symmetric, antisymmetric, transitive; combining relations", 1, "Lecture / Board", "Test given relations for each property"),
        ("n-ary Relations and their Applications – relational databases, selection, projection and join", 1, "Case Study / Demonstration", "Perform select, project and join on a sample student database"),
        ("Representing Relations – zero–one matrices and directed graphs", 1, "Lecture / Worked Examples", "Convert relations between matrix and digraph forms"),
        ("Closures of Relations – reflexive, symmetric and transitive closures; Warshall's algorithm", 1, "Worked Examples / Guided Practice", "Compute transitive closure using Warshall's algorithm"),
        ("Equivalence Relations – equivalence classes and partitions", 1, "Lecture / Problem Solving", "Find equivalence classes, e.g. congruence modulo n"),
        ("Partial Orderings – posets, Hasse diagrams, maximal/minimal elements, lattices, topological sorting", 1, "Problem Solving / Quiz", "Draw Hasse diagrams; topologically sort a task list; quiz on Unit IV"),
    ]),
    ("V", "Graphs and Trees", [
        ("Graphs and Graph Models; Graph Terminology and Special Types of Graphs – degree, handshaking theorem, complete, cycle, wheel, bipartite graphs", 1, "Lecture / Board", "Identify graph types; verify the handshaking theorem"),
        ("Representing Graphs and Graph Isomorphism – adjacency list, adjacency and incidence matrices", 1, "Worked Examples", "Represent graphs; test pairs of graphs for isomorphism"),
        ("Connectivity – paths, connected components, cut vertices and cut edges", 1, "Lecture / Problem Solving", "Find components and cut vertices; count paths using adjacency matrix"),
        ("Euler and Hamilton Paths and Circuits", 1, "Lecture / Worked Examples", "Check Euler and Hamilton conditions on given graphs"),
        ("Shortest-Path Problems – Dijkstra's algorithm, travelling salesperson problem", 1, "Demonstration / Guided Practice", "Trace Dijkstra's algorithm on a weighted graph"),
        ("Planar Graphs – Euler's formula, Kuratowski's theorem", 1, "Lecture / Problem Solving", "Apply Euler's formula; show K5 and K3,3 are non-planar"),
        ("Graph Colouring – chromatic number, applications to scheduling", 1, "Problem Solving / Think-Pair-Share", "Colour graphs; model an exam-timetable problem"),
        ("Introduction to Trees; Applications of Trees – binary search trees, decision trees, prefix codes, Huffman coding", 1, "Lecture / Worked Examples", "Build a BST; construct Huffman codes"),
        ("Tree Traversal – preorder, inorder, postorder; infix, prefix and postfix notation", 1, "Worked Examples", "Traverse trees; evaluate prefix and postfix expressions"),
        ("Spanning Trees – construction using DFS and BFS, backtracking", 1, "Demonstration / Guided Practice", "Find spanning trees by DFS and BFS"),
        ("Minimum Spanning Trees – Prim's and Kruskal's algorithms", 1, "Problem Solving / Quiz", "Find MSTs by both algorithms and compare; quiz on Unit V"),
    ]),
    ("VI", "Boolean Algebra and Modelling Computation", [
        ("Boolean Functions – Boolean expressions, identities of Boolean algebra, duality", 1, "Lecture / Board", "Prove Boolean identities; find duals"),
        ("Representing Boolean Functions (sum-of-products, functional completeness); Logic Gates", 1, "Lecture / Worked Examples", "Write SOP expansions; draw gate circuits for given functions"),
        ("Minimization of Circuits – Karnaugh maps and the Quine–McCluskey method", 2, "Worked Examples / Guided Problem Solving", "Minimise functions of 3 and 4 variables"),
        ("Languages and Grammars – phrase-structure grammars, types of grammars, derivation trees", 1, "Lecture / Worked Examples", "Derive strings and classify grammars"),
        ("Finite-State Machines with Output – Mealy and Moore machines", 1, "Demonstration / Problem Solving", "Design a vending-machine or unit-delay machine"),
        ("Finite-State Machines with No Output; Language Recognition – DFA, NFA, regular sets, Kleene's theorem", 1, "Lecture / Worked Examples", "Construct DFAs for given languages; convert NFA to DFA"),
        ("Turing Machines – definition, computing with Turing machines", 1, "Lecture / Quiz", "Trace a Turing machine on an input tape; quiz on Unit VI"),
    ]),
    ("VII", "Revision and Assessment", [
        ("Revision of Units I–III – logic, proofs, number theory, induction and counting", 1, "Tutorial / Problem Solving", "Solve previous university question papers"),
        ("Revision of Units IV–VI – relations, graphs, trees, Boolean algebra and FSMs", 1, "Tutorial / Problem Solving", "Solve previous university question papers"),
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
for text, size, font, gap in [("COURSE PLAN", 18, BD, 10), (COURSE, 22, BD, 8), (CLASS, 12, R, 40),
                              ("Prepared by", 12, R, 4), (FACULTY, 18, BD, 4),
                              ("Department of CSSE", 12, R, 2), ("Andhra University", 12, BD, 0)]:
    story += [Paragraph(text, st("c", size, font, TA_CENTER)), Spacer(1, gap * mm / 2 + 4)]
story.append(PageBreak())

story += [
    Paragraph("<u>UNIT-WISE COURSE PLAN</u>", st("t1", 15, BD, TA_CENTER, spaceAfter=6)),
    Paragraph("<u>DISCRETE MATHEMATICAL STRUCTURES (CS2101)</u>", st("t2", 11.5, BD, TA_CENTER, spaceAfter=6)),
    Paragraph(f"<b>Class:</b> {CLASS} &nbsp; | &nbsp; <b>Total Hours:</b> 60 (15 weeks × 4 hours)", BODY),
    Spacer(1, 3),
    Paragraph("<b>Text Book:</b> Kenneth H. Rosen, <i>Discrete Mathematics &amp; Its Applications with "
              "Combinatorics and Graph Theory</i>, Tata McGraw-Hill", BODY),
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
    "Each session is a 1-hour lecture: concepts are introduced on the board or through PPT, followed by worked examples from the text book.",
    "Every unit includes guided problem-solving hours where students solve exercises in class with faculty support.",
    "Active-learning techniques such as Think-Pair-Share and short quizzes check understanding at the end of each unit.",
    "Algorithmic topics (Euclidean algorithm, Warshall's, Dijkstra's, Prim's, Kruskal's, K-maps, FSMs) are demonstrated by step-by-step tracing on sample inputs.",
    "Case studies such as RSA cryptography, relational databases and exam timetabling by graph colouring connect theory with real-world applications.",
    "Continuous assessment through unit-wise assignments, quizzes, slip tests and mid-semester examinations.",
    "Additional problem sheets are given to fast learners, and remedial tutorials are held for slow learners.",
    "The final three hours are for revision, solving previous question papers and the slip test.",
]
story.append(KeepTogether([
    Paragraph("General Modes of Teaching", UNIT_H),
    ListFlowable([ListItem(Paragraph(m, BODY), leftIndent=10) for m in modes],
                 bulletType="bullet", leftIndent=10, bulletFontSize=7),
]))

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=12 * mm, rightMargin=12 * mm,
                        topMargin=12 * mm, bottomMargin=12 * mm,
                        title="Discrete Mathematical Structures (CS2101) – Course Plan", author=FACULTY)
doc.build(story)
print("wrote", OUT)
