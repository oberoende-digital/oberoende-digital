# OD backend — Phase 1 skeleton

This is the first backend skeleton after the Phase 0 constitutional bootstrap gate. It is deliberately conservative: no live Discord posting and no external LLM call happens by default.

## What is included

- Environment/config loader with Discord and LLM defaults.
- Synthetic-agent disclosure wrapper for outbound messages.
- Agent registry including Anna Medelvärde and her `soul.md` path.
- Simple deterministic router for dry-run messages.
- SQLite audit log for routed dry-run events.
- Discord readiness check that stays in dry-run mode without credentials.
- Safety-report generator from the audit log.
- Unit tests for routing, disclosure, audit logging, Discord dry-run mode, and safety report output.

## Local commands

```bash
PYTHONPATH=backend python3 -m od_backend.cli doctor
PYTHONPATH=backend python3 -m od_backend.cli route "What is the cost-benefit risk?" --channel manual-test
PYTHONPATH=backend python3 -m od_backend.cli safety-report
PYTHONPATH=backend python3 -m unittest discover -s backend/tests
```

## Safety gates

- Live Discord connection requires `DISCORD_BOT_TOKEN` and `DISCORD_GUILD_ID` to be present and an explicit operator launch.
- `OD_LLM_PROVIDER` defaults to `disabled`; external model calls are not implemented in this skeleton.
- Every dry-run response includes synthetic-agent disclosure.
- Raw public message storage is limited to explicit dry-run audit payloads until retention/anonymization jobs are defined.
