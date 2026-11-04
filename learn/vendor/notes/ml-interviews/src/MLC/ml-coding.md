# <a name="ml-coding"></a> 2. ML/Data Coding :robot:

This page is the canonical index for ML coding interview practice. Work through one category at a time: implement the prompt without looking, compare with the linked answer, test edge cases, and explain the trade-offs aloud.

The catalog is intentionally divided by interview skill rather than framework:

1. **Classic ML** — algorithms, data preparation, metrics, and training fundamentals.
2. **Language Models (LM)** — tokenization, attention, decoding, and sequence batching.
3. **Generative AI (GenAI)** — adaptation, retrieval, preference learning, and generation primitives.
4. **Agentic AI coding** — tools, orchestration, memory, retries, permissions, and termination.

Every catalog row has an answer. Python answers are deliberately interview-sized and self-contained; a few established visual exercises use an existing notebook as their answer.

## How to use this chapter

1. Pick a question and restate its input, output, shapes, and assumptions.
2. Implement a correct baseline without opening the answer.
3. Test a normal case and at least one boundary or failure case.
4. Compare with the linked answer, then discuss complexity and production trade-offs.
5. Revisit **Easy** questions in 15 minutes, **Medium** questions in 20–35 minutes, and **Hard** questions in 40–60+ minutes.

Run all Python answer tests from the repository root:

```bash
uv run --with numpy python -m unittest discover -s src/MLC/tests -p "test_*.py"
```

Difficulty colors: ![Easy](./assets/difficulty-easy.svg) ![Medium](./assets/difficulty-medium.svg) ![Hard](./assets/difficulty-hard.svg)

## Priority ML coding problems

### Classic ML

These questions cover the core implementation patterns expected in general ML, applied-science, and data-focused interviews.

| Problem | Difficulty | Tags | Company tags | Answer | Interview focus |
| --- | --- | --- | --- | --- | --- |
| Numerically stable softmax and cross-entropy | ![Easy](./assets/difficulty-easy.svg) | `NumPy`, probability, numerical stability | Apple, Meta, Google, Amazon | [Python](./problems/classic_ml/softmax_cross_entropy.py) | Max subtraction, log-sum-exp, shapes, class-index validation |
| Linear regression with gradient descent | ![Medium](./assets/difficulty-medium.svg) | regression, optimization, vectorization | — | [Python](./problems/classic_ml/linear_regression.py) · [Notebook](./notebooks/linear_regression_md.ipynb) | MSE gradients, bias, feature scale, convergence |
| Logistic regression with gradient descent | ![Hard](./assets/difficulty-hard.svg) | classification, optimization, numerical stability | Google, Meta, Amazon | [Python](./problems/classic_ml/logistic_regression.py) · [Notebook](./notebooks/logistic_regression_md.ipynb) | Stable sigmoid, binary targets, gradients, decision threshold |
| k-nearest neighbors | ![Medium](./assets/difficulty-medium.svg) | distance, vectorization, classification | Uber, LinkedIn, Meta | [Python](./problems/classic_ml/knn.py) · [Notebook](./notebooks/k_nearest_neighbors.ipynb) | Pairwise distances, top-k selection, ties, time and memory cost |
| k-means clustering | ![Medium](./assets/difficulty-medium.svg) | clustering, unsupervised learning, convergence | Uber, LinkedIn, Google, Amazon | [Python](./problems/classic_ml/kmeans.py) · [Notebook](./notebooks/k_means_2.ipynb) | Initialization, assignment/update steps, empty clusters |
| Decision-tree split | ![Medium](./assets/difficulty-medium.svg) | trees, Gini impurity, search | — | [Python](./problems/classic_ml/decision_tree_split.py) · [Notebook](./notebooks/decision_tree.ipynb) | Candidate thresholds, weighted impurity, stopping conditions |
| Principal component analysis | ![Medium](./assets/difficulty-medium.svg) | linear algebra, dimensionality reduction, SVD | — | [Python](./problems/classic_ml/pca.py) | Centering, component ordering, explained variance |
| 2D convolution | ![Medium](./assets/difficulty-medium.svg) | deep learning, computer vision, tensor shapes | — | [Python](./problems/classic_ml/conv2d.py) · [Notebook](./notebooks/convolution.ipynb) | Output shape, stride, cross-correlation versus convolution |
| Binary metrics and ROC-AUC | ![Medium](./assets/difficulty-medium.svg) | evaluation, ranking, class imbalance | — | [Python](./problems/classic_ml/binary_metrics_roc_auc.py) | Zero denominators, tied scores, rank interpretation |
| Reservoir sampling | ![Medium](./assets/difficulty-medium.svg) | streaming, probability, sampling | — | [Python](./problems/classic_ml/reservoir_sampling.py) | Unknown stream length, uniform inclusion probability, O(k) memory |
| Linear SVM and hinge loss | ![Medium](./assets/difficulty-medium.svg) | margin methods, optimization, classification | — | [Notebook](./notebooks/svm.ipynb) | Hinge loss, margin violations, regularization |
| Perceptron learning rule | ![Easy](./assets/difficulty-easy.svg) | online learning, linear classification | — | [Notebook](./notebooks/perceptron.ipynb) | Update condition, convergence assumptions, decision boundary |
| Feedforward neural network and backpropagation | ![Hard](./assets/difficulty-hard.svg) | neural networks, chain rule, gradients | — | [Notebook](./notebooks/feedforward.ipynb) | Forward cache, gradient flow, parameter updates, shape checks |
| Multiclass metrics and macro averaging | ![Medium](./assets/difficulty-medium.svg) | evaluation, confusion matrix, averaging | — | [Python](./problems/classic_ml/multiclass_metrics.py) | Per-class counts, macro versus micro, absent classes |
| Multinomial Naive Bayes for text | ![Medium](./assets/difficulty-medium.svg) | NLP, probability, smoothing | — | [Python](./problems/classic_ml/multinomial_naive_bayes.py) | Log space, Laplace smoothing, unseen tokens, independence assumption |
| Matrix factorization for recommendations | ![Medium](./assets/difficulty-medium.svg) | recommendation, embeddings, SGD | — | [Python](./problems/classic_ml/matrix_factorization.py) | Observed entries, regularization, latent rank, cold start |
| Gradient-boosting residual step | ![Hard](./assets/difficulty-hard.svg) | ensembles, residual fitting, regression trees | — | [Python](./problems/classic_ml/gradient_boosting_step.py) | Negative gradients, weak learner, learning-rate shrinkage |
| Train/validation/test split without leakage | ![Easy](./assets/difficulty-easy.svg) | data splitting, reproducibility, stratification | — | [Python](./problems/classic_ml/dataset_split.py) | Disjoint indices, class balance, train-only fitting |
| Feature standardization with training statistics | ![Easy](./assets/difficulty-easy.svg) | preprocessing, leakage, numerical stability | — | [Python](./problems/classic_ml/feature_standardization.py) | Fit/transform separation, constant features, shape validation |
| Missing values and unseen categories | ![Medium](./assets/difficulty-medium.svg) | preprocessing, imputation, categorical encoding | — | [Python](./problems/classic_ml/categorical_preprocessing.py) | Training-only state, unknown bucket, all-missing columns |
| Uniform, weighted, and stratified sampling | ![Medium](./assets/difficulty-medium.svg) | sampling, imbalance, reproducibility | — | [Python](./problems/classic_ml/sampling_strategies.py) | Replacement, normalized weights, per-class guarantees |
| Sample-weighted losses and streaming metrics | ![Medium](./assets/difficulty-medium.svg) | evaluation, streaming, distributed aggregation | — | [Python](./problems/classic_ml/streaming_weighted_mean.py) | Weight by sample count, mergeable state, empty state |

