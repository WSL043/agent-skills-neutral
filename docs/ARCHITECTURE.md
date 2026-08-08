# Architecture

The repository separates **source growth** from **runtime growth**. The source reservoir may grow continuously; the canonical library and the context loaded for any one task stay filtered by capability and evidence.

The canonical library is optimized first for **agent capability lift**: reusable mechanisms that improve how an agent reasons, searches, decomposes, selects tools, handles uncertainty, tests hypotheses, verifies claims, recovers from failure, compresses experience, and decides when to stop. Domain and product coverage is secondary and should not turn the library into a handbook collection.

## Layers

### 0. Discovery — untrusted metadata

`discover_upstreams.py` and other discovery tools find repositories that may contain useful Agent Skill implementations or maintenance mechanisms. Discovery may inspect repository metadata and source relationships, but it does not execute candidate code or import candidate instructions into the canonical library.

Output from this layer is a candidate set, not acceptance.

Discovery has two conceptual lanes:

- **skill discovery** — reusable task workflows expressed as Agent Skills or comparable instructions;
- **mechanism discovery** — evaluators, optimizers, planners, verifiers, search systems, memory/distillation systems, routing systems, tool-governance systems, self-correction loops, trajectory learners, or other implementations whose mechanism may improve many skills at once.

The second lane has higher strategic value when it yields a transferable agent behavior rather than another topic-specific recipe.

### 1. Watch / quarantine

`upstreams.json` records repositories worth incremental review and the last commit whose relevant delta was fully classified.

A null reviewed commit means first review is pending. A repository can remain in this layer indefinitely without affecting routing or normal agent context.

Product/framework repositories may remain useful indefinitely as specialist reservoirs even when nothing in them merits a canonical trigger.

### 2. Capability normalization

A candidate is translated out of its author-specific vocabulary into:

- outcome;
- trigger and negative trigger;
- inputs and trust boundary;
- decision logic;
- completion evidence;
- failure modes;
- runtime/provider dependencies;
- **capability-lift claim** — what observable decision, search path, correction, evidence standard, or stopping behavior improves;
- **transfer boundary** — whether the mechanism survives removal of product, framework, vendor, and domain names.

This is the semantic unit used for comparison. Names, popularity, prompt length, repository structure, and product coverage are not capabilities.

### 3. Baseline comparison

Compare the candidate with the canonical implementation that owns the same outcome or with the shared execution architecture when the candidate is a cross-cutting mechanism. Use the same representative task conditions and assertions for both sides.

Deterministic evidence is preferred where possible. Judgment-heavy capabilities may use model evaluation, rendered review, or human review, but the evaluation contract is defined before candidate output is inspected.

For a mechanism claimed to generalize, include contrasting or held-out tasks outside the source domain. A mechanism that only wins on its own product examples remains a specialist result.

The result may be `strengthen`, `replace`, `new capability`, `architecture lesson`, or `reject`.

### 4. Promotion

Promotion copies no upstream artifact by default. It retains the smallest behavior that improves the canonical implementation and records a contributing source only when that source materially shaped retained behavior.

Promotion pressure is intentionally asymmetric:

1. cross-cutting capability-lift mechanisms are preferred when evidence is comparable;
2. general workflows may become canonical when their outcome is genuinely distinct;
3. domain specialists require evidence that domain invariants change correctness, safety, evidence, or completion;
4. product/framework adapters normally remain outside the main canonical set unless repeated real tasks show that primary documentation plus general skills is insufficient.

For a genuinely new capability with no established winner, a useful evidence-backed implementation may become the **current baseline**. Baseline means "best retained implementation currently available to this project," not "globally optimal." It remains replaceable.

A placeholder created only to fill a category is not a baseline.

### 5. Canonical library

`skills/`, `catalog.json`, routes, and profiles contain retained capabilities. One canonical trigger owns a capability; materially different strategies remain modes or conditional references when that is cleaner than another global trigger.

Canonical does not mean permanent. A skill may be strengthened, merged, replaced, demoted to a specialist layer, or deleted when a more general mechanism covers its useful behavior with less runtime surface.

A canonical-count increase is not a success metric. Improvements that strengthen several existing skills without adding a trigger are often more valuable.

### 6. Runtime compilation / serving boundary

