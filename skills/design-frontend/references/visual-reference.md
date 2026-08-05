# Visual reference to implementation

## Use the clearest source

Prefer the user's native design file or supplied screenshot/mockup. Generate a reference first only when visual direction is central and no adequate source exists. The number of references follows uncertainty and readability, not section count.

Generate or request an additional focused reference when text, spacing, controls, or responsive intent cannot be read reliably. Prefer a fresh focused render over enlarging a tiny crop whose proportions are already distorted.

## Extract before coding

Record:

- hierarchy, grid, alignment anchors, whitespace, and section/screen rhythm;
- visible copy and content priority;
- type roles, line wrapping, scale relationships, and density;
- semantic palette, borders, radius, elevation, and media treatment;
- component/state family and any implied interaction;
- what is ambiguous and must be inferred or clarified.

Separate observed evidence from inferred implementation. Do not mistake image-generation artifacts for intended UI.

## Implement without drift

Build semantic, responsive components that reproduce the observed system rather than tracing fixed pixels. Reuse supplied assets and repository primitives when they preserve fidelity. Resolve missing details by system consistency first, then by a focused reference or user decision—not a generic template.

## Compare

Render the implementation at matching viewports. Compare major geometry, hierarchy, typography, palette, assets, component details, and visible states. Fix the largest perceptual mismatch first, then verify responsive and accessibility behavior the static reference cannot prove.
