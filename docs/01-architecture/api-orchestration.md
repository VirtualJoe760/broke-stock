# API / orchestration

## Responsibility

The boundary between the Python engine and the TypeScript web / voice / agent layers.

## Surface

- **FastAPI** service co-located with the engine.
- **REST** for account/history/config/strategy actions.
- **WebSocket** for streaming quotes, fills, P&L, signals, and alerts to the dashboards and voice layer.
- Auth via better-auth-issued sessions/tokens.

## REST endpoints (draft)

- `GET /portfolio` · `GET /positions` · `GET /orders` · `GET /account`
- `POST /orders` (proposed → requires approval for live) · `DELETE /orders/{id}`
- `GET /strategies` · `GET /strategies/{id}` · `PATCH /strategies/{id}` (config/params)
- `GET /signals` · `GET /digest/today`
- `GET /alerts` · `POST /alerts/rules`

## WebSocket channels (draft)

`quotes`, `fills`, `pnl`, `signals`, `alerts` — the dashboards subscribe; the [Jarvis layer](../03-voice-and-alerts/jarvis-mcp.md) consumes the same streams.

## Approval flow

Order endpoints return a **proposed** order for live mode; execution only proceeds after explicit approval ([risk gate](risk-gate.md), [ADR-004](../00-overview/decisions-log.md)). Paper mode may auto-execute within limits.

## Deployment note

The engine + API is a **stateful, long-running service** — it runs on the Mac mini or a Linux VPS in a container, **not** serverless/Vercel. Only the Next.js frontend runs on Vercel ([ADR-006](../00-overview/decisions-log.md), [deployment](../08-deployment/deployment-and-portability.md)).

## AuthN/Z across surfaces

One identity model spans web, voice/MCP, and the agent. Tokens are scoped; the agent and voice get **propose-only** scopes on the money path.

## Open questions

- Payload schemas + versioning.
- How the MCP/agent authenticates to the API (service token vs. user-delegated).
