---
name: design-visual-theme
description: "Create or apply a coherent visual theme across documents, presentations, interfaces, or artwork using semantic color, typography, spacing, and style rules. Use when selecting a theme, deriving design tokens, or aligning multiple artifacts visually."
---

# Design Visual Theme

## Goal

Produce a reusable theme whose tokens and usage rules create consistency without erasing content hierarchy.

## Workflow

1. Inspect audience, medium, content, brand constraints, accessibility requirements, and existing assets.
2. Choose a design direction and define semantic color roles, type scale, font pairing, spacing rhythm, shape, and imagery treatment.
3. Test the system on representative dense, sparse, data-heavy, and emphasis-heavy content.
4. Document token names and rules for backgrounds, text, accents, states, charts, and exceptions.
5. Apply the theme through shared variables or styles rather than one-off values.
6. Review contrast, font availability, hierarchy, and consistency in the final medium.

## Decision rules

- Derive a new theme when source content has a strong identity; use a preset only when it genuinely fits.
- Keep data colors distinguishable from semantic status colors.
- Choose fonts available in the target runtime or package them legally.

## Guardrails

- Do not apply accent color to every element.
- Do not use brand or decorative colors where they reduce contrast or imply status incorrectly.
- Do not copy proprietary theme assets without permission.

## Completion evidence

- Theme tokens cover required semantic roles and representative artifacts use them consistently.
- Contrast, font fallback, grayscale differentiation, and target-medium rendering are checked.

## Related skills

- `design-frontend`
- `create-visual-art`

## Conditional reference

Read [references/variants.md](references/variants.md) when the task depends on implementation strategy or runtime capability.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
