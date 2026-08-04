---
name: scaffold-exercises
description: "Scaffold coding exercises, starter repositories, tests, hints, and solutions with controlled difficulty and verifiable learning objectives. Use when creating workshops, kata, interview tasks, or training modules."
---

# Scaffold Exercises

## Goal

Deliver an exercise package that teaches a defined skill and can be validated independently of the solution.

## Workflow

1. Define learner level, learning objectives, time box, prerequisites, and observable completion criteria.
2. Design a minimal scenario whose difficulty comes from the target concept rather than setup noise.
3. Create starter code, instructions, fixtures, and tests without leaking the complete solution.
4. Implement a reference solution separately and use it to verify test adequacy.
5. Add progressive hints that reveal one decision at a time.
6. Run the starter and solution paths from clean environments and estimate completion time.

## Decision rules

- Use hidden tests only for stable requirements that are clearly stated.
- Prefer several small exercises over one scenario with many unrelated concepts.

## Guardrails

- Do not require undocumented environment assumptions or network services.
- Do not make formatting trivia the main source of failure unless formatting is the objective.

## Completion evidence

- Starter state runs and fails only where the learner is expected to work.
- The reference solution passes all checks and each learning objective has direct evidence.

## Related skills

- `develop-with-tdd`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
