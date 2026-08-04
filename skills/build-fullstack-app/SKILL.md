---
name: build-fullstack-app
description: "Build or extend full-stack web applications through a thin vertical slice covering UI, server logic, data, authentication, errors, and deployment-ready verification. Use when a feature crosses frontend and backend boundaries or when scaffolding a complete web application."
---

# Build Full-Stack App

## Goal

Deliver an end-to-end feature with explicit contracts, ownership, security, and observable runtime behavior.

## Workflow

1. Inspect the existing stack, routing, rendering model, API boundaries, data schema, authentication, deployment, and tests.
2. Define the user flow, UI states, server contract, validation, authorization, persistence, and failure behavior.
3. Implement the smallest end-to-end slice before expanding architecture or surface area.
4. Keep shared contracts generated or explicitly versioned; avoid duplicating hidden validation rules.
5. Add unit, integration, and browser-level tests at the boundaries with highest failure cost.
6. Run the application from a clean setup and verify real requests, persistence, refresh, errors, and production build behavior.

## Decision rules

- Render on the server when it materially improves first load, indexing, or data boundary simplicity; use client state for interactive local behavior.
- Use background work for slow operations that do not need to hold a request open.

## Guardrails

- Do not expose server secrets or privileged logic to client bundles.
- Do not validate only one side of a network contract.
- Do not add infrastructure before the vertical slice proves the need.

## Completion evidence

- A clean environment can start the app and complete the critical user flow.
- Production build, migrations, authorization, validation, persistence, and browser behavior are verified.

## Related skills

- `design-frontend`
- `test-web-app`
- `review-security-practices`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
