"""Environment-driven configuration. All secrets come from env / .env — never hardcoded.

See docs/08-deployment/deployment-and-portability.md (12-factor) and .env.example.
"""

from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Load env from the engine dir AND the repo root, so a key in services/engine/.env
# OR broke/.env OR broke/.env.local all work (later files win). Resolved from this
# file's location, so it's independent of the current working directory.
_ENGINE_DIR = Path(__file__).resolve().parents[1]  # services/engine
_REPO_ROOT = Path(__file__).resolve().parents[3]  # broke


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            str(_ENGINE_DIR / ".env"),
            str(_REPO_ROOT / ".env"),
            str(_REPO_ROOT / ".env.local"),
        ),
        extra="ignore",
    )

    # Mode
    trading_mode: str = "paper"  # paper | live

    # LLM provider (swappable — see llm/provider.py)
    llm_provider: str = "anthropic"  # anthropic | openai-compatible
    anthropic_api_key: str | None = None
    llm_model: str = "claude-opus-4-8"
    openai_compatible_base_url: str | None = None
    openai_compatible_api_key: str | None = None
    triage_model: str | None = None

    # Broker
    alpaca_api_key: str | None = None
    alpaca_api_secret: str | None = None
    alpaca_paper: bool = True

    # Data
    polygon_api_key: str | None = None
    polygon_base_url: str = "https://api.polygon.io"  # rebrand: set to api.massive.com if needed
    databento_api_key: str | None = None
    perplexity_api_key: str | None = None
    fmp_api_key: str | None = None  # Financial Modeling Prep — transcripts + fundamentals

    # Datastores
    database_url: str | None = None
    redis_url: str = "redis://redis:6379"
    questdb_host: str = "questdb"
    questdb_port: int = 9009

    # Notifications
    telegram_bot_token: str | None = None
    telegram_chat_id: str | None = None

    @property
    def is_live(self) -> bool:
        return self.trading_mode.lower() == "live"


settings = Settings()
