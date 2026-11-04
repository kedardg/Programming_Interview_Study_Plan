"""Fetch the captions of Aditya Verma's playlists into learn/transcripts/ so the
"AV Patterns" chapter (learn/aditya-verma-patterns.html) can show each video's transcript.

Run this on your own machine (it needs internet access to YouTube):

    pip install yt-dlp
    python3 scripts/fetch_transcripts.py            # all playlists below
    python3 scripts/fetch_transcripts.py "Stack"    # only playlists whose title contains "Stack"

For every playlist it lists the videos (yt-dlp --flat-playlist), downloads the
manual or automatic captions in Hindi/English (the videos are in Hindi/Hinglish, so
the auto captions are usually "hi"), strips timestamps, and writes:

    learn/transcripts/<video-id>.txt      plain-text transcript
    learn/transcripts/index.json          [{id, title, playlist, lang, url}, ...]

The chapter matches transcripts to its video slots by id or by title, so nothing
else needs editing. Videos without captions are listed in the summary and skipped.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "learn" / "transcripts"

# Channel playlists (titles as shown on https://www.youtube.com/@theadityaverma/playlists).
# The script resolves each title to its playlist URL at runtime from the channel's playlist
# listing, so playlist ids do not need to be hard-coded here.
CHANNEL_PLAYLISTS_URL = "https://www.youtube.com/@theadityaverma/playlists"
PLAYLIST_TITLES = [
    "Dynamic Programming",
    "Sliding Window",
    "Stack",
    "Binary Search",
    "Recursion",
    "Backtracking",
    "Heap",
    "Graph",
]
LANGS = ["hi", "en", "hi-en", "en-IN", "hi-IN"]


def run(args, **kw):
    return subprocess.run(["yt-dlp", *args], capture_output=True, text=True, **kw)


def list_channel_playlists():
    """Return [(title, url)] for the channel's playlists."""
    r = run(["--flat-playlist", "-J", CHANNEL_PLAYLISTS_URL])
    if r.returncode != 0:
        sys.exit("yt-dlp could not list the channel's playlists:\n" + r.stderr[-2000:])
    data = json.loads(r.stdout)
    out = []
    for e in data.get("entries", []):
        if not e:
            continue
        title, url = e.get("title", ""), e.get("url") or e.get("webpage_url", "")
        if url and "list=" in url:
            out.append((title, url))
    return out


def list_videos(playlist_url):
    r = run(["--flat-playlist", "-J", playlist_url])
    if r.returncode != 0:
        print("  could not list playlist:", r.stderr.strip().splitlines()[-1:])
        return []
    data = json.loads(r.stdout)
    return [(e.get("id"), e.get("title", "")) for e in data.get("entries", []) if e and e.get("id")]


SRT_TS = re.compile(r"^\d+\s*$|^\d{2}:\d{2}:\d{2},\d{3} --> .*$")
TAGS = re.compile(r"<[^>]+>")


def srt_to_text(path):
    lines, last = [], None
    for raw in path.read_text(errors="ignore").splitlines():
        line = TAGS.sub("", raw).strip()
        if not line or SRT_TS.match(line):
            continue
        if line != last:  # auto captions repeat lines as they scroll
            lines.append(line)
            last = line
    return "\n".join(lines)


def fetch_subs(video_id):
    """Download captions for one video; return (lang, text) or (None, None)."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    with tempfile.TemporaryDirectory() as tmp:
        r = run(["--skip-download", "--write-sub", "--write-auto-sub", "--sub-lang", ",".join(LANGS),
                 "--convert-subs", "srt", "-o", f"{tmp}/%(id)s.%(ext)s", url])
        files = sorted(Path(tmp).glob(f"{video_id}*.srt"))
        if not files:
            return None, None
        # prefer manual over auto, hi over en: yt-dlp names them <id>.<lang>.srt
        def rank(p):
            lang = p.name.split(".")[-2]
            return (LANGS.index(lang) if lang in LANGS else 99, len(p.name))
        best = sorted(files, key=rank)[0]
        return best.name.split(".")[-2], srt_to_text(best)


def main():
    if shutil.which("yt-dlp") is None:
        sys.exit("yt-dlp is not installed: pip install yt-dlp")
    wanted = [w.lower() for w in sys.argv[1:]]
    OUT.mkdir(parents=True, exist_ok=True)
    index_path = OUT / "index.json"
    index = {e["id"]: e for e in json.loads(index_path.read_text())} if index_path.exists() else {}
    channel = list_channel_playlists()
    chosen = [(t, u) for t, u in channel if any(k.lower() in t.lower() for k in PLAYLIST_TITLES)
              and (not wanted or any(w in t.lower() for w in wanted))]
    if not chosen:
        sys.exit("No matching playlists found on the channel; titles seen: " + ", ".join(t for t, _ in channel))
    missing = []
    for title, url in chosen:
        print(f"== {title}")
        for vid, vtitle in list_videos(url):
            dst = OUT / f"{vid}.txt"
            if dst.exists():
                print(f"   skip (have) {vtitle}")
                continue
            lang, text = fetch_subs(vid)
            if not text:
                missing.append((title, vtitle))
                print(f"   no captions   {vtitle}")
                continue
            dst.write_text(text)
            index[vid] = {"id": vid, "title": vtitle, "playlist": title, "lang": lang,
                          "url": f"https://www.youtube.com/watch?v={vid}"}
            print(f"   saved [{lang}] {vtitle}")
    index_path.write_text(json.dumps(sorted(index.values(), key=lambda e: (e['playlist'], e['title'])), ensure_ascii=False, indent=1))
    print(f"\n{len(index)} transcripts in {OUT}; index written to {index_path}")
    if missing:
        print(f"{len(missing)} videos had no captions:")
        for p, t in missing:
            print(f"  - {p}: {t}")


if __name__ == "__main__":
    main()
