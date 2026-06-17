# GDPR Article 30 ROPA — Phase 0 skeleton

**Project:** Oberoende Digital Quberon 0 backend  
**Document type:** Record of Processing Activities (ROPA) skeleton under GDPR Article 30  
**Status:** Phase 0 bootstrap; requires legal/admin review before production processing  
**Controller candidate:** Oberoende Digital / Rasmus Lundqvist (to be legally confirmed)  
**Primary sources:** GDPR Articles 6, 17, 30; OD White Paper v2.2 Dataskydd/risk sections; backend instruction v2.

> This is an operational compliance map, not legal advice. Phase 1 code must not process a personal-data category unless the corresponding row below has a lawful basis, purpose, retention period, DSAR handling, erasure/anonymization behavior, and sub-processor inventory.

## Global principles

- **Data minimization:** store only what the backend needs for dialogue continuity, poll integrity, auditability, legal compliance, and safety review.
- **Purpose limitation:** do not reuse Discord/vote/donation data for marketing, model training, or unrelated analytics without a new lawful basis and explicit review.
- **Transparency:** users must be told they are interacting with AI agents and that public political dialogue may be logged/summarized.
- **Human political freedom:** reasoning scores prioritize review and policy work; they must never be used to silence lawful political views.
- **Security:** audit logs and backups require access controls; sensitive exports require human-admin handling.
- **Timezone:** operational timestamps are displayed in Europe/Stockholm; storage uses UTC.

## Processing activity register

| ID | Activity | Data subjects | Personal data categories | Purpose | GDPR Art. 6 lawful basis candidate | Retention default | Sub-processors/systems | DSAR behavior | Erasure behavior | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| ROPA-001 | Discord message intake and metadata logging | Discord users who interact with OD channels/bot | Discord user ID, username/display name, message ID, channel/thread ID, timestamps, message content where needed, language signal | Enable AI-assisted political dialogue, thread continuity, auditability, abuse/spam resilience | Legitimate interests, Art. 6(1)(f), subject to LIA; possibly explicit consent for non-public/marketing flows | Raw thread context 12 months; conversation summaries 36 months | Discord, Hermes gateway, local DB, GitHub only for approved summaries | Export messages/metadata linked to user ID | Anonymize author references and remove raw content where not overridden by political record/audit necessity | amber |
| ROPA-002 | Agent routing and governance checks | Discord users; OD operators | User message excerpt/context, routing classification, governance verdict, correlation ID | Route to appropriate virtual politician; prevent false mandate/impersonation/fabricated authority | Legitimate interests, Art. 6(1)(f) | Governance checks 36 months; incident-relevant logs up to 7 years if needed | Q0 backend, Q1 agent runtime/LLM provider (TBD) | Export classifications/verdicts tied to user/thread | Pseudonymize user identifiers while preserving audit trail when needed | amber |
| ROPA-003 | Poll creation and voting | Discord users/members/voters | Discord user ID, vote choice/ranking, poll ID, timestamp, anti-duplicate metadata | Advisory deliberation signals and future mandate tracking | Legitimate interests, Art. 6(1)(f); explicit consent may be required for membership/official votes | Votes 7 years; poll summaries public/indefinite if anonymized | Discord, local DB, GitHub exports | Export votes and poll metadata for the requester | Remove/pseudonymize voter ID if legally possible; preserve aggregate political record | amber |
| ROPA-004 | Mandate registry | Members/voters, OD admins | Vote-derived mandate status, thresholds, approval record, admin signer | Prevent mandate laundering; record when a mandate exists | Legitimate interests, Art. 6(1)(f); legal/organizational obligation depending on party status | 7 years minimum; longer for constitutional record if anonymized | Local DB, GitHub | Export requester-linked mandate/vote records | Pseudonymize personal identifiers unless legal/organizational record requires retention | amber |
| ROPA-005 | Nightly reasoning and topic review | Discord participants | Thread summaries, topic tags, argument-quality scores, evidence/conflict/novelty signals | Prioritize policy analysis and surface strong arguments without moderating humans | Legitimate interests, Art. 6(1)(f) | Conversation summaries/reviews 36 months | Local jobs, Q1/LLM provider (TBD), GitHub approved summaries | Export summaries/scores linked to requester | Remove raw attribution; keep anonymized topic-level analysis where feasible | amber |
| ROPA-006 | DSAR and erasure handling | Data subjects requesting access/erasure | Contact details, identity-verification data, request content, fulfillment log | Fulfil GDPR rights | Legal obligation, Art. 6(1)(c) | DSAR records 3 years after closure unless dispute requires longer | Email/WhatsApp/manual files/local DB | The request itself is part of export | Delete request data after retention period; keep minimal legal proof if needed | amber |
| ROPA-007 | Donations, membership payments, financing records | Donors, members, payers | Name/contact if supplied, payment IDs, amount, date, donation category, KYC status where required, wallet/account IDs | Legal financing transparency, bookkeeping, anonymous donation cap enforcement | Legal obligation Art. 6(1)(c); contract Art. 6(1)(b) for membership payments | 7 years per Swedish bookkeeping/financing record practice unless counsel says longer | Crossmint/fiat provider, bank/payment processor, local DB, Kammarkollegiet reports | Export requester-linked payment/identity records | Erasure limited by legal obligation; restrict/pseudonymize where possible | amber |
| ROPA-008 | Email/contact correspondence | People contacting OD | Email address, name/signature, message content, attachments | Respond to inquiries, legal/admin communications | Legitimate interests Art. 6(1)(f); consent Art. 6(1)(a) for marketing-style outreach | 36 months default; legal/finance correspondence 7 years | Email provider, local archive | Export messages linked to requester | Delete/anonymize when no overriding record-keeping need | amber |
| ROPA-009 | GitHub issue/PR sync | Contributors, admins, users quoted in summaries | GitHub usernames, issue/PR text, approved summaries, report authorship | Version-controlled political and technical development | Legitimate interests Art. 6(1)(f) | Public repo records indefinite; private repo per project retention | GitHub | Export GitHub-linked records where OD controls them | Avoid publishing raw personal data; redact before public issue/PR; deletion may require GitHub admin action | amber |
| ROPA-010 | Safety reports and incident logs | Discord users, agents/operators, admins | Aggregated counts, incident descriptions, blocked response references, autonomy changes | Audit, risk management, AI Act evidence, public accountability | Legitimate interests Art. 6(1)(f); legal obligation if applicable | Public/anonymized reports indefinite; raw incident data 7 years if material | Local DB, GitHub, public website after redaction | Export requester-linked raw incident references | Redact/anonymize personal identifiers in public reports; raw erasure assessed case-by-case | amber |

