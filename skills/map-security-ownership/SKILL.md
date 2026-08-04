---
name: map-security-ownership
description: "Map security-sensitive code and assets to maintainers using repository history, dependency paths, and risk boundaries. Use for security ownership analysis, bus-factor review, sensitive-area stewardship, or CODEOWNERS gap assessment."
---

# Map Security Ownership

## Goal

Produce an evidence-backed ownership map that identifies unowned sensitive areas and concentration risk.

## Workflow

1. Define sensitive paths and assets from the threat model, secrets, authentication, authorization, cryptography, build, deployment, and data boundaries.
2. Collect current ownership files, repository history, review activity, and organizational mappings.
3. Attribute meaningful changes and reviews over a representative time window, accounting for renames and generated/vendor code.
4. Build file-to-owner and sensitive-area-to-owner mappings with confidence and recency.
5. Calculate concentration, orphaned paths, inactive ownership, and single-maintainer hotspots.
6. Validate surprising assignments with maintainers before changing policy.

## Decision rules

- Weight substantive changes and reviews more than mechanical commits.
- Separate formal ownership from observed stewardship; report both when they differ.

## Guardrails

- Do not publish personal risk conclusions beyond the authorized audience.
- Do not infer expertise from commit count alone.
- Do not automatically rewrite CODEOWNERS from an unreviewed statistical map.

## Completion evidence

- Every sensitive area has formal and observed owner evidence or is marked unowned.
- Bus-factor and confidence calculations can be reproduced from recorded inputs.

## Related skills

- `threat-model-system`
- `review-security-practices`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
