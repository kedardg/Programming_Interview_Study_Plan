"""Build index.html from README.md.

Run from the repository root:

    python3 scripts/build_index.py

The page shows the whole plan with every item linked, checkboxes that remember
progress in the browser, and a search box. In the 3-Month Schedule, "#12"
links to Blind 75 problem 12, "L9" to GPU MODE lecture 9 and "Ch 4" to system
design chapter 4.
"""

import hashlib
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
OUT = ROOT / "index.html"

LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
ITEM = re.compile(r"^( *)(-|\d+\.) (.*)$")
STEP_HEADING = re.compile(r"^Step (\d+) - (.+)$")
STEP_REF = re.compile(r"\b(Steps? )(\d+)((?:\s*[-–]\s*\d+)?)")
PROBLEM_REF = re.compile(r"#(\d+(?:–\d+)?(?:, \d+(?:–\d+)?)*)")
LECTURE_REF = re.compile(r"\bL(\d+)\b")
CHAPTER_REF = re.compile(r"\bCh (\d+(?:–\d+)?(?:, \d+(?:–\d+)?)*)")
DIFFICULTY = re.compile(r" - (Easy|Medium|Hard)( \(Premium\))?$")


def esc(text):
    return html.escape(text, quote=True)


def slug(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def plain(text):
    return LINK.sub(lambda m: m.group(1), text).replace("**", "").replace("`", "")


def key_for(*parts):
    return hashlib.sha1("|".join(parts).encode()).hexdigest()[:12]


def expand(numbers):
    out = []
    for part in numbers.split(", "):
        lo, _, hi = part.partition("–")
        out.extend(range(int(lo), int(hi or lo) + 1))
    return out


class Index:
    """Problems, lectures and chapters found in the README, for linking references."""

    def __init__(self, sections):
        self.problems, self.lectures, self.chapters = {}, {}, {}
        for sid, _, lines in sections:
            for line in lines:
                m = ITEM.match(line)
                if not m:
                    continue
                text = m.group(3)
                link = LINK.search(text)
                if sid == "step-4" and m.group(2) != "-" and link:
                    diff = DIFFICULTY.search(text)
                    self.problems[int(m.group(2)[:-1])] = (link.group(1), link.group(2), diff.group(1) if diff else "")
                lec = re.match(r"Lecture (\d+): (.+?)(?: - |$)", text)
                if lec:
                    self.lectures[int(lec.group(1))] = (plain(lec.group(2)), link.group(2) if link else "")
                if link and "system-design-notes/tree/" in link.group(2) and m.group(2) != "-":
                    self.chapters[int(m.group(2)[:-1])] = (link.group(1), link.group(2))


class Renderer:
    def __init__(self, index):
        self.index = index

    def inline(self, text, refs=False):
        out, pos = [], 0
        for m in LINK.finditer(text):
            out.append(self.text(text[pos:m.start()], refs))
            out.append(f'<a href="{esc(m.group(2))}" target="_blank" rel="noopener">{self.text(m.group(1), False, steps=False)}</a>')
            pos = m.end()
        out.append(self.text(text[pos:], refs))
        return "".join(out)

    def text(self, text, refs, steps=True):
        parts = text.split("`")
        out = []
        for i, part in enumerate(parts):
            if i % 2:
                out.append(f"<code>{esc(part)}</code>")
                continue
            part = re.sub(r"\*\*(.+?)\*\*", lambda m: f"\x00b{m.group(1)}\x00/b", part)
            part = esc(part).replace("\x00b", "<strong>").replace("\x00/b", "</strong>")
            if steps:
                part = STEP_REF.sub(lambda m: f'<a class="stepref" href="#step-{m.group(2)}">{m.group(0)}</a>', part)
            if refs:
                part = PROBLEM_REF.sub(self.problem_chips, part)
                part = LECTURE_REF.sub(self.lecture_chip, part)
                part = CHAPTER_REF.sub(self.chapter_chips, part)
            out.append(part)
        return "".join(out)

    def problem_chips(self, m):
        chips = []
        for n in expand(m.group(1)):
            title, url, diff = self.index.problems[n]
            chips.append(f'<a class="chip lc d-{diff.lower()}" href="{esc(url)}" target="_blank" rel="noopener" '
                         f'title="{esc(f"#{n} {title} ({diff})")}">#{n}</a>')
        return "".join(chips)

    def lecture_chip(self, m):
        n = int(m.group(1))
        title, url = self.index.lectures[n]
        href = esc(url) if url else f"#lecture-{n}"
        target = ' target="_blank" rel="noopener"' if url else ""
        return f'<a class="chip lec" href="{href}"{target} title="{esc(f"Lecture {n}: {title}")}">L{n}</a>'

    def chapter_chips(self, m):
        chips = []
        for n in expand(m.group(1)):
            title, url = self.index.chapters[n]
            chips.append(f'<a class="chip ch" href="{esc(url)}" target="_blank" rel="noopener" '
                         f'title="{esc(f"Chapter {n}: {title}")}">Ch {n}</a>')
        return "".join(chips)

    def blocks(self, sid, lines, refs=False, ticks=True):
        out, i, sub = [], 0, ""
        while i < len(lines):
            line = lines[i]
            if not line.strip():
                i += 1
            elif line.startswith("###### "):
                sub = line[7:].strip()
                out.append(f"<h3>{self.inline(sub)}</h3>")
                i += 1
            elif line.startswith("|"):
                rows = []
                while i < len(lines) and lines[i].startswith("|"):
                    rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                    i += 1
                out.append(self.table(rows, refs))
            elif ITEM.match(line):
                items = []
                while i < len(lines) and ITEM.match(lines[i]):
                    items.append(lines[i])
                    i += 1
                tick = ticks and (sid.startswith("step-") and not sub.startswith("How to") or sub.startswith("Weeks"))
                out.append(self.list(sid, items, refs, tick))
            else:
                para = []
                while i < len(lines) and lines[i].strip() and not ITEM.match(lines[i]) \
                        and not lines[i].startswith(("|", "###### ")):
                    para.append(lines[i].strip())
                    i += 1
                text = " ".join(para)
                if "index.html" not in text:
                    out.append(f"<p>{self.inline(text, refs)}</p>")
        return "\n".join(out)

    def table(self, rows, refs):
        head, body = rows[0], [r for r in rows[2:]]
        out = ['<div class="table-wrap"><table class="schedule"><thead><tr>']
        out += [f"<th>{self.inline(c)}</th>" for c in head]
        out.append("</tr></thead><tbody>")
        for row in body:
            week = row[0]
            out.append(f'<tr class="week" data-text="{esc(plain(" ".join(row)).lower())}">')
            out.append(f'<td class="wk"><label><input type="checkbox" class="tick" data-key="week-{esc(week)}" '
                       f'aria-label="Week {esc(week)} done"><span>{esc(week)}</span></label></td>')
            out += [f"<td>{self.inline(c, refs)}</td>" for c in row[1:]]
            out.append("</tr>")
        out.append("</tbody></table></div>")
        return "".join(out)

    def list(self, sid, items, refs, tick):
        ordered = items[0].lstrip()[0].isdigit()
        out, depth_stack = [], []

        def open_list(line):
            m = ITEM.match(line)
            if m.group(2) == "-":
                return "<ul>", "</ul>"
            return f'<ol start="{m.group(2)[:-1]}">', "</ol>"

        for line in items:
            m = ITEM.match(line)
            indent, marker, text = len(m.group(1)), m.group(2), m.group(3)
            while depth_stack and indent < depth_stack[-1][0]:
                out.append("</li>" + depth_stack.pop()[1])
            if depth_stack and indent == depth_stack[-1][0]:
                out.append("</li>")
            elif not depth_stack or indent > depth_stack[-1][0]:
                tag_open, tag_close = open_list(line)
                out.append(tag_open)
                depth_stack.append((indent, tag_close))
            attrs = ""
            if sid == "step-4" and marker != "-":
                attrs = f' id="problem-{marker[:-1]}"'
            lec = re.match(r"Lecture (\d+):", text)
            if lec:
                attrs = f' id="lecture-{lec.group(1)}"'
            body = self.inline(DIFFICULTY.sub("", text) if sid == "step-4" else text, refs)
            diff = DIFFICULTY.search(text) if sid == "step-4" else None
            if diff:
                body += f' <span class="badge d-{diff.group(1).lower()}">{diff.group(1)}</span>'
                if diff.group(2):
                    body += ' <span class="badge premium">Premium</span>'
            box = ""
            if tick:
                box = (f'<input type="checkbox" class="tick" data-key="{key_for(sid, plain(text))}" '
                       f'aria-label="Done: {esc(plain(text)[:80])}">')
            out.append(f'<li class="item"{attrs}>{box}<div class="body">{body}</div>')
        while depth_stack:
            out.append("</li>" + depth_stack.pop()[1])
        return "".join(out)


def parse(readme):
    lines = readme.splitlines()
    title = lines[0].lstrip("# ").replace("_", " ")
    intro, sections, cur = [], [], None
    for line in lines[1:]:
        if line.startswith("## "):
            heading = line[3:].strip()
            m = STEP_HEADING.match(heading)
            sid = f"step-{m.group(1)}" if m else slug(heading)
            cur = (sid, heading, [])
            sections.append(cur)
        elif cur:
            cur[2].append(line)
        else:
            intro.append(line)
    return title, intro, sections


def build():
    title, intro, sections = parse(README.read_text())
    index = Index(sections)
    r = Renderer(index)
    toc, body = [], []
    for sid, heading, lines in sections:
        m = STEP_HEADING.match(heading)
        label = (f'<span class="num">{m.group(1)}</span>{esc(m.group(2))}' if m else esc(heading))
        toc.append(f'<li><a href="#{sid}">{label}</a><span class="count" data-count="{sid}"></span></li>')
        h2 = (f'<span class="num">Step {m.group(1)}</span> {r.inline(m.group(2))}' if m else r.inline(heading))
        refs = not m
        body.append(f'<section id="{sid}" class="block"><div class="block-head"><h2>{h2}</h2>'
                    f'<span class="count" data-count="{sid}"></span></div>'
                    f"{r.blocks(sid, lines, refs=refs)}</section>")
    page = TEMPLATE.format(
        title=esc(title),
        intro=r.blocks("intro", intro, ticks=False),
        toc="\n".join(toc),
        body="\n".join(body),
        n_problems=len(index.problems), n_lectures=len(index.lectures), n_chapters=len(index.chapters),
    )
    OUT.write_text(page)
    print(f"Wrote {OUT.relative_to(ROOT)}: {len(sections)} sections, {len(index.problems)} problems, "
          f"{len(index.lectures)} lectures, {len(index.chapters)} chapters")


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
:root {{
  --bg: #f7f7f5; --surface: #ffffff; --text: #1d1d1f; --muted: #66666b; --border: #e3e1dc;
  --accent: #3550c8; --accent-weak: #e9edfb; --chip: #f0f0ee; --done: #2b8a3e;
  --easy: #2b8a3e; --medium: #b06a00; --hard: #c92a2a;
  --radius: 10px; --shadow: 0 1px 2px rgba(0,0,0,.05);
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --bg: #131315; --surface: #1b1b1e; --text: #ececee; --muted: #9c9ca3; --border: #2c2c31;
    --accent: #93a6ff; --accent-weak: #232a47; --chip: #26262b; --done: #69db7c;
    --easy: #69db7c; --medium: #ffc078; --hard: #ff8787; --shadow: none;
  }}
}}
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; scroll-padding-top: 76px; }}
body {{ margin: 0; background: var(--bg); color: var(--text);
  font: 15px/1.55 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }}
