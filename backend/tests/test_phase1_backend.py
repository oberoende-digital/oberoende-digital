from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from od_backend.audit_log import AuditLog
from od_backend.config import Settings
from od_backend.discord_adapter import check_discord_readiness
from od_backend.disclosure import with_synthetic_disclosure
from od_backend.router import choose_agent, route_message
from od_backend.safety_report import build_safety_report


class Phase1BackendTests(unittest.TestCase):
    def test_disclosure_is_added_once(self) -> None:
        msg = with_synthetic_disclosure("Hello", "AI generated")
        self.assertTrue(msg.endswith("— AI generated"))
        self.assertEqual(with_synthetic_disclosure(msg, "AI generated"), msg)

    def test_policy_cost_message_routes_to_anna(self) -> None:
        agent = choose_agent("What is the cost benefit and public sentiment risk?")
        self.assertEqual(agent.slug, "anna-medelvarde")

    def test_route_records_audit_event(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            audit = AuditLog(Path(tmp) / "audit.sqlite3")
            result = route_message("budget policy", channel="manual-test", audit_log=audit, disclosure="Synthetic disclosure")
            self.assertEqual(result.agent.slug, "anna-medelvarde")
            self.assertEqual(result.audit_event_id, 1)
            self.assertEqual(audit.count(), 1)
            event = audit.recent(1)[0]
            self.assertEqual(event["synthetic_disclosure"], "Synthetic disclosure")
            self.assertIn("Synthetic disclosure", event["payload"]["response"])

    def test_discord_readiness_defaults_to_dry_run(self) -> None:
        readiness = check_discord_readiness(Settings())
        self.assertFalse(readiness.configured)
        self.assertEqual(readiness.mode, "dry-run")

    def test_safety_report_uses_audit_log(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            audit = AuditLog(Path(tmp) / "audit.sqlite3")
            route_message("integrity risk", channel="manual-test", audit_log=audit, disclosure="Synthetic disclosure")
            report = build_safety_report(audit)
            self.assertIn("Audit events recorded: 1", report)
            self.assertIn("dry_run_route", report)


if __name__ == "__main__":
    unittest.main()
