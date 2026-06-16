# Deployment & portability

> Status: drafted. Goal: develop on Windows, run on the Mac mini, deploy to any VPS — without porting anything.

## Principle: the container is the portability layer

The engine + agent + API are packaged as **Docker** images and orchestrated with **docker-compose**. "Moving the project to the Mac mini" or "deploying to a VPS" is not a port — it's `git clone` → set `.env` → `docker compose up`. Identical behavior on Windows, macOS, and Linux.

## The dev → runtime → deploy path

| Stage | Host | Role |
|---|---|---|
| Develop | Windows PC | write code, run tests, build images |
| Runtime | Mac mini (Apple Silicon) | run the agent/engine 24/7 at home |
| Deploy | VPS (Linux x86) | optional cloud hosting / distribution targets |

## Multi-arch is mandatory

The Mac mini is **ARM64 (Apple Silicon)**; most VPS are **x86 (amd64)**. NautilusTrader and some quant libs have native components that differ by arch. Build **multi-arch images** (`docker buildx` for `linux/amd64` + `linux/arm64`) and test on both. Cheap now, painful to retrofit.

## 12-factor discipline (what makes it cloneable)

- **Config via environment variables** — one `.env` per deployment, never committed.
- **Secrets externalized** — broker keys, LLM keys, DB URLs in env / a secret store, never in the repo or `CLAUDE.md` ([ADR-008](../00-overview/decisions-log.md)).
- **No hardcoded OS paths** in app code — OS-agnostic paths only (our *tooling* uses Windows paths; the *app* must not).
- **Stateless services + external state** — Postgres/Neon, object storage for data/snapshots; containers are restartable and disposable.
- **Reproducible builds** — pinned base images, a Python lockfile (uv/poetry), a Node lockfile.

## The compose stack

- `engine` — NautilusTrader + strategy logic + risk gate (Python).
- `api` — FastAPI (REST + WebSocket).
- `agent` — the conversational/scheduled analyst (propose-only).
- `worker`/`scheduler` — cron jobs, alert engine.
- External: Postgres (Neon), time-series store, object storage. Frontend (Next.js) deploys separately on Vercel.

## One-command deploy

`git clone` → copy `.env.example` to `.env` and fill keys → `docker compose up -d`. This is also the [distribution](distribution.md) mechanism for self-hosters.

## Open questions

- Where live snapshots/data persist across container restarts (object storage vs. mounted volume).
- CI to build + publish multi-arch images on push.
