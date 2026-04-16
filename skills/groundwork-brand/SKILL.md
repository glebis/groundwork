---
name: groundwork-brand
description: Interactive brand-direction picker/evolver. Writes brand.md tokens the visual skills use. D1 "The Terminal" is the starter direction; users can evolve palette, typography, and accent.
io_contract:
  reads:
    - "{data_folder}/visuals/brand/brand.md"
  writes:
    - "{data_folder}/visuals/brand/brand.md"
    - "{data_folder}/visuals/brand/tokens.css"
  returns: "summary of brand changes"
modes: [interactive]
tiers: [line, brief, full]
---

# groundwork-brand

Picks or evolves the user's brand tokens. D1 "The Terminal" is shipped as the default starter direction.

## When to use

- First run (via `groundwork-intake` → brand prompt).
- User wants to tweak colors, accent, or typography: `groundwork-brand`.

## What you do

1. **Read current brand.md.** If it's the default D1 version, offer the starter palette picker (Scriptorium / Studio / Fern / Ember / Ice). If the user has already customized, offer to evolve, not replace.

2. **Picker flow.**
   - Show each palette as a swatch row (mono chars in Geist Mono) with a one-line aesthetic note.
   - User picks one. Update `brand.md` palette section and `tokens.css` CSS variables.

3. **Evolver flow.**
   - Ask which aspect to change: color / typography / accent / personality words.
   - For color: ask for a single hex or a named accent. Validate contrast against the background.
   - For typography: constrain to Google Fonts families (to avoid missing-font rendering). Offer the approved list: Geist, Geist Mono, Instrument Serif, Space Mono, JetBrains Mono, Fraunces, Inter, Inconsolata.
   - For accent: enforce the "one accent per surface" rule by warning if the user tries to define multiple.
   - For personality words: free-text; stored as brand.md's "feel" paragraph.

4. **Always write both files.** `brand.md` (human-readable) and `tokens.css` (machine-readable) must stay in sync. Regenerate `tokens.css` from `brand.md`.

5. **Never silently replace.** Any change is confirmed before write.

## Tiers

- **line**: `"brand updated: {changed}"`
- **brief**: palette + accent + font stack after change
- **full**: the above + a regenerated sample card preview (ASCII, not HTML — for terminal surfaces)

## Failure modes

- User picks a palette not in the starter set → accept it as custom; mark `direction: custom` in brand.md.
- Font not on the approved list → warn; require explicit confirmation before writing.
- Accent contrast ratio against background < 4.5:1 → warn but allow.