a {{ color: var(--accent); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
code {{ font: 13px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; background: var(--chip);
  padding: 1px 5px; border-radius: 5px; }}
.top {{ position: sticky; top: 0; z-index: 5; background: color-mix(in srgb, var(--bg) 92%, transparent);
  backdrop-filter: blur(8px); border-bottom: 1px solid var(--border); }}
.top-inner {{ max-width: 1240px; margin: 0 auto; padding: 10px 16px; display: flex; gap: 16px;
  align-items: center; flex-wrap: wrap; }}
.top h1 {{ font-size: 17px; margin: 0; letter-spacing: -.01em; }}
.progress {{ display: flex; align-items: center; gap: 10px; flex: 1 1 220px; min-width: 180px; }}
.bar {{ flex: 1; height: 8px; background: var(--chip); border-radius: 99px; overflow: hidden; }}
.bar span {{ display: block; height: 100%; width: 0; background: var(--done); transition: width .2s; }}
.progress small {{ color: var(--muted); white-space: nowrap; font-variant-numeric: tabular-nums; }}
.controls {{ display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }}
.controls input[type=search] {{ width: 220px; max-width: 100%; padding: 6px 10px; border-radius: 8px;
  border: 1px solid var(--border); background: var(--surface); color: var(--text); font: inherit; }}
.controls label {{ color: var(--muted); font-size: 13px; display: flex; gap: 6px; align-items: center; }}
.controls button {{ font: inherit; font-size: 13px; color: var(--muted); background: none;
  border: 1px solid var(--border); border-radius: 8px; padding: 5px 10px; cursor: pointer; }}
.layout {{ max-width: 1240px; margin: 0 auto; padding: 20px 16px 60px; display: grid;
  grid-template-columns: 260px minmax(0, 1fr); gap: 28px; }}
nav.toc {{ position: sticky; top: 76px; align-self: start; max-height: calc(100vh - 96px); overflow: auto;
  font-size: 13.5px; }}
nav.toc ol {{ list-style: none; margin: 0; padding: 0; }}
nav.toc li {{ display: flex; justify-content: space-between; gap: 8px; padding: 3px 0; }}
nav.toc a {{ color: var(--text); display: flex; gap: 8px; }}
nav.toc .num {{ color: var(--muted); min-width: 18px; font-variant-numeric: tabular-nums; }}
nav.toc .count {{ color: var(--muted); font-size: 12px; white-space: nowrap; font-variant-numeric: tabular-nums; }}
nav.toc .count.full {{ color: var(--done); }}
main {{ min-width: 0; }}
.intro {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 18px 22px; box-shadow: var(--shadow); margin-bottom: 18px; }}
.intro h2 {{ margin: 0 0 6px; font-size: 22px; letter-spacing: -.02em; }}
.intro .stats {{ color: var(--muted); font-size: 13px; margin: 0 0 8px; }}
.block {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 16px 22px; margin-bottom: 14px; box-shadow: var(--shadow); }}
.block-head {{ display: flex; justify-content: space-between; align-items: baseline; gap: 12px; }}
.block h2 {{ font-size: 18px; margin: 4px 0 10px; letter-spacing: -.01em; }}
.block h2 .num {{ color: var(--muted); font-weight: 500; margin-right: 4px; }}
.block-head .count {{ color: var(--muted); font-size: 13px; white-space: nowrap; font-variant-numeric: tabular-nums; }}
.block h3 {{ font-size: 13px; text-transform: uppercase; letter-spacing: .05em; color: var(--muted);
  margin: 18px 0 6px; font-weight: 600; }}
