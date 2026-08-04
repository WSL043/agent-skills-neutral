---
name: work-with-pdf
description: "Read, extract, create, fill, edit, merge, split, OCR, or visually validate PDF files with task-specific routing. Use whenever a PDF is a primary input or required deliverable, especially when layout fidelity matters."
---

# Work With PDF

## Goal

Produce or analyze a PDF with correct content, stable structure, and visually verified pages.

## Workflow

1. Route the request to read/extract, create, fill, edit/reformat, merge/split, OCR, or render/verify.
2. Inspect page count, metadata, encryption, text layer, forms, images, and page geometry before mutation.
3. Use structural extraction for text and tables, but render pages when spatial meaning or visual fidelity matters.
4. Choose a generation or editing tool that preserves the required forms, vectors, fonts, and accessibility features.
5. Write to a new file, reopen it, and run structural checks.
6. Render representative and boundary pages; inspect clipping, substitutions, layering, fields, and pagination.

## Decision rules

- Use OCR only when the text layer is missing or unusable; retain page coordinates and confidence where possible.
- Use form-field editing for AcroForms and page-overlay techniques only when fields are absent.
- For visual redesign, rebuild from structured content rather than repeatedly stamping over a poor source.

## Guardrails

- Do not assume extracted text preserves reading order or table structure.
- Do not remove encryption, signatures, or restrictions without authorization.
- Do not claim visual quality without rendering the final PDF.

## Completion evidence

- The final file opens, has the expected page count, and passes the requested structural checks.
- Rendered pages show correct fonts, spacing, layering, forms, and no clipped content.

## Related skills

- `work-with-docx`
- `capture-screen`

## Conditional reference

Read [references/variants.md](references/variants.md) when the task depends on implementation strategy or runtime capability.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
