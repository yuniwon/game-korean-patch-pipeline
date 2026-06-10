---
name: game-korean-patch-pipeline
description: Use when starting, maintaining, testing, or releasing a Korean game localization patch, especially for engine/text discovery, lore and terminology research, extracted-text lore passes, category batching, source-update sync, platform-specific text forks, mistranslation audits, speaker tone polish, QA gates, clean-original install/restore tests, beginner-friendly patcher UX, playtest handoff, GitHub release packaging, or blog/notice drafting.
---

# Game Korean Patch Pipeline

## Overview

Use this skill to turn an unfamiliar game or a live Korean patch into a structured localization workflow. The core principle is: `discover -> research -> plan -> translate or sync -> QA -> playtest -> release`, with humans acting mainly as testers rather than full-time line reviewers.

Modes: **Bootstrap** starts a new or poor-quality localization from extracted text; **Maintenance** updates an existing patch after game updates, user reports, platform divergence, or release-tool regressions.

## Required Outputs

Do not begin main translation until these artifacts exist:
- `engine_report`
- `localization_asset_inventory`
- `extraction_manifest`
- `source_language_matrix`
- `lore_packet`
- `localization_quality_standard`
- `style_bible`
- `translation_plan`
- `agent_batch_contracts`
- `quality_scorecard`

Do not hand work to playtest until these artifacts exist:
- `translated_working_set`
- `qa_report`
- `playtest_pack`

For a live patch maintenance pass, require these artifacts instead:
- `source_diff_report`
- `platform_matrix`
- `quality_standard_delta`
- `reviewed_change_log`
- `regression_watchlist`
- `updated_working_sets`
- `runtime_text_surface_inventory`
- `platform_runtime_delta_report`
- `qa_delta_report`
- `release_decision`
- `release_notice_full_template`

## Quality Scorecard

Use exactly five numeric criteria, each scored from `0` to `100` with a pass threshold of `95`: discovery/extraction coverage, context/source-language control, segmentation/agent orchestration, Korean localization quality, and technical/runtime/release QA. Any hard failure caps the relevant criterion at `94`. Read `references/quality-scorecard.md` when creating or evaluating the scorecard. Before translation, criteria `1`, `2`, and `3` must be at least `95`; before playtest, criteria `3`, `4`, and `5` must be at least `95`; before public release, all five must be at least `95`.

## Quick Start

### Bootstrap mode

1. Detect the engine and patching risk with `scripts/detect_engine.py`.
2. Inventory candidate text assets with `scripts/scan_localization_assets.py`.
3. Build an `extraction_manifest`: source paths, commands, hashes, extracted row counts, language files, failed assets, and runtime-only candidates.
4. Build a `source_language_matrix`: available languages, likely original language, quality/alignment signals, controlling source by surface, and fallback reasons.
5. Research the game on the web and compile a lore packet with `scripts/build_lore_packet.py`.
6. Read high-signal extracted lore, diaries, item descriptions, quests, and dialogue headers before locking names.
7. Write a project-specific localization quality standard: what "good Korean" means for this game, surface-specific style, literalness risks, LQA gates, and examples.
8. Convert lore into an enforceable style bible: canonical names, forbidden renderings, tone cards, and examples.
9. Split content into categories and risks with `scripts/build_translation_plan.py`.
10. Build `agent_batch_contracts` before dispatching work; each contract names the category, controlling source language, references, glossary/tone rules, output schema, and QA gates.
11. Translate into a working dataset only. Do not patch original game assets yet.
12. Score risky rows with `scripts/score_translation_risk.py` and keep high-risk rows in smaller review batches.
13. Maintain the five-part `quality_scorecard`; do not advance if any required criterion is below `95`.
14. Build a tester-facing issue sheet with `scripts/build_playtest_report_template.py`.

### Maintenance mode

