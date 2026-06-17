# Phase 1.6 progress report — talk-to-od-ai listener dry-run and minimization

**Phase:** 1.6 — Discord listener dry-run with retention/minimization  
**Prepared by:** Hermes backend implementation instance on Quberon 0  
**Status:** PR-ready dry-run monitor

## Channel selected

- Discord channel: `🤖-talk-to-od-ai`
- Channel ID: `1509855875102277652`
- Config key: `OD_DISCORD_MONITOR_CHANNEL_ID`

## Implemented

- Retention/minimization helper module:
  - redacts email addresses, URLs, and Discord mentions
  - truncates message previews
  - pseudonymizes Discord author IDs with HMAC-SHA256 and `OD_RETENTION_HASH_SECRET`
- Discord dry-run event handling now routes redacted previews rather than raw message content.
- One-channel allowlist check for listener/polling dry-run.
- Bot/self-message ignore path.
- Recent-message polling dry-run via Discord REST API:
  - fetches recent messages from the allowlisted channel
  - routes only human messages
  - records audit events with `posted=false`
- Retention sweep CLI for counting or deleting old audit events.
- CLI commands:
  - `discord-listen-dry-run --channel-id 1509855875102277652 --limit N`
  - `retention-sweep --days N [--apply]`
- Unit tests for minimization, raw-content avoidance, allowlist behavior, bot ignore, scan dry-run, and retention sweep.

## Still gated / not implemented

- No Discord gateway websocket listener.
- No live Discord posting.
- No external LLM calls.
- No autonomous responses.
- No broad channel monitoring beyond `talk-to-od-ai`.

## Next recommended slice

1. Run `discord-doctor` with real local credentials.
2. Run `discord-listen-dry-run` against `talk-to-od-ai` and inspect the safety report.
3. If the dry-run audit trail looks correct, add a background polling worker with explicit rate limits.
4. Only after that, approve a single private-channel live-post test.
