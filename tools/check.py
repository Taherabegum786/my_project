#!/usr/bin/env python3
"""Lint the question banks in data/ for ambiguities that make a question unfair.

Flags: two identical options; a "Match List I with List II" question whose List II
contains the same entry twice (so more than one option can be correct); a match
option that maps two List I items to the same List II item. Run after editing data/.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build  # noqa: E402

ROMAN = re.compile(r"\s*\b(?:IV|V|I{1,3})\. ")
MAPPING = re.compile(r"(?:[A-E]-(?:IV|V|I{1,3}),? ?)+")


def main():
    problems = 0
    for path in sorted((build.ROOT / "data").glob("*/*.txt")):
        _, questions = build.parse(path)
        for n, q in enumerate(questions, 1):
            text, opts = q[1], q[2:6]
            where = f"{path.relative_to(build.ROOT)} Q{n}"
            if len({o.strip().lower() for o in opts}) < 4:
                print(f"{where}: duplicate options {opts}")
                problems += 1
            m = re.search(r"List II \([^)]*\): (.*)", text)
            if not m:
                continue
            items = [x.strip().rstrip(".").lower() for x in ROMAN.split(m.group(1)) if x.strip()]
            if len(set(items)) < len(items):
                print(f"{where}: List II has duplicate entries {items}")
                problems += 1
            for o in opts:
                if MAPPING.fullmatch(o.strip()):
                    rhs = re.findall(r"-(IV|V|I{1,3})", o)
                    if len(set(rhs)) != len(rhs):
                        print(f"{where}: option maps two items to one: {o}")
                        problems += 1
    print(f"{problems} problem(s) found")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
