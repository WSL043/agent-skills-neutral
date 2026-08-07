# Design quality protocol

Read [aesthetic-judgment.md](aesthetic-judgment.md) for durable visual judgment and [aesthetic-signals.md](aesthetic-signals.md) only as a dated calibration layer for recurring generator defaults.

## Design read

Before implementation, state one compact direction:

- product/page kind, primary user action, and information task;
- audience, context of use, and emotional character;
- subject-specific visual material already present in the product, brand, industry, or content;
- visual concept and the relationship that should make the composition recognizable;
- hierarchy, density, motion character, and material language;
- existing assets, design system, references, and constraints to preserve.

Use a documented design system when the product or platform calls for one. Use an aesthetic direction when the brief is brand-led. A named style is a starting grammar, not permission to copy its most obvious clichés.

## Derive, do not decorate

For every prominent choice, be able to answer why it belongs to this subject.

- Typography may come from the product's cultural register, reading task, technical character, or brand material.
- Shape may express physical product geometry, interaction affordance, density, softness, precision, or another real property.
- Color may come from brand recognition, imagery, semantic state, environment, or deliberate emotional contrast.
- Imagery, texture, illustration, diagrams, and motion should carry content or character rather than fill empty space.
- Structural devices such as labels, numbers, dividers, timelines, grids, and frames should encode actual structure when they imply it.

Do not force every project to invent an exotic motif. Specificity can come from excellent proportion, restrained typography, a distinctive content rhythm, or faithful product material.

## System extraction

Define semantic relationships rather than isolated values:

- typography roles, measure, wrapping, emphasis, and fallback behavior;
- background, surface, text, border, accent, status, and data colors;
- layout anchors, gutters, vertical rhythm, content width, and responsive transitions;
- shape, border, elevation, material, icon, and media treatment;
- interaction hierarchy, focus, disabled, loading, empty, error, and success states;
- motion vocabulary: what moves, why, how often, where it originates, and how it stops or reverses.

Test the system against both sparse and dense real content before multiplying components.

## Composition and rhythm

- Give each section or screen a job in the user's journey.
- Establish a few strong alignment anchors, then use deliberate variation where content changes.
- Balance visual mass optically; mathematical equality is not automatically visual balance.
- Use negative space to reveal hierarchy and pacing, not to conceal missing content.
- Use containers only when they express grouping, clipping, interaction, or material.
- Let one or a small number of high-attention gestures carry the identity while surrounding structure stays disciplined.
- Keep the first viewport legible at a representative small target size; do not force the whole product into it.

## Style coherence

A coherent style is a set of related decisions, not a palette plus radius preset. Check whether typography, shape, spacing, imagery, borders, surface treatment, icon weight, and motion seem to belong to the same material and cultural world.

Intentional contrast is allowed. A sharp element inside a soft system, an asymmetric break in a strict grid, or an expressive display face in an otherwise quiet interface can create productive tension when the contrast has a clear role. Repeating the exception everywhere destroys the tension.

## Content and asset integrity

- Use believable copy and real supplied assets before inventing placeholder brands, fake metrics, or pseudo-technical labels.
- Keep imagery consistent in crop, grade, subject, and narrative role unless contrast itself is the concept.
- Do not force imagery into tools, dashboards, or workflows where typography and data are the content.
- Treat copy as part of the visual system: verbosity, label length, tone, and information order alter composition.
- Confirm rights and runtime availability for fonts and media.

## Genericity and generator-fingerprint review

Run the content-swap check from `aesthetic-judgment.md`: if an unrelated product could inherit the same skeleton, type logic, palette role, and decorative devices with only nouns replaced, find where the brief has not yet shaped the design.

Then inspect the dated examples in `aesthetic-signals.md`. Flag a pattern only when it is being used from habit rather than because it fits the current brief. Do not replace one generator cliché with a different fashionable cliché just to appear original.

## Rendered critique

Inspect representative sizes with real content. Review in this order:

1. Does the composition and scan order communicate the intended hierarchy before polish is considered?
2. Do type, scale, spacing, visual mass, and alignment feel optically resolved?
3. Does the style have a coherent internal grammar and enough subject specificity?
4. Does the memorable gesture strengthen the concept, or is it decorative noise?
5. Do hover, focus, active, loading, empty, error, long-content, reduced-motion, and responsive states preserve that grammar?
6. Are accessibility, contrast, clipping, wrapping, input behavior, and performance good enough that the aesthetic survives real use?

Compare the rendered result to the design read and correct the largest mismatch first. Do not compensate for a weak composition by adding more effects.

## Calibration of this skill

When revising design guidance, test multiple deliberately different briefs rather than one showcase. The resulting designs should share quality of judgment but not collapse to the same composition, typography family, palette structure, card grammar, or motion style.

If a new rule improves one aesthetic but makes unrelated styles converge, narrow the rule to its actual context or move it to a dated reference instead of the durable core.
