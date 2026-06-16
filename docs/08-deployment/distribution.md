# Distribution

> ⚠️ **SUPERSEDED.** The model is now a **multi-tenant membership SaaS** at broke.finance ([ADR-015](../00-overview/decisions-log.md)) — software/signals only, users BYO broker, we never hold funds. The single-tenant self-host model below ([ADR-012](../00-overview/decisions-log.md)) is kept for history.

> ~~Status: drafted. Model chosen: **self-hostable, single-tenant, clone & deploy** (ADR-012).~~

## The model

Each user deploys **their own isolated instance** with **their own broker keys**, on their own machine (Mac mini) or VPS. We do not host a multi-tenant app and we do not hold anyone else's credentials or money.

```
user clones repo → fills their own .env → docker compose up → their own private instance
```

## Why single-tenant (the compliance reason)

Hosting other people's accounts, broker credentials, and money would put us in **custody** and trigger heavy FINRA/SEC obligations ([regulatory-and-risk](../06-compliance/regulatory-and-risk.md)). Single-tenant self-hosting sidesteps almost all of it: each user runs their own software, with their own keys, bearing their own risk. It also matches the "clone & deploy from a VPS" goal directly.

## What this requires of the build

- **Config-driven, zero hardcoded identity** — no baked-in accounts, keys, or user-specific values. Everything per-deployment via `.env` ([deployment & portability](deployment-and-portability.md)).
- **First-run setup** — a guided onboarding (broker keys, strategy selection, risk limits, messaging channel) instead of assuming our own setup.
- **Update mechanism** — `git pull` + image pull, or a versioned release; document the upgrade path so self-hosters can take new versions safely (esp. migrations).
- **Sane, safe defaults** — ships in **paper mode**, conservative risk limits, no strategy live until the user opts in. A fresh clone must never trade real money by accident.
- **Licensing & terms** — license the repo, and ship clear "not financial advice / simulated results / use at your own risk" terms ([compliance](../06-compliance/regulatory-and-risk.md)).
- **Optional telemetry** — if we collect any usage data, it's opt-in and privacy-respecting (self-hosters expect data to stay on their box).

## What we explicitly are NOT doing (for now)

- Multi-tenant SaaS holding user funds/credentials (custody/regulatory burden).
- A shared hosted "user base."

These remain possible later only if an equities track is L4-proven and there's a deliberate, separately-reviewed case ([ADR-010](../00-overview/decisions-log.md), [ADR-012](../00-overview/decisions-log.md)).

## Open questions

- Packaging: raw repo + compose, a one-click VPS template (e.g. Hostinger/Railway), or both?
- How strategies are distributed: bundled, or a separate opt-in strategy pack?