1. Re-extract the current game text and compare it against the last supported source.
2. Inventory runtime text surfaces as well as the main localization table; cutscene subtitles, track display names, compressed subtitle assets, and platform supplements can change even when the main table is byte-identical.
3. Split the diff into `added`, `removed`, `changed`, `runtime-only`, and `unchanged-but-platform-specific`.
4. Safe-sync mechanical rows first; send semantic changes to manual or high-context review.
5. Update the localization quality standard, style bible, and regression watchlist before touching working sets.
6. Update common and platform-specific working sets separately; keep platform inject paths separate even after proven source parity.
7. For dialogue or character text, generate character review packs from the extracted scripts/working sets and review by character before editing tone.
8. Rebuild inject/patch assets from working sets, not from edited game bundles.
9. Run QA gates: JSON parse, token/tag preservation, glossary, source-anchored mistranslation audit, speaker tone, Korean naturalness/literalness, UI length, mixed-language audit, regression watchlist, runtime subtitle coverage, and platform-specific smoke checks.
10. Decide release strategy: same asset replacement only for non-auto-updater patches; new tag when existing launchers must detect an update.
11. Write release notes and public notices from the durable full template, then package and verify the published asset digest.

Read these references only when needed:
- `references/workflow.md` for the full order of operations
- `references/research-playbook.md` before web research
- `references/glossary-rules.md` when deciding terminology or tone
- `references/category-design.md` before batching or parallel translation
- `references/qa-gates.md` before merge, packaging, or playtest handoff
- `references/quality-scorecard.md` when scoring the five `95`-point acceptance gates
- `references/multi-agent-workflow.md` before dispatching parallel translation agents
- `references/font-insertion.md` when Korean glyph rendering or font replacement is required
- `references/adapter-unity.md`, `references/adapter-unreal.md`, or `references/adapter-table-files.md` after engine discovery
- `assets/release_notice_template_ko.md` when drafting Korean distribution posts, GitHub release notes, or user-facing patch notices

## Workflow Rules

### 1. Discover before translating

Always identify probable engine/runtime family and localization storage before drafting translations. If the engine is unclear, keep discovery open and report confidence rather than guessing.

### 2. Research before naming

If the game contains proper nouns, factions, locations, item families, lore terms, or speaker-specific tone, browse the web before locking Korean terminology. Use official sources first, then reputable wikis or community references, and record confidence when evidence is weak.

After text extraction, do an extracted-text lore pass before final polishing. Update the lore packet and glossary from in-game diaries, codex entries, item descriptions, objectives, and repeated named entities; web research alone is not enough for narrative games.

### 2.2 Write a project-specific localization quality standard

Before main translation, create or update a project-specific quality standard. Do not rely only on a generic style bible. The quality standard defines what "good Korean localization" means for this game and must include:
- target audience and expected Korean gamer readability
- surface-specific style: UI labels, buttons, tooltips, quest objectives, tutorials, subtitles, character dialogue, item flavor, system messages
- naturalness rules: no raw machine translation, no word-order preservation when it makes Korean stiff, no ending-only tone fixes
- common literalness risks with before/after examples
- LQA gates: source-target accuracy, Korean naturalness, speaker tone, UI length, token/tag preservation, platform divergence, regression watchlist
- accepted exceptions for English terms, abbreviations, brand names, model codes, or intentionally foreign in-world terms
- source-language hierarchy when multiple source languages exist

If the project already has an equivalent document, read it before translating and update it when new evidence appears. Do not create duplicate authority files unless the repo already uses that pattern.

### 2.3 Prefer source languages by surface

Do not assume English, Japanese, or the game's original language is always the best translation base. Choose a controlling source per surface and record it in `source_language_matrix`.

Default hierarchy:
- Character dialogue, subtitles, emotional intent, speech level, sentence rhythm, jokes, sarcasm, and relationship distance: Japanese first when it is present, aligned, and high quality because its honorifics, omissions, and distance markers often map better to Korean.
- If Japanese is missing, low quality, clearly mistranslated, over-compressed, machine-like, or weaker than the original language, use the original language or the best available source for that surface and record why Japanese was not controlling.
- UI labels, item names, location names, system terms, quest conditions, crafting materials, and already-approved glossary terms: approved glossary/current Korean first, then original/English source evidence, then Japanese for nuance.
- If multiple source languages disagree, preserve game function and established terminology first; send emotional or lore ambiguity to the evidence queue rather than guessing.

