---
name: discover-agent-skills
description: "Discover reusable Agent Skills and adjacent skill-system implementations from local catalogs or remote repositories, assess compatibility and trust, and recommend the smallest suitable set or evolution candidate. Use when an agent needs a capability that may already exist or when comparing installable skills, evaluators, generators, optimizers, or related skill infrastructure."
---

# Discover Agent Skills

## Goal

Find the smallest trustworthy skill set or ecosystem mechanism that improves the requested capability without redundant triggers, vendor lock-in disguised as general guidance, or accumulation for its own sake.

## Workflow

1. Translate the task into capability, trigger, inputs, decision logic, required tools, and completion evidence.
2. Search local canonical coverage first. For library maintenance, read `upstreams.json` and use `scripts/scan_upstreams.py` so already reviewed history is not re-audited; use `scripts/discover_upstreams.py` for untracked and transitive source leads.
3. Search both direct skill implementations and adjacent routes when the gap may be in evaluation, generation, optimization, routing, security, specialization, packaging, or feedback rather than in task instructions themselves.
4. Read candidate descriptions or manifests before bodies; shortlist by outcome and mechanism compatibility rather than naming similarity. A source cited by another project is only a lead and must be inspected directly.
5. Inspect the complete candidate material needed to understand its behavior, bundled scripts, dependencies, source history, license, privileged actions, network behavior, and provider assumptions before recommending, executing, or adapting it.
6. Compare candidates with the current canonical implementation or architecture at the semantic level: what decision or mechanism is genuinely stronger, what is merely more detailed, and what conflicts with project policy or evidence.
7. Classify each candidate as strengthen, replace, new capability, architecture lesson, or reject. Prefer modifying one canonical skill or shared mechanism over installing overlapping source implementations.
8. For a retained candidate, define assertions and compare it against the relevant baseline before absorbing the smallest behavior that produces the improvement. Use fresh downstream execution or deterministic graders when they better prove the claimed effect.
9. Return selected paths or proposed canonical changes, rejected alternatives material to the user, trust/licensing boundaries, transitive sources worth direct inspection, and unresolved checks.

## Decision rules

- Prefer a local, vendor-neutral implementation when outcomes are equivalent.
- A provider-specific skill or adjacent project can still contain reusable logic; extract only the provider-independent decision rule or mechanism when doing so preserves meaning and can be validated independently.
- Keep distinct strategies only when runtime, fidelity, safety, or outcome tradeoffs materially differ.
- A new canonical skill needs a distinct outcome and trigger. New vocabulary, a new framework example, or a larger checklist is not a new capability by itself.
- An adjacent evaluator, optimizer, generator, scanner, or learning system does not need to become a user-facing skill to improve the library; architecture lessons are first-class retained outcomes.
- Treat upstream popularity, author reputation, recency, benchmark headlines, and file length as discovery signals, never as acceptance evidence.
- A missing capability may receive a useful current baseline before a globally dominant implementation exists, but never a placeholder created for catalog symmetry.

## Guardrails

- Do not execute code from a newly discovered skill or adjacent project before inspection and authorization appropriate to its effects.
- Do not install or vendor a whole repository when the retained capability or mechanism is smaller.
- Do not infer license permission from public visibility.
- Do not preserve rejected source prose locally just to remember the review; retain only a normalized lesson when it materially changes future decisions.
- Do not allow a specialist source to turn a vendor-neutral core skill into a disguised dependency on that source's product, benchmark, model, or runtime.
- Do not inherit trust transitively. If source A cites or adapts source B, inspect B independently before using B's behavior or claims.
- Do not treat a clean security scanner result as proof that a candidate is safe; scanner evidence is one layer of the promotion trust review.

## Completion evidence

- Each recommendation or retained change names its capability or mechanism, source boundary, compatibility, trust boundary, overlap treatment, and evidence of improvement.
- The recommended or canonical set has no unexplained duplicate triggers.
- Architecture lessons state what transfers and what does not transfer from the source context.
- For an upstream maintenance pass, every relevant changed candidate is classified before `last_reviewed_commit` advances.

## Related skills

- `create-agent-skill`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
