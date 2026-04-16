---
name: Groundwork brand kit
version: 0.1
direction: D1 "The Terminal"
status: draft
updated: 2026-04-16
---

# Groundwork — brand · D1 "The Terminal"

```
 ██████  ██████   ██████  ██    ██ ███    ██ ██████  ██     ██  ██████  ██████  ██   ██
██       ██   ██ ██    ██ ██    ██ ████   ██ ██   ██ ██     ██ ██    ██ ██   ██ ██  ██
██   ███ ██████  ██    ██ ██    ██ ██ ██  ██ ██   ██ ██  █  ██ ██    ██ ██████  █████
██    ██ ██   ██ ██    ██ ██    ██ ██  ██ ██ ██   ██ ██ ███ ██ ██    ██ ██   ██ ██  ██
 ██████  ██   ██  ██████   ██████  ██   ████ ██████   ███ ███   ██████  ██   ██ ██   ██
```

## The feel

A terminal at 2am that cares about typography. Monochrome, deliberate, functional, a little weird. ASCII is decoration and structure both. Nothing shouts. The page knows it's made of characters.

Base reads like the Claude Code Lab — dark, Geist, extreme type scale, negative tracking. Weirder than the Lab because:

- ASCII block glyphs (`░ ▒ ▓ █`) texture long surfaces
- Box drawing (`╔═╗ ║ ╚═╝`, `┌─┐ │ └─┘`) frames artifacts
- Dither bands (`░▒▓█▓▒░`) replace hr/section breaks
- Occasional figlet banners for display headers
- Every artifact has a prompt-like prefix (`▸ values  ·  gleb  ·  2026-04-16`)
- A single warm accent (ember) shows up once per surface, never more

## The principles

1. **Mono is structure, sans is reading.** Geist Mono for ASCII, labels, artifact frames, file paths, anything that should not reflow. Geist Sans for display headlines and body prose.
2. **One accent per surface.** Ember (`#c17a53`) appears once per view: a cursor, a single highlighted word, a glyph. Never two.
3. **Negative tracking on display.** Big type is tight (`-0.025em`). Body is 0. Mono is `+0.01em`.
4. **Ligatures off in mono.** ASCII glyphs must render as themselves; no `->` → `→` auto-conversion anywhere.
5. **Nothing animates except the cursor.** A blink is the only moving pixel. Hovers are one-property, 120ms.
6. **Rough over sleek.** When nano banana generates imagery, prefer photocopied, scanlined, halftoned — not polished.

## Type

- **Geist Sans** — 300/400/500/600 from Google Fonts
- **Geist Mono** — 400/500/600 from Google Fonts
- Display: Geist Sans, 400, `-0.025em`, `lh 0.92`
- Section: Geist Sans, 400, `-0.02em`, `lh 0.96`
- Body: Geist Sans, 300, 0 tracking, `lh 1.6`
- Mono (ASCII, code, labels): Geist Mono, 400, `+0.01em`, `lh 1.5`, ligatures **off**
- Label (all-caps): Geist Mono, 500, `+0.14em`

## Color

```
bg              #0b0b0c    near-black, faint blue shift
bg-elevated     #111112    card surface
bg-sunken       #060607    wells, code blocks
fg              #f5f4f0    off-white, faint warm shift
fg-muted        #98938a    labels, captions
fg-dim          #555148    borders-as-type, low-priority glyphs
border          #1e1d1a    hairline
border-strong   #2a2925    card edge
accent          #c17a53    ember — single warm accent, used once
accent-dim      #5a3a28    accent backgrounds, pressed states
```

**Why not pure black/white:** pure `#000`/`#fff` burn on OLED and feel clinical. The off-warm shift gives the monochrome a faint paper quality without becoming sepia.

## ASCII palette

Curated — the only glyphs used anywhere in brand surfaces:

```
dither       ░ ▒ ▓ █
box single   ─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼
box double   ═ ║ ╔ ╗ ╚ ╝ ╠ ╣ ╦ ╩ ╬
bullets      ◆ ◇ ◈ ▸ ▹ · •
marks        ⎯ ⟶ ⟵ ↯ ※
```

New glyphs need a reason. Cute is not a reason.

## Surfaces

### Artifact card

Double-box frame, title in mono label style, body in sans body, footer in mono-small with a dither ornament.

```
╔══════════════════════════════════════════════════════════╗
║  VALUES                                                  ║
║  ─────────                                               ║
║                                                          ║
║  ◆  truth over comfort                                   ║
║  ◆  make, don't perform                                  ║
║  ◆  kin over scale                                       ║
║  ◆  the work is the output                               ║
║  ◆  slow is a signal                                     ║
║                                                          ║
║                       ░▒▓ gleb · 2026-04 ▓▒░             ║
╚══════════════════════════════════════════════════════════╝
```

### Section break

Dither band replaces hr:

```
░▒▓█▓▒░
```

### Prompt / log

Single-box frame, prompt prefix, blinking cursor at end:

```
┌───────────────────────────────────────────────────────────┐
│ ▸ groundwork session  ·  values  ·  2026-04-16 14:02      │
│                                                           │
│ q. what did you avoid this week?                          │
│ a. ▌                                                      │
└───────────────────────────────────────────────────────────┘
```

### Display hero

Big Geist Sans, tight, off-white on near-black, a single dither strip on the side:

```
┌──┐
│░░│   groundwork
│▒▒│   work on your
│▓▓│   core values.
│██│
└──┘
```

## Nano banana (image generation) direction

When Gemini 2.5 Flash Image ("nano banana") is wired up, use these prompt patterns:

- **Hero textures:** "rough black and white photocopied texture, high contrast, scanline artifacts, slightly crushed blacks, monochrome, no color, [mood word from artifact]"
- **Editorial illustrations:** "pen and ink sketch, loose hatching, monochrome, slightly smudged, published-zine quality, single subject: [concept]"
- **Glyph studies:** "typographic experiment, bold mono-spaced character, torn edge, risograph overprint, single ink (warm ember if color requested), otherwise black on warm off-white"

Generated images sit in `visuals/output/ai/`. Every AI-generated asset carries a `source_prompt.txt` sibling file for reproducibility.

## What this brand explicitly isn't

- Not a startup landing page. No hero gradients, no floating CTAs, no glow.
- Not a corporate style guide. No logo grid, no spacing deck, no Poppins anywhere.
- Not cute. No emoji. No rounded corners that soften the box-drawing.
- Not skeuomorphic — the "terminal" is a typographic metaphor, not a pretense.

## Open

- Secondary serif for long-form reading (Values manifesto, community letters)?  Candidate: **Instrument Serif** (Google Fonts, distinctive italic — breaks the mono monotony without becoming warm).
- When to allow a second accent? Probably never. Revisit after 10 artifacts exist.
- Print form: the dither and box-drawing survive photocopy beautifully. Values cards should have a pressable PDF/Letter format.
