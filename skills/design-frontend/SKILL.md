---
name: design-frontend
description: "Design, implement, audit, or redesign web and application interfaces with a coherent visual direction, faithful reference translation, complete states, accessibility, responsiveness, and rendered QA. Use for new UI, visual redesign, image-to-code work, design systems, component composition, or anti-generic interface polish."
---

# Design Frontend

## Goal

Create an interface whose visual language is specific to its product and audience, whose hierarchy and relationships hold together as a design rather than a template, whose implementation preserves those choices, and whose critical states remain usable across target viewports and input modes.

## Workflow

1. Inspect the product, audience, task, content, brand, existing routes/components/tokens, real assets, platform conventions, references, and target viewports.
2. Write a one-line design read: what this is, who it is for, what should feel distinctive, the intended hierarchy/density/material character, and what must remain quiet or familiar. Ask one question only when a missing choice materially changes the direction.
3. Derive the visual language from the subject and brief. Choose an established design system when it is genuinely authoritative; otherwise define one coherent aesthetic grammar across typography, composition, color/light, shape/material, imagery, and interaction.
4. Establish hierarchy and composition before decoration. Decide what dominates, what supports it, where visual tension belongs, which alignments anchor the page, and what one relationship or gesture makes the result recognizable.
5. Design the critical flow plus loading, empty, error, success, disabled, focus, overflow, long-content, and permission states that actually apply.
6. If a visual reference is the source of truth, extract its system and intentional irregularities rather than merely matching isolated pixels or normalizing it into the agent's usual component grammar.
7. Implement responsive components around content priority and existing architecture. Preserve information architecture and behavior during redesign unless structural change is approved.
8. Render and critique representative states. Judge hierarchy, proportion, optical balance, rhythm, specificity, style coherence, content integrity, interaction feel, accessibility, and performance before adding further polish.

## Decision rules

- No visual style is inherently superior. Judge minimal, editorial, luxury, brutalist, playful, technical, experimental, utilitarian, and other directions by how well their own visual logic serves the brief.
- Prefer choices that can be explained from product meaning, content, interaction, audience, or deliberate visual tension over choices justified only by trend or familiarity.
- Use real brand/product assets when they exist; generate or source new media only when it has a defined narrative or structural role.
- Prefer existing system components when they meet interaction and visual intent; extend deliberately when the brief needs a distinctive high-attention surface.
- Treat common patterns as neutral tools. A card, gradient, serif, pill, bento grid, glass surface, or asymmetry is acceptable when it is the clearest expression of the current design and suspect when it appears as an unrelated default.
- When a design feels generic, diagnose the repeated mechanism instead of swapping to a different fashionable motif.

## Guardrails

- Do not encode personal taste, one designer's preferences, or one model era's anti-pattern list as universal aesthetic law.
- Do not default to repetitive card rows, nested containers, decorative labels, fake metrics, generic prestige cues, or one composition repeated through every section without a content reason.
- Do not encode hierarchy with color alone.
- Do not impose arbitrary style dials, fixed image counts, mandatory dark/light mode, fixed fonts, a fixed framework, or motion intensity without authority from the brief, project, platform, or measured evidence.
- Do not polish the happy path while omitting failure, long-content, responsive, keyboard, or reduced-motion states.
- Do not alter routes, analytics, accessibility behavior, brand recognition, or core copy during a visual redesign without evidence and approval.

## Completion evidence

- The rendered design has a brief-specific visual rationale and does not collapse to the same system used for unrelated briefs.
- Critical flows work at target viewports with keyboard, touch, and assistive semantics where applicable.
- Typography, spacing, proportion, contrast, alignment, material consistency, content integrity, state coverage, and visual-reference fidelity are reviewed from rendered output.
- Any claimed generator-default issue names the recurring visual mechanism rather than relying on the label "AI-looking."

## Conditional reference

Read [references/variants.md](references/variants.md) to select the task mode. Then load only the linked detail references for that mode.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
