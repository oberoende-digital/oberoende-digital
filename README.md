# Oberoende Digital / Independent Digital

Oberoende Digital is building a Safe Autonomous Party Lab: a public platform for AI-assisted democratic deliberation, policy formation, transparency, and civic research.

This repository is the technical and governance workspace for the Oberoende Digital web platform.

## Status

Oberoende Digital is currently a pre-formal platform build and research environment. It is not yet a formally registered political party. The Google Doc remains the canonical white paper source for now.

## Public site

Website: https://oberoendedigital.se

The public site is deployed from the `public/` directory through GitHub Pages using the workflow in `.github/workflows/deploy-pages.yml`.

## Core principle

AI may assist, summarize, analyze, draft, critique, and audit. Democratic legitimacy remains human, auditable, contestable, and transparent.

## Repository layout

- `public/` — static website published through GitHub Pages.
- `public/assets/` — public static assets.
- `docs/` — governance, platform, launch, and research documents.
- `docs/accountability-matrix.md` — draft accountability matrix for member/data protection and public AI operations.
- `docs/governance/` — constitutional core and governance framework drafts.
- `docs/research/` — research protocol and publication planning drafts when available.
- `docs/platform-roadmap.md` — public platform roadmap, safety gates, and forgotten-item watchlist.
- `docs/rag/` — source notes and metadata for the civic research/RAG work.
- `docs/financing-transparency.md` — draft financing transparency and donation-control gates.
- `docs/policy-development-backlog.md` — draft evidence-first policy backlog derived from the White Paper and platform gates.
- `docs/safety-reporting.md` — draft safety-reporting and audit-evidence gates for Discord/backend operations.
- `docs/public-correction-log.md` — draft public correction/change-log gate for website, policybase, agent-profile, safety-report, and poll updates.
- `docs/voting-research-data-governance.md` — draft DPIA/data-governance gate for voting, polls, and civic research data.
- `scripts/` — operational scripts for data, research, and community setup.
- `server/` — experimental backend services and local prototypes.

## GitHub workflow

This project uses a simple, public-facing GitHub workflow:

1. Keep `main` deployable.
2. Use descriptive branches for changes, for example `docs/readme-polish` or `feat/proposal-lab`.
3. Prefer pull requests for reviewable changes.
4. Use clear commit messages such as `docs: polish README` or `feat: add proposal workflow`.
5. Verify GitHub Pages deployment after changes to public pages.

## Contributing

Contributions should strengthen one of four areas:

- Public understanding of the Safe Autonomous Party Lab.
- Transparent governance and constitutional safeguards.
- Civic research, source libraries, and accountable data workflows.
- Practical platform features for deliberation, proposals, feedback, and auditing.

Before contributing, please check the current status of the project and keep speculative ideas clearly labeled as drafts, prompts, or research notes.

## Development

Developer-only setup notes are kept outside the public-facing README to keep the repository front page focused and professional.

See `docs/development.md` for contributor setup notes.
