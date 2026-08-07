---
name: design-motion
description: "Design, audit, or refine interface motion using explicit purpose, timing, easing, continuity, interruption behavior, accessibility, and performance constraints. Use for animation vocabulary, motion opportunities, animation review, or implementation planning."
---

# Design Motion

## Goal

Use motion that feels native to the product's visual language and clarifies state, causality, space, or feedback without adding delay, distraction, generator-style spectacle, or accessibility regressions.

## Workflow

1. Inventory existing motion, interaction frequency, spatial relationships, libraries, product character, performance constraints, and reduced-motion behavior.
2. Name the purpose of each candidate motion: orientation, feedback, continuity, hierarchy, explanation, narrative emphasis, or restrained delight. Reject motion that has no job.
3. Decide the motion grammar before individual effects: what feels immediate, what has inertia, what shares an origin, what may overshoot, what remains still, and how repeated interactions differ from rare moments.
4. Specify trigger, animated properties, origin, path, easing or spring behavior, interruption, exit, and reduced-motion alternative using values justified by the actual interaction or existing system.
5. Prototype high-impact transitions at realistic content size and interaction speed. Exercise reversal, rapid repetition, cancellation, and input during motion.
6. Audit the whole product for inconsistent tempo, arbitrary direction, repeated reveal choreography, unnecessary frequency, non-composited work, abrupt cancellation, and motion that competes with reading or control.
7. Measure or inspect performance and review the final feel in context rather than judging isolated demos.

## Decision rules

- Frequency changes the answer. An effect that is delightful once can become friction when repeated; highly repeated actions should usually become quieter and more immediate.
- Motion should preserve spatial causality: anchored elements should appear related to their trigger, state transitions should preserve identity when useful, and exits should make the disappearance understandable.
- Use spring-like behavior when continuity, gesture, velocity, or interruption benefits from it; do not use bounce or springiness merely as a modern-looking default.
- Use deterministic easing when sequence and timing matter more than simulated physical continuity.
- A coherent motion system may contain contrast, but repeated interactions should feel like they belong to the same product unless the difference communicates a different class of event.

## Guardrails

- Do not invent universal duration, bounce, stiffness, damping, or motion-count defaults. Derive values from an existing system, platform behavior, measured interaction needs, or the specific effect being tuned.
- Do not force spring physics, scroll choreography, fade-and-slide reveals, parallax, magnetic hover, or perpetual movement as style requirements.
- Do not animate large layout regions without testing reflow and input responsiveness.
- Do not remove content or focus before an exit transition completes when that would break interaction or accessibility.
- Do not ignore reduced-motion preferences or make the reduced version lose state information.

## Completion evidence

- Each retained motion has a named purpose, a relationship to the product's motion grammar, and implementation values that came from an actual constraint or tuned evidence rather than an arbitrary preset.
- Interruptions, rapid repetition, reduced motion, realistic content, and lower-performance conditions are tested where relevant.
- Repeated motion patterns do not overpower hierarchy or make unrelated interfaces converge on the same generator-default choreography.

## Related skills

- `design-frontend`

## Conditional reference

Read [references/variants.md](references/variants.md) when the task depends on implementation strategy or runtime capability.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
