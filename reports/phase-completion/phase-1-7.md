# Phase 1.7 progress report — stateful Discord dry-run poller

**Phase:** 1.7 — Stateful dry-run polling primitive for `talk-to-od-ai`  
**Prepared by:** Hermes backend implementation instance on Quberon 0  
**Status:** PR-ready worker building block

## Implemented

- Added `backend/od_backend/discord_poller.py` with:
  - a minimal `discord_poll_state` SQLite table for per-channel cursor state;
  - a `poll_channel_dry_run` one-tick worker primitive;
  - explicit `max_handle_per_tick` rate limiting;
  - first-run cursor bootstrap that does not process existing history unless `--process-existing` is explicit.
- Added CLI command:
  - `discord-poll-once --channel-id 1509855875102277652 --limit N [--max-handle N] [--process-existing]`.
- Added `OD_DISCORD_POLL_MAX_PER_TICK` config and `.env.example` documentation.
- Updated backend README safety gates and local commands.
- Added unit tests for cursor bootstrap, rate limiting, minimized handling, and raw identifier avoidance.

## Safety posture

- No live Discord posting.
- No external LLM calls.
- No broad channel monitoring beyond the configured allowlist.
- No raw message-content persistence by the poller; audit entries keep minimized previews only.
- The poller records only the channel cursor (`last_seen_message_id`) plus aggregate dry-run tick counts.

## Next recommended slice

1. Run `discord-poll-once` with real local credentials and the `talk-to-od-ai` channel ID.
2. Inspect the dry-run safety report and audit counts.
3. If stable, wrap `discord-poll-once` in an operator-controlled background service with low-frequency schedule and a documented disable command.
4. Only after the dry-run worker has operated cleanly should a human admin consider one private-channel live-post test.
