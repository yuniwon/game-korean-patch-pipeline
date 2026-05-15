# Table-File Adapter

Use this file when the localizable content already lives in JSON, CSV, TSV, XLSX, or similar structured tables.

## Why this is the v1 fast path

Structured tables support the most reliable version of this skill:
- discovery is simpler
- schema safety is explicit
- batching is deterministic
- QA can be automated aggressively

## Rules

- Treat keys, IDs, and non-text columns as immutable.
- Identify the exact translatable columns before editing anything.
- Preserve escaping, quoting, separators, placeholders, and inline tags.
- Prefer file/path-based grouping only when it aligns with functional categories.

## Recommended flow

1. inventory every candidate table
2. map text columns and schema invariants
3. derive categories from content and path patterns
4. build risk-scored batches
5. translate into a working copy
6. run structural and terminology QA
7. package a reversible playtest artifact if the game supports it

## Common traps

- translating metadata columns
- breaking CSV quoting or separator rules
- treating every duplicate English string as globally identical
- skipping lore research because the files feel self-explanatory
