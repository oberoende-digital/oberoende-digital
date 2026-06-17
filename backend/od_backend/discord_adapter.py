from __future__ import annotations

from dataclasses import dataclass

from .config import Settings


@dataclass(frozen=True)
class DiscordReadiness:
    configured: bool
    mode: str
    reason: str


def check_discord_readiness(settings: Settings) -> DiscordReadiness:
    if settings.discord_configured:
        return DiscordReadiness(
            True,
            "configured",
            "DISCORD_BOT_TOKEN and DISCORD_GUILD_ID are present; live connection still requires operator launch.",
        )
    return DiscordReadiness(False, "dry-run", "Discord credentials are absent; backend remains in dry-run/manual-test mode.")