Japanese often carries honorifics, casual/polite contrast, omissions, kanji nuance, and word order that map better to Korean than English. Use that advantage for tone and prose, but do not create new Korean proper nouns from Japanese when the English source or project glossary already establishes the game term.

### 2.4 Build a source-language matrix before batching

For every source family or representative row group, record:
- `surface`: UI, item, quest, dialogue, subtitle, texture/image, launcher, system, or other.
- `available_languages`: language files or columns found, with row counts and missing rates.
- `original_language`: known, inferred, or unknown, with evidence.
- `alignment_quality`: row/key parity, placeholder parity, obvious truncation, machine-localized artifacts, and semantic disagreement.
- `controlling_source`: the language used for Korean decisions on that surface.
- `fallback_reason`: why a normally preferred language was not used.

The matrix is a gate artifact, not a note. Batch prompts, agent contracts, QA reports, and reviewed change logs must reference it.

### 2.5 Turn lore into enforceable style rules

A lore packet is background; a style bible is a control surface. Before batching, write:
- canonical Korean names for people, places, shops, factions, items, events, and UI concepts
- forbidden or deprecated translations with reasons
- character tone cards: speech level, relationship to player, recurring verbal habits, and exceptions
- localization policy for culture-specific terms: prefer the Korean gamer/common usage when it preserves meaning
- evidence keys or source snippets for high-risk decisions

Every translator prompt, batch instruction, and QA gate should reference the style bible. If a rule is important but not in glossary, tone policy, prompt text, or an automated check, it is not actually enforced.

The quality standard and style bible are living control documents. Improve them only from evidence:
- official sources, extracted game text, or in-game screenshots
- user playtest reports
- QA failures
- repeated mistranslation or literalness patterns
- confirmed conflicts with existing glossary, tone cards, or platform sources

When updating them, record the reason and make the rule reusable. Avoid adding personal preference as a rule without evidence.

### 3. Plan categories before batching

Do not translate a monolithic dump of mixed UI, dialogue, quests, and item text. Split content into stable categories, note risk level, and batch only within safe consistency boundaries.

For dispatching work to other agents, create one contract per batch. Minimum fields: `batch_id`, `surface`, `risk_tier`, `controlling_source_language`, `source_paths`, `row_count`, `required_references`, `glossary_refs`, `tone_refs`, `forbidden_patterns`, `output_schema`, `allowed_actions`, `qa_before_apply`, and `scorecard_criteria_touched`. Dialogue and subtitle contracts must also include speaker evidence or a rule that the agent must skip unresolved speakers.

### 4. Translate working sets, not original assets

Write translations into extracted or generated working files. Do not overwrite original game assets during early passes. Treat direct injection or repacking as an explicit later stage gated by QA.

### 5. Preserve structure mechanically

Do not change keys or schema. Preserve placeholders, format tokens, rich-text tags, escape sequences, and ordering requirements. If preservation cannot be guaranteed, stop and downgrade confidence instead of guessing.

### 5.5 Do not ship raw machine translation

Machine translation or AI draft output may be used only as a rough aid, never as accepted final text. Final Korean must be manually localized against source meaning, extracted lore, glossary, speaker tone, UI surface, and Korean gamer readability. Rewrite literal or stiff lines instead of lightly post-editing them.

### 5.6 Communication brevity does not apply to localized output

Compressed agent modes or terse status updates are only for coordination with the user. They must not shorten Korean translations, remove nuance, or flatten dialogue. Shorten target text only when the surface itself requires it, such as a UI label, button, or hard layout limit, and record that as a surface decision.

### 6. Treat humans as testers

Humans are not default line-by-line reviewers. Limit human intervention to:
- high-impact term sanity checks
- playtesting
- release approval for critical issues

### 7. Feed findings back into knowledge

Playtest findings are not disposable notes. Use accepted issues to update glossary choices, lore packet gaps, category heuristics, and retranslation targets.

