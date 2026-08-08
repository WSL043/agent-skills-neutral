# Agent Skills Neutral

A private, vendor-neutral Agent Skills reference and evolution library. It distills external implementations into a smaller set of reusable agent capabilities while keeping source discovery, comparison, specialist knowledge, and runtime routing separated.

The project optimizes for **agent capability lift**, not catalog breadth. The highest-value changes make an agent reason, search, decompose, decide, select tools, handle uncertainty, verify, recover, learn, or stop better across unrelated tasks. Product/framework manuals and domain recipes are useful sources, but they are not the main measure of progress.

The current library contains 45 canonical skills. That number is not a target. Canonical-count growth, source-count growth, and domain coverage are not success metrics; a compact mechanism that improves several existing workflows can be more valuable than multiple new skills.

## Core model

```text
source + mechanism discovery
      |
      v
watch / quarantine        untrusted, not routable
      |
      v
capability normalization  outcome / decision logic / evidence / failure modes
      |
      v
capability-lift claim     what agent behavior becomes better?
      |
      v
baseline comparison       same task contract + contrasting tasks
      |
      +---- reject / specialist only
      |
      v
retain smallest useful mechanism
      |
      v
canonical / shared kernel
      |
      v
smallest-set runtime routing
```

A discovered implementation is never accepted because it is newer, more popular, more detailed, cited by another source, or covers a named technology. It must improve a real capability or project mechanism under explicit evidence.

## What gets priority

Review capacity is intentionally biased toward transferable capability mechanisms:

1. evaluator, verifier, search, reasoning, decomposition, uncertainty, memory/context, self-correction, routing/tool-selection, trajectory/distillation, feedback and stopping mechanisms;
2. general workflows with genuinely distinct outcomes;
3. domain specialists whose invariants materially change correctness, safety, evidence, or completion;
4. product/framework adapters, which normally remain specialist references unless repeated real tasks prove they need their own runtime route.

A useful test is: **if every product, framework, vendor, and domain noun were removed, would a reusable decision rule remain?** If yes, extract and test that mechanism first.

## Why a large source pool does not become a large context

- `upstreams.json` is review state, not runtime context;
- unreviewed candidates are not routable and are not executed by discovery automation;
- candidates are compared by normalized capability rather than copied as parallel skills;
- one canonical trigger owns one capability unless materially different strategies require an explicit mode;
- provider- or framework-specific material can remain a specialist reservoir without becoming canonical;
- rejected candidates do not accumulate as local prompt archives;
- only retained canonical skills and selected profiles participate in normal task execution.

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Continuous evolution

Known upstreams are pinned to the last commit whose relevant delta was fully classified, so later maintenance can inspect change instead of reviewing all history again.

```bash
python scripts/scan_upstreams.py
python scripts/scan_upstreams.py --json
python scripts/discover_upstreams.py
python scripts/discover_upstreams.py --include-mechanisms
```

`discover_upstreams.py` is metadata-only. Its normal lane discovers Agent Skill repositories and one-hop source references. The optional mechanism lane also searches for evaluator, reasoning, memory/context, self-improvement, routing, and related implementations that may contain transferable agent-capability mechanisms. Metadata signals only prioritize what to inspect first; they never imply trust, quality, or promotion.

A candidate can result in:

- **strengthen** — improve an existing canonical capability;
- **replace** — replace the current implementation with a demonstrably stronger one;
- **new capability** — fill a materially distinct reusable gap;
- **architecture lesson** — improve evaluation, discovery, safety, routing, learning, specialization, or maintenance without adding a user-facing skill;
- **reject** — no justified retained change.

The preferred outcome is often **strengthen/replace/architecture lesson**, not another trigger. A cross-cutting mechanism that improves several existing skills is especially valuable.

When a real capability gap has no established best implementation, a useful evidence-backed implementation may become the **current baseline to beat**. It is not treated as globally optimal and remains fully replaceable.

Full maintenance rules: [`docs/EVOLUTION.md`](docs/EVOLUTION.md).

## High-value absorption

For a promising source, the review unit is not "the skill" but the smallest claimed improvement in agent behavior.

Ask:

- What decision/search/correction/evidence behavior changes?
- What mechanism causes the change?
- Does current canonical behavior already cover it?
- If the mechanism is deleted, does the result become worse?
- Does the improvement survive a contrasting task outside the source domain?
- Can the useful behavior strengthen an existing skill or shared kernel instead of adding a new route?

