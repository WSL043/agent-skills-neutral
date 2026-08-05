# Redesign protocol

## Audit before changing

Capture representative current screens and identify:

- what users rely on: information architecture, routes, primary actions, content, data density, and platform conventions;
- what carries identity: logo, typography, palette, imagery, voice, and recognizable interaction patterns;
- what is broken: hierarchy, spacing, contrast, responsiveness, state gaps, inconsistency, accessibility, or performance;
- what is merely a preference rather than a defect.

Classify the requested change as polish, visual-system modernization, interaction redesign, or structural overhaul. If unclear, propose the smallest class supported by evidence.

## Preservation contract

Unless the user approves otherwise, preserve:

- routes, slugs, analytics hooks, accessibility semantics, and functional behavior;
- content meaning, brand recognition, and critical conversion/user flows;
- working repository architecture and component contracts.

List every intended exception before implementation.

## Modernization order

Correct foundational inconsistencies first: typography and semantic color, layout and spacing, component/state vocabulary, responsive behavior, then motion and decorative polish. Do not hide structural problems with effects.

## Verification

Compare before/after at the same viewports and states. Verify preserved behavior, route and analytics continuity, keyboard/screen-reader paths, performance, and that the change solves the named audit findings rather than only looking different.
