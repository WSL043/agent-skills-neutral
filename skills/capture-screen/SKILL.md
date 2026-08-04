---
name: capture-screen
description: "Capture full screens, windows, applications, or bounded regions with correct coordinates, scale, and privacy handling. Use when visual evidence, UI diagnosis, documentation, or pixel-based verification requires a screenshot."
---

# Capture Screen

## Goal

Produce a correctly scoped screenshot with enough metadata to support reliable visual reasoning.

## Workflow

1. Identify the target display, window, client area, or region and the reason for capture.
2. Record display scale, coordinate system, window bounds, and whether occlusion is acceptable.
3. Choose an OS, browser, or application capture path that preserves the needed fidelity.
4. Capture the smallest sufficient region and store it in a task-local location.
5. Inspect the image dimensions and content; recapture if the target is clipped, stale, covered, or scaled unexpectedly.
6. Remove or mask unrelated sensitive information before sharing.

## Decision rules

- Use application-native capture when window occlusion or HDR handling matters.
- Normalize to logical/CSS pixels only when coordinates will be reused for interaction.
- Keep original pixels for fidelity-sensitive image inspection.

## Guardrails

- Do not capture unrelated displays, notifications, credentials, or personal content.
- Do not infer interaction coordinates from an image whose scaling is unknown.

## Completion evidence

- The image contains the intended target at known dimensions and scale.
- No unrelated sensitive content is visible in the shared artifact.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
