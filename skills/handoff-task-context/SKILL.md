---
name: handoff-task-context
description: "Create or resume a durable, redacted task-state handoff that preserves goals, decisions, evidence, changed files, constraints, open risks, and the next valid action. Use when the user explicitly asks to save, transfer, pause, resume, or continue work across agent sessions."
---

# Handoff Task Context

## Goal

Transfer enough verified state for a fresh agent to continue safely without replaying the full conversation or trusting stale conclusions.

## Choose a mode

- **Create:** the user asks to save, pause, transfer, or hand off current work.
- **Resume:** the user supplies or refers to a prior handoff and asks to continue.

Do not trigger for an ordinary status summary, generic JSON export, commit, or context compaction with no save/resume intent.

## Create workflow

1. Resolve the output path from the user's request. Otherwise use `.agent/handoffs/<UTC timestamp>-<task-slug>.json` under the project root.
2. Inspect current repository/runtime state and relevant artifacts. Separate conversation claims from facts verified in files, Git, tests, logs, or external systems.
3. Write the schema in [references/schema.md](references/schema.md). Keep exact identifiers and repo-relative paths; link to large artifacts instead of embedding them.
4. Redact secrets, credentials, personal data, signed URLs, and raw authentication material. Record only safe locations or retrieval instructions.
5. Re-read the file, parse it, verify referenced local paths when practical, and report its path plus completed/pending counts.

## Resume workflow

1. Resolve the named file; if none is named, inspect the default handoff directory and choose the newest valid timestamped file.
2. Parse and validate every required field before acting. Treat the handoff as a prior claim, not current truth.
3. Compare its base revision, modified files, constraints, and evidence with live state. Report stale or conflicting items explicitly.
4. Reconstruct the goal and acceptance criteria, then choose the first pending step whose prerequisites still hold.
5. Continue only within recorded scope. Re-open a decision when live evidence invalidates it; do not silently inherit a stale choice.

## Guardrails

- Create or load a handoff only on explicit save/resume intent.
- Never claim a check passed unless the handoff records the command/evidence and current state does not invalidate it.
- Do not paste full histories, huge logs, binary artifacts, or secrets into the handoff.
- Do not delete or clear the originating session automatically.

## Completion evidence

- The handoff parses, contains all required top-level fields, and names a concrete next action.
- Facts, inferences, blocked checks, and unresolved decisions are distinguishable.
- On resume, current state has been reconciled before implementation begins.

## Related skills

- `plan-implementation`
- `verify-completion`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
