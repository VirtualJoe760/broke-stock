# broke web

Next.js (App Router) + TypeScript frontend. Hosts the two dashboards:

- [Trader cockpit](../../docs/02-frontend/trader-dashboard.md) — `/trader`
- [Content digest](../../docs/02-frontend/content-dashboard.md) — `/digest`

Talks to the engine over the [API](../../docs/01-architecture/api-orchestration.md); currently uses `lib/mock.ts` (paper-mode mock data) until the API is wired.

## Run

```
npm install        # not run during the offline build — do this first
npm run dev        # http://localhost:3000
```

## Status

Hand-written scaffold (no `npm install` yet): App Router layout, dark theme, landing page, shared mock data. Dashboard pages (`/trader`, `/digest`) are built in subsequent passes. Charts use `lightweight-charts`.
