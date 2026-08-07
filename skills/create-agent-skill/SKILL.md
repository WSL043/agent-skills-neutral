---
name: create-agent-skill
description: "Create or revise portable Agent Skills with standard SKILL.md frontmatter, concise trigger descriptions, progressive disclosure, reusable resources, and evidence-based validation. Use when designing, consolidating, testing, or improving an agent skill or skill library."
---

# Create Agent Skill

## Goal

Produce a focused, portable skill whose behavior is more reliable than an unstructured prompt or the current canonical implementation it is intended to improve.

## Workflow

1. Collect representative positive triggers, boundary cases, and at least one non-trigger. Add a case only for a distinct failure mode, and write the branch conditions that decide whether linked references must be read.
2. Choose the smallest reusable unit and a verb-led kebab-case name; split unrelated outcomes into separate skills.
3. Put only name and description in core frontmatter. Put concise trigger branches in the description, and make each pointer identify both its target and the condition for reaching it.
4. Write the minimum decision workflow in SKILL.md. Move branch-specific detail to references and deterministic repetition to scripts; let repository files, config, and command help remain the source of truth for facts they expose.
5. Define assertions before reading evaluation outputs. Compare representative runs with the candidate skill against the relevant baseline: no skill for a new capability, or the current canonical skill for an improvement.
6. Give every step a clear, checkable completion criterion and enough demand to account for every file, case, or claim material to the skill's stated contract. Revise only instructions linked to observed gaps, then rerun affected and regression cases.
7. Run structural validation and inspect every retained artifact before publishing.

## Decision rules

- Use high freedom for judgment-heavy work, medium freedom for preferred patterns, and low freedom for fragile deterministic operations.
- Create an adapter outside core frontmatter when a client needs non-standard metadata or invocation controls.
- Merge skills only when they share outcome, inputs, and completion evidence; preserve materially different strategies as modes or references.
- A newer, longer, more popular, or more opinionated upstream implementation is a candidate, not authority. Keep only the behavior that produces a demonstrated improvement without creating overlapping triggers or unjustified constraints.
- When a rule performs well only in one style, framework, model family, or operating environment, scope it there instead of promoting it to universal guidance.
- Treat the environment as authoritative for discoverable commands, paths, versions, and configuration; document only conventions, rationale, and gotchas that cannot be looked up reliably.
- Negative triggers are hard vetoes, so reserve them for genuinely incompatible intent. Do not use generic neighboring verbs or phases as negative triggers when a valid request can naturally contain both concepts; add mixed-intent regression coverage for important veto boundaries.

## Guardrails

- Do not hide prerequisites, privileged actions, network access, or destructive effects.
- Do not copy upstream scripts, templates, assets, or prose without checking their licenses and necessity.
- Do not add README-style process history inside an individual skill.
- Do not invent numeric thresholds, sample counts, retries, loop counts, file-size rules, or other gates merely to make a skill look precise.
- Do not improve a skill by accumulating guardrails for hypothetical failures; add or retain a rule because evidence shows it closes a real gap.

## Completion evidence

- The skill passes structural validation and has a non-empty decision-oriented body.
- Positive triggers select it, negative or boundary prompts do not misroute it, and baseline comparisons show useful improvement on explicit assertions.
- An improvement to an existing canonical skill preserves previously proven behavior unless the governing contract intentionally changed.
- Referenced files exist and deterministic scripts have been executed on representative cases when they are part of the implementation.

## Related skills

- `discover-agent-skills`
- `verify-completion`

## Conditional reference

Read [references/variants.md](references/variants.md) when the task depends on implementation strategy or runtime capability.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
