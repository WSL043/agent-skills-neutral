---
name: work-with-xlsx
description: "Create, read, analyze, edit, or validate XLSX, XLSM, CSV, and related spreadsheet files while preserving formulas, formatting, and advanced workbook features when required. Use whenever a spreadsheet is a primary input or deliverable."
---

# Work With XLSX

## Goal

Produce a correct, recalculable workbook with preserved structure and verified presentation.

## Workflow

1. Classify the task as analysis, new workbook, ordinary edit, or format-preserving edit.
2. Inventory sheets, named ranges, tables, formulas, external links, macros, pivots, charts, validations, hidden content, and protection.
3. Choose a dataframe or workbook library for analysis and ordinary creation; choose package-level editing when advanced features must survive unchanged.
4. Apply formulas and formats systematically, keep raw inputs separate from calculations, and avoid unexplained constants.
5. Recalculate with a compatible spreadsheet engine when formulas changed.
6. Reopen the workbook, scan formula errors, compare preservation-sensitive parts, and visually inspect important sheets.

## Decision rules

- Use CSV only when formulas, types, styles, multiple sheets, and workbook metadata are irrelevant.
- Use package-level edits for VBA, pivots, slicers, sparklines, or unsupported drawing features.
- Keep assumptions in dedicated cells with labels and units.

## Guardrails

- Do not replace formulas with cached values unless requested.
- Do not open and resave a complex workbook with a library known to drop unsupported parts.
- Do not claim correctness without recalculation and error scanning.

## Completion evidence

- The workbook reopens without repair warnings and expected sheets/features remain.
- Formula cells recalculate without new errors and key totals reconcile.
- Important sheets render with readable widths, formats, and print areas.

## Related skills

- `verify-completion`

## Conditional reference

Read [references/variants.md](references/variants.md) when the task depends on implementation strategy or runtime capability.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
