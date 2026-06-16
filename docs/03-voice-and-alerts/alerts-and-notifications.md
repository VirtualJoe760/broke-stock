# Alerts & notifications

> Status: drafted.

## Pull vs. push

The interactive surfaces (dashboards, voice Q&A) are **pull**. Alerts are **push** and must originate from a component that runs without a user present: the **scheduler + alert engine**, not MCP (which is pull-only). See [agent runtime & scheduling](../01-architecture/agent-runtime-and-scheduling.md).

## Trigger types

- **Price / position:** target hit, stop hit, trailing-stop breach, % move.
- **Risk:** exposure/concentration/daily-loss limit approached or breached (→ may also trip the [kill switch](../01-architecture/risk-gate.md)).
- **Signal:** new Claude signal above a confidence/surprise threshold on a holding or watchlist name.
- **News:** material news on a position (sentiment + "priced in?" flag).
- **Change detection:** **snapshot diff** — compare today's portfolio/option-chain snapshot to yesterday's to detect new strikes/expiries or large IV moves (reference design: digest 001).
- **Scheduled report:** the weekly review (reference: digest 002) — portfolio, return vs. benchmark, trade history, self-graded performance.

## Channels

- **Telegram / Slack / WhatsApp** — push to phone.
- **SMS (Twilio)** — for higher-urgency.
- **Email** — digests and reports.
- **ClickUp** (or the user's task tool) — weekly review reports (reference: digest 002).
- **Spoken** — render via [Jarvis](jarvis-mcp.md) TTS.
- **Outbound call** — top-urgency escalation: ElevenLabs Conversational AI calls the phone and reads the alert.

## Urgency tiers

| Tier | Example | Channel |
|---|---|---|
| Info | daily brief, weekly review | email / ClickUp / push |
| Notice | target hit, new high-confidence signal | Telegram + push |
| Urgent | stop hit, daily-loss limit, kill-switch trip | SMS + spoken |
| Critical | risk breach requiring action | outbound call + SMS |

## Audit

Every alert (trigger, content, channel, timestamp, and any generated audio) is logged to the [event store](../01-architecture/persistence-and-events.md) — for debugging and compliance.

## To detail

- Alert-rule schema; dedupe/snooze/quiet-hours; delivery retries
