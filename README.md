```
 ██████  ██████   ██████  ██    ██ ███    ██ ██████  ██     ██  ██████  ██████  ██   ██
██       ██   ██ ██    ██ ██    ██ ████   ██ ██   ██ ██     ██ ██    ██ ██   ██ ██  ██
██   ███ ██████  ██    ██ ██    ██ ██ ██  ██ ██   ██ ██  █  ██ ██    ██ ██████  █████
██    ██ ██   ██ ██    ██ ██    ██ ██  ██ ██ ██   ██ ██ ███ ██ ██    ██ ██   ██ ██  ██
 ██████  ██   ██  ██████   ██████  ██   ████ ██████   ███ ███   ██████  ██   ██ ██   ██
```

# groundwork

> **work on your core values.**
>
> A universal skill pack that turns wide, coach-shaped questions into living artifacts — Values first, then Audience, Offer, Positioning. Distributed via `npx skills`. Runs in any agent the skills ecosystem supports: Claude Code, Hermes, Cursor, Codex, and more.

```
░▒▓█▓▒░
```

## status

```
phase        ░▒▓ design  ▓▒░  spec  ▓▒░  brand  ▓▒░  scaffold  ▓▒░  skills  ▓▒░  release  ▓▒░
                  ✓          ✓          ✓           ◐
```

- **spec** — `docs/specs/2026-04-16-groundwork-design.md`
- **brand kit (D1 "The Terminal")** — `docs/brand/brand.md` + `docs/brand/tokens.css` + live sample at `docs/brand/samples/index.html`
- **nano banana helper** — `scripts/nano-banana.py` (gemini-2.5-flash-image via the `llm` CLI keystore)
- **skills** — not yet implemented. Implementation plan pending.

```
░▒▓█▓▒░
```

## what it is

A set of agent skills that help a solo operator do values-work over time. The spine:

```
question  →  session (raw)  →  synthesize  →  artifact (distilled)
```

Frameworks from the coaching canon (Coaching Habit 7Q, 5 Prism, Ikigai, GROW, JTBD, BMC…) become the inquiry vocabulary. Artifacts (Values, Audience, Offer, Positioning, Principles) are markdown files that live in a hidden `.groundwork/` folder under a user-chosen location (Obsidian vault, repo, home folder).

**v1 ships one vertical slice: Values end-to-end** — intake, ingest (link/file/keyword), seed, session, synthesize, review, plus a brand kit and a `visual-card` skill that renders a shareable Values card. Audience, Offer, Positioning follow in v1.x.

See the full design spec for the why and the how.

```
░▒▓█▓▒░
```

## who it's for

- **you, solo** — founder, coach, creator, consultant: the operator who lives by values and wants them tight enough to steer with
- **community members** — delivered via [Hermes Agent](https://github.com/NousResearch/hermes-agent)'s multi-platform gateway (Telegram, Slack, Discord, WhatsApp, Signal), so non-technical users never need to install anything beyond a chat client
- **anyone** with a supported runtime — Claude Code, Claude Desktop, Cursor, Codex, 40+ others via `npx skills`

```
░▒▓█▓▒░
```

## install  ⟶  (coming soon)

```bash
npx skills add glebis/groundwork
# then, in your agent of choice:
▸ run groundwork-intake
```

The intake skill asks about your cadence, your data-folder location, your runtime, and offers a research-seeded onboarding that ingests material you've already written / said / recorded to warm your first artifact instead of starting blank.

```
░▒▓█▓▒░
```

## repo layout

```
groundwork/
├── skills/                         each subdir is an installable SKILL.md
├── template-vault/                 what gets copied to .groundwork/ on first run
├── docs/
│   ├── specs/                      design spec (start here)
│   ├── plans/                      implementation plans
│   ├── brand/                      D1 "The Terminal" — tokens, guide, samples, AI imagery
│   └── frameworks/                 canonical inquiry tools (markdown, not code)
└── scripts/
    └── nano-banana.py              image generation helper
```

```
░▒▓█▓▒░
```

## principles

```
◆  values first, everything else cascades
◆  questions are the atomic unit; artifacts are distilled
◆  frameworks are content, not code
◆  append-only sessions; distilled artifacts
◆  skills are near-pure functions — files in, files out, two modes
◆  three output tiers always: line (15w), brief (40w), full
◆  voice and bot-ready by contract, not by wrapper
◆  one source of truth; many runtimes
```

```
░▒▓█▓▒░
```

## license

MIT — see `LICENSE` (to be added).

```
                                                  ░▒▓ gleb · 2026-04 ▓▒░
```
