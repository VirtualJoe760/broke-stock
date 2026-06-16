# Digest 004 — Hermes as a conversational Telegram analyst

- **Source:** YouTube (AI Pathways / aipathways.io) — setting up Hermes as a 24/7 conversational trading analyst you chat with on Telegram. Heavily affiliate-driven (Hostinger VPS one-click, paid community, 1:1 consulting).
- **No performance claim** — this is a tooling/setup tutorial, not a results video. Nothing to debunk; the value is the pattern.
- **Extracted strategy:** [003 — the wheel (options income)](../../04-strategies/003-the-wheel-options-income.md)

## What it is (and how it relates to digest 003)

Same framework as [digest 003](003-hermes-self-improving-agent.md), used differently. Useful clarification: **Hermes is an open-source agent framework by Nous Research** — persistent memory, a built-in scheduler (cron), a self-learning loop that writes "skills" files, and tools (web browse, code execution, computer use).

- **Interface:** chat with it like an employee on **Telegram/Discord/Slack/iMessage** — approve trades from your phone without opening a laptop.
- **LLM:** ChatGPT Codex (~$20/mo subscription), Claude ("a bit more powerful"), or any API via OpenRouter.
- **Hosting:** local or a VPS (recommended for 24/7; the video pushes Hostinger's one-click deploy via affiliate link).
- **Multi-agent:** run several specialized Hermes agents (trader / researcher / morning-brief), each excelling at one task.
- **Demoed uses:** morning briefing (VIX macro regime + portfolio review), insider-activity research (web + filings), "scan for new longs" (macro gate → picks with bull/bear/catalyst/IV), and pre-trade checks → a suggested trade ticket with starter size and stops on a $200k account.

Creator describes themselves as a **swing trader who also runs the wheel** on options, entering when VIX < 20 — i.e. squarely in our scope ([ADR-002](../../00-overview/decisions-log.md)).

## Two usage modes (the useful distinction vs. digest 003)

- **Digest 003:** Hermes deployed *autonomously*, self-modifying a live strategy on real money (high risk; gated by [ADR-009](../../00-overview/decisions-log.md)).
- **Digest 004:** Hermes as a *conversational, human-in-the-loop analyst* — it researches, briefs, proposes; the human approves. This is the safer mode and aligns with our [human-in-the-loop stance](../../00-overview/decisions-log.md) (ADR-004), our [alerts](../../03-voice-and-alerts/alerts-and-notifications.md), and the [Jarvis layer](../../03-voice-and-alerts/jarvis-mcp.md).

## Honest read

- **More sober than 003** (no return claim) but **heavily commercial** — the video is an affiliate funnel (Hostinger, community, consulting). Treat enthusiasm accordingly.
- **Security surface to respect:** an open-source agent with code-execution + computer-use tools, holding broker credentials on a VPS, is a real attack/operational surface. Secrets hygiene and sandboxing are non-negotiable ([compliance](../../06-compliance/regulatory-and-risk.md), [ADR-008](../../00-overview/decisions-log.md)).
- **Self-learning ≠ self-modifying-strategy.** Building *workflow/research* skills from chat is low-risk and useful. Self-modifying *trading parameters* on live capital is the gated case ([ADR-009](../../00-overview/decisions-log.md)). Keep the two separate.

## What we adopt vs. reject

**Adopt:**
- **Conversational analyst via messaging** as a human-in-the-loop interface, complementing dashboards + voice (Telegram/Discord channel → [alerts & notifications](../../03-voice-and-alerts/alerts-and-notifications.md)).
- **Multi-agent specialization** (trader / researcher / brief) — already noted in [self-improvement & optimization](../../01-architecture/self-improvement-and-optimization.md).
- **The wheel** as a testable, in-scope options strategy → [strategy 003](../../04-strategies/003-the-wheel-options-income.md).
- Hermes (Nous Research) noted as a real **reference runtime** ([agent runtime & scheduling](../../01-architecture/agent-runtime-and-scheduling.md)).

**Reject / gate:**
- Adopting Hermes wholesale as *our* runtime — we control our stack ([ADR-006](../../00-overview/decisions-log.md), [ADR-007](../../00-overview/decisions-log.md)); we borrow patterns, and any agent that touches money still goes through the risk gate and validation ladder.
- Broker creds + code-exec on an agent without strict secrets/sandboxing.
- Self-modifying live strategy logic ([ADR-009](../../00-overview/decisions-log.md)).
