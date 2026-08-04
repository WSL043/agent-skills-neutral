---
name: use-git-worktrees
description: "Create and manage isolated Git worktrees for parallel branches without disturbing the current checkout. Use when work needs separate dependency state, concurrent agents, or safe branch isolation."
---

# Use Git Worktrees

## Goal

Create a verified isolated checkout with a clear branch, path, baseline, and cleanup plan.

## Workflow

1. Inspect repository status, remotes, existing worktrees, branch names, and ignore rules.
2. Choose an explicit path outside build output and confirm it does not contain unrelated data.
3. Create or attach the intended branch with `git worktree add` and verify the resolved path.
4. Install dependencies inside the worktree only when needed and keep caches appropriately shared or isolated.
5. Run a baseline check before making changes so pre-existing failures are recorded.
6. After integration, remove the worktree deliberately and prune only stale administrative entries.

## Decision rules

- Use a new branch for implementation; use detached state only for read-only inspection.
- Keep simultaneous tasks in separate worktrees when they need different branches or generated state.

## Guardrails

- Do not recursively delete a path until its absolute location and worktree registration are verified.
- Do not create a worktree inside another worktree.
- Do not reuse a branch already checked out elsewhere.

## Completion evidence

- `git worktree list` shows the expected path and branch.
- The baseline status is clean or all existing changes are accounted for.

## Related skills

- `finish-development-branch`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
