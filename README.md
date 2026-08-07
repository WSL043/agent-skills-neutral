# Agent Skills Neutral

A private, vendor-neutral reference library of 37 canonical Agent Skills. It consolidates overlapping public implementations into concise standard `SKILL.md` files without bundling proprietary services, provider-specific runtimes, deprecated skills, weak platform checklists, upstream scripts, or licensed assets.

The repository is maintained as a distillation layer rather than a frozen pack: upstream sources can keep expanding while canonical skills are strengthened, replaced, merged, or removed through evidence-based comparison.

## Agent quick start

```bash
gh repo clone WSL043/agent-skills-neutral
python scripts/select_skills.py "debug a flaky integration test" --json
python scripts/validate_catalog.py
python scripts/test_routing.py
python scripts/scan_upstreams.py
```

Point an Agent Skills-compatible loader at `skills/`, or copy only the selected skill directories into the client's skill path. Agents should follow `AGENTS.md`: route first, load one primary SKILL.md completely, and add at most one support skill for a distinct second phase.

The compact discovery path is `index.json` → one `routes/<category>.json` → one `skills/<name>/SKILL.md`. `catalog.json` remains the full audit inventory and is intentionally not the first-read routing file.

For maintenance, `upstreams.json` records the last fully reviewed commit for tracked source repositories. `scripts/scan_upstreams.py` reports only changed or not-yet-reviewed sources; see `docs/EVOLUTION.md` for the absorb/replace/reject loop.

## Layout

```text
index.json               compact first-read category index
routes/*.json            bilingual positive/negative routing rules
profiles/*.txt           small install/reference sets
catalog.json             full machine-readable audit inventory
CATALOG.md               human-readable complete list
AGENTS.md                loading, trust, necessity, and evolution instructions
skills/<name>/SKILL.md   portable canonical skills
provenance.json          exact pointers for sources actually absorbed
upstreams.json           incremental upstream review state
docs/EVOLUTION.md        continuous distillation and replacement protocol
docs/SKILL_REVIEW.md     all 37 implementations, limits, and retention decisions
scripts/select_skills.py bilingual smallest-set router
scripts/scan_upstreams.py changed-upstream detector
scripts/test_routing.py  positive and anti-misrouting tests
scripts/validate_catalog.py deterministic integrity validator
```

## Levels

- **S (9):** core workflows; only six are in `profiles/default.txt`.
- **A (28):** high-value task-domain modules, loaded only when routed.

There is no B tier in the active library. Twelve former B entries were removed after re-evaluation because their useful content was already covered by stronger general workflows or their implementation was too narrow/tool-light to justify routing context.

The level is an installation/reference recommendation, not a license grant or authorization to perform external actions.

## 中文说明

这是经过官方 Agent Skills 结构校验、厂商依赖剔除和语义去重后的私有参考库。Agent 应先运行路由器；无法运行时读取 `index.json` 和一个领域路由文件，只加载一个主技能，必要时再加一个辅助技能。不要把 37 个技能或完整 `catalog.json` 一次性塞进上下文。

这个库不是一次性精选集。`upstreams.json` 会保留各上游已经完整审查到的 commit，扫描器只找之后的增量；新实现必须与现有 canonical 版本比较，证明有增量价值后才吸收。重复、厂商绑定、弱实现或无法胜过当前版本的候选只被判定后跳过，不把原始内容堆进仓库。

逐项实现、局限和保留理由见 [`docs/SKILL_REVIEW.zh-CN.md`](docs/SKILL_REVIEW.zh-CN.md)（[English](docs/SKILL_REVIEW.md)），持续进化规则见 [`docs/EVOLUTION.md`](docs/EVOLUTION.md)。默认配置仍只有六个核心工作流；设计、API、交接、可观测性和迁移能力都按具体任务单独路由。
