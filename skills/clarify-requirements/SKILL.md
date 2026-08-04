---
name: clarify-requirements
description: "Clarify goals, users, constraints, edge cases, and decision tradeoffs before implementation; challenge an existing proposal when hidden ambiguity remains. Use when requirements are underspecified, conflicting, high-impact, or likely to change the solution materially."
---

# Clarify Requirements

## Goal

Reach a decision-ready brief with explicit assumptions and no unresolved branch that would materially change the implementation.

## Workflow

1. Summarize the requested outcome, affected users, current behavior, and why the change matters.
2. Separate known facts, assumptions, preferences, constraints, and open decisions.
3. Ask the smallest high-information question that changes architecture, scope, safety, or acceptance criteria.
4. Explore realistic scenarios, boundaries, failures, permissions, compatibility, and non-goals.
5. Present viable options with consequences when the answer is a product or design choice.
6. Record the selected decisions as testable acceptance criteria and note deferred questions.

## Decision rules

- Use explore mode for a new idea and challenge mode for stress-testing an existing plan.
- Proceed with a labeled reversible assumption when the missing detail has low impact; stop for choices with materially different outcomes.
- Prefer one focused question over a questionnaire dump.

## Guardrails

- Do not ask for information that can be inspected from available files or runtime state.
- Do not treat the first implementation idea as a requirement.
- Do not continue interrogation after the work is decision-ready.

## Completion evidence

- The brief states goal, actors, constraints, scenarios, acceptance criteria, non-goals, and assumptions.
- Any remaining open question is explicitly non-blocking or assigned to a decision owner.

## Related skills

- `prototype-solution`
- `plan-implementation`

## Conditional reference

Read [references/variants.md](references/variants.md) when the task depends on implementation strategy or runtime capability.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
