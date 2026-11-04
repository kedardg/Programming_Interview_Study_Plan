# Audio course — how it was made and how to regenerate it

Every chapter of the notebook has a narrated episode. The narration **scripts are the source of
truth** and live in [`scripts/`](scripts/) as plain text written to be spoken (no markdown or
symbols; formulas in words; one blank line between paragraphs = a short pause). The MP3s next to
this file were generated from them offline. If the MP3s are ever missing or you want different
voices, regenerate them with the steps below.

## Episodes

| Script | Voice | Words | Length | MP3 present |
|---|---|---|---|---|
| [agents](scripts/agents.txt) | `am_echo` | 1,787 | 9:53 | yes |
| [architectures](scripts/architectures.txt) | `af_bella` | 2,841 | 19:04 | yes |
| [attention](scripts/attention.txt) | `am_fenrir` | 3,073 | 16:58 | yes |
| [coding-patterns](scripts/coding-patterns.txt) | `af_bella` | 2,136 | 13:08 | yes |
| [customization](scripts/customization.txt) | `af_heart` | 2,237 | 14:20 | yes |
| [deep-learning](scripts/deep-learning.txt) | `am_michael` | 2,406 | 16:38 | yes |
| [frameworks](scripts/frameworks.txt) | `af_heart` | 2,248 | 14:38 | yes |
| [gallery](scripts/gallery.txt) | `bm_george` | 834 | 5:37 | yes |
| [gpu](scripts/gpu.txt) | `bm_lewis` | 1,604 | 10:08 | yes |
| [hardware](scripts/hardware.txt) | `bf_isabella` | 1,804 | 10:21 | yes |
| [inference](scripts/inference.txt) | `af_heart` | 1,813 | 11:17 | yes |
| [interview-journey](scripts/interview-journey.txt) | `af_heart` | 2,082 | 12:25 | yes |
| [interview-math](scripts/interview-math.txt) | `af_heart` | 2,767 | 16:54 | yes |
| [kernels](scripts/kernels.txt) | `af_sarah` | 1,775 | 10:51 | yes |
| [math](scripts/math.txt) | `af_heart` | 2,298 | 14:06 | yes |
| [ml-coding](scripts/ml-coding.txt) | `af_heart` | 2,838 | 17:22 | yes |
| [multimodal](scripts/multimodal.txt) | `af_nicole` | 1,900 | 18:45 | yes |
| [parallelism](scripts/parallelism.txt) | `bm_daniel` | 1,811 | 9:37 | yes |
| [quantization](scripts/quantization.txt) | `am_adam` | 1,809 | 10:12 | yes |
| [rl-systems](scripts/rl-systems.txt) | `af_heart` | 3,232 | 20:51 | yes |
| [robot-learning](scripts/robot-learning.txt) | `am_michael` | 3,020 | 20:10 | yes |
| [system-design](scripts/system-design.txt) | `bf_emma` | 1,802 | 10:14 | yes |
| [training](scripts/training.txt) | `af_nova` | 1,821 | 9:43 | yes |
| [transformers](scripts/transformers.txt) | `bf_emma` | 2,750 | 16:09 | yes |

Total: 24 episodes, about 318 minutes. Each script ends by naming which animation
or calculator to open on the chapter page, which flashcard deck to drill, and what to read next.

## Regenerate the audio (Kokoro, CPU, no GPU needed)

1. Install the TTS engine and audio writer (Python 3.10+):

       pip install kokoro-onnx soundfile

   `ffmpeg` must be on your PATH (used for the MP3 encode).

2. Download the Kokoro v1.0 model and voice pack. They are hosted as GitHub release assets of the
   kokoro-onnx project (no Hugging Face login needed):

       curl -L -o kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
       curl -L -o voices-v1.0.bin  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin

3. From the repository root, synthesize (all episodes whose MP3 is missing or older than its script):

       KOKORO_DIR=/path/to/model/files python3 scripts/build_audio.py
       # or one episode:
       KOKORO_DIR=/path/to/model/files python3 scripts/build_audio.py inference

   Useful knobs: `KOKORO_WORKERS` (parallel episodes, default = CPU count), `KOKORO_THREADS`
   (threads per episode, default 1), `KOKORO_BUDGET` (seconds; the run stops cleanly when the
   budget is spent and resumes where it left off, because every paragraph is cached under
   `KOKORO_DIR/cache/`). Expect roughly 4x real time on a 4-core machine.

4. Attach the players and refresh the hub's episode list:

       python3 scripts/add_audio_players.py

5. To change a voice, edit the `VOICES` table at the top of `scripts/build_audio.py` (54 voices
   ship with the pack: `af_*`/`am_*` American, `bf_*`/`bm_*` British, plus other languages), delete
   that episode's cache directory and MP3, and rerun step 3.

## Editing a script

Edit the `.txt`, keep paragraphs separated by blank lines, write numbers and formulas as you
would say them, and avoid markdown. Inserting paragraphs shifts the cache indices, so delete
`KOKORO_DIR/cache/<episode>/` before regenerating that episode. Appending only new paragraphs at
the end needs no cache reset.

## Other engines

The scripts are engine-agnostic. They work as-is with any TTS that accepts plain text:
Kokoro via the Hugging Face `kokoro` package (needs HF access for the weights), Higgs Audio v2
(better prosody, needs a GPU), or a hosted API. Keep paragraph breaks as pause markers and
re-run `scripts/add_audio_players.py` after writing new MP3s with the same file names.