ul, ol {{ margin: 4px 0; padding-left: 22px; }}
li.item {{ margin: 3px 0; }}
li.item > .body {{ display: inline; }}
li.item > input.tick {{ margin: 0 8px 0 -2px; vertical-align: -2px; accent-color: var(--done); }}
li.item.done > .body {{ color: var(--muted); }}
li.item.done > .body a {{ color: var(--muted); }}
li.item.done > .body > a:first-child {{ text-decoration: line-through; }}
.badge {{ font-size: 11px; padding: 1px 6px; border-radius: 99px; border: 1px solid currentColor;
  margin-left: 2px; vertical-align: 1px; }}
.d-easy {{ color: var(--easy); }} .d-medium {{ color: var(--medium); }} .d-hard {{ color: var(--hard); }}
.badge.premium {{ color: var(--muted); }}
.table-wrap {{ overflow-x: auto; margin: 6px 0; border: 1px solid var(--border); border-radius: 8px; }}
table.schedule {{ border-collapse: collapse; width: 100%; font-size: 13.5px; }}
.schedule th, .schedule td {{ text-align: left; vertical-align: top; padding: 8px 10px;
  border-bottom: 1px solid var(--border); }}
.schedule th {{ background: var(--chip); font-size: 12px; font-weight: 600; color: var(--muted); }}
.schedule tr:last-child td {{ border-bottom: 0; }}
.schedule td.wk label {{ display: flex; gap: 6px; align-items: center; font-weight: 600; }}
.schedule td.wk input {{ accent-color: var(--done); }}
.schedule tr.done td {{ color: var(--muted); background: color-mix(in srgb, var(--done) 7%, transparent); }}
.chip {{ display: inline-block; font-size: 12px; line-height: 1.5; padding: 0 6px; margin: 1px 2px 1px 0;
  border-radius: 6px; background: var(--chip); color: var(--text); font-variant-numeric: tabular-nums; }}
