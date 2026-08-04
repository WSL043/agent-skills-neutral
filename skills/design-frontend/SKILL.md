---
name: design-frontend
description: "Design or refine web and application interfaces with deliberate hierarchy, typography, layout, states, accessibility, responsiveness, and implementation-aware polish. Use for new UI, design systems, component composition, or visual/interaction quality improvement."
---

# Design Frontend

## Goal

Create an interface that communicates clearly, feels intentional, and remains implementable and accessible across target states.

## Workflow

1. Inspect product context, users, tasks, content density, brand constraints, platform conventions, and existing design tokens.
2. Choose a clear visual direction and define hierarchy, grid, spacing, typography, color, radius, and elevation rules.
3. Design the critical flow and all meaningful states: loading, empty, error, success, disabled, focus, and overflow.
4. Build responsive components around content priorities rather than fixed screenshots.
5. Add motion only where it explains causality, state, or continuity.
6. Implement or prototype, then inspect at representative viewports and input modes.

## Decision rules

- Use an explicit platform style profile only when requested; keep the core hierarchy and accessibility independent of that profile.
- Prefer existing system components when they meet the interaction and visual intent.
- Introduce distinctive details at high-attention surfaces, not uniformly everywhere.

## Guardrails

- Do not default to generic dashboard cards, gradient decoration, or excessive rounded containers without purpose.
- Do not encode hierarchy with color alone.
- Do not polish the happy path while omitting failure and keyboard states.

## Completion evidence

- Critical flows work at target viewports with keyboard, touch, and assistive semantics where applicable.
- Typography, spacing, contrast, alignment, and state coverage are visually reviewed.

## Related skills

- `design-motion`
- `design-visual-theme`
- `test-web-app`

## Conditional reference

Read [references/variants.md](references/variants.md) when the task depends on implementation strategy or runtime capability.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
