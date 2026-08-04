---
name: work-with-pptx
description: "Create, read, edit, template, or validate PPTX and POTX presentations with layout-aware routing, reusable design systems, and rendered visual QA. Use whenever slides or PowerPoint files are a primary input or deliverable."
---

# Work With PPTX

## Goal

Deliver a coherent, editable presentation whose slide structure and rendered visuals are both verified.

## Workflow

1. Route to content extraction, new deck creation, template-based creation, surgical edit, or review.
2. Inspect slide masters, layouts, theme, fonts, notes, relationships, charts, and existing visual patterns.
3. Define narrative, audience, slide roles, and a compact design system before producing slides.
4. For new decks, generate editable shapes and text; for high-fidelity template edits, duplicate layouts or modify package XML carefully.
5. Validate package relationships and reopen the deck after every structural transformation.
6. Render all slides, inspect a montage and full-resolution outliers, then correct overflow, collisions, contrast, and repetition.

## Decision rules

- Reuse a template layout when it already encodes the desired composition; do not simulate it with arbitrary coordinates.
- Choose charts only when the relationship is clearer than a short statement or table.
- Keep specialized slide-generation, design, and editing modules behind one presentation router.

## Guardrails

- Do not use a single title-and-bullets layout for the whole deck.
- Do not replace editable content with screenshots unless explicitly requested.
- Do not trust a package that has not been reopened and rendered.

## Completion evidence

- The PPTX opens without repair warnings and all expected slides, notes, and relationships remain.
- Rendered slides show no clipping, collisions, placeholder text, font substitution, or low-contrast content.
- The deck has a clear narrative and deliberate layout variation.

## Related skills

- `design-visual-theme`
- `capture-screen`

## Conditional reference

Read [references/variants.md](references/variants.md) when the task depends on implementation strategy or runtime capability.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
