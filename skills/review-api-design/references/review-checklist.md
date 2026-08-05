# API review domains

Load only the domains relevant to the supplied contract.

## Consumer and domain fit

- Resource and operation names use domain language rather than database or framework internals.
- The contract identifies intended consumers, trust level, latency/availability needs, and compatibility horizon.
- Operations model the user or business action clearly; RPC-style actions are acceptable when CRUD would obscure the invariant.

## Contract shape

- Inputs, outputs, required/optional/null semantics, defaults, limits, and content types are explicit.
- Collection operations define pagination, stable ordering, filtering, and maximum page size where data can grow.
- Errors have stable machine-readable identifiers, safe human detail, field-level validation when needed, and consistent media types.
- New fields can be added safely; removals, type changes, enum growth, and nullability changes have an evolution policy.

## HTTP and interaction semantics

- Methods, status codes, caching, conditional requests, and content negotiation match observable behavior.
- Non-idempotent writes that can be retried or duplicate expensive effects define deduplication/idempotency behavior.
- Concurrent updates define conflict or precondition behavior where lost updates matter.
- Long-running work defines asynchronous status, cancellation, completion, and failure semantics.

## Identity, authorization, and data exposure

- Authentication and authorization are separate, with object- and operation-level checks at every relevant boundary.
- Public identifiers do not unnecessarily expose sequence or business volume; opaque IDs remain defense-in-depth, not authorization.
- Sensitive fields, logs, URLs, errors, and examples avoid credentials, internal topology, and unnecessary personal data.
- Cookie-authenticated state changes address CSRF; cross-origin access and browser credentials are explicitly constrained.
- Rate and resource limits protect authentication, search, export, upload, and high-value business flows proportionally.

## Resilience and dependencies

- Client and server timeout budgets, retryable failures, backoff, `Retry-After`, and partial failure behavior are defined where needed.
- Downstream calls have ownership, fallback/degradation, circuit isolation, and unsafe-retry constraints.
- WebSocket, SSE, GraphQL, queues, or polling are chosen from direction, frequency, ordering, replay, caching, and operating constraints.
- A gateway centralizes cross-cutting policy only when multiple services or external consumers justify it; business rules stay in owned services.

## Operability and lifecycle

- Correlation/trace context, health/readiness, useful metrics, audit events, and redaction expectations are part of the design where production operation requires them.
- Deprecation includes usage measurement, consumer communication, overlap, cutover, and removal criteria.
- Non-functional targets are measurable and consistent with dependency budgets.
- Documentation, examples, contract tests, and generated clients are planned for the actual consumer set.

## Readiness calibration

- **Critical:** reachable design defect likely to cause unauthorized access, corruption, unrecoverable duplication, or broad contract breakage.
- **Warning:** likely production/integration problem that should be resolved before build.
- **Suggestion:** meaningful improvement whose deferral is understood and reversible.
- **Good:** a concrete decision worth preserving.

Do not penalize a contract for omitting a domain that is demonstrably irrelevant.
