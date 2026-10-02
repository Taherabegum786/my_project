#!/usr/bin/env bash
# Rebuild the LaTeX book and PDF from the Markdown notes.
#   1. Markdown → latex/chapters/*.tex        (pandoc + latex-filter.lua)
#   2. Mermaid  → latex/figures/*.pdf         (headless Chromium; unchanged diagrams skipped)
#   3. LuaLaTeX twice (contents/links)        → UGC-NET-CS-Study-Material.pdf
# Needs: python3, pandoc ≥ 3, node ≥ 18 (run `npm install` in scripts/ once), LuaLaTeX (TeX Live)
# with TeX Gyre, DejaVu and GNU FreeFont fonts. Set CHROME_PATH to reuse an installed Chromium.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/md2latex.py
node scripts/render-diagrams.cjs
cd latex
for pass in 1 2; do
  lualatex -interaction=nonstopmode -halt-on-error main.tex > build/lualatex.log || { tail -40 build/lualatex.log; exit 1; }
done
cp main.pdf ../UGC-NET-CS-Study-Material.pdf
echo "PDF: UGC-NET-CS-Study-Material.pdf ($(grep -c 'Overfull \\hbox' main.log || true) overfull lines)"
