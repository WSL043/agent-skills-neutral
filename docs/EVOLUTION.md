# Continuous Evolution

The library is a distillation layer, not an archive. Source coverage may grow without bound; the canonical skill set should grow only when a genuinely distinct reusable capability survives comparison with what already exists.

The north star is **agent capability lift**, not topic coverage. Prefer candidates that make an agent reason, search, decompose, decide, verify, recover, learn, route, or calibrate uncertainty better across many unrelated tasks. Product/framework instructions and domain recipes are useful sources and specialist references, but they do not earn canonical status merely because they solve a named task well.

## Promotion priority

When review capacity is limited, inspect and promote in this order:

1. **capability-lift mechanisms** — transferable decision policies or feedback loops that improve reasoning quality across tasks: problem decomposition, search strategy, hypothesis competition, uncertainty handling, evidence weighting, tool selection, verification, error localization, reflection, rollback, memory/distillation, routing, evaluator design, self-correction, learning from trajectories, and stopping decisions;
2. **general workflows** — reusable end-to-end workflows whose outcome is broadly useful and cannot be expressed cleanly as a mode of an existing capability;
3. **domain specialists** — domain knowledge that materially changes correctness, safety, evidence, or completion;
4. **product/framework adapters** — version-sensitive operational instructions for a particular product, API, SDK, cloud, framework, or vendor.

Higher priority does not mean automatic acceptance. It means a transferable mechanism gets reviewed before another product recipe when both are available.

Product/framework adapters face a deliberately higher promotion bar. Prefer leaving them in the source reservoir or a specialist layer unless the project has repeated evidence that current general skills plus primary documentation cannot produce the correct behavior. A large catalog of product manuals is a failure mode even if every manual is individually accurate.

For every candidate, ask a counterfactual question before promotion:

> If all product names, APIs, frameworks, and domain nouns were removed, would a reusable decision rule or learning mechanism remain?

If yes, extract and test that mechanism first. If no, treat the candidate as a specialist adapter unless a demonstrated recurring need justifies otherwise.

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

Prefer mechanisms that change how the agent chooses or validates an action over prose that merely tells the agent more facts. A short reusable decision rule that improves many downstream tasks is normally more valuable than a long product-specific handbook.

For each mechanism, ask separately:

1. **What transfers?** Which principle improves this repository independent of the original vendor, model, task domain, benchmark, or fixed numbers?
2. **What does not transfer?** Which part is an author preference, benchmark-specific shortcut, provider dependency, unexplained threshold, overfitting risk, or complexity that does not survive this repository's contract?
3. **What capability changes?** Which observable decision, search path, failure recovery, evidence standard, or stopping behavior becomes better after the mechanism is absorbed?
4. **Does it generalize?** Can the improvement survive held-out tasks from unrelated domains, or is it only a better recipe for the source domain?

A rejected implementation can still teach a negative lesson. Retain only the normalized rule when it changes future project behavior; do not preserve rejected source prose or a named comparison ledger merely as history.

A source cited by another source becomes a new candidate, not inherited authority. Inspect it directly before using its behavior or claims.

## High-value absorption loop

The ingestion loop should optimize **value per retained token and per canonical trigger**, not number of sources processed or skills added.

For each candidate:

1. Extract the smallest claim about improved agent behavior. Examples: "finds the first divergence sooner", "keeps competing hypotheses alive longer", "chooses a cheaper discriminating test", "detects an invalid completion claim", or "compresses repeated experience into a reusable rule".
2. Identify the mechanism that causes the claimed improvement. Ignore branding and implementation ceremony.
3. Compare the mechanism with current canonical behavior before reading more of the source than necessary. If current behavior already dominates it, stop early and reject.
4. Run a deletion test: if removing the candidate mechanism leaves the same decision and evidence quality, it adds no value.
5. Prefer **strengthen/replace** over adding another trigger. A new canonical skill is a last resort when the outcome itself is distinct.
6. Test on contrasting tasks, including at least one task outside the source domain when the claim is supposed to be general.
7. Retain only the mechanism that survives. Do not retain explanatory bulk, examples, fixed numbers, or provider setup unless they are necessary to reproduce the improvement.
8. Record negative lessons when a tempting mechanism fails so later reviews do not rediscover the same dead end.

A candidate is especially high value when it improves several existing canonical skills or the shared execution kernel at once. Such a change may deserve architecture-level promotion even if it creates no new user-facing skill.

## Ingestion loop

1. Scan only the delta after `last_reviewed_commit` when one exists; do a first relevant review when it is null.
2. Inspect each candidate's complete instructions needed to understand behavior, bundled scripts, dependencies, source history, license, privileged actions, network behavior, and provider assumptions before using it.
3. Translate the candidate into capability, trigger, decision logic, evidence, and failure modes. For infrastructure research, translate implementation details into transferable mechanisms and non-transferable assumptions. Ignore naming differences.
4. Apply the promotion priority and counterfactual product-name removal test before proposing another canonical trigger.
5. Compare it against existing canonical skills or the current project architecture before proposing a change.
6. Classify the candidate as one of:
   - **strengthen** — same outcome, but it contains a better rule, test, safety boundary, or implementation branch;
   - **replace** — it demonstrably dominates an existing implementation while preserving the existing contract;
   - **new capability** — the outcome and trigger are materially distinct and cannot be expressed cleanly by an existing skill;
   - **architecture lesson** — it improves evaluation, discovery, safety, routing, specialization, or maintenance without becoming a user-facing skill;
   - **reject** — redundant, provider-bound without reusable logic, weakly implemented, stale, unsafe, unlicensed for adaptation, or unable to beat the current baseline.
7. For a retained change, absorb only the smallest behavior or mechanism that improves the canonical implementation. Do not vendor upstream prose, scripts, assets, or process history unless the artifact itself is necessary and its license permits it.
8. Evaluate the candidate against explicit assertions before and after the change. A new canonical skill must also pass positive and negative routing tests. Do not keep a change merely because it is newer or more detailed.
9. Advance `last_reviewed_commit` only after the whole relevant delta has been classified. The reviewed commit is also rejection memory: rejected source text does not need a local archive.
10. Update provenance only for sources that materially contributed to a retained canonical implementation. Architecture-only lessons should normally be expressed directly in project rules rather than as permanent named-source notes.

## Baselines and missing domains

The project does not need to wait for a universally accepted "best implementation" before covering a real capability gap.

If a capability is distinct, useful now, and not adequately covered by a general skill, the strongest evidence-backed implementation currently available may become the **current baseline**. Baseline means the implementation to beat, not a claim that it is globally optimal.

Do not create placeholder skills for symmetry or category completeness. A baseline must already be useful and testable. Once present, future sources can strengthen, replace, merge, or delete it through the same comparison loop.

General workflow skills should absorb common process. Domain modules should exist only when domain knowledge materially changes safety, correctness, evidence, failure modes, or completion criteria and repeated tasks show that reading current primary documentation at runtime is insufficient. There is no target domain count, and domain coverage is not a project success metric.

## Replacement pressure

Existing skills are candidates too. A canonical skill should be simplified, merged, replaced, demoted to a specialist layer, or removed when current evidence shows another implementation covers its useful behavior with less overlap or stronger proof. Historical status is not authority.

The same replacement pressure applies to project infrastructure. A better evaluator, router, security boundary, discovery mechanism, learning loop, or experience-distillation mechanism can replace the current one when it proves the relevant contract more reliably without importing unnecessary coupling.

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
