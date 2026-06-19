# Quberon 1 SOUL sync audit — 2026-06-19

This audit records the first safe SSH-based comparison between Quberon 0's version-controlled OD politician SOUL files and the running Quberon 1/Mac Mini 4 Hermes profiles.

## Scope

- Source host reached: `quberon1` via SSH `BatchMode=yes`.
- Remote user/host observed: `quberon1@Quberon1`.
- Remote profiles observed: `anna-medelvarde`, `lars-lagrum`, `mona-sky-levin`, `muhammad-mandat`, `od-coordinator`, `od-press`, `per-normalsson`, `sofia-samband`, `ulv-svikensson`.
- Remote files copied for comparison only: `~/.hermes/profiles/<profile>/SOUL.md`.
- No remote files were modified.
- No raw private Discord content, author IDs, credentials, or message payloads were inspected or published.

## Result

Remote SOUL files are **not safe to blindly promote into GitHub**. The local repository versions under `docs/politicians/<agent>/soul.md` should remain the canonical public-review baseline until a human reviews the Q1 differences.

Findings:

1. Several Q1 profiles still use the default Hermes persona template instead of an OD-specific synthetic politician identity.
2. The `od-coordinator` profile uses a generic Hermes assistant persona rather than the OD AI Orchestrator role text required by Backend Instruction v2.
3. `mona-sky-levin` contains role/persona text that presents a human-like biographical intern identity. This conflicts with OD's non-negotiable AI transparency boundary unless rewritten with explicit synthetic-agent disclosure and no human-claim framing.
4. Remote `anna-medelvarde` is a shorter operational persona than the repository's current canonical SOUL draft.
5. No remote equivalent was found for `fiona-envoy` in this run.
6. `od-press` exists remotely but is not yet mapped to a canonical politician slug in Backend Instruction v2; treat it as a separate profile requiring human mapping before sync.

## Safety decision

Do **not** overwrite the repository SOUL files from Q1 automatically. The repository versions are currently safer because they include explicit:

- AI identity / synthetic-agent disclosure,
- no-human-claim boundaries,
- human democratic authority boundaries,
- mandate limitations,
- PR/change-gate language for political identity updates.

## Next gate

Create a small review PR or task to reconcile Q1 runtime profile text with the repository SOUL files, especially:

- replace default Hermes persona templates in Q1 politician profiles,
- rewrite Mona Sky Levin with transparent synthetic identity language,
- map or retire `od-press`,
- decide whether Q1 Anna's shorter operational persona should be preserved as runtime style notes or superseded by the repository SOUL.

Any upload back to Q1 should happen only after human review of the repository version-controlled SOUL files.