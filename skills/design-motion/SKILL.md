---
name: design-motion
description: "Design, audit, or refine interface motion using explicit purpose, timing, easing, continuity, interruption behavior, accessibility, and performance constraints. Use for animation vocabulary, motion opportunities, animation review, or implementation planning."
---

# Design Motion

## Goal

Use motion to clarify state and causality without adding delay, distraction, or accessibility regressions.

## Workflow

1. Inventory existing motion, interaction states, libraries, performance constraints, and reduced-motion behavior.
2. Name the purpose of each candidate motion: orientation, feedback, continuity, hierarchy, narrative emphasis, or restrained delight.
3. Specify trigger, properties, origin, duration, easing or spring, interruption, exit, and reduced-motion alternative.
4. Prototype high-impact transitions at realistic content size and interaction speed.
5. Audit for unnecessary frequency, non-composited properties, abrupt cancellation, and inconsistent vocabulary.
6. Measure or inspect performance and review the final feel in context.

## Decision rules

- Use no motion when it delays a repeated action, competes with reading, or lacks informational value.
- Prefer transform and opacity for high-frequency UI transitions.
- Use spring motion for physical continuity and timed easing for deterministic sequencing.

## Guardrails

- Do not force spring physics, scroll choreography, or perpetual movement as a style requirement.
- Do not animate large layout regions without testing reflow and input responsiveness.
- Do not remove content or focus before an exit transition completes.
- Do not ignore reduced-motion preferences.

## Completion evidence

- Each motion has a named purpose and exact implementation values.
- Interruptions, rapid repetition, reduced motion, and lower-performance conditions are tested.

## Related skills

- `design-frontend`

## Conditional reference

Read [references/variants.md](references/variants.md) when the task depends on implementation strategy or runtime capability.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
