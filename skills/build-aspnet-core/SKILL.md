---
name: build-aspnet-core
description: "Build or extend ASP.NET Core applications and APIs using current framework conventions, dependency injection, configuration, authentication, data access, observability, and automated tests. Use for .NET web backends, services, or server-rendered applications."
---

# Build ASP.NET Core

## Goal

Deliver a secure, observable ASP.NET Core feature that fits the solution architecture and deployment model.

## Workflow

1. Inspect target framework, solution structure, hosting model, configuration, middleware order, authentication, persistence, and tests.
2. Define request contracts, validation, authorization, errors, data ownership, transactions, and compatibility.
3. Implement a vertical slice with explicit service lifetimes and cancellation propagation.
4. Use framework-native problem responses, logging, health checks, metrics, and configuration binding.
5. Add unit, integration, and authorization tests at the relevant boundaries.
6. Run the application with production-like configuration and exercise startup, migrations, requests, failures, and shutdown.

## Decision rules

- Use minimal APIs for compact endpoint surfaces and controllers when filters, conventions, or organization make them clearer.
- Keep scoped services out of singleton dependencies and background tasks unless a scope is created deliberately.

## Guardrails

- Do not expose detailed exceptions or secrets in production responses and logs.
- Do not perform blocking I/O in asynchronous request paths.
- Do not trust client-supplied identity or authorization claims without server validation.

## Completion evidence

- Build and tests pass on the target SDK.
- Authentication, authorization, validation, cancellation, error responses, and startup configuration are exercised.

## Related skills

- `review-security-practices`
- `verify-completion`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
