#!/usr/bin/env bash
# Rebuild the LaTeX book and PDF from the Markdown notes.
#   1. Markdown → latex/chapters/*.tex        (pandoc + latex-filter.lua)
#   2. Unmarked Mermaid blocks → latex/figures/*.pdf (headless Chromium; skipped when there are none)
#   3. LuaLaTeX twice (contents/links)        → UGC-NET-CS-Study-Material.pdf
# Needs: python3, pandoc ≥ 3, LuaLaTeX (TeX Live) with TeX Gyre, DejaVu and GNU FreeFont fonts;
# node ≥ 18 (`npm install` in scripts/) only when unmarked Mermaid diagrams exist. Set CHROME_PATH to reuse an installed Chromium.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/md2latex.py
if [ "$(tr -d ' \n' < latex/build/diagrams.json)" != "[]" ]; then node scripts/render-diagrams.cjs; fi
cd latex
for pass in 1 2; do
  lualatex -interaction=nonstopmode -halt-on-error main.tex > build/lualatex.log || { tail -40 build/lualatex.log; exit 1; }
done
cp main.pdf ../UGC-NET-CS-Study-Material.pdf
echo "PDF: UGC-NET-CS-Study-Material.pdf ($(grep -c 'Overfull \\hbox' main.log || true) overfull lines)"
