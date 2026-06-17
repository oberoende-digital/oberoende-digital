# OD Phase 1 threat model

**Scope:** the Phase 1 backend dry-run foundation in `backend/od_backend/` and the first controlled Discord-facing increments. This document is intentionally conservative: it describes controls that must exist before live public-message ingestion or posting.

## Assets

- Public trust in OD's democratic experiment and clear separation between humans and synthetic agents.
- Discord community safety, including protection against impersonation, harassment, brigading, and mandate confusion.
- Audit evidence for operator accountability and incident review.
- Configuration secrets such as Discord bot tokens and future provider credentials.
- Any future personal data collected from community interactions.

## Actors

- **Human admin/operator:** accountable for launches, approvals, escalation, and mandate changes.
- **Synthetic OD agents:** may draft, classify, route, or answer only within disclosed, advisory constraints.
- **Community members:** may ask questions, report bugs, and participate in advisory polls.
- **Adversaries or confused users:** may try prompt injection, impersonation, spam, social engineering, or mandate inflation.

## Primary risks and required controls

| Risk | Phase 1 control |
| --- | --- |
| Synthetic agent appears to claim human identity or democratic mandate | Every outbound agent message must include synthetic-agent disclosure; copy must say human operators remain accountable. |
| Advisory poll is mistaken for binding governance | Poll outputs must be labeled advisory-only until a human admin approves mandate thresholds and constitutional upgrade process. |
| Live Discord messages create untracked personal-data processing | No raw live Discord ingestion until the ROPA is updated with purpose, categories, retention, recipients, rights, and legal basis. |
| Prompt injection via Discord content changes agent behavior | Treat user content as untrusted input; keep routing deterministic until an LLM policy layer has tests and refusal rules. |
| Secret leakage from configuration or logs | Keep secrets in environment variables only; never commit `.env`; redact tokens in logs and reports. |
| Autonomous spending or crypto actions | Crypto/wallet functionality remains disabled in Phase 1; no autonomous spending; anonymous donation cap remains 2,940 SEK. |
| Abuse, harassment, or unsafe political claims | Route incidents to a human admin; preserve minimal audit facts; do not let agents escalate, punish, or claim enforcement authority. |
| Discord bot over-posting or spam | Live posting must be behind explicit operator launch and rate-limit/allowlist checks. |

## Phase gates

1. **Current allowed mode:** dry-run routing, synthetic responses, local audit log, readiness checks.
2. **Before live read access:** update `docs/gdpr-ropa.md` for Discord message processing and add retention/anonymization behavior.
3. **Before live write access:** require explicit operator command, target-channel allowlist, disclosure enforcement test, and rollback/disable command.
4. **Before LLM calls:** add prompt-injection tests, refusal/safety policy checks, cost limits, and human escalation paths.
5. **Before any mandate upgrade:** human-admin approval plus documented threshold rules; synthetic agents may not self-authorize.

## Incident minimums

- Capture time, channel, event type, affected synthetic agent, and a short sanitized summary.
- Do not store more personal data than needed for the safety purpose.
- Escalate security/compliance risks to the human admin before continuing automation.
