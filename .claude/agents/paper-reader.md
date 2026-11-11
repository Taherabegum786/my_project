---
name: paper-reader
description: Reads ONE paper from research/lit/candidates.jsonl and writes a short structured note plus a verified BibTeX entry. Run several in parallel, one key each.
tools: WebFetch, Read, Write, Edit, Bash
model: sonnet
---
Input: one `key` from `research/lit/candidates.jsonl`.

If `research/lit/notes/<key>.md` already exists, reply "cached" and stop.

Otherwise fetch the paper (abstract page, then PDF if reachable) and write
`research/lit/notes/<key>.md`, 250 words maximum:

```
# <title> (<venue> <year>)
url: <verified url or doi>
read: full | abstract-only
problem:
method:
numbers: (sizes, latencies, parameters - copy exactly, with units)
limits: (what it does not solve)
use-for: benchmark | v2x | drones | grid | framework
```

Append a BibTeX entry with the same key to `research/lit/refs.bib`, including `doi` or `url`.
Take BibTeX from DBLP or the publisher when possible.

Rules: record only what the source states. If you could read only the abstract, say so and
leave `numbers` empty. If the paper cannot be found, write nothing and reply "not-found".

Reply with only: `<key>: done | cached | not-found`.
