# learn/transcripts — captions for Aditya Verma's playlists

This folder holds the transcripts that the **AV Patterns** chapter
(`learn/aditya-verma-patterns.html`) shows under each video slot. It is empty in the
repository because YouTube could not be reached when the chapter was built; fill it from
your own machine:

```bash
pip install yt-dlp
python3 scripts/fetch_transcripts.py          # all of his pattern playlists
python3 scripts/fetch_transcripts.py "Stack"  # just the playlists matching a word
```

The script lists the channel's playlists (Dynamic Programming, Sliding Window, Stack,
Binary Search, Recursion, Backtracking, Heap, Graph), downloads each video's own captions
(manual if present, otherwise YouTube's automatic captions — the videos are in
Hindi/Hinglish, so most transcripts are `hi` auto-captions; they read as spoken Hinglish
and are rough but searchable), strips the timestamps, and writes:

- `<video-id>.txt` — one transcript per video, plain text, one caption line per line
- `index.json` — `[{id, title, playlist, lang, url}, …]`, used by the chapter to attach a
  transcript to a video slot (by id when the slot has one, otherwise by matching the title)

Open the notebook over HTTP for the transcripts to load (`python3 -m http.server` in the
repository root, then `/learn/aditya-verma-patterns.html`); browsers block `fetch()` from
`file://` pages. Videos without captions are listed at the end of the script's output and
their slots keep the "not fetched" note.

The transcripts are the videos' captions and belong to their author; they are kept here
for personal study alongside the pattern map, which links every video back to the channel.
