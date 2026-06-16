# Model hosting

> Status: drafted. Decision: **cloud API default, swappable provider, no GPU required** ([ADR-011](../00-overview/decisions-log.md)). Local hosting is optional and, for us, mostly a *triage* cost-saver.

## Why API by default (the economics)

- **API = variable cost.** Pay per token. Our usage is bursty/low-volume (a few scheduled jobs/day) — realistically tens to a few hundred dollars/month.
- **Self-hosting = fixed cost.** A GPU runs 24/7 whether used or idle: ~$300–600/mo for a 24GB card, ~$700–1,500/mo for an A100. For an agent computing ~1–2 hrs/day, you pay for ~22 idle hours.

At our profile, **API is cheaper, not more expensive.** Self-hosting wins on cost only at high sustained throughput.

## The quality + hardware double-bind

- Open models that are actually good at the trading task (Qwen3-235B, Kimi-K2, DeepSeek) are **huge** → need multi-GPU hardware costing more than the API.
- Models cheap enough to self-host (7–13B) are **weaker** at the nuanced text→signal judgment the [signal layer](../01-architecture/signal-layer.md) needs.
- Frontier API models (Claude) remain best at the hard reasoning that drives edge.

So: small = cheap but worse; capable = good but pricier than API.

## Where local hosting *does* pay off for us

1. **The Mac mini is free compute we already own.** Run a small open model on it via **Ollama** (Apple Silicon, Metal) for **high-volume, low-difficulty triage** — first-pass news/headline classification — and route only the passes to Claude for real analysis. Cuts token spend where volume is high and judgment is cheap, without losing quality where it matters.
2. **Privacy** — for self-hosters who don't want data leaving their box.
3. **No rate limits / offline resilience.**

## The swappable provider interface

All model calls go through one interface; provider is config (`.env`):

- **Default:** Claude via the Anthropic API.
- **Triage (optional):** a local Ollama endpoint on the Mac mini.
- Both API and local servers (Ollama, vLLM) expose an **OpenAI-compatible endpoint**, so switching is just a `base_url` + model name — no app rework.

## If/when we self-host: how

- **Source weights:** HuggingFace (accept licenses; some gated). Ollama's registry is a simpler curated source; **GGUF** quantized builds for Mac/CPU.
- **Serving:** **Ollama** (easy, Mac-friendly, dev + small models) or **vLLM** (production throughput on a GPU VPS). Both OpenAI-compatible.
- **Model picks:** triage → Qwen/Llama 7–8B quantized (runs on the Mac mini); stronger local reasoning → Qwen3 / DeepSeek mid-size (mind the hardware).

## Bottom line

Don't self-host to dodge API fees on the reasoning — you'll pay more for worse output. The one early win is **small-model triage on the Mac mini**, with Claude doing the analysis.
