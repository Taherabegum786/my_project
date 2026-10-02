-- Pandoc Lua filter used by md2latex.py to turn the Markdown notes into book chapters.
--  * "# Paper 2 · Unit 7 — Title"  → \unitchapter{2}{7}{Title}{id}  (other chapters → \plainchapter)
--  * "## 3. Keys" → \section{Keys}: manual numbers are dropped, LaTeX numbers sections itself
--  * hand-made art (\input{art/…}, inserted by md2latex.py) passes through untouched
--  * remaining code blocks → listing environment, font size chosen so the widest line fits
--  * tables → column widths from content length, bold header
--  * "Syllabus Checklist" / "Quick Revision Box" sections → framed environments
--  * links between notes → internal PDF links

local fileid, filedir

local function id_for(path)
  local p, n = path:match('^Paper%-(%d)/(%d%d)')
  if p then return 'p' .. p .. '-' .. n end
  if path:match('^Revision/Formula') then return 'rev-formula' end
  if path:match('^Revision/Study') then return 'rev-plan' end
  if path:match('README') then return 'intro' end
  return nil
end

local function normalize(path)
  local parts = {}
  for seg in path:gmatch('[^/]+') do
    if seg == '..' then table.remove(parts) elseif seg ~= '.' then table.insert(parts, seg) end
  end
  return table.concat(parts, '/')
end

local function latex_inlines(inlines)
  return (pandoc.write(pandoc.Pandoc({ pandoc.Plain(inlines) }), 'latex'):gsub('%s+$', ''))
end

-- ---------- code / listing blocks ----------
local TEXT_PT = 440   -- usable width of a listing (text width minus indentation), pt
local MONO_EM = 0.6   -- advance width of the monospaced font, em

