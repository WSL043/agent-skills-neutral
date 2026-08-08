# Semantic Skill Routing

Skill activation is a semantic agent decision. Deterministic code may discover, filter, organize, and test candidate metadata, but it must not replace the model's understanding of the user's requested outcome.

## Current runtime contract

For the current library size, expose compact progressive-disclosure metadata:

```text
name
description
location
```

The agent compares skill descriptions semantically, selects the smallest useful skill set, then loads only the selected `SKILL.md` bodies and any conditionally required references.

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

As the source or specialist library grows, do not respond by exposing every full skill or by making keyword rules authoritative. Add structure progressively.

### Layer 1: semantic groups

Organize skills into stable capability groups with short model-facing summaries. A group is a navigation aid, not a hard partition: a task may inspect more than one plausible group when necessary.

Prefer groups based on reusable capability or outcome rather than vendor/product taxonomy.

### Layer 2: semantic shortlist

When a group still contains too many candidates, use semantic retrieval over `name + description + structural metadata` to produce a shortlist. Lexical evidence may contribute to recall but cannot hard-veto a semantically correct candidate.

The model makes the final selection from the shortlist.

### Layer 3: dependency-aware bundles

When tasks routinely require multiple cooperating skills, represent meaningful dependency or role relationships separately from activation descriptions. Retrieval may return a compact bundle such as:

```text
start: primary semantic owner
support: distinct second-phase capability
check: verification or evaluation capability
avoid: known incompatible or redundant path
```

These roles describe an execution relationship; they do not make every related skill mandatory.

### Layer 4: graph/tree navigation

For very large libraries, build the capability tree or graph offline from reviewed canonical metadata. Inference-time traversal may narrow the search using semantic and structural signals under a context budget.

The graph is an index. It is not a source of new behavior and it cannot grant trust to an unreviewed skill.

## Capability layer and specialist layer

The library should distinguish reusable agent capability from specialist operational knowledge.

### Capability layer

Prioritize skills or mechanisms that improve reusable judgment across unrelated tasks, including:

- decomposition and planning;
- evidence search and weighting;
- hypothesis competition;
- uncertainty calibration;
- tool and strategy selection;
- failure localization and recovery;
- verification and stopping;
- orchestration and context control;
- skill evolution and evaluation.

This layer defines the project's quality direction.

### Specialist layer

Specialists encode knowledge that changes correctness or completion in a narrower task family, format, protocol, technology, or domain.

Specialists remain valuable, but catalog breadth in this layer is not the project goal. Prefer expanding a specialist branch only when a real task requires knowledge that cannot be recovered reliably from the capability layer plus current primary documentation.

A future host may expose the capability layer first and expand specialist metadata only when the task indicates that a specialist branch is relevant.

## Description quality

Because the model selects skills semantically, descriptions are part of the deployed behavior.

A good description states:

- the outcome the skill owns;
- when it materially changes behavior;
- important boundaries that distinguish it from neighboring skills.

A description should not be a bag of search keywords. Adding synonyms only to satisfy a lexical test is a routing regression, not an improvement.

Evaluate descriptions on realistic should-use, should-not-use, and mixed-intent tasks with a fresh model-native selector.

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

Routing only chooses among already eligible canonical skills. Discovery candidates, upstream material, provenance references, and quarantined sources never become selectable merely because semantic retrieval finds them relevant.

Trust/promotion and runtime relevance are separate decisions.

## Success criterion

The routing system is successful when the agent loads the smallest context that materially improves the requested outcome, while semantic choice remains robust as the library grows. Fewer model decisions are not inherently better; cheaper routing that consistently chooses the wrong workflow is a regression.
