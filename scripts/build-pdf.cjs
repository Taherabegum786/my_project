// Builds UGC-NET-CS-Study-Material.pdf from the Markdown notes.
// Usage:  cd scripts && npm install && node build-pdf.cjs
// Set CHROME_PATH to use an existing Chromium/Chrome instead of puppeteer's download.
const fs = require('fs');
const path = require('path');
const { marked } = require('marked');
const puppeteer = require('puppeteer');

const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'UGC-NET-CS-Study-Material.pdf');

const PARTS = [
  { title: 'Paper 1 — Teaching & Research Aptitude', files: fs.readdirSync(path.join(ROOT, 'Paper-1')).sort().map(f => 'Paper-1/' + f) },
  { title: 'Paper 2 — Computer Science & Applications', files: fs.readdirSync(path.join(ROOT, 'Paper-2')).sort().map(f => 'Paper-2/' + f) },
  { title: 'Revision', files: ['Revision/Formula-Sheet.md', 'Revision/Study-Plan.md'] },
];

const fileId = rel => 'f-' + rel.replace(/\.md$/, '').replace(/[^A-Za-z0-9]+/g, '-');
const escapeHtml = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

// Mermaid timelines are unreadably small at A4 width, so print them as a year/event table instead.
function timelineTable(src) {
  const lines = src.split('\n').map(l => l.trim()).filter(Boolean);
  const title = (lines.find(l => l.startsWith('title ')) || '').slice(6);
  const rows = lines.filter(l => l.includes(' : ')).map(l => {
    const [year, ...events] = l.split(' : ');
    return `<tr><td class="year">${escapeHtml(year)}</td><td>${events.map(escapeHtml).join('<br>')}</td></tr>`;
  });
  return `<table class="timeline"><thead><tr><th colspan="2">${escapeHtml(title || 'Timeline')}</th></tr></thead><tbody>${rows.join('')}</tbody></table>`;
}

// Mermaid blocks become <pre class="mermaid"> so mermaid renders them in the browser.
const convertMermaid = md => md.replace(/```mermaid\n([\s\S]*?)```/g, (_, src) =>
  /^\s*timeline\b/.test(src) ? timelineTable(src) : `<pre class="mermaid">${escapeHtml(src)}</pre>`);

function render(rel) {
  let md = convertMermaid(fs.readFileSync(path.join(ROOT, rel), 'utf8'));
  let html = marked.parse(md, { gfm: true, headerIds: true, headerPrefix: fileId(rel) + '--', mangle: false });
  // Rewrite links to other notes (file.md or file.md#anchor) into in-document anchors.
  html = html.replace(/href="([^"#:]+\.md)(#[^"]*)?"/g, (_, target, anchor) => {
    const resolved = path.posix.normalize(path.posix.join(path.posix.dirname(rel), target));
    return `href="#${fileId(resolved)}${anchor ? '--' + anchor.slice(1) : ''}"`;
  });
  return `<section class="unit" id="${fileId(rel)}">${html}</section>`;
}

