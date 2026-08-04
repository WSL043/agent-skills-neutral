---
name: design-codebase
description: "Design or improve a codebase structure by mapping responsibilities, dependency direction, module boundaries, and change pressure. Use for architecture proposals, modularization, package boundaries, or codebase-wide structural changes."
---

# Design Codebase

## Goal

Produce an architecture that localizes change, makes dependencies explicit, and can be migrated incrementally.

## Workflow

1. Map entry points, modules, data ownership, side effects, dependency cycles, and frequently co-changing files.
2. Name the concrete forces driving change: scale, team ownership, testability, deployment, latency, or product variation.
3. Define responsibilities and dependency direction before proposing folders or frameworks.
4. Compare at least two viable structures against the identified forces and current constraints.
5. Choose seams that allow incremental migration and specify compatibility boundaries.
6. Write a staged migration with tests, observability, rollback points, and explicit non-goals.

## Decision rules

- Prefer boundaries around stable business capabilities over incidental technical layers when ownership and change align that way.
- Keep a modular monolith unless independent deployment or scaling provides measured value.
- Introduce abstraction after identifying at least two real consumers or a proven volatile boundary.

## Guardrails

- Do not redesign from directory names alone; inspect runtime and change history when available.
- Do not combine migration, feature work, and broad cleanup without separable checkpoints.

## Completion evidence

- The proposal names current evidence, target boundaries, dependency rules, migration order, and risks.
- At least one thin vertical migration slice is testable before the full reorganization.

## Related skills

- `model-domain`
- `plan-implementation`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
