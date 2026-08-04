---
name: orchestrate-agent-work
description: "Coordinate multiple agents or isolated work streams by decomposing tasks, controlling context, assigning disjoint scopes, and integrating verified results. Use when the runtime supports delegation and independent subtasks can materially reduce latency or context contention."
---

# Orchestrate Agent Work

## Goal

Use delegation only where task boundaries are real, then integrate results without duplicated work or hidden assumptions.

## Workflow

1. Map dependencies, shared state, write scopes, required artifacts, and the immediate critical path.
2. Keep the blocking next step local; delegate only bounded side tasks with self-contained context.
3. Assign explicit inputs, outputs, constraints, validation, and disjoint write ownership.
4. Continue non-overlapping local work while delegates run; avoid repeated status polling.
5. Review returned artifacts and evidence, resolve conflicts, and run integration-level checks.
6. Close or release delegated contexts after their results are integrated.

## Decision rules

- Use parallel-analysis mode for independent investigations with no shared mutation.
- Use sequential-implementation mode when each task depends on the previous state or requires staged review.
- Fall back to one agent when delegation support, isolation, or task boundaries are insufficient.

## Guardrails

- Do not delegate the immediate blocker and then wait idly.
- Do not assign overlapping write sets without an explicit integration owner.
- Do not leak expected answers into independent validation tasks.

## Completion evidence

- Each delegated result is traceable to its scope and validation evidence.
- The integrated state passes checks that no individual work stream could prove alone.

## Related skills

- `plan-implementation`
- `verify-completion`

## Conditional reference

Read [references/variants.md](references/variants.md) when the task depends on implementation strategy or runtime capability.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
