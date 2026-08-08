# Benchmark Contract

Do not claim that a canonical change improves agent behavior merely because it is shorter, newer, or synthesized from more sources. Improvements need deployment evidence.

This document defines the comparison structure. It intentionally does not invent one universal score, pass threshold, trial count, or model requirement.

## Comparisons

For a capability under evaluation, compare whichever of these states are necessary to settle the claim:

- **no-skill baseline** — the same agent receives the task without the capability skill;
- **previous canonical** — the current or prior retained implementation;
- **raw candidate** — the candidate as authored, when its license and trust boundary allow evaluation;
- **normalized candidate** — provider-specific details removed or scoped before comparison;
- **proposed canonical** — the smallest retained synthesis after the candidate delta is applied;
- **specialized variant** — when testing whether a local optimization should remain local instead of entering the shared base.

All compared states receive the same task inputs, environment, tools, and evaluation contract unless the capability itself requires a different runtime. Any unavoidable difference is reported rather than hidden in a combined score.

## Evidence axes

Use only axes that are relevant to the capability.

### Outcome correctness

Did the deployed agent achieve the requested result and preserve the stated invariants?

Prefer deterministic checks: tests, file state, API responses, calculations, schema validation, browser assertions, citation resolution, or other executable evidence.

### Model-native activation

Did a capable agent select the right skill from the compact `name` + `description` catalog, and decline skills when none materially helped?

Evaluate activation as an agent behavior, not as a keyword-table lookup. Use realistic positive, boundary, mixed-intent, and near-miss tasks. Include cases where the relevant intent is expressed without the skill's preferred vocabulary.

The deterministic `select_skills.py` harness is a reproducible metadata diagnostic and weak-client fallback. Its `primary` suggestion is not ground truth for model-native activation. When the model and lexical harness disagree, inspect the deployed outcome before deciding which side is wrong.

A description is stronger when the model can distinguish neighboring semantic owners without loading every full skill body.

### Decision quality

For judgment-heavy skills, did the skill make materially better decisions under the same brief or evidence?

Define the rubric before viewing candidate output. Keep separate dimensions separate rather than hiding tradeoffs in one arbitrary weighted score.

### Generalization

Does the proposed canonical rule improve more than the exact task or source context that produced it?

Use held-out or deliberately contrasting cases when claiming a shared rule. If an improvement only survives on one repository, brand, framework, model family, or benchmark instance, treat it as specialization until broader evidence exists.

For a mechanism claimed to improve general agent capability, include tasks outside the source domain. Product-name removal without behavioral loss is useful evidence that a mechanism may transfer, but deployment tests still decide the claim.

### Efficiency

When it matters to the task, report context loaded, turns, tool calls, latency, or token use as evidence. Efficiency never overrides correctness or safety by itself.

For routing, compare total catalog/context cost with misrouting cost rather than minimizing selection tokens in isolation. A slightly more expensive semantic choice can be better if it avoids loading the wrong workflow.

### Safety and trust

Did the candidate introduce new privileged actions, network access, credential access, destructive behavior, hidden dependencies, prompt-injection exposure, or provider coupling?

A functional improvement that creates unresolved material risk is not eligible for promotion.

### Canonical compression

Did the retained implementation reduce duplicate triggers or redundant behavior while preserving or improving the task contract?

A candidate can be individually useful and still be rejected because the canonical library already expresses its useful behavior more cleanly.

A cross-cutting mechanism that strengthens several skills without adding another routable trigger should receive explicit credit here; canonical-count growth is not an improvement metric.

## Skill-evolution evidence

When a skill is revised from execution experience, separate three roles:

- **experience/proposal set** — diverse trajectories used to discover local lessons and propose edits;
- **held-out acceptance set** — tasks not used to author the edit and used to decide whether it survives;
- **regression set** — previously proven behavior that should remain stable.

Do not use one anecdotal failure as both diagnosis and proof. Prefer patterns across diverse successful and failed trajectories before promoting a transferable rule.

For each edit:

1. state the smallest behavioral claim;
2. link the edit to the trajectory/failure pattern that motivated it;
3. evaluate it on held-out tasks;
4. inspect material per-task regressions rather than only an aggregate score;
5. retain, narrow, or reject the edit;
6. preserve a concise rejected-edit/negative lesson only when it prevents repeated exploration of the same failed mechanism.

Incremental add/delete/replace edits are preferred when the existing structure is sound. A full rewrite requires evidence that the structure itself caused the failure, because repeated rewrites can silently erase previously useful detail.

## Fresh deployment rule

When the claim concerns how instructions change agent behavior, prefer evaluating with a fresh downstream session that did not author the candidate. This reduces self-review anchoring and detects skills that are ignored, ambiguously triggered, or misunderstood in deployment.

The authoring trace may explain why a change was proposed; it is not the proof that the deployed change works.

For model-native skill selection, the fresh downstream session should see the same compact catalog shape intended for deployment, not hidden trigger tables unavailable to the real client.

## Deterministic and judgment graders

Use deterministic graders for claims they can directly settle. Use model or human judgment for irreducibly qualitative claims.

Do not convert model-judge consistency into determinism. When graders disagree, report the disagreement or narrow the claim instead of manufacturing certainty through a global weight.

Deterministic infrastructure can verify catalog consistency, file existence, permissions, route metadata, test fixtures, and outcome checks. It should not pretend to replace semantic model judgment where the deployment mechanism is model-driven.

## Promotion decision

A candidate may be promoted when the evidence proves the contract gap it was meant to close and no material regression is introduced in affected canonical behavior.

Possible outcomes remain:

- strengthen;
- replace;
- new capability;
- architecture lesson;
- specialization only;
- reject.

A candidate is allowed to produce no canonical change. Rejection is a valid successful evaluation result.

Prefer architecture/shared-kernel or strengthen outcomes when one mechanism improves several workflows. A new canonical trigger is appropriate only when the user-facing outcome itself is materially distinct.

## Benchmark suites

Accumulate capability-specific suites rather than one artificial master benchmark. A suite may be deterministic, agent-run, rendered/visual, security-focused, routing-focused, evolution-focused, or domain-specific.

Any quality claim should point to the exact suite, source versions, agent/model/runtime, task set, and evidence used. Results from one suite do not silently become a quality ranking for unrelated skills.

For semantic routing, maintain model-run activation suites separately from deterministic lexical regression fixtures. Both are useful, but they answer different questions.

## Evaluation infrastructure

Evaluation tools are replaceable adapters around this contract. Use existing or custom harnesses when they provide relevant independent evidence, but do not import their default thresholds, weights, trial counts, or assumptions as project policy without authority.

The durable contract is: explicit behavioral claim, comparable conditions, proposal-versus-held-out separation when learning from experience, fresh deployment where relevant, semantic activation evidence for model-driven routing, and no hidden regression.