.chip:hover {{ text-decoration: none; background: var(--accent-weak); }}
.chip.lc {{ font-weight: 600; }}
.chip.lc.d-easy {{ color: var(--easy); }} .chip.lc.d-medium {{ color: var(--medium); }} .chip.lc.d-hard {{ color: var(--hard); }}
.chip.lec {{ background: var(--accent-weak); color: var(--accent); }}
.chip.ch {{ outline: 1px solid var(--border); }}
.stepref {{ border-bottom: 1px dotted currentColor; }}
.stepref:hover {{ text-decoration: none; }}
.hidden {{ display: none !important; }}
.empty {{ color: var(--muted); padding: 30px 0; text-align: center; }}
footer {{ color: var(--muted); font-size: 12.5px; text-align: center; padding: 10px 16px 30px; }}
@media (max-width: 900px) {{
  .layout {{ grid-template-columns: 1fr; gap: 14px; }}
  nav.toc {{ position: static; max-height: none; background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 10px 14px; }}
  nav.toc details summary {{ cursor: pointer; font-weight: 600; }}
  .block, .intro {{ padding: 14px 16px; }}
  .controls input[type=search] {{ width: 100%; }}
  .controls {{ width: 100%; }}
  table.schedule {{ min-width: 760px; }}
}}
</style>
</head>
<body>
<header class="top"><div class="top-inner">
  <h1>{title}</h1>
  <div class="progress"><div class="bar"><span id="bar"></span></div><small id="overall"></small></div>
  <div class="controls">
    <input type="search" id="q" placeholder="Search lectures, problems, papers..." aria-label="Search">
    <label><input type="checkbox" id="hide-done"> Hide done</label>
    <button type="button" id="reset">Reset progress</button>
  </div>
