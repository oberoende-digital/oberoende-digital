from __future__ import annotations

from dataclasses import dataclass
import json
import urllib.error
import urllib.parse
import urllib.request

from .audit_log import AuditLog
from .config import Settings
from .content_triage import triage_redacted_preview
from .monitor_state import MonitorState, load_monitor_state, max_message_id, save_monitor_state
from .retention import MinimizedDiscordMessage, minimize_discord_message
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


@dataclass(frozen=True)
class DiscordDryRunResult:
    handled: bool
    reason: str
    audit_event_id: int | None = None
    route_event_id: int | None = None
    agent_slug: str | None = None
    message_id: str | None = None


@dataclass(frozen=True)
class MonitorRunResult:
    channel_id: str
    fetched: int
    handled: int
    ignored: int
    duplicate_skipped: int
    last_seen_message_id: str | None
    summary_event_id: int
    results: tuple[DiscordDryRunResult, ...]


def check_discord_readiness(settings: Settings) -> DiscordReadiness:
    if settings.discord_configured:
        mode = "live-post-gated" if not settings.discord_live_post_enabled else "live-post-enabled"
        return DiscordReadiness(
            True,
            mode,
            "DISCORD_BOT_TOKEN and DISCORD_GUILD_ID are present; live posting still requires the explicit live-post command.",
        )
    return DiscordReadiness(False, "dry-run", "Discord credentials are absent; backend remains in dry-run/manual-test mode.")


