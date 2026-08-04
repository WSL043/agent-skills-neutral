---
name: build-flutter-app
description: "Build or extend Flutter applications with explicit state ownership, adaptive UI, navigation, platform integration, and tested release builds. Use for Dart, Flutter widgets, packages, mobile/desktop/web targets, or cross-platform app architecture."
---

# Build Flutter App

## Goal

Deliver a Flutter feature that behaves consistently across the declared targets while isolating platform differences.

## Workflow

1. Inspect supported targets, Flutter/Dart constraints, state management, routing, themes, plugins, and build flavors.
2. Define screen states, events, data flow, error handling, persistence, and platform capability differences.
3. Implement a vertical slice with small widgets and testable non-UI logic.
4. Add adaptive layout, keyboard/focus behavior, semantics, loading, empty, and error states.
5. Test logic, widgets, navigation, and plugin boundaries at appropriate levels.
6. Run and build each declared target, then inspect release-mode behavior and generated artifacts.

## Decision rules

- Use conditional adapters around platform APIs instead of scattering platform checks through UI code.
- Choose local widget state for ephemeral UI and a shared owner for cross-screen or persisted state.

## Guardrails

- Do not assume hot reload represents cold-start or release behavior.
- Do not add a plugin without checking target support and maintenance status.

## Completion evidence

- Tests pass and release builds succeed for every claimed target.
- Responsive layouts, input modes, navigation, and platform integrations are exercised.

## Related skills

- `design-frontend`
- `verify-completion`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
