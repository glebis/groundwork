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
                  ✓          ✓          ✓          ✓            ✓          ◐
```

- **spec** — `docs/specs/2026-04-16-groundwork-design.md`
- **brand kit (D1 "The Terminal")** — `docs/brand/brand.md` + `docs/brand/tokens.css` + live sample at `docs/brand/samples/index.html`
- **nano banana helper** — `scripts/nano-banana.py` (gemini-2.5-flash-image via the `llm` CLI keystore)
- **skills (v1 values slice)** — 11 skills shipped: `intake`, `ingest`, `seed`, `session`, `synthesize`, `review`, `rhythm`, `framework`, `brand`, `visual-card`, `ask` — plus a `/groundwork` dispatcher.
- **frameworks** — 5 seed frameworks (Coaching Habit 7Q, 5 Prism, GROW, Ikigai, **ACT Values Clarification**) + optional `examples/personal-modes.md.example` template.
- **release** — unpublished on `npx skills` registry; install via git clone + symlink (see below).

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

The values session uses **Acceptance and Commitment Therapy (ACT)** clarification by default — values as chosen directions (not achievable goals), surfaced via peak moments, life domains, and behavior rather than declaration. Other frameworks (Coaching Habit 7Q, 5 Prism, GROW, Ikigai) layer in for deepening and grounding.

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

## install

### npx skills (coming soon)

```bash
npx skills add glebis/groundwork
```

### manual install (today)

Clone the repo and symlink the skills into your agent's skill directory.

```bash
git clone https://github.com/glebis/groundwork ~/ai_projects/groundwork

# Claude Code
mkdir -p ~/.claude/skills
for d in ~/ai_projects/groundwork/skills/groundwork-*; do
  ln -s "$d" ~/.claude/skills/"$(basename "$d")"
done
ln -s ~/ai_projects/groundwork/commands/groundwork.md ~/.claude/commands/groundwork.md

# Hermes (optional)
mkdir -p ~/.hermes/skills/coaching
printf -- "---\ndescription: Coaching and self-direction skills.\n---\n" \
  > ~/.hermes/skills/coaching/DESCRIPTION.md
for d in ~/ai_projects/groundwork/skills/groundwork-*; do
  ln -s "$d" ~/.hermes/skills/coaching/"$(basename "$d")"
done
```

Then, in your agent:

```
▸ run groundwork-intake
```

The intake skill asks about your cadence, your data-folder location (default `~/.groundwork`; an Obsidian vault subfolder or `$XDG_DATA_HOME/groundwork` also work), your runtime, and offers a research-seeded onboarding that ingests material you've already written / said / recorded to warm your first artifact instead of starting blank.

### first session

```
▸ /groundwork session values
```

Opens an ACT values-clarification dialog. Goal: by the end, 2-4 candidate values each paired with a concrete episode, at least one tension between declared and lived values, and one direction-not-goal to move toward this week.

```
░▒▓█▓▒░
```

## repo layout

```
groundwork/
├── skills/                         each subdir is an installable SKILL.md
├── commands/
│   └── groundwork.md               /groundwork slash-command dispatcher
├── template-vault/                 what gets copied to .groundwork/ on first run
│   └── .groundwork/
│       ├── profile.md              placeholder (owner, data_folder, rhythm)
│       ├── artifacts/values.md     seed artifact
│       ├── frameworks/             5 seed frameworks + examples/
│       ├── intake/                 sources/, inbox/, research-findings.md
│       ├── sessions/               (empty; append-only session logs land here)
│       └── visuals/brand/          user-editable brand tokens
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

MIT — see `LICENSE`.

```
                                                  ░▒▓ gleb · 2026-04 ▓▒░
```
