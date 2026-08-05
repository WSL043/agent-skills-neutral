---
name: plan-implementation
description: "Write an implementation plan grounded in the current repository, with concrete file changes, dependency order, tests, risks, and completion evidence. Use before multi-file features, migrations, refactors, or work that another agent or engineer must execute."
---

# Plan Implementation

## Goal

Produce an executable plan that a capable implementer can follow without rediscovering architecture or inventing requirements.

## Workflow

1. Restate the approved behavior, non-goals, constraints, and unresolved decisions.
2. Inspect relevant entry points, data flow, tests, conventions, dependencies, and recent history.
3. Choose the implementation shape and explain why it fits the current architecture.
4. Break work into dependency-ordered tracer slices, each completing a verifiable behavior across the necessary layers. Record explicit blocking edges and keep each slice small enough for one focused context.
5. Include migrations, compatibility, observability, rollout, rollback, documentation, and cleanup when relevant.
6. Review the plan for hidden decisions, oversized steps, and requirements without evidence.

## Decision rules

- Use one step per coherent behavior change, not one step per vague phase.
- Use expand-migrate-contract batches for wide mechanical changes that cannot land as one vertical slice while keeping checks green.
- Add an explicit decision checkpoint when multiple viable designs materially change scope or risk.
- Prefer incremental compatibility over flag-day migration.

## Guardrails

- Do not write a plan from issue text alone when the repository is available.
- Do not use placeholders such as 'update tests' without naming scenarios and locations.
- Do not claim file or symbol names that were not inspected.
- Do not publish issues or mutate an external tracker unless the user explicitly asked for that action.

## Completion evidence

- Every requirement maps to one or more steps and a concrete verification.
- Dependencies, risky transitions, rollback, and final acceptance are explicit.

## Related skills

- `clarify-requirements`
- `execute-plan`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
