# Phase 1.7 progress report — talk-to-od-ai dry-run monitor and poller state

**Phase:** 1.7 — duplicate-protected Discord monitor and stateful dry-run polling primitive  
**Prepared by:** Hermes backend implementation instance on Quberon 0  
**Status:** PR-ready monitor/poller gate

## Channel monitored

- Discord channel: `🤖-talk-to-od-ai`
- Channel ID: `1509855875102277652`
- Config key: `OD_DISCORD_MONITOR_CHANNEL_ID`

## Implemented

- Persistent monitor state file via `OD_MONITOR_STATE`.
- `last_seen_message_id` tracking.
- Duplicate protection using a bounded `seen_message_ids` set.
- Monitor CLI command:
  - `discord-monitor-dry-run --channel-id 1509855875102277652 --once --limit N`
  - bounded/background loop support with `--interval` and `--max-iterations`.
- Monitor run audit event:
  - fetched count;
  - handled count;
  - ignored count;
  - duplicate_skipped count;
  - last_seen_message_id;
  - posted=false.
- Safety report monitor summary:
  - monitor run count;
  - messages fetched;
  - messages handled;
  - messages ignored;
  - duplicate messages skipped;
  - last seen message ID.
- Added `backend/od_backend/discord_poller.py` with:
  - a minimal `discord_poll_state` SQLite table for per-channel cursor state;
  - a `poll_channel_dry_run` one-tick worker primitive;
  - explicit `max_handle_per_tick` rate limiting;
  - first-run cursor bootstrap that does not process existing history unless `--process-existing` is explicit.
- Poller CLI command:
  - `discord-poll-once --channel-id 1509855875102277652 --limit N [--max-handle N] [--process-existing]`.
- Added `OD_DISCORD_POLL_MAX_PER_TICK` config and `.env.example` documentation.
- Updated backend README safety gates and local commands.
- Added/kept unit tests for first-run monitor handling, duplicate skipping, cursor bootstrap, rate limiting, minimized handling, safety-report counters, and raw identifier avoidance.

## Safety posture

- No live Discord posting.
- No external LLM calls.
- No autonomous public responses.
- No broad channel monitoring beyond `talk-to-od-ai`.
- No raw message-content persistence by the poller; audit entries keep minimized previews only.
- The poller records only the channel cursor (`last_seen_message_id`) plus aggregate dry-run tick counts.

## Next recommended slice

1. Merge the Phase 1.7 stateful poller PR after review.
2. Run `discord-poll-once` with real local credentials and the `talk-to-od-ai` channel ID.
3. Inspect the dry-run safety report and audit counts.
4. If stable, wrap the poller/monitor in an operator-controlled low-frequency dry-run schedule with a documented disable command.
5. Only after the dry-run worker has operated cleanly should a human admin consider one private-channel live-post test.
