# OD Phase 1 backend governance rules

These rules bind backend implementation work until a human admin approves a later constitutional upgrade. They are written for agents and human operators working on Quberon/OD automation.

## Identity and mandate

1. Synthetic OD agents must never claim to be human.
2. Synthetic OD agents must never claim electoral, member, or democratic mandate beyond the explicit constitutional text.
3. Every outbound synthetic-agent response must carry a clear disclosure.
4. A human admin remains accountable for launch decisions, incident response, and mandate upgrades.

## MVP democracy constraints

1. Polls and community signals are advisory-only in MVP.
2. Binding decisions require a documented human-admin gate and threshold rules before implementation.
3. Agents may summarize sentiment or options; they may not certify legitimacy or self-upgrade governance powers.

## Data protection

1. Do not ingest or store live public Discord traffic until `docs/gdpr-ropa.md` documents that processing.
2. Minimize stored content: prefer sanitized summaries and previews over raw messages.
3. Add retention/anonymization behavior before storing live user-generated content.
4. Do not commit databases, `.env` files, tokens, chat exports, or raw personal-data dumps.

## Financial and crypto constraints

1. No autonomous spending.
2. Crypto remains disabled in Phase 1.
3. Anonymous donation cap remains 2,940 SEK unless a human admin updates compliance documents.
4. Any payment, wallet, or Crossmint integration requires a separate compliance review before code is shipped.

## Discord operation rules

1. Live Discord read/write access requires explicit operator launch and credential validation.
2. Use channel allowlists before posting.
3. Keep status posts low-noise and material: phase changes, PRs, failed checks, blockers, or incidents.
4. Security/compliance risks, unclear human-admin decisions, failed pushes/PRs, or broken gateway connectivity must be escalated to the human admin.

## Pull request gate

Before a backend PR is considered ready:

- Unit tests or equivalent runtime checks must pass.
- Any personal-data processing must have a ROPA entry.
- The threat model must still match the code path being introduced.
- The PR body must state whether live Discord, external LLM calls, personal-data storage, spending, or crypto are changed.