### Language Models (LM)

These questions move from text features to the token, attention, and decoding mechanics used by modern language models.

| Problem | Difficulty | Tags | Company tags | Answer | Interview focus |
| --- | --- | --- | --- | --- | --- |
| TF-IDF | ![Medium](./assets/difficulty-medium.svg) | NLP, sparse features, information retrieval | — | [Python](./problems/language_models/tfidf.py) | Token counts, document frequency, smoothing, vocabulary order |
| Scaled dot-product attention | ![Medium](./assets/difficulty-medium.svg) | attention, transformer, masking | — | [Python](./problems/language_models/scaled_dot_product_attention.py) | Q/K/V shapes, 1/sqrt(d_k), masking before stable softmax |
| Learn and apply byte-pair encoding | ![Easy](./assets/difficulty-easy.svg) | tokenization, BPE, vocabulary | — | [Python](./problems/language_models/byte_pair_encoding.py) | Pair counts, deterministic merges, unseen-word encoding |
| Build a causal attention mask | ![Easy](./assets/difficulty-easy.svg) | transformer, masking, autoregressive decoding | — | [Python](./problems/language_models/causal_attention_mask.py) | Query/key semantics, padding, boolean-mask convention |
| Sinusoidal positional encoding | ![Easy](./assets/difficulty-easy.svg) | transformer, position, vectorization | — | [Python](./problems/language_models/sinusoidal_position_encoding.py) | Alternating sine/cosine channels, odd widths, shape |
| Temperature, top-k, and top-p sampling | ![Medium](./assets/difficulty-medium.svg) | decoding, probability, generation | Anthropic, OpenAI, DeepMind | [Python](./problems/language_models/top_k_top_p_sampling.py) | Filtering order, renormalization, deterministic tests |
| Append-only KV cache | ![Medium](./assets/difficulty-medium.svg) | inference, attention, latency, memory | Anthropic, OpenAI, Meta, Perplexity | [Python](./problems/language_models/kv_cache.py) | Cache shape, capacity, prefill versus decode, memory growth |
| Pad variable-length token batches | ![Medium](./assets/difficulty-medium.svg) | batching, padding, masks | — | [Python](./problems/language_models/padded_batches.py) | Padding ID, validity mask, empty sequences, batch shape |

### Generative AI (GenAI)

