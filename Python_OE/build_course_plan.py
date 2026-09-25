"""Generates Course_Plan_Python_Programming.pdf — unit-wise course plan."""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, ListFlowable, ListItem, KeepTogether)

COURSE = "PYTHON PROGRAMMING"
SUBTITLE = "Open Elective"
FACULTY = "Dr. K. Venkata Ramana"
OUT = __file__.replace("build_course_plan.py", "Course_Plan_Python_Programming.pdf")

R, BD = "Times-Roman", "Times-Bold"
def st(name, size, font=R, align=0, **kw):
    return ParagraphStyle(name, fontName=font, fontSize=size, leading=size * 1.25, alignment=align, **kw)

CELL, CELLC, HEAD = st("cell", 9), st("cellc", 9, align=TA_CENTER), st("head", 9, BD)
BODY = st("body", 9.5)
UNIT_H = st("unit", 11.5, BD, spaceBefore=6, spaceAfter=3, keepWithNext=1)

# (topic, hours, mode of teaching, learning activity)
UNITS = [
    ("I", "Introduction to Python", [
        ("Rapid Introduction to Procedural Programming – Python interpreter, IDLE / Jupyter, first programs", 1, "Lecture / Demonstration", "Write and run simple Python programs"),
        ("Data Types – Identifiers and Keywords, Integral Types, Floating-Point Types", 1, "Lecture / Board", "Evaluate expressions with int, float, bool and complex values"),
        ("Strings – Comparing Strings, Slicing and Striding Strings", 1, "Lecture / Worked Examples", "Extract and reverse substrings using slices and strides"),
        ("String Operators and Methods; String formatting with str.format", 1, "Lecture / Worked Examples", "Format a report using str.format and f-strings"),
        ("Collection Data Types – Tuples and Lists", 2, "Lecture / Demonstration", "Build and manipulate lists and tuples of records"),
        ("Sets and Dictionaries", 1, "Lecture / Worked Examples", "Word-frequency count using dictionaries and sets"),
        ("Iterating and Copying Collections – shallow vs. deep copy", 1, "Demonstration / Think-Pair-Share", "Predict outputs of copy vs. reference programs"),
        ("Introduction to PIP – installing and managing packages", 1, "Demonstration / Quiz", "Install NumPy and Pandas with pip; quiz on Unit I"),
    ]),
    ("II", "Control Structures and Functions", [
        ("Python Control Structures – Conditional Branching", 1, "Lecture / Board", "Programs on grading and leap-year checks"),
        ("Looping – for, while, break, continue, else on loops; comprehensions", 1, "Lecture / Worked Examples", "Generate number patterns and prime numbers"),
        ("Exception Handling – try, except, else, finally; raising exceptions", 1, "Lecture / Worked Examples", "Handle invalid input and file errors"),
        ("Custom Functions – arguments, default and keyword arguments, *args/**kwargs, lambda, scope", 2, "Lecture / Problem Solving", "Write reusable functions for common tasks"),
        ("Python Library Modules – random, math, time, os, shutil, sys", 1, "Demonstration", "Simulate dice rolls; list and copy files"),
        ("Python Library Modules – glob, re, statistics", 1, "Demonstration / Worked Examples", "Search files with glob; validate text with regular expressions"),
        ("Creating a custom module", 1, "Demonstration / Quiz", "Package own functions as a module; quiz on Unit II"),
    ]),
    ("III", "Object Oriented Programming and File Handling", [
        ("Object Oriented Concepts and Terminology", 1, "Lecture / PPT", "Identify classes and objects in real-world scenarios"),
        ("Custom Classes – Attributes and Methods; special methods", 2, "Lecture / Worked Examples", "Design a Student / BankAccount class"),
        ("Inheritance and Polymorphism", 2, "Lecture / Worked Examples", "Build a Shape class hierarchy with overridden methods"),
        ("Using Properties to Control Attribute Access", 1, "Lecture / Demonstration", "Add validated properties to a class"),
        ("File Handling – Writing and Reading Binary Data (pickle, struct)", 1, "Demonstration", "Save and load objects with pickle"),
        ("Writing and Parsing Text Files", 1, "Problem Solving / Quiz", "Parse a text/CSV file into objects; quiz on Unit III"),
    ]),
    ("IV", "NumPy Arrays and Vectorized Computation", [
        ("NumPy arrays – ndarray, data types; Array creation", 1, "Lecture / Demonstration", "Create arrays using array, arange, zeros, linspace"),
        ("Indexing and slicing; Fancy indexing", 2, "Lecture / Worked Examples", "Select rows, columns and elements with boolean and integer arrays"),
        ("Numerical operations on arrays; Array functions – universal functions, broadcasting", 2, "Lecture / Worked Examples", "Vectorise loops; compare timing with plain Python"),
        ("Data processing using arrays – conditional logic, statistics, sorting, unique", 1, "Demonstration / Problem Solving", "Summarise a dataset with array methods"),
        ("Loading and saving data – saving an array, loading an array (npy, npz, text)", 1, "Demonstration", "Save and reload arrays in binary and text formats"),
        ("Linear algebra with NumPy", 1, "Worked Examples", "Matrix product, inverse, determinant, solving linear systems"),
        ("NumPy random numbers", 1, "Demonstration / Quiz", "Simulate random walks; quiz on Unit IV"),
    ]),
    ("V", "Data Analysis with Pandas", [
        ("An overview of the Pandas package; Pandas data structures – Series", 1, "Lecture / Demonstration", "Create and operate on Series objects"),
        ("The DataFrame – creation, columns and rows", 1, "Lecture / Demonstration", "Build DataFrames from dictionaries and CSV files"),
        ("Essential Basic Functionality – Reindexing and altering labels, Head and tail, Binary operations", 2, "Lecture / Worked Examples", "Reindex and align two DataFrames"),
        ("Functional statistics; Function application; Sorting", 1, "Worked Examples", "Apply functions and sort a dataset"),
        ("Indexing and selecting data – loc, iloc, boolean selection", 1, "Lecture / Problem Solving", "Query a dataset with conditions"),
        ("Computational tools – covariance, correlation, ranking, rolling windows", 1, "Lecture / Worked Examples", "Compute correlations and moving averages"),
        ("Working with Missing Data – detecting, dropping and filling", 1, "Demonstration / Problem Solving", "Clean a dataset with missing values"),
        ("Advanced Uses of Pandas – Hierarchical indexing; the Panel data structure", 2, "Lecture / Quiz", "Use MultiIndex for multi-level data; quiz on Unit V"),
    ]),
    ("VI", "Data Analysis Application Examples", [
        ("Data munging; Cleaning data", 1, "Case Study / Demonstration", "Clean a raw real-world dataset"),
        ("Filtering data", 1, "Worked Examples", "Filter records by multiple conditions"),
        ("Merging data – merge, join, concat", 1, "Worked Examples", "Combine related tables"),
        ("Reshaping data – pivot, melt, stack and unstack", 1, "Demonstration / Problem Solving", "Convert between wide and long formats"),
        ("Data aggregation and Grouping data – groupby, pivot tables", 2, "Case Study / Quiz", "Produce group-wise summaries; quiz on Unit VI"),
    ]),
    ("VII", "Data Visualization", [
        ("The matplotlib API primer – Line properties", 1, "Lecture / Demonstration", "Plot functions with different line styles and colours"),
        ("Figures and subplots", 1, "Demonstration", "Create multi-panel figures"),
        ("Exploring plot types – Scatter plots and Bar plots", 1, "Worked Examples", "Visualise relationships and category comparisons"),
        ("Histogram plots", 1, "Worked Examples", "Plot distributions with different bin sizes"),
        ("Legends and annotations", 1, "Demonstration / Think-Pair-Share", "Annotate key points in a plot"),
        ("Plotting functions with Pandas", 2, "Case Study / Quiz", "Exploratory data analysis of a dataset; quiz on Unit VII"),
    ]),
    ("VIII", "Revision and Assessment", [
        ("Revision of Units I–IV – Python basics, functions, OOP and NumPy", 1, "Tutorial / Discussion", "Solve previous question papers"),
        ("Revision of Units V–VII – Pandas, data analysis and visualization", 1, "Tutorial / Discussion", "Solve previous question papers"),
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
    Paragraph("<b>Software / Tools:</b> Python 3, Jupyter Notebook / IDLE, pip, NumPy, Pandas, Matplotlib "
              "(Anaconda distribution)", BODY),
    Spacer(1, 3),
    Paragraph("<b>Text Books:</b> (1) Mark Summerfield, <i>Programming in Python 3: A Complete Introduction to the "
              "Python Language</i>, 2/e, Addison-Wesley; (2) Phuong Vo.T.H, Martin Czygan, <i>Python: End-to-End Data "
              "Analysis Learning Path, Module 1: Getting Started with Python Data Analysis</i>, Packt", BODY),
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
    "Each session is a 1-hour lecture: concepts are introduced on the board or through PPT, followed by live coding in Jupyter Notebook.",
    "Every topic is illustrated with small programs that students run and modify during the class.",
    "Case studies on real datasets connect NumPy, Pandas and Matplotlib with practical data analysis.",
    "Active-learning techniques such as Think-Pair-Share and short quizzes check understanding at the end of each unit.",
    "Continuous assessment through programming assignments, quizzes, slip test and mid-semester examinations.",
    "Additional exercises are given to fast learners, and remedial sessions are held for slow learners.",
    "The final three hours are for revision, solving previous question papers and the slip test.",
]
story.append(KeepTogether([
    Paragraph("General Modes of Teaching", UNIT_H),
    ListFlowable([ListItem(Paragraph(m, BODY), leftIndent=10) for m in modes],
                 bulletType="bullet", leftIndent=10, bulletFontSize=7),
]))

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=12 * mm, rightMargin=12 * mm,
                        topMargin=12 * mm, bottomMargin=12 * mm,
                        title="Python Programming – Course Plan", author=FACULTY)
doc.build(story)
print("wrote", OUT)
