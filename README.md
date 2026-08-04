# Agent Skills Neutral

A private, vendor-neutral reference library of 45 canonical Agent Skills. It consolidates overlapping public implementations into concise standard `SKILL.md` files without bundling proprietary services, provider-specific runtimes, deprecated skills, upstream scripts, or licensed assets.

## Agent quick start

```bash
gh repo clone WSL043/agent-skills-neutral
python scripts/select_skills.py "debug a flaky integration test" --json
python scripts/validate_catalog.py
python scripts/test_routing.py
```

Point an Agent Skills-compatible loader at `skills/`, or copy only the selected skill directories into the client's skill path. Agents should follow `AGENTS.md`: route first, load one primary SKILL.md completely, and add at most one support skill for a distinct second phase.

The compact discovery path is `index.json` → one `routes/<category>.json` → one `skills/<name>/SKILL.md`. `catalog.json` remains the full audit inventory and is intentionally not the first-read routing file.

## Layout

```text
index.json               compact first-read category index
routes/*.json            bilingual positive/negative routing rules
profiles/*.txt           small install/reference sets
catalog.json             full machine-readable audit inventory
CATALOG.md               human-readable complete list
AGENTS.md                minimal loading and trust instructions
skills/<name>/SKILL.md   portable canonical skills
provenance.json          exact upstream source pointers and commits
docs/SKILL_REVIEW.md     all 45 implementations, limits, and retention decisions
scripts/select_skills.py bilingual smallest-set router
scripts/test_routing.py  positive and anti-misrouting tests
scripts/validate_catalog.py deterministic integrity validator
```

## Levels

- **S (9):** core workflows; only six are in `profiles/default.txt`.
- **A (24):** high-value task-domain modules.
- **B (12):** conditional specialists, excluded from the default profile and routed only by explicit matches.

The level is an installation/reference recommendation, not a license grant or authorization to perform external actions.

## 中文说明

这是经过官方 Agent Skills 结构校验、厂商依赖剔除和语义去重后的私有参考库。Agent 应先运行路由器；无法运行时读取 `index.json` 和一个领域路由文件，只加载一个主技能，必要时再加一个辅助技能。不要把 45 个技能或完整 `catalog.json` 一次性塞进上下文。

逐项实现、局限和保留理由见 [`docs/SKILL_REVIEW.zh-CN.md`](docs/SKILL_REVIEW.zh-CN.md)（[English](docs/SKILL_REVIEW.md)）。其中 `migrate-test-fixtures` 被明确标成 experimental；其余 B 级条目也都不会进入默认配置。
