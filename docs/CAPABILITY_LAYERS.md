# Capability Layers

The project has one durable subject: how an agent thinks. Runtime therefore has two canonical layers and one explicit non-canonical boundary.

## 1. Always-on thinking core

[`../runtime/AGENTS.md`](../runtime/AGENTS.md) is the default policy for every task. It is deliberately compact and cross-domain. It governs:

- task-contract framing and authority boundaries;
- fact, inference, hypothesis, and unknown separation;
- competing explanations and discriminating evidence;
- next-action choice by information value, risk, cost, and safe recoverability;
- verification at the consumed or observed surface;
- correction, recovery, claim narrowing, learning, and stopping.

The core is not a skill and cannot fail to activate because routing missed a keyword. It contains only behavior the model should carry across unrelated tasks.

## 2. Optional thinking workflows

A workflow owns a distinct cognitive outcome that benefits from a fuller process than the core can carry economically. Examples include root-cause diagnosis, threat modeling, evidence appraisal, implementation planning, collaborative writing, interface design, migration reasoning, and agent evaluation.

The scenario set is open-ended. Categories organize current owners; they are not a claim that every future situation is already enumerated. A new scenario becomes canonical only when its reasoning result is independently useful and cannot be expressed cleanly as a branch of the core or an existing workflow.

Every workflow remains on demand. `S` means high-transfer and `A` means scenario-specific; neither means always loaded.

## 3. Non-canonical operational knowledge

The following are useful but replaceable and therefore stay outside canonical runtime:

- exact tool commands, flags, SDK calls, and provider setup;
- file-format manipulation recipes;
- product or framework manuals;
- technology-specific installation and maintenance procedures;
- domain facts that current primary sources or the live environment can supply.

Agents obtain these from host capabilities, repository instructions, current official documentation, and observed runtime state. Canonical reasoning decides what evidence is needed and how to verify it; it does not duplicate every mechanism for obtaining that evidence.

Operational material may still contribute a transferable rule. For example, document, browser, media, and spreadsheet workflows all support the general rule “verify the rendered or consumed result”; database and Git operations support “preserve invariants and a safely recoverable path.” Those rules belong in the core or an existing thinking workflow, while the format- or command-specific manual does not.

## Deletion test

For any proposed canonical entry, ask:

1. Remove product, framework, file-format, tool, provider, and domain nouns. What reasoning behavior remains?
2. Does that behavior change a decision, evidence requirement, recovery path, or stopping condition?
3. Is it already present in the thinking core or an existing workflow?
4. If the candidate is removed, does controlled or repeated evidence show a meaningful behavior loss?
5. When transfer is claimed, does the loss and recovery appear on a contrasting or held-out task?

If no independent behavior remains, reject the canonical route. If a rule remains but has no independent outcome, strengthen the core or existing owner. Add a workflow only when both the outcome and evidence justify it.

## Activation boundary

```text
always-on runtime/AGENTS.md
          |
          v
identify current cognitive bottleneck
          |
          +---- core sufficient / direct tool lookup ----> no workflow
          |
          v
runtime-catalog.json metadata
          |
          v
smallest useful thinking workflow
          |
          v
selected SKILL.md body only
```

`routes/*.json` and `select_skills.py` provide navigation, diagnostics, regression evidence, and weak-client fallback. They do not define task-time semantic authority.

## Reclassification

Canonical status is not permanent. Repeated real-task evidence may strengthen, merge, narrow, or remove a workflow. A source with useful operational detail can remain available through its original project or current documentation without occupying this runtime. Git history preserves removed implementations; canonical context does not need to preserve them as an archive.
