# UGC NET Computer Science — Unit-wise Practice Bits

Practice MCQs for UGC NET Paper II (Computer Science and Applications), organised by
syllabus unit and topic, in the question styles used in the exam: single-correct MCQ,
Match List I with List II, Assertion–Reason, Statement I / Statement II, multiple-statement
("choose the correct answer from the options given below") and ordering questions.

## Available

| Subject (syllabus unit) | Questions | Link |
|---|---|---|
| Data Communication and Computer Networks (Unit 8) | 417 | [practice/computer-networks](practice/computer-networks/README.md) |

More subjects will be added in the same format.

## Priority tags

Every question is tagged `High`, `Medium` or `Low`. The tag is an estimate of how often
that topic and question type has recurred in previous years' papers — it is a judgement
based on PYQ trends, not a computed statistic. Do the `High` questions first.

The questions are original practice questions modelled on PYQ patterns, not copies of
actual exam questions.

## Editing or adding questions

Question banks live in `data/<subject>/*.txt`, one question per line:

    PRIORITY|question|option1|option2|option3|option4|answer|explanation

Run `python3 tools/build.py` to regenerate the Markdown in `practice/`. Options are
shuffled (deterministically) at build time so the answer key is evenly spread.
