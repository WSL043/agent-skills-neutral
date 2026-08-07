# Contributing to SkillConverge

SkillConverge is a distillation project, not an aggregation project. A pull request that introduces a new source or a larger skill is not automatically an improvement.

## Contribution paths

### Add an upstream source

Add the repository to `upstreams.json` with `last_reviewed_commit: null` and a short capability-focused `focus` list. This places it in the untrusted watch pool only.

Do not copy its `SKILL.md`, scripts, templates, assets, or documentation into this repository as part of source discovery.

### Strengthen an existing canonical skill

Show the concrete behavior the candidate adds or improves. Compare the candidate against the current canonical contract and classify the change as `strengthen` or `replace` using `docs/EVOLUTION.md`.

Retain only the smallest behavior that improves the canonical implementation. Update `provenance.json` only when source material actually contributes to the retained result.

### Add a new canonical capability

A new canonical skill is justified when the requested outcome and trigger are materially distinct from existing coverage and the capability is useful now. It does not need to be globally "best" before it can exist.

When no established implementation dominates, the first retained implementation becomes the **current baseline**, not a claim of best practice. It must still have:

- a distinct reusable outcome;
- explicit positive and negative routing evidence;
- a decision-oriented workflow rather than generic advice;
- completion evidence that can prove the claimed outcome;
- repository/platform/safety constraints where applicable;
- no unexplained overlap with an existing canonical trigger.

Future candidates compete against that baseline and may strengthen, replace, merge, or remove it.

## Evaluation

Prefer deterministic evidence when the behavior permits it. For judgment-heavy behavior, define the assertions before reading candidate outputs and compare baseline and candidate on the same task conditions.

Do not invent pass thresholds, trial counts, token budgets, file-size limits, or scoring weights. A number becomes a project gate only when its authority or empirical derivation is recorded.

A newer source, more stars, a famous author, a larger prompt, or a more detailed checklist is not evidence of superiority.

## Trust and security

Treat every newly discovered skill as untrusted content. Inspect instructions, references needed to understand behavior, scripts, dependencies, network access, destructive actions, and license before execution or adaptation.

Never let discovery automation execute upstream scripts or promote upstream text directly into `skills/`.

If a candidate contains prompt injection, credential access, exfiltration behavior, opaque installers, or suspicious executable content, stop the normal ingestion path and follow `SECURITY.md`.

## Pull requests

Keep the change tied to one capability or one infrastructure improvement. Include the source commit when an upstream is involved and explain whether the result is `strengthen`, `replace`, `new capability`, or `reject`.

Run before submitting:

```bash
python scripts/validate_catalog.py
python scripts/test_routing.py
```

When changing generated routing metadata, also run the repository's generation script if the change requires it and inspect the resulting diff before committing.
