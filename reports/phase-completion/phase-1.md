# Phase 1 progress report — Backend skeleton

**Phase:** 1 — Backend skeleton
**Prepared by:** Hermes backend implementation instance on Quberon 0
**Status:** Initial dry-run skeleton

## Implemented

- Conservative Python backend package under `backend/od_backend/`.
- `.env.example` documenting dry-run defaults and Discord credential names.
- Synthetic disclosure enforcement for outbound agent messages.
- Agent registry with Anna Medelvärde mapped to `docs/politicians/anna-medelvarde/soul.md`.
- Simple deterministic router for manual dry runs.
- SQLite audit log for routed events.
- Discord readiness check that remains dry-run unless credentials exist.
- Safety report generated from audit-log data.
- Unit tests for disclosure, routing, audit logging, readiness, and safety reporting.

## Still gated / not implemented

- No live Discord event loop or message posting.
- No external LLM provider calls.
- No storage of raw live Discord traffic.
- No wallet/Crossmint integration.
- No inter-node API yet.

## Next recommended slice

1. Add `docs/threat-model.md`, `docs/inter-node-api.md`, and `docs/governance-rules.md`.
2. Add retention/anonymization jobs before any live public-message ingestion.
3. Add a live Discord adapter behind explicit operator command and credential validation.
4. Add CI for Python unit tests and Markdown checks.
