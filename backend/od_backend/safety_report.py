from __future__ import annotations

from .audit_log import AuditLog, utc_now


def _monitor_summary(audit_log: AuditLog) -> list[str]:
    monitor_events = audit_log.events_by_type("discord_monitor_run", limit=1000)
    if not monitor_events:
        return ["- No monitor runs recorded."]
    handled = sum(int(event["payload"].get("handled", 0)) for event in monitor_events)
    ignored = sum(int(event["payload"].get("ignored", 0)) for event in monitor_events)
    duplicate_skipped = sum(int(event["payload"].get("duplicate_skipped", 0)) for event in monitor_events)
    fetched = sum(int(event["payload"].get("fetched", 0)) for event in monitor_events)
    latest = monitor_events[0]
    latest_payload = latest["payload"]
    return [
        f"- Monitor runs: {len(monitor_events)}",
        f"- Messages fetched: {fetched}",
        f"- Messages handled: {handled}",
        f"- Messages ignored: {ignored}",
        f"- Duplicate messages skipped: {duplicate_skipped}",
        f"- Last seen message ID: {latest_payload.get('last_seen_message_id') or 'n/a'}",
    ]


def build_safety_report(audit_log: AuditLog) -> str:
    recent = audit_log.recent(10)
    total = audit_log.count()
    lines = [
        "# OD backend safety report — dry run",
        "",
        f"Generated: {utc_now()}",
        f"Audit events recorded: {total}",
        "",
        "## Monitor summary",
        *_monitor_summary(audit_log),
        "",
        "## Recent events",
    ]
    if not recent:
        lines.append("- No events recorded.")
    for event in recent:
        lines.append(
            f"- #{event['id']} {event['created_at']} {event['event_type']} "
            f"agent={event['agent_slug']} channel={event['channel']}"
        )
    lines.extend(
        [
            "",
            "## Gates",
            "- Live Discord posting remains disabled unless credentials are explicitly configured and an operator starts the adapter.",
            "- Every dry-run response includes synthetic-agent disclosure text.",
            "- Monitor mode stores duplicate-protection state but still posts nothing.",
            "- This report is generated from audit-log data, not from unlogged side effects.",
        ]
    )
    return "\n".join(lines) + "\n"
