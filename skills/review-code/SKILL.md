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
4. Validate each potential finding against reachable behavior, existing safeguards, and the governing contract.
5. Report only actionable findings with severity, location, mechanism, impact, and a concrete correction or test. A material idea that fails the necessity test may be noted as optional, but is not required work.
6. After fixes, inspect the new diff and rerun focused checks before resolving feedback.

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

## Completion evidence

- Every required finding is tied to code, a plausible execution path, and an impact on the contract or binding constraints.
- Requirements, tests, and the final diff were all inspected.
- Resolved findings have fix evidence; unresolved risks are explicit.

## Related skills

- `verify-completion`
- `review-security-practices`

## Conditional reference

Read [references/variants.md](references/variants.md) when the task depends on implementation strategy or runtime capability.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
