# Design quality protocol

## Design read

Before implementation, state one compact direction:

- product/page kind and primary user action;
- audience and emotional character;
- visual concept and one recognizable motif;
- hierarchy and composition approach;
- variance, motion, and density on low/medium/high scales;
- existing assets, design system, and constraints to preserve.

Use a documented design system when the product or platform calls for one. Use an aesthetic direction when the brief is brand-led. Do not mix several systems into a collage.

## System extraction

Define semantic rules rather than isolated values:

- typography roles, line length, wrapping, and fallback behavior;
- background, surface, text, border, accent, status, and data colors;
- layout grid, gutters, vertical rhythm, content width, and breakpoints;
- shape, border, elevation, material, icon, and media treatment;
- interaction hierarchy, focus, disabled, loading, empty, error, and success states.

Test the system against both sparse and dense real content before multiplying components.

## Composition and rhythm

- Give each section or screen a job in the user journey.
- Vary composition when the content changes; preserve common alignment anchors so the product still feels related.
- Use negative space to clarify hierarchy, not to conceal missing content.
- Use containers only when they express grouping, clipping, interaction, or material—not as default decoration.
- Keep the first viewport legible at a representative small target size; do not force the whole product into it.

## Content and asset integrity

- Use believable copy and real supplied assets before inventing placeholder brands, fake metrics, or pseudo-technical labels.
- Keep imagery consistent in crop, grade, subject, and narrative role.
- Do not force imagery into tools, dashboards, or workflows where typography and data are the content.
- Confirm rights and runtime availability for fonts and media.

## Anti-default review

Ask whether the design repeats a familiar generator shortcut: identical cards, one left/right layout, generic glow, giant rounded wrappers, tiny pills, decorative dashboards, or unmotivated gradients. Replace only the shortcuts that weaken the brief; a common pattern is acceptable when it is the clearest solution.

## Rendered QA

Inspect at representative sizes with real content. Check scan order, clipping, wrapping, alignment, contrast, focus, pointer/touch targets, reduced motion, slow loading, empty/error states, and layout stability. Compare the output to the design read and correct drift before adding more decoration.
