#!/usr/bin/env python3
"""Convert the Markdown notes into LaTeX chapters for latex/main.tex.

Hand-made LaTeX (TikZ figures, typeset formulas and tables) lives in latex/art/<name>.tex.
A Markdown comment `<!-- latex: name -->` placed before a fenced block replaces that block
with \\input{art/name} in the book (GitHub still shows the Markdown/Mermaid version); a marker
not followed by a block simply inserts the art at that point.

Unmarked Mermaid diagrams fall back to \\diagram{figures/<id>-NN} (rendered to PDF by
render-diagrams.cjs). Everything else goes through pandoc + latex-filter.lua.
"""
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
LATEX = ROOT / 'latex'
CHAPTERS = LATEX / 'chapters'
BUILD = LATEX / 'build'
FILTER = pathlib.Path(__file__).resolve().parent / 'latex-filter.lua'


def file_id(rel):
    m = re.match(r'Paper-(\d)/(\d\d)', rel)
    if m:
        return f'p{m.group(1)}-{m.group(2)}'
    if rel.startswith('Revision/Formula'):
        return 'rev-formula'
    if rel.startswith('Revision/Study'):
        return 'rev-plan'
    return 'intro'


def sources():
    yield 'README.md'
    for paper in ('Paper-1', 'Paper-2'):
        for p in sorted((ROOT / paper).glob('*.md')):
            yield f'{paper}/{p.name}'
    yield 'Revision/Formula-Sheet.md'
    yield 'Revision/Study-Plan.md'


def intro_markdown():
    """The strategy parts of README.md (pattern, 250+ split, PYQ note, golden rules) — not the build notes."""
    md = (ROOT / 'README.md').read_text()
    end = md.find('## 7. Building') if '## 7. Building' in md else len(md)
    body = md[md.index('## 1. Exam Pattern'):md.index('## 3. Material Index')] + md[md.index('## 5. About the PYQs'):end]
    return '# Exam Pattern & the 250+ Strategy\n\n' + body


def timeline_table(src):
    lines = [l.strip() for l in src.splitlines() if l.strip()]
    title = next((l[6:] for l in lines if l.startswith('title ')), 'Timeline')
    rows = []
    for l in lines:
        if ' : ' in l:
            year, *events = [x.strip() for x in l.split(' : ')]
            rows.append(f'| **{year}** | {"; ".join(e.replace("|", "/") for e in events)} |')
    return f'**{title}**\n\n| Year | Event |\n|------|-------|\n' + '\n'.join(rows) + '\n'


ART = LATEX / 'art'
MARKER = re.compile(r'<!--\s*latex:\s*([\w-]+)\s*-->[ \t]*\n(?:[ \t]*\n)*(```[^\n]*\n.*?```)?', re.S)


def substitute_art(rel, md, used):
    def repl(m):
        name = m.group(1)
        if not (ART / f'{name}.tex').exists():
            raise SystemExit(f'{rel}: missing latex/art/{name}.tex')
        used.add(name)
        return f'```{{=latex}}\n\\input{{art/{name}}}\n```\n'
    return MARKER.sub(repl, md)


def preprocess(rel, md, jobs):
    fid = file_id(rel)
    counter = iter(range(1000))

    def repl(m):
        i = next(counter)
        src = m.group(1)
        if re.match(r'\s*timeline\b', src):
            return timeline_table(src)
        name = f'{fid}-{i:02d}'
        jobs.append({'name': name, 'src': src})
        return f'```{{=latex}}\n\\diagram{{figures/{name}}}\n```'

    return re.sub(r'```mermaid\n(.*?)```', repl, md, flags=re.S)


def main():
    CHAPTERS.mkdir(parents=True, exist_ok=True)
    BUILD.mkdir(parents=True, exist_ok=True)
    jobs, used = [], set()
    for rel in sources():
        md = intro_markdown() if rel == 'README.md' else (ROOT / rel).read_text()
        md = substitute_art(rel, md, used)
        md = preprocess(rel, md, jobs)
        fid = file_id(rel)
        out = CHAPTERS / f'{fid}.tex'
        subprocess.run([
            'pandoc', '-f', 'gfm+raw_attribute-tex_math_dollars', '-t', 'latex',
            '--top-level-division=chapter', '--wrap=preserve',
            '--lua-filter', str(FILTER),
            '-M', f'fileid={fid}', '-M', f'filedir={str(pathlib.PurePosixPath(rel).parent).replace(".", "")}',
            '-o', str(out),
        ], input=md, text=True, check=True)
        print(f'{rel:55s} -> chapters/{out.name}')
    (BUILD / 'diagrams.json').write_text(json.dumps(jobs, indent=1))
    print(f'{len(jobs)} Mermaid diagrams without hand-made art (rendered as fallback); {len(used)} art pieces used')
    unused = sorted(p.stem for p in ART.glob('*.tex') if p.stem not in used)
    if unused:
        print('art files not referenced by any marker:', ', '.join(unused))


if __name__ == '__main__':
    main()
