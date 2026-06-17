# OD backend — Phase 1 skeleton

This is the first backend skeleton after the Phase 0 constitutional bootstrap gate. It is deliberately conservative: no live Discord posting and no external LLM call happens by default.

## What is included

- Environment/config loader with Discord and LLM defaults.
- Synthetic-agent disclosure wrapper for outbound messages.
- Agent registry including Anna Medelvärde and her `soul.md` path.
- Simple deterministic router for dry-run messages.
- SQLite audit log for routed dry-run events.
- Discord credential/guild validation without printing secrets.
- Discord dry-run adapter that logs intended responses and never posts.
- One-channel Discord listener/polling dry-run for the allowlisted `talk-to-od-ai` channel.
- Background/once dry-run monitor with duplicate protection and `last_seen_message_id` state.
- Redacted-preview content triage that flags human-review categories without replying.
- Retention/minimization helpers that redact direct identifiers, pseudonymize author IDs, and avoid raw content storage by default.
- Explicit live-post gate requiring `OD_DISCORD_LIVE_POST_ENABLED=true` and credentials.
- Safety-report generator from the audit log.
- Unit tests for routing, disclosure, audit logging, Discord dry-run mode, minimization, allowlisting, and safety report output.

## Local commands

```bash
PYTHONPATH=backend python3 -m od_backend.cli doctor
PYTHONPATH=backend python3 -m od_backend.cli route "What is the cost-benefit risk?" --channel manual-test
PYTHONPATH=backend python3 -m od_backend.cli discord-doctor --skip-network
PYTHONPATH=backend python3 -m od_backend.cli discord-dry-run "What is the public sentiment risk?" --channel-id manual-channel --author-id manual-author
PYTHONPATH=backend python3 -m od_backend.cli discord-listen-dry-run --channel-id 1509855875102277652 --limit 5
PYTHONPATH=backend python3 -m od_backend.cli discord-monitor-dry-run --channel-id 1509855875102277652 --once --limit 10
PYTHONPATH=backend python3 -m od_backend.cli retention-sweep --days 30
PYTHONPATH=backend python3 -m od_backend.cli safety-report
PYTHONPATH=backend python3 -m unittest discover -s backend/tests
```

`discord-doctor` performs live Discord REST validation when credentials are configured and `--skip-network` is omitted. It reports bot and guild identity but never prints the token.

`discord-listen-dry-run` fetches recent messages from the single allowlisted channel (`OD_DISCORD_MONITOR_CHANNEL_ID`) and records only minimized audit events with `posted=false`.

`discord-monitor-dry-run` adds persistent duplicate protection via `OD_MONITOR_STATE`; use `--once` for one safe poll or omit it for a bounded/background dry-run loop.

Content triage currently flags these categories for human review only: `prompt_injection_attempt`, `requests_live_action`, `privacy_sensitive_content`, `legal_election_compliance`, `media_journalist_inquiry`, `abuse_or_harassment`, `possible_policy_question`, `high_value_public_question`, and generic `human_question`.

## Safety gates

- Live Discord validation requires `DISCORD_BOT_TOKEN` and `DISCORD_GUILD_ID` to be present.
- The only allowlisted monitored channel is `OD_DISCORD_MONITOR_CHANNEL_ID`; other channels are ignored.
- Discord author IDs are pseudonymized with `OD_RETENTION_HASH_SECRET` before audit storage.
- Message content is redacted/truncated before routing and audit storage; raw public Discord content is not stored by default.
- Duplicate monitor state stores message IDs only and is ignored as runtime data.
- Content triage runs on redacted previews only; it creates human-review flags but never generates public replies.
- Live Discord posting is disabled unless `OD_DISCORD_LIVE_POST_ENABLED=true`; even then, Phase 1.8 only checks the gate and does not implement posting.
- `OD_LLM_PROVIDER` defaults to `disabled`; external model calls are not implemented in this skeleton.
- Every dry-run response includes synthetic-agent disclosure.

## Governance design docs

- `docs/threat-model.md` — Phase 1 risks, assets, controls, and live-mode gates.
- `docs/inter-node-api.md` — future node/API envelope and non-goals; design only, no live service yet.
- `docs/governance-rules.md` — implementation rules for identity, mandate, data protection, Discord operation, and PR readiness.
