---
name: work-with-postgresql
description: "Design, query, migrate, secure, or diagnose PostgreSQL systems using runtime, schema, workload, and evidence-aware decisions. Use when PostgreSQL tables, queries, indexes, transactions, roles, row policies, migrations, or database performance are central."
---

# Work With PostgreSQL

## Goal

Change or diagnose a PostgreSQL system while preserving data integrity, access policy, concurrency behavior, and the workload contract.

## Workflow

1. Inspect the actual server version, extensions, schema, constraints, roles, access path, data shape, workload, consistency requirements, and operational topology. Treat current runtime and project configuration as the source of truth.
2. Define the query, schema, security, or migration contract. For query and performance work, inspect plans, statistics, indexes, locks, and representative data before selecting a change.
3. Choose the smallest reversible change. Account for read and write cost, storage, transaction scope, connection pooling, concurrency, deadlocks, privilege boundaries, and row-level access policies. Stage backfills and cutovers when live consumers or large data sets are involved.
4. Validate with representative queries and data, plan or timing evidence, constraint and permission checks, migration rehearsal or rollback evidence, application tests, and reconciliation. Observe the running system after deployment when the change is live.
5. Report the exact version and scope, evidence, trade-offs, residual risks, and any checks that could not run. Keep destructive cleanup separate from the change that proves it is safe.

## Decision rules

- Inspect before indexing, rewriting queries, changing types, or changing connection settings; a plausible optimization can harm another workload.
- Preserve constraints and least-privilege access. Do not disable row-level policies or bypass permissions to make a test convenient.
- Match transaction and migration strategy to lock duration, concurrency, failure recovery, and the ability to roll back or reconcile.
- Use current PostgreSQL documentation and the project's actual extensions and deployment model rather than assuming a hosted provider behaves like every other installation.

## Guardrails

- Do not run destructive migrations, bulk rewrites, or privilege changes without an explicit scope, recovery path, and verification plan.
- Do not guess at pool limits, timeouts, index usefulness, or plan stability from a single query or environment.
- Keep credentials and private data out of logs, fixtures, reports, and examples.

## Completion evidence

- Runtime, schema, workload, access, and consistency assumptions are recorded.
- The chosen change has representative correctness, plan/performance, security, and migration evidence appropriate to its risk.
- Rollback, reconciliation, monitoring, and unverified conditions are explicit.

## Related skills

- `migrate-system-safely`
- `diagnose-software`
- `review-security-practices`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
