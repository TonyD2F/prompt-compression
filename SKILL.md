---
name: prompt-compression
description: Optimize prompts for token efficiency and quality. Use for user-style production responses, token minimization techniques, prompt compression algorithms (LLMLingua family), and LongLLMLingua RAG optimization. Triggers include prompt compression, token optimization, LongLLMLingua, RAG cost reduction, minimize tokens, no mock data, production-ready prompts.
---

# Prompt Compression

Apply production-grade prompt optimization. Prioritize token minimization while preserving or improving output quality. Never use mock data.

## User Response Style (always apply)

- Deliver complete, state-of-the-art, production-ready results.
- Chat replies: short, lead with the answer.
- Code/docs/configs: put full detail in the file or artifact. No filler.
- Clarify first: if goal, scope, platform, or format is missing, ask 1-3 multiple-choice questions. If already specific, state any assumption in one line.
- Research, do not guess: for current facts, tools, or recommendations, use tools. Say "unverified" when needed.
- Build workflow: after research, write a task checklist and mark each task done as finished. Keep every quality-affecting step.
- Verify: run and test code (syntax + real execution) before delivery. Final check against original request once.
- Free-tier constraint: minimize tokens aggressively. Deliver only the tested file when possible.

## Token Optimization Techniques

1. Front-load strictest constraints.
2. Delete filler language ("please", "kindly", "make sure to", "I would like you to", etc.).
3. Prefer short imperative sentences.
4. Collapse lists into dense lines when readable.
5. One concept = one short sentence. Avoid restatement.
6. Remove examples unless critical.
7. Put absolute priorities in ALL CAPS or at top/bottom extremes.
8. No polite closers or meta-instructions.
9. Separate prompt components explicitly (instruction / question / context / examples) — sensitivity differs.

## Prompt Compression Algorithms (2026)

### Hard / Extractive (preferred — no hallucination)
- **LLMLingua-2**: BERT-level token classifier (XLM-RoBERTa). 2–5× (up to 8×). ~150 ms. Task-agnostic, multilingual. Best general-purpose default.
- **LongLLMLingua**: Query-aware coarse-to-fine + reordering. Best for RAG. 4–10×. Often improves accuracy.
- **Selective-Context**: Self-information / perplexity scoring.
- **RECOMP (extractive)**: Sentence selection. Fastest (~80 ms) when verbatim text is required.
- Lexical pipelines (stopword, POS, entity preservation): training-free, 30–40% reduction.

### Abstractive
- SCOPE, Cmprsr, LLM summarization: higher ratios possible but risk paraphrase drift. Use only when extractive is insufficient.

### Decision rules
- Static system prompts → manual restructuring + provider prompt caching.
- RAG / multi-document → LongLLMLingua (or top-k rerank + LongLLMLingua).
- General dynamic prompts → LLMLingua-2.
- Need exact wording (legal, compliance, code) → pure extractive / lexical only.
- Code & tool-call JSON → protect with `force_tokens` or skip aggressive compression.

## LongLLMLingua for RAG

Four-stage pipeline:

1. Question-aware coarse-grained: score documents by p(question | document). Keep relevant ones.
2. Document reordering: place highest-relevance docs at start and end (mitigates lost-in-the-middle).
3. Question-aware fine-grained: contrastive perplexity  
   `s_i = PPL(token | context) - PPL(token | question, context)`.  
   Dynamic budgets favor high-relevance documents.
4. Subsequence recovery: restore fragmented entities.

Typical results: +21.4% accuracy at ~4× fewer tokens on NaturalQuestions; 1.4–2.6× latency speedup.

### Usage (LongLLMLingua)

```python
from llmlingua import PromptCompressor

compressor = PromptCompressor()
result = compressor.compress_prompt(
    context=retrieved_chunks,
    instruction="Answer based on the context.",
    question=user_question,
    target_token=500,                       # or rate=0.25
    rank_method="longllmlingua",
    condition_in_question="after",
    reorder_context="sort",
    dynamic_context_compression_ratio=0.3,
    condition_compare=True,
    force_tokens=["\n", "?", "```"],        # protect structure
)
```

### Usage (LLMLingua-2 — faster general case)

```python
compressor = PromptCompressor(
    model_name="microsoft/llmlingua-2-xlm-roberta-large-meetingbank",
    use_llmlingua2=True,
)
result = compressor.compress_prompt(prompt, rate=0.33, force_tokens=["\n", "?"])
```

See `scripts/longllmlingua_example.py` for a complete working example.

Official library: https://github.com/microsoft/LLMLingua

## Practical limits & best practices (from 2026 deployments)

- Always separate instruction / question / context before compression.
- Start at 2–4× and validate accuracy; do not max the ratio first.
- Protect code blocks, tool schemas, numbers, and negations with `force_tokens`.
- Query-aware methods cannot cache the compressed result across different questions.
- Aggressive compression harms code structure — prefer lighter ratios or manual extraction for code-heavy contexts.
- After compression, verify downstream task accuracy on a held-out set.

## Limitations to respect

- Query-aware → no cross-question caching.
- Code & highly structured text resist compression.
- Always measure end-task quality, not just token count.

