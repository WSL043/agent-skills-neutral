---
name: develop-shaders
description: "Develop, port, debug, or optimize real-time graphics shaders with explicit coordinate spaces, numerical constraints, visual targets, and GPU-aware verification. Use for GLSL, HLSL, WGSL, materials, post-processing, procedural effects, or shader performance work."
---

# Develop Shaders

## Goal

Deliver a visually correct shader that compiles across intended targets and stays within the declared performance budget.

## Workflow

1. Identify shader stage, language/profile, renderer, coordinate conventions, color space, precision, inputs, and target hardware.
2. Create the smallest compilable shader and a deterministic test scene before adding the effect.
3. Build the effect from named spaces and intermediate values; visualize masks, normals, depth, and ranges while debugging.
4. Handle edge cases such as zero length, discontinuities, UV seams, depth conventions, and out-of-range values.
5. Capture reference frames and profile instruction cost, texture access, branching, overdraw, and precision.
6. Test intended platforms, quality levels, camera conditions, and representative content.

## Decision rules

- Use analytic functions for simple procedural shapes and textures when they are cheaper than sampled assets.
- Move invariant computation to CPU or earlier stages when interpolation and precision permit.

## Guardrails

- Do not optimize before a reference image and bottleneck measurement exist.
- Do not rely on undefined behavior, NaN propagation, or one vendor's compiler quirks.
- Do not mix coordinate or color spaces implicitly.

## Completion evidence

- The shader compiles without warnings on intended backends and matches reference captures.
- Profiling supports the performance claim and visual edge cases are exercised.

## Related skills

- `capture-screen`
- `verify-completion`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
