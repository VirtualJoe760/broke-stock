# Content dashboard (financial digest)

## Purpose

The "understand & decide" surface. Calm, narrative, skimmable in 60 seconds, deep on demand.

## Features (priority)

- **AI daily brief** (hero) — overnight narrative + what it means today. [MVP]
- **"Why we hold what we hold"** — per-position thesis with surprise score + confidence. [MVP]
- **Scored news feed** — deduped, ranked, tied to holdings, with a "priced in?" flag. [MVP]
- **Curated articles & video** — embedded with an AI TL;DR. [MVP]
- Earnings center, sentiment heatmap, macro context (VIX/breadth/credit), thesis scorecard, explain-this layer. [Phase 2]

## Component inventory + data contracts

| Component | Source |
|---|---|
| Daily brief | `GET /digest/today` |
| Position theses | `GET /positions` + `GET /strategies/{id}` (thesis, surprise, confidence) |
| News feed | `signals` WS channel + `GET /signals` |
| Curated media | digest payload (links + AI TL;DR) |

## The bridge

Every thesis links to the live position it drove (trader dashboard); every position links back to its reasoning here. The round-trip *reason → trade → outcome* is the differentiator.

## Tech

Next.js + React + TS on Vercel; live updates over WebSocket to the [API](../01-architecture/api-orchestration.md). A chat-first version of this surface can also be delivered via the conversational agent / Telegram ([digest 004](../05-research/video-digests/004-hermes-telegram-analyst.md)).

## Reference

Mockup built during the design phase (AI daily brief, position theses, scored news, curated media).
