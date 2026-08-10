# Agent Skills Neutral

A private, vendor-neutral thinking-core and workflow evolution library. It distills external implementations and execution experience into an always-on reasoning core plus a small set of optional thinking workflows, while keeping source discovery, evaluation, and replaceable operational knowledge outside task-time canonical context.

The project optimizes for **agent capability lift**, not catalog breadth. The highest-value changes make an agent frame, reason, search, decompose, decide, handle uncertainty, verify, recover, learn, or stop better across unrelated tasks. Product/framework manuals, file-format recipes, and tool syntax remain replaceable runtime knowledge; they may inspire a transferable mechanism but are not canonical skills.

The current library contains 27 canonical thinking workflows. That number is derived from the current deletion test, not a target. Canonical-count growth, source-count growth, and domain coverage are not success metrics; a compact mechanism that improves the thinking core can be more valuable than multiple new workflows.

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
always-on thinking core
      +
optional thinking workflows
      |
      v
model-native semantic activation
```

A discovered implementation is never accepted because it is newer, more popular, more detailed, cited by another source, or covers a named technology. It must improve a real capability or project mechanism under explicit evidence.

## Runtime activation

The compact [`runtime/AGENTS.md`](runtime/AGENTS.md) thinking core is **always on**. It supplies the default cross-domain reasoning loop even when no workflow is selected.

Workflow selection is **model-native and semantic by default**.

For hosts with native Agent Skills discovery, expose each workflow's compact frontmatter metadata and let the model choose semantically. For hosts without native discovery, use [`runtime-catalog.json`](runtime-catalog.json), which contains only:

```text
name
description
location
```

The model selects by the current cognitive outcome and workflow description, then loads only the selected `SKILL.md` body and any conditionally required references. No workflow is a valid result when the thinking core is sufficient or the request only needs current tool documentation.

`python scripts/select_skills.py "<task>" --json` remains available as an **advisory lexical fallback and offline regression harness**. Its suggestion is not task-time authority and must not hard-veto a semantically correct model choice.

At the current library size, the full compact metadata catalog is small enough for direct semantic selection. If the library grows materially, scale through semantic capability groups, shortlists, and dependency-aware navigation while preserving model judgment as the final activation step.

See [`docs/SEMANTIC_ROUTING.md`](docs/SEMANTIC_ROUTING.md).

## Runtime bundle

This repository is the authoring and evolution source of truth. Task agents should consume the generated runtime-only bundle instead of the maintenance repository root when the deployment environment supports that boundary.

```bash
python scripts/build_runtime_bundle.py build --output dist/runtime
python scripts/build_runtime_bundle.py verify --bundle dist/runtime
```

The generated surface contains only the always-on thinking core as `AGENTS.md`, `runtime-catalog.json`, `MANIFEST.json`, and canonical thinking workflows under `skills/`. Evolution, provenance, discovery, tests, benchmarks, tool/domain adapters, and maintainer policy remain outside task-time context.

`dist/` is disposable staging output and is never canonical source. When a host such as Codex discovers `AGENTS.md` from ancestor directories, do not use an in-repository `dist/` bundle as the task working root: deploy and reverify the artifact outside the authoring repository tree so maintainer instructions cannot join the runtime prompt.

See [`docs/RUNTIME_BUNDLE.md`](docs/RUNTIME_BUNDLE.md).

## Execution attribution

Future trajectory mining can bind a real session to the exact Runtime Bundle it was assigned without adding provenance or bookkeeping to task-time instructions. A privacy-minimal execution receipt derives artifact identity from `MANIFEST.json`, uses runtime-specific adapters for session linkage, and keeps actual serving, full Skill-body delivery, and separately evidenced compliance as distinct claims.

The first adapter uses Codex `SessionStart` / `SessionEnd` hooks, `debug prompt-input` preflight, and local JSONL trace evidence. Old pre-instrumentation sessions correctly remain `unknown` for serving and activation even when model/runtime metadata is recoverable.

See [`docs/EXECUTION_ATTRIBUTION.md`](docs/EXECUTION_ATTRIBUTION.md).

## Capability layers

Runtime has only two canonical layers:

1. **always-on thinking core** — cross-domain control over task framing, uncertainty, alternatives, next-action choice, evidence, recoverability, verification, learning, and stopping;
2. **optional thinking workflow** — a distinct scenario-specific reasoning process that materially improves an active cognitive outcome.

Tool syntax, file-format operations, provider setup, and product/domain manuals are non-canonical operational knowledge. Agents recover them from the live environment, host capabilities, and current primary documentation.

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
    > thinking workflow
        > non-canonical operational knowledge
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
- provider/framework material remains a non-canonical source reservoir;
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
runtime/AGENTS.md          always-on cross-domain thinking core source
index.json                 semantic routing metadata and category navigation
routes/*.json              diagnostic/fallback boundary metadata
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
scripts/execution_attribution.py receipt core + Codex adapter + failure attribution interface
scripts/test_execution_attribution.py deterministic serving/activation/privacy tests
docs/ARCHITECTURE.md       source/runtime separation and capability-lift model
docs/EXECUTION_ATTRIBUTION.md serving/activation evidence boundary and Codex adapter
docs/SEMANTIC_ROUTING.md   model-native activation and scale-up path
docs/CAPABILITY_LAYERS.md  thinking-core/workflow/non-canonical boundary
docs/LEARNING_LOOP.md      trajectory-grounded, held-out-gated evolution loop
docs/CURATOR_POLICY.md     worker/analyst/curator/judge model policy
docs/EVOLUTION.md          high-value ingestion and replacement protocol
docs/BENCHMARK.md          baseline/candidate evidence contract
docs/SKILL_REVIEW.md       canonical implementation review
```

## Current levels

- **S:** high-transfer thinking workflow, loaded on demand for its cognitive outcome.
- **A:** scenario thinking workflow, loaded on demand when it adds independent reasoning value.

S/A is reference metadata, not a semantic routing score. Neither level is a persistent default profile; the only always-on layer is `runtime/AGENTS.md`. Material that cannot justify a thinking workflow should strengthen the core, merge into an existing owner, or remain outside canonical runtime.

User authorization, repository guidance, runtime safety, and tool-specific approval boundaries remain authoritative regardless of skill selection.

## Automation

The repository contains deterministic validation and read-only ecosystem scanning. Discovery and preprocessing may be highly automated; semantic promotion remains evidence-gated and uses stronger reasoning capacity only at the high-leverage decision points.

While the repository remains private, scheduled ecosystem scanning stays disabled unless manually dispatched, avoiding unnecessary private Actions usage.

## 中文说明

这个项目的目标不是收集最多的 Agent Skill，也不是让 Agent 记住产品说明书，而是持续进化一个默认常驻的思维核心，并提炼那些能让 Agent **更会判断、更会搜索、更会分解问题、更会验证、更会纠错、更会利用经验** 的场景思维工作流。

运行时优先让 Agent 根据 `name + description` 自己做语义选择，代码路由只作为回归测试和弱客户端 fallback。维护时，便宜模型可以做扫描、整理和测试，但跨来源抽象、泛化范围、合并/删除和 canonical promotion 交给强 reasoning curator，并用 held-out 和独立证据决定是否真正保留。

来源数量可以持续增长，但真正高价值的结果通常是强化思维核心或已有 workflow，而不是增加产品、工具、文件格式或领域 trigger。此类可替代知识由 Agent 在任务时从当前环境和一手文档获取。
