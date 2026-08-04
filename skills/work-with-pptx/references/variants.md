# Implementation variants

## New-deck generation

Use an editable slide-generation library, a shared theme, reusable geometry helpers, and deterministic layout checks.

## Existing-template editing

Map content to real layouts first. For transformations unsupported by a high-level library, unpack the OOXML package, edit relationships and slide XML, then repackage and validate.

## Orchestrated production

Treat narrative planning, slide implementation, visual-system selection, and package editing as support modules behind one skill. Run deck-level QA after module outputs are combined.
