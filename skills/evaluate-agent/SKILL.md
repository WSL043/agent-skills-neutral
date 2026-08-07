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
3. Declare the intervention being evaluated, then hold constant every condition that is not intentionally part of it. If the candidate changes a prompt, model, tool set, permission, context policy, memory, orchestration strategy, or other system component, name that treatment variable explicitly and keep the remaining conditions comparable. Persist inputs, outputs, relevant traces, grader evidence, and run conditions.
4. Apply deterministic checks first. Use a model or human grader only for qualities that cannot be checked reliably otherwise, with a rubric that is independent of the candidate's preferred answer.
5. Analyze failure patterns by task, step, tool use, trajectory, grounding, instruction following, and final response as appropriate. Preserve counterexamples; do not lower the rubric or delete failures to improve a summary.
6. Re-run target failures and regression cases after a change, then report the claim's scope, evidence, uncertainty, and unresolved gaps.

## Decision rules

- Decide the acceptance rubric before seeing outputs; otherwise the evaluation is exploratory evidence, not a fixed verdict.
- Keep task success, process quality, tool behavior, and final-answer quality distinct when they can fail independently.
- Treat a score as evidence about the tested tasks and conditions, not as a universal capability claim.
- A changed condition is a confound only when it differs outside the declared intervention. When attribution to one component matters, isolate that component or narrow the conclusion accordingly.
- A bundled system change may be evaluated as a bundle, but its observed effect must not be attributed to an individual component without an isolating experiment.

## Guardrails

- Never fabricate scores, traces, pass rates, or missing evidence.
- Do not compare runs with uncontrolled differences in prompts, tools, context, permissions, data, environment, or stopping conditions without labeling the confound.
- Do not promote a candidate from a polished example while ignoring representative failures or held-out cases.

## Completion evidence

- The claim, task set, declared intervention, baseline or no-skill comparison, grader rules, and run conditions are recorded.
- Results and failure evidence are reproducible enough to support the stated conclusion.
- The report distinguishes observed results, inference, indeterminate cases, and the next regression check.

## Related skills

- `create-agent-skill`
- `discover-agent-skills`
- `verify-completion`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
