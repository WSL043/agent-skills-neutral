---
name: model-domain
description: "Model a problem domain with explicit concepts, invariants, state transitions, ownership, and ubiquitous language. Use when business rules are ambiguous, entities are overloaded, or implementation needs a durable domain model."
---

# Model Domain

## Goal

Create a domain model that makes rules and invalid states explicit before code structure hardens around ambiguity.

## Workflow

1. Collect real scenarios, terms, inputs, outputs, exceptions, and decisions from source material or stakeholders.
2. Build a glossary and resolve synonyms, overloaded terms, and actor-specific language.
3. Identify entities, values, policies, events, commands, and boundaries of consistency.
4. Write invariants and state transitions with valid and invalid examples.
5. Assign rule and data ownership; identify integrations and translation boundaries.
6. Validate the model against edge cases, then map it to code only after the language stabilizes.

## Decision rules

- Use a value object when identity is irrelevant and validity can be enforced at construction.
- Use an event when downstream behavior reacts to a completed fact; use a command for requested intent.
- Split bounded contexts when the same word has legitimately different rules or ownership.

## Guardrails

- Do not mirror database tables as the model by default.
- Do not invent business rules; label assumptions and seek evidence.

## Completion evidence

- The glossary, invariants, transitions, and ownership agree across examples.
- Previously ambiguous scenarios can be decided without ad hoc exceptions.

## Related skills

- `clarify-requirements`
- `design-codebase`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
