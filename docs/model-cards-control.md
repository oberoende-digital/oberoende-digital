# Model Cards and AI-System Documentation Control Gate

Status: draft control artifact; does not enable runtime behavior.

## Purpose

OD White Paper v2.2 commits OD to EU AI Act Article 11-style technical documentation, published model cards where possible, architecture descriptions, audit reports, and clear limits on AI-generated political communication. This document defines the minimum control gate before any OD backend, Discord workflow, public website, or Q1 politician runtime treats a model/provider/prompt stack as approved for public-facing use.

This artifact is deliberately docs-only. It creates no live posting, no personal-data expansion, no Q1 runtime write, no autonomous merge, no autonomous spending, and no crypto/payment flow.

## Source anchors

- White Paper v2.2 §1.4: risk management, data governance, technical documentation, logging, transparency, human oversight, robustness, and cybersecurity.
- White Paper v2.2 §3.1–§3.3: AI responses must be labeled; uncertainty must not be concealed; quarterly AI audit reports must include model, prompt, system architecture, data-source, accuracy, correction, and security-test changes.
- Backend Instruction v2 §2–§4: public responses must include synthetic disclosure, cite policy basis, preserve auditability, keep MVP polls advisory-only, and never claim democratic mandate without Mandate Registry support.
- Backend Instruction v2 §4.12 and §7: SOUL.md, AI Constitution, role, orientation, and autonomy changes are GitHub PR-gated.

## Minimum model card fields

Every public-facing or decision-supporting OD model stack must have a model card or provider documentation record containing at least:

| Field | Required content | Publication level |
| --- | --- | --- |
| `system_id` | Stable OD system identifier, e.g. `discord_router`, `public_spokesagent`, `q1_politician_agent` | public when system is public-facing |
| `provider` / `model` | Provider name, model family/name, deployment surface, and known version or snapshot where available | public unless it reveals a secret |
| `purpose` | Intended OD use: routing, drafting, summarization, source analysis, safety triage, or public response drafting | public |
| `not_for` | Explicit prohibited uses, including final political decisions, binding mandate claims, autonomous spending, crypto/payment authorization, and unsupervised moderation of lawful political disagreement | public |
| `synthetic_disclosure` | How users are told the output is AI-generated or AI-assisted | public |
| `human_oversight` | Accountable human/body, review gate, escalation path, and rollback owner | public |
| `data_inputs` | Input categories, data minimization rule, PII handling, lawful-basis/DPIA/ROPA references, and whether personal data is processed | public summary; sensitive operational detail internal |
| `evaluation_evidence` | Tests, red-team checks, safety-report evidence, known failure modes, and last review date | public summary |
| `prompt_and_policy_basis` | Prompt/SOUL/Constitution paths or hashes, policy/source anchors, and PR/change history | public where safe |
| `limits_and_uncertainty` | Capability limits, source limits, latency/availability risks, hallucination risk, and uncertainty language requirements | public |
| `status` | `draft`, `review`, `approved_for_dry_run`, `approved_for_public_response`, `suspended`, or `retired` | public for public-facing systems |

## Approval gates

A model stack may move from draft to any public or operational state only after these gates are satisfied:

1. **Documentation gate** — model card fields are complete enough for external scrutiny, with no hidden human impersonation or false certainty.
2. **Safety gate** — tests or dry-run evidence show synthetic disclosure, no false democratic mandate, advisory-only MVP poll language, no autonomous spending, crypto disabled in Phase 1, and no live posting unless separately approved.
3. **Privacy gate** — GDPR lawful basis, minimization, retention, subject-rights handling, and ROPA/DPIA references exist before personal-data processing expands.
4. **Human oversight gate** — accountable human/body, operational owner, emergency stop, rollback path, and incident escalation are documented.
5. **Change-control gate** — provider/model/prompt/SOUL/Constitution/role/orientation changes are committed through GitHub PRs and linked from the relevant model card.
6. **Publication gate** — public summaries omit secrets, raw private Discord content, raw author IDs, private prompts where unsafe, and any redacted-sensitive content.

## Required defaults

- Transparent AI identity is mandatory for every public-facing response and public profile.
- MVP polls are advisory-only unless a later human-admin gate upgrades them and the Mandate Registry supports the wording.
- No agent may claim democratic mandate unless the Mandate Registry records source, scope, thresholds, eligible-voter definition, expiry/review date, human-admin approval, and publication wording.
- Internal agents do not post directly to Discord; their output must flow through approved external/public surfaces or internal review.
- Model/provider failures shown to public users must be generic and safe; detailed provider errors, request/account URLs, credential IDs, stack traces, and raw HTTP bodies go only to an operator back-channel.
- Model cards do not authorize live posting, personal-data expansion, Q1 runtime writes, autonomous merges, autonomous spending, or crypto/payment flows.

## Evidence and review cadence

- Review every public-facing model card at least before each major launch gate and after any provider/model/prompt/SOUL/Constitution change.
- Link relevant safety reports, watchdog output, red-team summaries, incident records, and PRs.
- Mark stale or unverifiable provider/model stacks as `suspended` until revalidated.
- Treat missing model-card evidence as a blocker for public-facing automation, not as a reason to silently proceed.

## Non-goals for this PR

This document does not implement backend model routing, select a provider, upload SOUL files to Q1, publish a public model-card page, enable live Discord posting, enable personal-data collection, create payment/crypto flows, or merge itself autonomously.
