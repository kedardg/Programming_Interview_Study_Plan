"""job-prep only: embed the original figures from raw/resources/images/ next to the
notebook sections that reproduce them as animations, so the reader can compare
the source diagram with the interactive version.

Run from the job-prep repository root:

    python3 scripts/add_source_figures.py

Idempotent: existing figure cards are replaced. Figures are referenced by
relative path (not copied), so this is a no-op in a checkout without raw/.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEARN = ROOT / "learning_content" / "llm"
IMG = "../../raw/resources/images"
BOOK = "Alisa Liu's Book of LLMs"
NATO = "Nathan Lambert, AI PhD Job Hunt"

# (page, anchor-text regex that marks the section to append after, figure path, caption)
FIGURES = [
    ("deep-learning.html", r'id="decisionBoundary"|why one hidden layer', f"{IMG}/alisa-book-of-llms/01-image.png", f"Figure 1 in {BOOK}: a linear classifier's boundary vs a one-hidden-layer MLP's on the same points — reproduced live above."),
    ("deep-learning.html", r'backward pass|Backward pass', f"{IMG}/alisa-book-of-llms/02-image.png", f"Figure 2 in {BOOK}: the single-neuron / small-MLP diagram the backprop walkthrough above animates."),
    ("ml-coding.html", r'computational graph|Computational graph', f"{IMG}/alisa-book-of-llms/03-image.png", f"Figure 3 in {BOOK} (from CS224N): forward values and local gradients on f=(x+y)·max(y,z) — the graph animation above uses the same method."),
    ("transformers.html", r'shape-annotated dataflow', f"{IMG}/alisa-book-of-llms/04-image.png", f"Figure 4 in {BOOK}: the decoder block as an einsum dataflow — reproduced as the interactive above."),
    ("attention.html", r'attention patterns as masks', f"{IMG}/alisa-book-of-llms/05-image.png", f"Figure 5 in {BOOK} (from Longformer): full, sliding-window, dilated, and global+sliding attention — the mask explorer above draws each."),
    ("attention.html", r'head-sharing|Multi-head', f"{IMG}/alisa-book-of-llms/06-image.png", f"Figure 6 in {BOOK}: MHA, GQA, MQA, MLA and what each caches — the head-sharing animation above."),
    ("architectures.html", r'id="rnn"', f"{IMG}/alisa-book-of-llms/07-rnn.png", f"Figure 7 in {BOOK}: the unrolled RNN — the gradient-through-time interactive above."),
    ("parallelism.html", r'what each collective does', f"{IMG}/alisa-book-of-llms/08-collectives.png", f"Figure 8 in {BOOK}: reduce-scatter, all-gather and all-reduce as data layouts — the collective explorer above."),
    ("parallelism.html", r'sharding notation', f"{IMG}/alisa-book-of-llms/09-image.png", f"Figure 9 in {BOOK} (notation from How to Scale Your Model, ch. 4): every sharding of A[I, J] over a 2×2 mesh."),
    ("parallelism.html", r'sharded-matmul rule', f"{IMG}/alisa-book-of-llms/10-parallelism.png", f"Figure 10 in {BOOK}: multiplying sharded matrices — the rule the explorer above applies."),
    ("parallelism.html", r'Tensor parallelism|tensor parallelism', f"{IMG}/alisa-book-of-llms/11-mlp-tp.png", f"Figure 11 in {BOOK}: column-sharded up-projection, row-sharded down-projection, one all-reduce — the Megatron animation above."),
    ("multimodal.html", r'LLaVA', f"{IMG}/alisa-book-of-llms/12-llava_arch.png", f"Figure 12 in {BOOK} (from LLaVA): vision encoder → projection → language model."),
    ("interview-journey.html", r'two-lane timeline|timeline', f"{IMG}/natolambert-ai-phd-job-hunt/calls-timeline.png", f"{NATO}: his networking calls and interviews per day, Oct 2021 – Mar 2022 — the data behind the timeline above."),
    ("interview-journey.html", r'two-lane timeline|timeline', f"{IMG}/natolambert-ai-phd-job-hunt/interview-results.png", f"{NATO}: every company's process as a Gantt chart with outcomes (offer / withdrawn / ghosted / rejected)."),
]

CARD = '<div class="card source-figure"><details><summary>Source figure — {title}</summary><img src="{src}" alt="{alt}" loading="lazy" style="max-width:100%;border-radius:8px;background:#fff;margin-top:8px"><p class="caption">{cap}</p></details></div>\n'

def place(html, pattern, card):
    m = re.search(pattern, html, re.I)
    if not m:
        return html, False
    # append the card at the end of the enclosing <div class="card"> if inside one, else after the next </div> or </p>
    start = html.rfind('<div class="card', 0, m.start())
    if start != -1:
        depth, i = 0, start
        while i < len(html):
            nxt_open = html.find('<div', i); nxt_close = html.find('</div>', i)
            if nxt_close == -1: break
            if nxt_open != -1 and nxt_open < nxt_close: depth += 1; i = nxt_open + 4
            else:
                depth -= 1; i = nxt_close + 6
                if depth == 0: return html[:i] + "\n" + card + html[i:], True
    end = html.find('</p>', m.end())
    end = end + 4 if end != -1 else m.end()
    return html[:end] + "\n" + card + html[end:], True

if __name__ == "__main__":
    pages = {}
    for page, pat, src, cap in FIGURES:
        pages.setdefault(page, []).append((pat, src, cap))
    for page, items in pages.items():
        f = LEARN / page
        if not f.exists():
            print("missing", page); continue
        html = f.read_text()
        html = re.sub(r'<div class="card source-figure">.*?</div>\n', '', html, flags=re.S)
        n = 0
        for pat, src, cap in items:
            title = cap.split(":")[0]
            html, ok = place(html, pat, CARD.format(title=title, src=src, alt=title, cap=cap))
            n += ok
            if not ok: print(f"  {page}: anchor not found for {src.rsplit('/',1)[-1]}")
        f.write_text(html); print(f"{page}: {n}/{len(items)} figures placed")
