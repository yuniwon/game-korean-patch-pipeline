# AGENTS.md — Game Korean Patch Pipeline

This file activates the game-korean-patch-pipeline skill for this project.
Copy this file into the root of any game localization project folder and fill in the sections below.

---

## Project

- **Game name**: [FILL IN]
- **Engine**: [Unity / Unreal / Table-files / Retro-ROM / Unknown]
- **Platforms**: [Steam / Xbox / PS / Switch / ROM — list all]
- **Patch repo**: [GitHub URL or local path]
- **Working directory**: [path to this project folder]
- **Skill reference**: https://github.com/yuniwon/game-korean-patch-pipeline

---

## Active documents

Load these before any translation or QA work:

- `glossary.tsv` — canonical Korean term mappings
- `style_bible.md` — tone cards, forbidden terms, naming policy
- `lore_packet.md` — setting, factions, characters, open questions
- `localization_quality_standard.md` — what "good Korean" means for this game
- `source_language_matrix.md` or `.tsv` — controlling source language per surface
- `quality_scorecard.md` or `.tsv` — five 95-point acceptance gates

If any of these do not exist yet, create them before starting bulk translation.

---

## Workflow rules (summary)

Follow the full pipeline from `SKILL.md`:

1. `engine_report` — detect engine and patching risk
2. `localization_asset_inventory` — find all text assets
3. `extraction_manifest` — commands, hashes, row counts, failed assets, runtime-only surfaces
4. `source_language_matrix` — controlling source language and fallback reasons per surface
5. `lore_packet` + `localization_quality_standard` + `style_bible` — research and knowledge base
6. `translation_plan` + `agent_batch_contracts` — categorize and batch safely
7. `quality_scorecard` — five criteria, each at least `95` before moving forward
8. `translated_working_set` — translate into working files, never original assets
9. `qa_report` — structural, consistency, naturalness gates
10. `playtest_pack` — tester-ready build
11. `release_decision` + `release_package` + `release_notice`

**Do not start bulk translation before steps 1–7 are complete and the pre-translation scorecard gates are at least `95`.**

---

## Translation quality rules

- Do not treat AI draft output as final. Rewrite from intended meaning.
- Preserve all placeholders, tags, keys, and schema exactly.
- Consult `glossary.tsv` before naming any proper noun.
- Consult `style_bible.md` before deciding any character's speech level.
- Use Japanese as the primary source for dialogue/cutscene tone only when it is present, aligned, and higher quality than the original or other source languages.
- Use the original language or best available source when Japanese is missing, weak, over-compressed, machine-like, or lower quality than the original.
- Use approved Korean glossary/current Korean plus original or English evidence for UI, item names, locations, controls, and system terms.
- Run a naturalness pass on story, dialogue, quests, and item flavor before packaging.

---

## Multi-agent work

When running parallel subagent sessions:

- The orchestrator holds `glossary.tsv`, `style_bible.md`, and `lore_packet.md`.
- Each subagent receives: its assigned scope, relevant glossary excerpt, tone card(s), and source slice.
- Subagents return proposals: `key / source / old_target / new_target / reason / confidence`.
- The orchestrator merges and runs QA before committing to the master working set.
- Do not parallelize before the shared knowledge base is stable.
- Every subagent must receive an `agent_batch_contract` with controlling source language, allowed actions, output schema, and QA-before-apply rules.

---

## Platform notes

<!-- Fill in per-platform divergence notes as you discover them -->

| Platform | Source path | Known divergences |
|----------|-------------|-------------------|
| Steam    |             |                   |
| Xbox     |             |                   |

---

## Known issues / regression watchlist

<!-- Add bad patterns here as they are found. Run this list after every sync. -->

| Old Korean | Expected Korean | Source term / key family | Platform scope |
|------------|-----------------|--------------------------|----------------|
|            |                 |                          |                |

---

## Red flags — stop and fix if any appear

- Translation started before `engine_report`, `lore_packet`, or `localization_quality_standard`
- Translation started before `source_language_matrix`, `agent_batch_contracts`, or `quality_scorecard`
- Original game assets modified directly (not via working set)
- Parallel subagents running without a stable shared glossary
- Character tone pass started without a character review pack
- Character speaker decisions made only from key prefixes when better evidence exists
- QA passed but source-target semantic drift was never checked
- Release tested only on an already-patched install
- Public package requires command-line knowledge for basic install or restore
