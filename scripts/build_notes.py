"""Vendor permissively licensed notes repositories into learn/vendor/notes/ and
render them as themed HTML pages under learn/notes/, plus the index learn/notes.html.

Sources (cloned shallowly next to this repo or given via NOTES_SRC):
  stas00/ml-engineering                     CC-BY-SA 4.0   training infrastructure book
  zhaochenyang20/Awesome-ML-SYS-Tutorial    Apache-2.0     verl/slime/SGLang/RL-systems notes (English files)
  alirezadir/Machine-Learning-Interviews    MIT            ML / GenAI system design interview guide
  amitshekhariitbhu/ai-engineering-interview-questions  Apache-2.0  AI engineering Q&A

Run from the repository root:
    NOTES_SRC=/path/to/clones python3 scripts/build_notes.py
"""
import html
import os
import re
import shutil
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
LEARN = ROOT / "learn"
VENDOR = LEARN / "vendor" / "notes"
OUT = LEARN / "notes"
SRC = Path(os.environ.get("NOTES_SRC", ROOT.parent))
MAX_ASSET = 2 * 1024 * 1024
IMG_EXT = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}

REPOS = [
    {"key": "ml-engineering", "dir": "ml-engineering", "title": "Machine Learning Engineering Open Book",
     "author": "Stas Bekman", "license": "CC BY-SA 4.0", "license_file": "LICENSE-CC-BY-SA",
     "url": "https://github.com/stas00/ml-engineering",
     "blurb": "The training-infrastructure bible: accelerators, networking, storage, SLURM, model parallelism, performance, fault tolerance, training instabilities, debugging, dtypes.",
     "include": lambda p: p.suffix == ".md" and not p.parts[0].startswith(".") and "build" not in p.parts},
    {"key": "ml-sys-tutorial", "dir": "Awesome-ML-SYS-Tutorial", "title": "Awesome ML-SYS Tutorial (English notes)",
     "author": "Chenyang Zhao and contributors", "license": "Apache-2.0", "license_file": "LICENSE",
     "url": "https://github.com/zhaochenyang20/Awesome-ML-SYS-Tutorial",
     "blurb": "Working notes from SGLang / slime / verl developers: RL-system weight updates, FSDP and Megatron backends, verl and slime code walkthroughs, multi-turn agentic RL, SGLang scheduler and KV cache internals, omni-model inference.",
     "include": None},  # decided by language filter below
    {"key": "ml-interviews", "dir": "Machine-Learning-Interviews", "title": "Machine Learning Interviews (incl. ML & GenAI System Design)",
     "author": "Alireza Dirafzoon", "license": "MIT", "license_file": "LICENSE",
     "url": "https://github.com/alirezadir/Machine-Learning-Interviews",
     "blurb": "A complete ML interview guide: fundamentals, ML coding, ML/GenAI system design with worked designs (search, feeds, ads ranking, recommendation, harmful-content), behavioral prep.",
     "include": lambda p: p.suffix == ".md" and p.parts[0] in ("src", "README.md") and "cn" not in p.parts and "fa" not in p.parts},
    {"key": "ai-eng-interview", "dir": "ai-engineering-interview-questions", "title": "AI Engineering Interview Questions and Answers",
     "author": "Amit Shekhar (Outcome School)", "license": "Apache-2.0", "license_file": "LICENSE",
     "url": "https://github.com/amitshekhariitbhu/ai-engineering-interview-questions",
     "blurb": "Q&A across LLM fundamentals, prompting, RAG, agents, fine-tuning, vector DBs, AI system design, LLMOps, evaluation, safety, multimodal, and infrastructure — written for AI/forward-deployed engineer loops.",
     "include": lambda p: p.name == "README.md"},
]

CJK = re.compile(r"[一-鿿]")
def is_english(text):
    letters = max(1, len(re.findall(r"[A-Za-z]", text)))
    return len(CJK.findall(text)) / letters < 0.08

