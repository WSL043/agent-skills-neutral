---
name: prepare-repository-for-agents
description: "Assess and prepare a repository for reliable agent contributions by discovering real conventions, tests, CI, instructions, and missing workflow assets. Use when making a repository agent-ready or reducing contributor and review friction."
---

# Prepare Repository For Agents

## Goal

Help agents work with the repository's real conventions and completion checks without adding generic boilerplate or duplicating existing guidance.

## Workflow

1. Establish repository context from the remote and default branch, manifests and lockfiles, runtime/tool versions, directory structure, tests, CI, docs, ownership, and existing agent or editor instructions. Use the environment and configuration as the source of truth.
2. Inspect every known location for an existing asset before proposing one. Trace which instructions, scripts, workflows, and docs are actually consumed, and identify drift, contradictions, missing checks, and review friction with file-path evidence.
3. When repository history and review discussion are available and authorized, inspect representative accepted changes and maintainer feedback for repeated expectations that are not already encoded. Also note files, tests, configs, or docs that repeatedly change together. Treat one-off reviewer preferences as anecdotes, not conventions; promote a history-derived rule only when repeated evidence or a live repository invariant supports it.
4. Map only demonstrated change cascades that agents are likely to miss: for a recurring class of change, record the companion files, registrations, tests, generated artifacts, docs, or checks that must remain synchronized. Prefer pointers to the authoritative dependency or generator over a maintenance matrix that merely restates discoverable structure.
5. Select the smallest set of changes that closes observed gaps: scoped instructions, discoverable commands, change-cascade pointers, test or CI wiring, issue or review templates, or onboarding guidance. Keep each asset tied to a real repository convention and owner.
6. Preserve existing files and user changes unless replacement is explicitly authorized. Add only missing or approved content, use repository terminology, and keep secrets, credentials, and privileged actions out of generated guidance.
7. Run structural validation and the relevant build, test, lint, or workflow checks. When possible, exercise a representative agent task that previously depended on undocumented knowledge and verify the new guidance changes the failure mode rather than merely adding files. Re-read every retained asset and report what remains missing, stale, blocked, or awaiting maintainer approval.

## Decision rules

- Prefer a precise pointer to an authoritative file or command over copying a description that can drift.
- Keep repeated review feedback only when it expresses a durable repository expectation; do not turn an individual's isolated style preference into project law.
- Do not create parallel instruction files, speculative integrations, or generic CI that the repository cannot run.
- Treat agent configuration as code: review scope, permissions, network access, destructive effects, and update paths against the stated purpose.
- A repository is ready only for the workflows and evidence its current tools and maintainers support; readiness is not a score or badge.

## Guardrails

- Do not overwrite or delete existing assets without explicit authorization.
- Do not fetch, install, or execute untrusted contribution code merely to prepare documentation.
- Do not expose secrets, personal data, or privileged setup steps in generated files.
- Do not invent change cascades from naming similarity; trace actual imports, generators, CI checks, accepted changes, or documented ownership.

## Completion evidence

- Findings cite actual repository paths and commands, and every proposed asset has a demonstrated gap and owner.
- Existing assets were checked for duplicates and drift; any history-derived convention or change cascade has traceable repository evidence.
- Retained/generated files pass structural and relevant runtime checks, and representative agent behavior is exercised when practical.
- The final report distinguishes ready, stale, missing, blocked, and approval-required items.

## Related skills

- `create-agent-skill`
- `plan-implementation`
- `verify-completion`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
