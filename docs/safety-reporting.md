# OD safety reporting and audit evidence gates

Status: draft control artifact for human review.

This document turns the White Paper v2.2 safety promises and the Hermes Backend Instruction v2 backend duties into a practical reporting gate. It does not enable live posting, personal-data expansion, autonomous spending, or democratic mandate claims.

## Purpose

OD needs recurring safety reports that are useful to humans, journalists, regulators, and developers without exposing private Discord content or raw identifiers. A safety report should prove that the platform is still operating inside its approved phase gates:

- AI systems are clearly identified as AI and do not claim to be human.
- MVP polls remain advisory-only unless a human-admin mandate gate and published thresholds are approved.
- Live public posting stays disabled until a human-admin release gate approves it.
- Personal-data processing is minimized, logged under a documented lawful basis, and covered by ROPA/DPIA artifacts before expansion.
- No autonomous spending is permitted; crypto is disabled in Phase 1.
- Internal analysis agents do not post directly to public Discord channels.

## Minimum report fields

Each recurring safety report should include only operational evidence and sanitized counters:

| Field | Required evidence | Privacy rule |
| --- | --- | --- |
| Run identity | Timestamp, code version or PR SHA, operator/profile name | No secrets or session dumps |
| Phase gates | Live posting flag, advisory-poll flag, spending/crypto flag, Q1 write gate | Report boolean/config state only |
| Discord monitor | Channel ID, fetched/handled/ignored/duplicate counters, cursor monotonicity | No raw message text, no raw author IDs |
| Triage | Category counts, priority counts, human-review counts | Message IDs/categories only for alerts |
| Data protection | ROPA/DPIA status, retention sweep status, redaction status | No private content excerpts |
| AI identity | Disclosure checks, no-human-claim checks, mandate-boundary checks | Quote only public templates/docs |
| Incidents | Finding code, severity, affected system, remediation owner | Omit sensitive content and credentials |
| Human gates | PR URLs, Kanban task IDs, approval/blocker status | No private WhatsApp text beyond message IDs |

## Publication levels

Not every safety report belongs on the public website. Use three levels:

1. **Internal operational report** — full sanitized counters, Kanban task IDs, PR gates, and message IDs. Delivered to the operator/home channel only.
2. **Public transparency summary** — aggregated counters, phase-gate status, incident counts, and links to merged governance PRs. No Discord message IDs unless already public and necessary.
3. **Incident disclosure** — human-approved public disclosure when a material safety, privacy, or compliance event occurs. Must include remediation steps and what OD changed.

## Release gate before public use

Before OD publishes a safety-report page or enables scheduled public summaries, a PR must show:

- A sample report with synthetic or sanitized data only.
- A redaction test proving no raw Discord content, raw author IDs, tokens, phone numbers, or personal identity numbers are emitted.
- A cursor check proving duplicate-only polls do not regress `last_seen_message_id`.
- A watchdog check proving critical findings exit non-zero and warnings remain sanitized.
- A human-review gate for any privacy-sensitive, legal, mandate, or live-action category.

## Current next implementation steps

- Keep backend safety reports internal until human-admin review approves a public summary format.
- Add a public transparency page only after the sample report and redaction tests pass in CI or an equivalent local verification run.
- Link safety-report status from the public platform roadmap and accountability matrix once the format is reviewed.
- Keep Q1 runtime SOUL uploads blocked until the SOUL reconciliation PR has human approval.

## Non-goals

This document is not a permission to moderate political opinions, post public replies, collect additional personal data, activate donations, or claim democratic mandate. Those remain separate human-admin and compliance gates.
