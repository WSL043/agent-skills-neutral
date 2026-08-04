# Implementation variants

## Tight-loop diagnosis

Prioritize a minimal reproducer, fast instrumentation, and short hypothesis cycles when the subsystem is well bounded.

## Four-phase diagnosis

For cross-component failures, separate evidence gathering, pattern comparison, hypothesis testing, and implementation. Do not advance phases without the evidence produced by the previous one.
