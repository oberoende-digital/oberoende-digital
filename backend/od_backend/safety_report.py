from __future__ import annotations

from .audit_log import AuditLog, utc_now


def build_safety_report(audit_log: AuditLog) -> str:
    recent = audit_log.recent(10)
    total = audit_log.count()
    lines = [
        "# OD backend safety report — dry run",
        "",
        f"Generated: {utc_now()}",
        f"Audit events recorded: {total}",
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
            "- This report is generated from audit-log data, not from unlogged side effects.",
        ]
    )
    return "\n".join(lines) + "\n"
