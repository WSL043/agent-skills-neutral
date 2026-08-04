---
name: create-agent-skill
description: "Create or revise portable Agent Skills with standard SKILL.md frontmatter, concise trigger descriptions, progressive disclosure, reusable resources, and evidence-based validation. Use when designing, consolidating, testing, or improving an agent skill or skill library."
---

# Create Agent Skill

## Goal

Produce a focused, portable skill whose behavior is more reliable than an unstructured prompt.

## Workflow

1. Collect two or three concrete trigger prompts and at least one prompt that must not trigger the skill.
2. Choose the smallest reusable unit and a verb-led kebab-case name; split unrelated outcomes into separate skills.
3. Put only name and description in core frontmatter. Put trigger conditions in description, not in a body section.
4. Write the minimum decision workflow in SKILL.md. Move detailed variants to references and deterministic repetition to scripts.
5. Test representative prompts with and without the skill, compare outputs against explicit assertions, and revise the instructions that caused the gap.
6. Run a standards validator and inspect every generated file before publishing.

## Decision rules

- Use high freedom for judgment-heavy work, medium freedom for preferred patterns, and low freedom for fragile deterministic operations.
- Create an adapter outside core frontmatter when a client needs non-standard metadata or invocation controls.
- Merge skills only when they share outcome, inputs, and completion evidence; preserve materially different strategies as modes or references.

## Guardrails

- Do not hide prerequisites, privileged actions, network access, or destructive effects.
- Do not copy upstream scripts, templates, or prose without checking their licenses.
- Do not add README-style process history inside an individual skill.

## Completion evidence

- The skill passes structural validation and has a non-empty body.
- Positive triggers select it, negative triggers do not, and baseline comparisons show a useful improvement.
- Referenced files exist and scripts have been executed on at least one representative case.

## Related skills

- `discover-agent-skills`
- `verify-completion`

## Conditional reference

Read [references/variants.md](references/variants.md) when the task depends on implementation strategy or runtime capability.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
