from __future__ import annotations

from collections import Counter

from .audit_log import AuditLog, utc_now


def _monitor_summary(audit_log: AuditLog) -> list[str]:
    monitor_events = audit_log.events_by_type("discord_monitor_run", limit=1000)
    if not monitor_events:
        return ["- No monitor runs recorded."]
    handled = sum(int(event["payload"].get("handled", 0)) for event in monitor_events)
    ignored = sum(int(event["payload"].get("ignored", 0)) for event in monitor_events)
    duplicate_skipped = sum(int(event["payload"].get("duplicate_skipped", 0)) for event in monitor_events)
    fetched = sum(int(event["payload"].get("fetched", 0)) for event in monitor_events)
    last_seen_message_ids = [
        str(event["payload"].get("last_seen_message_id"))
        for event in monitor_events
        if event["payload"].get("last_seen_message_id")
    ]
    last_seen_message_id = max(last_seen_message_ids, key=int) if last_seen_message_ids else None
    return [
        f"- Monitor runs: {len(monitor_events)}",
        f"- Messages fetched: {fetched}",
        f"- Messages handled: {handled}",
        f"- Messages ignored: {ignored}",
        f"- Duplicate messages skipped: {duplicate_skipped}",
        f"- Last seen message ID: {last_seen_message_id or 'n/a'}",
    ]


def _triage_summary(audit_log: AuditLog) -> list[str]:
    events = audit_log.events_by_type("discord_dry_run_intended_response", limit=1000)
    if not events:
        return ["- No triaged messages recorded."]
    category_counts: Counter[str] = Counter()
    priority_counts: Counter[str] = Counter()
    review_needed = 0
    for event in events:
        payload = event["payload"]
        priority_counts[str(payload.get("triage_priority", "none"))] += 1
        if payload.get("human_review_needed"):
            review_needed += 1
        for category in payload.get("triage_categories", []) or []:
            category_counts[str(category)] += 1
    category_text = ", ".join(f"{name}={count}" for name, count in sorted(category_counts.items())) or "none"
    priority_text = ", ".join(f"{name}={count}" for name, count in sorted(priority_counts.items())) or "none"
    return [
        f"- Triaged messages: {len(events)}",
        f"- Human review needed: {review_needed}",
        f"- Priorities: {priority_text}",
        f"- Categories: {category_text}",
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
        "## Content triage summary",
        *_triage_summary(audit_log),
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
            "- Content triage runs on redacted previews only and creates human-review flags, not replies.",
            "- This report is generated from audit-log data, not from unlogged side effects.",
        ]
    )
    return "\n".join(lines) + "\n"
