// Renders every Mermaid diagram listed in latex/build/diagrams.json to a vector PDF
// in latex/figures/, cropped to the diagram. Unchanged diagrams are skipped (hash check).
// Set CHROME_PATH to use an existing Chromium instead of puppeteer's bundled one.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const puppeteer = require('puppeteer');

const LATEX = path.resolve(__dirname, '..', 'latex');
const FIG = path.join(LATEX, 'figures');
const jobs = JSON.parse(fs.readFileSync(path.join(LATEX, 'build', 'diagrams.json'), 'utf8'));

(async () => {
  fs.mkdirSync(FIG, { recursive: true });
  const hash = s => crypto.createHash('sha1').update(s).digest('hex');
  const todo = jobs.filter(j => {
    const h = path.join(FIG, j.name + '.sha1');
    return !(fs.existsSync(path.join(FIG, j.name + '.pdf')) && fs.existsSync(h) && fs.readFileSync(h, 'utf8') === hash(j.src));
  });
  // Remove figures that no longer correspond to a diagram.
  const keep = new Set(jobs.map(j => j.name));
  for (const f of fs.readdirSync(FIG)) {
    if (!keep.has(f.replace(/\.(pdf|sha1)$/, ''))) fs.unlinkSync(path.join(FIG, f));
  }
  console.log(`${jobs.length} diagrams, ${todo.length} to render`);
  if (!todo.length) return;

  const browser = await puppeteer.launch({ executablePath: process.env.CHROME_PATH || undefined, args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setContent('<!doctype html><html><head><style>html,body{margin:0;padding:0;background:#fff}</style></head><body><div id="out"></div></body></html>');
  await page.addScriptTag({ path: require.resolve('mermaid/dist/mermaid.min.js') });
  await page.evaluate(() => mermaid.initialize({
    startOnLoad: false, theme: 'neutral', fontFamily: 'DejaVu Sans, sans-serif',
    flowchart: { useMaxWidth: false }, sequence: { useMaxWidth: false }, state: { useMaxWidth: false },
    class: { useMaxWidth: false }, er: { useMaxWidth: false }, pie: { useMaxWidth: false }, mindmap: { useMaxWidth: false },
  }));
  for (const job of todo) {
    const size = await page.evaluate(async (src, id) => {
      const { svg } = await mermaid.render(id, src);
      const out = document.getElementById('out');
      out.innerHTML = svg;
      const el = out.querySelector('svg');
      const vb = el.viewBox.baseVal;
      const w = Math.ceil(vb && vb.width ? vb.width : el.getBoundingClientRect().width);
      const h = Math.ceil(vb && vb.height ? vb.height : el.getBoundingClientRect().height);
      el.setAttribute('width', w); el.setAttribute('height', h); el.style.maxWidth = 'none';
      return { w, h };
    }, job.src, 'm' + job.name.replace(/[^a-z0-9]/gi, ''));
    await page.pdf({
      path: path.join(FIG, job.name + '.pdf'), width: `${size.w + 2}px`, height: `${size.h + 2}px`,
      printBackground: true, pageRanges: '1', margin: { top: 0, right: 0, bottom: 0, left: 0 },
    });
    fs.writeFileSync(path.join(FIG, job.name + '.sha1'), hash(job.src));
    process.stdout.write('.');
  }
  await browser.close();
  console.log('\ndone');
})();
