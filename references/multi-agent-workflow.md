# Multi-Agent Workflow

Use this file when the translation workload is large enough that sequential processing would be impractical.

## When to Parallelize

- Character dialogue polish: one subagent per character or character group.
- Category batching: one subagent per category when UI, items, quests, and dialogue are independent.
- Platform divergence: run Steam and Xbox working-set updates concurrently after a common diff pass.
- Lore pass: let subagents read different source families in parallel and report candidates to the orchestrator.

Do not parallelize before `lore_packet`, `style_bible`, `glossary`, `source_language_matrix`, and `agent_batch_contracts` are stable.

## Orchestrator Responsibilities

- Hold and update the canonical `glossary`, `style_bible`, and `lore_packet`.
- Assign a bounded scope: exact character names, category slice, platform, or source family.
- Provide each subagent with relevant glossary excerpts, tone cards, source slices, controlling source language, and output schema.
- Require proposal rows before accepting changes: `key`, `source`, `old_target`, `new_target`, `reason`, `confidence`, `surface`, `speaker`.
- Merge accepted proposals into the master working set.
- Run QA gates on the merged output, not on individual subagent outputs.

## Character Tone Prompt Template

```text
You are polishing Korean dialogue for [CHARACTER NAME].
Tone card: [speech level, relationship to player, verbal habits, exceptions]
Glossary: [relevant excerpt]
Style bible rules: [relevant rules]
Controlling source language: [ja/original/en/etc.]
Source: [working set slice: key, source, current_target columns]
Output: for each changed line, return key / source / old_target / new_target / reason / confidence / surface / speaker
Do not change keys, placeholders, tags, or schema.
Do not invent new proper nouns not in the glossary.
Goal: Korean a local player would accept in this game context, not lightly post-edited machine translation.
```

## Character Review Pack Workflow

1. Build the alias registry (`dialog_character_alias_registry.tsv`) to map key patterns to canonical character names.
2. Build scene overrides (`dialog_speaker_scene_overrides.tsv`) for aliasless or mixed scenes.
3. Generate per-character review packs that gather `talk/chat/gift/shop/mail/date/bubble/mission/online` keys together.
4. Assign one subagent per character pack, not per file prefix.
5. After subagents return proposals, update registry or override rules if unresolved patterns were found.

## Parallel Session Management

- Give each session a distinct scope, glossary slice, tone card, and batch contract.
- Use separate output files or branches to avoid file conflicts.
- Collect outputs to a merge staging area before touching the master working set.
- The orchestrator reviews merged proposals before any QA gate run.
