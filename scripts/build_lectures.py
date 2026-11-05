"""Vendor the GPU MODE lectures repository (Apache-2.0) into learn/vendor/gpu-mode-lectures/,
render its notebooks as themed pages under learn/lectures/, and build learn/lectures.html:
every lecture with its speaker, materials, the study-plan step that assigns it, and the
notebook chapter that teaches the same ground.

Run from the repository root (clone next to the repo or set LECTURES_SRC):
    LECTURES_SRC=/path/to/lectures python3 scripts/build_lectures.py
"""
import html
import json
import os
import re
import shutil
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
LEARN = ROOT / "learn"
SRC = Path(os.environ.get("LECTURES_SRC", ROOT.parent / "lectures"))
VEND = LEARN / "vendor" / "gpu-mode-lectures"
OUT = LEARN / "lectures"
MAX_BINARY = 10 * 1024 * 1024
SKIP_EXT = {".o", ".ninja_log", ".ninja_deps", ".so", ".pyc"}
REPO = "https://github.com/gpu-mode/lectures"

# lecture -> notebook chapter (by topic); everything else falls back to the step's chapter
CHAPTER_BY_LECTURE = {
    1: "gpu.html", 2: "gpu.html", 3: "kernels.html", 4: "gpu.html", 5: "kernels.html", 6: "training.html",
    7: "quantization.html", 8: "gpu.html", 9: "kernels.html", 10: "frameworks.html", 11: "kernels.html",
    12: "attention.html", 13: "attention.html", 14: "kernels.html", 15: "kernels.html", 16: "kernels.html",
    17: "parallelism.html", 18: "attention.html", 19: "quantization.html", 20: "kernels.html", 21: "kernels.html",
    22: "inference.html", 23: "kernels.html", 24: "kernels.html", 25: "hardware.html", 26: "hardware.html",
    27: "hardware.html", 28: "kernels.html", 29: "kernels.html", 30: "quantization.html", 31: "hardware.html",
    32: "training.html", 33: "kernels.html", 34: "quantization.html", 35: "inference.html", 36: "attention.html",
    37: "gpu.html", 39: "parallelism.html", 40: "attention.html", 42: "hardware.html", 57: "kernels.html",
    67: "parallelism.html", 70: "parallelism.html", 71: "training.html", 72: "attention.html", 74: "attention.html",
    75: "kernels.html", 78: "parallelism.html", 79: "attention.html", 84: "quantization.html", 103: "kernels.html",
    104: "kernels.html", 106: "frameworks.html",
}
CHAPTER_TITLE = {"gpu.html": "GPU Architecture", "kernels.html": "Writing Kernels", "attention.html": "Attention",
                 "quantization.html": "Quantization", "inference.html": "Inference", "parallelism.html": "Parallelism",
                 "training.html": "Training", "hardware.html": "Hardware", "frameworks.html": "Frameworks"}

def plan_steps():
    """Map lecture number -> (step number, step title) from the study plan README."""
    steps, cur = {}, None
    for line in (ROOT / "README.md").read_text().splitlines():
        m = re.match(r"^## Step (\d+) - (.+)", line)
        if m:
            cur = (int(m.group(1)), m.group(2).strip())
        for n in re.findall(r"Lecture (\d+):", line):
            if cur:
                steps.setdefault(int(n), cur)
    return steps

def parse_readme():
    """Lecture number -> {title, speaker, lines} from the lectures repo README."""
    lectures, cur = {}, None
    for line in (SRC / "README.md").read_text().splitlines():
        m = re.match(r"^## Lecture (\d+):\s*(.+)", line)
        if m:
            cur = int(m.group(1)); lectures[cur] = {"title": m.group(2).strip(), "speaker": "", "lines": []}
            continue
        if cur is None or not line.strip():
            continue
        sm = re.match(r"^- Speaker:\s*(.+)", line)
        if sm:
            lectures[cur]["speaker"] = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", sm.group(1)).strip(); continue
        if line.startswith("- "):
            lectures[cur]["lines"].append(line[2:].strip())
    return lectures

def md_links_to_html(text, folder):
    def repl(m):
        label, target = m.group(1), m.group(2)
        if target.startswith("http"):
            return f'<a href="{html.escape(target)}">{html.escape(label)}</a>'
        local = VEND / target.lstrip("./")
        if local.exists():
            return f'<a href="vendor/gpu-mode-lectures/{html.escape(target.lstrip("./"))}">{html.escape(label)}</a>'
        return f'<a href="{REPO}/blob/main/{html.escape(target.lstrip("./"))}">{html.escape(label)}</a> <span class="dim">(on GitHub)</span>'
    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", repl, html.escape(text, quote=False).replace("&lt;", "<").replace("&gt;", ">"))

