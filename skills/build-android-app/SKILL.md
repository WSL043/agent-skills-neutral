---
name: build-android-app
description: "Build or extend native Android applications with lifecycle-aware architecture, modern UI, state management, persistence, and device-level verification. Use for Kotlin, Jetpack Compose, Android platform APIs, packaging, or app architecture tasks."
---

# Build Android App

## Goal

Deliver an Android feature that survives lifecycle changes and works on the declared device/API range.

## Workflow

1. Inspect Gradle modules, minimum/target SDK, architecture, navigation, dependency injection, and existing UI conventions.
2. Define UI states, events, data ownership, permissions, offline behavior, and lifecycle boundaries.
3. Implement a thin vertical slice using platform-recommended APIs and repository conventions.
4. Handle configuration change, process recreation, background/foreground transition, errors, and accessibility.
5. Add unit tests for state/rules and instrumentation or UI tests for platform behavior.
6. Build, install, and exercise the feature on an emulator or device across representative API levels.

## Decision rules

- Keep composables declarative and hoist durable state to an appropriate owner.
- Request runtime permissions at the point of need and handle denial without dead ends.

## Guardrails

- Do not block the main thread with I/O or long computation.
- Do not assume emulator success covers device sensors, OEM behavior, or release signing.

## Completion evidence

- Debug and release builds succeed for the intended variants.
- The feature survives rotation/recreation, handles denied permissions, and passes relevant tests.

## Related skills

- `design-frontend`
- `verify-completion`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
