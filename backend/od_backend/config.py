from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    environment: str = "local"
    database_path: Path = Path("data/backend/od_backend.sqlite3")
    discord_bot_token: str | None = None
    discord_guild_id: str | None = None
    llm_provider: str = "disabled"
    synthetic_disclosure: str = "AI-generated synthetic OD agent response; human operator remains accountable."

    @property
    def discord_configured(self) -> bool:
        return bool(self.discord_bot_token and self.discord_guild_id)


def load_settings() -> Settings:
    return Settings(
        environment=os.getenv("OD_ENV", "local"),
        database_path=Path(os.getenv("OD_BACKEND_DB", "data/backend/od_backend.sqlite3")),
        discord_bot_token=os.getenv("DISCORD_BOT_TOKEN") or None,
        discord_guild_id=os.getenv("DISCORD_GUILD_ID") or None,
        llm_provider=os.getenv("OD_LLM_PROVIDER", "disabled"),
        synthetic_disclosure=os.getenv(
            "OD_SYNTHETIC_DISCLOSURE",
            "AI-generated synthetic OD agent response; human operator remains accountable.",
        ),
    )
