---
name: finish-development-branch
description: "Finish a development branch by verifying scope, cleaning the diff, choosing an integration path, and preserving recoverability. Use when implementation is complete and the branch should be prepared for merge, review, handoff, or safe abandonment."
---

# Finish Development Branch

## Goal

Leave the branch in a verified, reviewable state with an explicit next integration action.

## Workflow

1. Inspect branch status, upstream, commits, untracked files, worktrees, and the full diff from the target base.
2. Run final tests, lint, build, and task-specific verification against the current branch.
3. Remove accidental artifacts, split or squash only when history policy requires it, and write a clear change summary.
4. Choose merge, pull request, handoff, keep-open, or abandon based on repository policy and user intent.
5. Push or integrate only with authorization; record commit and remote state.
6. Clean up worktrees or branches only after confirming the change is safely reachable.

## Decision rules

- Prefer a pull request when review, CI, or protected branches are part of the workflow.
- Keep the branch when blocked checks or unresolved review make integration premature.

## Guardrails

- Do not delete the only reachable copy of work.
- Do not push unrelated changes or secrets.
- Do not call a branch ready when required checks are skipped.

## Completion evidence

- The diff and commit range are intentional, required checks pass, and remote reachability is confirmed.
- The selected integration or handoff path is explicit.

## Related skills

- `use-git-worktrees`
- `review-code`
- `verify-completion`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
