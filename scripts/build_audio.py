"""Synthesize the audio course: one narrated MP3 per chapter from
learn/audio/scripts/<chapter>.txt using Kokoro (kokoro-onnx, CPU).

Setup (one time):
    pip install kokoro-onnx soundfile
    # model + voices from the kokoro-onnx GitHub release (hosted on GitHub, no HF needed)
    curl -L -o kokoro-v1.0.onnx  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
    curl -L -o voices-v1.0.bin   https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin

Run from the repository root (model files in the current directory or set KOKORO_DIR):
    python3 scripts/build_audio.py            # all chapters whose mp3 is older than its script
    python3 scripts/build_audio.py inference  # one chapter

Scripts are plain text written to be spoken. Blank lines are paragraph pauses.
"""
import os
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "learn" / "audio" / "scripts"
OUT = ROOT / "learn" / "audio"
MODEL_DIR = Path(os.environ.get("KOKORO_DIR", "."))

# One pleasant voice per chapter so the course doesn't sound monotonous.
VOICES = {
    "math": "af_heart", "deep-learning": "am_michael", "transformers": "bf_emma",
    "attention": "am_fenrir", "architectures": "af_bella", "gallery": "bm_george",
    "multimodal": "af_nicole", "gpu": "bm_lewis", "kernels": "af_sarah",
    "quantization": "am_adam", "inference": "af_heart", "parallelism": "bm_daniel",
    "training": "af_nova", "robot-learning": "am_michael", "hardware": "bf_isabella",
    "agents": "am_echo", "system-design": "bf_emma", "coding-patterns": "af_bella",
}
SPEED = 1.0

CACHE = Path(os.environ.get("KOKORO_CACHE", str(MODEL_DIR / "cache")))
THREADS = int(os.environ.get("KOKORO_THREADS", "1"))
import time
DEADLINE = time.time() + float(os.environ.get("KOKORO_BUDGET", "1e9"))  # seconds; stop cleanly and resume next run

def synth(name):
    """Resumable: each paragraph's samples are cached, so an interrupted run picks up where it left off."""
    import numpy as np
    import onnxruntime as ort
    import soundfile as sf
    _orig = ort.InferenceSession
    def _limited(*a, **k):
        so = k.get("sess_options") or ort.SessionOptions()
        so.intra_op_num_threads = THREADS
        so.inter_op_num_threads = 1
        k["sess_options"] = so
        return _orig(*a, **k)
    ort.InferenceSession = _limited
    from kokoro_onnx import Kokoro
    k = Kokoro(str(MODEL_DIR / "kokoro-v1.0.onnx"), str(MODEL_DIR / "voices-v1.0.bin"))
    text = (SCRIPTS / f"{name}.txt").read_text()
    voice = VOICES.get(name, "af_heart")
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    cdir = CACHE / name
    cdir.mkdir(parents=True, exist_ok=True)
    chunks = []
    sr = 24000
    for i, para in enumerate(paras):
        f = cdir / f"{i:03d}.npy"
        if f.exists():
            samples = np.load(f)
        else:
            if time.time() > DEADLINE:
                return name, voice, None  # out of time budget; cached paragraphs persist
            samples, sr = k.create(para, voice=voice, speed=SPEED, lang="en-us")
            np.save(f, samples)
        chunks.append(samples)
        chunks.append(np.zeros(int(sr * 0.55), dtype=samples.dtype))
    audio = np.concatenate(chunks)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        sf.write(tmp.name, audio, sr)
        mp3 = OUT / f"{name}.mp3"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp.name, "-ac", "1", "-b:a", "48k",
                        "-metadata", f"title={name} — Interactive Notebook audio", str(mp3)], check=True)
    os.unlink(tmp.name)
    return name, voice, len(audio) / sr

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    wanted = sys.argv[1:] or sorted(p.stem for p in SCRIPTS.glob("*.txt"))
    todo = []
    for n in wanted:
        src, dst = SCRIPTS / f"{n}.txt", OUT / f"{n}.mp3"
        if not src.exists():
            print("no script:", n); continue
        if sys.argv[1:] or not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
            todo.append(n)
    workers = max(1, min(len(todo), int(os.environ.get("KOKORO_WORKERS", os.cpu_count() or 2))))
    with ProcessPoolExecutor(workers) as ex:
        for name, voice, secs in ex.map(synth, todo):
            print(f"{name:18s} {voice:12s} " + (f"{secs/60:5.1f} min" if secs else "partial (resume)"))
