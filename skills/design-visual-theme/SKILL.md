---
name: design-visual-theme
description: "Create, extract, or apply a coherent brand and visual theme across documents, presentations, interfaces, or artwork using a meaningful concept plus semantic color, typography, spacing, imagery, and style rules. Use for brand-system direction, theme derivation, design tokens, or cross-artifact visual alignment."
---

# Design Visual Theme

## Goal

Produce a reusable visual grammar whose typography, color, spacing, shape, imagery, material, and emphasis rules feel intentionally related without flattening every artifact into the same look.

## Workflow

1. Inspect audience, medium, content, brand constraints, accessibility requirements, existing assets, references, and the visual character already present.
2. Name the brand/content promise and identify visual material that can legitimately express it: cultural register, product geometry, photography, physical material, editorial behavior, technical precision, playfulness, heritage, or another real source.
3. Define semantic color roles, typography roles, spacing rhythm, shape relationships, borders/elevation/material, icon/logo behavior, imagery treatment, and emphasis grammar as a connected system rather than independent presets.
4. Test the system on representative dense, sparse, data-heavy, image-heavy, and emphasis-heavy content that actually belongs to the project.
5. Examine optical relationships in rendered output: type-to-space proportion, nested shape relationships, border weight, visual mass, contrast, crop behavior, and how exceptions create tension without becoming noise.
6. Document token names and usage rules for backgrounds, text, accents, states, charts, media, marks, and justified exceptions.
7. Apply the theme through shared variables or styles rather than one-off values, then review it in the target medium and remove rules that do not survive real content.

## Decision rules

- Treat palettes, fonts, radii, shadows, and spacing recipes as ingredients, not styles by themselves. The theme must explain how the ingredients relate and why they fit the subject.
- Derive a new theme when source content has a strong identity; use a preset only when its existing visual logic genuinely fits.
- Keep data colors distinguishable from semantic status colors and preserve brand recognition where it is a binding requirement.
- Contrast can be part of a coherent system: an exception is useful when it creates deliberate emphasis or tension and remains recognizably connected to the base grammar.
- Choose fonts available in the target runtime or package them legally; do not infer quality from novelty or price.

## Guardrails

- Do not turn style labels such as luxury, tech, playful, editorial, minimal, or premium into fixed palette/font/radius recipes.
- Do not apply accent color, rounding, elevation, glass, texture, or decorative framing uniformly to every element.
- Do not use brand or decorative colors where they reduce contrast or imply status incorrectly.
- Do not invent a random symbol, mockup, palette, serif, metallic accent, or gradient merely because it is culturally associated with the requested adjective.
- Do not copy proprietary theme assets without permission.
- Do not encode a current generator fingerprint as a permanent design law; keep dated observations in the frontend design calibration reference.

## Completion evidence

- Theme rules cover required semantic roles and representative artifacts use them consistently without erasing content hierarchy or medium-specific needs.
- The rendered system demonstrates coherent relationships among type, color, space, shape, material, imagery, and emphasis rather than only token consistency.
- Contrast, font fallback, grayscale differentiation, dense/sparse content behavior, and target-medium rendering are checked.

## Related skills

- `design-frontend`

## Conditional reference

Read [references/variants.md](references/variants.md) when the task depends on implementation strategy or runtime capability.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
