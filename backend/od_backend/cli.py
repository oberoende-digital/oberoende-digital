from __future__ import annotations

import argparse

from .audit_log import AuditLog
from .config import load_settings
from .discord_adapter import check_discord_readiness
from .router import route_message
from .safety_report import build_safety_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Oberoende Digital Phase 1 backend skeleton")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor", help="Check local backend readiness")

    route = sub.add_parser("route", help="Dry-run route a message through the agent registry")
    route.add_argument("message")
    route.add_argument("--channel", default="manual")

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

    if args.command == "safety-report":
        print(build_safety_report(audit), end="")
        return 0

    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
