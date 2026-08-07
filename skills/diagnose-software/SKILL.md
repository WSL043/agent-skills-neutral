---
name: diagnose-software
description: "Diagnose software failures through reproduction, evidence collection, hypothesis testing, root-cause isolation, and regression verification. Use for bugs, flaky tests, performance regressions, integration failures, or unexplained runtime behavior."
---

# Diagnose Software

## Goal

Identify the root mechanism with discriminating evidence before implementing a durable fix.

## Workflow

1. Reproduce the failure with exact inputs, environment, observed result, expected result, and frequency.
2. Minimize the reproducer while preserving the failure and establish the last known-good boundary when possible.
3. Inspect logs, state transitions, data, timing, dependencies, and recent changes near the first divergence.
4. State one falsifiable hypothesis and the observation that would distinguish it from alternatives.
5. Run the smallest discriminating experiment; update the hypothesis from evidence rather than layering fixes.
6. Fix the root cause, add a regression test, and verify focused plus broader behavior.

## Decision rules

- Use instrumentation before code changes when the failing state is not observable.
- For flaky behavior, measure timing, concurrency, shared state, retries, and environmental variance across repeated runs.
- Label facts, inferences, and blocked checks separately.
- Treat each hypothesis, instrumentation step, adjacent anomaly, and proposed fix as a claim; pursue it only if it can explain the contract failure or invalidate current proof.

## Guardrails

- Do not apply multiple speculative changes in one experiment.
- Do not confuse a retry, restart, or symptom suppression with a root-cause fix.
- Do not declare success from a single non-reproduction when the bug is intermittent.
- Do not continue investigating adjacent behavior once the causal chain and fix are proven unless new evidence invalidates that proof.

## Completion evidence

- The report explains the causal chain and cites the observations that falsified alternatives.
- A regression test fails before the fix and passes after it, or equivalent repeated evidence is recorded.
- Broader checks show no introduced regression.

## Related skills

- `develop-with-tdd`
- `verify-completion`

## Conditional reference

Read [references/variants.md](references/variants.md) when the task depends on implementation strategy or runtime capability.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