## GDPR Article 17 erasure logic

1. Receive erasure request through DSAR endpoint or manual admin intake.
2. Verify the requester controls the relevant Discord/payment/email identity without collecting excessive identity data.
3. Locate records by Discord ID, payment/customer ID, email, GitHub username, and free-text aliases where appropriate.
4. Classify each record:
   - **Erase:** no longer necessary, consent withdrawn, no overriding basis.
   - **Anonymize/pseudonymize:** political record/audit value remains but identity is not needed.
   - **Restrict/retain:** legal obligation, financing/bookkeeping, dispute, security incident, or public-interest political record requires retention.
5. Produce a response within 30 days, including what was erased, anonymized, retained, and why.
6. Log the DSAR outcome without retaining unnecessary identity documents.

## Sub-processor inventory to complete before production

| Processor | Role | Data categories | DPA/status | Transfer notes | Status |
|---|---|---|---|---|---|
| Discord | Message transport/community platform | IDs, usernames, content, metadata | To review | Discord terms + regional processing must be reviewed | red |
| GitHub | Version control/issues/pages | PR/issue authors, summaries, reports | To review | Public/private repo publication risk | red |
| Crossmint/payment provider | Wallet/payments | payment/identity/KYC/payment metadata | To review | Read-only MVP; no autonomous spending | red |
| LLM provider/Q1 runtime | Agent response generation/reasoning | message context, summaries, policy context | To review | Avoid sending unnecessary personal data; no training without lawful basis | red |
| Hermes gateway/local Mac | Operational processing | all operational data | Internal/operator controlled | Local security/backups required | amber |

## Phase 1 implementation gates

- Add database entities: `PrivacyRecord`, `DSARRequest`, and per-entity retention metadata.
- Add retention configuration and documented purge/anonymization job before storing raw Discord content.
- Add `/about` transparency text and privacy link before first public bot use.
- Add an admin-only DSAR export path, even if manual fulfillment remains acceptable in MVP.
- Confirm controller identity, contact address, and DPA/sub-processor positions with human admin/legal review.
