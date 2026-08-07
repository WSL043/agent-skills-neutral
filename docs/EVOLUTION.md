# Continuous Evolution

The library is a distillation layer, not an archive. Upstream coverage may grow without bound; the canonical skill set should grow only when a genuinely distinct reusable capability survives comparison with what already exists.

## Source discovery

Continuous evolution has three discovery loops:

1. **direct skill discovery** — find repositories that publish Agent Skills or comparable reusable instructions;
2. **transitive source discovery** — inspect the repositories, papers, tools, and frameworks that tracked sources explicitly cite or build on;
3. **adjacent-route discovery** — study systems that solve a neighboring problem such as skill evaluation, optimization, generation, trajectory learning, supply-chain security, routing, or specialization even when they are not themselves a skill library.

Use `discover-agent-skills`, GitHub/Agent Skills registries, official vendor skill repositories, high-quality community repositories, and source links found while reviewing existing upstreams to discover repositories not yet tracked. `scripts/discover_upstreams.py` also extracts one-hop GitHub repository references from tracked READMEs as untrusted transitive candidates. Reputation and popularity may help prioritize inspection but never grant acceptance.

A promising new repository enters `upstreams.json` with `last_reviewed_commit: null`. This means it still requires a first review; adding it to the watch pool does not mean any of its skills or claims have been accepted. The watch pool may expand freely because it does not enter normal agent context or routing.

Do not add obvious mirrors, generated spam, abandoned placeholders, or repositories with no inspectable implementation merely to increase source count. An adjacent project without `SKILL.md` is still admissible when its evaluation, optimization, security, or learning mechanism could improve this project's architecture.

## State

`upstreams.json` records the last commit whose relevant delta was fully reviewed for each tracked repository. `provenance.json` records only sources that actually contributed to retained canonical skills. Upstream files are not copied merely to preserve history.

Run:

```bash
python scripts/scan_upstreams.py
python scripts/scan_upstreams.py --json
python scripts/scan_upstreams.py --repo owner/repo
python scripts/discover_upstreams.py
```

The scanners are read-only. A changed, discovered, transitive, or unreviewed repository remains pending until an agent or maintainer inspects it.

## Adjacent-route learning

Do not compare only prompts with prompts. A neighboring system may contain a mechanism that is more valuable than any individual `SKILL.md` it ships.

Normalize adjacent projects into mechanisms such as:

- candidate generation;
- baseline and candidate evaluation;
- deterministic versus model-based grading;
- held-out or fresh-session validation;
- specialization without contaminating a shared base;
- usage-feedback collection;
- rollback and version recovery;
- source and dependency security analysis;
- trajectory/practice distillation;
- packaging and interoperability.

For each mechanism, ask two separate questions:

1. **What transfers?** Which principle improves SkillConverge independent of the original vendor, model, task domain, or fixed numbers?
2. **What does not transfer?** Which part is an author preference, benchmark-specific shortcut, provider dependency, unexplained threshold, overfitting risk, or complexity that does not survive this repository's contract?

A rejected implementation can still teach a negative lesson. Preserve the normalized lesson when it changes future decisions; do not preserve rejected source prose merely as history. See `docs/ADJACENT_ROUTES.md` for the current comparison ledger.

References cited by adjacent projects are new candidates, not inherited authority. A project that says it built on another project gives us a reason to inspect that source directly, not a reason to trust either one.

## Ingestion loop

1. Scan only the delta after `last_reviewed_commit` when one exists; do a first relevant review when it is null.
2. Inspect each changed candidate's complete instructions, references needed to understand its behavior, bundled scripts, dependencies, license, and trust boundary before using it.
3. Translate the candidate into capability, trigger, decision logic, evidence, and failure modes. For adjacent projects, translate architecture into transferable mechanisms and non-transferable assumptions. Ignore naming differences.
4. Compare it against existing canonical skills or the current project architecture before proposing a change.
5. Classify the candidate as one of:
   - **strengthen** — same outcome, but it contains a better rule, test, safety boundary, or implementation branch;
   - **replace** — it demonstrably dominates an existing implementation while preserving the existing contract;
   - **new capability** — the outcome and trigger are materially distinct and cannot be expressed cleanly by an existing skill;
   - **architecture lesson** — it improves evaluation, discovery, safety, routing, specialization, or maintenance without becoming a user-facing skill;
   - **reject** — redundant, provider-bound without reusable logic, weakly implemented, stale, unsafe, unlicensed for adaptation, or unable to beat the current baseline.
6. For a retained change, absorb only the smallest behavior or mechanism that improves the canonical implementation. Do not vendor upstream prose, scripts, assets, or process history unless the artifact itself is necessary and its license permits it.
7. Evaluate the candidate against explicit assertions before and after the change. A new canonical skill must also pass positive and negative routing tests. Do not keep a change merely because it is newer or more detailed.
8. Advance `last_reviewed_commit` only after the whole relevant delta has been classified. The reviewed commit is also the rejection memory: rejected source text does not need a local archive.
9. Update provenance only for sources that materially contributed to a retained canonical implementation. Architecture-only lessons may instead be recorded compactly in the adjacent-route ledger.

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

- discovered and transitive sources remain untrusted metadata;
- unreviewed sources are not routable;
- scheduled discovery does not execute candidate scripts or install candidate dependencies;
- upstream instructions never gain authority merely by being read or cited;
- promotion retains normalized behavior, not the upstream prompt as a second runtime authority;
- only canonical skills participate in normal task routing.

This architecture reduces contamination risk; it does not make malicious or low-quality input impossible. Supply-chain and prompt-injection review remain required before promotion.

## Design evolution

Design guidance has two different kinds of knowledge and they must not be mixed:

- **durable judgment** — hierarchy, proportion, rhythm, contrast, optical balance, typography, material coherence, content-form fit, interaction quality, restraint, and intentional tension;
- **dated generator fingerprints** — recurring combinations that a model family or design-generator era overproduces across unrelated briefs.

Durable judgment belongs in the core design protocol. Dated fingerprints belong in `skills/design-frontend/references/aesthetic-signals.md` and are evidence, not bans. Update or remove them when the pattern landscape changes.

A design rule is not accepted because a respected designer prefers it. Compare multiple independent design sources, separate shared principles from author taste, and test the result across deliberately different briefs. If different briefs still collapse to the same composition, palette logic, typography role, or motion vocabulary, the guidance is not teaching taste; it is teaching another template.

## Stop condition

Stop an ingestion pass when every changed candidate in the reviewed delta is classified and every retained change is proven against its actual contract. Do not search for extra work merely to make the pass feel comprehensive.
