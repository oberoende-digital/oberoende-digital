from __future__ import annotations

import argparse
import time
from datetime import datetime, timedelta, timezone

from .audit_log import AuditLog
from .config import load_settings
from .discord_adapter import (
    assert_live_post_allowed,
    check_discord_readiness,
    dry_run_discord_event,
    monitor_channel_once,
    scan_channel_dry_run,
    validate_discord_credentials,
)
from .discord_poller import DiscordPollState, poll_channel_dry_run
from .router import route_message
from .safety_report import build_safety_report


def _cutoff_iso(days: int) -> str:
    return (datetime.now(timezone.utc) - timedelta(days=days)).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Oberoende Digital Phase 1 backend skeleton")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor", help="Check local backend readiness")

    route = sub.add_parser("route", help="Dry-run route a message through the agent registry")
    route.add_argument("message")
    route.add_argument("--channel", default="manual")

    discord_doctor = sub.add_parser("discord-doctor", help="Validate Discord credentials and intended guild without printing secrets")
    discord_doctor.add_argument("--skip-network", action="store_true", help="Only report whether required env vars are present")

    discord_dry = sub.add_parser("discord-dry-run", help="Simulate a Discord message and log intended response without posting")
    discord_dry.add_argument("message")
    discord_dry.add_argument("--channel-id", default="manual-channel")
    discord_dry.add_argument("--author-id", default="manual-author")
    discord_dry.add_argument("--message-id", default="manual-message")

    listen = sub.add_parser("discord-listen-dry-run", help="Fetch recent messages from the allowlisted Discord channel and dry-run route them")
    listen.add_argument("--channel-id", required=True)
    listen.add_argument("--limit", type=int, default=10)

    monitor = sub.add_parser("discord-monitor-dry-run", help="Poll the allowlisted Discord channel with duplicate protection; posts nothing")
    monitor.add_argument("--channel-id", required=True)
    monitor.add_argument("--limit", type=int, default=10)
    monitor.add_argument("--once", action="store_true", help="Run a single poll and exit")
    monitor.add_argument("--interval", type=int, default=90, help="Seconds between polls when not using --once")
    monitor.add_argument("--max-iterations", type=int, default=0, help="Optional bounded loop count; 0 means run until interrupted")

    poll_once = sub.add_parser("discord-poll-once", help="Run one stateful dry-run poll tick for the allowlisted Discord channel")
    poll_once.add_argument("--channel-id", required=True)
    poll_once.add_argument("--limit", type=int, default=10)
    poll_once.add_argument("--max-handle", type=int, default=None)
    poll_once.add_argument("--process-existing", action="store_true", help="Process existing fetched messages instead of bootstrapping the cursor")

    sweep = sub.add_parser("retention-sweep", help="Count or delete audit events older than a retention window")
    sweep.add_argument("--days", type=int, default=30)
    sweep.add_argument("--apply", action="store_true", help="Actually delete matching old audit events")

    live_post = sub.add_parser("discord-live-post", help="Gate check for future live Discord posting; currently posts nothing")
    live_post.add_argument("--channel-id", required=True)
    live_post.add_argument("message")

    sub.add_parser("safety-report", help="Print a dry-run safety report from the audit log")

    args = parser.parse_args(argv)
    settings = load_settings()
    audit = AuditLog(settings.database_path)

    if args.command == "doctor":
        readiness = check_discord_readiness(settings)
        print(f"environment={settings.environment}")
        print(f"database_path={settings.database_path}")
        print(f"monitor_state_path={settings.monitor_state_path}")
        print(f"discord_mode={readiness.mode}")
        print(f"discord_reason={readiness.reason}")
        print(f"discord_monitor_channel_id={settings.discord_monitor_channel_id or ''}")
        print(f"discord_poll_max_per_tick={settings.discord_poll_max_per_tick}")
        print(f"llm_provider={settings.llm_provider}")
        return 0

    if args.command == "route":
        result = route_message(args.message, channel=args.channel, audit_log=audit, disclosure=settings.synthetic_disclosure)
        print(f"agent={result.agent.slug}")
        print(f"audit_event_id={result.audit_event_id}")
        print(result.response)
        return 0

    if args.command == "discord-doctor":
        readiness = check_discord_readiness(settings)
        print(f"discord_mode={readiness.mode}")
        print(f"discord_configured={str(settings.discord_configured).lower()}")
        print(f"monitor_channel_configured={str(bool(settings.discord_monitor_channel_id)).lower()}")
        print(f"live_post_enabled={str(settings.discord_live_post_enabled).lower()}")
        if args.skip_network:
            print("network_validation=skipped")
            return 0 if settings.discord_configured else 2
        validation = validate_discord_credentials(settings)
        if validation.bot:
            print(f"bot={validation.bot.safe_label}")
        if validation.guild:
            print(f"guild={validation.guild.name} ({validation.guild.guild_id})")
        for error in validation.errors:
            print(f"error={error}")
        return 0 if validation.ok else 2

    if args.command == "discord-dry-run":
        event_id = dry_run_discord_event(
            args.message,
            channel_id=args.channel_id,
            author_id=args.author_id,
            audit_log=audit,
            settings=settings,
            message_id=args.message_id,
        )
        print(f"discord_dry_run_event_id={event_id}")
        print("posted=false")
        print("mode=dry-run")
        return 0

    if args.command == "discord-listen-dry-run":
        results = scan_channel_dry_run(channel_id=args.channel_id, limit=args.limit, audit_log=audit, settings=settings)
        handled = sum(1 for item in results if item.handled)
        ignored = len(results) - handled
        print(f"channel_id={args.channel_id}")
        print(f"handled={handled}")
        print(f"ignored={ignored}")
        for item in results:
            print(f"result={item.reason} audit_event_id={item.audit_event_id or ''} agent={item.agent_slug or ''}")
        return 0 if handled or results else 2

    if args.command == "discord-monitor-dry-run":
        if args.interval < 30:
            print("error=--interval must be >= 30 seconds")
            return 2
        iterations = 1 if args.once else args.max_iterations
        count = 0
        while True:
            result = monitor_channel_once(channel_id=args.channel_id, limit=args.limit, audit_log=audit, settings=settings)
            print(f"channel_id={result.channel_id}")
            print(f"fetched={result.fetched}")
            print(f"handled={result.handled}")
            print(f"ignored={result.ignored}")
            print(f"duplicate_skipped={result.duplicate_skipped}")
            print(f"last_seen_message_id={result.last_seen_message_id or ''}")
            print(f"monitor_summary_event_id={result.summary_event_id}")
            for item in result.results:
                print(f"result={item.reason} message_id={item.message_id or ''} audit_event_id={item.audit_event_id or ''} agent={item.agent_slug or ''}")
            count += 1
            if args.once or (iterations and count >= iterations):
                return 0
            time.sleep(args.interval)

    if args.command == "discord-poll-once":
        poll_state = DiscordPollState(settings.database_path)
        tick = poll_channel_dry_run(
            channel_id=args.channel_id,
            limit=args.limit,
            max_handle_per_tick=args.max_handle or settings.discord_poll_max_per_tick,
            audit_log=audit,
            poll_state=poll_state,
            settings=settings,
            process_existing=args.process_existing,
        )
        print(f"channel_id={tick.channel_id}")
        print(f"reason={tick.reason}")
        print(f"fetched={tick.fetched}")
        print(f"handled={tick.handled}")
        print(f"ignored={tick.ignored}")
        print(f"state_updated={str(tick.state_updated).lower()}")
        print(f"last_seen_message_id={tick.last_seen_message_id or ''}")
        print(f"audit_event_id={tick.audit_event_id or ''}")
        for item in tick.results:
            print(f"result={item.reason} audit_event_id={item.audit_event_id or ''} agent={item.agent_slug or ''}")
        return 0 if tick.audit_event_id is not None or tick.reason in {"channel_not_allowlisted", "discord_validation_failed"} else 2

    if args.command == "retention-sweep":
        if args.days < 1:
            print("error=--days must be >= 1")
            return 2
        cutoff = _cutoff_iso(args.days)
        count = audit.count_older_than(cutoff)
        if args.apply:
            deleted = audit.delete_older_than(cutoff)
            print(f"deleted={deleted}")
        else:
            print(f"would_delete={count}")
        print(f"cutoff={cutoff}")
        return 0

    if args.command == "discord-live-post":
        try:
            assert_live_post_allowed(settings)
        except PermissionError as exc:
            print(f"error={exc}")
            return 2
        print("Live-post gate passed, but posting is intentionally not implemented in Phase 1.7.")
        print(f"channel_id={args.channel_id}")
        return 0

    if args.command == "safety-report":
        print(build_safety_report(audit), end="")
        return 0

    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