const firstHeading = rel => (fs.readFileSync(path.join(ROOT, rel), 'utf8').match(/^# (.*)$/m) || [, rel])[1];

let toc = '';
let body = '';
for (const part of PARTS) {
  toc += `<h3>${part.title}</h3><ol>`;
  body += `<section class="part-title"><h1>${part.title}</h1></section>`;
  for (const rel of part.files) {
    toc += `<li><a href="#${fileId(rel)}">${escapeHtml(firstHeading(rel))}</a></li>`;
    body += render(rel);
  }
  toc += '</ol>';
}

// The README's strategy sections (pattern, 250+ split, weightage) open the book.
const readme = fs.readFileSync(path.join(ROOT, 'README.md'), 'utf8');
const intro = readme.slice(readme.indexOf('## 1. Exam Pattern'), readme.indexOf('## 3. Material Index'))
  + readme.slice(readme.indexOf('## 5. About the PYQs'));
body = render_intro(intro) + body;
function render_intro(md) {
  md = convertMermaid(md);
  return `<section class="unit" id="intro"><h1>Exam Pattern &amp; the 250+ Strategy</h1>${marked.parse(md, { gfm: true, headerIds: true, headerPrefix: 'intro--', mangle: false })}</section>`;
}

const css = `
  @page { size: A4; margin: 16mm 13mm 18mm 13mm; }
  :root { --ink:#1b1f24; --muted:#57606a; --accent:#0b5cad; --rule:#d0d7de; --soft:#f3f6f9; }
  body { font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif; font-size: 10pt; line-height: 1.45; color: var(--ink); }
  h1 { font-size: 19pt; color: var(--accent); border-bottom: 2px solid var(--accent); padding-bottom: 4px; margin-top: 0; }
  h2 { font-size: 14pt; color: var(--accent); border-bottom: 1px solid var(--rule); padding-bottom: 2px; margin-top: 18px; break-after: avoid; }
  h3 { font-size: 11.5pt; margin-top: 14px; break-after: avoid; }
  h4 { font-size: 10.5pt; break-after: avoid; }
  a { color: var(--accent); text-decoration: none; }
  table { border-collapse: collapse; width: 100%; margin: 8px 0; font-size: 8.8pt; }
  th, td { border: 1px solid var(--rule); padding: 3px 6px; vertical-align: top; }
  th { background: var(--soft); }
  tr { break-inside: avoid; }
  table.timeline td.year { white-space: nowrap; font-weight: bold; color: var(--accent); width: 1%; }
  code { font-family: 'DejaVu Sans Mono', monospace; font-size: 8.8pt; background: var(--soft); padding: 0 2px; border-radius: 3px; }
  pre { font-family: 'DejaVu Sans Mono', monospace; background: var(--soft); border: 1px solid var(--rule); border-radius: 4px;
        padding: 6px 8px; font-size: 8.3pt; line-height: 1.3; white-space: pre; overflow: hidden; break-inside: avoid; }
  pre code { background: none; padding: 0; font-size: inherit; }
  pre.mermaid { background: none; border: none; text-align: center; white-space: normal; padding: 4px 0; }
  pre.mermaid svg { max-width: 100%; max-height: 200mm; height: auto; }
  blockquote { border-left: 3px solid var(--accent); margin: 8px 0; padding: 2px 10px; color: var(--muted); }
  ul, ol { padding-left: 20px; }
  li { margin: 1px 0; }
  li input[type=checkbox] { margin-right: 5px; }
  li:has(> input[type=checkbox]) { list-style: none; margin-left: -16px; }
  .unit { break-before: page; }
  .part-title { break-before: page; height: 240mm; display: flex; align-items: center; justify-content: center; }
  .part-title h1 { font-size: 26pt; border: none; text-align: center; }
  .cover { height: 255mm; display: flex; flex-direction: column; justify-content: center; text-align: center; }
  .cover h1 { font-size: 30pt; border: none; margin-bottom: 6px; }
  .cover .sub { font-size: 14pt; color: var(--muted); }
  .cover .target { margin: 28px auto 0; padding: 10px 18px; border: 2px solid var(--accent); border-radius: 8px; font-size: 13pt; display: inline-block; }
  .toc { break-before: page; }
  .toc ol { font-size: 10.5pt; line-height: 1.8; }
`;

const html = `<!doctype html><html><head><meta charset="utf-8"><title>UGC NET CS Study Material</title><style>${css}</style></head><body>
<section class="cover">
  <h1>UGC NET Computer Science</h1>
  <div class="sub">Complete Study Material · Paper 1 &amp; Paper 2 (Code 87)</div>
  <div class="sub">Notes · Diagrams · Worked examples · PYQ-pattern questions with answers</div>
  <div><span class="target">Target: 250+ / 300 &nbsp;≈&nbsp; 126 of 150 correct</span></div>
</section>
<section class="toc"><h1>Contents</h1><ol><li><a href="#intro">Exam Pattern &amp; the 250+ Strategy</a></li></ol>${toc}</section>
${body}
</body></html>`;

(async () => {
  const browser = await puppeteer.launch({ executablePath: process.env.CHROME_PATH || undefined, args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setContent(html, { waitUntil: 'load' });
  await page.addScriptTag({ path: require.resolve('mermaid/dist/mermaid.min.js') });
  const report = await page.evaluate(async () => {
    mermaid.initialize({ startOnLoad: false, theme: 'neutral', securityLevel: 'loose', fontFamily: 'DejaVu Sans' });
    await mermaid.run({ querySelector: 'pre.mermaid' });
    // Shrink ASCII diagrams that are wider than the page instead of clipping them.
    let shrunk = 0;
    for (const pre of document.querySelectorAll('pre:not(.mermaid)')) {
      let size = 8.3;
      while (pre.scrollWidth > pre.clientWidth && size > 5.5) { size -= 0.3; pre.style.fontSize = size + 'pt'; }
      if (size < 8.3) shrunk++;
    }
    const ids = new Set([...document.querySelectorAll('[id]')].map(e => e.id));
    const broken = [...document.querySelectorAll('a[href^="#"]')].map(a => a.getAttribute('href').slice(1)).filter(id => !ids.has(id));
    return { diagrams: document.querySelectorAll('pre.mermaid svg').length, shrunk, broken };
  });
  console.log(`mermaid diagrams rendered: ${report.diagrams}; ASCII blocks shrunk to fit: ${report.shrunk}`);
  if (report.broken.length) console.log('broken internal links:', report.broken);
  await page.pdf({
    path: OUT, format: 'A4', printBackground: true, displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: '<div style="width:100%;font-size:8px;color:#57606a;padding:0 13mm;display:flex;justify-content:space-between;font-family:DejaVu Sans,sans-serif"><span>UGC NET Computer Science — Study Material</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
    margin: { top: '16mm', bottom: '18mm', left: '13mm', right: '13mm' },
  });
  await browser.close();
  console.log('wrote', OUT);
})();
