# Workflow

Use this file after the main skill triggers and the target game workspace is known.

## Required outputs

Produce these artifacts in order:
1. `engine_report`
2. `localization_asset_inventory`
3. `extraction_manifest`
4. `source_language_matrix`
5. `lore_packet`
6. `localization_quality_standard`
7. `style_bible`
8. `translation_plan`
9. `agent_batch_contracts`
10. `quality_scorecard`
11. `translated_working_set`
12. `qa_report`
13. `playtest_pack`
14. `release_decision`
15. `release_package`
16. `release_notice`

Do not skip an artifact because the game "looks simple." The point is reproducibility.

## Phase order

### 1. Project intake

- Inspect the folder layout and executable/runtime neighbors.
- Infer the probable engine family and patching risk.
- Record evidence in `engine_report`.

### 2. Source discovery

- Find likely localization assets.
- Separate structured text, binary assets, and support files.
- Record source path, file type, candidate text columns/keys, and risk in `localization_asset_inventory`.
- Record extraction commands, hashes, row counts, platform/build versions, failed assets, and runtime-only text candidates in `extraction_manifest`.

### 2.5 Source-language matrix

- Identify available languages and the likely original language.
- Compare key/row alignment, missing rates, placeholder parity, obvious compression, and translation quality.
- Select a controlling source per surface. Prefer Japanese for dialogue, cutscenes, emotional intent, speech level, jokes, sarcasm, and relationship distance only when it is present, aligned, and higher-quality than the original or other available sources.
- Prefer approved glossary/current Korean and original/English evidence for UI labels, item names, system terms, quest conditions, controls, and crafting materials.
- Record fallback reasons whenever the normally preferred source language is not used.

### 3. Lore research

- Browse public sources before main translation when names, lore, factions, locations, or tone matter.
- Summarize what is known, what is uncertain, and what needs conservative handling.
- Output a `lore_packet` plus glossary candidates.

### 3.5 Extracted-text lore pass

- Read high-signal extracted in-game text before final translation polish: diary, codex, lore, item descriptions, objectives, cutscene/dialogue headers, and repeated proper nouns.
- Update `lore_packet`, glossary, and "do not drift" terminology from the extracted text.
- Record unresolved names or ambiguous terms with conservative temporary translations instead of silently guessing.
- Do this even if web research already exists; public sources often miss the exact in-game wording.

### 3.7 Localization quality standard and style bible

- Write a `localization_quality_standard` before main translation: what "good Korean" means for this game, target audience readability, surface-specific style, naturalness rules, common literalness risks with before/after examples, and LQA gates.
- Convert the lore packet into an enforceable `style_bible`: canonical Korean names for people, places, factions, items, events; forbidden or deprecated translations with reasons; character tone cards (speech level, relationship to player, verbal habits, exceptions); localization policy for culture-specific terms.
- Both documents are living control documents — update them from evidence (playtest findings, QA failures, repeated patterns), never from personal preference alone.
- Do not start bulk translation until both documents exist.

### 4. Translation planning

- Split work by function and tone domain: UI, systems, tutorial, items, quests, dialogue, other.
- Mark high-risk slices before batching.
- Output a `translation_plan` with category, subcategory, batch ownership, and risk notes.
- Build `agent_batch_contracts` before dispatching any work. Each contract must state the controlling source language, required references, glossary/tone rules, forbidden patterns, output schema, allowed actions, and QA gates.
- Keep speaker worksets and unresolved/mixed queues separate from UI, narration, and player choices.

### 5. Draft translation

- Translate into a working dataset, never straight into original game assets.
- Preserve keys, schema, placeholders, tags, and escapes.
- Reuse approved glossary terms and benchmark translations only where they fit current evidence.
- Treat machine translation and AI draft text as unapproved draft material. Do not mark a row final merely because the Korean exists.

### 5.5 Manual localization polish

- Review by category, speaker, or lore surface rather than a single mixed dump.
- Rewrite Korean from the intended meaning, player context, and tone; do not merely smooth literal machine output.
- For narrative text, check who knows what, what the line is trying to imply, and whether the Korean sounds like a game line a Korean player would accept.
- For UI text, rewrite for function and space: labels short, descriptions clear, tutorials direct.
- Promote rows to reviewed/final only after they pass glossary, structure, and naturalness expectations.

### 6. Automated QA

- Run structural, terminology, consistency, and length-risk checks.
- Fail closed on placeholder or tag breakage.
- Output `qa_report` and a retranslation queue when needed.
- Maintain a five-criterion `quality_scorecard`: discovery/extraction coverage, context/source-language control, segmentation/agent orchestration, Korean localization quality, and technical/runtime/release QA.
- Do not advance to translation until the first three criteria are at least `95`; do not advance to playtest until segmentation, Korean quality, and technical QA are at least `95`; do not publish until all five criteria are at least `95`.

### 7. Playtest packaging

- Build a test-ready patch artifact or an inject-ready intermediate file.
- Package tester instructions and issue intake format as `playtest_pack`.
- Feed accepted findings back into glossary and translation fixes.

### 8. Release packaging

- Build from the reviewed working set, not from a manually edited game folder.
- Test install on a clean original baseline or a freshly verified game install.
- Test restore from the same installer-generated backup.
- Provide a beginner-friendly install/restore path: GUI, launcher, or menu. CLI flags may remain as an advanced path only.
- Verify the package contains no original game executable, full data directory, bundles, assets, or other copyrighted game files.
- Record release version, digest, package contents, tested game/platform version, and known issues.

### 9. Release notice

- Draft a Korean user-facing notice before or alongside the GitHub release.
- Include latest version, supported platform/game version, download link, install/update steps, restore steps, automatic actions, known issues, report format, and unofficial patch disclaimer.
- Prefer a reusable template such as `assets/release_notice_template_ko.md` when the user has an established blog style.

## Hard stops

- Do not start bulk translation before `engine_report`, `localization_asset_inventory`, and `lore_packet` exist.
- Do not start bulk translation before `extraction_manifest`, `source_language_matrix`, `agent_batch_contracts`, and pre-translation scorecard gates are at least `95`.
- Do not package a test build before `qa_report` is clean enough for playtesting.
- Do not overwrite original game assets during normal translation passes.
- Do not publish a public release until install and restore have been tested from a clean original baseline.
- Do not publish a public release whose basic install or restore flow requires command-line knowledge.
- Do not publish a package that contains original game assets unless explicit rights allow it.
