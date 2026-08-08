# Agent Skills Neutral

A private, vendor-neutral Agent Skills reference and evolution library. It distills external implementations and execution experience into a smaller set of reusable agent capabilities while keeping source discovery, specialist knowledge, evaluation, and runtime activation separated.

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
capability normalization  decision logic / evidence / failure modes
      |
      v
capability-lift claim     what agent behavior becomes better?
      |
      v
baseline comparison       fresh + held-out + regression evidence
      |
      +---- reject / specialize / narrow
      |
      v
retain smallest useful mechanism
      |
      v
canonical / shared kernel
      |
      v
model-native semantic activation
```

A discovered implementation is never accepted because it is newer, more popular, more detailed, cited by another source, or covers a named technology. It must improve a real capability or project mechanism under explicit evidence.

## Runtime activation

Skill selection is **model-native and semantic by default**.

For hosts with native Agent Skills discovery, expose each skill's compact frontmatter metadata and let the model choose semantically. For hosts without native discovery, use [`runtime-catalog.json`](runtime-catalog.json), which contains only:

```text
name
description
location
```

The model selects by requested outcome and the skill's description, then loads only the selected `SKILL.md` body and any conditionally required references.

`python scripts/select_skills.py "<task>" --json` remains available as an **advisory lexical fallback and offline regression harness**. Its suggestion is not task-time authority and must not hard-veto a semantically correct model choice.

At the current library size, the full compact metadata catalog is small enough for direct semantic selection. If the library grows materially, scale through semantic capability groups, shortlists, and dependency-aware navigation while preserving model judgment as the final activation step.

See [`docs/SEMANTIC_ROUTING.md`](docs/SEMANTIC_ROUTING.md).

## Runtime bundle

This repository is the authoring and evolution source of truth. Task agents should consume the generated runtime-only bundle instead of the maintenance repository root when the deployment environment supports that boundary.

```bash
python scripts/build_runtime_bundle.py build --output dist/runtime
python scripts/build_runtime_bundle.py verify --bundle dist/runtime
```

The generated surface contains only the minimal runtime `AGENTS.md`, `runtime-catalog.json`, `MANIFEST.json`, and canonical `skills/`. Evolution, provenance, discovery, tests, benchmarks, and maintainer policy remain outside task-time context.

`dist/` is disposable generated output and is never canonical source.

See [`docs/RUNTIME_BUNDLE.md`](docs/RUNTIME_BUNDLE.md).

## Capability layers

Canonical skills have different strategic roles:

1. **meta capability** — improves how the agent thinks, learns, verifies, routes, or coordinates across many tasks;
2. **reasoning workflow** — owns a narrower outcome but still contributes reusable judgment;
3. **specialist operation** — adds correctness for a particular artifact, protocol, tool family, runtime, or technical domain;
4. **product/framework adapter** — normally remains outside the main canonical surface unless repeated evidence proves a dedicated runtime route is necessary.

Evolution effort is intentionally biased toward the first two layers. Specialist breadth is useful but is not the project's north star.

See [`docs/CAPABILITY_LAYERS.md`](docs/CAPABILITY_LAYERS.md).

## High-value absorption

For a promising source, the review unit is not "the skill" but the smallest claimed improvement in agent behavior.

Ask:

- What decision, search, correction, evidence, memory, or verification behavior changes?
- What mechanism causes the change?
- Does current canonical behavior already cover it?
- If the mechanism is deleted, does the demonstrated improvement disappear?
- Does the improvement survive held-out or contrasting tasks outside the source context?
- Can it strengthen an existing skill or shared kernel instead of adding a new route?

Retain only the smallest mechanism that survives those checks. Provider setup, fixed thresholds, examples, explanatory bulk, and author style do not come along automatically.

Review priority is:

```text
meta capability mechanism
    > reasoning workflow
        > specialist operation
            > product/framework adapter
