---
name: review-api-design
description: "Review an API contract, endpoint set, schema, or service interface before implementation for consumer fit, HTTP semantics, compatibility, errors, security boundaries, resilience, and operability. Use for REST/OpenAPI or comparable request-response API design review, not for debugging implemented handlers or reviewing a code diff."
---

# Review API Design

## Goal

Determine whether an API contract is ready to build and identify the smallest high-impact changes needed before consumers depend on it.

## Workflow

1. Read the complete contract, endpoint list, or specification. Infer domain, consumers, trust boundaries, scale, and compatibility commitments from supplied evidence.
2. Ask only for missing context that can change severity or the contract. A vague idea without concrete operations requires clarification before a formal review.
3. Review the relevant domains in [references/review-checklist.md](references/review-checklist.md); skip domains that do not apply and say why.
4. For each finding, distinguish observed contract evidence from inference, explain the consumer or operational consequence, and propose a concrete contract-level correction.
5. Calibrate severity by reachability, asset value, failure cost, consumer count, and reversibility rather than checklist presence alone.
6. End with readiness: ready, ready with named changes, or needs design work. List at most three blocking priorities.

## Finding format

- **Evidence:** exact operation, schema, field, header, or omitted contract element.
- **Impact:** what breaks, leaks, becomes ambiguous, or becomes costly.
- **Recommendation:** a specific design change and verification method.
- **Severity:** critical, warning, suggestion, or good.

## Decision rules

- Prefer consistent consumer behavior over stylistic REST purity.
- Treat versioning, envelopes, metadata, opaque IDs, gateways, and GraphQL as contextual choices, not universal requirements.
- Recommend idempotency, concurrency control, retries, or stronger authentication in proportion to duplicate-effect and asset risk.
- Use current primary standards or official guidance for temporally sensitive security and protocol claims.

## Guardrails

- Do not generate implementation code unless the user asks after the contract review.
- Do not label an unspecified concern critical when the missing context could make it irrelevant; ask or mark it unresolved.
- Do not confuse opaque identifiers with authorization or a gateway with business logic ownership.
- Use `review-security-practices` when the primary task is vulnerability analysis of implemented code.

## Completion evidence

- Every finding points to contract evidence or an explicit omission.
- Security, compatibility, failure, and operability risks are reviewed at a depth proportional to the API.
- The readiness verdict and next decisions are unambiguous.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
