# EU AI Act conformity mapping — Phase 0 skeleton

**Project:** Oberoende Digital (OD) Quberon 0 backend  
**Version:** Phase 0 bootstrap  
**Status legend:** `green` = implemented/evidence exists, `amber` = design target documented but implementation pending, `red` = missing/blocker.  
**Primary legal source:** Regulation (EU) 2024/1689 (AI Act), especially Articles 8–15 and 50.  
**Constitutional source:** `docs/OD_whitepaper_v2_2_english_export.txt`, especially §1.4 and §3.

> Phase 0 rule: no personal-data-touching backend code should ship until its evidence path and Article 30 ROPA entry exist. This file is the first evidence map, not a legal compliance certification.

## System classification posture

OD will voluntarily apply a **high-risk-equivalent governance model** to political AI dialogue even before final legal classification is resolved. This follows White Paper v2.2 §1.4: compliance by design, verification through audit, transparent limitations, and human ratification for final political decisions.

## Article 8 — compliance with requirements

| Requirement | OD control | Evidence path | Status | Owner |
|---|---|---|---|---|
| Establish and maintain conformity evidence for the AI system lifecycle | Versioned docs, audit logs, governance checks, safety reports, PR-only changes to agent identity | `docs/ai-act-conformity.md`, `docs/governance-rules.md` (planned), `reports/safety/` | amber | Q0 backend + human admin |
| Ensure dependencies and instructions to deployers are documented | README, architecture, inter-node API contract, operator runbooks | `README.md`, `docs/architecture.md` (planned), `docs/inter-node-api.md` (planned) | amber | Q0 backend |

## Article 9 — risk management system

| Requirement | OD control | Evidence path | Status |
|---|---|---|---|
| Continuous risk management across lifecycle | Threat model, incident log, governance monitor, rate limits, autonomy promotion gates | `docs/threat-model.md` (planned), `reports/safety/`, `agents/*/CONSTITUTION.md` (planned) | amber |
| Identify and evaluate known/foreseeable risks | Initial threat scenarios: prompt injection, raids, Sybil voting, mandate laundering, hallucinations, impersonation, data exfiltration, cost DoS | Backend instruction §11; to be copied into `docs/threat-model.md` before Phase 1 code | amber |
| Test and mitigate risks before deployment | Mock-agent path, governance monitor tests, inter-node failure tests, Discord manual commands | Test suite planned; no production code yet | red |
| Post-market monitoring and incident response | Nightly reasoning review + weekly safety report cadence | `reports/safety/YYYY-WW.md` | amber |

## Article 10 — data and data governance

| Requirement | OD control | Evidence path | Status |
|---|---|---|---|
| Data governance and management practices | Data-flow inventory, lawful basis, retention, DSAR/erasure workflow | `docs/gdpr-ropa.md` | amber |
| Training/validation/test data suitability | Q0 does not train models in MVP; agent context sources must be logged and versioned | `docs/data-model.md` (planned), InterNode audit logs (planned) | amber |
| Bias/error assessment | Nightly reasoning review scores evidence use, uncertainty, conflict, and public interest; not used to silence humans | `src/reasoning/` (planned), `reports/safety/` | amber |
| Sensitive data controls | Minimize stored Discord content; special-category/political opinions handled with documented lawful basis and retention limits | `docs/gdpr-ropa.md` | amber |

## Article 11 — technical documentation

| Requirement | OD control | Evidence path | Status |
|---|---|---|---|
| System purpose and architecture documented | Modular Q0 backend docs and Q0↔Q1 API contract | `docs/architecture.md`, `docs/inter-node-api.md` (planned) | amber |
| Capabilities and limitations documented | Transparency page, AI disclosure, governance rules, model cards once provider chosen | `public/`, `docs/governance-rules.md` (planned) | amber |
| Design specifications and changes tracked | GitHub PRs; Constitution changes require 2 reviewers | `agents/*/CONSTITUTION.md`, PR history | amber |
| Validation/test logs retained | Test reports and CI output once skeleton exists | CI/test artifacts (planned) | red |