The source repository remains the single authoring and evolution authority. A deterministic compiler converts validated canonical source into a runtime-only artifact for task agents.

The generated surface contains the compact runtime catalog, the canonical skill-owned runtime files, a minimal runtime AGENTS contract, and an integrity manifest. It excludes discovery state, provenance, evolution machinery, tests, benchmarks, rejected candidates, and maintainer policy.

Generated runtime output is disposable and must not become a second source of truth. A future standalone runtime repository or package may mirror the verified artifact automatically, but it must not be hand-maintained independently.

### 7. Runtime semantic activation

Model-native semantic selection uses the compact runtime catalog and loads the selected `SKILL.md` progressively. The size of the source reservoir therefore does not directly increase runtime context.

This is the primary contamination boundary: unreviewed sources never participate in task routing.

Product or framework specialization should preferably be loaded as a narrow conditional reference or specialist adapter rather than made globally routable when the generic capability remains the same.

### 8. Feedback and evolution

Routing failures, task failures, user corrections, benchmarks, upstream changes, and newly discovered sources become evidence for another ingestion pass. The feedback points back to a capability; it does not grant an external source permission to edit canonical instructions.

Feedback should answer not only "which skill failed?" but also "which reusable decision mechanism was missing?" Repeated failures across unrelated skills are evidence for a shared capability-lift improvement rather than several domain patches.

## What prevents contamination

The architecture relies on separation rather than assuming perfect filters:

```text
external sources
      |
      v
 discovery metadata        (untrusted, automatic)
      |
      v
 watch/quarantine          (not routable, not executed)
      |
      v
 normalize + inspect       (license / trust / behavior)
      |
      v
 baseline comparison       (same contract/evidence)
      |
      v
 promotion decision
      |
      +---- reject --------> reviewed boundary only
      |
      v
 canonical library         (smallest retained behavior)
      |
      v
 runtime semantic activation (smallest relevant context)
```

No filter makes poisoning impossible. The safety property is that discovery itself has no path to execution or canonical promotion.

## Domain and specialist expansion

General capability skills and domain specialists solve different problems.

General capabilities cover reusable decision process: clarify, plan, search, diagnose, compare hypotheses, review, verify, research, migrate, design, evaluate, recover, and learn. They can often operate in an unfamiliar domain by reading current primary sources.

A domain specialist is justified only when domain knowledge changes one or more of:

- what must be inspected before acting;
- safety or correctness invariants;
- failure modes and diagnostic evidence;
- version-sensitive implementation choices that cannot be discovered cheaply at runtime;
- what counts as completion.

Even then, prefer a specialist layer or conditional reference when the underlying reasoning workflow is unchanged. Do not create a domain skill merely because a technology has a name or a source repository contains a detailed manual.

Before a domain/product candidate receives a new canonical trigger, remove its product and domain nouns mentally. If no reusable decision mechanism remains, require repeated real-task evidence that a specialist route is necessary.

The domain set therefore has no target size, and domain coverage is not a project success metric.

## High-value absorption architecture

The most valuable source may improve the system without becoming a skill.

A mechanism can be promoted into:

- the shared execution/necessity kernel;
- routing and trigger selection;
- candidate discovery and ranking;
- evaluation and benchmark contracts;
- verification and completion evidence;
- error-correction or rollback logic;
- memory/trajectory distillation;
- source trust and supply-chain boundaries;
- an existing canonical skill;
- a new canonical skill only when the outcome itself is distinct.

This order prevents a common failure mode: discovering one useful idea and wrapping it in another globally routable prompt even though it belongs in shared behavior.

For every proposed retention, measure value as **behavioral improvement per retained token, trigger, and maintenance surface**. A compact mechanism that improves ten workflows should normally outrank ten new product skills.

## Automation boundary

Safe scheduled automation may:

- discover repository candidates and source relationships;
- compare tracked commits;
- validate the canonical repository;
- produce machine-readable reports and artifacts;
- rank candidates for review using metadata-only signals of likely mechanism value.

Scheduled automation must not, by default:

- execute newly discovered upstream code;
- install candidate dependencies;
- trust instructions embedded in candidate content;
- change a canonical skill because a source changed;
- advance a reviewed commit before the relevant delta is classified.

More of the comparison loop may be automated later, but promotion remains gated by explicit evidence and repository policy rather than source-controlled instructions.
