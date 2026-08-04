# Agent Skills Neutral

A private, vendor-neutral reference library of 45 canonical Agent Skills. It consolidates overlapping public implementations into concise standard `SKILL.md` files without bundling proprietary services, provider-specific runtimes, deprecated skills, upstream scripts, or licensed assets.

## Agent quick start

```bash
gh repo clone WSL043/agent-skills-neutral
python scripts/select_skills.py "debug a flaky integration test"
python scripts/validate_catalog.py
```

Point an Agent Skills-compatible loader at `skills/`, or copy only the selected skill directories into the client's skill path. Agents that inspect repositories should read `AGENTS.md` and `catalog.json` first.

## Layout

```text
catalog.json             machine-readable discovery index
CATALOG.md               human-readable complete list
AGENTS.md                minimal loading and trust instructions
skills/<name>/SKILL.md   portable canonical skills
provenance.json          exact upstream source pointers and commits
scripts/select_skills.py lightweight local selector
scripts/validate_catalog.py deterministic integrity validator
```

## Levels

- **S (9):** first-wave core workflows.
- **A (24):** high-value task-domain modules.
- **B (12):** specialist modules loaded only when needed.

The level is an installation/reference recommendation, not a license grant or authorization to perform external actions.

## 中文说明

这是经过官方 Agent Skills 结构校验、厂商依赖剔除和语义去重后的私有参考库。Agent 应先读取 `catalog.json`，只加载命中任务的最少技能；不要把 45 个技能一次性全部塞进上下文。
