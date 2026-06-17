from __future__ import annotations

import argparse

from .audit_log import AuditLog
from .config import load_settings
from .discord_adapter import (
    assert_live_post_allowed,
    check_discord_readiness,
    dry_run_discord_event,
    validate_discord_credentials,
)
from .router import route_message
from .safety_report import build_safety_report


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
        print(f"discord_mode={readiness.mode}")
        print(f"discord_reason={readiness.reason}")
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
        )
        print(f"discord_dry_run_event_id={event_id}")
        print("posted=false")
        print("mode=dry-run")
        return 0

    if args.command == "discord-live-post":
        try:
            assert_live_post_allowed(settings)
        except PermissionError as exc:
            print(f"error={exc}")
            return 2
        print("Live-post gate passed, but posting is intentionally not implemented in Phase 1.5.")
        print(f"channel_id={args.channel_id}")
        return 0

    if args.command == "safety-report":
        print(build_safety_report(audit), end="")
        return 0

    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
