# Risk Register and Incident Response Control Gate (Draft)

This draft turns the White Paper v2.2 EU AI Act risk-management promise into a reviewable control gate before OD treats automated Discord, voting, mandate, research, or Q1 politician-agent workflows as production systems.

It is a governance/control artifact only. It does not enable live posting, personal-data expansion, autonomous spending, crypto/payment flows, mandate-bearing behavior, or Q1 runtime writes.

## Source anchors

- White Paper v2.2 §1.4: OD voluntarily applies a high-risk-equivalent governance model with risk management, data governance, technical documentation, logging, transparency, human oversight, robustness, and cybersecurity.
- White Paper v2.2 §3: the AI Constitution must be complemented by technical documentation, a risk register, an incident process, security tests, and recurring audits.
- White Paper v2.2 §3.3: public AI audit reports should include weaknesses, incidents, remediation, model/prompt/system changes, and security tests.
- Backend Instruction v2 §1.1: GDPR, EU AI Act Articles 8–15/50, Swedish financing constraints, auditability, and human oversight are hard constraints.
- Backend Instruction v2 §4.1–§4.12: Discord, polling, mandate, inter-node API, SOUL, and autonomy behavior must be gated, version-controlled, and auditable.

## Non-goals / safety boundary

This artifact does **not**:

- declare OD legally compliant with the EU AI Act or GDPR,
- create a live production incident-response team,
- enable live Discord posting or public automated replies (`no live posting` remains the default until a separate human-approved gate),
- collect or process additional personal data,
- publish raw Discord content, raw author IDs, secrets, or private incident evidence,
- grant democratic mandate or make MVP polls binding (`advisory_only` remains the default),
- enable autonomous spending or crypto/payment flows; crypto remains disabled in Phase 1,
- make advisory-only MVP polls binding without a separate mandate registry gate,
- change Q1 runtime profiles, SOUL.md files, Constitution files, roles, or political orientation.

## Minimum risk-register fields

Before a workflow moves beyond dry-run/control-artifact status, its risk register entry should include:

| Field | Minimum requirement |
|---|---|
| `risk_id` | Stable ID, for example `OD-RISK-DISCORD-001` |
| `workflow` | Discord monitor, public Q&A, advisory poll, mandate registry, SOUL sync, policybase, finance, etc. |
| `source_anchor` | White Paper / Backend Instruction / legal or policy source requiring the control |
| `risk_description` | Clear description without raw private content |
| `affected_people` | Public users, Discord participants, members, operators, voters, candidates, minors, etc. |
| `data_categories` | No data, pseudonymous Discord metadata, member identity data, poll data, payment data, special-category data, etc. |
| `severity` / `likelihood` | Human-reviewed low/medium/high rating and rationale |
| `existing_controls` | Current prevention/detection/mitigation controls |
| `required_gate` | Human-admin decision, PR review, DPIA/ROPA, legal review, security test, rollback test, etc. |
| `evidence_artifacts` | PRs, tests, safety reports, watchdog reports, review notes, incident tickets |
| `owner` | Accountable human/body and operational owner |
| `status` | Draft, accepted, mitigated, transferred, blocked, retired |
| `review_date` | Next required review date or trigger |

## Required incident process fields

Before live public behavior or personal-data workflows are enabled, OD should maintain an incident process with:

1. **Detection channels** — watchdog findings, audit-log anomalies, user reports, operator reports, platform-abuse notices, GitHub issues, and security-test results.
2. **Severity classes** — privacy/security, incorrect mandate claim, unlabeled AI output, unlawful content, platform-rule violation, Q1 runtime drift, spending/finance issue, data-loss issue, and operational outage.
3. **Immediate containment** — emergency stop / live-post disablement, Discord permission pause, credential rotation, Q1 profile rollback, PR freeze, or public correction hold.
4. **Human accountability** — named accountable human/body and operational owner for triage, decision, and closure.
5. **Privacy-preserving evidence handling** — store only minimized evidence where possible; use redacted evidence in review artifacts; do not publish raw Discord content, raw author IDs, secrets, private personal data, or sensitive incident details.
6. **Notification decision** — when to notify affected users, Rasmus/admins, Discord moderators, GitHub, data-protection contacts, or authorities.
7. **Correction and transparency path** — public correction log or safety-report entry when safe, lawful, and useful; incident-only internal record otherwise.
8. **Root cause and remediation** — code/docs/config fix, test addition, safety-report update, risk-register update, and rollback verification.
9. **Closure evidence** — PR links, command outputs, raw GitHub checks, watchdog/safety-report counters, and human approval notes.
10. **Review cadence** — recurring review of open incidents and stale mitigations.

## Gate checklist before runtime adoption

A PR or issue that tries to move an OD workflow from draft/dry-run to runtime use must show:

- [ ] Risk register entry exists and is human-reviewed.
- [ ] Incident process owner and escalation path are named.
- [ ] GDPR lawful basis, minimization, retention, DSAR/erasure, and ROPA/DPIA linkage are documented where personal data is involved.
- [ ] EU AI Act transparency, synthetic-disclosure controls, and transparent AI identity wording are documented for public AI output.
- [ ] Public/internal agent separation is preserved; internal agents do not post directly.
- [ ] `advisory_only` remains the MVP poll default unless a separate mandate registry gate is approved.
- [ ] No false democratic mandate claim is possible without Mandate Registry evidence and human-admin approval.
- [ ] No autonomous spending, no crypto/payment flows, and crypto disabled in Phase 1 remain enforced.
- [ ] Safety-report/watchdog outputs omit raw private content, raw author IDs, secrets, and sensitive previews.
- [ ] Rollback/emergency-stop behavior is tested or explicitly blocked pending implementation.
- [ ] Changes to SOUL.md, Constitution, role, visibility, autonomy level, or political orientation remain GitHub-PR-gated.

## Current status

Status: **draft control artifact**. It can be reviewed and linked from the repository now, but it must not be treated as a complete legal compliance program or production incident-response process until human-admin review, legal/privacy review where needed, and implementation PRs connect it to specific workflows.
