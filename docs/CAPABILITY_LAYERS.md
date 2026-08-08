# Capability Layers

The repository is not optimized for the number of tasks or products it can name. Its primary purpose is to improve agent judgment and reliable action.

Canonical skills therefore have different strategic roles even when they are all valid runtime skills.

## Layers

### 1. Meta capability

A meta capability improves how an agent thinks, learns, selects, checks, or coordinates across many unrelated tasks. This is the highest-priority evolution layer.

Current meta-capability owners:

- `create-agent-skill`
- `discover-agent-skills`
- `evaluate-agent`
- `clarify-requirements`
- `plan-implementation`
- `execute-plan`
- `diagnose-software`
- `review-code`
- `verify-completion`
- `prototype-solution`
- `research-primary-sources`
- `orchestrate-agent-work`
- `handoff-task-context`

A mechanism that can strengthen one of these across domains is normally more valuable than another narrow task adapter.

### 2. Reasoning workflow

A reasoning workflow owns a narrower outcome but still teaches reusable judgment rather than a product manual. These skills may contain domain concepts, but their main value is a decision process that cannot be replaced by looking up API syntax.

Current reasoning-workflow owners:

- `design-codebase`
- `model-domain`
- `review-api-design`
- `prepare-repository-for-agents`
- `develop-with-tdd`
- `optimize-performance`
- `simplify-code`
- `instrument-observability`
- `migrate-system-safely`
- `finish-development-branch`
- `coauthor-documents`
- `evaluate-scientific-evidence`
- `formulate-scientific-hypotheses`
- `review-security-practices`
- `threat-model-system`
- `design-frontend`
- `design-motion`
- `design-visual-theme`

These remain useful canonical skills, but they should not dominate source discovery merely because they have clear names or large source ecosystems.

### 3. Specialist operation

A specialist changes correctness for a specific artifact, protocol, tool family, runtime, or technical domain. Specialists are legitimate runtime capabilities, but breadth in this layer is not the project's success metric.

Current specialist owners:

- `build-mcp-server`
- `work-with-docx`
- `work-with-pdf`
- `work-with-pptx`
- `work-with-xlsx`
- `work-with-postgresql`
- `build-cli`
- `capture-screen`
- `resolve-merge-conflicts`
- `use-git-worktrees`
- `work-with-jupyter-notebook`
- `produce-programmatic-video`
- `map-security-ownership`
- `test-web-app`

A specialist should stay compact and defer version-sensitive facts to the live environment and current primary documentation whenever possible.

## Product/framework adapters

A product/framework adapter is below the three canonical priority layers. It primarily explains how to operate a named vendor product, SDK, API, cloud service, framework, or release-specific interface.

Product adapters belong in the source reservoir or an explicit optional specialist branch by default. They become canonical only when repeated evidence shows that:

- the task recurs materially;
- the capability cannot be recovered reliably from existing reasoning skills plus current primary documentation;
- the retained content includes real decision logic rather than syntax lookup;
- the extra runtime surface is worth its routing and maintenance cost.

Removing the product and API nouns is a useful test: if no reusable decision rule remains, do not promote the source as a capability-lift skill.

## Evolution priority

When several candidates are available, prefer review effort in this order:

```text
meta capability
    > reasoning workflow
        > specialist operation
            > product/framework adapter
```

This is a review priority, not an automatic quality score. A weak meta-level idea can still be rejected, and a specialist can still be essential for a real recurring task.

## Promotion pressure

A new source should first compete to strengthen an existing owner.

For a proposed new canonical skill, ask:

1. Is the outcome genuinely unowned?
2. Does the skill contain non-trivial decision logic that the agent cannot reliably reconstruct from the environment or primary documentation?
3. Does it improve future task behavior rather than merely expose knowledge?
4. Could the behavior be a mode, branch, reference, or specialist extension of an existing owner instead?
5. Would deleting the candidate leave the demonstrated capability gap open?

If the answer to the last question is no, do not add a new canonical owner.

## Runtime implications

The current library is small enough that model-native selection can inspect the compact metadata catalog directly.

If the library grows enough that flat metadata becomes noisy, preserve the strategic layers during hierarchical semantic discovery:

- expose meta capabilities directly;
- expose compact reasoning-workflow groups;
- expand specialist groups only when task intent makes them plausible;
- never expose unreviewed source candidates as runtime options.

This hierarchy reduces context competition without making a lexical router authoritative.

## Reclassification

Layer assignment is not permanent. Reclassify when evidence shows that a skill:

- contains more cross-task judgment than originally understood;
- has collapsed into version-sensitive operational instructions;
- can be absorbed into a stronger shared capability;
- no longer changes agent behavior beyond what current models and primary documentation already provide.

Reclassification may lead to strengthening, merging, specialist demotion, or deletion. Historical canonical status is not protection from compression.
