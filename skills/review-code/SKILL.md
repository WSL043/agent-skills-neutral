---
name: review-code
description: "Review code changes for requirement fit, correctness, security, maintainability, and verification evidence; also prepare and process review feedback. Use for diffs, pull requests, patches, or pre-merge self-review."
---

# Review Code

## Goal

Produce prioritized, evidence-backed findings and a reviewed change whose remaining risks are explicit.

## Workflow

1. Fix the review scope to a diff or commit range and read the governing requirements, tests, and repository guidance.
2. Review requirement compliance separately from implementation quality so a polished wrong feature is still caught.
3. Trace changed data, control flow, error paths, permissions, concurrency, and compatibility boundaries.
4. Validate each potential finding against reachable behavior and existing safeguards.
5. Report only actionable findings with severity, location, mechanism, impact, and a concrete correction or test.
6. After fixes, inspect the new diff and rerun focused checks before resolving feedback.

## Decision rules

- Use self-review before requesting external review; use request-review mode to package scope and evidence.
- In receive-review mode, verify the comment technically before accepting or rejecting it.
- Separate blockers from optional improvements and style preferences.

## Guardrails

- Do not invent issues from unfamiliar patterns without proving impact.
- Do not hide uncertainty; state blocked checks and assumptions.
- Do not approve solely because tests are green.

## Completion evidence

- Every finding is tied to code and a plausible execution path.
- Requirements, tests, and the final diff were all inspected.
- Resolved findings have fix evidence; unresolved risks are explicit.

## Related skills

- `verify-completion`
- `review-security-practices`

## Conditional reference

Read [references/variants.md](references/variants.md) when the task depends on implementation strategy or runtime capability.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