```

Higher priority is not automatic acceptance.

## Learning from execution experience

The library should improve from real outcomes without converting every failure into permanent prompt text.

The evolution loop is:

```text
experience / trajectories
      |
      v
failure attribution
      |
      v
trajectory-local lessons
      |
      v
semantic consolidation
      |
      v
smallest transferable claim
      |
      v
bounded candidate edit
      |
      +---- held-out tasks
      +---- regression suite
      |
      v
retain / narrow / specialize / reject
      |
      v
slow library consolidation
```

Proposal experience and acceptance evidence are separated. Memory and retrieval policy are also treated as potentially learnable objects when evidence shows they are the bottleneck.

See [`docs/LEARNING_LOOP.md`](docs/LEARNING_LOOP.md).

## Evolution Runner

`python scripts/evolution_runner.py` turns a proposed capability change into a deterministic experiment state: baseline/candidate evidence, held-out cases, regressions, transfer evidence, semantic judgments, and an explicit curator decision.

The runner never generates or auto-promotes a candidate. `retain` and `merge` require a promotion-ready gate; `narrow` and `specialize` are explicit scope-reduction outcomes when the broader claim does not survive.

Local run state lives under `.evolution/` and is ignored by Git.

See [`docs/EVOLUTION_RUNNER.md`](docs/EVOLUTION_RUNNER.md).

## Model roles

The weakest worker should not determine the quality ceiling of shared canonical behavior.

Deterministic code and inexpensive/local models are appropriate for inventory, extraction, diffing, validation, execution, and already-specified mechanical edits. High-impact semantic decisions—cross-source abstraction, generalization boundaries, promotion, merge/delete decisions, held-out design, and failure attribution—should use a high-capability reasoning curator.

Where semantic judging is necessary, prefer acceptance evidence from a fresh or independent judging context rather than the same proposal trace. Stronger models improve the search space, but model confidence never replaces evidence.

See [`docs/CURATOR_POLICY.md`](docs/CURATOR_POLICY.md).

## Continuous evolution

Known direct skill upstreams are pinned to the last commit whose relevant delta was fully classified, so later maintenance can inspect change instead of reviewing all history again.

```bash
python scripts/scan_upstreams.py
python scripts/scan_upstreams.py --json
python scripts/discover_upstreams.py
python scripts/discover_upstreams.py --include-mechanisms
```

`discover_upstreams.py` is metadata-only. Its normal lane discovers Agent Skill repositories and one-hop source references. The optional mechanism lane also searches for evaluator, reasoning, memory/context, self-improvement, routing, trajectory/distillation, and related implementations that may contain transferable capability mechanisms. Discovery signals only prioritize what to inspect; they never imply trust or promotion.

A candidate can result in:

- **strengthen** — improve an existing canonical owner;
- **replace** — replace the current implementation with stronger demonstrated behavior;
- **new capability** — fill a genuinely unowned reusable gap;
- **architecture lesson** — improve routing, evaluation, memory, discovery, safety, learning, or maintenance without adding a user-facing skill;
- **specialize/narrow** — retain useful behavior without promoting it to shared scope;
- **reject** — no justified retained change.

The preferred result is often **strengthen, replace, architecture lesson, specialize, or reject**, not another trigger.

See [`docs/EVOLUTION.md`](docs/EVOLUTION.md).

## Evidence model

Canonical changes should beat the relevant baseline on the specific behavior claim they are intended to improve.

Prefer:

- deterministic checks when they directly settle the outcome;
- comparable baseline and candidate conditions;
- fresh downstream execution for behavior-sensitive instructions;
- proposal/training experience separated from held-out acceptance evidence;
- contrasting or cross-domain cases for claims of general capability lift;
- explicit regression suites protecting previously proven behavior;
- separate evidence dimensions instead of one arbitrary global quality score.

See [`docs/BENCHMARK.md`](docs/BENCHMARK.md).

## Why a large source pool does not become a large context

- `upstreams.json` is review state, not runtime context;
- unreviewed candidates are never routable;
- discovery automation does not execute candidate code or install dependencies;
- candidates compete by normalized mechanisms rather than being copied as parallel prompts;
- provider/framework material can remain a source or specialist reservoir;
- rejected prose does not accumulate as runtime prompt history;
- only retained canonical metadata participates in normal skill discovery.

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Agent quick start

For a native Agent Skills host, point it at `skills/` and let the model perform semantic activation from skill frontmatter.

For a host without native discovery:

```text
runtime-catalog.json
   -> model chooses semantically
      -> skills/<name>/SKILL.md
         -> conditional references only when needed