NAV = """<nav class="topnav"><a class="home" href="{root}index.html">Learn</a><div class="links"><a href="{root}notes.html" class="here">Notes library</a><a href="{root}index.html">All chapters</a><a href="{root}flashcards.html">Flashcards</a></div><div class="spacer"></div><button class="theme-btn" id="themeBtn">◐ theme</button></nav>"""
THEME = """<script>(function(){const b=document.getElementById('themeBtn');function cur(){try{return localStorage.getItem('learn-theme')||'dark'}catch(e){return 'dark'}}
function apply(t){document.documentElement.dataset.theme=t;try{localStorage.setItem('learn-theme',t)}catch(e){}}
apply(cur());b.onclick=()=>apply(document.documentElement.dataset.theme==='light'?'dark':'light');})();</script>"""
STYLE = """<style>
.note img{max-width:100%;height:auto;border-radius:8px;background:var(--bg-inset)}
.note pre{background:var(--bg-inset);border:1px solid var(--border);border-radius:10px;padding:12px 14px;overflow-x:auto;font-size:.85rem}
.note pre code{background:none;padding:0}
.note table{border-collapse:collapse;font-size:.9rem;display:block;overflow-x:auto}
.note th,.note td{border:1px solid var(--border);padding:6px 10px}
.note th{background:var(--bg-inset)}
.note blockquote{border-left:3px solid var(--accent);margin:10px 0;padding:4px 14px;color:var(--text-dim)}
.note h1{font-size:1.6rem}.note h2{border-top:none;margin-top:1.6em}
.crumb{font-size:.85rem;color:var(--text-dim);margin:6px 0 14px}
.attrib{font-size:.8rem;color:var(--text-dim);border-top:1px solid var(--border);margin-top:30px;padding-top:10px}
</style>"""

md = markdown.Markdown(extensions=["extra", "sane_lists", "toc", "admonition"], output_format="html5")

def rel_root(out_file):
    depth = len(out_file.relative_to(LEARN).parts) - 1
    return "../" * depth

def convert_repo(repo):
    src = SRC / repo["dir"]
    if not src.exists():
        print("missing source", src); return []
    vend = VENDOR / repo["key"]
    outdir = OUT / repo["key"]
    shutil.rmtree(vend, ignore_errors=True); shutil.rmtree(outdir, ignore_errors=True)
    vend.mkdir(parents=True); outdir.mkdir(parents=True)
    lic = src / repo["license_file"]
    if lic.exists():
        shutil.copy(lic, vend / "LICENSE")
    (vend / "VENDORED.txt").write_text(f"Vendored from {repo['url']} ({repo['license']}, {repo['author']}). Markdown copied verbatim; rendered to learn/notes/{repo['key']}/ by scripts/build_notes.py.\n")
    pages = []
    md_files = []
    for p in sorted(src.rglob("*.md")):
        rel = p.relative_to(src)
        if any(part.startswith(".") for part in rel.parts):
            continue
        text = p.read_text(errors="ignore")
        if repo["include"] is None:
            keep = is_english(text) and len(text) > 400 and not rel.name.lower().endswith(("-cn.md", "_cn.md", "-zh.md", "_zh.md"))
        else:
            keep = repo["include"](rel)
        if keep:
            md_files.append((rel, text))
    kept = {str(rel) for rel, _ in md_files}
    for rel, text in md_files:
        (vend / rel).parent.mkdir(parents=True, exist_ok=True)
        (vend / rel).write_text(text)
        # copy referenced images
        for m in re.finditer(r'!\[[^\]]*\]\(([^)\s]+)', text):
            ref = m.group(1).split("#")[0]
            if ref.startswith("http"):
                continue
            img = (src / rel).parent / ref
            try:
                img = img.resolve()
            except Exception:
                continue
            if img.exists() and img.suffix.lower() in IMG_EXT and img.stat().st_size <= MAX_ASSET:
                dst = vend / img.relative_to(src)
                dst.parent.mkdir(parents=True, exist_ok=True)
                if not dst.exists():
                    shutil.copy(img, dst)
        out_file = outdir / rel.with_suffix(".html")
        out_file.parent.mkdir(parents=True, exist_ok=True)
        root = rel_root(out_file)
        # rewrite links: .md -> .html (when kept), images -> vendored copy, else leave remote
        def fix_link(m):
            label, target = m.group(1), m.group(2)
            if target.startswith(("http", "mailto:", "#")):
                return m.group(0)
            tpath, _, frag = target.partition("#")
            cand = (rel.parent / tpath)
            norm = Path(os.path.normpath(cand))
            if str(norm) in kept:
                depth_here = len(rel.parts) - 1
                return f"[{label}]({'../' * depth_here}{norm.with_suffix('.html')}{('#' + frag) if frag else ''})"
            if norm.suffix.lower() in IMG_EXT:
                depth_here = len(rel.parts) - 1
                return f"[{label}]({root}vendor/notes/{repo['key']}/{norm})"
            return f"[{label}]({repo['url']}/blob/main/{norm})"
        text2 = re.sub(r'(?<!!)\[([^\]]*)\]\(([^)\s]+)\)', fix_link, text)
        def fix_img(m):
            target = m.group(2)
            if target.startswith("http"):
                return m.group(0)
            norm = Path(os.path.normpath(rel.parent / target.split('#')[0]))
            if (vend / norm).exists():
                return f"![{m.group(1)}]({root}vendor/notes/{repo['key']}/{norm.as_posix()})"
            return f"![{m.group(1)}]({repo['url']}/raw/main/{norm.as_posix()})"  # too large to vendor: hotlink original
        text2 = re.sub(r'!\[([^\]]*)\]\(([^)\s]+)\)', fix_img, text2)
        md.reset()
        body = md.convert(text2)
        title_m = re.search(r"^#\s+(.+)$", text, re.M)
        title = html.escape(title_m.group(1).strip()) if title_m else rel.stem
        page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><link rel="stylesheet" href="{root}learn.css">{STYLE}</head><body>
{NAV.format(root=root)}<main><div class="crumb"><a href="{root}notes.html">Notes library</a> › <a href="{root}notes.html#{repo['key']}">{html.escape(repo['title'])}</a> › {html.escape(str(rel))}</div>
<article class="note">{body}</article>
<div class="attrib">Source: <a href="{repo['url']}/blob/main/{rel}">{html.escape(str(rel))}</a> from <strong>{html.escape(repo['title'])}</strong> by {html.escape(repo['author'])}, reproduced under {repo['license']} (see <code>learn/vendor/notes/{repo['key']}/LICENSE</code>). Rendered by scripts/build_notes.py; math and some formatting may differ from the original.</div>
</main>{THEME}</body></html>"""
        out_file.write_text(page)
        pages.append((str(rel), title, out_file.relative_to(LEARN).as_posix(), len(text.split())))
    return pages

def build_index(all_pages):
    sections = []
    for repo, pages in all_pages:
        if not pages:
            continue
        words = sum(p[3] for p in pages)
        items = "".join(f'<li><a href="{href}">{title}</a> <span class="dim">({rel})</span></li>' for rel, title, href, _ in pages)
        sections.append(f"""<h2 id="{repo['key']}">{html.escape(repo['title'])}</h2>
