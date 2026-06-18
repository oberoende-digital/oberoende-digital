# Phase 2 architecture: public Q&A agent vs platform/operator agent

**Status:** implementation-ready architecture note. This document defines separation boundaries before any live public Q&A, expanded Discord permissions, or privileged operational automation is enabled.

**Safety posture:** dry-run and human-approved by default. Nothing in this design authorizes live Discord posting, public replies, personal-data collection, voting/research data collection, or privileged administrative actions without a separate explicit approval gate.

## Goals

1. Keep the public-facing Discord Q&A agent low-privilege, explainable, and reversible.
2. Keep the OD platform/operator agent privileged but non-public by default.
3. Prevent one agent from combining public persuasion powers with repository, deployment, moderation, database, or credential powers.
4. Preserve auditability, minimization, duplicate protection, and human approval for sensitive gates.

## Role model

| Role | Primary audience | Allowed purpose | Default mode |
| --- | --- | --- | --- |
| Public Q&A agent | Visitors in allowlisted public Discord channels | Answer project questions with source-grounded, AI-labelled, advisory-only text | Dry-run draft only |
| Platform/operator agent | Rasmus/operators and internal automation surfaces | Maintain repos, Kanban, safety reports, docs, watchdogs, and operational gates | Private/operator-only |
| Human approver | Rasmus or delegated operator | Approve live gates, merges, public replies, sensitive data collection, and emergency changes | Required for gated actions |

## Public Q&A agent boundary

### May do

- Read only allowlisted public channel messages needed for Q&A routing.
- Ignore bots/self, wrong channels, duplicates, and non-allowlisted surfaces.
- Classify redacted previews for category/priority/human-review flags.
- Draft responses that include synthetic-agent disclosure and advisory-only framing.
- Cite public OD pages/docs when making factual claims.
- Escalate to the operator/human when a message requests live action, personal help, moderation, legal advice, policy commitments, or new data processing.

### Must not do

- Post live replies until the public Q&A safety gate is explicitly approved.
- Read private channels, DMs, broader guild history, member lists, or role membership unless separately approved and documented.
- Store raw author IDs, raw message text, phone numbers, personnummer, or other direct identifiers in normal audit trails.
- Use repository, shell, Kanban, GitHub, gateway-admin, moderation, credential, database-migration, or deployment tools.
- Create political profiles, infer sensitive political opinions about individuals, rank people for targeting, or personalize mobilisation based on sensitive traits.
- Represent an AI draft as party mandate, legal advice, or a human decision.

## Platform/operator agent boundary

### May do

- Maintain Kanban tasks, repo branches/PRs, docs, backend tests, and safety reports.
- Run dry-run Discord monitor checks against canonical allowlists and state files.
- Inspect gateway health, target inventory, and sanitized logs needed for operations.
- Prepare approval requests with task ID, decision needed, options, recommended default, and safety impact.
- Execute emergency stop/disable actions that reduce public-facing risk when pre-authorized by policy.

### Must not do without explicit approval

- Merge PRs that require human decision.
- Enable live Discord posting or public replies.
- Expand Discord bot permissions, channel access, or data retention scope.
- Collect voting, research, participant, or political-profile data.
- Delete or moderate public content except under an explicit safety/moderation instruction and verified message/channel IDs.
- Send routine heartbeats to WhatsApp or public channels when a low-noise Kanban comment is sufficient.

## Tool and credential separation

| Capability | Public Q&A agent | Platform/operator agent | Notes |
| --- | --- | --- | --- |
| Discord read | Allowlisted channel only | Allowlisted monitor/admin checks | Public agent receives minimized events, not raw gateway power. |
| Discord write | Disabled until approved | Disabled by default; approval-gated | Live posting requires separate gate and kill switch. |
| Git/GitHub | No | Yes, private ops only | Public chat must not trigger repo writes. |
| Kanban | No direct access | Yes | Public requests become human/operator-reviewed tasks. |
| Shell/filesystem | No | Yes within canonical workdirs | Preserve unrelated dirty files and no destructive commands. |
| Databases | No raw DB | Canonical backend DB for audits/reports | Public agent only gets redacted previews. |
| Secrets/env | No | Minimal required ops env | Never expose secrets in prompts, logs, or public drafts. |
| Messaging/WhatsApp | No | Approval/blocker messages only | No routine WhatsApp noise. |

## Data-flow pattern

1. **Fetch:** monitor fetches only the allowlisted channel window.
2. **Minimize:** strip or pseudonymize author identifiers and redact direct identifiers before model-facing classification.
3. **Deduplicate:** skip already-seen message IDs; keep monitor cursor monotonic across fetched IDs, seen IDs, and previous cursor.
4. **Classify:** classify redacted previews into safety categories and human-review priority.
5. **Draft:** public Q&A agent may produce a disclosed, advisory draft only after classification permits it.
6. **Gate:** live posting stays disabled unless the relevant approval task is unblocked.
7. **Audit:** store sanitized event metadata, triage category, priority, human-review flag, and no raw sensitive content.
8. **Escalate:** high-priority or approval-needed items create an operator task/message without echoing sensitive content.

## Escalation matrix

| Trigger | Public Q&A handling | Operator handling |
| --- | --- | --- |
| Source-grounded project question | Draft disclosed answer; no live post by default | Review safety report/triage; approve only if live gate exists |
| Request for live action or binding commitment | Refuse/escalate as human decision | Ask Rasmus/blocked Kanban task |
| Personal data or personnummer | Redact, flag high priority, no content echo | Verify deletion/handling only with sanitized IDs/statuses |
| Moderation/admin request | Escalate | Human approval unless emergency policy pre-authorizes risk-reducing action |
| Voting/research/data collection | Escalate | Remain blocked pending DPIA/data-governance gate |
| Repo/deployment request | No access | Normal PR/test/approval workflow |

## Required implementation tasks

1. Define a public-agent runtime profile/toolset with no shell, GitHub, Kanban, messaging-send, gateway-admin, or DB write tools.
2. Define an operator-agent runtime profile/toolset for private ops only, with explicit workdir and canonical backend env paths.
3. Add a router contract that passes minimized Q&A events to the public agent and approval/blocker events to the operator agent.
4. Add tests proving public-agent configuration cannot access privileged toolsets.
5. Add tests proving live posting requires explicit config plus approval state.
6. Add tests proving audit payloads contain redaction markers/categories, not raw author IDs or raw sensitive content.
7. Add an emergency-stop checklist and verify it disables live posting before any live gate is considered.
8. Add operator runbook entries for PR merge gates, watchdog failures, and privacy incidents.

## Human approval gates that remain blocked

- Public Q&A live response safety gate.
- Live posting approval workflow and emergency stop activation.
- Voting/research DPIA and any collection of political profiles, voting signals, or research participant data.
- Expanded Discord permissions beyond the current allowlisted dry-run monitor.
- Any merge/close decision that is not clearly superseded by already-merged work.

## Acceptance criteria for Phase 2 implementation

- Public agent and operator agent are represented as separate profiles/configs or equivalent isolated runtime manifests.
- No public-agent path can obtain privileged tools or credentials.
- Dry-run monitor and safety report continue to pass with live posting disabled.
- Tests prove duplicate protection, monotonic cursor, privacy redaction, and disclosed/advisory output invariants.
- A human can see exactly which approval gate must be unblocked before any live public behavior starts.
