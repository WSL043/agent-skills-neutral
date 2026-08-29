---
name: migrate-system-safely
description: "Plan or execute a reversible migration from an old API, schema, dependency, service, format, or implementation to a replacement while preserving live consumers and data. Use for deprecation, backfill, expand-contract, dual-read/write, staged cutover, or removal of a legacy path."
---

# Migrate System Safely

## Goal

Move all verified consumers and state to the replacement through reversible stages, then remove the old path only after evidence shows it is unused.

## Workflow

1. Inventory the old capability, replacement, owners, consumers, data, undocumented behavior, current usage, and operational dependencies.
2. Define parity, compatibility, integrity, performance, and removal criteria. Identify the source of truth during every phase.
3. Choose a staged pattern: adapter/strangler for behavior, expand-backfill-switch-contract for schemas, or parallel validation for risky transformations.
4. Split the migration into independently deployable slices with explicit forward, rollback, and recovery behavior.
5. Add comparison telemetry and reconciliation. Backfill in restartable, idempotent, bounded batches with checkpoints and error quarantine.
6. Move consumers or traffic gradually; verify correctness, load, lag, errors, and business outcomes at each gate.
7. Stop old writes first, prove zero required reads/traffic for a defined observation window, then remove code, data, flags, configuration, tests, and documentation in a separate step.

## Decision rules

- Add before changing and change before deleting; destructive contraction is last and isolated.
- Keep old and new application versions valid throughout rolling deployment.
- Prefer measured consumer migration over deprecation-by-announcement.
- A database `down` migration is not sufficient rollback when data has already changed; define restore or forward-repair procedures.

## Guardrails

- Do not rename/drop a live field in the same release that introduces its replacement.
- Do not dual-write without defining partial-failure, retry, ordering, and reconciliation behavior.
- Do not backfill the entire production dataset in one unbounded transaction.
- Do not remove a legacy path from repository search alone; check runtime usage and external consumers.

## Completion evidence

- Every phase has entry criteria, checks, stop/rollback conditions, and a named source of truth.
- Reconciliation shows expected parity or documents accepted differences.
- Zero required usage is observed before contraction, and cleanup leaves no active stale path.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