local function code_block(el)
  local lines, maxlen = {}, 1
  for line in (el.text .. '\n'):gmatch('(.-)\n') do
    table.insert(lines, line)
    local n = utf8.len(line) or #line
    if n > maxlen then maxlen = n end
  end
  local size = math.min(9, TEXT_PT / (MONO_EM * maxlen))
  size = math.max(5.2, math.floor(size * 10) / 10)
  local lead = math.floor(size * 1.22 * 10) / 10
  local height = math.ceil(#lines * lead + 20)
  return pandoc.RawBlock('latex', string.format(
    '\\begin{listingblock}{%dpt}\n\\begin{Verbatim}[fontsize=\\fontsize{%.1f}{%.1f}\\selectfont]\n%s\n\\end{Verbatim}\n\\end{listingblock}',
    height, size, lead, table.concat(lines, '\n')))
end

-- ---------- tables ----------
local CAP = 96 -- line width at \small, in "average lowercase letter" units

local function wlen(s)
  local n = 0
  for _, c in utf8.codes(s) do
    if c >= 65 and c <= 90 then n = n + 1.35
    elseif c == 109 or c == 119 then n = n + 1.4
    elseif c == 105 or c == 108 or c == 106 or c == 116 or c == 102 or c == 114 then n = n + 0.65
    elseif c == 32 then n = n + 0.55
    elseif c >= 48 and c <= 57 then n = n + 1.0
    elseif c < 128 then n = n + 0.8
    else n = n + 1.3 end
  end
  return n
end

local function cell_len(cell, bold)
  local s = pandoc.utils.stringify(cell.contents)
  local f = bold and 1.12 or 1.0
  local longest = 0
  for w in s:gmatch('%S+') do longest = math.max(longest, wlen(w) * f) end
  return wlen(s) * f + 1.5, longest + 2.2
end

local function table_widths(tbl)
  local n = #tbl.colspecs
  local nat, minw = {}, {}
  for i = 1, n do nat[i], minw[i] = 3, 3 end
  local function scan(rows, bold)
    for _, row in ipairs(rows) do
      for i, cell in ipairs(row.cells) do
        if i <= n then
          local l, w = cell_len(cell, bold)
          nat[i] = math.max(nat[i], math.min(l, 400))
          minw[i] = math.max(minw[i], math.min(w, 26))
        end
      end
    end
  end
  scan(tbl.head.rows, true)
  for _, body in ipairs(tbl.bodies) do scan(body.body) end
  local avail = CAP - 3 * n
  local total = 0
  for i = 1, n do total = total + nat[i] end
  local width = {}
  if total <= avail then
    for i = 1, n do width[i] = nat[i] / avail end
    return width
  end
  local fixed, remaining, changed = {}, avail, true
  while changed do
    changed = false
    local k = 0
    for i = 1, n do if not fixed[i] then k = k + 1 end end
    if k == 0 then break end
    local share = remaining / k
    for i = 1, n do
      if not fixed[i] and nat[i] <= share then
        fixed[i] = nat[i]; remaining = remaining - nat[i]; changed = true
      end
    end
  end
  local sum = 0
  for i = 1, n do if not fixed[i] then sum = sum + nat[i] end end
  for i = 1, n do width[i] = fixed[i] or math.max(minw[i] + 1, remaining * nat[i] / sum) end
  local s = 0
  for i = 1, n do s = s + width[i] end
  for i = 1, n do width[i] = width[i] / s end
  return width
end

local function bold_header(tbl)
  for _, row in ipairs(tbl.head.rows) do
    for _, cell in ipairs(row.cells) do
      cell.contents = cell.contents:walk({
        Plain = function(p) return pandoc.Plain({ pandoc.Strong(p.content) }) end,
        Para = function(p) return pandoc.Plain({ pandoc.Strong(p.content) }) end,
      })
    end
  end
end

local function breakable(tbl)
  return tbl:walk({
    Str = function(el)
      if not el.text:find('[→/]') or utf8.len(el.text) < 12 then return nil end
      local out, buf = {}, ''
      for _, c in utf8.codes(el.text) do
        buf = buf .. utf8.char(c)
        if c == 0x2192 or c == 47 then
          table.insert(out, pandoc.Str(buf)); table.insert(out, pandoc.RawInline('latex', '\\allowbreak{}')); buf = ''
        end
      end
      if buf ~= '' then table.insert(out, pandoc.Str(buf)) end
      return out
    end,
  })
end

local function do_table(tbl)
  tbl = breakable(tbl)
  local w = table_widths(tbl)
  for i, spec in ipairs(tbl.colspecs) do tbl.colspecs[i] = { spec[1], w[i] } end
  bold_header(tbl)
  return { pandoc.RawBlock('latex', '\\begingroup\\small'), tbl, pandoc.RawBlock('latex', '\\endgroup') }
end

-- ---------- headers & links ----------
local function strip_number(inlines)
  -- drop a leading "3." / "1.4" / "12.3.1" and the following space
  if #inlines >= 2 and inlines[1].t == 'Str' and inlines[1].text:match('^%d+[%.%d]*$') and inlines[2].t == 'Space' then
    local out = {}
    for i = 3, #inlines do out[#out + 1] = inlines[i] end
    return out
  end
  return inlines
end

local function do_header(h)
  if h.level == 1 then
    local text = pandoc.utils.stringify(h.content)
    local paper, unit, title = text:match('^Paper (%d) · Unit (%d+) — (.+)$')
    if paper then
      local title_tex = latex_inlines(pandoc.read(title, 'gfm').blocks[1].content)
      return pandoc.RawBlock('latex', string.format('\\unitchapter{%s}{%s}{%s}{%s}', paper, unit, title_tex, fileid))
    end
    return pandoc.RawBlock('latex', string.format('\\plainchapter{%s}{%s}', latex_inlines(h.content), fileid))
  end
  h.identifier = fileid .. '--' .. h.identifier
  h.content = strip_number(h.content)
  return h
end

local function do_link(l)
  local target = l.target
  if target:match('^%a+:') then return l end
  local path, anchor = target:match('^([^#]*%.md)(#?.*)$')
  if not path then return l end
  local full = normalize((filedir ~= '' and (filedir .. '/') or '') .. path)
  local id = id_for(full)
  if not id then return l end
  if anchor ~= '' then l.target = '#' .. id .. '--' .. anchor:sub(2) else l.target = '#' .. id end
  return l
end

-- ---------- boxed sections ----------
local BOXES = { ['Syllabus Checklist'] = 'sylbox', ['Quick Revision Box'] = 'revbox' }

local function box_sections(blocks)
  local out, open = {}, nil
  for _, b in ipairs(blocks) do
    if b.t == 'Header' and b.level <= 2 then
      if open then table.insert(out, pandoc.RawBlock('latex', '\\end{' .. open .. '}')); open = nil end
      local env = BOXES[pandoc.utils.stringify(b.content)]
      if env then
        table.insert(out, pandoc.RawBlock('latex', '\\begin{' .. env .. '}'))
        open = env
      else
        table.insert(out, b)
      end
    else
      table.insert(out, b)
    end
  end
  if open then table.insert(out, pandoc.RawBlock('latex', '\\end{' .. open .. '}')) end
  return out
end

-- Keep a heading with what follows: reserve the height of a listing that directly follows,
-- or a few lines otherwise, so a heading never ends a page.
local function keep_headings(blocks)
  local out = {}
  for i, b in ipairs(blocks) do
    if b.t == 'Header' then
      local extra, paras, reserve = 50, 0, nil
      for j = i + 1, math.min(i + 5, #blocks) do
        local nb = blocks[j]
        local h = nb.t == 'RawBlock' and nb.text:match('^\\begin{listingblock}{(%d+)pt}')
        if h then reserve = math.min(tonumber(h) + extra, 560); break
        elseif nb.t == 'RawBlock' and nb.text:match('^\\begingroup\\small') then reserve = extra + 80; break
        elseif nb.t == 'Header' then extra = extra + 36
        elseif (nb.t == 'Para' or nb.t == 'Plain') and paras < 2 then extra = extra + 30; paras = paras + 1
        else break end
      end
      table.insert(out, pandoc.RawBlock('latex', string.format('\\needspace{%dpt}', reserve or (extra + 45))))
    end
    table.insert(out, b)
  end
  return out
end

function Pandoc(doc)
  fileid = pandoc.utils.stringify(doc.meta.fileid)
  filedir = pandoc.utils.stringify(doc.meta.filedir or '')
  doc.blocks = box_sections(doc.blocks)
  doc = doc:walk({
    Link = do_link,
    CodeBlock = code_block,
    Table = do_table,
    HorizontalRule = function() return {} end,
  })
  doc = doc:walk({ Header = do_header })
  -- "Expected questions: …" line under the chapter title → \unitmeta
  for i, b in ipairs(doc.blocks) do
    if (b.t == 'Para' or b.t == 'Plain') and pandoc.utils.stringify(b.content):match('^Expected questions') then
      local inl = (#b.content == 1 and b.content[1].t == 'Strong') and b.content[1].content or b.content
      doc.blocks[i] = pandoc.RawBlock('latex', '\\unitmeta{' .. latex_inlines(inl) .. '}')
      break
    end
  end
  doc.blocks = keep_headings(doc.blocks)
  return doc
end
