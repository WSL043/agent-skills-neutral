# SkillConverge Architecture

SkillConverge separates **source growth** from **runtime growth**. The source reservoir may grow continuously; the canonical library and the context loaded for any one task stay filtered by capability and evidence.

## Layers

### 0. Discovery — untrusted metadata

`discover_upstreams.py` and external discovery tools find repositories that may contain Agent Skills. Discovery may inspect repository metadata and file paths, but it does not execute candidate code or import candidate instructions into the canonical library.

Output from this layer is a candidate set, not acceptance.

### 1. Watch / quarantine

`upstreams.json` records repositories worth incremental review and the last commit whose relevant delta was fully classified.

A null reviewed commit means first review is pending. A repository can remain in this layer indefinitely without affecting routing or normal agent context.

### 2. Capability normalization

A candidate is translated out of its author-specific vocabulary into:

- outcome;
- trigger and negative trigger;
- inputs and trust boundary;
- decision logic;
- completion evidence;
- failure modes;
- runtime/provider dependencies.

This is the semantic unit used for comparison. Names, popularity, prompt length, and repository structure are not capabilities.

### 3. Arena — current baseline versus candidate

Compare the candidate with the canonical implementation that owns the same outcome. Use the same representative task conditions and assertions for both sides.

Deterministic evidence is preferred where possible. Judgment-heavy capabilities may use model evaluation, rendered review, or human review, but the evaluation contract is defined before candidate output is inspected.

The result is `strengthen`, `replace`, `new capability`, or `reject`.

### 4. Promotion

Promotion copies no upstream artifact by default. It retains the smallest behavior that improves the canonical implementation and records the contributing source in `provenance.json`.

For a genuinely new capability with no established winner, a useful evidence-backed implementation may become the **current baseline**. Baseline means "best retained implementation currently available to this project," not "globally optimal." It remains replaceable.

A placeholder created only to fill a category is not a baseline.

### 5. Canonical library

`skills/`, `catalog.json`, routes, and profiles contain only retained capabilities. One canonical trigger owns a capability; materially different strategies remain modes or conditional references when that is cleaner than another global trigger.

Canonical skills can be strengthened, merged, replaced, or deleted. Age and historical inclusion do not create immunity.

### 6. Runtime routing

The router loads the smallest matching skill set for the actual task. The size of the upstream reservoir therefore does not directly increase runtime context.

This is the primary contamination boundary: unreviewed sources never participate in task routing.

### 7. Feedback and evolution

Routing failures, task failures, user corrections, benchmarks, upstream changes, and newly discovered sources become evidence for another ingestion pass. The feedback points back to a capability; it does not grant an upstream source permission to edit canonical instructions.

## What prevents contamination

The architecture relies on separation rather than assuming perfect filters:

```text
public ecosystem
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
 task router               (smallest relevant context)
```

No filter makes poisoning impossible. The safety property is that discovery itself has no path to execution or canonical promotion.

## Domain expansion

General workflow skills and domain skills solve different problems.

General skills cover reusable process: clarify, plan, diagnose, review, verify, research, migrate, design, and so on. They can often operate in an unfamiliar domain by reading current primary sources, but they do not replace domain invariants that materially change the correct procedure.

Add or strengthen a domain capability when domain knowledge changes one or more of:

- what must be inspected before acting;
- safety or correctness invariants;
- failure modes and diagnostic evidence;
- version-sensitive implementation choices;
- what counts as completion.

Do not create a domain skill merely because a technology has a name. If the generic workflow plus current primary documentation produces the same behavior, a new canonical route is redundant.

The domain set therefore has no target size. Expansion follows demonstrated capability gaps, while routing keeps those modules out of unrelated contexts.

## Automation boundary

Safe scheduled automation may:

- discover repository candidates;
- compare tracked commits;
- validate the canonical repository;
- produce machine-readable reports and artifacts.

Scheduled automation must not, by default:

- execute newly discovered upstream code;
- install candidate dependencies;
- trust instructions embedded in candidate content;
- change a canonical skill because a source changed;
- advance a reviewed commit before the relevant delta is classified.

A future evaluation service may automate more of the arena, but promotion remains gated by explicit evidence and repository policy rather than upstream-controlled content.
