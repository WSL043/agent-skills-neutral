---
name: design-frontend
description: "Design, implement, audit, or redesign web and application interfaces with a coherent visual direction, faithful reference translation, complete states, accessibility, responsiveness, and rendered QA. Use for new UI, visual redesign, image-to-code work, design systems, component composition, or anti-generic interface polish."
---

# Design Frontend

## Goal

Create an interface whose visual choices follow the product brief, whose implementation preserves those choices, and whose critical states remain usable across target viewports and input modes.

## Workflow

1. Inspect the product, audience, task, content, brand, existing routes/components/tokens, real assets, platform conventions, and target viewports.
2. Write a one-line design read: visual concept, hierarchy, density, motion level, and what should remain quiet. Ask one question only when a missing choice materially changes the direction.
3. Choose either an established design system or one coherent aesthetic direction. Define semantic type, color, spacing, grid, shape, imagery, and interaction rules before polishing components.
4. Design the critical flow plus loading, empty, error, success, disabled, focus, overflow, long-content, and permission states that actually apply.
5. If a visual reference is the source of truth, analyze its structure and regenerate a clearer reference only when unreadable details would otherwise be guessed.
6. Implement responsive components around content priority and existing architecture. Preserve information architecture and behavior during redesign unless structural change is approved.
7. Render and inspect representative viewports, keyboard/touch behavior, assistive semantics, real content, and performance-sensitive paths. Compare the result to the design read or source reference and correct drift.

## Decision rules

- Use real brand/product assets when they exist; generate or source new media only when it has a defined narrative or structural role.
- Prefer existing system components when they meet interaction and visual intent; extend deliberately when a high-attention surface needs distinction.
- Tune visual variance, motion, and density to the brief instead of applying fixed defaults.
- Treat an image as a design reference, not as a substitute for responsive behavior or accessible semantics.

## Guardrails

- Do not default to repetitive card rows, nested rounded containers, decorative pills, generic gradients, fake technical labels, or one composition repeated through every section.
- Do not encode hierarchy with color alone.
- Do not impose arbitrary universal style bans, forced image counts, mandatory dark mode, a fixed framework, or motion without user value.
- Do not polish the happy path while omitting failure, long-content, responsive, and keyboard states.
- Do not alter routes, analytics, accessibility behavior, brand recognition, or core copy during a visual redesign without evidence and approval.

## Completion evidence

- Critical flows work at target viewports with keyboard, touch, and assistive semantics where applicable.
- Typography, spacing, contrast, alignment, content integrity, state coverage, and visual-reference fidelity are reviewed from rendered output.

## Related skills

- `design-motion`
- `design-visual-theme`
- `test-web-app`

## Conditional reference

Read [references/variants.md](references/variants.md) to select the task mode. Then load only the linked detail reference for that mode.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
