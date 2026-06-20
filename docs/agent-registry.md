# OD Agent Registry Control Artifact (Draft)

This draft registry turns the Backend Instruction v2 politician table into a reviewable, machine-readable control artifact. The source of truth is `docs/agent-registry.json`; this page explains the gate and the intended use.

## Purpose

The registry gives Quberon 0 and Quberon 1 a shared, auditable map of:

- stable `agent_id` values,
- public/internal visibility,
- accountable human/body and operational owner,
- Discord/email/social surface status,
- canonical `SOUL.md` path,
- candidate Q1 runtime profile names,
- autonomy level,
- posting and mandate boundaries.

It supports the Backend Instruction v2 requirements for the agent registry, SOUL/Constitution version control, inter-node API contracts, and accountability evidence without enabling any live behavior by itself.

## Non-goals / safety boundary

This artifact does **not**:

- enable live Discord posting,
- grant or imply democratic mandate,
- make MVP polls binding (`advisory_only` remains the default),
- expand personal-data processing,
- enable autonomous spending,
- enable crypto/payment flows,
- write to Q1 runtime profiles,
- activate Mona Sky Levin before human-admin role and visibility review.

All public-facing AI agents must remain transparently synthetic. Internal agents, including Anna Medelvärde, Sofia Samband, and Muhammad Mandat, must not post directly to Discord; their output must be routed through an approved external agent or human review path.

## Current draft registry

| Agent ID | Display name | Visibility | Role | Runtime profile candidates | External surface | Canonical SOUL |
|---|---|---:|---|---|---|---|
| `ai-orchestrator` | AI Orchestrator | external | System Architect & Agent Coordinator | `od-coordinator` | Discord/email after safety gate | `docs/politicians/ai-orchestrator/soul.md` |
| `per-normalsson` | Per Normalsson | external | Synthetic Spokesperson for Average Voter Concerns | `per-normalsson`, `od-press` | Discord/email/social after safety gate | `docs/politicians/per-normalsson/soul.md` |
| `anna-medelvarde` | Anna Medelvärde | internal | Public Sentiment & Policy Analysis | `anna-medelvarde` | no direct external surface | `docs/politicians/anna-medelvarde/soul.md` |
| `sofia-samband` | Sofia Samband | internal | Deliberation & Connection | `sofia-samband` | no direct external surface | `docs/politicians/sofia-samband/soul.md` |
| `lars-lagrum` | Lars Lagrum | external | Legal & Governance Guard | `lars-lagrum` | Discord/email/social after safety gate | `docs/politicians/lars-lagrum/soul.md` |
| `muhammad-mandat` | Muhammad Mandat | internal | Representation & Mandate Tracker | `muhammad-mandat` | no direct external surface | `docs/politicians/muhammad-mandat/soul.md` |
| `ulv-svikensson` | Ulv Svikensson | external | Adversarial Integrity & Anti-Corruption | `ulv-svikensson` | Discord/email/social after safety gate | `docs/politicians/ulv-svikensson/soul.md` |
| `fiona-envoy` | Fiona Envoy | external | International Spokesagent & Synthetic Liaison | `fiona-envoy` | Discord/email/social after safety gate | `docs/politicians/fiona-envoy/soul.md` |
| `mona-sky-levin` | Mona Sky Levin | planned/TBD | Synthetic Intern & Clarification Agent | `mona-sky-levin` | inactive until human-admin review | `docs/politicians/mona-sky-levin/soul.md` |

## Required review gate before runtime use

Before this JSON is consumed by backend code, Q1 sync scripts, public pages, or Discord routing, a human-admin review should confirm:

1. the current Backend Instruction v2 still matches all roles and visibility flags;
2. public/internal separation is correct;
3. every external surface is still human-admin gated;
4. autonomy levels are intentionally set and documented;
5. mandate wording cannot be mistaken for democratic legitimacy;
6. the registry aligns with GDPR, EU AI Act transparency, and accountability-matrix controls;
7. Q1 runtime profile mappings are correct and reversible.

Any later change to agent identity, SOUL.md, Constitution, role, orientation, visibility, or autonomy level must happen through a GitHub PR and must not be written directly into runtime profiles without a reversible backup and hash verification.