def vendor():
    shutil.rmtree(VEND, ignore_errors=True); VEND.mkdir(parents=True)
    shutil.copy(SRC / "LICENSE", VEND / "LICENSE")
    copied, skipped = 0, []
    for p in sorted(SRC.rglob("*")):
        if p.is_dir() or ".git" in p.parts:
            continue
        rel = p.relative_to(SRC)
        if p.suffix.lower() in SKIP_EXT or p.name.startswith("."):
            continue
        if p.suffix.lower() in {".pdf", ".pptx", ".png", ".jpg", ".jpeg", ".gif", ".mp4", ".zip"} and p.stat().st_size > MAX_BINARY:
            skipped.append((rel, p.stat().st_size)); continue
        (VEND / rel).parent.mkdir(parents=True, exist_ok=True); shutil.copy(p, VEND / rel); copied += 1
    (VEND / "VENDORED.txt").write_text(
        f"Vendored from {REPO} (Apache License 2.0). Build artifacts and binaries over {MAX_BINARY//1024//1024} MB were left out "
        f"(linked to GitHub instead): " + ", ".join(f"{r} ({s//1024//1024} MB)" for r, s in skipped) + "\n")
    return copied, skipped

THEME = """<script>(function(){const b=document.getElementById('themeBtn');function cur(){try{return localStorage.getItem('learn-theme')||'dark'}catch(e){return 'dark'}}
function apply(t){document.documentElement.dataset.theme=t;try{localStorage.setItem('learn-theme',t)}catch(e){}}
apply(cur());b.onclick=()=>apply(document.documentElement.dataset.theme==='light'?'dark':'light');})();</script>"""
NAV = """<nav class="topnav"><a class="home" href="{root}index.html">Learn</a><div class="links"><a href="{root}lectures.html" class="here">GPU MODE Lectures</a><a href="{root}index.html">All chapters</a><a href="{root}notes.html">Notes library</a></div><div class="spacer"></div><button class="theme-btn" id="themeBtn">◐ theme</button></nav>"""
NBSTYLE = """<style>.nb pre{background:var(--bg-inset);border:1px solid var(--border);border-radius:10px;padding:12px 14px;overflow-x:auto;font-size:.85rem}
.nb .cell{margin:14px 0}.nb .in{border-left:3px solid var(--accent);padding-left:10px}.nb .out{border-left:3px solid var(--accent2);padding-left:10px;margin-top:6px}
.nb img{max-width:100%;border-radius:8px}.nb table{border-collapse:collapse}.nb td,.nb th{border:1px solid var(--border);padding:4px 8px}.crumb{font-size:.85rem;color:var(--text-dim)}
.attrib{font-size:.8rem;color:var(--text-dim);border-top:1px solid var(--border);margin-top:30px;padding-top:10px}</style>"""
md = markdown.Markdown(extensions=["extra", "sane_lists"], output_format="html5")

