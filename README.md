# Oberoende Digital / Independent Digital

Oberoende Digital is building the world’s first Safe Autonomous Party Lab.

Safe Autonomous Party Lab for AI-assisted democratic deliberation, policy formation, transparency, and research.

This repository is the technical and governance workspace for the Oberoende Digital web platform.

Current status: pre-formal platform build. The Google Doc remains the canonical white paper source for now.

## Repository layout

- `public/` — current website monolith imported from the OD Drive folder.
- `public/assets/` — static assets.
- `docs/` — governance, platform, and research documents.
- `docs/governance/` — constitutional core and governance framework drafts.
- `docs/research/` — research protocol and publication planning drafts.

## Core principle

AI may assist, summarize, analyze, draft, critique, and audit. Democratic legitimacy remains human, auditable, contestable, and transparent.

## Local preview

```bash
cd public
python3 -m http.server 8080
```

Then open http://localhost:8080
