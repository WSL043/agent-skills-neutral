# SkillConverge

**A vendor-neutral Agent Skill distillation and convergence system.**

SkillConverge treats the public Agent Skill ecosystem as a growing source reservoir, not as a package to install wholesale. It discovers implementations, tracks upstream changes, compares overlapping capabilities, and retains a smaller canonical library whose skills can be strengthened, replaced, merged, or removed as evidence improves.

The current library contains 37 canonical skills. That number is not a target. Source coverage may grow without bound while runtime context stays filtered by capability and routing.

## The idea

Most skill repositories optimize one of these problems:

- publish more skills;
- generate a skill for a target;
- evaluate one skill;
- optimize a skill on one task or repository;
- learn skills from trajectories;
- scan skills for security problems.

SkillConverge connects those routes at the **ecosystem level**:

```text
public skill ecosystem + adjacent evaluators/optimizers
                    |
                    v
          metadata discovery
             (untrusted)
                    |
                    v
          watch / quarantine
                    |
                    v
     capability normalization
                    |
                    v
 current baseline <-> candidate
       same evaluation contract
                    |
          +---------+---------+
          |                   |
        reject             retain delta
                              |
                              v
                    canonical library
                              |
                              v
                  smallest-set routing
```

A new source never becomes runtime authority merely because it is public, popular, newer, or referenced by another project.

## Why the source pool can grow without polluting runtime

Discovery, promotion, and runtime routing are separate layers:

- `upstreams.json` is a watch/quarantine pool and may grow freely;
- discovered and transitive sources are untrusted and not routable;
- scheduled discovery does not execute upstream scripts or install dependencies;
- candidate behavior is normalized before comparison;
- only retained canonical skills under `skills/` participate in normal task routing;
- one capability keeps one canonical trigger unless materially different strategies require an explicit mode.

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) and [`SECURITY.md`](SECURITY.md).

## Continuous evolution

Known upstreams are pinned to the last commit whose relevant delta was fully classified. New scans therefore inspect change instead of repeatedly reviewing history.

```bash
python scripts/scan_upstreams.py
python scripts/scan_upstreams.py --json
python scripts/discover_upstreams.py
```

`discover_upstreams.py` performs metadata-only discovery and also extracts one-hop GitHub repository references from tracked READMEs. This lets the project learn from the projects that its sources cite or build on without inheriting their trust decisions.

Candidates are classified as:

- **strengthen** — improve an existing canonical capability;
- **replace** — demonstrably dominate the current implementation;
- **new capability** — fill a materially distinct reusable gap;
- **architecture lesson** — improve evaluation, discovery, safety, routing, specialization, or maintenance without becoming a user-facing skill;
- **reject** — no justified canonical change.

When a real capability gap has no accepted global best implementation, the strongest useful evidence-backed implementation may become the **current baseline to beat**. Baseline is not a claim of global optimality and placeholders are not accepted merely to fill categories.

Full rules: [`docs/EVOLUTION.md`](docs/EVOLUTION.md).

## Learn from adjacent routes too

SkillConverge does not only compare `SKILL.md` files. It tracks neighboring systems for mechanisms that can improve the convergence loop: evaluation harnesses, skill generators, trajectory learners, specialization engines, and supply-chain scanners.

Current adjacent routes include work such as SkillCompass, skillgrade, SkillAnything, RepoSkillOpt, SkillEvolver, SkillWeaver, and Cisco Skill Scanner. Their useful mechanisms and non-transferable assumptions are separated in [`docs/ADJACENT_ROUTES.md`](docs/ADJACENT_ROUTES.md).

A project cited by an adjacent route becomes another source candidate, not inherited authority.

## Evidence, not vibes

A canonical change should be able to beat the relevant baseline on the claim it is intended to improve.

SkillConverge prefers:

- deterministic graders when they can directly settle the outcome;
- the same task conditions for baseline and candidate;
- fresh downstream agent sessions for behavior-sensitive guidance;
- held-out or contrasting cases when promoting a rule into the shared base;
- separate evidence axes instead of one invented universal quality score.

See [`docs/BENCHMARK.md`](docs/BENCHMARK.md).

## Domain expansion

General workflow skills cover reusable process such as clarification, planning, diagnosis, review, verification, research, migration, and design. They do **not** eliminate the need for domain skills when domain knowledge changes correctness, safety, failure modes, evidence, or completion criteria.

The domain set can therefore expand indefinitely on demand while remaining out of unrelated task context. A technology does not deserve a skill merely because it has a name; a domain module is retained because the generic workflow plus current primary documentation is not enough to express the reusable contract cleanly.

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

`catalog.json` is the complete audit inventory, not the first-read routing file.

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
upstreams.json           untrusted incremental source/watch state
scripts/select_skills.py smallest-set router
scripts/scan_upstreams.py changed-upstream detector
scripts/discover_upstreams.py metadata + transitive source discovery
scripts/test_routing.py  positive and anti-misrouting tests
scripts/validate_catalog.py deterministic repository validator
docs/ARCHITECTURE.md     contamination boundaries and layer model
docs/EVOLUTION.md        source ingestion and replacement protocol
docs/ADJACENT_ROUTES.md neighboring-system lessons
docs/BENCHMARK.md        baseline/candidate evidence contract
docs/SKILL_REVIEW.md     canonical implementation review
```

## Current levels

- **S:** reusable core workflows. Only the default task loop is loaded persistently.
- **A:** high-value task-domain workflows loaded only when routed.

There is no parking tier for weak skills. A capability that cannot justify canonical context is removed or stays outside the runtime library.

Priority is not permission. User authorization, repository guidance, runtime safety, and tool-specific approval boundaries remain authoritative.

## Automation

The repository includes two GitHub Actions workflows:

- canonical validation on pushes and pull requests;
- scheduled ecosystem scanning that stays read-only and uploads discovery reports as artifacts.

The scheduled scan is intentionally disabled while the repository is private unless manually dispatched. After public release it can run on schedule without granting candidate sources write or execution authority.

## Contributing

Contributions may add a source, strengthen/replace a canonical implementation, propose a distinct new capability, or improve the convergence infrastructure. Bigger is not automatically better.

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before proposing upstream-derived changes.

## License and attribution

SkillConverge's original synthesis and tooling are released under the **Apache License 2.0**. Third-party source pointers and source-specific attribution/adaptation information remain in [`provenance.json`](provenance.json) and [`NOTICE`](NOTICE).

Public availability of an upstream repository is not treated as permission to copy its contents.

## 中文说明

SkillConverge 不是把大量 Agent Skill 全部装进上下文，而是把公开生态当作不断扩大的“原料池”：自动发现、追踪版本、隔离待审、归一化能力、与当前 canonical baseline 对比，只有证明有增量价值的最小行为才进入正式技能库。

来源池可以不断扩大，但待审来源不会进入正常路由，也不会因为被某个知名项目引用就继承信任。相邻的评测、优化、生成、自学习和安全扫描项目同样会被研究；好的机制可以进入项目架构，不适合迁移的固定阈值、作者偏好、单模型假设和 benchmark 特例则保留为负面经验。

目标不是声称已经知道“最佳实现”，而是让每个能力始终有一个可被证据推翻和替换的当前版本，并让后续候选持续和它竞争。
