---
name: migrate-test-fixtures
description: "Migrate test fixtures between formats, factories, directories, or harnesses while preserving scenario intent and failure coverage. Use for bulk fixture conversion or test-data modernization."
---

# Migrate Test Fixtures

## Goal

Convert fixtures reproducibly without weakening the behaviors the tests are meant to protect.

## Workflow

1. Inventory fixture consumers, implicit defaults, snapshots, generators, and scenario coverage.
2. Define the source-to-target mapping and identify fields or behaviors that cannot translate directly.
3. Build a deterministic converter or codemod with dry-run and narrow selection support.
4. Convert a representative slice and compare parsed semantics, not only text.
5. Migrate consumers incrementally while both formats can be validated.
6. Remove the old path only after all consumers and CI use the new fixtures.

## Decision rules

- Preserve intentionally malformed fixtures; do not normalize away the failure being tested.
- Use golden comparisons for complex serialized output and semantic assertions for unstable formatting.

## Guardrails

- Do not hand-edit large fixture sets when a repeatable converter is feasible.
- Do not delete source fixtures before conversion and consumer tests pass.

## Completion evidence

- Fixture counts and named scenarios reconcile before and after migration.
- Representative success, boundary, and malformed cases preserve expected test behavior.

## Related skills

- `verify-completion`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
