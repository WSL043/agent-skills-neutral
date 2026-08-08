# Interaction quality protocol

Use this reference when an interface must survive real keyboard, touch, assistive-technology, localization, long-content, and asynchronous use. It complements visual judgment; it is not a substitute for the product's own platform rules.

## Semantics and focus

- Use native interactive elements for their intended roles before reaching for ARIA or click handlers on generic containers.
- Every interactive control needs an accessible name, and decoration should stay out of the accessibility tree.
- Every user flow must remain operable from the keyboard where the platform supports keyboard input.
- Focus must stay visible, move deliberately when dialogs or validation change the task, and return to a sensible origin when temporary surfaces close.
- Do not disable browser zoom or rely on color as the only carrier of state or meaning.
- Announce important asynchronous status changes through the platform's accessible notification mechanism.

## Forms and input

- Associate controls with meaningful labels, names, autocomplete hints, input types, and input modes when those semantics exist.
- Let users paste. Do not make validation depend on blocking ordinary editing behavior.
- Keep the whole visible control target interactive; avoid dead zones between a label and its checkbox, radio, or related control.
- Show validation close to the affected field and make recovery discoverable. On failed submission, move attention to the first actionable error when that improves recovery.
- Preserve unsaved user input across validation, rerenders, and hydration. Warn before destructive navigation when the platform cannot otherwise preserve it.
- Loading and disabled states must explain what is happening without erasing the action or value the user was working with.

## Navigation and state

- Use links for navigation so browser and platform navigation behaviors continue to work.
- Put shareable or history-sensitive state in a durable navigation surface such as the URL when that matches the product model; do not hide important navigation state in ephemeral component state.
- Back, forward, refresh, deep links, and restored scroll position should preserve the user's mental model where the platform provides those behaviors.
- Destructive actions need a deliberate recovery model: confirmation before irreversible work, or a trustworthy undo/restore path.

## Responsive and content resilience

- Test sparse, typical, dense, empty, error, and very long real content. Flex/grid children, labels, tables, media, and controls must wrap, truncate, scroll, or reflow intentionally rather than break the layout.
- Respect device safe areas, virtual keyboards, zoom, browser chrome, and input modality when they affect usable space.
- Prefer intrinsic layout and CSS/platform layout systems over JavaScript measurement unless measurement is genuinely required by the interaction.
- Verify at representative small, medium, and large target viewports instead of encoding a universal breakpoint or device list.

## Motion and direct manipulation

- Honor reduced-motion preferences and keep interaction-critical state understandable without animation.
- Motion should communicate feedback, continuity, hierarchy, or causality; it must remain interruptible when the user changes direction.
- Prefer properties and mechanisms that avoid unnecessary layout work, but measure real performance before treating an implementation technique as universally faster.
- Dragging, scrolling, overlays, and nested surfaces should define selection, overscroll, pointer, and focus behavior deliberately so multiple interaction systems do not fight each other.

## Media, rendering, and performance

- Give images and media stable geometry when their dimensions are known so loading does not unexpectedly move surrounding content.
- Prioritize only resources that materially affect the first useful view; defer non-critical media and work according to measured behavior.
- Avoid reading layout and writing layout-affecting styles in a pattern that repeatedly forces synchronous reflow.
- Virtualize or otherwise bound rendering when measured list or document size makes full rendering harmful; do not use a fixed item-count threshold as a universal rule.
- For server/client rendered interfaces, verify hydration preserves values, focus, semantics, and visible state instead of merely suppressing mismatch warnings.

## Locale and verbatim content

- Format dates, times, numbers, currencies, and text direction using locale-aware platform APIs rather than hardcoded display conventions.
- Prefer user language settings to location inference when choosing language.
- Protect brand names, code tokens, identifiers, and other verbatim strings from automatic translation when the platform supports an explicit mechanism such as `translate="no"`.
- Check expansion, contraction, alternate scripts, and long translated labels as layout inputs rather than treating localization as a copy-only change.

## Verification

Inspect the rendered product, not only source code:

1. Complete the critical flow with keyboard and pointer/touch input as applicable.
2. Inspect focus order, accessible names/roles, validation recovery, and asynchronous announcements.
3. Exercise navigation history, refresh/deep links, long content, empty/error/loading states, zoom, reduced motion, and representative viewports.
4. Check console/runtime errors, hydration behavior, layout shifts, and measured interaction performance when relevant.
5. Treat a checklist item as a finding only when it applies to the current platform, product contract, and actual rendered behavior.
