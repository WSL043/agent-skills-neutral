# Continuous Evolution

The library is a distillation layer, not an archive. Source coverage may grow without bound; the canonical skill set should grow only when a genuinely distinct reusable capability survives comparison with what already exists.

## Source discovery

Continuous evolution has three discovery paths:

1. **direct skill discovery** — find repositories that publish Agent Skills or comparable reusable instructions;
2. **source-graph discovery** — inspect repositories, papers, tools, and frameworks that tracked sources explicitly cite or build on;
3. **mechanism discovery** — study external implementations of evaluation, optimization, generation, routing, security, specialization, feedback, or learning when those mechanisms could improve this repository even if they are not user-facing skills.

Use `discover-agent-skills`, public registries, official repositories, high-quality community sources, and links found while reviewing existing upstreams to discover candidates not yet tracked. `scripts/discover_upstreams.py` extracts one-hop GitHub repository references from tracked README metadata as untrusted leads. Reputation and popularity may help prioritize inspection but never grant acceptance.

A promising direct skill source may enter `upstreams.json` with `last_reviewed_commit: null`. This means it still requires a first review; adding it to the watch pool does not mean any of its skills or claims have been accepted. The watch pool may expand freely because it does not enter normal agent context or routing.

Do not add obvious mirrors, generated spam, abandoned placeholders, or sources with no inspectable implementation merely to increase source count. External mechanism research does not need permanent source entries unless ongoing version tracking is useful.

## State

`upstreams.json` records the last commit whose relevant delta was fully reviewed for tracked skill sources. `provenance.json` records only sources that actually contributed to retained canonical skills. Upstream files are not copied merely to preserve history.

Run:

```bash
python scripts/scan_upstreams.py
python scripts/scan_upstreams.py --json
python scripts/scan_upstreams.py --repo owner/repo
python scripts/discover_upstreams.py
```

The scanners are read-only. A changed, discovered, referenced, or unreviewed source remains pending until an agent or maintainer inspects it.

## Learning from external mechanisms

Do not compare only prompts with prompts. An external implementation may contain a mechanism that improves the project without becoming a canonical skill.

Normalize useful mechanisms into project-native concepts such as:

- candidate generation;
- baseline and candidate evaluation;
- deterministic versus judgment-based grading;
- held-out or fresh-session validation;
- specialization without contaminating a shared base;
- usage-feedback collection;
- rollback and version recovery;
- source and dependency security analysis;
- trajectory/practice distillation;
- packaging and interoperability.

For each mechanism, ask separately:

1. **What transfers?** Which principle improves this repository independent of the original vendor, model, task domain, benchmark, or fixed numbers?
2. **What does not transfer?** Which part is an author preference, benchmark-specific shortcut, provider dependency, unexplained threshold, overfitting risk, or complexity that does not survive this repository's contract?

A rejected implementation can still teach a negative lesson. Retain only the normalized rule when it changes future project behavior; do not preserve rejected source prose or a named comparison ledger merely as history.

A source cited by another source becomes a new candidate, not inherited authority. Inspect it directly before using its behavior or claims.

## Ingestion loop

1. Scan only the delta after `last_reviewed_commit` when one exists; do a first relevant review when it is null.
2. Inspect each candidate's complete instructions needed to understand behavior, bundled scripts, dependencies, source history, license, privileged actions, network behavior, and provider assumptions before using it.
3. Translate the candidate into capability, trigger, decision logic, evidence, and failure modes. For infrastructure research, translate implementation details into transferable mechanisms and non-transferable assumptions. Ignore naming differences.
4. Compare it against existing canonical skills or the current project architecture before proposing a change.
5. Classify the candidate as one of:
   - **strengthen** — same outcome, but it contains a better rule, test, safety boundary, or implementation branch;
   - **replace** — it demonstrably dominates an existing implementation while preserving the existing contract;
   - **new capability** — the outcome and trigger are materially distinct and cannot be expressed cleanly by an existing skill;
   - **architecture lesson** — it improves evaluation, discovery, safety, routing, specialization, or maintenance without becoming a user-facing skill;
   - **reject** — redundant, provider-bound without reusable logic, weakly implemented, stale, unsafe, unlicensed for adaptation, or unable to beat the current baseline.
6. For a retained change, absorb only the smallest behavior or mechanism that improves the canonical implementation. Do not vendor upstream prose, scripts, assets, or process history unless the artifact itself is necessary and its license permits it.
7. Evaluate the candidate against explicit assertions before and after the change. A new canonical skill must also pass positive and negative routing tests. Do not keep a change merely because it is newer or more detailed.
8. Advance `last_reviewed_commit` only after the whole relevant delta has been classified. The reviewed commit is also rejection memory: rejected source text does not need a local archive.
9. Update provenance only for sources that materially contributed to a retained canonical implementation. Architecture-only lessons should normally be expressed directly in project rules rather than as permanent named-source notes.

## Baselines and missing domains

The project does not need to wait for a universally accepted "best implementation" before covering a real capability gap.

If a capability is distinct, useful now, and not adequately covered by a general skill, the strongest evidence-backed implementation currently available may become the **current baseline**. Baseline means the implementation to beat, not a claim that it is globally optimal.

Do not create placeholder skills for symmetry or category completeness. A baseline must already be useful and testable. Once present, future sources can strengthen, replace, merge, or delete it through the same comparison loop.

General workflow skills should absorb common process; domain modules should exist when domain knowledge materially changes safety, correctness, evidence, failure modes, or completion criteria. There is no target domain count.

## Replacement pressure

Existing skills are candidates too. A canonical skill should be simplified, merged, replaced, or removed when current evidence shows another implementation covers its useful behavior with less overlap or stronger proof. Historical status is not authority.

The same replacement pressure applies to project infrastructure. A better evaluator, router, security boundary, or discovery mechanism can replace the current one when it proves the relevant contract more reliably without importing unnecessary coupling.

## Contamination boundary

Unbounded source growth is safe only because source discovery and runtime execution are separated.

- discovered and referenced sources remain untrusted metadata;
- unreviewed sources are not routable;
- scheduled discovery does not execute candidate scripts or install candidate dependencies;
- external instructions never gain authority merely by being read or cited;
- promotion retains normalized behavior, not the source prompt as a second runtime authority;
- only canonical skills participate in normal task routing.

This architecture reduces contamination risk; it does not make malicious or low-quality input impossible. Supply-chain and prompt-injection review remain required before promotion.

## Design evolution

Design guidance has two different kinds of knowledge and they must not be mixed:

- **durable judgment** — hierarchy, proportion, rhythm, contrast, optical balance, typography, material coherence, content-form fit, interaction quality, restraint, and intentional tension;
- **dated generator fingerprints** — recurring combinations that a model family or design-generator era overproduces across unrelated briefs.

Durable judgment belongs in the core design protocol. Dated fingerprints belong in `skills/design-frontend/references/aesthetic-signals.md` and are evidence, not bans. Update or remove them when the pattern landscape changes.

A design rule is not accepted because a respected designer prefers it. Compare independent design evidence, separate shared principles from author taste, and test the result across deliberately different briefs. If different briefs still collapse to the same composition, palette logic, typography role, or motion vocabulary, the guidance is teaching another template rather than judgment.

## Stop condition

Stop an ingestion pass when every changed candidate in the reviewed delta is classified and every retained change is proven against its actual contract. Do not search for extra work merely to make the pass feel comprehensive.
