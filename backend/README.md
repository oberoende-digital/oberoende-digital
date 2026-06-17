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
- Explicit live-post gate requiring `OD_DISCORD_LIVE_POST_ENABLED=true` and credentials.
- Safety-report generator from the audit log.
- Unit tests for routing, disclosure, audit logging, Discord dry-run mode, and safety report output.

## Local commands

```bash
PYTHONPATH=backend python3 -m od_backend.cli doctor
PYTHONPATH=backend python3 -m od_backend.cli route "What is the cost-benefit risk?" --channel manual-test
PYTHONPATH=backend python3 -m od_backend.cli discord-doctor --skip-network
PYTHONPATH=backend python3 -m od_backend.cli discord-dry-run "What is the public sentiment risk?" --channel-id manual-channel --author-id manual-author
PYTHONPATH=backend python3 -m od_backend.cli safety-report
PYTHONPATH=backend python3 -m unittest discover -s backend/tests
```

`discord-doctor` performs live Discord REST validation when credentials are configured and `--skip-network` is omitted. It reports bot and guild identity but never prints the token.

## Safety gates

- Live Discord validation requires `DISCORD_BOT_TOKEN` and `DISCORD_GUILD_ID` to be present.
- Live Discord posting is disabled unless `OD_DISCORD_LIVE_POST_ENABLED=true`; even then, Phase 1.5 only checks the gate and does not implement posting.
- `OD_LLM_PROVIDER` defaults to `disabled`; external model calls are not implemented in this skeleton.
- Every dry-run response includes synthetic-agent disclosure.
- Raw public message storage is limited to explicit dry-run audit payloads until retention/anonymization jobs are defined.

## Governance design docs

- `docs/threat-model.md` — Phase 1 risks, assets, controls, and live-mode gates.
- `docs/inter-node-api.md` — future node/API envelope and non-goals; design only, no live service yet.
- `docs/governance-rules.md` — implementation rules for identity, mandate, data protection, Discord operation, and PR readiness.