def _discord_get(token: str, path: str, timeout: int = 15) -> dict[str, object] | list[dict[str, object]]:
    req = urllib.request.Request(
        f"{DISCORD_API_BASE}{path}",
        headers={"Authorization": f"Bot {token}", "User-Agent": "od-backend-phase1.6"},
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
        assert isinstance(me, dict)
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
        assert isinstance(guild_data, dict)
        guild = DiscordGuild(guild_id=str(guild_data.get("id", settings.discord_guild_id)), name=str(guild_data.get("name", "unknown guild")))
    except urllib.error.HTTPError as exc:
        errors.append(f"Discord guild check failed with HTTP {exc.code}")
    except Exception as exc:  # pragma: no cover - network/environment dependent
        errors.append(f"Discord guild check failed: {exc.__class__.__name__}")

    return DiscordValidation(True, bot, guild, tuple(errors))


def is_channel_allowlisted(settings: Settings, channel_id: str) -> bool:
    return bool(settings.discord_monitor_channel_id and channel_id == settings.discord_monitor_channel_id)


def _minimize_from_raw(message: str, *, channel_id: str, author_id: str, message_id: str | None, created_at: str | None, settings: Settings) -> MinimizedDiscordMessage:
    return minimize_discord_message(
        message_id=message_id or "manual-message",
        channel_id=channel_id,
        author_id=author_id,
        content=message,
        created_at=created_at,
        secret=settings.retention_hash_secret,
    )


def dry_run_discord_event(
    message: str,
    *,
    channel_id: str,
    author_id: str,
    audit_log: AuditLog,
    settings: Settings,
    message_id: str | None = None,
    created_at: str | None = None,
) -> int:
    """Route a simulated Discord event, log a minimized preview, and never post to Discord."""
    minimized = _minimize_from_raw(
        message,
        channel_id=channel_id,
        author_id=author_id,
        message_id=message_id,
        created_at=created_at,
        settings=settings,
    )
    result = route_message(minimized.redacted_preview, channel=f"discord:{channel_id}", audit_log=audit_log, disclosure=settings.synthetic_disclosure)
    triage = triage_redacted_preview(minimized.redacted_preview)
    event_id = audit_log.record(
        "discord_dry_run_intended_response",
        agent_slug=result.agent.slug,
        channel=f"discord:{channel_id}",
        synthetic_disclosure=settings.synthetic_disclosure,
        payload={
            "message_id": minimized.message_id,
            "channel_id": minimized.channel_id,
            "author_hash": minimized.author_hash,
            "created_at": minimized.created_at,
            "message_preview": minimized.redacted_preview,
            "route_event_id": result.audit_event_id,
            "intended_response_preview": result.response[:500],
            "triage_categories": list(triage.categories),
            "triage_priority": triage.priority,
            "human_review_needed": triage.human_review_needed,
            "triage_reasons": list(triage.reasons),
            "posted": False,
            "reason": "dry-run adapter never posts to Discord",
        },
    )
    return event_id


def handle_discord_message_dry_run(message: dict[str, object], *, audit_log: AuditLog, settings: Settings, bot_user_id: str | None = None) -> DiscordDryRunResult:
    channel_id = str(message.get("channel_id", ""))
    if not is_channel_allowlisted(settings, channel_id):
        return DiscordDryRunResult(False, "channel_not_allowlisted", message_id=str(message.get("id", "")) or None)
    author = message.get("author")
    author_id = str(author.get("id", "")) if isinstance(author, dict) else ""
    is_bot = bool(author.get("bot")) if isinstance(author, dict) else False
    if is_bot or (bot_user_id and author_id == bot_user_id):
        return DiscordDryRunResult(False, "bot_or_self_message", message_id=str(message.get("id", "")) or None)
    content = str(message.get("content", ""))
    event_id = dry_run_discord_event(
        content,
        channel_id=channel_id,
        author_id=author_id or "unknown-author",
        audit_log=audit_log,
        settings=settings,
        message_id=str(message.get("id", "")) or None,
        created_at=str(message.get("timestamp", "")) or None,
    )
    recent = audit_log.recent(1)[0]
    return DiscordDryRunResult(
        True,
        "handled",
        audit_event_id=event_id,
        route_event_id=recent["payload"].get("route_event_id"),
        agent_slug=recent["agent_slug"],
        message_id=str(message.get("id", "")) or None,
    )


def fetch_recent_channel_messages(settings: Settings, *, channel_id: str, limit: int = 10) -> list[dict[str, object]]:
    if not settings.discord_bot_token:
        raise PermissionError("DISCORD_BOT_TOKEN is required to fetch Discord channel messages.")
    limit = min(max(limit, 1), 25)
    path = f"/channels/{urllib.parse.quote(channel_id)}/messages?limit={limit}"
    data = _discord_get(settings.discord_bot_token, path)
    if not isinstance(data, list):
        raise RuntimeError("Discord messages endpoint returned a non-list payload")
    return data


def scan_channel_dry_run(*, channel_id: str, limit: int, audit_log: AuditLog, settings: Settings) -> list[DiscordDryRunResult]:
    if not is_channel_allowlisted(settings, channel_id):
        return [DiscordDryRunResult(False, "channel_not_allowlisted")]
    validation = validate_discord_credentials(settings)
    if not validation.ok or validation.bot is None:
        return [DiscordDryRunResult(False, "discord_validation_failed")]
    messages = fetch_recent_channel_messages(settings, channel_id=channel_id, limit=limit)
    results = [handle_discord_message_dry_run(message, audit_log=audit_log, settings=settings, bot_user_id=validation.bot.bot_id) for message in reversed(messages)]
    return results


def monitor_channel_once(*, channel_id: str, limit: int, audit_log: AuditLog, settings: Settings) -> MonitorRunResult:
    """Poll the allowlisted Discord channel once, skipping messages already seen in local state."""
    if not is_channel_allowlisted(settings, channel_id):
        event_id = audit_log.record(
            "discord_monitor_run",
            agent_slug=None,
            channel=f"discord:{channel_id}",
            synthetic_disclosure=settings.synthetic_disclosure,
            payload={"fetched": 0, "handled": 0, "ignored": 0, "duplicate_skipped": 0, "reason": "channel_not_allowlisted", "posted": False},
        )
        return MonitorRunResult(channel_id, 0, 0, 0, 0, None, event_id, tuple())

    validation = validate_discord_credentials(settings)
    if not validation.ok or validation.bot is None:
        event_id = audit_log.record(
            "discord_monitor_run",
            agent_slug=None,
            channel=f"discord:{channel_id}",
            synthetic_disclosure=settings.synthetic_disclosure,
            payload={"fetched": 0, "handled": 0, "ignored": 0, "duplicate_skipped": 0, "reason": "discord_validation_failed", "posted": False},
        )
        return MonitorRunResult(channel_id, 0, 0, 0, 0, None, event_id, tuple())

    state = load_monitor_state(settings.monitor_state_path)
    messages = fetch_recent_channel_messages(settings, channel_id=channel_id, limit=limit)
    messages_oldest_first = list(reversed(messages))
    results: list[DiscordDryRunResult] = []
    duplicate_skipped = 0
    observed_ids: list[str] = []
    seen = set(state.seen_message_ids)

    for message in messages_oldest_first:
        message_id = str(message.get("id", ""))
        if message_id:
            observed_ids.append(message_id)
        if message_id and message_id in seen:
            duplicate_skipped += 1
            results.append(DiscordDryRunResult(False, "duplicate_skipped", message_id=message_id))
            continue
        result = handle_discord_message_dry_run(message, audit_log=audit_log, settings=settings, bot_user_id=validation.bot.bot_id)
        results.append(result)
        if message_id:
            seen.add(message_id)

    last_seen = max_message_id(observed_ids) or state.last_seen_message_id
    save_monitor_state(settings.monitor_state_path, MonitorState(last_seen, frozenset(seen)))
    handled = sum(1 for item in results if item.handled)
    ignored = sum(1 for item in results if not item.handled and item.reason != "duplicate_skipped")
    event_id = audit_log.record(
        "discord_monitor_run",
        agent_slug=None,
        channel=f"discord:{channel_id}",
        synthetic_disclosure=settings.synthetic_disclosure,
        payload={
            "fetched": len(messages),
            "handled": handled,
            "ignored": ignored,
            "duplicate_skipped": duplicate_skipped,
            "last_seen_message_id": last_seen,
            "posted": False,
            "reason": "once_poll_complete",
        },
    )
    return MonitorRunResult(channel_id, len(messages), handled, ignored, duplicate_skipped, last_seen, event_id, tuple(results))


def assert_live_post_allowed(settings: Settings) -> None:
    if not settings.discord_live_post_enabled:
        raise PermissionError("Live Discord posting is disabled. Set OD_DISCORD_LIVE_POST_ENABLED=true and use an explicit live-post command.")
    if not settings.discord_configured:
        raise PermissionError("Live Discord posting requires DISCORD_BOT_TOKEN and DISCORD_GUILD_ID.")