```

Useful validation commands:

```bash
python scripts/validate_catalog.py
python scripts/test_routing.py
python scripts/select_skills.py "debug a flaky integration test" --json
```

The last command is advisory diagnostics, not the preferred runtime selection path.

## Repository layout

```text
runtime-catalog.json       compact model-facing name/description/location catalog
index.json                 semantic routing metadata and category navigation
routes/*.json              diagnostic/fallback boundary metadata
profiles/*.txt             small persistent install/reference sets
catalog.json               full machine-readable canonical inventory
CATALOG.md                 human-readable canonical list
AGENTS.md                  loading, trust, necessity, and evolution contract
skills/<name>/SKILL.md     portable canonical skills
provenance.json            exact pointers for sources actually absorbed
upstreams.json             incremental direct-source review state
scripts/select_skills.py   advisory lexical fallback + regression harness
scripts/scan_upstreams.py  changed-upstream detector
scripts/discover_upstreams.py metadata-only skill + mechanism discovery
scripts/test_routing.py    deterministic boundary regression tests
scripts/validate_catalog.py deterministic repository validator
docs/ARCHITECTURE.md       source/runtime separation and capability-lift model
docs/SEMANTIC_ROUTING.md   model-native activation and scale-up path
docs/CAPABILITY_LAYERS.md  meta/workflow/specialist strategic classification
docs/LEARNING_LOOP.md      trajectory-grounded, held-out-gated evolution loop
docs/CURATOR_POLICY.md     worker/analyst/curator/judge model policy
docs/EVOLUTION.md          high-value ingestion and replacement protocol
docs/BENCHMARK.md          baseline/candidate evidence contract
docs/SKILL_REVIEW.md       canonical implementation review
```

## Current levels

- **S:** reusable core workflows; only the default task loop is installed persistently when a host chooses to use that profile.
- **A:** high-value retained capabilities loaded on demand.

S/A is reference metadata, not a semantic routing score. A capability that cannot justify canonical context should be merged, deleted, demoted to a specialist layer, or remain in the source reservoir.

User authorization, repository guidance, runtime safety, and tool-specific approval boundaries remain authoritative regardless of skill selection.

## Automation

The repository contains deterministic validation and read-only ecosystem scanning. Discovery and preprocessing may be highly automated; semantic promotion remains evidence-gated and uses stronger reasoning capacity only at the high-leverage decision points.

While the repository remains private, scheduled ecosystem scanning stays disabled unless manually dispatched, avoiding unnecessary private Actions usage.

## 中文说明

这个项目的目标不是收集最多的 Agent Skill，也不是让 Agent 记住最多产品说明书，而是持续提炼那些能让 Agent **更会判断、更会搜索、更会分解问题、更会验证、更会纠错、更会利用经验** 的通用机制。

运行时优先让 Agent 根据 `name + description` 自己做语义选择，代码路由只作为回归测试和弱客户端 fallback。维护时，便宜模型可以做扫描、整理和测试，但跨来源抽象、泛化范围、合并/删除和 canonical promotion 交给强 reasoning curator，并用 held-out 和独立证据决定是否真正保留。

来源数量可以持续增长，但真正高价值的结果通常是强化已有 capability 或共享学习机制，而不是再增加一个产品 trigger。
