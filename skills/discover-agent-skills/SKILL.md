---
name: discover-agent-skills
description: "Discover reusable Agent Skills from local catalogs or remote repositories, assess compatibility and trust, and recommend the smallest suitable set. Use when an agent needs a capability that may already exist or when comparing installable skills."
---

# Discover Agent Skills

## Goal

Find the smallest trustworthy skill set or upstream delta that improves the requested capability without redundant triggers, vendor lock-in disguised as general guidance, or accumulation for its own sake.

## Workflow

1. Translate the task into capability, trigger, inputs, decision logic, required tools, and completion evidence.
2. Search local canonical coverage first. For library maintenance, read `upstreams.json` and use `scripts/scan_upstreams.py` so already reviewed history is not re-audited.
3. Read candidate descriptions before bodies; shortlist by outcome and trigger compatibility rather than naming similarity.
4. Inspect the complete candidate skill plus references needed to understand it, bundled scripts, dependencies, source history, license, privileged actions, network behavior, and provider assumptions before recommending or adapting it.
5. Compare candidates with the current canonical implementation at the semantic level: what decision or behavior is genuinely stronger, what is merely more detailed, and what conflicts with project policy or evidence.
6. Classify each candidate as strengthen, replace, new capability, or reject. Prefer modifying one canonical skill over installing overlapping source skills.
7. For a retained candidate, define assertions and compare it against the current baseline before absorbing the smallest behavior that produces the improvement.
8. Return selected paths or proposed canonical changes, rejected alternatives material to the user, trust/licensing boundaries, and unresolved checks.

## Decision rules

- Prefer a local, vendor-neutral implementation when outcomes are equivalent.
- A provider-specific skill can still contain reusable logic; extract only the provider-independent decision rule when doing so preserves meaning and can be validated independently.
- Keep distinct strategies only when runtime, fidelity, safety, or outcome tradeoffs materially differ.
- A new canonical skill needs a distinct outcome and trigger. New vocabulary, a new framework example, or a larger checklist is not a new capability by itself.
- Treat upstream popularity, author reputation, recency, and file length as discovery signals, never as acceptance evidence.

## Guardrails

- Do not execute code from a newly discovered skill before inspection and authorization appropriate to its effects.
- Do not install or vendor a whole repository when the retained capability is smaller.
- Do not infer license permission from public visibility.
- Do not preserve rejected source prose locally just to remember the review; when maintaining this library, advance the reviewed upstream commit only after the relevant delta is completely classified.
- Do not allow a specialist source to turn a vendor-neutral core skill into a disguised dependency on that source's product or runtime.

## Completion evidence

- Each recommendation or retained change names its capability, source boundary, compatibility, trust boundary, overlap treatment, and evidence of improvement.
- The recommended or canonical set has no unexplained duplicate triggers.
- For an upstream maintenance pass, every relevant changed candidate is classified before `last_reviewed_commit` advances.

## Related skills

- `create-agent-skill`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