Every accepted bug should produce at least one durable artifact:
- exact replacement or reviewed mapping if the issue is deterministic
- glossary/style-bible update if it affects future wording
- quality-standard update if it changes naturalness, surface style, or LQA expectations
- regression watchlist entry if the old bad string can reappear
- platform note if it was Steam/Xbox-specific

### 8. Treat platform divergence as first-class

If Steam, Xbox PC, Game Pass, console, or beta branches ship different text assets, do not force one localization file onto all platforms. Maintain:
- a common terminology/glossary layer
- one source baseline per platform
- one working set per platform if keys or values diverge
- one install-time selector that chooses the correct inject/patch asset by game path or platform metadata

Always verify platform-specific user reports against that platform's source, not against the other platform's bundle.

### 8.5 Runtime subtitle surfaces are separate localization surfaces

For Unity and asset-bundle projects, do not treat the main localization table as the whole subtitle system. User screenshots of English cutscene text must be verified against all known runtime subtitle surfaces, including `TIMELINE:*` rows, `PerformanceSubtitle` JSON fields, compressed MessagePack/LZ4 `PerformanceSubtitle` TextAssets, `KSubtitleClip.Template.content`, subtitle track display names such as `K Subtitle Track.m_Clips[*].m_DisplayName`, and platform-specific supplemental JSON. A cutscene fix is not complete until the patcher consumes every required supplemental source and the runtime subtitle missing count is zero for each supported platform.

### 8.6 Platform parity is evidence, not permission to collapse forks

Steam and Xbox/Game Pass may become byte-identical for a source table after an update, but that must be proven by current hashes, build IDs, package versions, row counts, and missing-key checks. After parity is proven, syncing one platform from another is allowed, but keep platform-specific source baselines, inject assets, install-time selectors, and release checks. If the main table is unchanged but runtime subtitle surfaces changed, ship a release anyway when users need the launcher to detect the update.

### 9. Count completion by outcome, not just translated rows

For progress and remaining work, separate:
- translated/applied
- reviewed-keep
- policy-excluded
- structural-excluded
- untranslated/actionable
- untranslated/non-actionable

Do not report raw untranslated rows as remaining work when they are placeholders, structural values, keys intentionally left in English, DLC/system names, or other documented exclusions.

### 10. Speaker tone polish is speaker-scoped

For character dialogue, inspect all high-confidence player-facing lines for that speaker together. Do not split by file prefix alone when the same character appears in talk, gift, shop, mail, bubble, and relationship dialogue.

Before editing tone:
- map aliases to canonical character names
- decide the character's player-facing speech level
- separate direct speech from player choices, narration, system text, and mixed-cast scenes
- record exceptions where a key group contains multiple speakers

Use bulk scripts only to apply already-reviewed exact replacements. Do not use broad regex or honorific conversion scripts to "fix" a character's tone.

### 10.1 Build character review packs before tone edits

When extracted scripts or working sets are available, build a character-scoped review table before polishing dialogue. The grouping must use more than raw key prefixes:
- alias registry: `dialog_character_alias_registry.tsv`
- scene overrides for aliasless scenes: `dialog_speaker_scene_overrides.tsv`
- alias+index patterns such as `TianRuLv4` or `FavorChat_TianRuLv4`
- generic buckets such as tourist/common NPC
- unresolved or mixed-speaker buckets

Each per-character review pack should include platform, speaker confidence, alias, canonical name, tone policy, surface, risk flags, key, source, and current target. Use it to read all `talk/chat/gift/shop/mail/date/bubble/mission/online` lines for that character together.

Do not edit from the pack blindly. Treat player choices, UI labels, narration, ambient self-talk, and mixed-cast scenes as separate review classes. If real character speech appears in the unresolved/mixed pack, update the alias registry or scene override first, regenerate the packs, then edit.

For unfamiliar games, create the equivalent of these artifacts even if filenames differ: `speaker_alias_registry`, `speaker_scene_overrides`, `speaker_evidence_index`, `speaker_worksets`, and `unresolved_or_mixed_queue`. Use engine-native dialogue metadata first when available, then file/path/key hints, then source text and scene context. A speaker pass cannot score `95` in segmentation if it relies only on key prefixes while better speaker evidence exists.

