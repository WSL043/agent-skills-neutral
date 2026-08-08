---
name: evaluate-scientific-evidence
description: "Evaluate scientific claims, studies, and evidence by matching conclusions to study design, measurement, bias, statistical inference, robustness, and replication. Use for paper critique, methodology validity, evidence quality, or deciding what a study actually supports."
---

# Evaluate Scientific Evidence

## Goal

Determine what conclusions a scientific study or body of evidence can support, what must be qualified, and what remains unresolved.

## Workflow

1. Freeze the claim being evaluated. Separate reported observations and results from interpretation, causal language, mechanism claims, recommendations, and generalization.
2. Identify the study design and target question: population or system, sampling, intervention or exposure, comparator, outcomes, timing, unit of observation, unit of analysis, and unit of inference.
3. Ask whether the design can identify the stated claim. For causal or mechanistic conclusions, inspect allocation or identification assumptions, confounding, selection and collider bias, reverse causation, contamination, controls, and plausible rival explanations.
4. Evaluate measurement and data handling: construct validity, reliability, calibration, masking or blinding where relevant, preprocessing, exclusions, attrition, missingness, detection limits, and whether important choices were data-dependent.
5. Evaluate statistical inference in relation to the design: estimand or target quantity, effect magnitude, uncertainty, model assumptions, multiplicity, precision or information rationale, robustness and sensitivity checks, and whether analyses were prespecified or exploratory.
6. Evaluate reproducibility, replication, external validity, population or context boundaries, and consistency or heterogeneity with relevant independent evidence.
7. Map each material conclusion to `supported`, `qualified`, `unsupported`, or `indeterminate`. Cite the exact evidence or missing information that drives the classification and state what additional evidence could change it.

## Decision rules

- Judge a claim against the design that produced it, not the prestige of the venue, author, institution, or result.
- Keep reporting completeness, internal validity, statistical precision, practical importance, reproducibility, and generalizability distinct; weakness in one does not automatically determine the others.
- Use domain-specific appraisal or risk-of-bias frameworks only when they fit the study design and are current enough for the task.
- Match criticism severity to its effect on the central conclusion. Distinguish a fatal identification problem from a limitation that merely narrows scope.
- Absence of evidence is not automatically evidence of absence, and rejection of one null or rival does not prove a preferred mechanism.
- Preserve strengths and counterevidence alongside limitations so the final assessment is proportional rather than adversarial by default.

## Guardrails

- Do not invent unreported methods, data, analyses, approvals, citations, or results.
- Do not infer causation from association without a design or explicit identification assumptions that support the causal claim.
- Do not treat statistical significance, a p-value threshold, an evidence hierarchy, or sample size alone as a verdict on scientific importance or validity.
- Do not convert an evidence appraisal into patient-specific diagnosis, treatment, dose, or other clinical action without the separate evidence and authority such advice requires.
- For confidential or unpublished material, confirm authorization and applicable review, privacy, retention, and AI-use policy before exposing it to external systems.

## Completion evidence

- Every material conclusion is bounded to the design, population or system, measurements, and evidence that actually support it.
- Major threats to validity and the strongest supported findings are both visible.
- Causal, statistical, reproducibility, and generalization limits are stated separately where they matter.
- Unresolved uncertainty and the evidence needed to reduce it are explicit.

## Related skills

- `research-primary-sources`
- `formulate-scientific-hypotheses`
- `coauthor-documents`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
