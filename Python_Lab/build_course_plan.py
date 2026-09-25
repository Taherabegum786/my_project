"""Generates Course_Plan_Python_Lab.pdf — unit-wise course plan."""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, ListFlowable, ListItem, KeepTogether)

COURSE = "PYTHON PROGRAMMING LAB"
FACULTY = "Dr. K. Venkata Ramana"
OUT = __file__.replace("build_course_plan.py", "Course_Plan_Python_Lab.pdf")

R, BD = "Times-Roman", "Times-Bold"
def st(name, size, font=R, align=0, **kw):
    return ParagraphStyle(name, fontName=font, fontSize=size, leading=size * 1.25, alignment=align, **kw)

CELL, CELLC, HEAD = st("cell", 9), st("cellc", 9, align=TA_CENTER), st("head", 9, BD)
BODY = st("body", 9.5)
UNIT_H = st("unit", 11.5, BD, spaceBefore=6, spaceAfter=3, keepWithNext=1)

# (topic, hours, mode of teaching, learning activity)
UNITS = [
    ("I", "Python Data Structures, Text and File Handling", [
        ("Lab introduction; Python programs on Lists and Dictionaries – creation, indexing, slicing, methods, comprehensions", 3, "Lecture / Demonstration", "Word-frequency counter; student-marks dictionary"),
        ("Python programs on Searching and Sorting – linear and binary search; bubble, selection, insertion, merge and quick sort", 3, "Demonstration / Guided Practice", "Implement and compare techniques on lists"),
        ("Python programs on Text Handling – string methods, formatting, regular expressions", 3, "Worked Examples / Hands-on Practice", "Count words, vowels and palindromes; validate e-mail IDs"),
        ("Python programs on File Handling – reading, writing, appending text and CSV files; exception handling", 3, "Guided Hands-on Practice", "Copy, merge and search files; process a CSV file"),
    ]),
    ("II", "Statistical Measures", [
        ("Python programs for calculating Mean, Mode, Median, Variance and Standard Deviation", 3, "Worked Examples / Hands-on Practice", "Compute measures manually and verify with the statistics module"),
        ("Python programs for Karl Pearson Coefficient of Correlation and Rank Correlation", 3, "Worked Examples / Hands-on Practice", "Compute correlations and verify with NumPy / SciPy"),
    ]),
    ("III", "NumPy and Pandas", [
        ("Python programs on NumPy Arrays – creation, indexing, slicing, broadcasting; Linear algebra with NumPy", 3, "Demonstration / Guided Practice", "Matrix operations, determinant, inverse, eigenvalues, solving linear equations"),
        ("Python programs for creation and manipulation of Data Frames using Pandas – selection, filtering, grouping, merging", 3, "Demonstration / Hands-on Practice", "Load a CSV dataset and summarise it with Pandas"),
    ]),
    ("IV", "Data Visualization with Matplotlib", [
        ("Simple Line Plots; Adjusting the Plot – line colours and styles, axes limits, labelling; Simple Scatter Plots; Histograms; Boxplot", 3, "Demonstration / Guided Practice", "Plot a dataset in different chart types"),
        ("Customizing Plot Legends; Choosing Elements for the Legend; Multiple Legends; Customizing Colorbars; Multiple Subplots; Text and Annotation; Customizing Ticks", 3, "Worked Examples / Hands-on Practice", "Build a multi-panel annotated figure"),
    ]),
    ("V", "Machine Learning with Python", [
        ("Data pre-processing – handling missing values, handling categorical data, bringing features to the same scale, selecting meaningful features", 3, "Demonstration / Guided Practice", "Clean and prepare a real dataset with Pandas and scikit-learn"),
        ("Compressing data via dimensionality reduction – Principal Component Analysis (PCA)", 3, "Worked Examples / Hands-on Practice", "Apply PCA to the Wine dataset; plot explained variance"),
        ("Data Clustering – K-Means, hierarchical clustering; elbow method", 3, "Demonstration / Hands-on Practice", "Cluster the Iris dataset and visualise the clusters"),
        ("Classification – k-NN, Decision Tree, Logistic Regression; Model Evaluation using K-fold cross-validation", 3, "Case Study / Hands-on Practice", "Train classifiers and compare K-fold cross-validation accuracy"),
    ]),
    ("VI", "Revision and Assessment", [
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
    Paragraph("<b>Software / Tools:</b> Python 3, Jupyter Notebook / IDLE, NumPy, Pandas, SciPy, Matplotlib, "
              "scikit-learn (Anaconda distribution); Linux or Windows", BODY),
    Spacer(1, 3),
    Paragraph("<b>Reference Books:</b> (1) Wesley J. Chun, <i>Core Python Programming</i>, 2/e, Prentice Hall; "
              "(2) Chris Albon, <i>Machine Learning with Python Cookbook</i>, O'Reilly, 2018; "
              "(3) Mark Summerfield, <i>Programming in Python 3</i>, 2/e, Addison-Wesley; "
              "(4) Phuong Vo.T.H, Martin Czygan, <i>Getting Started with Python Data Analysis</i>, Packt; "
              "(5) Armando Fandango, <i>Python Data Analysis</i>, Packt; "
              "(6) Magnus Vilhelm Persson, Luiz Felipe Martins, <i>Mastering Python Data Analysis</i>, Packt; "
              "(7) Sebastian Raschka, Vahid Mirjalili, <i>Python Machine Learning</i>, Packt", BODY),
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
    "Programs are developed in Jupyter Notebook so that code, output and plots are recorded together.",
    "Standard datasets (Iris, Wine and CSV files) are used so that statistical, visualization and machine-learning results can be compared.",
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
                        title="Python Programming Lab – Course Plan", author=FACULTY)
doc.build(story)
print("wrote", OUT)
