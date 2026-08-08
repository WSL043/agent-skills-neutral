---
name: evaluate-agent
description: "Evaluate an agent, skill, workflow, or tool-using system with explicit claims, repeatable tasks, traceable graders, and failure analysis. Use when comparing agent behavior, validating a skill, or building an evaluation loop."
---

# Evaluate Agent

## Goal

Determine whether an agent or workflow satisfies a stated behavioral claim, and turn failures into evidence for the smallest useful next change without overfitting the evaluation itself.

## Workflow

1. State the claim, task boundary, acceptance conditions, and dimensions to evaluate before inspecting candidate outputs. Define what counts as success, partial success, failure, and an indeterminate result.
2. Build a representative task pool from real work, diverse execution trajectories, known failures, successful counterexamples, and held-out cases. Preserve provenance and scope. Use synthetic tasks only to cover a documented gap.
3. Separate evidence roles before optimization begins: tasks or traces used to discover/edit a candidate are proposal evidence; held-out tasks decide whether the candidate is accepted. Keep additional regression cases for previously proven behavior.
4. Declare the intervention being evaluated, then hold constant every condition that is not intentionally part of it. If the candidate changes a prompt, model, tool set, permission, context policy, memory, orchestration strategy, skill text, or other system component, name that treatment variable explicitly and keep the remaining conditions comparable. Persist inputs, outputs, relevant traces, grader evidence, and run conditions.
5. Apply deterministic checks first. Use a model or human grader only for qualities that cannot be checked reliably otherwise, with a rubric independent of the candidate's preferred answer. For model-driven skill activation, evaluate semantic selection from `name` + `description` separately from any deterministic fallback router.
6. Analyze failures and successes by task, step, tool use, trajectory, grounding, instruction following, routing/activation, final response, and stopping behavior as appropriate. Extract candidate lessons from patterns across trajectories rather than turning each failure into its own rule.
7. For an optimization/evolution loop, propose the smallest edit linked to the diagnosed pattern, then run held-out and regression cases. Retain it only when the claimed improvement survives and material regressions do not appear. Keep rejected edits or negative lessons when they prevent repeated exploration of the same dead end.
8. Re-run target failures after a retained change, then report the claim's scope, evidence, uncertainty, transfer limits, and unresolved gaps. If improvement appears only on source-domain or proposal tasks, narrow the conclusion instead of calling it general agent improvement.

## Decision rules

- Decide the acceptance rubric before seeing outputs; otherwise the evaluation is exploratory evidence, not a fixed verdict.
- Keep proposal/evolution evidence separate from held-out acceptance evidence. Reusing the same small task set for both can optimize to the evaluator rather than the real capability.
- Keep task success, process quality, tool behavior, routing/activation, and final-answer quality distinct when they can fail independently.
- Treat a score as evidence about the tested tasks and conditions, not as a universal capability claim.
- For a mechanism claimed to improve general agent capability, include contrasting tasks outside the source domain or narrow the claim to the domain actually tested.
- A changed condition is a confound only when it differs outside the declared intervention. When attribution to one component matters, isolate that component or narrow the conclusion accordingly.
- A bundled system change may be evaluated as a bundle, but its observed effect must not be attributed to an individual component without an isolating experiment.
- Prefer failure-cluster and trajectory analysis over patching individual benchmark examples. Repeated local fixes that do not transfer are evidence of overfitting.
- Aggregate metrics must not hide material regressions. Inspect important per-task failures and disagreement even when an average improves.

## Guardrails

- Never fabricate scores, traces, pass rates, or missing evidence.
- Do not compare runs with uncontrolled differences in prompts, tools, context, permissions, data, environment, or stopping conditions without labeling the confound.
- Do not promote a candidate from a polished example while ignoring representative failures or held-out cases.
- Do not let an advisory keyword router define semantic correctness for a capable model. Use it as reproducible metadata evidence and investigate disagreements.
- Do not repeatedly rewrite an agent or skill without an acceptance gate; uncontrolled self-revision can erase previously useful behavior.
- Do not invent trial counts, acceptance thresholds, learning rates, or score deltas. Use values justified by the task, benchmark, statistical needs, or explicit owner policy.

## Completion evidence

- The claim, task pool, declared intervention, proposal-versus-held-out split, baseline or no-skill comparison, grader rules, and run conditions are recorded.
- Results and failure evidence are reproducible enough to support the stated conclusion.
- Skill-routing evaluations distinguish model-native semantic activation from deterministic fallback metadata tests.
- A retained evolution edit has held-out evidence for its claimed benefit and regression evidence for behavior expected to remain stable.
- Rejected edits or negative lessons are retained only when they materially reduce future repeated failure, not as a historical archive.
- The report distinguishes observed results, inference, transfer claims, indeterminate cases, and the next regression check.

## Related skills

- `create-agent-skill`
- `discover-agent-skills`
- `verify-completion`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
