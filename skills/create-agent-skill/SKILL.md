---
name: create-agent-skill
description: "Create or revise portable Agent Skills with standard SKILL.md frontmatter, concise trigger descriptions, progressive disclosure, reusable resources, and evidence-based validation. Use when designing, consolidating, testing, or improving an agent skill or skill library."
---

# Create Agent Skill

## Goal

Produce a focused, portable skill whose behavior is more reliable than an unstructured prompt or the current canonical implementation it is intended to improve.

## Workflow

1. Define the behavioral claim before writing instructions. Collect representative positive triggers, boundary cases, near-misses, and the completion evidence that would show the skill helped rather than merely sounded plausible.
2. For an existing capability, gather execution evidence before editing. Prefer a diverse pool of successful and failed trajectories over reacting to one anecdote. Extract trajectory-local lessons first, then consolidate repeated patterns, conflicts, and exceptions into candidate rules.
3. Choose the smallest reusable unit and a verb-led kebab-case name. Prefer strengthening an existing semantic owner or shared mechanism over creating another trigger; split only genuinely different outcomes.
4. Put only name and description in core frontmatter. Treat the description as the model-facing routing contract: describe user intent and when the skill helps, not a keyword list or internal implementation. Put branch-specific detail in references and deterministic repetition in scripts.
5. Write or revise the minimum decision workflow. Preserve proven instructions by default and make bounded add/delete/replace changes tied to observed evidence instead of rewriting the whole skill for stylistic consistency. Let repository files, config, command help, and current primary documentation remain the source of truth for facts they expose.
6. Define evaluation assertions before inspecting candidate results. Keep the experience used to propose edits separate from held-out tasks used to decide whether the edit survives. Compare the candidate against no-skill for a new capability or the current canonical implementation for an improvement.
7. Accept an edit only when its claimed behavior improves without material regression on previously proven behavior. If the evidence is mixed, narrow or reject the edit rather than averaging away the failure. Preserve a concise negative lesson for rejected edits when it prevents the same failed idea from being rediscovered later.
8. When several local lessons survive, curate them incrementally: merge duplicates, resolve contradictions by scope or branch conditions, remove rules whose deletion does not change behavior, and keep the smallest playbook that explains the observed gain.
9. Give every retained step a clear, checkable completion criterion and enough demand to account for every file, case, or claim material to the skill's stated contract. Run structural validation and inspect every retained artifact before publishing.

## Decision rules

- Skill evolution is an evidence loop, not prompt polishing: experience -> local lessons -> consolidated mechanism -> bounded edit -> held-out validation -> retain/reject.
- Do not generalize from one trajectory when the claimed rule is meant to transfer. Seek contrasting executions and, for a cross-domain claim, at least one held-out context outside the source domain.
- Preserve trajectory diversity before synthesis. A successful path can reveal a useful strategy; a failed path can reveal a boundary; neither alone defines the universal rule.
- Prefer incremental curation to full rewrites so proven detail is not silently dropped. Rewrite broadly only when the structure itself is the demonstrated failure.
- Use high freedom for judgment-heavy work, medium freedom for preferred patterns, and low freedom for fragile deterministic operations.
- Create an adapter outside core frontmatter when a client needs non-standard metadata or invocation controls.
- Merge skills only when they share outcome, inputs, and completion evidence; preserve materially different strategies as modes or references.
- A newer, longer, more popular, or more opinionated upstream implementation is a candidate, not authority. Keep only the behavior that produces a demonstrated improvement without creating overlapping semantic owners or unjustified constraints.
- When a rule performs well only in one style, framework, model family, or operating environment, scope it there instead of promoting it to universal guidance.
- Treat the environment as authoritative for discoverable commands, paths, versions, and configuration; document only conventions, rationale, and gotchas that cannot be looked up reliably.
- Descriptions carry the model-facing activation burden. Optimize them against realistic should-use and near-miss tasks; do not depend on a harness-side keyword router to rescue an ambiguous description.
- Negative routing metadata is a test aid, not a semantic law. A valid mixed-intent task may contain neighboring vocabulary that would be unsafe as a hard lexical veto.

## Guardrails

- Do not hide prerequisites, privileged actions, network access, or destructive effects.
- Do not copy upstream scripts, templates, assets, or prose without checking their licenses and necessity.
- Do not add README-style process history inside an individual skill.
- Do not invent numeric thresholds, sample counts, retries, loop counts, file-size rules, score targets, or other gates merely to make a skill-evolution loop look precise.
- Do not improve a skill by accumulating guardrails for hypothetical failures; add or retain a rule because evidence shows it closes a real gap.
- Do not train and validate an edit on the same small set of trajectories and call the result generalization.
- Do not keep a candidate edit because it improved an aggregate score while creating a material regression hidden inside the average.

## Completion evidence

- The skill passes structural validation and has a non-empty decision-oriented body.
- Its description gives a capable agent enough intent-level information to select it semantically from neighboring skills.
- Representative activation tasks select it, near-miss tasks do not, and model-native routing is evaluated separately from the advisory lexical harness where both are available.
- Baseline comparisons show useful improvement on explicit assertions, with proposal evidence separated from held-out acceptance evidence for evolved skills.
- An improvement to an existing canonical skill preserves previously proven behavior unless the governing contract intentionally changed.
- Retained rules can be traced to repeated or otherwise material execution evidence; rejected high-risk edits have enough negative memory to avoid needless rediscovery.
- Referenced files exist and deterministic scripts have been executed on representative cases when they are part of the implementation.

## Related skills

- `discover-agent-skills`
- `evaluate-agent`
- `verify-completion`

## Conditional reference

Read [references/variants.md](references/variants.md) when the task depends on implementation strategy or runtime capability.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
