# Documentation

## Map

| Section | Contents |
|---|---|
| [00-overview](00-overview/) | System overview, decisions log, glossary |
| [01-architecture](01-architecture/) | Engine & parity, runtime & scheduling, self-improvement, data, signal, strategy, risk, execution, persistence, API |
| [02-frontend](02-frontend/) | Content dashboard, trader dashboard |
| [03-voice-and-alerts](03-voice-and-alerts/) | Jarvis MCP, alerts & notifications |
| [04-strategies](04-strategies/) | Strategy library — every hypothesis + its validation status |
| [05-research](05-research/) | Validation methodology, video digests |
| [06-compliance](06-compliance/) | Regulatory & risk |
| [07-roadmap](07-roadmap/) | Build phasing |
| [08-deployment](08-deployment/) | Deployment & portability, distribution, model hosting |

## The two recurring workflows

**Digesting a video / idea** → write a [video digest](05-research/video-digests/), extract a strategy using the [template](04-strategies/_TEMPLATE.md), register it in the [strategy library](04-strategies/README.md) at validation level L0.

**Validating a strategy** → move it up the [validation ladder](05-research/validation-methodology.md). Update its status in the library. Nothing is "proven" until it clears L4.
