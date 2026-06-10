# Quality Scorecard

Use this file when creating or evaluating `quality_scorecard`.

## Scoring Rule

Score exactly five criteria from `0` to `100`. The pass threshold is `95` for every criterion.

Formula: `round(100 * passed_weight / applicable_weight)`.

Mark a subcheck `not_applicable` only when the surface truly does not exist in the game, and state the evidence. Any hard failure caps the criterion at `94` even if the weighted score would be higher. A release-facing change is not complete until all five scores are at least `95`.

## Criteria

### 1. Discovery and extraction coverage

- Engine/runtime evidence, adapter choice, and patching risk are documented: `20`.
- All likely text surfaces are inventoried, including structured tables, scripts, subtitles, images/textures, launcher text, and runtime-only bundles: `25`.
- Extraction is reproducible from commands or scripts and records source hashes/build IDs/platform versions: `20`.
- Platform forks and runtime subtitle surfaces are separated instead of merged by assumption: `20`.
- Unknown or high-risk assets have an explicit follow-up queue: `15`.

### 2. Context and source-language control

- Lore packet, glossary/style bible, and forbidden/deprecated renderings exist before batching: `25`.
- `source_language_matrix` records each available source language, original language when known, quality signals, and controlling source by surface: `25`.
- Dialogue, cutscenes, emotional intent, speech level, jokes, sarcasm, and relationship distance prefer Japanese when it is available and demonstrably usable; if Japanese is missing, localized poorly, compressed, misaligned, or lower quality than the original language, use the original or best available source instead and record the reason: `20`.
- UI, item names, location names, system terms, quest conditions, and crafting terms prefer approved glossary/current Korean and original/English term evidence over inventing names from Japanese: `15`.
- Unresolved names, lore conflicts, and weak evidence are queued instead of silently guessed: `15`.

### 3. Segmentation and agent orchestration

- Translation plan separates UI, system, tutorial, item, quest, dialogue, subtitle, texture/image, and other surfaces by tone and risk: `20`.
- Character/script separation uses real speaker evidence where available, not only key prefixes; mixed, player-choice, narration, and side-NPC rows are isolated: `25`.
- Every batch has a contract with category, controlling source language, references, glossary/tone rules, forbidden patterns, output schema, and acceptance gates: `20`.
- Subagents produce proposal tables or reviewed change logs; they do not directly mutate source JSON, registries, override files, or game bundles unless explicitly assigned to an apply step: `15`.
- Progress counts distinguish translated, reviewed-keep, policy-excluded, structural-excluded, actionable untranslated, and pending evidence: `20`.

### 4. Korean localization quality

- Source meaning, gameplay function, quantities, conditions, buttons, rewards, and emotional intent are preserved: `25`.
- Korean reads as native game text, not source-order machine output or ending-only post-editing: `25`.
- Speaker voice and surface register fit dialogue, subtitles, UI labels, tutorials, item flavor, system messages, mail, notices, and patcher text: `20`.
- Terminology, names, item families, facilities, controls, and styled spans are consistent across common and platform working sets: `15`.
- Accepted tester or QA findings update exact replacements, glossary/style rules, regression watchlists, or playtest packs: `15`.

### 5. Technical, runtime, and release QA

- Keys, schema, placeholders, format tokens, rich-text tags, control glyphs, escapes, and line-break constraints are preserved: `25`.
- Automated QA covers structure, glossary hard gates, source-target drift, mixed-language residue, UI length, speaker tone, and regression watchlists: `20`.
- Runtime application is verified on each supported platform, including subtitle-specific surfaces and smoke checks when the game has them: `20`.
- Release packages exclude original game assets, install/update/restore from a clean baseline, and expose a non-technical user path: `20`.
- Release notes, public notices, version detection, package digest, known issues, and report format match the shipped artifact: `15`.

## Phase Gates

- Before translation: criteria `1`, `2`, and `3` must be at least `95`.
- Before playtest: criteria `3`, `4`, and `5` must be at least `95`.
- Before public release: all five criteria must be at least `95`.
