# Methodology

## Inclusion

- Standard Agent Skills directory and SKILL.md structure.
- Non-empty procedural content with a reusable outcome.
- Local tools, open file formats, open frameworks, or generic agent capabilities.
- No required proprietary model, API, SaaS, cloud resource, or client-only runtime primitive in a canonical core capability.

## Exclusion

- Provider APIs and proprietary SaaS workflows when no provider-independent decision logic survives extraction.
- Client-only tools or configuration semantics in the core workflow.
- Organization branding, internal templates, and repository-specific review processes.
- Deprecated, in-progress, placeholder, or structurally invalid skills.
- New implementations that add detail without improving behavior, evidence, safety, portability, or a genuinely distinct outcome.

## Consolidation

Physical implementations are mapped to semantic canonical skills. Equivalent workflows are merged. Different lifecycle stages become modes. Different runtimes or fidelity strategies become conditional references rather than duplicate global triggers.

A candidate is compared against the current canonical implementation, not against an empty baseline. When the existing skill already covers the outcome, absorb only the behavior that demonstrates an improvement. A new canonical entry requires a distinct reusable capability and trigger rather than a new source name or technology example.

## Continuous evolution

`upstreams.json` stores the commit boundary already reviewed for each tracked source. `scripts/scan_upstreams.py` reports only later deltas or sources that have not yet had a first review. Follow `EVOLUTION.md` for strengthen/replace/new/reject classification.

The reviewed boundary acts as rejection memory: source content that did not survive filtering is not copied into this repository. Existing canonical skills remain contestable and may be simplified, merged, replaced, or removed when stronger evidence appears.

For judgment-heavy domains such as visual design, compare multiple independent sources and separate durable principles from author taste and model-era defaults. Time-sensitive pattern observations stay in dated references rather than becoming permanent universal rules.

## Source boundary

The skill text in this repository is an original synthesis. `provenance.json` records source ideas and immutable commits only for sources that materially contributed to retained skills. Upstream code, assets, templates, and long-form instructions are intentionally not copied; consult upstream licenses before porting any of them.
