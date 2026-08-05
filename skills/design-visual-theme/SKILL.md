---
name: design-visual-theme
description: "Create, extract, or apply a coherent brand and visual theme across documents, presentations, interfaces, or artwork using a meaningful concept plus semantic color, typography, spacing, imagery, and style rules. Use for brand-system direction, theme derivation, design tokens, or cross-artifact visual alignment."
---

# Design Visual Theme

## Goal

Produce a reusable theme whose tokens and usage rules create consistency without erasing content hierarchy.

## Workflow

1. Inspect audience, medium, content, brand constraints, accessibility requirements, and existing assets.
2. Name the brand or content promise and choose one visual metaphor or design direction that supports it.
3. Define semantic color roles, type scale, font pairing, spacing rhythm, shape, icon/logo behavior, and imagery treatment.
4. Test the system on representative dense, sparse, data-heavy, and emphasis-heavy content or applications.
5. Document token names and rules for backgrounds, text, accents, states, charts, media, marks, and exceptions.
6. Apply the theme through shared variables or styles rather than one-off values, then review the rendered target medium.

## Decision rules

- Derive a new theme when source content has a strong identity; use a preset only when it genuinely fits.
- Keep data colors distinguishable from semantic status colors.
- Choose fonts available in the target runtime or package them legally.

## Guardrails

- Do not apply accent color to every element.
- Do not use brand or decorative colors where they reduce contrast or imply status incorrectly.
- Do not invent a random symbol, mockup, or palette without connecting it to the audience and product meaning.
- Do not copy proprietary theme assets without permission.

## Completion evidence

- Theme tokens cover required semantic roles and representative artifacts use them consistently.
- Contrast, font fallback, grayscale differentiation, and target-medium rendering are checked.

## Related skills

- `design-frontend`

## Conditional reference

Read [references/variants.md](references/variants.md) when the task depends on implementation strategy or runtime capability.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
