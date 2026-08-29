---
name: review-code
description: "Review code changes for requirement fit, correctness, security, maintainability, and verification evidence; also prepare and process review feedback. Use for diffs, pull requests, patches, or pre-merge self-review."
---

# Review Code

## Goal

Produce prioritized, evidence-backed findings and a reviewed change whose remaining risks are explicit.

## Workflow

1. Fix the review scope to a verified diff or commit range and read the governing requirements, tests, and repository guidance. For a pull request, resolve the live base and exact head rather than inferring the base from the current branch; re-establish the range after a retarget, rebase, or merge.
2. Review requirement compliance separately from implementation quality so a polished wrong feature is still caught.
3. Trace changed data, control flow, error paths, permissions, concurrency, and compatibility boundaries across both sides of changed interfaces and through the shipped entry path. Follow enforcement to the final operation, and follow retained values through ownership, notifications, caches, and output views.
4. Validate each potential finding against reachable behavior, existing safeguards, and the governing contract. For bounds and invariants, inspect the owner of the complete emitted or retained result and require a negative case that fails for the intended rule rather than merely echoing the implementation.
5. Review changed documentation, comments, prompts, diagnostics, and visible strings semantically. Verify current-state claims against their owner, exercise safe documented operations when they are part of the contract, and remove authoring-session, review, or change narration that does not belong in an explicit history record.
6. Report only actionable findings with severity, location, mechanism, impact, and a concrete correction or test. A material idea that fails the necessity test may be noted as optional, but is not required work.
7. After fixes, inspect the new diff and rerun focused checks before resolving feedback.

## Decision rules

- Use self-review before requesting external review; use request-review mode to package scope and evidence.
- In receive-review mode, treat each comment and severity label as a claim; verify its technical and contract impact before accepting or rejecting it.
- Derive severity from demonstrated impact, not from who raised the issue.
- Separate blockers from optional improvements and style preferences.

## Guardrails

- Do not invent issues from unfamiliar patterns without proving impact.
- Do not promote a useful refactor, style preference, or hypothetical future concern into required work unless the contract or authoritative project policy makes it necessary.
- Do not hide uncertainty; state blocked checks and assumptions.
- Do not approve solely because tests are green.
- Do not treat a diff-scoping helper as semantic review; it identifies the changed surface but does not establish correctness.

## Completion evidence

- Every required finding is tied to code, a plausible execution path, and an impact on the contract or binding constraints.
- Requirements, tests, and the final diff were all inspected.
- Behavioral evidence exercises the shipped entry path where relevant, and its negative controls fail for the intended defect or rule.
- The reviewed base/head range is explicit and still matches the final change state.
- Resolved findings have fix evidence; unresolved risks are explicit.

## Conditional reference

Read [references/variants.md](references/variants.md) when the task depends on implementation strategy or runtime capability.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
