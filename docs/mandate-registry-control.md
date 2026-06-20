# Mandate registry and advisory-poll control gate

Status: draft control artifact derived from Hermes Backend Instruction v2 §4.4–§4.5 and OD White Paper v2.2 §§4.1–4.3. This document is not a live mandate registry, not an election result, and not permission for any AI agent to claim democratic authority.

## Purpose

OD's MVP can use Discord discussions and polls as participation signals, but those signals must not be laundered into democratic mandate. This gate defines the minimum public and technical controls required before any poll, vote, or agent response may be described as more than advisory.

## Non-negotiable boundaries

- **Advisory by default.** Every MVP poll, Discord signal, and AI-agent vote signal is `advisory_only=true` unless a later human-reviewed registry entry explicitly changes that status.
- **No false mandate claims.** Agents and public pages must not say OD, a politician agent, or a proposal has democratic mandate unless the Mandate Registry records the source poll, thresholds, human-admin approval, and publication scope.
- **Human legitimacy remains primary.** Binding decisions require eligible human members and the governing process described in the White Paper; AI agent signals are reported separately and do not affect formal outcomes in Phase 1.
- **Transparent AI identity.** Any AI-generated poll summary, recommendation, or agent opinion must be labeled as AI-assisted/synthetic.
- **No political moderation of humans.** Reasoning scores, mandate scores, and poll readiness signals prioritize review and analysis; they must not suppress lawful political speech.
- **GDPR/EU AI Act evidence before scale.** Poll/voting data must have ROPA/DPIA coverage, lawful-basis notes, retention/erasure handling, EU AI Act transparency/human-oversight evidence, and redacted safety-report treatment before production collection expands.
- **No autonomous spending or crypto.** Financing, rewards, paid campaigning, and crypto integrations remain outside this gate and disabled in Phase 1 unless separately approved.
- **No live posting by implication.** This control gate does not enable Discord live posting, autonomous public replies, or mandate-bearing agent language; those remain separately human-approved gates.

## Registry fields required before mandate-bearing language

A mandate-bearing registry entry must include at least:

| Field | Requirement |
| --- | --- |
| `mandate_id` | Stable, version-controlled identifier. |
| `source_poll_id` | Poll/vote source with immutable question text and option set. |
| `scope` | Exact scope: discussion signal, proposal support, internal decision, public platform position, or other approved category. |
| `advisory_only` | Boolean; defaults true and must be false only after human-admin approval. |
| `eligible_voter_definition` | Who could vote and how duplicate voting was prevented. |
| `threshold_profile` | Versioned threshold rule used for advisory/weak/strong mandate labels. |
| `result_summary` | Counts/percentages with uncertainty and turnout context. |
| `human_admin_approval` | Approver, timestamp, rationale, and PR/review link. |
| `publication_text` | Exact language agents/pages may use when citing the result. |
| `expiry_or_review_date` | Date when the mandate must be rechecked or retired. |
| `privacy_evidence` | ROPA/DPIA/safety-report references and redaction status. |

## Safe publication wording

Allowed before a mandate registry exists:

- "This is an advisory poll result from OD's MVP process."
- "The result is a participation signal for further human review, not a binding mandate."
- "AI agents may use this as context, but human members retain political decision authority."

Disallowed unless the registry supports it:

- "OD voters mandated this policy."
- "The AI politician has democratic authority to decide this."
- "This Discord poll is binding."
- "AI agent votes changed the formal outcome."

## Implementation checklist

- [ ] Add a backend `MandateRecord` entity with `advisory_only=true` as the safe default.
- [ ] Store threshold profiles in version-controlled config; placeholder thresholds must be labeled as human-review drafts.
- [ ] Add Governance Monitor checks that block or revise mandate-bearing language when no matching registry entry exists.
- [ ] Add poll templates that display advisory-only labels in Swedish and English.
- [ ] Add tests showing MVP polls cannot become mandate-bearing without explicit human-admin approval metadata.
- [ ] Add safety-report counters for mandate-claim blocks/revisions without exposing raw Discord content or raw author IDs.
- [ ] Link registry entries to GitHub PRs/issues before public pages summarize them.

## Review gate

Before enabling live mandate-bearing language, a human reviewer must confirm:

1. The registry entry exists and is version-controlled.
2. The source poll/vote has lawful-basis, retention, DSAR, and erasure handling.
3. The threshold profile and eligible-voter definition are public enough to audit.
4. The publication text is narrowly scoped and does not overstate legitimacy.
5. AI-agent signals are separately labeled as advisory in Phase 1.
6. No Q1 runtime SOUL/constitution change, Discord live posting, public reply behavior, personal-data expansion, autonomous spending, or crypto feature is being smuggled in through this gate.
