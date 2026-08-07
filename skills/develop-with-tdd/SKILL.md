---
name: develop-with-tdd
description: "Implement behavior through a red-green-refactor test-driven cycle with explicit failure observation and minimal production changes. Use for new behavior, bug fixes, or refactoring where executable tests can define the contract."
---

# Develop With TDD

## Goal

Deliver behavior whose contract was demonstrated by a failing test before the implementation and remains protected afterward.

## Workflow

1. Choose one externally observable behavior at a public or integration boundary and write the smallest test that expresses it in domain language.
2. Use an expected value or fixture from an independent contract, specification, known-good example, or consumer—not a value recomputed by the implementation—and confirm the focused test fails for the intended missing behavior, not setup or syntax.
3. Implement the minimum production change that makes the test pass.
4. Run the focused test, then the relevant suite; inspect failures rather than weakening assertions.
5. Refactor names and structure while keeping all tests green.
6. Repeat one behavior at a time and finish with broader regression checks.

## Decision rules

- Use integration or contract tests when the risk lies at a boundary; use unit tests for isolated rules.
- For legacy code, first add a characterization test around current behavior unless the behavior is explicitly being changed.
- If the failure lives across callers, adapters, persistence, or transport, test at the shallowest public seam that still reaches that contract rather than a private helper.

## Guardrails

- Do not write production code before observing a meaningful red test except for trivial compilation scaffolding.
- Do not mock the unit under test or assert implementation details without a concrete reason.
- Do not delete or loosen a valid failing test to obtain green.

## Completion evidence

- The test was observed failing for the intended reason and passing after the minimal change.
- Relevant regression tests pass and refactoring did not alter behavior.

## Related skills

- `diagnose-software`
- `verify-completion`

## Conditional reference

Read [references/variants.md](references/variants.md) when the task depends on implementation strategy or runtime capability.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
