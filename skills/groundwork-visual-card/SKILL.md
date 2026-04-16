---
name: groundwork-visual-card
description: Render a named artifact as a share-ready card — SVG plus PNG — using the user's brand tokens. Print- and social-ready.
io_contract:
  reads:
    - "{data_folder}/profile.md"
    - "{data_folder}/artifacts/{artifact}.md"
    - "{data_folder}/visuals/brand/brand.md"
    - "{data_folder}/visuals/brand/tokens.css"
  writes:
    - "{data_folder}/visuals/output/{artifact}-{YYYYMMDD}.svg"
    - "{data_folder}/visuals/output/{artifact}-{YYYYMMDD}.png"
  returns: "paths to SVG and PNG"
modes: [interactive, headless]
tiers: [line, brief, full]
---

# groundwork-visual-card

Renders an artifact as a shareable card. D1 "The Terminal" card template: double-box ASCII frame, label + artifact body + dither footer, one accent highlight.

## When to use

- User wants to share their Values: `groundwork-visual-card values`.
- Cadence review wants a visual snapshot.

## What you do

1. **Read artifact + brand.** Parse the Values artifact (frontmatter + Candidate values list). Load brand tokens.

2. **Compose the card content.** Template:

```
╔══════════════════════════════════════════════════════════════╗
║  {ARTIFACT_TYPE_UPPER}                                       ║
║  ─────────                                                   ║
║                                                              ║
║  {BULLET}  {value_1_text}                                    ║
║  {BULLET}  {value_2_text}                                    ║
║  {BULLET}  {value_3_text}                                    ║
║  ...                                                         ║
║                                                              ║
║                       ░▒▓ {owner} · {YYYY-MM} ▓▒░            ║
╚══════════════════════════════════════════════════════════════╝
```

Pick exactly one value to highlight with the accent color (the one most recently added, or the one marked as `primary` if any).

3. **Render SVG.** Build an SVG document using brand tokens:
   - Background: `--bg` (`#0b0b0c`)
   - Foreground text: `--fg` (`#f5f4f0`)
   - Accent word: `--accent` (`#c17a53`)
   - Font: Geist Mono (embed as web-font link for SVG used in browser; rasterize with local font for PNG)
   - Preserve `font-variant-ligatures: none` so box-drawing glyphs render as glyphs.

4. **Render PNG.** From SVG, rasterize at 1600×1200 (share-ready dimensions). Use `cairosvg` if available; fall back to documenting a manual `rsvg-convert` command if not.

5. **Write both files.** `visuals/output/values-{YYYYMMDD}.svg` and `.png`.

6. **Surface the results.** Return the paths. If runtime allows, open the PNG preview.

## Tiers

- **line**: `"card → {png_path}"`
- **brief**: paths + dimensions
- **full**: paths + a renders ASCII-only preview (what the SVG card contains, minus styling) for terminal surfaces

## Headless mode

Non-interactive — just produce the card. Used by cadence reviews and scheduled exports.

## Failure modes

- Artifact has no values (status seeded, no candidates) → stop; suggest running a session first.
- `cairosvg` not installed → write only the SVG; print a note with the install command.
- Font not available locally for rasterization → use the closest web-safe fallback; warn.
