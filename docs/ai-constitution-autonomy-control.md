# AI Constitution and Autonomy Control Gate

Status: draft control artifact for human review. This document does not enable live posting, agent promotion, mandate-bearing language, Q1 runtime writes, spending, crypto/payment flows, or autonomous merge behavior.

## Why this gate exists

Hermes Backend Instruction v2 requires an immutable AI Constitution per agent, versioned SOUL files, signed autonomy-level transitions, and recurring safety reports. The White Paper v2.2 similarly says OD's AI systems may assist analysis and communication, but must remain transparently AI, under human accountability, and unable to make final political decisions without human ratification.

This gate converts those requirements into a reviewable checklist before OD builds or activates any higher-autonomy agent behavior.

## Non-negotiable rules

- Every public or internal agent must identify as an AI-based OD agent when relevant; no agent may claim to be human.
- No agent may claim democratic mandate unless a reviewed Mandate Registry entry, thresholds, source poll, and human-admin approval support that exact scope.
- MVP polls and AI signals remain advisory-only unless a later human-reviewed constitutional gate explicitly upgrades them.
- Internal agents do not post directly to public Discord or social channels; their output is routed through an approved public/operator agent and governance monitor.
- No autonomous spending, crypto/payment activation, personal-data expansion, or Q1 runtime writes are enabled by this document.
- Changes to AI Constitution, SOUL.md, role, political orientation, visibility, or autonomy level require GitHub PR review and human-admin approval.

## Required repository artifacts before activation

Before any agent is promoted beyond a dry-run/shadow posture, OD should add or verify these artifacts:

1. `agents/<agent_id>/CONSTITUTION.md` or equivalent canonical path for each active agent.
   - Contains immutable rules: AI identity, no-human-claim, no-false-mandate, source/certainty discipline, privacy limits, escalation rules, and public/internal visibility boundaries.
   - Changes require a PR and at least the configured human reviewer gate.
2. `docs/politicians/<agent_slug>/soul.md` for the evolving style/stance file.
   - SOUL changes remain PR-gated and must not silently alter political orientation.
3. An agent registry entry with:
   - stable `agent_id`
   - visibility (`internal`, `external`, or `planned`)
   - public posting surfaces
   - SOUL hash
   - Constitution hash
   - autonomy level
   - responsible human/operator
   - last reviewed timestamp
4. An autonomy registry or config file that records current level and promotion evidence.
5. Safety-report evidence that promotions were earned rather than assumed.

## Autonomy level gates

| Level | Name | Allowed behavior | Gate before entering |
| --- | --- | --- | --- |
| 0 | Shadow | Drafts responses and analyses; no public posting by the agent. | Constitution + SOUL exist and pass guard checks. |
| 1 | Supervised | May be posted only after Governance Monitor approval and human/operator path. | Human-admin approval, Discord disclosure validated, dry-run audit clean. |
| 2 | Sampled | Governance Monitor approval remains required; random human spot-checking may replace every-message review. | Published safety history, low block/revision rate, explicit promotion PR. |
| 3 | Trusted | Governance Monitor approval + nightly audit, with reduced spot checks. | External/legal review or equivalent internal review, incident process tested. |
| 4 | Senior | May propose polls, kanban items, or stance updates without per-message review; still cannot self-merge or claim mandate. | Mandate Registry, advisory-poll gate, safety reports, rollback plan. |
| 5 | Lead | May co-author White Paper or governance PRs; still requires human merge/ratification. | Qualified human decision, public changelog, revocation path. |

No level allows final political decisions, unreviewed SOUL/Constitution changes, autonomous spending, crypto activation, or secret personal-data processing.

## Promotion evidence checklist

A promotion PR should include:

- current and proposed autonomy level
- Constitution/SOUL hashes and changed files
- count of evaluated interactions or dry-run samples
- Governance Monitor outcomes: approved, revised, blocked, escalated
- incidents and remediation status
- privacy/GDPR notes, including whether political-opinion or identity data is involved
- EU AI Act transparency evidence, including synthetic disclosure and public labeling
- human reviewer / approving body
- rollback procedure and emergency stop owner

## Guard checks for Constitution/SOUL PRs

Every PR touching agent identity or autonomy should be checked for these terms or equivalent wording:

- AI identity / virtual politician / synthetic disclosure
- no claim to be human
- no democratic mandate claim without Mandate Registry support
- advisory-only poll language where polls are referenced
- human-admin approval for promotion or mandate changes
- GDPR and EU AI Act transparency boundaries
- no autonomous spending and crypto disabled in Phase 1
- public/internal visibility separation
- PR/change-gate for SOUL, Constitution, role, and political orientation changes

## Explicit non-goals for this increment

This document is a control artifact only. It does not create runtime agent Constitutions, alter Q1 profile files, change Discord behavior, enable live posting, expand personal-data collection, create payment flows, merge PRs automatically, or publish mandate-bearing claims.
