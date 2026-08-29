# Semantic Workflow Activation

The thinking core is always active. Optional workflow activation is a semantic agent decision. Deterministic code may discover, filter, organize, and test candidate metadata, but it must not replace the model's understanding of the current cognitive outcome.

## Current runtime contract

Always expose `runtime/AGENTS.md` as the default thinking policy. For optional workflows, expose compact progressive-disclosure metadata:

```text
name
description
location
```

The agent compares workflow descriptions semantically, selects the single workflow that owns the current cognitive phase, then loads only that `SKILL.md` body and any conditionally required references. No workflow is a valid result when the core is sufficient or the request only needs replaceable operational knowledge.

Do not load all skill bodies merely to make a selection.

`runtime-catalog.json` is a portable metadata view for hosts that do not provide native skill discovery. A compatible host may discover the same metadata directly from skill frontmatter instead.

## Authority boundary

The model owns:

- interpreting the user's actual goal;
- distinguishing neighboring intents;
- deciding whether no skill is needed;
- choosing the semantic owner of the current blocking phase;
- deciding whether a second skill is materially necessary.

Deterministic infrastructure owns:

- finding available skills;
- validating metadata and paths;
- applying authorization or trust filters that are independent of semantic intent;
- reducing a very large library to a manageable candidate set;
- checking dependency and compatibility metadata;
- running offline routing regression cases;
- reporting model/router disagreement for later improvement.

A lexical fallback suggestion is evidence, not authority.

## Small-library mode

When compact metadata for the whole active library fits comfortably in context, prefer direct model-native selection from the complete metadata catalog. This avoids a retrieval layer becoming a second, weaker semantic router.

The model should select by outcome, decision boundary, required evidence, and exclusions rather than isolated term overlap.

## Scaling path

As the source or workflow library grows, do not respond by exposing every full body or by making keyword rules authoritative. Add structure progressively.

### Layer 1: semantic groups

Organize skills into stable capability groups with short model-facing summaries. A group is a navigation aid, not a hard partition: a task may inspect more than one plausible group when necessary.

Prefer groups based on reusable capability or outcome rather than vendor/product taxonomy.

### Layer 2: semantic shortlist

When a group still contains too many candidates, use semantic retrieval over `name + description + structural metadata` to produce a shortlist. Lexical evidence may contribute to recall but cannot hard-veto a semantically correct candidate.

The model makes the final selection from the shortlist.

### Layer 3: phase-aware owner transitions

When a task contains several cognitive phases, keep one semantic owner active at a time. A later phase may select a different workflow only after it becomes the current bottleneck; stop using the previous workflow body rather than composing both. Record incompatible or redundant paths in routing metadata, not as additional active skills.

Every workflow owns its own outcome, guardrails, and completion evidence. Cross-workflow relationships may remain in offline architecture or evaluation metadata, but task-time skill bodies must not instruct the agent to load neighboring workflows.

### Layer 4: graph/tree navigation

For very large libraries, build the capability tree or graph offline from reviewed canonical metadata. Inference-time traversal may narrow the search using semantic and structural signals under a context budget.

The graph is an index. It is not a source of new behavior and it cannot grant trust to an unreviewed skill.

## Core, workflow, and operational boundary

The always-on core owns reusable judgment across unrelated tasks, including:

- decomposition and planning;
- evidence search and weighting;
- hypothesis competition;
- uncertainty calibration;
- tool and strategy selection;
- failure localization and recovery;
- verification and stopping;
- orchestration and context control;
- skill evolution and evaluation.

Optional workflows add a distinct reasoning process for one active cognitive bottleneck. Operational knowledge such as exact commands, file-format procedures, SDK behavior, and domain facts stays outside canonical activation and is recovered from the live environment or current primary documentation.

## Description quality

Because the model selects skills semantically, descriptions are part of the deployed behavior.

A good description states:

- the outcome the skill owns;
- when it materially changes behavior;
- important boundaries that distinguish it from neighboring skills.

A description should not be a bag of search keywords. Adding synonyms only to satisfy a lexical test is a routing regression, not an improvement.

Evaluate descriptions on realistic should-use, should-not-use, and mixed-intent tasks with a fresh model-native selector.

## Atomic identity and naming

Treat each skill name as a stable routing API. Prefer a short `action-object` name that identifies one cognitive outcome, such as `review-code` or `verify-completion`; use another grammatical form only when it is materially clearer to a model.

- Keep one canonical name for one semantic owner. Source, vendor, model, tool, repository, and implementation-mode names do not create new canonical identities.
- Put lifecycle stages or runtime variants behind one owner when they share the same outcome and completion evidence. Split only when they require independently selectable reasoning processes.
- Reject names that describe a persona, collection, quality adjective, or vague capability without telling the selector what result it owns.
- Do not rename for cosmetic consistency. Rename only when realistic routing evidence shows ambiguity or when the owned outcome has materially changed; update every catalog, route, reference, deployment, and regression case atomically.
- A new upstream name is never evidence for a new skill. First attempt to strengthen the existing owner, then the always-on core, before approving another route.

## Router disagreement

Keep the deterministic router as a regression harness and weak-client fallback.

When model-native selection and the advisory router disagree:

1. inspect the task and both candidates;
2. determine which selection better owns the requested outcome;
3. if the model is correct, improve metadata or fallback heuristics only when doing so preserves other cases;
4. if the model is wrong, improve the description/boundary evidence or capability structure;
5. if neither can be settled reliably, keep the case unresolved rather than encoding a brittle lexical exception.

Do not force a capable model to imitate a weaker heuristic solely to make the test green.

## Trust boundary

Routing only chooses among already eligible canonical thinking workflows. Discovery candidates, upstream material, provenance references, operational adapters, and quarantined sources never become selectable merely because semantic retrieval finds them relevant.

Trust/promotion and runtime relevance are separate decisions.

## Success criterion

The activation system is successful when the thinking core handles ordinary tasks and the agent loads only the smallest workflow context that materially improves the requested outcome. Fewer model decisions are not inherently better; cheaper routing that consistently chooses the wrong workflow is a regression.
