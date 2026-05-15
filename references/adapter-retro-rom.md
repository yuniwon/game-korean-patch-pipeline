# Retro / ROM Adapter

Use this file when the target is a cartridge-era ROM (SNES, GBA, PS1, NDS, etc.) or a binary executable where text is embedded in the binary rather than in a structured data file.

## Engine signals

Common evidence:
- `.sfc`, `.smc`, `.gba`, `.nds`, `.iso`, `.bin`, `.cue` ROM files
- No folder-based text assets
- Text extracted only via emulator tools or ROM editors
- Existing fan-translation projects using tools like Atlas, Cartographer, Relative, or table-file editors

## Discovery order

1. Identify the ROM format and platform (SNES, GBA, NDS, PS1, etc.)
2. Search for existing fan-translation or localization tools for this specific ROM
3. Extract text using a dedicated tool (Cartographer, Atlas, Crystal Tile 2, etc.) or script
4. Identify text encoding: standard ASCII, Shift-JIS, custom encoding table, or pointer-based
5. Map text pointers and table files before editing anything

## Text encoding

Retro ROMs frequently use custom encoding tables. Before translating:

- Locate or build a `.tbl` file that maps hex values to characters
- Identify the character set: does it include Korean glyphs, or must you add a custom font?
- Confirm whether the encoding supports the full Hangul block or only a subset
- For games with Japanese source text, check whether the encoding is Shift-JIS or custom

## Font insertion

Korean localization of retro ROMs almost always requires a custom font:

### Steps

1. **Identify the font storage location** — fonts may be in the ROM as a tile set (1bpp, 2bpp, or 4bpp) or as a bitmap strip
2. **Extract the existing font** using a tile editor (Crystal Tile 2, YY-CHR, Tile Molester)
3. **Design or source a Korean glyph set** that fits the tile size constraints (8×8, 8×16, 12×12, 16×16 pixels are common)
4. **Check rendering bounds** — Korean syllables often need more horizontal space than Latin characters; verify glyph height and descent so the bottom is not clipped
5. **Insert the font** back into the ROM at the correct offset
6. **Update the encoding table** to map new hex values to Korean syllable blocks
7. **Test in-game** across multiple text boxes, dialogue windows, UI labels, and status screens

### Common font problems

- **Bottom clipping**: glyph height exceeds the tile row spacing — reduce glyph height or increase line spacing via ASM patch
- **Width overflow**: Korean syllables wider than Latin characters cause wrapping or truncation — reduce font width or patch the text-rendering routine
- **Missing glyphs**: not all syllable combinations are present — expand the tile set or use a variable-width rendering approach
- **Encoding collision**: new Korean hex codes conflict with control characters — remap control codes before assigning Korean slots

## Text insertion workflow

1. Extract source text to a working file (`.txt`, `.csv`, or tool-specific format)
2. Translate into a working copy — do not edit the ROM directly at this stage
3. Reinsert translated text using Atlas, Cartographer, or a custom inserter script
4. Handle text expansion: Korean text is often longer than Japanese or English — implement line breaks, text speed adjustments, or dialog box resizing as needed
5. Test dialog boxes, menus, item descriptions, and cutscene text in-game

## Pointer tables

Most retro ROMs use pointer tables to locate text:

- Extract and document the pointer table before editing text
- After reinsertion, update all affected pointers
- For variable-length text, use a relative pointer or free-space bank system
- Confirm that pointer updates do not corrupt adjacent data

## QA for ROM patches

In addition to standard QA gates:

- Test every dialog box for clipping, overflow, and encoding errors
- Test menu screens at minimum and maximum text lengths
- Test save/load screens
- Test on multiple emulators (Snes9x, RetroArch, Mesen) and hardware if available
- Verify the patch applies cleanly to an unmodified original ROM
- Verify restore: applying the patch to an already-patched ROM should fail gracefully or be documented

## Distribution

- Distribute as an IPS, BPS, or xdelta patch file — never include the original ROM
- Include a README with: supported ROM version (checksum), patching tool name and version, emulator recommendations, and known issues
- Verify the patch file applies to the correct ROM checksum before publishing

## Tools reference

| Tool | Use |
|------|-----|
| Cartographer | Text extraction from ROM |
| Atlas | Text insertion into ROM |
| Crystal Tile 2 | Tile/font editing |
| YY-CHR | Font tile editing |
| Tile Molester | Font and graphics editing |
| Floating IPS (Flips) | IPS/BPS patch creation and application |
| xdelta | Delta patch creation |
| Snes9x, Mesen | SNES emulation and testing |
| mGBA, VisualBoyAdvance | GBA emulation and testing |
| DeSmuME, melonDS | NDS emulation and testing |
