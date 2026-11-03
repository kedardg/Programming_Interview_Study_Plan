"""Insert (or refresh) a "Listen" audio player card at the top of every chapter
that has learn/audio/<chapter>.mp3, and build the Audio Course section data for the hub.

Run from the repository root after scripts/build_audio.py:

    python3 scripts/add_audio_players.py
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEARN = ROOT / "learn"
AUDIO = LEARN / "audio"

def duration(mp3):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp3)],
                         capture_output=True, text=True).stdout.strip()
    secs = float(out or 0)
    return f"{int(secs // 60)}:{int(secs % 60):02d}"

CARD_RE = re.compile(r'<div class="card audio-card">.*?</div>\s*', re.S)
rows = []
for mp3 in sorted(AUDIO.glob("*.mp3")):
    name = mp3.stem
    page = LEARN / f"{name}.html"
    if not page.exists():
        continue
    dur = duration(mp3)
    rows.append((name, dur))
    card = (f'<div class="card audio-card"><h3>🎧 Listen to this chapter ({dur})</h3>'
            f'<audio controls preload="none" src="audio/{name}.mp3" style="width:100%"></audio>'
            f'<p class="caption">Narrated explainer of this chapter: concepts, the papers behind them, and what to open next. '
            f'<a href="audio/scripts/{name}.txt">Read the transcript</a>.</p></div>\n')
    s = page.read_text()
    s = CARD_RE.sub("", s, count=1)
    # insert after the intro paragraph (first <p class="dim"> following <h1>) or after <h1>
    m = re.search(r'(<h1>.*?</h1>\s*(?:<p class="dim">.*?</p>\s*)?)', s, re.S)
    s = s[:m.end()] + card + s[m.end():]
    page.write_text(s)
    print(f"{name:18s} {dur}")

# hub section
hub = LEARN / "index.html"
s = hub.read_text()
SEC_RE = re.compile(r'<h2>Audio course</h2>.*?(?=<h2>)', re.S)
titles = {}
for name, _ in rows:
    t = re.search(r"<title>(.*?)</title>", (LEARN / f"{name}.html").read_text())
    titles[name] = t.group(1) if t else name
items = "".join(f'<li><a href="{n}.html">{titles[n]}</a> — {d} · <a href="audio/{n}.mp3">mp3</a></li>' for n, d in rows)
total = sum(int(d.split(":")[0]) for _, d in rows)
section = (f'<h2>Audio course</h2>\n<p class="dim">Every chapter narrated ({len(rows)} episodes, about {total} minutes) by a rotating cast of Kokoro voices, '
           f'generated offline with <code>scripts/build_audio.py</code>. Each episode ends by telling you which animation to open and what to read next. '
           f'Play from the chapter page, or grab the mp3s from <code>learn/audio/</code> for your phone.</p>\n<ul>{items}</ul>\n\n')
if SEC_RE.search(s):
    s = SEC_RE.sub(section, s, count=1)
else:
    s = s.replace("<h2>The best of the web</h2>", section + "<h2>The best of the web</h2>", 1)
hub.write_text(s)
print("hub audio section:", len(rows), "episodes")
