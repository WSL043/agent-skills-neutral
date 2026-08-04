---
name: execute-plan
description: "Execute an approved implementation plan in bounded batches while preserving scope, validating each step, and reporting deviations. Use when a written plan already defines the intended change and the task is to carry it out."
---

# Execute Plan

## Goal

Complete the approved plan with traceable evidence and controlled handling of newly discovered work.

## Workflow

1. Read the complete plan, repository guidance, current status, and dependencies before editing.
2. Check that plan assumptions still match the current code and record any pre-existing failures.
3. Execute the next coherent batch in dependency order, keeping changes inside stated scope.
4. Run the verification attached to each step and inspect the resulting diff.
5. Update plan status and report deviations, blockers, or newly discovered decisions before expanding scope.
6. Finish with end-to-end checks and a requirement-to-evidence summary.

## Decision rules

- Continue through mechanical deviations that preserve intent; stop for choices that alter architecture, behavior, risk, or external state.
- Split oversized steps when they cannot be reviewed or verified independently.

## Guardrails

- Do not reinterpret an approved requirement silently.
- Do not mark a step complete before its stated evidence exists.
- Do not include opportunistic refactors that obscure the planned diff.

## Completion evidence

- Every plan item is completed, explicitly deferred, or blocked with a reason.
- Required checks ran against the final state and the final diff matches the plan scope.

## Related skills

- `plan-implementation`
- `verify-completion`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
