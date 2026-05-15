# Unity Adapter

Use this file when the game looks like Unity or Unity-derived packaging.

## Engine signals

Common evidence:
- `UnityPlayer.dll`
- `GameAssembly.dll`
- `*_Data/`
- `StreamingAssets/`
- `resources.assets`
- `globalgamemanagers`
- AssetBundle files

## Discovery order

1. check for direct table files inside `StreamingAssets`, `Localization`, `Addressables`, or data folders
2. check loose JSON/CSV/TSV before touching bundles
3. inspect bundles or assets only when structured text is not directly available

Prefer the cheapest stable path. Do not force bundle editing if a table-file path exists.

## Translation safety

- Treat extracted tables as the primary working dataset when possible.
- Keep bundle or asset replacement as a later packaging step.
- Check font coverage early if Korean glyph support is uncertain.
- Distinguish runtime replacement, direct asset patching, and table/localization-file patching. Runtime replacement is useful for discovery or diagnostics, but public releases should prefer the least fragile path that applies consistently across menus, save/load screens, and in-game UI.

## Patch guidance

- Produce inject-ready or replacement-ready artifacts in the working area first.
- Avoid overwriting original bundle files during normal iteration.
- If patching requires invasive tooling, record the risk in `engine_report` and keep the translation workflow independent of the final injection step.
- For Addressables or AssetBundle patching, account for catalog/hash/CRC validation. If the game hangs at loading after patched bundles are present, verify whether CRC/hash bypass, catalog update, or a non-bundle text path is required.
- Patch built-in `.assets` files separately from Addressables bundles when the same TextAssets are duplicated in both places; menus, save/load screens, and in-game screens may read from different copies.
- Verify applied text in multiple surfaces: main menu, load/save screen, tutorial, in-game interaction, inventory/journal/codex, and at least one scene-loaded text source.
- Test restore after patching Unity assets. A backup taken after a file was already patched is not an original backup.

## Public release checks

- Do not ship modified original `.bundle`, `.assets`, `.resS`, `.resource`, or executable files unless rights explicitly allow it.
- Ship patchable payloads, inject scripts, delta data, or installer logic that modifies the user's local copy.
- Include any required runtime plugin only if it is redistributable and documented.
- Keep developer probes and diagnostic text-replacement plugins out of the public payload unless they are intentionally part of the supported patch path.
