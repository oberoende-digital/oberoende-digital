# OD public platform roadmap and safety gates

Status: draft operational roadmap derived from Hermes Backend Instruction v2 and OD White Paper v2.2. This document is a planning and transparency artifact, not a political programme, mandate claim, or launch approval.

## Purpose

OD's platform work should be legible before it is powerful. This roadmap turns the White Paper's commitments into reviewable implementation gates so that GitHub issues, pull requests, safety reports, and public pages can show what is built, what is blocked, and what still requires human/legal review.

## Non-negotiable operating boundaries

- **AI identity is explicit.** Public-facing agents, pages, and Discord flows must clearly disclose when a response or profile is AI-generated or AI-operated.
- **No false mandate.** MVP polls and Discord feedback are advisory unless the Mandate Registry, thresholds, and human-admin approval explicitly support a stronger status.
- **No autonomous spending or crypto.** Phase 1 keeps crypto/payment integrations disabled or read-only; financing must be openly auditable.
- **GDPR and AI Act evidence before scale.** Personal-data processing needs lawful-basis notes, ROPA coverage, retention rules, subject-rights paths, and audit logs before production use.
- **Internal agents do not post directly.** Public Q&A agents and privileged platform/operator agents stay separated.
- **SOUL/constitution changes go through PRs.** Changes to agent identity, role, political orientation, or constitutional boundaries must be version-controlled and reviewable.

## Roadmap gates

| Gate | Public outcome | Required evidence | Current safe next action |
| --- | --- | --- | --- |
| 1. Transparency baseline | Visitors can see what OD is, what it is not, and what is still experimental. | Homepage/about wording, AI disclosure, public contact path, correction/update log. | Add a public correction/change-log page and link it from the site footer/navigation. |
| 2. Governance documentation | Reviewers can inspect rules before trusting agents. | White Paper links, AI Constitution/SOUL index, role separation, safety gate docs. | Keep SOUL files and Q1 runtime reconciliation behind PR/human review. |
| 3. Discord dry-run monitor | OD can observe the talk-to-ai channel without posting or leaking raw content. | Dry-run audit rows, duplicate protection, redacted-preview triage, watchdog checks. | Continue duplicate-only watchdog verification until merge approvals land. |
| 4. Compliance artifacts | GDPR/AI Act work is tracked before personal-data processing expands. | ROPA, DPIA candidates, risk register, retention/erasure process, safety reports. | Draft ROPA entries for Discord monitor and advisory polls before live ingestion. |
| 5. Advisory participation | People can suggest issues and respond to polls with honest limitations. | Advisory-only labels, no mandate claims, human-admin poll upgrade gate. | Prepare poll wording templates that label MVP results as advisory. |
| 6. Public accountability loop | Users can see what changed, why, and what remains blocked. | GitHub PRs/issues, safety-report summaries, public roadmap, correction log. | Convert this roadmap into linked public pages once reviewed. |

## Forgotten-item watchlist

These are recurring items that can be easy to overlook during fast backend work:

1. Keep a **public correction/change log** for website, policybase, and agent-behavior updates.
2. Publish or link **human-review gates** for SOUL.md changes and Q1 runtime uploads.
3. Create **ROPA/DPIA drafts** before expanding Discord processing beyond redacted dry-run monitoring.
4. Add **advisory-only poll labels** to every MVP poll surface and template.
5. Maintain a **financing transparency checklist**, including the anonymous-donation ceiling and Phase 1 crypto-disabled rule.
6. Keep **operator/internal agent separation** visible so internal automation is not mistaken for public representation.

## Review checklist before publishing more broadly

- [ ] No claim that OD is already fully autonomous, fully compliant, or democratically mandated.
- [ ] No implication that AI agents are humans.
- [ ] No promise of live public replies before human-admin approval.
- [ ] No collection of unnecessary personal data.
- [ ] Links to GitHub/PR evidence are available where implementation claims are made.
