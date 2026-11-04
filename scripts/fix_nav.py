"""Rewrite every learn/*.html topnav to the canonical chapter order (marking the
current page), and verify the footer prev/next chain.

Run from the repository root:

    python3 scripts/fix_nav.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEARN = ROOT / "learn"

ORDER = [
    ("math.html", "Math"), ("interview-math.html", "Interview Math"), ("deep-learning.html", "Deep Learning"), ("transformers.html", "Transformers"), ("ml-coding.html", "ML Coding"),
    ("attention.html", "Attention"), ("architectures.html", "Architectures"), ("gallery.html", "Gallery"),
    ("multimodal.html", "Multimodal"), ("gpu.html", "GPU"), ("kernels.html", "Kernels"),
    ("quantization.html", "Quantization"), ("inference.html", "Inference"), ("parallelism.html", "Parallelism"),
    ("training.html", "Training"), ("customization.html", "Customization &amp; Evals"), ("rl-systems.html", "RL Systems"), ("frameworks.html", "Frameworks"), ("robot-learning.html", "RL &amp; Robotics"), ("hardware.html", "Hardware"),
    ("agents.html", "Agents"), ("system-design.html", "System Design"), ("coding-patterns.html", "Coding Patterns"), ("aditya-verma-patterns.html", "AV Patterns"), ("interview-journey.html", "Interview Journey"), ("notes.html", "Notes"),
    ("flashcards.html", "Flashcards"),
]
LINKS_RE = re.compile(r'<div class="links">.*?</div>', re.S)
FOOT_RE = re.compile(r'<div class="footer-nav">.*?</div>', re.S)

def links_for(page):
    return '<div class="links">\n    ' + "".join(
        f'<a href="{h}"{" class=\"here\"" if h == page else ""}>{t}</a>' for h, t in ORDER
    ) + "\n  </div>"

def footer_for(page):
    i = [h for h, _ in ORDER].index(page)
    prev = ORDER[i - 1] if i > 0 else ("index.html", "Hub")
    nxt = ORDER[i + 1] if i + 1 < len(ORDER) else ("index.html", "Hub")
    return f'<div class="footer-nav"><a href="{prev[0]}">← {prev[1]}</a><a href="{nxt[0]}">{nxt[1]} →</a></div>'

for page, _ in ORDER:
    f = LEARN / page
    if not f.exists():
        print("missing", page); continue
    s = f.read_text()
    s2, n = LINKS_RE.subn(links_for(page), s, count=1)
    s2, m = FOOT_RE.subn(footer_for(page), s2, count=1)
    if s2 != s:
        f.write_text(s2)
    print(f"{page}: nav {'ok' if n else 'NOT FOUND'}, footer {'ok' if m else 'none'}")
