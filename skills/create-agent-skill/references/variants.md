# Implementation variants

## Authoring core

Keep the portable core concise: standard frontmatter, a decision-oriented body, and one-level references. Treat client UI metadata as an adapter.

## Evaluation mode

For behavior-sensitive skills, run paired cases against the relevant baseline. Define assertions before reading the outputs, then revise only instructions linked to observed failures. Choose cases because they exercise distinct contracts or failure modes, not to satisfy an arbitrary sample count.

Prefer deterministic graders when workspace state, files, API behavior, calculations, or other machine-checkable outcomes can settle the claim. Use qualitative/model review only for claims that genuinely require judgment, and keep those claims separate from deterministic ones.

For judgment-heavy skills, include deliberately different inputs that should produce materially different decisions. A design skill, for example, should preserve quality across contrasting briefs without converging on one visual template.

When the skill changes downstream agent behavior rather than producing a directly checkable artifact, prefer a **fresh deployment run**: give the candidate skill to a new agent/session that did not author the change and judge the deployed result against the same assertions as the baseline. This catches silent non-activation, ambiguous guidance, and self-review anchoring that text-only inspection can miss.

Use held-out tasks or contrasting environments when claiming that an improvement belongs in a general canonical skill. A rule that improves only the task it was derived from is evidence for specialization, not yet for the shared base.

## Upstream evolution mode

When a new upstream implementation overlaps an existing canonical skill:

1. isolate the new decision rule, implementation branch, evidence pattern, or safety boundary it contributes;
2. compare the current canonical behavior and the candidate on the cases that contribution should change;
3. absorb only the smallest delta that produces the improvement;
4. rerun affected regression cases and, where behavior is agent-mediated, a fresh downstream run;
5. reject the candidate if it cannot beat the current implementation or requires provider-specific assumptions that do not survive extraction.

Do not create a parallel canonical skill merely to preserve the upstream's name or taxonomy.

## Baseline-for-a-gap mode

When a useful capability is genuinely missing, do not wait for a mythical globally optimal implementation. Build or adapt the strongest implementation the available evidence supports and make it the **current baseline** only if it already has a distinct trigger, useful decision logic, and completion evidence.

A baseline is deliberately replaceable. Record what it proves today and keep future candidates eligible to strengthen, replace, merge, or delete it. Do not create placeholders merely to make the library look complete.

## Specialization mode

Keep generalization and local optimization separate.

- the canonical skill owns rules expected to transfer across its declared domain;
- a repository-, organization-, platform-, or task-specific specialization may tune local behavior without writing those local quirks back into the canonical base;
- promote a specialized lesson only after it survives validation on cases outside the specialization target.

This allows aggressive local optimization without contaminating shared guidance.

## Security pre-accept mode

Before accepting an external skill or generated skill package, inspect the trust boundary independently of functional quality. Check instructions, scripts, dependencies, network access, credential access, destructive behavior, and hidden provider coupling. Dedicated skill supply-chain scanners may provide evidence, but a clean scan is not a security certification.

## Pressure-test mode

Test realistic ambiguity, time pressure, missing tools, tempting shortcuts, and the failure modes the skill claims to prevent. Add guardrails for demonstrated failures rather than hypothetical prose.