### 10.5 Naturalness pass is separate from correctness

After source correctness passes, run a Korean-naturalness pass on high-impact text: story, diary, quest, romance/date, tutorial, item flavor, subtitles, and public UI. For these surfaces, translation is not complete until the naturalness pass is done. Look for:
- stiff machine-like endings
- English or Chinese sentence order
- English-only subtitle phrasing that flattens Japanese speech level or emotional distance
- unclear subject/object after placeholder removal
- over-literal metaphors
- Korean terms that are technically correct but uncommon in games
- system-message wording that appears in character speech
- tone edits that only changed endings without rewriting the Korean sentence

Rewrite from intended meaning, not word order. For character lines, rewrite from `source meaning -> speaker intent -> Korean utterance`; do not preserve source part-of-speech or sentence shape when it hurts Korean readability. Keep compact UI labels short, but let descriptions read like natural Korean prose.

Maintain a literalness/naturalness watchlist. When a playtester reports a stiff phrase, search the same scene, family, speaker workset, and platform fork for variants before declaring it fixed.

### 11. Classify UI text before shortening it

UI text must be classified before changing length:
- `label`: short noun or status, prefer concise Korean
- `button`: short action phrase, avoid explanatory endings
- `tooltip`: can include guidance
- `description`: preserve full meaning even if longer
- `system/raw key fallback`: likely needs alias or missing key support

If a short source label has a separate explanatory key nearby, keep the label short and put guidance in the description. If no separate explanation exists, keep enough action guidance to avoid confusing players.

### 11.5 Run source-anchored mistranslation QA

Good Korean prose is not enough. After translation or update sync, compare source and target directly for meaning-critical drift:
- proper nouns and facilities: source name present but canonical Korean missing
- platform forks: same key has different Steam/Xbox source meaning
- multi-source drift: Japanese dialogue tone conflicts with English subtitle wording, or Japanese/English disagree on a proper noun
- raw English or CJK residue after stripping tags/placeholders
- literal false friends, machine-output artifacts, and typo patterns
- item/facility/action terms inside styled tags

Do this as a separate gate from tone, glossary, and UI length. Structural QA can pass while meaning is wrong.

When multiple source languages are available, record which source controlled the accepted Korean. For dialogue, Japanese normally controls tone and sentence shape while English helps identify canonical terms. For UI and item names, glossary/current Korean and English normally control the term while Japanese can confirm nuance.

When a source term maps to different Korean by platform, encode the platform split explicitly instead of forcing one common value. Example: if Steam says `Treasure Chest in Sylvain's Room` but Xbox says `Sewing Table`, each working set needs its own Korean.

Use broad scripts only for already-reviewed exact string pairs. For semantic fixes, keep a reviewed changelog with source, old Korean, new Korean, and reason.

For translation or polishing agents, require proposal output rather than direct blind edits when context risk is non-trivial:
- `key`
- `source`
- `old_target`
- `new_target`
- `reason`
- `confidence`
- `surface`
- `speaker` when applicable

Agent instructions must explicitly say that the goal is not to lightly post-edit machine translation, but to produce Korean that a local player would accept in the game context.

### 11.6 Maintain a regression watchlist

When a bad translation is found, add its old form to a watchlist before declaring the issue fixed. Include:
- old Korean pattern
- expected Korean pattern
- source term or key family
- allowed exceptions
- platform scope

Run the watchlist after every update sync. A fixed typo or wrong name should not be rediscovered by playtesters in the next patch.

### 12. Release decisions must account for launchers

If users update through a launcher that checks the latest GitHub release tag, changing only an existing ZIP asset may not be detected. Use a new release tag when:
- existing launchers need to see an update
- package metadata changes
- platform inject assets changed
- install/restore/update scripts changed
- user-facing hotfixes should reach existing users automatically

Asset replacement under the same tag is only safe when users are explicitly told to redownload that same version or when no auto-update detection depends on the tag.

### 13. Distribution must work for non-technical users

