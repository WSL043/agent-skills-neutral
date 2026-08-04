---
name: test-web-app
description: "Test and debug web applications in a real browser using stable selectors, controlled server lifecycle, functional assertions, console/network evidence, screenshots, and cleanup. Use for UI-flow verification, browser automation, visual checks, or frontend runtime diagnosis."
---

# Test Web App

## Goal

Produce reproducible browser evidence that the requested flow works in the final application state.

## Workflow

1. Define the target flow, environment, accounts/data, viewports, expected states, and failure evidence.
2. Start or attach to the application deterministically and confirm readiness with a bounded condition.
3. Inspect the live DOM and accessible roles before choosing selectors; prefer role, label, test ID, or stable semantics.
4. Execute the flow step by step while collecting assertions, console errors, failed requests, URLs, and state transitions.
5. Capture screenshots at decision points and inspect responsive, empty, loading, error, and keyboard behavior when relevant.
6. Clean up browser contexts and owned servers, then rerun the critical path from a fresh state.

## Decision rules

- Use a persistent browser session for iterative diagnosis only when the runtime supports it generically; use isolated sessions for reproducible tests.
- Use network stubbing for deterministic boundary tests, but retain at least one real integration path when integration is in scope.
- Wait on observable conditions rather than fixed sleeps.

## Guardrails

- Do not use brittle coordinates or generated CSS classes when semantic selectors exist.
- Do not treat a screenshot alone as functional proof.
- Do not leave servers, browser processes, test data, or authenticated sessions running unintentionally.

## Completion evidence

- The critical flow passes from a fresh browser state with assertions at each important transition.
- Console, network, screenshot, and cleanup evidence support the final claim.

## Related skills

- `capture-screen`
- `diagnose-software`
- `verify-completion`

## Conditional reference

Read [references/variants.md](references/variants.md) when the task depends on implementation strategy or runtime capability.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
