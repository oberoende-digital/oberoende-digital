from __future__ import annotations

from dataclasses import dataclass
import sqlite3
from pathlib import Path

from .audit_log import AuditLog, utc_now
from .config import Settings
from .discord_adapter import DiscordDryRunResult, fetch_recent_channel_messages, handle_discord_message_dry_run, is_channel_allowlisted, validate_discord_credentials

POLL_STATE_SCHEMA = """
CREATE TABLE IF NOT EXISTS discord_poll_state (
    channel_id TEXT PRIMARY KEY,
    last_seen_message_id TEXT NOT NULL,
    last_checked_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
"""


@dataclass(frozen=True)
class DiscordPollTick:
    channel_id: str
    handled: int
    ignored: int
    fetched: int
    state_updated: bool
    reason: str
    last_seen_message_id: str | None
    audit_event_id: int | None
    results: tuple[DiscordDryRunResult, ...]


class DiscordPollState:
    """Persist minimal per-channel poll cursor without storing raw Discord content."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as con:
            con.execute(POLL_STATE_SCHEMA)

    def get_last_seen(self, channel_id: str) -> str | None:
        with sqlite3.connect(self.path) as con:
            row = con.execute("SELECT last_seen_message_id FROM discord_poll_state WHERE channel_id = ?", (channel_id,)).fetchone()
        return str(row[0]) if row else None

    def upsert_last_seen(self, channel_id: str, message_id: str, *, checked_at: str | None = None) -> None:
        now = utc_now()
        checked_at = checked_at or now
        with sqlite3.connect(self.path) as con:
            con.execute(
                """
                INSERT INTO discord_poll_state(channel_id,last_seen_message_id,last_checked_at,updated_at)
                VALUES(?,?,?,?)
                ON CONFLICT(channel_id) DO UPDATE SET
                    last_seen_message_id=excluded.last_seen_message_id,
                    last_checked_at=excluded.last_checked_at,
                    updated_at=excluded.updated_at
                """,
                (channel_id, message_id, checked_at, now),
            )


def _message_id(message: dict[str, object]) -> str:
    return str(message.get("id", ""))


def _is_newer(message_id: str, last_seen_message_id: str | None) -> bool:
    if not message_id:
        return False
    if not last_seen_message_id:
        return True
    try:
        return int(message_id) > int(last_seen_message_id)
    except ValueError:
        return message_id > last_seen_message_id


def _sortable_message_id(message_id: str) -> tuple[int, int | str]:
    if message_id.isdigit():
        return (1, int(message_id))
    return (0, message_id)


def poll_channel_dry_run(
    *,
    channel_id: str,
    limit: int,
    max_handle_per_tick: int,
    audit_log: AuditLog,
    poll_state: DiscordPollState,
    settings: Settings,
    process_existing: bool = False,
) -> DiscordPollTick:
    """Fetch one allowlisted Discord channel and dry-run only new human messages.

    The first run bootstraps the cursor to the latest fetched message unless
    ``process_existing`` is explicit. This prevents a newly started worker from
    back-processing old community history without a human/operator decision.
    """

    if max_handle_per_tick < 1:
        raise ValueError("max_handle_per_tick must be >= 1")
    if not is_channel_allowlisted(settings, channel_id):
        return DiscordPollTick(channel_id, 0, 1, 0, False, "channel_not_allowlisted", None, None, tuple())

    validation = validate_discord_credentials(settings)
    if not validation.ok or validation.bot is None:
        return DiscordPollTick(channel_id, 0, 1, 0, False, "discord_validation_failed", poll_state.get_last_seen(channel_id), None, tuple())

    messages = fetch_recent_channel_messages(settings, channel_id=channel_id, limit=limit)
    fetched = len(messages)
    message_ids = [_message_id(message) for message in messages if _message_id(message)]
    newest_seen = max(message_ids, key=_sortable_message_id, default=None)
    previous_seen = poll_state.get_last_seen(channel_id)

    if previous_seen is None and newest_seen and not process_existing:
        poll_state.upsert_last_seen(channel_id, newest_seen)
        event_id = audit_log.record(
            "discord_poll_tick",
            agent_slug=None,
            channel=f"discord:{channel_id}",
            synthetic_disclosure=settings.synthetic_disclosure,
            payload={
                "channel_id": channel_id,
                "fetched": fetched,
                "handled": 0,
                "ignored": fetched,
                "posted": False,
                "reason": "bootstrap_latest_without_processing_existing_messages",
                "last_seen_message_id": newest_seen,
            },
        )
        return DiscordPollTick(channel_id, 0, fetched, fetched, True, "bootstrapped_latest", newest_seen, event_id, tuple())

    new_messages = [message for message in reversed(messages) if _is_newer(_message_id(message), previous_seen)]
    to_handle = new_messages[:max_handle_per_tick]
    results = tuple(
        handle_discord_message_dry_run(message, audit_log=audit_log, settings=settings, bot_user_id=validation.bot.bot_id)
        for message in to_handle
    )
    handled = sum(1 for item in results if item.handled)
    ignored = len(results) - handled + max(0, len(new_messages) - len(to_handle))
    if newest_seen:
        poll_state.upsert_last_seen(channel_id, newest_seen)
    event_id = audit_log.record(
        "discord_poll_tick",
        agent_slug=None,
        channel=f"discord:{channel_id}",
        synthetic_disclosure=settings.synthetic_disclosure,
        payload={
            "channel_id": channel_id,
            "fetched": fetched,
            "new_messages": len(new_messages),
            "handled": handled,
            "ignored": ignored,
            "max_handle_per_tick": max_handle_per_tick,
            "posted": False,
            "reason": "dry_run_poll_tick",
            "last_seen_message_id": newest_seen or previous_seen,
        },
    )
    return DiscordPollTick(channel_id, handled, ignored, fetched, bool(newest_seen), "polled", newest_seen or previous_seen, event_id, results)
