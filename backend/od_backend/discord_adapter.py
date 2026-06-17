from __future__ import annotations

from dataclasses import dataclass
import json
import urllib.error
import urllib.request

from .audit_log import AuditLog
from .config import Settings
from .router import route_message

DISCORD_API_BASE = "https://discord.com/api/v10"


@dataclass(frozen=True)
class DiscordReadiness:
    configured: bool
    mode: str
    reason: str


@dataclass(frozen=True)
class DiscordIdentity:
    bot_id: str
    username: str
    discriminator: str | None = None

    @property
    def safe_label(self) -> str:
        if self.discriminator and self.discriminator != "0":
            return f"{self.username}#{self.discriminator} ({self.bot_id})"
        return f"{self.username} ({self.bot_id})"


@dataclass(frozen=True)
class DiscordGuild:
    guild_id: str
    name: str


@dataclass(frozen=True)
class DiscordValidation:
    configured: bool
    bot: DiscordIdentity | None
    guild: DiscordGuild | None
    errors: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return self.configured and not self.errors and self.bot is not None and self.guild is not None


def check_discord_readiness(settings: Settings) -> DiscordReadiness:
    if settings.discord_configured:
        mode = "live-post-gated" if not settings.discord_live_post_enabled else "live-post-enabled"
        return DiscordReadiness(
            True,
            mode,
            "DISCORD_BOT_TOKEN and DISCORD_GUILD_ID are present; live posting still requires the explicit live-post command.",
        )
    return DiscordReadiness(False, "dry-run", "Discord credentials are absent; backend remains in dry-run/manual-test mode.")


def _discord_get(token: str, path: str, timeout: int = 15) -> dict[str, object]:
    req = urllib.request.Request(
        f"{DISCORD_API_BASE}{path}",
        headers={"Authorization": f"Bot {token}", "User-Agent": "od-backend-phase1.5"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def validate_discord_credentials(settings: Settings) -> DiscordValidation:
    """Validate Discord bot identity and intended guild without printing or returning the token."""
    errors: list[str] = []
    if not settings.discord_bot_token:
        errors.append("DISCORD_BOT_TOKEN is missing")
    if not settings.discord_guild_id:
        errors.append("DISCORD_GUILD_ID is missing")
    if errors:
        return DiscordValidation(False, None, None, tuple(errors))

    assert settings.discord_bot_token is not None
    assert settings.discord_guild_id is not None
    bot: DiscordIdentity | None = None
    guild: DiscordGuild | None = None
    try:
        me = _discord_get(settings.discord_bot_token, "/users/@me")
        bot = DiscordIdentity(
            bot_id=str(me.get("id", "")),
            username=str(me.get("username", "unknown")),
            discriminator=str(me.get("discriminator")) if me.get("discriminator") is not None else None,
        )
    except urllib.error.HTTPError as exc:
        errors.append(f"Discord bot identity check failed with HTTP {exc.code}")
    except Exception as exc:  # pragma: no cover - network/environment dependent
        errors.append(f"Discord bot identity check failed: {exc.__class__.__name__}")

    try:
        guild_data = _discord_get(settings.discord_bot_token, f"/guilds/{settings.discord_guild_id}")
        guild = DiscordGuild(guild_id=str(guild_data.get("id", settings.discord_guild_id)), name=str(guild_data.get("name", "unknown guild")))
    except urllib.error.HTTPError as exc:
        errors.append(f"Discord guild check failed with HTTP {exc.code}")
    except Exception as exc:  # pragma: no cover - network/environment dependent
        errors.append(f"Discord guild check failed: {exc.__class__.__name__}")

    return DiscordValidation(True, bot, guild, tuple(errors))


def dry_run_discord_event(message: str, *, channel_id: str, author_id: str, audit_log: AuditLog, settings: Settings) -> int:
    """Route a simulated Discord event, log a redacted preview, and never post to Discord."""
    result = route_message(message, channel=f"discord:{channel_id}", audit_log=audit_log, disclosure=settings.synthetic_disclosure)
    event_id = audit_log.record(
        "discord_dry_run_intended_response",
        agent_slug=result.agent.slug,
        channel=f"discord:{channel_id}",
        synthetic_disclosure=settings.synthetic_disclosure,
        payload={
            "author_id": author_id,
            "message_preview": message[:160],
            "intended_response_preview": result.response[:500],
            "posted": False,
            "reason": "dry-run adapter never posts to Discord",
        },
    )
    return event_id


def assert_live_post_allowed(settings: Settings) -> None:
    if not settings.discord_live_post_enabled:
        raise PermissionError("Live Discord posting is disabled. Set OD_DISCORD_LIVE_POST_ENABLED=true and use an explicit live-post command.")
    if not settings.discord_configured:
        raise PermissionError("Live Discord posting requires DISCORD_BOT_TOKEN and DISCORD_GUILD_ID.")
