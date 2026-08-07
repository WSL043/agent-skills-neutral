# Implementation variants

## Authoring core

Keep the portable core concise: standard frontmatter, a decision-oriented body, and one-level references. Treat client UI metadata as an adapter.

## Evaluation mode

For behavior-sensitive skills, run paired cases against the relevant baseline. Define assertions before reading the outputs, then revise only instructions linked to observed failures. Choose cases because they exercise distinct contracts or failure modes, not to satisfy an arbitrary sample count.

For judgment-heavy skills, include deliberately different inputs that should produce materially different decisions. A design skill, for example, should preserve quality across contrasting briefs without converging on one visual template.

## Upstream evolution mode

When a new upstream implementation overlaps an existing canonical skill:

1. isolate the new decision rule, implementation branch, evidence pattern, or safety boundary it contributes;
2. compare the current canonical behavior and the candidate on the cases that contribution should change;
3. absorb only the smallest delta that produces the improvement;
4. rerun affected regression cases;
5. reject the candidate if it cannot beat the current implementation or requires provider-specific assumptions that do not survive extraction.

Do not create a parallel canonical skill merely to preserve the upstream's name or taxonomy.

## Pressure-test mode

Test realistic ambiguity, time pressure, missing tools, tempting shortcuts, and the failure modes the skill claims to prevent. Add guardrails for demonstrated failures rather than hypothetical prose.
