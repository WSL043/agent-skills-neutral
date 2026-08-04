---
name: configure-pre-commit
description: "Configure repository pre-commit checks that are fast, reproducible, and aligned with existing CI. Use when adding or repairing local commit-time linting, formatting, validation, or secret checks."
---

# Configure Pre Commit

## Goal

Create a low-friction pre-commit gate that catches cheap deterministic failures without blocking normal work unnecessarily.

## Workflow

1. Inspect existing package managers, formatter/linter configs, CI jobs, generated files, and contributor workflows.
2. Select only fast deterministic checks suitable for changed files.
3. Pin hook or tool versions and reuse repository-native commands where possible.
4. Configure file filters, exclusions, language runtimes, and autofix behavior explicitly.
5. Run against representative changed files and once against the full repository.
6. Ensure CI independently runs equivalent checks so local bypass does not remove protection.

## Decision rules

- Move slow integration, network, or platform-dependent tests to pre-push or CI.
- Allow automatic formatting when the resulting diff is deterministic and visible.

## Guardrails

- Do not download unpinned executable code during every commit.
- Do not mutate unrelated files silently.
- Do not treat local hooks as the only enforcement layer.

## Completion evidence

- A clean checkout can install and run hooks using documented repository commands.
- Known-bad fixtures fail and corrected files pass locally and in CI-equivalent checks.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
