# Benchmark Contract

SkillConverge should not claim that convergence improves agent behavior merely because a canonical skill is shorter, newer, or synthesized from more sources. Improvements need deployment evidence.

This document defines the comparison structure. It intentionally does not invent one universal score, pass threshold, trial count, or model requirement.

## Comparisons

For a capability under evaluation, compare whichever of these states are necessary to settle the claim:

- **no-skill baseline** — the same agent receives the task without the capability skill;
- **previous canonical** — the current or prior retained implementation;
- **raw upstream candidate** — the candidate as authored, when its license and trust boundary allow evaluation;
- **normalized candidate** — provider-specific details removed or scoped before comparison;
- **proposed canonical** — the smallest retained synthesis after the candidate delta is applied;
- **specialized variant** — when testing whether a local optimization should remain local instead of entering the shared base.

All compared states receive the same task inputs, environment, tools, and evaluation contract unless the capability itself requires a different runtime. Any unavoidable difference is reported rather than hidden in a combined score.

## Evidence axes

Use only axes that are relevant to the capability.

### Outcome correctness

Did the deployed agent achieve the requested result and preserve the stated invariants?

Prefer deterministic checks: tests, file state, API responses, calculations, schema validation, browser assertions, citation resolution, or other executable evidence.

### Trigger behavior

Did the skill activate on tasks it owns and stay out of tasks it does not own?

Use positive, boundary, and negative routing cases. Do not reward a skill for activating more often if the extra activations are overlap.

### Decision quality

For judgment-heavy skills, did the skill make materially better decisions under the same brief or evidence?

Define the rubric before viewing candidate output. Keep separate dimensions separate rather than hiding tradeoffs in one arbitrary weighted score.

### Generalization

Does the proposed canonical rule improve more than the exact task or source context that produced it?

Use held-out or deliberately contrasting cases when claiming a shared rule. If an improvement only survives on one repository, brand, framework, model family, or benchmark instance, treat it as specialization until broader evidence exists.

### Efficiency

When it matters to the task, report context loaded, turns, tool calls, latency, or token use as evidence. Efficiency never overrides correctness or safety by itself.

### Safety and trust

Did the candidate introduce new privileged actions, network access, credential access, destructive behavior, hidden dependencies, prompt-injection exposure, or provider coupling?

A functional improvement that creates unresolved material risk is not eligible for promotion.

### Canonical compression

Did the retained implementation reduce duplicate triggers or redundant behavior while preserving or improving the task contract?

This is the library-level benefit that ordinary single-skill benchmarks miss: a candidate can be individually good and still be rejected because the canonical library already expresses its useful behavior more cleanly.

## Fresh deployment rule

When the claim concerns how instructions change agent behavior, prefer evaluating with a fresh downstream session that did not author the candidate. This reduces self-review anchoring and detects skills that are ignored, ambiguously triggered, or misunderstood in deployment.

The authoring trace may explain why a change was proposed; it is not the proof that the deployed change works.

## Deterministic and model graders

Use deterministic graders for claims they can directly settle. Use model or human judgment for irreducibly qualitative claims.

Do not convert model-judge consistency into determinism. When graders disagree, report the disagreement or narrow the claim instead of manufacturing certainty through a global weight.

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

## Benchmark suites

The project should accumulate capability-specific suites rather than one artificial master benchmark. A suite may be deterministic, agent-run, rendered/visual, security-focused, or domain-specific.

A public claim such as "SkillConverge improves X" should point to the exact suite, source versions, agent/model/runtime, task set, and evidence used. Results from one suite do not silently become a quality ranking for unrelated skills.

## Comparing the project against adjacent routes

Where practical, use existing evaluators or benchmarks as independent evidence rather than rebuilding every harness. `skillgrade`, SkillEvolver/SkillsBench-style deployment evaluation, repository-grounding checks, or other tools may be adapters into this contract.

The benchmark tool is replaceable. The contract — same task conditions, explicit assertions, baseline comparison, fresh deployment where relevant, and no hidden regression — is the durable part.