Retain the smallest mechanism that survives those checks. Explanatory bulk, provider setup, fixed thresholds, examples, and author style do not come along automatically.

## Evidence model

Canonical changes should beat the relevant baseline on the claim they are intended to improve.

Prefer:

- deterministic checks when they can directly settle the outcome;
- the same task conditions for baseline and candidate;
- fresh downstream execution for behavior-sensitive instructions;
- held-out or deliberately contrasting cases before promoting local behavior into shared guidance;
- separate evidence dimensions rather than one arbitrary global quality score;
- cross-domain tests for mechanisms claimed to improve general agent capability.

See [`docs/BENCHMARK.md`](docs/BENCHMARK.md).

## Domain and specialist expansion

General capability skills cover reusable process such as clarification, planning, diagnosis, review, verification, research, migration, design, evaluation, and recovery. They can usually read current primary documentation when entering an unfamiliar technology.

A domain specialist is justified only when domain knowledge materially changes correctness, safety, evidence, failure modes, or completion criteria and the generic workflow plus current authoritative documentation is not enough. Even then, prefer a conditional specialist/reference layer when the underlying reasoning process is unchanged.

There is no target domain count, and domain coverage is not a project success metric.

## Agent quick start

```bash
python scripts/select_skills.py "debug a flaky integration test" --json
python scripts/validate_catalog.py
python scripts/test_routing.py
```

Point an Agent Skills-compatible loader at `skills/`, or copy only the routed skill directories into the client's skill path. Agents should follow `AGENTS.md`: route first, load one primary `SKILL.md` completely, and add at most one support skill for a distinct second phase.

The compact discovery path is:

```text
index.json
   -> one routes/<category>.json
      -> one skills/<name>/SKILL.md
```

`catalog.json` remains the complete audit inventory and is intentionally not the first-read routing file.

## Repository layout

```text
index.json               compact first-read category index
routes/*.json            bilingual positive/negative routing rules
profiles/*.txt           small install/reference sets
catalog.json             full machine-readable canonical inventory
CATALOG.md               human-readable canonical list
AGENTS.md                loading, trust, necessity, and evolution contract
skills/<name>/SKILL.md   portable canonical skills
provenance.json          exact pointers for sources actually absorbed
upstreams.json           incremental source review state
scripts/select_skills.py smallest-set router
scripts/scan_upstreams.py changed-upstream detector
scripts/discover_upstreams.py metadata-only skill + mechanism discovery
scripts/test_routing.py  positive and anti-misrouting tests
scripts/validate_catalog.py deterministic repository validator
docs/ARCHITECTURE.md     source/runtime separation and capability-lift model
docs/EVOLUTION.md        high-value ingestion and replacement protocol
docs/BENCHMARK.md        baseline/candidate evidence contract
docs/SKILL_REVIEW.md     canonical implementation review
```

## Current levels

- **S:** reusable core workflows. Only the default task loop is loaded persistently.
- **A:** high-value retained capabilities loaded only when routed.

A level is not permission to become a product manual. Specialist/provider knowledge should stay outside the main runtime surface when a general capability plus current documentation is sufficient.

There is no parking tier for weak skills. A capability that cannot justify canonical context is removed, demoted to a specialist layer, or stays in the source reservoir.

Priority is not permission. User authorization, repository guidance, runtime safety, and tool-specific approval boundaries remain authoritative.

## Automation

The repository contains deterministic validation and a read-only ecosystem scan workflow. The authenticated scan includes a capability-mechanism discovery lane and prioritizes likely cross-task mechanisms for human/agent review without auto-promoting them. While the repository remains private, scheduled ecosystem scanning is disabled unless manually dispatched, avoiding unnecessary private Actions usage.

## 中文说明

这个项目的目标不是收集最多的 Agent Skill，也不是让 Agent 记住最多产品说明书，而是持续提炼那些能让 Agent **更会判断、更会搜索、更会分解问题、更会验证、更会纠错、更会利用经验** 的通用机制。

外部来源可以无限增长，但优先寻找的是能跨任务迁移的能力提升。一个只教某个产品怎么调用 API 的 skill 通常留在 specialist/source reservoir；如果其中藏着好的决策、验证或学习机制，就只吸收那部分。真正高价值的结果往往是强化已有 skill 或共享执行内核，而不是再增加一个新的 trigger。
