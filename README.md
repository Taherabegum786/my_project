# UGC NET Computer Science — Unit-wise Practice Bits

Practice MCQs for UGC NET Paper II (Computer Science and Applications), organised by
syllabus unit and topic, in the question styles used in the exam: single-correct MCQ,
Match List I with List II, Assertion–Reason, Statement I / Statement II, multiple-statement
("choose the correct answer from the options given below") and ordering questions.

## Available

| Unit | Subject | Questions | Link |
|---|---|---|---|
| 3 | Programming Languages and Computer Graphics | 290 | [practice/programming-graphics](practice/programming-graphics/README.md) |
| 4 | Database Management Systems | 480 | [practice/dbms](practice/dbms/README.md) |
| 5 | System Software and Operating System | 556 | [practice/operating-systems](practice/operating-systems/README.md) |
| 6 | Software Engineering | 239 | [practice/software-engineering](practice/software-engineering/README.md) |
| 7 | Data Structures and Algorithms | 458 | [practice/data-structures-algorithms](practice/data-structures-algorithms/README.md) |
| 8 | Theory of Computation and Compilers | 346 | [practice/toc-compilers](practice/toc-compilers/README.md) |
| 9 | Data Communication and Computer Networks | 417 | [practice/computer-networks](practice/computer-networks/README.md) |

More subjects will be added in the same format.

## LaTeX / PDF version

The same questions are generated as LaTeX in `latex/`:

- `latex/main.tex` — the single merged book. It `\input`s every subject in syllabus-unit
  order, so compiling it always gives one file with all subjects completed so far.
- `latex/preamble.tex` — shared packages and macros (edit this to change the layout).
- `latex/subjects/<subject>.tex` — one chapter per subject, with no preamble of its own.

The book compiles cleanly with pdflatex (TeX Live 2023: `texlive-latex-recommended`,
`texlive-fonts-recommended`, `lmodern`). Compile with `pdflatex main.tex` (twice, for the
table of contents) from inside `latex/`,
or upload the `latex/` folder to Overleaf and set `main.tex` as the main document. Answers
with explanations are printed at the end of each set.

## Priority tags

Every question is tagged `High`, `Medium` or `Low`. The tag is an estimate of how often
that topic and question type has recurred in previous years' papers — it is a judgement
based on PYQ trends, not a computed statistic. Do the `High` questions first.

The questions are original practice questions modelled on PYQ patterns, not copies of
actual exam questions.

## Editing or adding questions

Question banks live in `data/<subject>/*.txt`, one question per line:

    PRIORITY|question|option1|option2|option3|option4|answer|explanation

Run `python3 tools/build.py` to regenerate the Markdown in `practice/` and the LaTeX in `latex/`.
Run `python3 tools/check.py` to catch ambiguous questions (duplicate options or
duplicate List II entries in match questions). Options are
shuffled (deterministically) at build time so the answer key is evenly spread.
