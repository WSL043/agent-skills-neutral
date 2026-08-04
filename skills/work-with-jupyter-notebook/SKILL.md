---
name: work-with-jupyter-notebook
description: "Create, edit, execute, or validate Jupyter notebooks as reproducible computational narratives. Use for .ipynb experiments, tutorials, analyses, or notebook repair."
---

# Work With Jupyter Notebook

## Goal

Produce a notebook that runs top-to-bottom from a clean kernel and communicates its result clearly.

## Workflow

1. Define the notebook audience, question, inputs, expected outputs, and environment assumptions.
2. Inspect existing cells, metadata, hidden state, large outputs, and execution order before editing.
3. Organize setup, data loading, analysis, validation, and conclusion into small purposeful cells.
4. Move reusable logic into importable modules when it needs tests or reuse beyond the notebook.
5. Restart the kernel and execute all cells in order in the target environment.
6. Review errors, warnings, output size, charts, paths, randomness, and saved metadata.

## Decision rules

- Pin random seeds and record data/environment versions when results depend on them.
- Keep exploratory branches only when they help the reader; remove dead cells and contradictory outputs.

## Guardrails

- Do not rely on variables created by out-of-order execution.
- Do not embed credentials, private data, or massive binary outputs.
- Do not hide a failing cell by leaving stale successful output.

## Completion evidence

- A clean-kernel run completes in order and produces the saved outputs.
- Inputs, environment, assumptions, and key conclusions are visible to a new reader.

## Related skills

- `work-with-xlsx`
- `verify-completion`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
