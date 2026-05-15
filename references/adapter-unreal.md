# Unreal Adapter

Use this file when the game looks like Unreal Engine packaging.

## Engine signals

Common evidence:
- `Engine/`
- `Content/`
- `.pak`
- `.ucas` and `.utoc`
- `Localization/`
- `.locres`
- `.uasset`

## Discovery order

1. look for `Localization/` or `.locres` first
2. look for `DataTable`-style structured assets or exported text tables
3. treat raw asset repacking as a higher-risk path

## Translation safety

- Prefer extracted working text sets over direct archive editing.
- Record whether text can be round-tripped safely before promising a playtest patch.
- If strings remain embedded in opaque assets, mark the workflow as blocked or invasive instead of pretending it is a simple table-file project.

## v1 packaging rule

For v1 of this skill:
- working translation sets are required
- test packaging is optional and risk-gated
- manual or semi-manual injection guidance is acceptable when direct automation is unsafe

Check font and fallback behavior early, especially when the project uses custom UI fonts.
