# Provenance Model

Provenance answers where retained behavior came from. It is not a runtime dependency graph and it is not a public comparison ledger.

## Two source roles

The project distinguishes direct skill sources from mechanism-only research sources.

### Direct skill source

A direct skill source publishes Agent Skills or comparable reusable instructions that are reviewed as a continuing source reservoir.

Its state is split across:

- `upstreams.json:last_reviewed_commit` — how far the configured source focus has been reviewed;
- `provenance.json:source_snapshots` — exact repository snapshots referenced by retained canonical lineage;
- per-skill provenance entries — exact files/paths/commits that materially shaped retained behavior.

A direct source may be fully reviewed without contributing anything new. Conversely, a specific path may contribute retained behavior while the broader repository remains unreviewed.

### Mechanism-only research source

A mechanism source is inspected for a transferable evaluator, optimizer, reasoning, routing, memory, learning, distillation, verification, or other architecture mechanism. It does not need to be treated as a continuing Agent Skill upstream.

Mechanism sources belong only in provenance when they materially shaped retained behavior. They must not be added to `upstreams.json` merely so validation can reference them.

Use a separate top-level `mechanism_snapshots` mapping in `provenance.json`:

```json
{
  "source_snapshots": {
    "owner/direct-skill-source": "<commit>"
  },
  "mechanism_snapshots": {
    "owner/mechanism-research": "<commit>"
  }
}
```

A per-skill mechanism provenance entry should include:

```json
{
  "source_kind": "mechanism",
  "repository": "owner/repository",
  "path": "path/to/relevant/source",
  "commit": "<exact commit>",
  "url": "<commit-pinned URL>",
  "adaptation_note": "What transferable mechanism was retained and what source assumptions were excluded."
}
```

When an applicable source license is known and material to adaptation, record `license` and `license_url`. If the repository's licensing signal is incomplete or ambiguous, do not manufacture a license conclusion; record an explicit `license_note` and ensure no upstream code, prose, template, or asset is copied under uncertain permission.

## Validation rules

`source_snapshots` and `mechanism_snapshots` are disjoint repository sets.

For direct source provenance:

- repository must appear in `source_snapshots`;
- repository must also appear in `upstreams.json`;
- per-entry commit and URL must be pinned;
- `upstreams.json` remains the only review-progress authority.

For mechanism provenance:

- `source_kind` must be `mechanism`;
- repository must appear in `mechanism_snapshots`;
- repository does not need to appear in `upstreams.json`;
- commit and URL must be pinned;
- the adaptation note must state the retained mechanism and excluded source-specific assumptions;
- mechanism provenance creates no automatic recurring review obligation.

A repository cannot silently switch roles. If a mechanism repository later becomes a tracked direct skill source, migrate its role explicitly rather than duplicating it in both snapshot maps.

## What provenance does not mean

A provenance pointer does not mean:

- the source is globally trusted;
- the whole repository was reviewed;
- the source is a runtime dependency;
- the external implementation is installed or executed;
- the source's benchmark result transfers to this project;
- the project adopts the source's terminology, thresholds, architecture, or product assumptions.

It means only that a pinned source materially informed retained project behavior.

## Architecture-only lessons

Not every useful external observation needs provenance in a canonical skill.

If an external mechanism changes only project architecture, evaluation infrastructure, or review policy and no canonical skill retains behavior from it, the normalized project-native rule may be sufficient. Do not create an adjacent-project history file merely for completeness.

When the mechanism materially changes a canonical skill, record the source in that skill's provenance so later audits can distinguish independently invented behavior from source-informed synthesis.

## License boundary

The project normally retains decision rules and mechanism abstractions, not source prose or executable artifacts.

License still matters. Before copying or closely adapting code, templates, scripts, or substantial text, verify permission at the exact source path/snapshot. A downstream repository's claimed license does not automatically license material it copied from another source.

For conceptual mechanism synthesis where no protected source artifact is bundled, keep the provenance pointer and describe the transformation accurately; do not falsely claim a license review that was not completed.

## Public-release boundary

If a future public release is prepared, audit every retained lineage by exact path and commit. Mechanism provenance belongs in that audit, but it should remain provenance—not marketing copy or a named "projects we learned from" section.