</div></header>
<div class="layout">
  <nav class="toc"><details open id="toc-details"><summary>Contents</summary><ol>
{toc}
  </ol></details></nav>
  <main>
    <div class="intro"><h2>About this plan</h2>
      <p class="stats">{n_problems} problems, {n_lectures} GPU MODE lectures, {n_chapters} system design chapters. Tick items off as you go; progress is saved in this browser.</p>
      {intro}
    </div>
    {body}
    <p class="empty hidden" id="empty">Nothing matches your search.</p>
  </main>
</div>
<footer>Generated from README.md by scripts/build_index.py</footer>
<script>
(function () {{
  var KEY = "study-plan-progress-v1";
  var state = {{}};
  try {{ state = JSON.parse(localStorage.getItem(KEY) || "{{}}") || {{}}; }} catch (e) {{ state = {{}}; }}
  function save() {{ try {{ localStorage.setItem(KEY, JSON.stringify(state)); }} catch (e) {{}} }}
  var ticks = Array.prototype.slice.call(document.querySelectorAll("input.tick"));
  var q = document.getElementById("q"), hideDone = document.getElementById("hide-done");

  function update() {{
    var done = 0;
    ticks.forEach(function (cb) {{
      var row = cb.closest("li.item, tr.week");
      if (row) row.classList.toggle("done", cb.checked);
      if (cb.checked) done++;
    }});
    document.getElementById("bar").style.width = (ticks.length ? 100 * done / ticks.length : 0) + "%";
    document.getElementById("overall").textContent = done + " / " + ticks.length + " done";
    document.querySelectorAll("section.block").forEach(function (sec) {{
      var boxes = sec.querySelectorAll("input.tick");
      var n = 0;
      boxes.forEach(function (b) {{ if (b.checked) n++; }});
      document.querySelectorAll('[data-count="' + sec.id + '"]').forEach(function (el) {{
        el.textContent = boxes.length ? n + "/" + boxes.length : "";
        el.classList.toggle("full", boxes.length > 0 && n === boxes.length);
      }});
    }});
    filter();
  }}

  function filter() {{
    var term = q.value.trim().toLowerCase(), hide = hideDone.checked, any = false;
    document.querySelectorAll("li.item, tr.week").forEach(function (el) {{
      if (!el.dataset.text) el.dataset.text = el.textContent.toLowerCase();
      var cb = el.querySelector(":scope > input.tick, :scope > td.wk input.tick");
      var show = (!term || el.dataset.text.indexOf(term) !== -1) && !(hide && cb && cb.checked);
      el.classList.toggle("hidden", !show);
    }});
    document.querySelectorAll("section.block").forEach(function (sec) {{
      var visible = sec.querySelector("li.item:not(.hidden), tr.week:not(.hidden)");
      var title = sec.querySelector("h2").textContent.toLowerCase();
      var show = (!term && !hide) || !!visible || (term && title.indexOf(term) !== -1);
      sec.classList.toggle("hidden", !show);
      if (show) any = true;
    }});
    document.getElementById("empty").classList.toggle("hidden", any);
  }}

  ticks.forEach(function (cb) {{
    cb.checked = !!state[cb.dataset.key];
    cb.addEventListener("change", function () {{
      if (cb.checked) state[cb.dataset.key] = 1; else delete state[cb.dataset.key];
      save(); update();
    }});
  }});
  q.addEventListener("input", filter);
  hideDone.addEventListener("change", filter);
  document.getElementById("reset").addEventListener("click", function () {{
    if (!confirm("Clear all saved progress in this browser?")) return;
    state = {{}}; save();
    ticks.forEach(function (cb) {{ cb.checked = false; }});
    update();
  }});
  if (window.matchMedia("(max-width: 900px)").matches) document.getElementById("toc-details").open = false;
  update();
}})();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    build()
