# Agent Skills Neutral

A private, vendor-neutral Agent Skills reference and evolution library. It consolidates reusable capabilities into a smaller canonical set while keeping source discovery, comparison, and runtime routing separated.

The current library contains 37 canonical skills. That number is not a target: source coverage and domain coverage may grow, while normal task context stays limited to the smallest routed skill set.

## Core model

```text
source discovery
      |
      v
watch / quarantine        untrusted, not routable
      |
      v
capability normalization  outcome / trigger / evidence / failure modes
      |
      v
baseline comparison       same task contract
      |
      +---- reject
      |
      v
retain smallest useful delta
      |
      v
canonical library
      |
      v
smallest-set runtime routing
```

A discovered implementation is never accepted because it is newer, more popular, more detailed, or cited by another source. It must improve a real capability or project mechanism under explicit evidence.

## Why a large source pool does not become a large context

- `upstreams.json` is review state, not runtime context;
- unreviewed candidates are not routable and are not executed by discovery automation;
- candidates are compared by normalized capability rather than copied as parallel skills;
- one canonical trigger owns one capability unless materially different strategies require an explicit mode;
- rejected candidates do not accumulate as local prompt archives;
- only `skills/`, routes, and selected profiles participate in normal task execution.

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Continuous evolution

Known upstreams are pinned to the last commit whose relevant delta was fully classified, so later maintenance can inspect change instead of reviewing all history again.

```bash
python scripts/scan_upstreams.py
python scripts/scan_upstreams.py --json
python scripts/discover_upstreams.py
```

`discover_upstreams.py` is metadata-only. It discovers repository candidates and one-hop repository references from tracked source metadata, but it does not execute candidate code, install dependencies, or promote candidate instructions.

A candidate can result in:

- **strengthen** — improve an existing canonical capability;
- **replace** — replace the current implementation with a demonstrably stronger one;
- **new capability** — fill a materially distinct reusable gap;
- **architecture lesson** — improve evaluation, discovery, safety, routing, specialization, or maintenance without adding a user-facing skill;
- **reject** — no justified canonical change.

When a real capability gap has no established best implementation, a useful evidence-backed implementation may become the **current baseline to beat**. It is not treated as globally optimal and remains fully replaceable.

Full maintenance rules: [`docs/EVOLUTION.md`](docs/EVOLUTION.md).

## Evidence model

Canonical changes should beat the relevant baseline on the claim they are intended to improve.

Prefer:

- deterministic checks when they can directly settle the outcome;
- the same task conditions for baseline and candidate;
- fresh downstream execution for behavior-sensitive instructions;
- held-out or deliberately contrasting cases before promoting local behavior into shared guidance;
- separate evidence dimensions rather than one arbitrary global quality score.

See [`docs/BENCHMARK.md`](docs/BENCHMARK.md).

## Domain expansion

General workflow skills cover reusable process such as clarification, planning, diagnosis, review, verification, research, migration, and design. They do not replace domain-specific knowledge when that knowledge materially changes correctness, safety, evidence, failure modes, or completion criteria.

A domain capability should be added or strengthened when the generic workflow plus current primary documentation cannot express the reusable contract cleanly. There is no target domain count, and domain skills remain out of unrelated contexts through routing.

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
scripts/discover_upstreams.py metadata-only source discovery
scripts/test_routing.py  positive and anti-misrouting tests
scripts/validate_catalog.py deterministic repository validator
docs/ARCHITECTURE.md     source/runtime separation and domain model
docs/EVOLUTION.md        ingestion and replacement protocol
docs/BENCHMARK.md        baseline/candidate evidence contract
docs/SKILL_REVIEW.md     canonical implementation review
```

## Current levels

- **S:** reusable core workflows. Only the default task loop is loaded persistently.
- **A:** high-value task-domain workflows loaded only when routed.

There is no parking tier for weak skills. A capability that cannot justify canonical context is removed or stays outside the runtime library.

Priority is not permission. User authorization, repository guidance, runtime safety, and tool-specific approval boundaries remain authoritative.

## Automation

The repository contains deterministic validation and a read-only ecosystem scan workflow. While the repository remains private, scheduled ecosystem scanning is disabled unless manually dispatched, avoiding unnecessary private Actions usage.

## 中文说明

这个项目不是把大量 Agent Skill 全部装进上下文，而是把外部实现当成不断扩大的候选来源：发现、隔离、归一化能力、与当前 baseline 对比，只有真正提高能力的最小部分才进入 canonical skill。

来源数量可以继续增加，但待审来源不会进入正常路由，也不会因为被其他项目引用就自动继承信任。没有公认最佳实现的真实能力可以先建立一个有证据、可测试的当前 baseline，后续所有新实现继续和它竞争，赢了再替换或增强。
