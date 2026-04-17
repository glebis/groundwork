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

## voice mode

Groundwork is built voice-ready by contract, not by wrapper. Every skill returns output in three tiers:

```
◆  line   (~15 words)   → for status bars, voice pings, bot notifications
◆  brief  (~40 words)   → for voice summaries, bot replies, daily-note inserts
◆  full   (markdown)    → for terminal / document rendering
```

Each artifact carries a **`speakable_summary`** in its frontmatter — regenerated on every `synthesize`, ~40 words, voice-friendly. A voice agent can read the artifact out loud without touching the body.

**Configuration.** Your `.groundwork/profile.md` has a `voice_preferences` block:

```yaml
voice_preferences:
  language_autodetect: true    # Whisper auto-detects; never hard-code a language
  tier_default: full           # which tier a skill returns when not otherwise specified
```

**Stacks.** Any voice stack that can receive tier-1/tier-2 text and optionally send transcribed user replies back:

- **Hermes Agent** — built-in voice-memo transcription + TTS delivery across Telegram / Discord / Slack / WhatsApp / Signal. No groundwork config needed beyond `runtime: hermes`
- **Pipecat** — custom voice pipeline (Deepgram → LLM → ElevenLabs/TTS). Wrap `/groundwork ask` or `/groundwork session` calls; route tiered text to TTS
- **Custom** — anything that can call a skill and speak text. The three-tier contract is the whole interface

Skills never assume voice is happening — tier selection is the only hook. Language is never hard-coded; let Whisper auto-detect. This is what makes the same skill pack work equally well in a terminal, an Obsidian plugin, a Telegram chat, and a phone call.

```
░▒▓█▓▒░
```

## cadence

Groundwork supports scheduled rhythms, not just on-demand sessions. Your `rhythm` block in profile.md:

```yaml
rhythm:
  daily_anchor_time: "09:00"        # daily check-in time (null to disable)
  weekly_review_day: fri            # weekday for weekly review (null to disable)
  monthly_drift_day: 15             # day-of-month for drift check
  quarterly_direction: true         # first day of each quarter
```

- **Daily anchor** — a single focus question each morning via `groundwork-ask`
- **Weekly review** — `groundwork-review weekly` surfaces what moved vs. stalled
- **Monthly drift** — compare declared values against actual behavior for the month
- **Quarterly direction** — re-run `synthesize` across all artifacts to resurface direction

The `/groundwork` dispatcher detects what's due and suggests it. Cadence is optional — set any field to `null` to skip.

```
░▒▓█▓▒░
```

## data & privacy

Everything is markdown in a folder you choose. No external services, no telemetry, no cloud sync unless you set it up.

- `.groundwork/` lives wherever you point `data_folder` — your Obsidian vault, `~/.groundwork`, `$XDG_DATA_HOME/groundwork`, or any directory you own
- **Sessions are append-only** — the skills never overwrite a session log, only add new ones. Synthesize distills session content into artifacts; session logs stay as raw record
- **Artifacts are editable** — edit `artifacts/values.md` directly by hand any time; synthesize merges carefully, never overwrites blindly
- **Frameworks are yours** — the seed set is a starting point; copy, adapt, rename, delete
- **Version-control what you like** — running `git init` inside `.groundwork/` (or nesting it inside an existing repo) gives you memory history for free

The only network traffic is whatever your agent runtime already makes (LLM calls, Hermes gateway). Groundwork itself is pure file I/O.

```
░▒▓█▓▒░
```

## runtimes

```
runtime            install path                              notes
─────────────────  ────────────────────────────────────────  ──────────────────────────────
claude-code        ~/.claude/skills/groundwork-*             native AskUserQuestion for options
claude-desktop     ~/.claude/skills/groundwork-*             numbered-list fallback for options
hermes             ~/.hermes/skills/coaching/groundwork-*    multi-platform gateway + voice
cursor             per-project .cursor/skills/groundwork-*   headless mode via MCP
codex              ~/.codex/skills/groundwork-*              headless mode
other              any dir the agent scans                   plain-text I/O; degrades gracefully
```

The `session` skill's Runtime Adaptation section reads the `runtime:` field in profile.md and swaps tool calls accordingly. The same skill file runs under any agent that can read, write, and exchange messages.

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
