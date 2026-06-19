# OD financing transparency and donation gates

Status: draft implementation/control artifact. This is not a fundraising launch page and does not enable payments.

## Purpose

Oberoende Digital's financing must be open, auditable, and compatible with Swedish party-financing law before any collection or public fundraising workflow is enabled. This document translates the White Paper and Backend Instruction constraints into concrete Phase 1 gates.

## Non-negotiable boundaries

1. **No autonomous spending.** AI agents may draft, reconcile, audit, and flag financial information, but they may not approve spending, enter contracts, move funds, or execute payments.
2. **Crypto disabled in Phase 1.** Crypto or wallet integrations, including read-only Crossmint-style experiments, remain disabled unless a human-admin PR explicitly upgrades the phase and documents legal/accounting treatment.
3. **Open audit trail.** Donation and spending summaries must be published in a form that voters, journalists, auditors, and members can inspect.
4. **Anonymous donation ceiling.** Anonymous donations must never exceed the Swedish disclosure/legal ceiling referenced by Backend Instruction v2: **2,940 SEK**. The implementation must reject or hold anything above that ceiling until identity and legal handling are resolved by humans.
5. **Personal-data minimization.** Donor/member personal data is not collected until the lawful basis, retention schedule, ROPA entry, DSAR/erasure workflow, and access controls are approved.
6. **No mandate purchase.** Donations do not create democratic mandate, voting weight, priority access, or privileged influence over OD policy.

## Required evidence before enabling donations

| Gate | Required artifact | Owner | Status |
| --- | --- | --- | --- |
| Legal classification | Swedish party-financing and accounting review, including anonymous-donation handling | Human legal/accounting reviewer | Not started |
| Data protection | ROPA row, retention schedule, DSAR/erasure path, DPIA if personal-data risk expands | Human data-protection owner + Q0 backend | Not started |
| Public disclosure design | Public finance page template showing totals, ranges where needed, and review status | Q0 platform + human reviewer | Not started |
| Payment-provider risk | Provider terms, chargeback/fraud process, export format, and reconciliation path | Human finance owner | Not started |
| Security controls | Secrets handling, webhook signature verification, least-privilege operator access | Q0 backend | Not started |
| Spending control | Human approval matrix for every outgoing payment category | Human finance owner | Not started |

## Backend implementation checklist

Before any live donation or payment endpoint is merged:

- [ ] Add a configuration flag that defaults to `donations_enabled=false`.
- [ ] Reject or hold anonymous donations over **2,940 SEK** with a sanitized audit event and no public exposure of personal details.
- [ ] Store only the minimum fields required for accounting and legal compliance.
- [ ] Record immutable audit events for received, held, refunded, reconciled, and published states.
- [ ] Keep raw provider payloads out of public logs and model context.
- [ ] Provide an export for human accounting review.
- [ ] Publish aggregate public finance summaries only after human approval.
- [ ] Add tests for disabled-by-default behavior, anonymous-ceiling enforcement, redaction, refund/hold paths, and audit-report counters.

## Public communication rules

OD may say that it is designing transparent financing. It must not imply that:

- donations are already enabled if they are not;
- crypto funding is operational in Phase 1;
- AI agents can spend or financially bind the organization;
- donors receive political influence or democratic mandate;
- compliance is complete before legal/accounting review has occurred.

## Next implementation increment

A safe next PR after this document is reviewed is a disabled-by-default backend skeleton for donation audit events and finance safety reports: no payment provider credentials, no live webhooks, no public donor data, and no money movement.
