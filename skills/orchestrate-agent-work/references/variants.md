# Implementation variants

## Parallel analysis

Dispatch independent evidence-gathering tasks together. Require compact findings and source locations; keep synthesis and the critical-path decision with the parent agent.

## Sequential implementation

Give each implementation task a fresh bounded context, then perform specification and quality review before advancing. This costs more coordination but limits context drift.

## Decision-map mode

Use when the destination is known but the route cannot yet be sliced. Keep a low-resolution map of the destination, decisions with evidence, current unblocked questions, future questions not yet sharp enough to schedule, and explicit out-of-scope items. Resolve one decision at a time; convert the result to an implementation plan only when the route is clear.
