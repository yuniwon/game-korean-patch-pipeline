# Category Design

Use this file before batching. Informal grouping is not enough; always create a named `translation_plan`.

## Core categories

Start from these top-level groups:
- `UI`
- `System`
- `Tutorial`
- `Item`
- `Quest`
- `Dialogue`
- `Other`

Split further when tone, risk, or layout constraints differ.

## Risk signals

Raise the risk score when text includes:
- placeholders or rich-text tags
- very short UI labels
- narrow layout surfaces
- proper nouns without confirmed lore
- branching dialogue
- quest objectives or fail-state text
- repeated strings whose meaning may vary by context

## Batching rules

- Do not mix categories with different tone requirements in one batch.
- Keep dialogue separate from UI and item text.
- Keep high-risk strings in smaller batches.
- Prefer file/path coherence when it reinforces category boundaries.
- Duplicate-string handling can happen before unique-string translation, but only within compatible contexts.

## Human tester model

The default plan assumes humans are testers, not line-by-line reviewers.

Use narrow human spot checks only for:
- unresolved high-impact proper nouns
- risky UI surfaces with severe layout limits
- release-blocking narrative ambiguity

## Minimum plan fields

Every `translation_plan` should capture:
- category
- subcategory
- source files or tables
- estimated row count
- risk tier
- batch grouping
- required reference files
- tester focus after packaging