def render_notebook(nb_path, out_file, rel):
    nb = json.loads(nb_path.read_text(errors="ignore"))
    parts = []
    for cell in nb.get("cells", []):
        src = "".join(cell.get("source", []))
        if cell.get("cell_type") == "markdown":
            # notebook-relative links/images -> the vendored copy of the lecture folder
            vroot = "../" * (len(rel.parts)) + "vendor/gpu-mode-lectures/" + rel.parent.as_posix() + "/"
            src = re.sub(r"(!?\[[^\]]*\]\()(?!https?://|#|data:)([^)\s]+)", lambda m: m.group(1) + vroot + m.group(2).lstrip("./"), src)
            md.reset(); parts.append(f'<div class="cell md">{md.convert(src)}</div>')
        elif cell.get("cell_type") == "code":
            outs = []
            for o in cell.get("outputs", []):
                data = o.get("data", {})
                if "image/png" in data:
                    outs.append(f'<img src="data:image/png;base64,{"".join(data["image/png"]).strip()}" alt="output">')
                elif "text/html" in data:
                    outs.append("".join(data["text/html"]))
                elif "text/plain" in data:
                    outs.append("<pre>" + html.escape("".join(data["text/plain"])) + "</pre>")
                elif o.get("output_type") == "stream":
                    outs.append("<pre>" + html.escape("".join(o.get("text", []))) + "</pre>")
                elif o.get("output_type") == "error":
                    outs.append("<pre>" + html.escape("\n".join(o.get("traceback", []))[:4000]) + "</pre>")
            parts.append(f'<div class="cell"><div class="in"><pre><code>{html.escape(src)}</code></pre></div>' + (f'<div class="out">{"".join(outs)}</div>' if outs else "") + "</div>")
    depth = len(out_file.relative_to(LEARN).parts) - 1; root = "../" * depth
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(nb_path.stem)}</title><link rel="stylesheet" href="{root}learn.css">{NBSTYLE}</head><body>{NAV.format(root=root)}<main>
<div class="crumb"><a href="{root}lectures.html">GPU MODE Lectures</a> › {html.escape(str(rel))}</div><h1>{html.escape(nb_path.stem)}</h1>
<article class="nb">{"".join(parts)}</article>
<div class="attrib">Rendered from <a href="{REPO}/blob/main/{rel}">{html.escape(str(rel))}</a> in the GPU MODE lectures repository (Apache-2.0); the original notebook is vendored at <code>learn/vendor/gpu-mode-lectures/{rel}</code>. Outputs are those saved in the notebook.</div>
</main>{THEME}</body></html>"""
    out_file.parent.mkdir(parents=True, exist_ok=True); out_file.write_text(page)

def build():
    copied, skipped = vendor()
    shutil.rmtree(OUT, ignore_errors=True); OUT.mkdir(parents=True)
    lectures, steps = parse_readme(), plan_steps()
    rendered = {}
    for nb in sorted(VEND.rglob("*.ipynb")):
        rel = nb.relative_to(VEND); out = OUT / rel.with_suffix(".html")
        try:
            render_notebook(nb, out, rel); rendered.setdefault(rel.parts[0], []).append((rel, out.relative_to(LEARN).as_posix()))
        except Exception as e:
            print("notebook failed", rel, e)
    cards, assigned = [], 0
    for n in sorted(lectures):
        L = lectures[n]; folder = f"lecture_{n:03d}"
        step = steps.get(n); ch = CHAPTER_BY_LECTURE.get(n)
        if step: assigned += 1
        files = sorted((VEND / folder).rglob("*")) if (VEND / folder).exists() else []
        files = [f for f in files if f.is_file()]
        mats = "".join(f'<li>{md_links_to_html(l, folder)}</li>' for l in L["lines"])
        nbs = "".join(f'<li>Notebook rendered: <a href="{h}">{html.escape(r.name)}</a></li>' for r, h in rendered.get(folder, []))
        local = "".join(f'<li><a href="vendor/gpu-mode-lectures/{f.relative_to(VEND).as_posix()}">{html.escape(f.relative_to(VEND / folder).as_posix())}</a> <span class="dim">({f.stat().st_size//1024} KB)</span></li>' for f in files if f.suffix != ".ipynb")
        big = "".join(f'<li><a href="{REPO}/blob/main/{r.as_posix()}">{html.escape(r.name)}</a> <span class="dim">({s//1024//1024} MB, on GitHub)</span></li>' for r, s in skipped if r.parts[0] == folder)
        tags = (f'<span class="pill a">Step {step[0]}: {html.escape(step[1])}</span> ' if step else '<span class="pill w">not in the 3-month plan — reference</span> ') + (f'<a class="pill g" href="{ch}">{CHAPTER_TITLE[ch]} chapter</a>' if ch else "")
        cards.append(f"""<div class="card" id="l{n}"><h3>Lecture {n}: {html.escape(L["title"])}</h3><p class="dim">{html.escape(L["speaker"]) or "—"} · {tags}</p>
<ul>{mats}{nbs}{local}{big}</ul></div>""")
    nb_count = sum(len(v) for v in rendered.values())
    toc = " ".join(f'<a href="#l{n}">{n}</a>' for n in sorted(lectures))
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>GPU MODE Lectures</title><link rel="stylesheet" href="learn.css"><style>.toc a{{margin-right:8px}} .card ul{{margin:6px 0 0;padding-left:1.1em}} .card li{{font-size:.92rem}}</style></head><body>
{NAV.format(root="")}<main>
<h1>GPU MODE lectures, mapped to the plan and the notebook</h1>
<p>The study plan's <strong>Watch</strong> lists are the <a href="{REPO}">GPU MODE lectures</a> (Apache-2.0). This page brings the repository's supplementary material in: {copied} files vendored under <code>learn/vendor/gpu-mode-lectures/</code> (code, notebooks, slides up to 10 MB; {len(skipped)} larger decks linked to GitHub), {nb_count} notebooks rendered as pages you can read here, and every one of the {len(lectures)} lectures tagged with the study-plan step that assigns it ({assigned} are in the plan's Watch lists) and the notebook chapter that teaches the same ground — read the chapter, then work the lecture's code. Build: <code>scripts/build_lectures.py</code>. Videos are on the <a href="https://www.youtube.com/@GPUMODE">GPU MODE YouTube channel</a>.</p>
<p class="toc dim">Lecture: {toc}</p>
{"".join(cards)}
</main>{THEME}</body></html>"""
    (LEARN / "lectures.html").write_text(page)
    print(f"vendored {copied} files ({len(skipped)} large skipped); rendered {nb_count} notebooks; {len(lectures)} lectures, {assigned} mapped to plan steps")

if __name__ == "__main__":
    build()
