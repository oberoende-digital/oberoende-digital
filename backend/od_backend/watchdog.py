from __future__ import annotations

from dataclasses import dataclass

from .audit_log import AuditLog, utc_now


@dataclass(frozen=True)
class WatchdogFinding:
    severity: str
    code: str
    detail: str


def _as_int(value: object, default: int = 0) -> int:
    try:
        return int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return default


def _event_label(event: dict[str, object]) -> str:
    return f"event_id={event['id']}"


def evaluate_watchdog(audit_log: AuditLog, *, recent_limit: int = 100) -> list[WatchdogFinding]:
    """Evaluate dry-run Discord monitor health without exposing message content.

    The watchdog intentionally reports only event ids, counters, categories, and
    message ids. It must not echo raw Discord content, redacted previews, author
    ids, or intended response text because cron summaries may be delivered to
    external channels.
    """
    findings: list[WatchdogFinding] = []
    monitor_events = audit_log.events_by_type("discord_monitor_run", limit=recent_limit)
    if not monitor_events:
        return [WatchdogFinding("critical", "no_monitor_runs", "No discord_monitor_run audit events are present.")]

    latest = monitor_events[0]
    latest_payload = latest["payload"]
    latest_reason = str(latest_payload.get("reason", ""))
    if latest_payload.get("posted") is not False:
        findings.append(WatchdogFinding("critical", "posted_not_false", f"{_event_label(latest)} does not explicitly record posted=false."))
    if latest_reason and latest_reason != "once_poll_complete":
        findings.append(WatchdogFinding("critical", "monitor_not_complete", f"{_event_label(latest)} reason={latest_reason}."))

    fetched = _as_int(latest_payload.get("fetched"))
    handled = _as_int(latest_payload.get("handled"))
    ignored = _as_int(latest_payload.get("ignored"))
    duplicate_skipped = _as_int(latest_payload.get("duplicate_skipped"))
    if fetched != handled + ignored + duplicate_skipped:
        findings.append(
            WatchdogFinding(
                "critical",
                "counter_mismatch",
                f"{_event_label(latest)} fetched={fetched} handled={handled} ignored={ignored} duplicate_skipped={duplicate_skipped}.",
            )
        )

    cursor_values = [str(event["payload"].get("last_seen_message_id")) for event in monitor_events if event["payload"].get("last_seen_message_id")]
    if cursor_values and latest_payload.get("last_seen_message_id"):
        highest = max(cursor_values, key=int)
        latest_cursor = str(latest_payload.get("last_seen_message_id"))
        if int(latest_cursor) < int(highest):
            findings.append(WatchdogFinding("warning", "cursor_regression_in_latest_event", f"{_event_label(latest)} cursor={latest_cursor} below recent_high_water={highest}."))

    triage_events = audit_log.events_by_type("discord_dry_run_intended_response", limit=recent_limit)
    for event in triage_events:
        payload = event["payload"]
        priority = str(payload.get("triage_priority", "none"))
        review_needed = bool(payload.get("human_review_needed"))
        if priority == "high" and review_needed:
            categories = ",".join(str(item) for item in (payload.get("triage_categories") or [])) or "none"
            message_id = str(payload.get("message_id", "unknown"))
            findings.append(
                WatchdogFinding(
                    "warning",
                    "high_priority_triage_pending",
                    f"{_event_label(event)} message_id={message_id} categories={categories} needs human review; content intentionally omitted.",
                )
            )
    return findings


def build_watchdog_report(audit_log: AuditLog, *, recent_limit: int = 100) -> str:
    monitor_events = audit_log.events_by_type("discord_monitor_run", limit=recent_limit)
    latest = monitor_events[0] if monitor_events else None
    findings = evaluate_watchdog(audit_log, recent_limit=recent_limit)
    critical = sum(1 for finding in findings if finding.severity == "critical")
    warnings = sum(1 for finding in findings if finding.severity == "warning")
    lines = [
        "# OD Discord dry-run watchdog check",
        "",
        f"Generated: {utc_now()}",
        f"Status: {'critical' if critical else 'ok'}",
        f"Critical findings: {critical}",
        f"Warnings: {warnings}",
        "",
        "## Latest monitor run",
    ]
    if latest is None:
        lines.append("- n/a")
    else:
        payload = latest["payload"]
        lines.extend(
            [
                f"- event_id: {latest['id']}",
                f"- channel: {latest['channel']}",
                f"- fetched: {_as_int(payload.get('fetched'))}",
                f"- handled: {_as_int(payload.get('handled'))}",
                f"- ignored: {_as_int(payload.get('ignored'))}",
                f"- duplicate_skipped: {_as_int(payload.get('duplicate_skipped'))}",
                f"- last_seen_message_id: {payload.get('last_seen_message_id') or 'n/a'}",
                f"- posted: {payload.get('posted')}",
                f"- reason: {payload.get('reason') or 'n/a'}",
            ]
        )
    lines.extend(["", "## Findings"])
    if not findings:
        lines.append("- none")
    for finding in findings:
        lines.append(f"- {finding.severity} {finding.code}: {finding.detail}")
    lines.extend(
        [
            "",
            "## Privacy guardrail",
            "- Report intentionally omits Discord message content, redacted previews, raw author IDs, and intended response text.",
        ]
    )
    return "\n".join(lines) + "\n"
