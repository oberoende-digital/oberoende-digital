# Member Conduct Framework Control Gate (Draft)

This draft turns the White Paper v2.2 Member Conduct Framework requirement into a reviewable control gate before OD relies on member, voter, poll, or research-participant inputs for platform decisions.

The White Paper says the AI Constitution is complemented by a parallel governance layer for human member behaviour. This artifact does not create a membership system by itself. It defines the minimum controls that must exist before membership, voting, deliberation, or research workflows process human-member inputs at scale.

## Source anchors

- White Paper v2.2 §3: the AI Constitution is complemented by a Member Conduct Framework for human member behaviour, conflicts of interest, minority protection, conduct standards, and escalation.
- White Paper v2.2 §3.2: the framework must address coordinated manipulation, bad-faith participation, and attempts to instrumentalise AI against OD's constitutional values.
- Backend Instruction v2 §1.1: GDPR, EU AI Act transparency, auditability, and human oversight are hard constraints.
- Backend Instruction v2 §4.5 and §4.8: polls remain advisory in MVP and any mandate-bearing or constitutional effect requires explicit human-admin gates.

## Non-goals / safety boundary

This artifact does **not**:

- create member accounts or collect personal data,
- start BankID or identity-provider integration,
- make polls binding (`advisory_only` remains the default),
- grant or imply democratic mandate,
- enable live Discord posting,
- politically moderate lawful human opinions,
- enable autonomous spending,
- enable crypto/payment flows,
- change Q1 runtime profiles or SOUL.md files,
- create legal advice or a finished party-membership rulebook.

## Minimum framework components before runtime use

Before OD membership, poll, voting, or research systems rely on human-member inputs, a human-reviewed Member Conduct Framework should define:

1. **Scope and status** — whether the framework applies to registered members, volunteers, operators, Discord participants, research participants, or candidates.
2. **Human accountability** — the accountable human/body, operational owner, evidence artifact, and escalation route for each conduct decision.
3. **Conflict-of-interest disclosure** — when members, operators, contractors, donors, or AI-agent operators must disclose interests.
4. **Minority protection** — procedures that prevent majority voting, coordinated blocks, or AI-amplified campaigns from silencing lawful minority views.
5. **Conduct standards** — behavioural expectations for good-faith deliberation, source handling, harassment boundaries, and lawful participation.
6. **Bad-faith/coordinated manipulation handling** — evidence thresholds and review steps for suspected brigading, botting, coercion, or strategic abuse.
7. **Due process** — notice, human review, appeal, reversible sanctions, and audit records before material restrictions are imposed.
8. **AI-use disclosure** — when members or operators must disclose AI-assisted drafting, analysis, campaign material, or automated participation.
9. **Data protection** — lawful basis, minimisation, retention, DSAR/erasure flow, access controls, and ROPA/DPIA linkage before processing member data.
10. **Publication boundary** — what can be public, internal, incident-only, anonymised, or never published.
11. **Emergency handling** — who can pause a workflow during manipulation, harassment, security, or legal-risk incidents, and how the pause is reviewed.
12. **Change gate** — changes to the framework require a GitHub PR, human-admin review, and visible change log before runtime adoption.

## Moderation boundary

OD's systems must not politically moderate humans merely because they disagree with OD, criticize the party, use strong language, or express unpopular lawful views. Intervention is limited to law, platform rules, spam/abuse, operational safety, coercion/manipulation, privacy/security risk, or the explicitly adopted human framework.

Any automated classifier may only flag cases for human review unless a narrow, pre-approved safety rule requires temporary rate limiting or emergency pause. Classifier output must not be treated as a final conduct decision.

## Required evidence before implementation

Before backend code consumes this framework, the PR or implementation issue should attach evidence for:

- accountable human/body and operational owner,
- data-protection assessment and ROPA/DPIA linkage where personal data is involved,
- publication/redaction policy for conduct evidence,
- appeal and rollback process,
- tests or dry-run examples showing advisory-only polls and no false mandate claims,
- explicit confirmation that no live posting, Q1 writes, autonomous spending, or crypto/payment flows are enabled by the conduct gate.

## Current status

Status: **draft control artifact**. It is safe to review and publish as governance scaffolding, but it is not a runtime membership or moderation system until a later human-reviewed implementation PR connects it to backend workflows.
