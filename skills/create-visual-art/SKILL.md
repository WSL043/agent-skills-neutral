---
name: create-visual-art
description: "Create original static visual artwork, posters, covers, or decorative compositions with an explicit concept, hierarchy, typography, color system, and rendered QA. Use when the primary deliverable is a designed image or print-ready visual rather than an application UI."
---

# Create Visual Art

## Goal

Produce an original visual artifact with a coherent concept and verified output dimensions.

## Workflow

1. Define audience, message, medium, dimensions, content, constraints, and desired emotional character.
2. Choose one visual concept and write its hierarchy, composition, type, color, texture, and imagery rules.
3. Create a low-fidelity composition before polishing details.
4. Build at target aspect ratio with licensed or original imagery and deliberate negative space.
5. Render at final size and inspect hierarchy, contrast, alignment, cropping, and small-text legibility.
6. Export the requested formats and retain an editable source when appropriate.

## Decision rules

- Use typography as the main visual element when imagery would be generic or unsupported.
- Create variants only around a named decision such as composition or color, not random style churn.

## Guardrails

- Do not imitate a living artist's distinctive style or copy protected compositions.
- Do not use unlicensed fonts or imagery.
- Do not present a low-resolution preview as print-ready output.

## Completion evidence

- The final dimensions, color mode, bleed/safe area, and file format match the intended medium.
- The composition remains legible at actual viewing size.

## Related skills

- `design-visual-theme`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
