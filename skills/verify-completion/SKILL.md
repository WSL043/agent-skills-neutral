---
name: verify-completion
description: "Verify that claimed work is actually complete using fresh, task-relevant evidence rather than inference or stale output. Use before declaring a fix, implementation, migration, document, or deployment complete."
---

# Verify Completion

## Goal

Make the completion claim no broader than the evidence produced in the current state.

## Workflow

1. Restate the requested outcome and convert each requirement into an observable check.
2. Identify the authoritative runtime, file, interface, or external state for each claim.
3. Run the narrowest fresh checks that prove behavior, then broader regression checks proportional to risk.
4. Inspect outputs and exit codes; distinguish warnings, skipped checks, and partial success.
5. Verify side effects, cleanup, persistence, and final state where the task changes external systems.
6. Report verified facts, remaining uncertainty, and blocked checks separately.

## Decision rules

- Use rendered or runtime evidence for user-visible outcomes; static configuration is not enough.
- Repeat nondeterministic checks enough to support the reliability claim.
- Reduce the completion statement when a required check cannot run.

## Guardrails

- Do not cite an earlier run after relevant files or state changed.
- Do not treat process startup, successful build, or absence of an error as proof of end-to-end behavior.
- Do not conceal skipped checks.

## Completion evidence

- Every completion claim maps to fresh evidence and its scope.
- Required artifacts exist at the expected location and can be consumed by the intended client.
- Remaining risks and unverified conditions are stated.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
