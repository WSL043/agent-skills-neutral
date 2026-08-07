---
name: evaluate-agent
description: "Evaluate an agent, skill, workflow, or tool-using system with explicit claims, repeatable tasks, traceable graders, and failure analysis. Use when comparing agent behavior, validating a skill, or building an evaluation loop."
---

# Evaluate Agent

## Goal

Determine whether an agent or workflow satisfies a stated behavioral claim, and make failures useful for the next change.

## Workflow

1. State the claim, task boundary, acceptance conditions, and dimensions to evaluate before inspecting candidate outputs. Define what counts as success, partial success, failure, and an indeterminate result.
2. Build a representative task set from real work, traces, known failures, and held-out cases. Use synthetic tasks only to cover a documented gap, and preserve the provenance and scope of every case.
3. Compare baseline and candidate under the same prompts, tools, permissions, environment, data, and constraints. Persist inputs, outputs, relevant traces, grader evidence, and run conditions.
4. Apply deterministic checks first. Use a model or human grader only for qualities that cannot be checked reliably otherwise, with a rubric that is independent of the candidate's preferred answer.
5. Analyze failure patterns by task, step, tool use, trajectory, grounding, instruction following, and final response as appropriate. Preserve counterexamples; do not lower the rubric or delete failures to improve a summary.
6. Re-run target failures and regression cases after a change, then report the claim's scope, evidence, uncertainty, and unresolved gaps.

## Decision rules

- Decide the acceptance rubric before seeing outputs; otherwise the evaluation is exploratory evidence, not a fixed verdict.
- Keep task success, process quality, tool behavior, and final-answer quality distinct when they can fail independently.
- Treat a score as evidence about the tested tasks and conditions, not as a universal capability claim.
- Change one evaluation or workflow variable at a time when isolating a regression.

## Guardrails

- Never fabricate scores, traces, pass rates, or missing evidence.
- Do not compare runs with different tools, context, permissions, data, or stopping conditions without labeling the confound.
- Do not promote a candidate from a polished example while ignoring representative failures or held-out cases.

## Completion evidence

- The claim, task set, baseline or no-skill comparison, grader rules, and run conditions are recorded.
- Results and failure evidence are reproducible enough to support the stated conclusion.
- The report distinguishes observed results, inference, indeterminate cases, and the next regression check.

## Related skills

- `create-agent-skill`
- `discover-agent-skills`
- `verify-completion`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
