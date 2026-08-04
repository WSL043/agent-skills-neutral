---
name: build-ios-app
description: "Build or extend native Apple-platform applications with Swift, SwiftUI or UIKit, explicit state, persistence, concurrency, accessibility, and simulator/device verification. Use for iOS application features, architecture, packaging, or platform APIs."
---

# Build iOS App

## Goal

Deliver an iOS feature that follows platform conventions and behaves correctly across lifecycle and concurrency boundaries.

## Workflow

1. Inspect deployment target, project/workspace, package dependencies, architecture, navigation, signing, and existing UI conventions.
2. Define state ownership, async work, persistence, permissions, deep links, and foreground/background behavior.
3. Implement a vertical slice with testable models and platform-appropriate UI composition.
4. Handle cancellation, actor/thread boundaries, error recovery, Dynamic Type, VoiceOver, and localization expansion.
5. Add unit and UI tests around rules, navigation, and lifecycle-sensitive behavior.
6. Build and run on relevant simulators; verify a release/archive path when distribution is in scope.

## Decision rules

- Keep UI updates on the main actor and make ownership of asynchronous tasks explicit.
- Use UIKit bridges only where SwiftUI lacks required behavior or the existing app standardizes on UIKit.

## Guardrails

- Do not assume preview success proves runtime behavior.
- Do not put secrets in the app bundle or source-controlled configuration.

## Completion evidence

- Builds and relevant tests pass for the declared destination.
- Lifecycle, cancellation, permissions, accessibility, and error states are exercised.

## Related skills

- `design-frontend`
- `verify-completion`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