Treat CLI-only install or restore as a developer path, not a public release. Public packages should provide a double-click GUI, menu, or launcher that can:
- detect or browse for the game folder
- install/update the patch
- restore from the installer's own backup
- show clear success or failure messages
- avoid requiring PowerShell path syntax

### 14. Release from a clean original baseline

Before publishing, test install and restore from a clean original game state or a freshly verified equivalent. Do not validate release restore behavior only on a game folder that has already been manually patched; that can create empty or already-patched backups and make restore unreliable.

Before uploading a release ZIP, verify it contains no original game assets or full repacked game files unless rights explicitly allow it. Scan for engine-specific asset extensions and original executable/data directories.

## Red Flags

Stop and fix the workflow if any of these appear:
- translation starts before `engine_report`
- terminology is chosen without web research even though lore matters
- setting or lore docs exist but batch prompts and QA gates do not consume them
- no project-specific localization quality standard exists before main translation
- the quality standard exists but translators or QA gates do not consume it
- `source_language_matrix`, `agent_batch_contracts`, or `quality_scorecard` is missing before batch translation
- any required quality scorecard criterion is below `95` and work advances anyway
- UI, dialogue, and item text are mixed into one batch
- original game assets are patched before QA
- testers are expected to review every line manually
- no durable `qa_report` or `playtest_pack` exists
- live patch update starts without a source diff
- Steam/Xbox or beta/stable text differences are ignored
- a character tone pass uses broad automated honorific/banmal conversion
- a character has a tone card but shop, gift, mail, date, and bubble lines were not checked together
- a tone pass starts without a character review pack after script/text extraction
- alias+index keys such as `CharacterAlias4` are not grouped with the base character alias
- unresolved or mixed-speaker rows are translated directly instead of first updating alias/scene override evidence
- raw `$$UI:...$$` keys are fixed by guessing instead of finding the missing alias/source key
- QA passes but source-target semantic drift was never checked
- a source proper noun appears but the canonical Korean name is absent
- a facility name is translated as another facility because both are in the same domain
- Steam/Xbox source values differ but one Korean value is copied to both
- platform source parity is assumed without current hashes, build IDs, package versions, and missing-key checks
- cutscene subtitle fixes only patch the main localization table or `TIMELINE:*` rows while runtime subtitle assets remain unverified
- a release is skipped because the main source table is unchanged even though runtime text surfaces changed
- a playtest bug is fixed once but not added to glossary, style bible, or regression watchlist
- a playtest bug about stiffness or literalness is fixed once but not added to the quality standard or naturalness watchlist
- the Korean is fluent but uses an uncommon term where Korean gamers expect a conventional term
- release asset is replaced without deciding whether existing launchers will detect it
- remaining row counts include reviewed-keep or excluded structural rows
- raw machine translation is treated as complete because placeholders and schemas passed QA
- public package requires command-line knowledge for basic install or restore
- release restore was tested only over an already-patched local install
- release ZIP contains original game bundles, assets, executables, or full data directories

## Multi-Agent Parallel Work

Use parallel subagents only after shared lore, glossary, style, source-language, and batch-contract artifacts are stable. The orchestrator owns the knowledge base and merge decisions; subagents return scoped proposals. Read `references/multi-agent-workflow.md` before dispatching parallel agents.

## Engine Routing

After discovery, load only the relevant adapter reference:
- Unity or AssetBundle-heavy layout: `references/adapter-unity.md`
- Unreal or `.locres`/`.uasset` layout: `references/adapter-unreal.md`
- JSON/CSV/TSV/XLSX-heavy layout: `references/adapter-table-files.md`
- Cartridge-era ROM (SNES, GBA, NDS, PS1, etc.): `references/adapter-retro-rom.md`

If multiple engines or storage modes appear, prefer the cheapest high-confidence text path first and document fallbacks in the `engine_report`.

## Font Insertion

Font work is required whenever the game does not natively support Korean glyphs, especially retro ROMs and older Unity/Unreal titles. Read `references/font-insertion.md` when Korean renders as boxes, question marks, blanks, or clipped glyphs.

## Common Mistakes

### Using extracted strings alone as lore evidence

