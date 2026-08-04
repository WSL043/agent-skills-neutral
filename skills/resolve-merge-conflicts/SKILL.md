---
name: resolve-merge-conflicts
description: "Resolve Git merge or rebase conflicts by reconstructing intent from both sides, preserving invariants, and validating the integrated result. Use when a branch contains textual, semantic, rename, or generated-file conflicts."
---

# Resolve Merge Conflicts

## Goal

Produce an integrated change that preserves intended behavior from both histories rather than merely removing conflict markers.

## Workflow

1. Record the merge/rebase state, target branches, conflict list, renames, and unrelated working-tree changes.
2. Inspect the base, ours, theirs, and relevant commits to understand each side's intent.
3. Resolve source conflicts by integrating behavior and invariants, not by choosing a whole side blindly.
4. Regenerate derived files from the resolved source instead of manually merging generated output when possible.
5. Search for conflict markers and inspect the complete resulting diff.
6. Run focused tests for both change sets, then broader repository checks.

## Decision rules

- Prefer rename-aware history when a delete/add conflict may represent a moved file.
- Pause when both sides intentionally changed the same contract in incompatible ways.

## Guardrails

- Do not discard unrelated user changes or use destructive reset operations.
- Do not resolve lockfiles independently of their manifests unless the ecosystem requires it.
- Do not mark resolved before semantic tests pass.

## Completion evidence

- Git reports no unmerged paths or conflict markers.
- The final diff can be explained in terms of both original intents.
- Tests covering both sides pass.

## Related skills

- `review-code`
- `verify-completion`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
