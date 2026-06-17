# Phase 1.7 progress report — talk-to-od-ai monitor dry-run

**Phase:** 1.7 — background/once Discord monitor dry-run  
**Prepared by:** Hermes backend implementation instance on Quberon 0  
**Status:** PR-ready monitor gate

## Channel monitored

- Discord channel: `🤖-talk-to-od-ai`
- Channel ID: `1509855875102277652`
- Config key: `OD_DISCORD_MONITOR_CHANNEL_ID`

## Implemented

- Persistent monitor state file via `OD_MONITOR_STATE`.
- `last_seen_message_id` tracking.
- Duplicate protection using a bounded `seen_message_ids` set.
- New CLI command:
  - `discord-monitor-dry-run --channel-id 1509855875102277652 --once --limit N`
  - bounded/background loop support with `--interval` and `--max-iterations`
- Monitor run audit event:
  - fetched count
  - handled count
  - ignored count
  - duplicate_skipped count
  - last_seen_message_id
  - posted=false
- Safety report monitor summary:
  - monitor run count
  - messages fetched
  - messages handled
  - messages ignored
  - duplicate messages skipped
  - last seen message ID
- Tests for first-run handling, second-run duplicate skipping, and safety-report counters.

## Still gated / not implemented

- No live Discord posting.
- No external LLM calls.
- No autonomous public responses.
- No broad channel monitoring beyond `talk-to-od-ai`.
- No production daemon/scheduler yet; this PR provides the safe once/loop command that a scheduler can call after review.

## Next recommended slice

After review/merge, run a recurring dry-run monitor job every 1–2 minutes and alert only on anomalies. Once the monitor has run cleanly for a period, the next human-gated step is a single private-channel live-post test.
