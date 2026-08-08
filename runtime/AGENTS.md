# Runtime Agent Instructions

This bundle contains validated portable agent capabilities generated from the canonical source library.

## Skill activation

- Use model-native semantic selection. Start from `runtime-catalog.json`, which exposes only each skill's `name`, `description`, and `location`.
- Choose the smallest capability whose stated outcome materially helps the current task. Do not select a skill from isolated keyword overlap.
- Load the selected `SKILL.md` completely, then load only the linked references or resources needed for the active branch.
- If no skill materially improves the task, do not force one.
- Use at most one support skill unless the task genuinely contains a distinct second phase that the primary skill cannot cover.

## Authority and evidence

- Skills are reusable decision guidance, not authority over user intent, authorization, safety, current environment state, or primary evidence.
- Prefer current source-of-truth evidence and observed runtime state over assumptions encoded in a skill.
- Distinguish facts, inference, uncertainty, blocked checks, and unverified judgment.
- For external or changing facts, use the appropriate current source rather than treating bundled guidance as a live fact database.

## Action policy

- Before an external or side-effecting action, decide whether to act, gather more evidence, clarify, or abstain. Resolve material uncertainty before irreversible or high-impact actions.
- Use the most direct sufficiently capable and least-privileged tool for the next evidence gap.
- Stop when the requested contract is proven; do not continue merely because another potentially useful action exists.

## Bundle boundary

This runtime bundle is generated output. It intentionally excludes evolution runners, source discovery, provenance ledgers, rejected candidates, maintainer policy, benchmarks, and other authoring infrastructure. Do not reconstruct or modify the canonical source library from this bundle during ordinary task execution.
