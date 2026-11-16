# prompt-compression

Production-grade skill for token-efficient, high-quality prompting.

Optimized for agents that must stay brief, accurate, and cost-aware (especially free-tier / rate-limited models).

## What this skill does

- Enforces a strict **user response style** (complete, production-ready, minimal tokens, no mock data)
- Provides practical **token optimization techniques**
- Documents the current best **prompt compression algorithms** (LLMLingua family)
- Gives ready-to-use **LongLLMLingua** patterns for RAG cost & quality optimization

## When to use

Trigger this skill when the task involves any of:

- Prompt compression / token minimization
- LongLLMLingua or LLMLingua-2
- RAG cost reduction
- Production-ready agent responses under tight token budgets
- "No mock data" / free-tier Claude constraints

## Installation

Copy the folder into your agent skills directory:

```bash
# Example for Grok / compatible agents
cp -r prompt-compression /path/to/skills/
```
