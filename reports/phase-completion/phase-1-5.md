# Phase 1.5 progress report — Discord dry-run adapter gate

**Phase:** 1.5 — Discord adapter dry-run gate  
**Prepared by:** Hermes backend implementation instance on Quberon 0  
**Status:** PR-ready dry-run adapter

## Implemented

- Discord credential/guild validation helper using Discord REST API.
- Secret-safe validation output: bot token is never returned or printed.
- CLI commands:
  - `discord-doctor` — validate Discord credential presence and, unless skipped, bot/guild identity.
  - `discord-dry-run` — simulate a Discord message, route it through the backend, and log the intended response without posting.
  - `discord-live-post` — explicit gate check for future live posting; Phase 1.5 still posts nothing.
- `OD_DISCORD_LIVE_POST_ENABLED=false` default in `.env.example`.
- Tests covering:
  - dry-run default behavior
  - configured Discord still being live-post gated
  - token redaction in errors/readiness
  - successful mocked Discord identity/guild validation
  - dry-run audit logging with `posted=false`
  - live-post requiring both credentials and explicit env flag

## Still gated / not implemented

- No Discord gateway event loop.
- No live message posting.
- No external LLM calls.
- No long-term raw Discord message storage.
- No retention/anonymization worker yet.

## Next recommended slice

1. Run `discord-doctor` with real local credentials to verify bot identity and guild name.
2. Add a retention/anonymization module before any live message capture.
3. Add a one-channel Discord listener dry-run that consumes events but records only minimised metadata/previews.
4. Only after that, approve one live-post test in a private/operator Discord channel.
