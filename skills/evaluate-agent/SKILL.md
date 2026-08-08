---
name: evaluate-agent
description: "Evaluate an agent, skill, workflow, memory/routing policy, or tool-using system with explicit claims, repeatable tasks, traceable graders, and failure analysis. Use when comparing agent behavior, validating a skill, or building an evidence-gated improvement loop."
---

# Evaluate Agent

## Goal

Determine whether an agent or externalized behavior actually satisfies a stated claim, and turn failures into evidence for the smallest useful next change without overfitting the task set, judge, or benchmark.

## Workflow

1. State the behavioral claim, task boundary, acceptance conditions, and evidence dimensions before inspecting candidate outputs. Define what would count as success, partial success, failure, and an indeterminate result.
2. Build a representative task pool from real work, diverse execution trajectories, known failures, successful counterexamples, and held-out cases. Preserve provenance and scope. Use synthetic tasks only to cover a documented gap.
3. Separate evidence roles before optimization begins: tasks/traces used to discover or edit a candidate are **proposal evidence**; held-out tasks decide whether it is accepted; regression cases protect previously proven behavior. Keep transfer cases separate when claiming cross-domain, cross-model, or cross-runtime improvement.
4. Declare the intervention being evaluated, then hold constant every condition that is not intentionally part of it. If the candidate changes a prompt, model, skill text, tool set, permission, context policy, memory/retrieval policy, routing structure, orchestration strategy, or another system component, name that treatment variable explicitly and keep remaining conditions comparable. Persist inputs, outputs, relevant traces, grader evidence, and run conditions.
5. Use an **evaluation cascade**. Apply structural and deterministic checks first. Use fresh agent execution for behavior claims. Use a model or human judge only for qualities that cannot be checked reliably otherwise, with a rubric independent of the candidate's preferred answer. Stop when decisive deterministic failure already invalidates the claim.
6. Treat the evaluator as part of the experimental system. Record material judge model/runtime, rubric, prompt/context, and aggregation changes. Before relying on a semantic judge, test it on representative known-good, known-bad, ambiguous, and adversarial/gaming cases relevant to the decision.
7. Where semantic comparison is unavoidable, prefer a fresh or independent judging context that did not author the candidate. Blind or pairwise comparison can reduce anchoring when absolute scoring is poorly calibrated, but it does not turn model judgment into deterministic truth.
8. Analyze failures and successes by task, step, tool use, trajectory, grounding, instruction following, routing/activation, memory retrieval, final response, and stopping behavior as appropriate. Separate agent defects from route defects, environment failures, tool errors, and evaluator failures before proposing an edit.
9. For an optimization/evolution loop, cluster lessons across trajectories and propose the smallest edit linked to the diagnosed pattern. Run held-out and regression cases. Retain it only when the claimed benefit survives without material regression; narrow or specialize the edit when transfer evidence is weaker than the original claim.
10. Inspect for evaluator exploitation. If a candidate improves the measured score by changing formatting, verbosity, answer shape, stopping behavior, or another superficial property without improving the underlying contract, fix the evaluator or reject the optimization rather than encoding the exploit.
11. Re-run target failures after a retained change, then report scope, evidence, uncertainty, judge limitations, transfer limits, and unresolved gaps. If improvement appears only on source-domain or proposal tasks, do not call it general capability lift.

## Decision rules

- Decide the acceptance contract before seeing candidate outputs; otherwise the result is exploratory evidence, not a fixed verdict.
- Keep proposal/evolution evidence separate from held-out acceptance evidence. Reusing the same small pool for both can optimize to examples or the evaluator rather than the real capability.
- Keep task success, process quality, tool behavior, semantic activation, memory/retrieval behavior, final-answer quality, and stopping quality distinct when they can fail independently.
- Treat a score as evidence about the tested tasks, conditions, and grader—not as a universal capability claim.
- A semantic judge is an instrument with its own error modes. Agreement with the candidate author, higher model size, or higher self-reported confidence is not calibration evidence.
- When judge disagreement would change promotion, inspect the disputed cases or use a more authoritative evaluator instead of hiding disagreement in an arbitrary weighted average or majority vote.
- For a mechanism claimed to improve general agent capability, include contrasting tasks outside the source domain and, when claiming model/runtime portability, evidence outside the proposal model/runtime. Otherwise narrow the claim.
- A changed condition is a confound only when it differs outside the declared intervention. When attribution to one component matters, isolate that component or narrow the conclusion accordingly.
- A bundled system change may be evaluated as a bundle, but its effect must not be attributed to one component without isolating evidence.
- Prefer failure-cluster and trajectory analysis over patching benchmark examples. Repeated local fixes that fail transfer are evidence of overfitting.
- Aggregate improvement cannot excuse a material regression on a protected behavior. Inspect important per-task failures and disagreement even when a summary metric improves.
- Model choice is an experimental variable. Use inexpensive workers for mechanical execution when adequate; use stronger reasoning capacity for high-impact semantic adjudication, but require evidence from either.

## Guardrails

- Never fabricate scores, traces, pass rates, judge agreement, or missing evidence.
- Do not compare runs with uncontrolled differences in prompts, tools, context, permissions, data, environment, judge conditions, or stopping conditions without labeling the difference.
- Do not promote a candidate from a polished example while ignoring representative failures or held-out cases.
- Do not let an advisory keyword router define semantic correctness for a capable model. Use it as reproducible fallback evidence and investigate disagreements.
- Do not repeatedly rewrite an agent, skill, memory policy, or evaluator without an acceptance gate; uncontrolled self-revision can erase useful behavior or weaken the test.
- Do not let an evolution procedure change its own acceptance rubric silently because the previous rubric rejects its candidate.
- Do not invent trial counts, acceptance thresholds, learning rates, score deltas, or judge quorums. Use values justified by the task, benchmark, statistical needs, or explicit owner policy.
- Do not call model-judge output objective, deterministic, or ground truth merely because several calls agree.

## Completion evidence

- The claim, task pool, declared intervention, proposal/held-out/regression roles, baseline or no-skill comparison, grader rules, and material run conditions are recorded.
- Deterministic checks and semantic judgment are clearly separated by what each can actually establish.
- A semantic judge used for promotion has at least bounded evidence that its rubric behaves sensibly on representative acceptance cases, with unresolved disagreement reported.
- Skill-routing evaluations distinguish model-native semantic activation from deterministic fallback metadata tests.
- A retained evolution edit has held-out evidence for its claimed benefit and regression evidence for behavior expected to remain stable.
- Generalization or transfer claims are no broader than the tasks, models, runtimes, and environments actually tested.
- Rejected edits or negative lessons are retained only when they materially reduce repeated failure, not as a historical archive.
- The report distinguishes observed results, inference, evaluator limitations, transfer claims, indeterminate cases, and the next evidence needed.

## Related skills

- `create-agent-skill`
- `discover-agent-skills`
- `verify-completion`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