<p>{html.escape(repo['blurb'])} <span class="dim">{len(pages)} notes · ~{words//1000}K words · {repo['license']} · <a href="{repo['url']}">source</a></span></p>
<details><summary>Show all {len(pages)} notes</summary><ul>{items}</ul></details>""")
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Notes Library</title><link rel="stylesheet" href="learn.css"><style>details summary{{cursor:pointer;color:var(--accent);margin:6px 0}} details ul{{columns:1}}</style></head><body>
{NAV.format(root="")}<main>
<h1>Notes Library</h1>
<p>Four open-source note collections vendored into this repo (verbatim Markdown under <code>learn/vendor/notes/</code>, rendered here in the notebook's theme) so the chapters' explanations can be followed by the practitioners' own working notes. They cover the bases the chapters summarize: Stas Bekman's training-infrastructure book, the SGLang/slime/verl developers' RL-system and inference internals, a full ML/GenAI system-design interview guide, and an AI-engineering Q&amp;A bank. Each page links back to its source; licenses are preserved alongside the copies.</p>
<p class="dim">How to use: read the chapter first, then open the matching notes — <a href="parallelism.html">Parallelism</a> → ML Engineering's model-parallelism and network chapters; <a href="rl-systems.html">RL Systems</a> and <a href="frameworks.html">Frameworks</a> → the verl/slime walkthroughs and weight-update notes; <a href="inference.html">Inference</a> → the SGLang KV-cache and scheduler notes; <a href="system-design.html">System Design</a> → the ML system design worked designs; <a href="customization.html">Customization &amp; Evals</a> → the fine-tuning and evaluation Q&amp;A.</p>
{''.join(sections)}
</main>{THEME}</body></html>"""
    (LEARN / "notes.html").write_text(page)

if __name__ == "__main__":
    VENDOR.mkdir(parents=True, exist_ok=True); OUT.mkdir(parents=True, exist_ok=True)
    results = []
    for repo in REPOS:
        pages = convert_repo(repo)
        results.append((repo, pages))
        print(f"{repo['key']:18s} {len(pages):4d} pages")
    build_index(results)
    print("wrote learn/notes.html")
