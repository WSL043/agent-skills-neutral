---
name: simplify-code
description: "Simplify existing code while preserving its observable behavior, interfaces, and operational contracts. Use when reducing duplication, nesting, incidental complexity, or confusing structure in an existing implementation."
---

# Simplify Code

## Goal

Make existing code easier to understand and maintain without changing what callers, users, operators, or tests can observe.

## Workflow

1. Define the boundary and behavior to preserve: inputs, outputs, errors, side effects, ordering, timing assumptions, edge cases, public interfaces, and compatibility constraints. Read callers, tests, configuration, and repository conventions before editing.
2. Identify concrete complexity signals in the scoped implementation and its owned prose, such as duplicated logic, misleading names, unnecessary indirection, tangled control flow, stale implementation narration, speculative compatibility, dead surfaces, or hand-rolled machinery whose maintained dependency already fits. Separate a readability change from a semantic change.
3. Make the smallest coherent simplification. Keep abstractions that express a real domain concept, extension seam, or invariant; prefer clear names and straightforward control flow over clever compression.
4. Re-run focused tests and relevant type, build, lint, or runtime checks. Compare outputs and failure behavior where the contract is sensitive, and add a characterization check when existing behavior is not otherwise observable.
5. Inspect the final diff for scope, compatibility, and accidental behavior changes. Record what was simplified, what evidence proves preservation, and any ambiguity that remains.

## Decision rules

- Treat the current implementation, its callers, tests, and runtime configuration as evidence; do not infer that unused-looking code is safe to remove.
- Prove or reject each candidate against current consumers, ownership, lifecycle, and runtime evidence. Age, size, novelty, and apparent elegance are discovery signals, not removal criteria.
- Preserve evaluation order, error boundaries, logging or metrics that operators rely on, and security checks unless a separately approved behavior change covers them.
- Prefer local consistency with the repository over importing a new abstraction or style solely because it is shorter.
- If the only way to simplify is to change a public contract or an important side effect, stop and propose that as a separate change.

## Guardrails

- Keep the change scoped to the proven complexity and avoid opportunistic refactoring.
- A clean-slate request still requires an exact authorized deletion boundary; simplification evidence does not grant cleanup permission.
- Do not trade readable behavior for terse expressions, speculative generality, or a new dependency.
- Do not claim simplification success from a clean build alone; behavior-preservation evidence is required.

## Completion evidence

- The scoped behavior and preservation boundary are explicit.
- Focused and relevant regression checks pass, and the final diff contains no unexplained semantic change.
- Any unobservable or unverified behavior is identified rather than assumed safe.

## Related skills

- `develop-with-tdd`
- `review-code`
- `verify-completion`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
