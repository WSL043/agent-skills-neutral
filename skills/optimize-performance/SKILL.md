---
name: optimize-performance
description: "Improve software performance through measurement, bottleneck isolation, targeted changes, and remeasurement. Use for slow code, latency or throughput regressions, resource waste, or explicit performance optimization."
---

# Optimize Performance

## Goal

Improve a meaningful performance outcome without sacrificing correctness, safety, or maintainability.

## Workflow

1. Define the affected user or system outcome and a measurement that represents it. Capture a baseline under the same workload, data, environment, configuration, and correctness checks that will be used after the change; record meaningful variance.
2. Locate the bottleneck with profiling, traces, query plans, resource measurements, or a focused benchmark. Follow the evidence to the slow or expensive boundary instead of optimizing by intuition.
3. Choose one targeted change, state the expected mechanism and risks, and preserve functional, security, consistency, and resource contracts. Keep unrelated cleanup out of the experiment.
4. Re-run the same measurement after the change. Compare against the baseline and noise, inspect correctness and tail behavior where relevant, and revert or revise a change that is neutral, worse, or only improves an unimportant proxy.
5. Add a durable guard such as a focused benchmark, regression test, trace assertion, or operational signal. Report the measured effect, conditions, trade-offs, and remaining uncertainty.

## Decision rules

- Measure before changing and remeasure after changing; a faster local operation is not automatically a better system outcome.
- Prefer the narrowest bottleneck fix that explains the observed cost. Consider workload shape, concurrency, caching, I/O, memory, and downstream effects together.
- Keep performance and behavior evidence side by side. A speedup that changes results, security, ordering, or reliability is not an accepted optimization.
- Use current runtime and workload evidence over generic budgets or fixed thresholds.

## Guardrails

- Do not invent target budgets, sample counts, or universal thresholds merely to make a result look precise.
- Do not optimize unmeasured code, remove safety checks, or trade correctness for a benchmark win.
- Do not declare improvement from a single noisy measurement or from a successful build alone.

## Completion evidence

- A reproducible baseline, bottleneck signal, and post-change measurement are recorded under comparable conditions.
- Correctness and relevant regression checks pass, and the change has a durable guard or a stated reason one is not possible.
- Residual uncertainty, workload limits, and neutral or rejected attempts are visible.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
