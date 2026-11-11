#!/usr/bin/env python3
"""Mechanical integrity check for a manuscript. Usage: check_paper.py <paper-id>

Fails if the paper cites a key missing from refs.bib, a cited entry has no doi/url,
a cited key has no literature note, or placeholders remain.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CITE = re.compile(r"\\[a-zA-Z]*cite[a-zA-Z]*\*?(?:\[[^\]]*\])*\{([^}]*)\}")
ENTRY = re.compile(r"@\w+\s*\{\s*([^,\s]+)\s*,(.*?)(?=\n@|\Z)", re.S)
PLACEHOLDER = re.compile(r"TODO-RESULT|\\todo\b")


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    paper = ROOT / "papers" / sys.argv[1] / "paper"
    tex_files = sorted(paper.glob("**/*.tex"))
    if not tex_files:
        print(f"no .tex files under {paper}")
        return 2

    bib_path = ROOT / "research" / "lit" / "refs.bib"
    bib = {k: body for k, body in ENTRY.findall(bib_path.read_text() if bib_path.exists() else "")}
    notes = ROOT / "research" / "lit" / "notes"

    problems, cited = [], set()
    for tex in tex_files:
        for n, line in enumerate(tex.read_text().splitlines(), 1):
            code = re.sub(r"(?<!\\)%.*", "", line)
            for group in CITE.findall(code):
                cited.update(k.strip() for k in group.split(",") if k.strip())
            if PLACEHOLDER.search(code):
                problems.append(f"{tex.relative_to(ROOT)}:{n}: unresolved placeholder")

    for key in sorted(cited):
        if key not in bib:
            problems.append(f"cite '{key}': not in refs.bib")
            continue
        if not re.search(r"\b(doi|url)\s*=", bib[key], re.I):
            problems.append(f"cite '{key}': bib entry has no doi or url")
        if not (notes / f"{key}.md").exists():
            problems.append(f"cite '{key}': no literature note (source never read)")

    print(f"{len(cited)} cited keys, {len(problems)} problems")
    for p in problems:
        print("  " + p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
