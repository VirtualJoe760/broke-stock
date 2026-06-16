# Jarvis MCP (voice layer)

> Status: drafted.

The voice layer is a "Jarvis" that reads the daily digest, answers spoken questions about the portfolio, and showcases the content board. It is built as **two MCP layers**, not one.

## Topology

- **ElevenLabs MCP / API** = the mouth and ears. Ships officially: streaming TTS (Flash ~75ms), STT, voice cloning, voice design, sound effects, and full Conversational AI agents with native turn-taking + tool calling. We do not rebuild this.
- **Custom Jarvis MCP** = the domain brain. Assembles the digest, curates the content board, evaluates alert rules, holds the persona/preferences, and exposes portfolio context. Delegates all audio to ElevenLabs.

## Tools (custom MCP)

**Briefing**
- `generate_daily_digest(date, sections[], persona)` → structured digest
- `build_briefing_script(digest_id, style)` → spoken script with v3 audio tags (calm brief vs. urgent alert)
- `narrate(text|digest_id, voice_id, model)` → audio URL (delegates to ElevenLabs)
- `schedule_briefing(time, days, channels[])`

**Content board**
- `list_content_board()` / `get_content_item(id)`
- `summarize_for_voice(id)` → ~15s spoken TL;DR (reading articles verbatim is bad UX)
- `showcase(id)` → push to dashboard + narrate
- `rank_content(criteria)`

**Portfolio context** (bridges to the engine API)
- `get_portfolio_snapshot()`, `get_position_thesis(symbol)`, `get_market_movers()`

**Persona / prefs**
- `set_voice_persona(voice_id, name, verbosity, tone)`, `set_preferences(...)`

## Resources

`digest://today`, `portfolio://snapshot`, `content://board`, `alerts://active`

## Prompts

`morning_briefing`, `market_close_recap`, `explain_this_alert`, `whats_changed_since_open`

## Conversational loop

speak → STT → Claude → custom MCP tools → TTS reply, sub-second, via ElevenLabs Conversational AI with our tools attached. Claude is the reasoning layer; our MCP supplies the domain actions.

## Two hard constraints

- **Proactivity lives outside MCP.** MCP is pull-based. Timed briefings and "Jarvis warns you" come from the [scheduler + alert engine](alerts-and-notifications.md), which *calls* the narrate/dispatch tools.
- **Voice proposes, it never fires.** No live trade executes from a voice command without an explicit, separate confirmation step. See [risk gate](../01-architecture/risk-gate.md) and [compliance](../06-compliance/regulatory-and-risk.md).

## Cost

TTS is billed per character. Cache audio; regenerate only changed digest segments; pre-render the morning brief; stream only live conversation.
