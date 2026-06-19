# Voting and research data governance gate

Status: draft control artifact; no data collection is enabled by this document.

This gate exists before OD collects voting signals, poll metadata tied to people, research-participant records, interviews, survey exports, or other personal data that can reveal political opinions. It implements the Backend Instruction v2 requirement for GDPR, EU AI Act, auditability, advisory-only MVP polls, and human oversight before voting/research infrastructure goes live.

## Non-negotiable boundaries

- **No autonomous spending or provider purchase** is authorized by this gate.
- **Crypto remains disabled in Phase 1** and cannot be used for voting, donations, or incentives.
- **MVP polls are advisory-only** unless a future human-admin gate, mandate registry, and quantified thresholds explicitly upgrade them.
- **No democratic mandate claim** may be made from a poll, Discord reaction, survey, or research sample alone.
- **No live posting or public reply behavior** is enabled here; public Discord agents remain gated separately.
- **No political moderation of humans** beyond law, platform rules, spam, and operational safety.
- **No raw Discord content, raw author IDs, secrets, or unnecessary identifiers** may be published in public reports.
- **Transparent AI identity** is mandatory in survey/poll/research interfaces: users must know when they interact with OD AI systems.

## Data classes and default status

| Data class | Examples | Phase 1 default | Gate before use |
|---|---|---:|---|
| Anonymous public feedback | Non-identifying site feedback, public issue suggestions | allowed only if truly anonymous | publish collection text and retention note |
| Discord/user interaction metadata | channel/message IDs, hashed author references, timestamps, triage category | dry-run/minimized only | monitor safety report + redaction checks |
| Advisory poll response | option selected, poll ID, timestamp, optional pseudonymous participant ID | not enabled for personal-data-backed voting | DPIA + admin approval + deletion path |
| Political opinion profile | inferred stance, issue preference, party-support signal | blocked | explicit lawful basis, special-category assessment, human approval |
| Research participant record | consent form, interview note, contact details, compensation status | blocked | ethics review route + ROPA + DSAR path |
| Sensitive/special-category data | political opinion, health, union, ethnicity, religion, sexual orientation | blocked by default | legal review, necessity test, safeguards, explicit gate |
| Mandate registry data | verified eligibility, member/voter status, threshold evidence | future only | separate mandate-registry design + security review |

## DPIA checklist before any non-anonymous voting/research collection

1. **Purpose and necessity**
   - State the concrete research or deliberation purpose.
   - Explain why personal data is necessary and why aggregate/anonymous data is insufficient.
   - Tie the purpose to the White Paper and Backend Instruction section that authorizes the work.

2. **Lawful basis and special-category assessment**
   - Identify the GDPR Article 6 lawful basis.
   - Determine whether Article 9 special-category political-opinion data is involved.
   - If Article 9 data is involved, document the exception, safeguards, and human legal review before collection.

3. **Data minimization**
   - List each field to collect and the reason it is needed.
   - Prohibit collecting raw Discord author IDs, phone numbers, IP addresses, or free-text sensitive data unless separately justified.
   - Prefer salted pseudonymous identifiers and aggregate counters.

4. **User-facing transparency**
   - Show an AI identity disclosure before collection.
   - Explain advisory-only status, no mandate claim, purpose, retention, and how to request deletion/access.
   - Separate consent to research contact from general platform participation.

5. **Retention and deletion**
   - Define retention periods per data class.
   - Provide deletion/erasure workflow, including backups and derived aggregates.
   - Define what remains after deletion, such as non-identifying aggregate counts.

6. **Access control and audit trail**
   - Name the human accountable owner and operational owner.
   - Restrict raw records to the minimum operator set.
   - Record access, export, deletion, and schema-change events in an audit log.

7. **Security and integrity**
   - Encrypt or OS-protect local stores.
   - Validate backup handling and secret storage.
   - Run abuse-case review for coercion, vote buying, deanonymization, spam, and manipulation.

8. **Publication boundary**
   - Public reports may include only aggregated, redacted, non-identifying statistics.
   - High-priority privacy/safety alerts may cite event IDs, categories, and status only.
   - Never publish raw private Discord content, raw author IDs, contact details, or individual political profiles.

9. **Human review gate**
   - Obtain explicit human-admin approval before collection.
   - Record the PR, checklist, reviewer, approval date, and rollback/disable procedure.
   - If the purpose changes, rerun the DPIA gate.

## Records of processing seed

| Field | Draft value |
|---|---|
| Controller | Oberoende Digital / responsible human body to be confirmed |
| Operational owner | Quberon 0 backend/platform operator, under human review |
| Purpose | Advisory democratic dialogue, civic research, safety audit, and platform improvement |
| Data subjects | Discord participants, site visitors, poll respondents, research participants |
| Data categories | Minimized metadata, advisory poll choices, consent records, research notes where approved |
| Recipients | Internal authorized operators; public only receives aggregate/redacted reports |
| Transfers | None planned; document any processor/provider before use |
| Retention | Per collection notice; default short retention for raw/minimized logs and longer aggregate evidence only |
| Security | Access control, audit log, redaction, duplicate protection, backup discipline |
| DSAR/erasure | Must exist before non-anonymous collection |

## Release checklist

- [ ] DPIA completed and reviewed by a human accountable owner.
- [ ] ROPA entry completed and linked from the accountability matrix.
- [ ] User-facing notice drafted in plain language.
- [ ] Advisory-only poll and no-mandate language present.
- [ ] AI identity disclosure present.
- [ ] Data fields minimized and schema reviewed.
- [ ] Retention/deletion path tested.
- [ ] Access/export audit events tested.
- [ ] Safety report redaction checked.
- [ ] Rollback/disable switch documented.
- [ ] PR merged after review; no direct runtime change from an unreviewed branch.

## Current decision

OD should continue with aggregate, redacted, dry-run safety evidence only. Non-anonymous voting/research data collection remains blocked until this gate is completed, reviewed, and explicitly approved by a human accountable owner.
