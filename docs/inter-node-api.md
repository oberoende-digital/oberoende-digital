# OD Phase 1 inter-node API sketch

**Status:** design sketch only. No network service is implemented in Phase 1. The goal is to make future Quberon/OD nodes interoperable without introducing personal-data processing before the ROPA and retention controls are ready.

## Design principles

- Dry-run first; live traffic requires explicit operator launch.
- Synthetic-agent disclosure is a protocol invariant, not a UI afterthought.
- Advisory outputs must not be represented as democratic mandate.
- Raw personal data must not cross node boundaries unless documented in the ROPA and minimized.
- Idempotency and auditability are required for every accepted command.

## Proposed local message envelope

```json
{
  "version": "od-node-v0",
  "idempotency_key": "uuid-or-content-hash",
  "created_at": "2026-06-17T00:00:00Z",
  "source_node": "quberon-0",
  "target_node": "local-dry-run",
  "mode": "dry-run",
  "event_type": "route_request",
  "agent_slug": null,
  "channel_ref": "manual-test",
  "disclosure_required": true,
  "advisory_only": true,
  "payload": {
    "input_preview": "sanitized or operator-provided text"
  }
}
```

## Minimal endpoints for a future service

These are future-facing contracts, not current routes:

- `GET /health` — returns version, mode, storage status, and whether live Discord is disabled/enabled.
- `POST /v0/route` — accepts a sanitized route request and returns selected agent, disclosed response draft, and audit event id.
- `GET /v0/audit/events?limit=20` — returns sanitized audit metadata for operator review.
- `POST /v0/operator/disable-live` — immediately disables live posting/ingestion for incident response.

## Required fields for routed responses

- `agent_slug`
- `response_text`
- `synthetic_disclosure`
- `advisory_only: true`
- `audit_event_id`
- `live_posted: false` unless explicitly operator-launched

## Non-goals for Phase 1

- No wallet/Crossmint/crypto endpoint.
- No autonomous spending endpoint.
- No personal-data replication between nodes.
- No binding vote or mandate-upgrade endpoint.
- No unauthenticated public write API.

## Acceptance criteria before implementation

1. Threat model and governance rules are updated.
2. ROPA includes any live input categories the API would store or transmit.
3. Tests prove disclosure cannot be omitted.
4. Tests prove advisory-only flags remain true for MVP poll/route outputs.
5. Operator disable path is documented and tested before live posting exists.
