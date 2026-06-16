# Multi-tenancy & memberships

> Status: drafted. The broke.finance SaaS foundation ([ADR-015](../00-overview/decisions-log.md)).

## Model

A multi-tenant membership product. Every user gets their own customizable instance of the feed + tooling; we sell access (tiers), **not** money management.

**Bundled with thinkbigjoe ([ADR-016](../00-overview/decisions-log.md)):** broke.finance is a product *under the thinkbigjoe consulting umbrella*, so it **shares thinkbigjoe's Neon database and better-auth** (one login across the ecosystem — advisors get SSO). broke's tables live in a dedicated **`broke` Postgres schema** (`pgSchema("broke")`) so they never collide with thinkbigjoe's tables in the same DB.

- **Auth:** shared better-auth (thinkbigjoe's). App data references the better-auth **user id** (text). broke does not run its own separate auth.
- **Tenant scoping:** every app row carries a `user_id`. `accounts` (paper/live) belong to a user; `orders`/`positions`/`fills` hang off the account. The API only ever returns the caller's own rows.
- **Customization:** `user_preferences` (feed config + risk prefs as JSON), `watchlist_items`, `follows` (congress members / funds / in-app strategies / copy-platform traders).
- **BYO broker:** `broker_connections` stores `provider`, `mode`, `status`, and a `credentials_ref` — **a pointer to an encrypted secret store, never the raw key.** We never hold funds or place trades as a manager.
- **Memberships:** `memberships` (tier free/pro/broker, status, Stripe customer id, period end). Billing wired later via Stripe.

## The bright line (compliance)

We are a **software + signals + copy-ideas** product. Users execute in **their own** broker (BYO) or paper. We do not custody funds or manage accounts → not a broker-dealer/RIA. Signals and copy-ideas are **educational/informational with disclaimers**, not personalized investment advice. See [regulatory & risk](../06-compliance/regulatory-and-risk.md).

## Data model (Drizzle, `packages/db`)

`accounts` (now `user_id`-scoped), `user_preferences`, `watchlist_items`, `follows`, `broker_connections`, `memberships` — plus the existing `strategies`, `orders`, `positions`, `fills`, `audit`.

## To build

- better-auth wiring in `apps/web` (login/signup, session) + Neon connection.
- Session-scoped API (every endpoint filters by the caller's `user_id`).
- Per-user feed: the digest/cockpit read `user_preferences` + `watchlist_items` + `follows`.
- Encrypted secret store for BYO broker creds.
- Stripe for membership tiers.
- Tenant isolation tests (a user can never read another user's rows).
