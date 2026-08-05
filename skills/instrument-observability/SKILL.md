---
name: instrument-observability
description: "Design, add, or review production telemetry so operators can answer concrete questions with structured logs, bounded-cardinality metrics, traces, and actionable alerts. Use for observability, instrumentation, correlation IDs, SLO signals, or when a production feature is impossible to diagnose from existing evidence."
---

# Instrument Observability

## Goal

Make important production behavior diagnosable from outside the process without leaking sensitive data or generating unactionable noise.

## Workflow

1. Name two to four questions an operator must answer about the feature, dependency, or failure mode.
2. Inspect existing telemetry libraries, schemas, context propagation, dashboards, SLOs, retention, and privacy rules.
3. Map each question to the cheapest suitable signal: aggregate metrics for how often/how slow, traces for where time went, logs or audit events for what happened and why.
4. Define stable event names, bounded dimensions, trace/span boundaries, sampling, redaction, and ownership before adding calls.
5. Instrument the smallest useful boundary and propagate correlation context across process, queue, and network edges.
6. Trigger success, expected failure, retry/degradation, and unexpected failure paths; inspect actual emitted output and downstream ingestion.
7. Add symptom-based alerts only when a human can take a named action, with threshold rationale and a runbook.

## Decision rules

- Prefer established project telemetry and vendor-neutral conventions over a second stack.
- Keep high-cardinality identifiers in searchable logs/traces, never metric labels.
- Record business outcomes and dependency behavior where infrastructure metrics cannot answer user-impact questions.
- Sample routine traces when volume requires it, while preserving enough failures for investigation.

## Guardrails

- Never log tokens, passwords, secrets, full request bodies, or unredacted personal data.
- Do not use averages alone for latency or raw URLs/user IDs as metric dimensions.
- Do not declare observability complete from configuration; inspect real emitted signals and alert delivery.
- Do not add a dashboard or alert without a concrete operational question and owner.

## Completion evidence

- Each operational question maps to a verified signal and query.
- A test request can be followed across relevant boundaries and induced failures produce safe, useful evidence.
- Metric cardinality, sampling, retention, redaction, alert action, and runbook ownership are reviewed.

## Related skills

- `diagnose-software`
- `verify-completion`
- `migrate-system-safely`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