## Article 12 — record keeping / logging

| Requirement | OD control | Evidence path | Status |
|---|---|---|---|
| Automatic logging suitable for traceability | Append-only audit logs for Discord message metadata, routing, governance checks, poll events, inter-node calls | `src/db/` schema (planned), `InterNodeAuditLog` entity (planned) | amber |
| Correlation of events | Correlation IDs propagated through Discord → router → Q1 → governance → audit log | `docs/inter-node-api.md` (planned) | amber |
| Protection and retention of logs | Retention policy in ROPA; backups and 30-day snapshot policy | `docs/gdpr-ropa.md` | amber |

## Article 13 — transparency and instructions for use

| Requirement | OD control | Evidence path | Status |
|---|---|---|---|
| Users understand they interact with AI | Synthetic disclosure on first agent message in each thread; persistent Discord profile badge; `/about` command | `src/privacy/` and `src/discord/` (planned) | amber |
| Capabilities/limits disclosed | Public AI transparency page and bot `/about` command | `public/` (existing AI labels), future transparency page | amber |
| Human vs AI stance separation | Governance monitor blocks human impersonation and false official mandate | `docs/governance-rules.md` (planned) | amber |

## Article 14 — human oversight

| Requirement | OD control | Evidence path | Status |
|---|---|---|---|
| Human oversight measures proportional to risk | Agents start at autonomy Level 1; Governance Monitor approval for every post; promotion requires explicit human-admin signed registry change | `docs/andon-mapping.md` | amber |
| Ability to intervene/stop | Human admin commands for lockdown/escalation; queued messages if Q1 unreachable | Discord module/runbook (planned) | red |
| Avoid automation bias and false mandate | Mandate Registry; advisory-only polls by default; human-admin approval to upgrade mandate status | `docs/financing-compliance.md` for finance, `config/mandate.ts` planned | amber |

## Article 15 — accuracy, robustness and cybersecurity

| Requirement | OD control | Evidence path | Status |
|---|---|---|---|
| Accuracy and robustness appropriate to purpose | Cited policy basis required; uncertainty marking; nightly review of low-evidence high-confidence claims | `src/governance/` and `src/reasoning/` planned | amber |
| Resilience against manipulation | Prompt-injection controls, Constitution, governance monitor, rate limits | `docs/threat-model.md` (planned) | amber |
| Cybersecurity | Q0↔Q1 mTLS + bearer token, rate limits, audit logs; Discord permission checks | `docs/inter-node-api.md` (planned) | amber |
| Failure handling | If Q1 unreachable: queue, placeholder, retries, escalation | Inter-node module tests planned | amber |

## Article 50 — transparency obligations for synthetic interaction/content

| Requirement | OD control | Evidence path | Status |
|---|---|---|---|
| Disclose interaction with AI system | Swedish default disclosure: “Hej! Du chattar med en virtuell AI-politiker driven av Oberoende Digital. Mer info: <link>” | `src/privacy/synthetic_disclosure` planned | amber |
| Label AI-generated output | Bot profile badge and first-thread message; public profile text says openly synthetic | `agents/*/profile.md` planned; Discord profile checklist | amber |
| User-language disclosure where feasible | Swedish default, English fallback based on user message | Discord module tests planned | amber |

## Phase 0 blockers before Phase 1 code

1. Create `docs/threat-model.md` from the initial threat model before Discord code ships.
2. Create `docs/inter-node-api.md` before any Q0↔Q1 calls are implemented.
3. Create `docs/governance-rules.md` before posting agent responses.
4. Ensure every table in `docs/gdpr-ropa.md` has an owner, lawful basis, retention, and erasure behavior before storing live Discord messages/votes/donation records.
5. Add tests for at least five happy-path and three failure-path inter-node API flows before declaring MVP.
