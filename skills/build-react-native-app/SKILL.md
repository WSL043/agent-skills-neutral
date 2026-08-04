---
name: build-react-native-app
description: "Build or extend React Native applications with predictable state, navigation, native-module boundaries, performance controls, and Android/iOS verification. Use for cross-platform mobile features implemented with React Native."
---

# Build React Native App

## Goal

Deliver a cross-platform feature with shared behavior and explicitly tested native differences.

## Workflow

1. Inspect React Native version, architecture mode, navigation, state/data libraries, native projects, build flavors, and supported OS versions.
2. Define states, events, persistence, permissions, deep links, offline behavior, and platform-specific branches.
3. Implement a vertical slice with pure business logic separated from components and native adapters.
4. Control list rendering, re-renders, image cost, startup work, and bridge/native-module traffic.
5. Add unit, component, and end-to-end coverage at the highest-risk boundaries.
6. Run fresh Android and iOS builds and exercise cold start, backgrounding, navigation, and error paths.

## Decision rules

- Use a native module only when platform APIs or performance require it.
- Keep platform-specific files small and expose a shared typed contract.

## Guardrails

- Do not validate only in a JavaScript test environment.
- Do not assume parity between Android and iOS permission, keyboard, or navigation behavior.

## Completion evidence

- Both platform builds succeed and the feature is exercised on each.
- Performance-sensitive paths and native boundaries have direct evidence.

## Related skills

- `design-frontend`
- `verify-completion`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
