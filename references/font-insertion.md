# Font Insertion

Use this file when the game does not natively support Korean glyphs.

## When Font Work Is Needed

- Korean renders as boxes, question marks, blanks, or broken glyphs.
- The source game ships only Latin, CJK without Hangul, or narrow bitmap fonts.
- The game uses a custom tile-based font engine, common in retro ROMs.

## General Checklist

1. Identify font storage: ROM tile set, font atlas texture, TTF/OTF, TextMeshPro asset, Unreal font face, or composite font.
2. Extract the existing font with the engine-appropriate tool.
3. Design or source a Korean glyph set that matches tile size, atlas density, visual weight, and UI constraints.
4. Check glyph bounds: height, descent, width, baseline, and clipping at the bottom or right.
5. Insert the font and update encoding tables, atlas metadata, or fallback chains.
6. Test main menu, dialogue boxes, item descriptions, status screens, save/load, tutorials, and subtitles.
7. Patch line spacing, text box size, wrapping, or encoding logic if glyphs overflow.

## Retro ROM Notes

See `references/adapter-retro-rom.md` for ROM-specific steps: tile extraction, encoding table mapping, pointer updates, and common clipping fixes.

## Unity Notes

- Replace or supplement the font asset in the relevant bundle.
- For TextMeshPro, generate a TMP font asset with Hangul coverage.
- For legacy UI Text, replace the font asset reference in `.assets` or bundle files.
- Verify fallback font chains when the main font does not cover every glyph.

## Unreal Notes

- Replace the font face asset with a Korean-capable font.
- Verify composite font fallback covers Hangul syllables.
- Test at least HUD and menu widgets because they may reference different font assets.
