---
name: prototype-solution
description: "Prototype a solution to answer a specific product, design, architecture, or technical uncertainty with the smallest credible artifact. Use when learning is more valuable than production completeness."
---

# Prototype Solution

## Goal

Produce decision-grade evidence for a named uncertainty without disguising prototype shortcuts as production readiness.

## Workflow

1. State the decision, hypothesis, success threshold, time box, and what the prototype will deliberately omit.
2. Choose the lowest-fidelity artifact that can test the uncertainty: sketch, clickable flow, spike, benchmark, or thin vertical slice.
3. Use representative inputs and constraints at the risk boundary rather than polishing broad surface area.
4. Instrument or script the measurement needed to accept or reject the hypothesis.
5. Run the prototype with target users, realistic data, or the relevant runtime.
6. Summarize evidence, limitations, recommendation, and whether to discard, iterate, or productionize.

## Decision rules

- Use a visual prototype for interaction and comprehension questions; use an executable spike for feasibility, integration, or performance questions.
- Productionize only after replacing shortcuts with explicit requirements, tests, and architecture.

## Guardrails

- Do not expand scope to make the prototype look complete.
- Do not use fake data when the unknown concerns real data shape or scale.
- Do not merge prototype code into production by default.

## Completion evidence

- The result answers the original uncertainty against the stated threshold.
- Limitations and non-production shortcuts are visible.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
