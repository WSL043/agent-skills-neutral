---
name: produce-programmatic-video
description: "Plan, assemble, edit, render, and verify programmatic video timelines from source media, code, narration, captions, and scene assets. Use when a video file or timeline is the primary deliverable and timing, synchronization, rendering, or media QA must be controlled."
---

# Produce Programmatic Video

## Goal

Produce or revise a time-based video artifact whose timeline, source assets, synchronization, delivery properties, and final rendered output are explicit and verifiable.

## Workflow

1. Inspect the real source assets and current project state. Probe available media and record the delivery contract that actually applies: target duration, aspect or dimensions, frame/time base, audio, captions, destination constraints, locked scenes or approved material, and source-of-truth files.
2. Translate intent into a scene, shot, or timeline specification. Record first and final states, local versus global timing, narration or audio cues, transitions, asset dependencies, approval boundaries, and proof timestamps for risky moments. Ask only for choices that cannot be derived from the assets or existing project.
3. Choose the least destructive production path. Prefer editable source scenes, timeline manifests, and original media over repeatedly patching an already compressed final master. Preserve approved content and timing unless the requested change requires them to move.
4. Build only the layers the task needs. Establish visual scene outputs and a stable timing source, synchronize affected segments, then add requested captions, overlays, narration, music, or other audio before the final encode. When one cue changes, retime or re-render the smallest affected region instead of shifting unrelated downstream work.
5. Preview expensive or subjective decisions before a full final render. Use representative stills, proof frames, short moving previews, media probes, or equivalent evidence at scene boundaries, synchronization points, dense caption frames, crops, and transitions.
6. Build the final output from the current approved sources. Probe the resulting media and inspect the rendered master rather than relying only on source code, scene files, or an intermediate preview.
7. Report the final path, source/timeline decisions, delivery metadata, synchronization or retiming changes, verification artifacts, and any visual or audio judgment that remains unverified.

## Decision rules

- Choose the timing source that matches the task: final narration when speech drives the edit, source timecode when preserving recorded action, or an explicit storyboard/timeline when neither dominates.
- Keep one authoritative timeline or equivalent record when captions, audio, scenes, and downstream edits depend on shared timing.
- Patch source artifacts and rebuild affected outputs when sources exist; edit the final compressed master directly only when it is genuinely the authoritative or only available source.
- Codec, container, frame rate, dimensions, bitrate, caption style, loudness, and hardware acceleration are delivery- and runtime-specific decisions. Derive them from the target, actual media, available tools, and current authoritative documentation rather than universal defaults.
- Treat a locked or approved scene, frame, transition, crop, or timing range as a preservation constraint until the user authorizes a change.
- Subjective visual or audio choices need rendered or listened-to evidence; structural validation alone cannot prove aesthetic quality, readability, sync, or mix balance.

## Guardrails

- Do not invent a frame rate, codec, quality setting, bitrate, caption layout, music level, or transition duration merely because a source example used one.
- Do not globally retime, redesign, recolor, or regenerate unrelated material to fix a local problem.
- Do not claim a final render is correct because the composition source, command, or build succeeded; inspect the produced media.
- Keep private footage, recordings, voices, credentials, session data, and licensed assets within their authorized handling boundary.
- Do not make paid or externally hosted generation calls without authorization appropriate to their cost and data effects.

## Completion evidence

- The authoritative sources, timeline or timing decisions, and delivery contract are identifiable.
- Final duration, dimensions or aspect, frame/time base, and audio stream state are verified when relevant to the deliverable.
- Requested captions, narration, music, transitions, crops, or scene changes are checked in the final rendered media at the points where failure would be visible or audible.
- Scene boundaries or other synchronization-critical moments have proof frames, short previews, contact-sheet evidence, or an equivalent verification method when useful.
- Unverified subjective or platform-specific conditions are stated rather than assumed.

## Related skills

- `design-motion`
- `design-visual-theme`
- `verify-completion`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
