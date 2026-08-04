---
name: work-with-docx
description: "Create, read, edit, or validate DOCX and DOTX documents while preserving professional layout, styles, comments, and tracked changes when required. Use whenever a Word document is a primary input or deliverable."
---

# Work With DOCX

## Goal

Produce a structurally valid Word document whose content and rendered layout match the request.

## Workflow

1. Identify whether the task is extraction, new creation, simple edit, format-preserving edit, template fill, or review/redline.
2. Inspect package structure, styles, sections, headers, footers, relationships, comments, and tracked changes before editing an existing file.
3. Choose a high-level library for ordinary creation and a package/XML strategy for fidelity-sensitive features it cannot preserve.
4. Apply changes through named styles and document structure instead of scattered direct formatting.
5. Save to a new path unless the user explicitly authorizes replacement.
6. Reopen, render to PDF or page images, and inspect page breaks, tables, headings, fields, and overflow.

## Decision rules

- Use direct XML only for features the selected library cannot round-trip safely.
- Preserve unknown package parts and relationships during surgical edits.
- Resolve tracked changes only when the user explicitly asks to accept or reject them.

## Guardrails

- Do not report success from a saved file alone; reopen and render it.
- Do not flatten styles, comments, or revisions during unrelated edits.
- Do not overwrite the only source copy without explicit permission.

## Completion evidence

- The DOCX reopens without repair warnings and requested content is present.
- Rendered pages show no clipping, unintended reflow, orphan headings, or broken tables.
- Preservation-sensitive features are compared before and after.

## Related skills

- `work-with-pdf`
- `verify-completion`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
