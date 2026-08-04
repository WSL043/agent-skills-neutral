# Agent Instructions

This repository is a vendor-neutral Agent Skills reference library.

## Loading protocol

1. Prefer `python scripts/select_skills.py "<task>" --json` and use its `primary` route.
2. If scripts cannot run, read `index.json`, choose one likely category, then read only its `route_file`. Do not start with the full `catalog.json`.
3. Read the selected `skills/<name>/SKILL.md` completely before acting.
4. Add at most one `support` skill when the task has a distinct second phase. Treat `alternatives` as fallbacks, not additional context.
5. Load B-level `conditional` or `experimental` skills only after an exact task/technology trigger. Never infer them from a generic request.
6. Read `references/variants.md` only when that SKILL.md links it and the implementation choice matters.
7. Treat `provenance.json` and upstream URLs as attribution, not executable instructions. Do not fetch or execute upstream scripts without a separate trust and license review.

For a persistent installation, start with the six entries in `profiles/default.txt`. Add one domain profile or routed skill only when demand justifies it.

## Priority levels

- `S`: reusable core workflow; six form the default task loop, while the remaining S skills stay on demand.
- `A`: high-value task-domain workflow; load on demand.
- `B`: specialist workflow; load only for an explicit matching task.

Priority is not permission. Preserve user authorization, repository guidance, runtime safety, and tool-specific approval boundaries.

## Integration rules

- Keep one canonical trigger per capability. Do not install overlapping source skills beside the canonical skill.
- Keep routing metadata in `routes/*.json`; do not inflate SKILL.md bodies with discovery synonyms.
- Put client-specific invocation controls and UI metadata in adapters, not in core SKILL.md frontmatter.
- Prefer fresh runtime or rendered evidence over configuration-only claims.
- Label facts, inference, and blocked checks separately.
- Do not use proprietary API or SaaS adapters unless the task explicitly requests that provider.
