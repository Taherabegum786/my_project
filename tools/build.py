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


def main():
    for subject in sorted(p for p in (ROOT / "data").iterdir() if p.is_dir()):
        outdir = ROOT / "practice" / subject.name
        outdir.mkdir(parents=True, exist_ok=True)
        rows, total = [], 0
        for src in sorted(subject.glob("*.txt")):
            title, questions = parse(src)
            md, counts = render(title, questions)
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
        print(f"{subject.name}: {total} questions in {len(rows)} sets")


if __name__ == "__main__":
    main()