This causes late renaming and glossary churn. Build the `lore_packet` first when narrative context matters.

### Treating the setting bible as a reference document only

If agents merely read a setting document once, they will forget or override it under batch pressure. Convert important lore into canonical mappings, forbidden terms, tone cards, and QA checks.

### Treating quality standards as one-time paperwork

A quality standard is not a preface. It should change when playtesters report stiff Korean, when an LQA gate catches a new class of issue, or when repeated literal patterns appear. Feed those findings back into prompts, watchlists, and reviewed changelogs before continuing the next batch.

### Skipping the extracted-text lore pass

Public pages and wikis rarely capture all in-game wording. After extraction, read high-signal lore, diary, item, quest, and objective text and update terminology before final polish.

### Treating "fast" as "skip artifacts"

Speed comes from reusable artifacts, not from omitting them. If another agent cannot restart from your outputs, the workflow is incomplete.

### Overusing manual review

If the default plan still depends on a human reading everything, the pipeline is not AI-first. Fix automation, QA, or risk routing instead.

### Fixing the same class of issue repeatedly

If a bad term appears once, assume variants exist. Search the whole working set, add a regression watchlist entry, and update the style bible so future batches inherit the correction.

### Repacking too early

Do not jump straight from translation to game-asset patching. A separate working dataset plus QA catches cheaper failures first.

### Treating maintenance like first translation

A game update is not a request to retranslate everything. Compare sources, preserve existing accepted Korean, review only meaningful changes, then rebuild assets.

### Using one platform as evidence for another

If a Steam screenshot shows a raw UI key, inspect the Steam source and Steam inject. Xbox source parity does not prove Steam is fixed.

### Polishing tone by local string shape

Character tone drift often appears across gift, shop, relation, bubble, and mail keys. Review by speaker and player relationship, not by whether the key starts with `Dialog.Talk`.

If a project has extracted scripts, first generate a character review pack and use it as the work unit. Prefix-only grouping misses common live-game patterns such as aliasless tutorial scenes and alias+index keys (`Regis4`, `TianRuLv4`). Fix the grouping evidence before fixing the Korean.

### Natural Korean postponed until playtest

Playtest is too late for obvious stiffness. Run a naturalness pass on high-impact surfaces before packaging, especially romance/date dialogue, quest instructions, tutorials, and item flavor.

### Ending-only tone fixes

Changing `하세요` to `해` or `합니다` to `해` can still leave a machine-translated sentence intact. For dialogue, rewrite the whole line from the speaker's intent and relationship to the player. For tutorials and quest lines, make the action clear in Korean instead of preserving source phrasing.

### Flattening labels into descriptions

Short UI labels such as "Cannot Craft" should not inherit a full explanatory sentence if a nearby description key already carries the guidance. Conversely, if there is no separate guidance key, keep a compact action cue.

### Trusting fluent Korean without source alignment

A line can sound natural and still be wrong. Common failures include `Fang` becoming `방`, one shop name being replaced by another shop name, or styled item names staying in English. Always run source-anchored audits after fluency polishing.

### Using English as the only dialogue source

English subtitles may normalize honorifics, pronouns, distance, sarcasm, and sentence rhythm. If Japanese exists and is usable, use it as the primary dialogue source and treat English as term/alignment support. For names, items, places, UI, and system concepts, cross-check English and the approved glossary before accepting a Korean term.

### Treating a platform-specific fix as common

Live games often ship different text on Steam and Xbox. If a key's source value differs by platform, do not apply the same Korean blindly. Verify the current source on each platform, then branch the working set or inject asset.

### Shipping a developer-only installer

If a tester must know `.\Patch.exe --restore`, current-directory execution, or PowerShell quoting rules, the release package is not ready for general users. Add a visible install/restore flow and write a user-facing notice before publishing.

### Mistaking post-editing for localization

Lightly cleaning machine translation often leaves unnatural Korean, wrong emphasis, and unstable tone. For story, diary, quest, item flavor, and speaker-specific dialogue, rewrite the Korean line from the intended meaning and context. Keep machine output out of the accepted working set unless it survives the same manual localization review as any human draft.
