---
name: build-winui-app
description: "Build or extend Windows desktop applications with WinUI, Windows App SDK, XAML, packaging, accessibility, and runtime verification. Use for native Windows UI, app lifecycle, deployment, or platform integration tasks."
---

# Build WinUI App

## Goal

Deliver a Windows feature that follows the existing app architecture and works in the intended packaged or unpackaged deployment model.

## Workflow

1. Inspect target framework, Windows App SDK version, packaging mode, architecture, navigation, resources, and deployment constraints.
2. Define view state, commands, async work, window/lifecycle behavior, persistence, and Windows integration points.
3. Implement a vertical slice with binding-safe view models and reusable XAML resources.
4. Handle DPI, theme changes, keyboard access, screen readers, window resizing, and cancellation.
5. Add unit tests around view-model behavior and UI/integration tests for critical platform paths.
6. Build and run the intended architectures and packaging mode on a compatible Windows environment.

## Decision rules

- Use packaged deployment when identity-dependent Windows features are required.
- Keep UI-thread transitions explicit for asynchronous callbacks.

## Guardrails

- Do not assume XAML compilation proves runtime binding or resource resolution.
- Do not change packaging identity or capabilities without checking deployment impact.

## Completion evidence

- The application launches in the intended deployment mode and critical flows work.
- DPI, resize, theme, accessibility, and error states are exercised.

## Related skills

- `design-frontend`
- `verify-completion`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
