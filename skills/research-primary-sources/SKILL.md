---
name: research-primary-sources
description: "Research and synthesize primary or authoritative sources while preserving version context, citations, contradictions, and fact-versus-inference boundaries. Use for defensible multi-source research, literature review, scientific hypothesis or study appraisal, or material versioned claims; not for a single replaceable tool-option lookup."
---

# Research Primary Sources

## Goal

Deliver a synthesis whose important claims are traceable to current, authoritative evidence.

If one current manual page or live `--help` result can directly settle a tool-specific fact, use that source without activating this research workflow.

## Workflow

1. Define the question, decision context, freshness requirement, jurisdictions/versions, and what would change the answer.
2. List candidate primary sources such as official documentation, specifications, source code, datasets, filings, or papers.
3. Search broadly for discovery, then open and read the sources that directly support each material claim.
4. Record source date/version, scope, exact support, contradictions, qualifying differences, and inaccessible or missing checks. Structure each material claim around evidence that supports, contradicts, qualifies, or remains missing.
5. Triangulate unstable or high-impact claims and explain any inference from multiple sources.
6. Write the answer with citations next to claims, bounded quotations, and explicit uncertainty.

For scientific hypothesis formation or study-method appraisal, read [references/scientific-evidence.md](references/scientific-evidence.md). Keep it behind this owner instead of routing scientific submodes as separate global skills.

## Decision rules

- Prefer current official material over summaries; use secondary sources mainly to find or contextualize primary evidence.
- Use source code or executable tests when documentation and implementation disagree, while noting version scope.
- Preserve counterevidence and scope differences instead of collapsing them into a single verdict; label synthesis or inference explicitly.

## Guardrails

- Do not cite a search result page as evidence.
- Do not present memory-derived or inferred facts as directly verified.
- Do not overquote or reproduce copyrighted source material.

## Completion evidence

- Each material claim has a direct source or is labeled inference.
- Dates, versions, limitations, contradictions, and blocked checks are visible.

## Related skills

- `coauthor-documents`
- `verify-completion`

## Conditional reference

Read [references/scientific-evidence.md](references/scientific-evidence.md) only when the task requires falsifiable rival hypotheses, experiment-design reasoning, or appraisal of what a scientific study can support.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
