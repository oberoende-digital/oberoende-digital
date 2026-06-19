# OD public correction and change-log gate

Status: draft control artifact for human review.

This document defines the public correction and change-log process that OD needs before the website, policybase, public agent profiles, or Discord-facing behavior become more visible. It implements the White Paper v2.2 transparency commitment and the Hermes Backend Instruction v2 requirement that public AI systems stay auditable, version-controlled, and honest about uncertainty.

It is not a launch approval, mandate claim, legal compliance certification, or permission for live Discord replies.

## Scope

Track public corrections and material changes for:

- Website pages, public policybase pages, and public explanatory material.
- AI politician profile/SOUL summaries that are published or referenced publicly.
- Public safety-report summaries after their redaction gate is approved.
- Advisory poll wording, methodology notes, and mandate-boundary text.
- Corrections to claims about OD's status, compliance posture, financing, or AI autonomy.

Private Discord content, raw author IDs, phone numbers, personal identity numbers, credentials, and unreviewed internal reasoning do not belong in the public log.

## Minimum public log fields

| Field | Meaning | Safety rule |
| --- | --- | --- |
| Date | When the correction or material change was published | Use date only unless a precise time is necessary |
| Area | Website, policybase, SOUL/profile, safety report, poll, financing, compliance, or incident | Avoid naming private users |
| Summary | What changed in plain language | No raw Discord/private content |
| Reason | Error correction, evidence update, legal/compliance gate, safety gate, user feedback, or editorial clarification | Distinguish evidence from value judgment |
| Evidence | GitHub PR/commit, issue, public source, or approved incident report | Prefer public links; no secrets |
| Human gate | Who/which body approved when required | Record role/body, not private chat text |
| Impact | Whether the change affects policy interpretation, agent behavior, data processing, or only wording | No democratic-mandate claims without Mandate Registry support |

## Severity levels

1. **Editorial clarification** — improves wording, accessibility, links, translations, or formatting without changing meaning.
2. **Evidence update** — changes a factual claim, source reference, uncertainty statement, or policybase basis.
3. **Governance/safety correction** — fixes AI identity, mandate-boundary, advisory-only poll, privacy, financing, or live-posting language.
4. **Incident disclosure** — human-approved public notice for a material safety, privacy, security, or compliance event.

## Required gates

- SOUL.md, AI Constitution, role, visibility, or political-orientation changes require a GitHub PR and human review before runtime upload or public reliance.
- Public safety summaries require redaction tests proving no raw Discord content, raw author IDs, secrets, phone numbers, or Swedish personal identity numbers are emitted.
- MVP poll changes must keep advisory-only language unless a human-admin mandate gate and published thresholds approve stronger status.
- Financing changes must preserve the no-autonomous-spending rule, Phase 1 crypto-disabled rule, and anonymous-donation ceiling of **2,940 SEK**.
- Compliance wording must not claim full GDPR/EU AI Act compliance before legal analysis, implementation evidence, and independent/human review support it.

## Initial log template

```markdown
## YYYY-MM-DD — Short title

- **Area:** Website | policybase | SOUL/profile | safety report | poll | financing | compliance | incident
- **Severity:** Editorial clarification | evidence update | governance/safety correction | incident disclosure
- **Summary:** ...
- **Reason:** ...
- **Evidence:** PR #..., commit ..., issue ..., or public source ...
- **Human gate:** Not required / pending / approved by ...
- **Impact:** ...
```

## Current next implementation steps

- Add a public `/transparency/` or `/corrections/` page only after human review decides where the log belongs on the website.
- Link this gate from the public platform roadmap, accountability matrix, and safety-reporting document.
- Use GitHub PR numbers as the first evidence source for all public governance and website corrections.
- Keep live Discord posting, Q1 runtime SOUL uploads, personal-data expansion, autonomous spending, and crypto activation blocked unless their separate human/compliance gates are approved.

## Non-goals

This gate does not politically moderate humans, publish private user content, automate public replies, activate donations, create binding poll outcomes, or certify that OD is already fully autonomous or fully compliant.