These are compact implementations of common fine-tuning, retrieval, alignment, and generation building blocks.

| Problem | Difficulty | Tags | Company tags | Answer | Interview focus |
| --- | --- | --- | --- | --- | --- |
| LoRA update for a linear layer | ![Medium](./assets/difficulty-medium.svg) | fine-tuning, low rank, linear algebra | Meta, Google, Anthropic, OpenAI, Databricks | [Python](./problems/genai/lora_linear.py) | Matrix shapes, alpha/r scaling, parameter savings, merging |
| Symmetric contrastive loss | ![Medium](./assets/difficulty-medium.svg) | embeddings, InfoNCE, multimodal | OpenAI, Anthropic, DeepMind, Midjourney | [Python](./problems/genai/contrastive_loss.py) | Normalization, temperature, in-batch negatives, two directions |
| Exact cosine top-k retrieval for RAG | ![Medium](./assets/difficulty-medium.svg) | RAG, embeddings, retrieval, ranking | — | [Python](./problems/genai/rag_retrieval.py) | Normalization, top-k ordering, zero vectors, production ANN trade-offs |
| Direct Preference Optimization loss | ![Hard](./assets/difficulty-hard.svg) | alignment, preference learning, fine-tuning | Anthropic, OpenAI, DeepMind, Meta | [Python](./problems/genai/dpo_loss.py) | Policy/reference log-probability gaps, beta, stable log-sigmoid |
| Classifier-free guidance combination | ![Easy](./assets/difficulty-easy.svg) | diffusion, guidance, generation | — | [Python](./problems/genai/classifier_free_guidance.py) | Conditional/unconditional predictions, guidance scale trade-off |

### Agentic AI coding

These questions test the deterministic control plane around a model. The reference answers keep permissions, budgets, retries, and termination in code rather than relying on prompt text alone.

| Problem | Difficulty | Tags | Company tags | Answer | Interview focus |
| --- | --- | --- | --- | --- | --- |
| Validate JSON tool arguments | ![Easy](./assets/difficulty-easy.svg) | tools, schema, validation | — | [Python](./problems/agentic_ai/tool_argument_validation.py) | Required fields, types, enums, unexpected arguments |
| Permission-aware tool registry | ![Medium](./assets/difficulty-medium.svg) | tools, permissions, function calling | — | [Python](./problems/agentic_ai/tool_registry.py) | Registration, signature binding, side-effect approval boundary |
| Planner/executor boundary | ![Medium](./assets/difficulty-medium.svg) | planning, orchestration, tracing | — | [Python](./problems/agentic_ai/planner_executor.py) | Bounded plan, structured results, partial failure |
| Retry with idempotency | ![Medium](./assets/difficulty-medium.svg) | reliability, retries, side effects | — | [Python](./problems/agentic_ai/retry_with_idempotency.py) | Transient errors, exponential backoff, duplicate suppression |
| Sliding-window conversation memory | ![Medium](./assets/difficulty-medium.svg) | memory, context window, token budget | — | [Python](./problems/agentic_ai/sliding_window_memory.py) | Pinned instructions, recent history, eviction, summarization trade-off |
| Bounded agent tool-use loop | ![Hard](./assets/difficulty-hard.svg) | agents, tools, termination, safety | — | [Python](./problems/agentic_ai/bounded_agent_loop.py) | Step budget, repeated-call detection, unknown tools, traceability |

## Extended practice

- [PyTorch ML Coding Problems](./pytorch-ml-coding.md) is the extended framework-specific drill bank. It is supplementary; the four tables above are the canonical question index.
- [Legacy notebooks](./notebooks/) remain available for visual and exploratory practice. The canonical tables link only the notebooks used as current answers or supplements.
- [Agentic AI Systems interview prep](https://github.com/alirezadir/Agentic-AI-Systems/tree/main/06_interview_prep) covers the system-design layer that complements the agentic coding exercises here.

## Difficulty and company-tag policy

- **Easy:** one focused operation, usually about 15 minutes.
- **Medium:** multiple steps or meaningful edge cases, usually 20–35 minutes.
- **Hard:** interacting components, advanced debugging, or systems trade-offs, usually 40–60+ minutes.

Difficulty is an editorial judgment about the complete prompt. Exact matches were calibrated against [TorchLeet](https://github.com/Exorust/TorchLeet) and [Deep-ML](https://www.deep-ml.com/problems); unmatched prompts use the same scope-based rubric. Company tags appear only when a reference associates the company with the same implementation problem. They are historical preparation signals, not claims about a current interview loop. This repository uses metadata only and does not copy third-party prompts or answers.

## What to explain during the interview

1. State shapes, dtypes, assumptions, and expected outputs before coding.
2. Start with a correct baseline, then optimize the bottleneck.
3. Discuss time and space complexity, including large intermediate matrices and model state.
4. Handle numerical stability, empty inputs, invalid labels, ties, and permission boundaries.
5. Write a normal-case test and at least one failure or boundary test.
6. Explain how the answer changes for large datasets, GPUs, distributed execution, or production services.
