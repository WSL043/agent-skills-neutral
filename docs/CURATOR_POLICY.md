# Curator Model Policy

The repository may use agents of different capability levels, but semantic promotion quality must not be determined by the weakest worker in the pipeline.

## Principle

Use deterministic code for facts it can settle and model judgment only where semantic abstraction is unavoidable. Spend the strongest available reasoning capacity on the small number of decisions that can change shared agent behavior across many future tasks.

Model confidence is never promotion evidence by itself. A stronger model can propose a better abstraction, but retained behavior still needs independent task evidence.

## Roles

### Worker

Workers may use inexpensive or local models, or no model at all, for mechanically checkable work:

- repository and file inventory;
- metadata extraction and normalization;
- commit and license lookup;
- deterministic diffing;
- test execution and result collection;
- trajectory collection and redaction;
- schema validation;
- catalog generation;
- applying an already-specified bounded edit;
- commit and push operations after validation.

A worker may surface anomalies, but it does not decide that a behavior is transferable merely because it can describe the source.

### Analyst

An analyst performs bounded semantic work such as:

- extracting trajectory-local lessons;
- grouping similar failures;
- identifying candidate decision rules;
- comparing a candidate with an existing canonical owner;
- identifying likely specialization or provider coupling.

Analyst output is a proposal. It is not authority to promote, merge, delete, or generalize shared behavior.

### Curator

Use a high-capability reasoning model for decisions with broad downstream impact:

- cross-source mechanism abstraction;
- deciding whether a lesson generalizes beyond its source trajectory, model, repository, benchmark, or domain;
- choosing strengthen versus replace versus merge versus specialization versus reject;
- defining the smallest behavior claim an edit is intended to improve;
- designing held-out or contrasting cases that can falsify that claim;
- resolving conflicts between multiple plausible abstractions;
- approving a new canonical semantic owner;
- removing or merging established canonical behavior;
- deciding whether a repeated failure is evidence of a missing rule, a bad route, a weak model, a broken evaluator, or an environment problem.

"High-capability" is intentionally not tied to a provider or permanent model name. Use the strongest practical reasoning model available for the decision, subject to authorization, confidentiality, and cost constraints.

### Judge

When semantic judgment is needed after candidate execution, prefer a judge that is independent from the proposal trace. Independence may mean a fresh session, a separate model, a separate prompt/context, or a human reviewer depending on the claim.

The proposer must not receive extra authority because it authored the candidate. The judge sees the declared contract and evidence, not a request to defend the proposal.

## Promotion gate

A semantic change to shared behavior should follow this shape:

```text
experience / source / trajectories
        |
        v
worker preprocessing
        |
        v
analyst local lessons
        |
        v
curator: smallest transferable claim + bounded candidate edit
        |
        v
fresh baseline and candidate executions
        |
        +--> deterministic graders where possible
        |
        +--> independent semantic judge where necessary
        |
        v
held-out / contrasting evidence
        |
        v
retain / narrow / specialize / reject
```

The curator cannot waive failed deterministic evidence. A judge cannot convert missing evidence into a pass. If evidence is mixed, narrow the claim or reject the shared edit.

## Model-strength rules

- Do not require a frontier model for deterministic work.
- Do not use a weak worker as the sole authority for cross-domain generalization or canonical promotion.
- Do not assume a larger or newer model is automatically a better judge. Evaluate judge behavior on representative adjudication cases when the choice is material.
- Do not use majority vote as a substitute for evidence. Agreement among several weak or similarly biased judges can still be wrong.
- If the available model cannot reliably resolve an important semantic conflict, leave the candidate pending rather than lowering the promotion standard.
- Record the model/runtime used for behavior-sensitive evaluation when reproducibility or later re-audit matters.

## Proposal/judge separation

For high-impact changes, separate proposal evidence from acceptance evidence:

- training or proposal trajectories may explain why an edit exists;
- held-out tasks decide whether the edit generalizes;
- previously proven regression cases protect retained behavior;
- a fresh judge evaluates irreducibly qualitative differences;
- the final decision states the scope actually demonstrated.

Do not train and validate on the same small set and call the result generalization.

## Re-audit on model progress

Canonical history is not authority. When a materially stronger reasoning model or evaluation method becomes available, it may re-audit prior abstractions for:

- accidental provider or benchmark assumptions;
- duplicated skills that can now be merged;
- overly broad rules inferred by weaker curators;
- useful mechanisms previously missed;
- obsolete guardrails that no longer change behavior;
- descriptions that weaker models needed but stronger semantic routing no longer requires.

Any resulting change still passes the normal evidence gate. A new model generation is a reason to review, not a reason to rewrite.

## Failure attribution

Before editing a skill after a failure, distinguish at least these possibilities:

- the selected skill was wrong;
- the skill description was ambiguous;
- the workflow rule was wrong or missing;
- the agent failed to follow a sufficient rule;
- the tool or environment failed;
- the evaluator was wrong or underspecified;
- the task was outside the claimed capability.

Only the failure class supported by evidence should drive the next edit. This prevents a weak run from turning into permanent prompt accumulation.

## Stop rule

Promotion is complete when the claimed improvement is demonstrated on its acceptance evidence without material regression. Do not continue editing because another model can imagine more advice.
