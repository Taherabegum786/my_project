#!/usr/bin/env python3
"""Render question banks in data/<subject>/*.txt to Markdown practice sets.

Line format (one question per line, '#' lines are comments):
    PRIORITY|question|opt1|opt2|opt3|opt4|answer(1-4)|explanation
PRIORITY is H, M or L. Use \\n inside the question for a line break.
Shorthand for the option block: '@AR' (Assertion-Reason) or '@S2' (two statements).
The first comment line of a file ('# title: ...') gives the set title.
"""
import pathlib
import random
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PRIORITY = {"H": "High", "M": "Medium", "L": "Low"}
MACROS = {
    "@AR": [
        "Both A and R are true and R is the correct explanation of A",
        "Both A and R are true but R is NOT the correct explanation of A",
        "A is true but R is false",
        "A is false but R is true",
    ],
    "@S2": [
        "Both Statement I and Statement II are true",
        "Both Statement I and Statement II are false",
        "Statement I is true but Statement II is false",
        "Statement I is false but Statement II is true",
    ],
}


def parse(path):
    title, questions = path.stem, []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        if line.startswith("#"):
            if line.lower().startswith("# title:"):
                title = line.split(":", 1)[1].strip()
            continue
        parts = line.split("|")
        fixed = len(parts) == 5 and parts[2] in MACROS
        if fixed:
            parts = parts[:2] + MACROS[parts[2]] + parts[3:]
        if len(parts) != 8 or parts[0] not in PRIORITY or parts[6] not in "1234":
            sys.exit(f"{path.name}:{n}: malformed question line")
        if not fixed and not any(o.startswith(("None", "Both", "All")) for o in parts[2:6]):
            # The source lists options in authoring order; shuffle them (stably,
            # seeded by the question text) so the answer key is not guessable.
            order = [0, 1, 2, 3]
            random.Random(parts[1]).shuffle(order)
            opts = parts[2:6]
            parts[2:6] = [opts[k] for k in order]
            parts[6] = str(order.index(int(parts[6]) - 1) + 1)
        questions.append(parts)
    return title, questions


def render(title, questions):
    counts = {k: sum(q[0] == k for q in questions) for k in PRIORITY}
    out = [
        f"# {title}",
        "",
        f"**{len(questions)} questions** — High: {counts['H']}, "
        f"Medium: {counts['M']}, Low: {counts['L']}",
        "",
        "Each question carries 2 marks, has exactly one correct option and no "
        "negative marking (UGC NET Paper II pattern). Click **Answer** to check.",
        "",
        "---",
        "",
    ]
    for i, (pri, text, o1, o2, o3, o4, ans, expl) in enumerate(questions, 1):
        body = text.replace("\\n", "  \n")
        out += [f"**Q{i}.** `{PRIORITY[pri]}`  ", body, ""]
        out += [f"({k}) {o}  " for k, o in enumerate((o1, o2, o3, o4), 1)]
        out += [
            "",
            "<details><summary>Answer</summary>",
            "",
            f"**({ans})** — {expl}",
            "",
            "</details>",
            "",
        ]
    return "\n".join(out), counts


# ---------------------------------------------------------------- LaTeX output
TEX_ESCAPES = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
               "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}"}
TEX_UNICODE = {
    "−": "$-$", "×": r"$\times$", "≈": r"$\approx$", "≡": r"$\equiv$",
    "≠": r"$\neq$", "≥": r"$\geq$", "≤": r"$\leq$", "⊕": r"$\oplus$",
    "→": r"$\rightarrow$", "φ": r"$\varphi$", "α": r"$\alpha$", "ρ": r"$\rho$",
    "µ": r"$\mu$", "²": r"\textsuperscript{2}", "—": "---", "–": "--", "è": r"\`e",
}


def tex(text):
    """Convert one plain-text field of a question bank to LaTeX."""
    text = re.sub(r"_{3,}", "\x00", text)
    text = "".join(TEX_ESCAPES.get(c, c) for c in text)
    text = text.replace("\x00", r"\underline{\hspace{3em}}")
    text = re.sub(r'"([^"]*)"', r"``\1''", text)
    text = re.sub(r"\^(?:\(([^)]*)\)|([-−]?\w+))",
                  lambda m: r"\textsuperscript{%s}" % (m.group(1) or m.group(2)), text)
    for char, repl in TEX_UNICODE.items():
        text = text.replace(char, repl)
    bad = [c for c in text if ord(c) > 127]
    if bad:
        sys.exit(f"no LaTeX mapping for {set(bad)}; add it to TEX_UNICODE")
    return text.replace("\\textbackslash{}n", "\\\\\n")


