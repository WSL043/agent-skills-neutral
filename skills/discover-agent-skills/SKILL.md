---
name: discover-agent-skills
description: "Discover reusable Agent Skills from local catalogs or remote repositories, assess compatibility and trust, and recommend the smallest suitable set. Use when an agent needs a capability that may already exist or when comparing installable skills."
---

# Discover Agent Skills

## Goal

Find the smallest trustworthy skill set that covers the requested capability without redundant triggers.

## Workflow

1. Translate the task into capability terms, file types, tools, and completion evidence.
2. Search local manifests first, then approved registries or repositories when local coverage is insufficient.
3. Read candidate descriptions before bodies; shortlist by outcome and trigger compatibility.
4. Inspect the full candidate skill, dependencies, scripts, source history, and license before recommending installation.
5. Compare overlaps at the semantic level and select one canonical entry plus optional adapters.
6. Return the selected paths, rejected alternatives, and any unresolved compatibility checks.

## Decision rules

- Prefer a local, vendor-neutral implementation when outcomes are equivalent.
- Treat a proprietary service skill as an explicit integration, never as a generic core capability.
- Keep distinct strategies only when runtime, fidelity, or safety tradeoffs materially differ.

## Guardrails

- Do not execute code from a newly discovered skill before inspection.
- Do not install a whole repository when one or two skill directories are sufficient.
- Do not infer license permission from public visibility.

## Completion evidence

- Each recommendation names its capability, source, compatibility, trust boundary, and overlap treatment.
- The recommended set has no unexplained duplicate triggers.

## Related skills

- `create-agent-skill`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
