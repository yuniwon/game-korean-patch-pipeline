# QA Gates

Use this file after translation and before any playtest packaging.

## Fail-closed gates

Do not continue if any of these break:
- placeholder count or order mismatch
- rich-text or markup tag corruption
- schema/key drift
- malformed JSON/CSV/TSV output
- encoding damage

These are structural failures, not style issues.

## Consistency gates

Check for:
- same confirmed proper noun rendered multiple ways
- repeated system strings drifting across files
- glossary violations without evidence-based exceptions
- benchmark reuse applied where context changed meaning

## Risk gates

Flag, and usually retranslate, rows that are:
- very short but high-impact
- unusually long for the target UI surface
- dialogue lines with unclear referents
- mixed-language outputs that read unnaturally
- strings that remain identical to the source without a good reason

## Naturalness gates

Run a Korean gamer persona pass before release when the game has story, diaries, dialogue, or flavor text:
- read lines by category or speaker, not only by file order
- flag machine-translation tone, stiff literal phrasing, unnatural connective endings, and inconsistent register
- check whether lore terms still make sense after reading the in-game context
- keep exact placeholders and tags unchanged while polishing prose

This pass is separate from structural QA. A structurally valid translation can still be unfit for public release if it reads like raw machine output.

Reject or rewrite rows that show common machine-translation residue:
- English sentence order copied into Korean
- unnatural abstract nouns where Korean would use a verb phrase
- repeated "것/수/때문/상태" phrasing without need
- over-formal connective endings in diaries or spoken lines
- inconsistent honorific level for the same speaker
- literal fantasy terms that do not match the established glossary
- translated line explains the sentence but does not sound like in-game text

Passing naturalness QA requires a reviewed Korean line, not simply a post-edited machine line.

## Packaging gates

Before building `playtest_pack`, confirm:
- the translated working set passed structural gates
- the remaining issues are low enough for a tester to evaluate meaningfully
- the build or inject-ready artifact is reversible

Before publishing a public release, confirm:
- the installer was tested on a clean original baseline or freshly verified install
- install creates a usable backup of original files, not a backup of already-patched files
- restore works through the public UI/menu, not only through CLI flags
- the package can be used by double-click users without PowerShell knowledge
- the release ZIP contains no original executables, full game data directories, bundles, assets, `.resS`, `.resource`, or equivalent copyrighted game files
- the final ZIP digest, file count, and release version are recorded
- the GitHub release uses a new tag when launcher/update detection depends on tags

## Tester feedback intake

The playtest report should capture:
- screen or context
- source text or key
- observed Korean output
- issue type: mistranslation, awkwardness, truncation, tone, functional breakage
- severity
- suggested fix, if any

Accepted tester findings must flow back into glossary or translation fixes, not stay as loose notes.
