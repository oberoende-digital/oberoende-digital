# OD accountability matrix — member/data protection and public AI operations

**Status:** Draft for human/legal review  
**Scope:** Oberoende Digital Quberon 0 backend/platform operations, public website/docs, Discord dry-run monitor, Quberon 1 agent runtime coordination, and future member/poll/donation workflows.  
**Sources:** Hermes Backend Instruction v2, OD White Paper v2.2, GDPR Articles 6/17/30, EU AI Act transparency and high-risk-equivalent governance duties, and `docs/gdpr-ropa.md`.

> This is an operational accountability map, not legal advice. It should be reviewed before any formal membership, voting, donation, live-public-agent, or large-scale personal-data processing goes live.

## Non-negotiable guardrails

- OD agents and content must be transparent about AI identity; no public profile, answer, or report may imply that an AI agent is a human politician.
- MVP polls are advisory only unless a reviewed Mandate Registry, thresholds, human approval record, and publication rules prove otherwise.
- Internal agents do not post directly to Discord or other public channels; public output must pass the public-facing agent/operator gate.
- No autonomous spending, wallet movement, crypto execution, or donation classification; Phase 1 finance work is read-only and auditable.
- Humans are not politically moderated by OD agents except for law, platform rules, spam, abuse, or operational safety requirements.
- SOUL.md, AI Constitution, role, visibility, or political-orientation changes require version-controlled PR review before runtime upload.

## Accountability matrix

| Area | Accountable human / body | Operational owner | Evidence artifact | Required gate before expansion | Current status |
|---|---|---|---|---|---|
| AI identity disclosure and synthetic-agent labeling | OD human admin / party leadership | Q0 backend operator for implementation; Q1 orchestrator for runtime profiles | Public pages, agent registry, SOUL.md files, Discord intro/disclosure text, PR history | Disclosure text reviewed and present on every public AI interaction surface | In progress: local canonical SOUL files exist; Q1 runtime reconciliation still gated |
| Incorrect AI response or hallucinated policy claim | OD human admin / designated policy reviewer | Public-facing agent operator; backend audit job | Incident log, correction-log entry, linked conversation/audit IDs, GitHub issue/PR if docs/code change needed | Correction workflow and public correction page before live public answers | Draft/gated |
| Political mandate claim or poll interpretation | OD human admin / mandate reviewer | Mandate Registry module owner | Poll record, threshold configuration, admin approval, public rationale, changelog | Mandate Registry and advisory/mandate distinction reviewed before any mandate claim | Not live; advisory-only |
| Discord/user message processing | Controller candidate: Oberoende Digital / Rasmus Lundqvist pending legal confirmation | Q0 backend/gateway operator | ROPA rows, safety report counters, minimized audit logs, dry-run monitor state | Lawful-basis review, retention schedule, DSAR path, live-post approval | Dry-run only; live posting disabled |
| DSAR/access/erasure request | Controller / privacy contact | Privacy/admin operator | DSAR ticket, identity-verification note, export/erasure log | Admin-only DSAR playbook and retention implementation before production personal-data scale | ROPA skeleton exists; implementation pending |
| Incident/safety report | OD admin / safety reviewer | Q0 backend operator | Safety report, watchdog output, incident log, PR if code or docs change | Sanitized reporting that omits raw Discord content, raw author IDs, and sensitive previews | Active dry-run reports; public publication still gated |
| Technical backend change | Repository maintainers / human reviewer | Implementing agent/operator | GitHub branch, PR, tests, safety-report output, raw-file verification | PR review, test suite not `Ran 0 tests`, no unrelated dirty files committed | Active PR workflow |
| SOUL.md / AI Constitution / role or visibility change | OD human admin / constitutional reviewer | Q0 GitHub operator and Q1 runtime operator | PR diff, guard checks, runtime checksum after approved upload | Human review/merge before upload to Q1 or public profile update | PR-gated |
| External communications and public posts | OD comms/human admin | Public-facing approved agent/operator | Draft post, source references, correction/approval trail | Human approval for political claims, campaign messaging, or sensitive issues | Gated |
| Legal assessments and compliance claims | Qualified human/legal reviewer | Compliance documentation operator | Legal memo/reference, ROPA/DPIA updates, public limitation notes | No claim of full compliance without reviewed evidence | Draft/high-risk-equivalent posture only |
| Financial transaction/donation handling | Treasurer/human admin | Finance integration operator | Payment provider logs, donation register, anonymous cap check, bookkeeping export | No autonomous spending; donation workflow legal review and Swedish financing-law controls | Disabled/read-only in Phase 1 |
| Q1 remote politician runtime operations | OD/Q1 administrator | Q0 operator for SSH audit; Q1 operator for runtime change | SSH discovery log, downloaded checksums, PR mapping runtime vs canonical files | Reviewed PR and explicit upload approval before writing remote SOUL/runtime files | SSH reachable via `quberon1`; writes gated |

## Minimum incident record

Every material incident or correction should record:

1. Incident ID and timestamp in UTC plus displayed Europe/Stockholm time where public.
2. A sanitized description that does not echo private Discord content or raw author IDs.
3. Affected surface: website, Discord dry-run/live, Q1 runtime, GitHub, finance, membership, or policy docs.
4. Guardrail category: AI identity, mandate, personal data, safety, technical reliability, finance, legal/compliance, or public communication.
5. Immediate containment: disabled feature, blocked PR, deleted/hidden content, or human-review hold.
6. Evidence references: audit event IDs, GitHub PR/commit, safety-report counters, and approved public correction link.
7. Responsible human reviewer and operator.
8. Outcome: corrected, accepted risk, deferred, superseded, or escalated to legal/admin.

## Pre-live checklist for member/data-protection expansion

- [ ] Controller identity, contact address, and DPO/contact model confirmed.
- [ ] ROPA rows updated from amber/red to reviewed status for the processing activity being enabled.
- [ ] Retention schedule and DSAR/export/erasure path tested on synthetic data.
- [ ] DPIA or documented screening completed for any high-risk/special-category political data workflow.
- [ ] Sub-processor list reviewed for Discord, GitHub, LLM providers, payment providers, hosting, and Q1 runtime.
- [ ] Safety report proves live posting is disabled or explicitly approved, and that raw content/author IDs are not exposed in watchdogs.
- [ ] Public transparency text states AI identity, advisory-only polls, limitation of compliance claims, and correction process.
- [ ] Human approval record exists for any mandate, finance, live-public-agent, SOUL/constitution, or role/visibility change.

## Open follow-up tasks

- Convert this draft into public website copy once reviewed.
- Add a machine-readable owner/status field to each backend processing activity and agent registry entry.
- Connect incidents/corrections to a public correction log without exposing private content.
- Add tests that block live public posting unless the accountable gate fields are populated.