def render_tex(title, questions):
    out = [r"\section{%s}" % tex(title.split("—", 1)[-1].strip()), ""]
    for pri, text, o1, o2, o3, o4, _ans, _expl in questions:
        opts = [tex(o) for o in (o1, o2, o3, o4)]
        layout = r"\optsshort" if max(map(len, (o1, o2, o3, o4))) <= 28 else r"\optslong"
        out += [r"\begin{question}{%s}" % pri, tex(text),
                layout + "".join("{%s}" % o for o in opts), r"\end{question}", ""]
    out += [r"\begin{answers}"]
    out += [r"\ans{%d}{%s}{%s}" % (i, q[6], tex(q[7])) for i, q in enumerate(questions, 1)]
    out += [r"\end{answers}", ""]
    return "\n".join(out)


def write_tex(subjects):
    """subjects: list of (slug, [(title, questions), ...])."""
    outdir = ROOT / "latex"
    (outdir / "subjects").mkdir(parents=True, exist_ok=True)
    for slug, sets in subjects:
        body = [
            f"% Generated by tools/build.py -- do not edit; edit data/{slug}/*.txt",
            "% No preamble here: this file is \\input by main.tex.",
            r"\chapter{%s}" % slug.replace("-", " ").title(),
            "",
        ]
        body += [render_tex(title, questions) for title, questions in sets]
        (outdir / "subjects" / f"{slug}.tex").write_text("\n".join(body), encoding="utf-8")
    main = [
        "% Generated by tools/build.py. Every subject in data/ is included below,",
        "% so this one file always builds the complete merged book.",
        r"\documentclass[11pt,a4paper,oneside]{book}",
        r"\input{preamble}",
        r"\begin{document}",
        r"\frontmatter",
        r"\begin{titlepage}\centering\vspace*{5cm}",
        r"{\Huge\bfseries UGC NET\par\medskip Computer Science and Applications\par}",
        r"\vspace{1cm}{\LARGE Unit-wise Practice Questions\par}",
        r"\vspace{2cm}{\large Paper II pattern: 2 marks each, no negative marking\par}",
        r"\vfill{\large Priority tags: \prio{H} high, \prio{M} medium, \prio{L} low",
        r"likelihood, estimated from previous-year question trends\par}",
        r"\end{titlepage}",
        r"\tableofcontents",
        r"\mainmatter",
        *[r"\input{subjects/%s}" % slug for slug, _ in subjects],
        r"\end{document}",
        "",
    ]
    (outdir / "main.tex").write_text("\n".join(main), encoding="utf-8")


def main():
    subjects = []
    for subject in sorted(p for p in (ROOT / "data").iterdir() if p.is_dir()):
        sets = []
        outdir = ROOT / "practice" / subject.name
        outdir.mkdir(parents=True, exist_ok=True)
        rows, total = [], 0
        for src in sorted(subject.glob("*.txt")):
            title, questions = parse(src)
            md, counts = render(title, questions)
            sets.append((title, questions))
            (outdir / f"{src.stem}.md").write_text(md, encoding="utf-8")
            rows.append(
                f"| [{title}]({src.stem}.md) | {len(questions)} | "
                f"{counts['H']} | {counts['M']} | {counts['L']} |"
            )
            total += len(questions)
        index = [
            f"# {subject.name.replace('-', ' ').title()} — practice sets",
            "",
            f"Total: **{total} questions**",
            "",
            "| Set | Questions | High | Medium | Low |",
            "|---|---|---|---|---|",
            *rows,
            "",
        ]
        (outdir / "README.md").write_text("\n".join(index), encoding="utf-8")
        subjects.append((subject.name, sets))
        print(f"{subject.name}: {total} questions in {len(rows)} sets")
    write_tex(subjects)


if __name__ == "__main__":
    main()
