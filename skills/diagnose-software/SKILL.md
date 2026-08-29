---
name: diagnose-software
description: "Diagnose software failures through reproduction, evidence collection, hypothesis testing, and root-cause isolation. Use for bugs, flaky tests, performance regressions, integration failures, or unexplained runtime behavior; implement a fix only when the task authorizes changes."
---

# Diagnose Software

## Goal

Identify the root mechanism with discriminating evidence, then implement a durable fix only when the task authorizes changes.

## Workflow

1. Build a tight feedback loop that exercises the real failing path and asserts the user's exact symptom: inputs, environment, observed result, expected result, and frequency. Redact secrets before retaining commands or artifacts.
2. Reproduce the failure, then minimize the reproducer one element at a time while preserving the same symptom. Establish the last known-good boundary when possible.
3. Inspect logs, state transitions, data, timing, dependencies, and recent changes near the first divergence. Prefer evidence from the boundary where the symptom becomes observable over guesses about internals.
4. State ranked falsifiable hypotheses and the observation that would distinguish each from alternatives.
5. Run the smallest discriminating experiment; update the hypothesis from evidence rather than layering fixes.
6. If the task authorizes changes, fix the root cause, add a regression test when a correct seam exists, and verify focused plus broader behavior. Otherwise stop with the diagnosis, evidence, and the smallest justified fix recommendation.

## Decision rules

- Use instrumentation before code changes when the failing state is not observable.
- For flaky or probabilistic behavior, determinism is not required. A stable reproduction-rate shift, repeated trace pattern, statistically distinguishable signal, or other repeatable evidence can serve as the feedback loop when it is strong enough to test the causal claim.
- Label facts, inferences, and blocked checks separately.
- Treat each hypothesis, instrumentation step, adjacent anomaly, and proposed fix as a claim; pursue it only if it can explain the contract failure or invalidate current proof.
- If no sufficiently discriminating feedback loop or correct test seam exists, record that limitation and narrow the claim rather than presenting a guessed cause as proven.

## Guardrails

- Do not treat a request to diagnose, investigate, explain, or report as authorization to modify the system.
- Do not apply multiple speculative changes in one experiment.
- Do not confuse a retry, restart, or symptom suppression with a root-cause fix.
- Do not declare success from a single non-reproduction when the bug is intermittent.
- Do not continue investigating adjacent behavior once the causal chain and fix are proven unless new evidence invalidates that proof.

## Completion evidence

- The report explains the causal chain and cites the observations that falsified alternatives.
- For an authorized fix, a regression test fails before the fix and passes after it when a correct test seam exists; otherwise equivalent repeated evidence and the missing seam are recorded explicitly.
- When production state changed, broader checks show no introduced regression.

## Conditional reference

Read [references/variants.md](references/variants.md) when the task depends on implementation strategy or runtime capability.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
