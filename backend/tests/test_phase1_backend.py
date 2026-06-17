from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from od_backend.audit_log import AuditLog
from od_backend.config import Settings
from od_backend.discord_adapter import (
    assert_live_post_allowed,
    check_discord_readiness,
    dry_run_discord_event,
    validate_discord_credentials,
)
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

    def test_discord_readiness_configured_is_still_live_post_gated(self) -> None:
        readiness = check_discord_readiness(Settings(discord_bot_token="secret-token", discord_guild_id="123"))
        self.assertTrue(readiness.configured)
        self.assertEqual(readiness.mode, "live-post-gated")
        self.assertNotIn("secret-token", readiness.reason)

    def test_validate_discord_credentials_missing_values_does_not_expose_token(self) -> None:
        validation = validate_discord_credentials(Settings(discord_bot_token="super-secret-token"))
        self.assertFalse(validation.ok)
        self.assertIn("DISCORD_GUILD_ID is missing", validation.errors)
        self.assertNotIn("super-secret-token", "\n".join(validation.errors))

    def test_validate_discord_credentials_success_uses_safe_identity(self) -> None:
        def fake_get(token: str, path: str, timeout: int = 15) -> dict[str, object]:
            self.assertEqual(token, "super-secret-token")
            if path == "/users/@me":
                return {"id": "42", "username": "ODBot", "discriminator": "0"}
            if path == "/guilds/123":
                return {"id": "123", "name": "Oberoende Digital"}
            raise AssertionError(path)

        settings = Settings(discord_bot_token="super-secret-token", discord_guild_id="123")
        with patch("od_backend.discord_adapter._discord_get", fake_get):
            validation = validate_discord_credentials(settings)
        self.assertTrue(validation.ok)
        self.assertIsNotNone(validation.bot)
        self.assertIsNotNone(validation.guild)
        assert validation.bot is not None
        assert validation.guild is not None
        self.assertEqual(validation.bot.safe_label, "ODBot (42)")
        self.assertEqual(validation.guild.name, "Oberoende Digital")

    def test_discord_dry_run_never_posts_and_creates_audit_events(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            audit = AuditLog(Path(tmp) / "audit.sqlite3")
            settings = Settings(synthetic_disclosure="Synthetic disclosure")
            event_id = dry_run_discord_event(
                "What is the public sentiment risk?",
                channel_id="channel-1",
                author_id="author-1",
                audit_log=audit,
                settings=settings,
            )
            self.assertEqual(event_id, 2)
            self.assertEqual(audit.count(), 2)
            event = audit.recent(1)[0]
            self.assertEqual(event["event_type"], "discord_dry_run_intended_response")
            self.assertFalse(event["payload"]["posted"])
            self.assertIn("Synthetic disclosure", event["payload"]["intended_response_preview"])

    def test_live_post_requires_explicit_flag_and_credentials(self) -> None:
        with self.assertRaises(PermissionError):
            assert_live_post_allowed(Settings(discord_bot_token="token", discord_guild_id="123"))
        with self.assertRaises(PermissionError):
            assert_live_post_allowed(Settings(discord_live_post_enabled=True))
        assert_live_post_allowed(Settings(discord_bot_token="token", discord_guild_id="123", discord_live_post_enabled=True))

    def test_safety_report_uses_audit_log(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            audit = AuditLog(Path(tmp) / "audit.sqlite3")
            route_message("integrity risk", channel="manual-test", audit_log=audit, disclosure="Synthetic disclosure")
            report = build_safety_report(audit)
            self.assertIn("Audit events recorded: 1", report)
            self.assertIn("dry_run_route", report)


if __name__ == "__main__":
    unittest.main()
