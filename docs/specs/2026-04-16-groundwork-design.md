---
title: Groundwork — Design Spec v1
date: 2026-04-16
status: Draft, pending review
author: Gleb Kalinin
---

# Groundwork — Design Spec v1

## One-liner

**A universal skill pack that helps you work on your core values** — and, from that ground, on the audience, offer, and positioning that cascade from it.

Groundwork is a set of agent skills authored to the `SKILL.md` standard and distributed via `npx skills`. It turns wide, coach-shaped questions into living, per-user artifacts — Values first, then Audience, Offer, Positioning — through a rhythm of deep sessions, scheduled touches, and accumulated reflection.

## Why this exists

Solo operators, coaches, and community builders rarely have trouble generating *work*; they have trouble keeping that work tethered to *who they actually are and who they actually serve*. Existing tooling starts with metrics and funnels. Groundwork starts with values and widens outward. The point is not a values statement pinned to a wall — it's a coaching rhythm that keeps values live, interrogable, and ingredient to every downstream business decision.

Groundwork is also the foundation of an English language community that Gleb Kalinin is building. It must therefore work for three audiences:

- **A** — Gleb and his Claude Code Lab cohort (dogfood, immediate use)
- **B** — technical solopreneurs comfortable with CLI and agents
- **C** — non-technical solopreneurs, coaches, creators, community members reached via multi-platform chat

All three from v1, because the distribution layer (`npx skills`) and the runtime layer (Hermes's multi-platform gateway) remove the historical friction wall for audience C.

## Positioning

Not a productivity app. Not a BMC generator. Not a journaling tool. Groundwork is:

- **Values-first** — every other artifact is downstream of a living values document
- **Question-led → artifact-producing** — wide coach questions accumulate into refined documents over time
- **Framework-aware** — coaching and business frameworks are ingredients; users can bring their own
- **Universal by distribution** — one repo, every supported agent, no lock-in
- **Quiet, English, deliberate** — the product reads like a small independent press, not a SaaS

## Core object model

The whole system is six nouns:

1. **Profile** — who the user is; preferred cadence; chosen mode (deep / scheduled / ambient); data-folder location; voice/bot preferences
2. **Artifacts** — living documents, one per domain: *Values, Self-Map, Audience, Offer, Positioning, Principles, Drift Log*
3. **Frameworks** — named inquiry tools (GROW, 5 Prism, Coaching Habit 7Q, Ikigai, JTBD, BMC, Value Proposition Canvas, Wardley, and the user's own lexicon of modes). Each is a plain markdown file with frontmatter describing purpose, trigger, and question set
4. **Questions** — the atomic coaching unit; each question knows its framework, its target artifact, and when it is timely
5. **Sessions** — append-only logs of every interaction (deep dialogue transcripts, scheduled answers, ingested material). Artifacts are *distilled* from sessions; sessions are never mutated
6. **Rhythm** — the user's cadence schedule (daily anchor, weekly review, monthly drift-check, quarterly direction)

**Spine:** Question → Session (raw context accumulates) → Synthesize → Artifact (refined). Frameworks shape questions. Profile + Rhythm decide when the system proactively pushes vs. waits to be pulled.

## Audiences and modes

Each user configures an interaction mode in Profile:

- **Deep sessions on demand** — user invokes a skill, gets a 20–40 min guided dialogue
- **Scheduled touches** — cadence pings a single wide question; user answers briefly; context accumulates
- **Ambient** (v1.x) — system listens during general chat and inserts coaching moments when useful
- **Hybrid** — any combination, with one dominant

v1 ships deep + scheduled. Ambient is deferred to v1.x because it benefits from seeing real v1 usage before we design it.

## MVP scope (v1)

One artifact end-to-end — **Values** — with the full spine machinery around it. Extensibility is baked in: adding the next artifact (Audience in v1.1) is pure content work (a new artifact template, a few frameworks, a question bank) with no rebuild.

**In v1:**

- Profile intake (`groundwork-intake`)
- Ingest and seed (`groundwork-ingest`, `groundwork-seed`) — research-driven first-run that eliminates the blank-page problem by distilling material the user has already produced (articles, interviews, manifestos, videos, social posts)
- Values artifact, end-to-end
- Spine skills: session, ask, synthesize, review, rhythm, framework
- Framework library with 3–5 seed frameworks: Coaching Habit 7Q, 5 Prism, Ikigai, and Gleb's modes (fractal overwhelm, drift, avoidance pattern, inside-out, additive-subtractive)
- Template vault — ships alongside the skill pack, ready to drop into Obsidian or use as a flat markdown folder
- Visual brand kit (`groundwork-brand`) and `groundwork-visual-card` — load-bearing for v1 because the Values artifact needs a shareable face
- Voice-readiness and bot-readiness by contract (no wrappers yet in v1, but all skills honor the contracts)

**Stretch, v1.x-friendly if time is short:**

- `groundwork-visual-identity` (deterministic p5.js glyph per artifact)
- `groundwork-visual-map` (relational visuals — more useful once multi-element artifacts land)
- `groundwork-visual-hero` (nano banana / Gemini 2.5 Flash Image for editorial cover art)

**Not in v1:**

- Audience, Offer, Positioning, Principles, Drift Log artifacts (stubs with "coming soon" markers)
- Ambient mode
- Voice wrapper (delivered "for free" by Hermes for users on Hermes; Pipecat wrapper later)
- Telegram / Slack / Discord bot bridges (delivered "for free" by Hermes)
- Hosted Vercel Chat SDK variant (see v1.x roadmap)
- Multi-tenant / shared artifact features

## Architecture

### Repository layout

The project is one git repo, publishable via `npx skills add glebis/groundwork`:

```
groundwork/
├── README.md                       # install / onboard / link to docs
├── LICENSE
├── skills/                         # each subdir is an installable skill (per `npx skills` convention)
│   ├── groundwork-intake/
│   │   └── SKILL.md
│   ├── groundwork-ingest/
│   │   └── SKILL.md
│   ├── groundwork-seed/
│   │   └── SKILL.md
│   ├── groundwork-session/
│   │   └── SKILL.md
│   ├── groundwork-ask/
│   │   └── SKILL.md
│   ├── groundwork-synthesize/
│   │   └── SKILL.md
│   ├── groundwork-review/
│   │   └── SKILL.md
│   ├── groundwork-rhythm/
│   │   └── SKILL.md
│   ├── groundwork-framework/
│   │   └── SKILL.md
│   ├── groundwork-brand/
│   │   └── SKILL.md
│   └── groundwork-visual-card/
│       └── SKILL.md
├── template-vault/                 # ships with the pack; copied to user's chosen location on intake
│   └── .groundwork/
│       ├── profile.md              # user profile + rhythm config (frontmatter driven)
│       ├── artifacts/
│       │   └── values.md           # seeded stub for Values
│       ├── sessions/               # append-only raw logs
│       ├── intake/
│       │   ├── sources/            # cached ingested material
│       │   └── research-findings.md
│       ├── frameworks/             # per-user framework library (copy of seed, user-editable)
│       │   ├── coaching-habit-7q.md
│       │   ├── 5-prism.md
│       │   ├── ikigai.md
│       │   ├── gleb-modes.md
│       │   └── README.md           # how to add your own
│       └── visuals/
│           ├── brand/
│           │   ├── brand.md        # tokens, typography, palette
│           │   └── samples/
│           └── output/             # generated cards, glyphs, hero art
└── docs/
    ├── specs/
    │   └── 2026-04-16-groundwork-design.md   # this document
    ├── plans/                       # implementation plans (written by writing-plans skill)
    ├── frameworks/                  # canonical framework library (source; copied into user template on intake)
    │   ├── coaching-habit-7q.md
    │   ├── 5-prism.md
    │   ├── ikigai.md
    │   └── gleb-modes.md
    └── brand/
        └── starter-kits/            # 3-5 starter brand directions (Scriptorium, Studio, Fern, Ember, Ice)
```

### Key architectural decisions

1. **Skills are the unit of distribution.** One `SKILL.md` per skill, in its own subdirectory. Slash commands (`/groundwork-values` etc.) are thin ergonomic wrappers added only for Claude Code; skills work fine without them.

2. **`npx skills` is the distribution channel.** No npm package, no hosted install. Users run `npx skills add glebis/groundwork`; the tool symlinks the canonical skill files into each supported agent's skills directory. Updates via `npx skills update`.

3. **Frameworks are content, not code.** A framework is a markdown file with frontmatter (`name`, `purpose`, `when_to_use`, `questions[]`, `artifacts_served[]`, `source`). Adding a framework requires no release; users and Gleb can add frameworks by editing markdown in `.groundwork/frameworks/`.

4. **State lives in `.groundwork/`**, a hidden folder. Location configurable in Profile:
   - Gleb points it at his Obsidian vault (wikilinks flow naturally)
   - Tech solopreneurs point it at a git repo or project folder
   - Non-tech users let intake drop it in `~/Documents/groundwork/` by default
   - Hermes community members use Hermes's per-profile data directory

5. **Append-only sessions, distilled artifacts.** Sessions never get mutated or deleted; synthesize writes a new version of the artifact and appends a changelog section. The audit trail is free; disk is cheap.

6. **Scheduled tasks are runtime-dispatched.** Hermes has built-in cron and delivers scheduled prompts to any platform; Claude Code users use the `schedule` skill. Both dispatch the same `groundwork-ask` skill. Groundwork itself is not a scheduler.

7. **Profile is the config, not a database.** One markdown file with frontmatter. Human-editable. No SQLite, no sync layer.

### Data flow

```
                        ┌────────────────────────┐
                        │      USER (chat)       │
                        └────────────┬───────────┘
                                     │
                        ┌────────────▼───────────┐
                        │  Runtime (Claude Code, │
                        │  Hermes, Cursor, etc.) │
                        └────────────┬───────────┘
                                     │ invokes skill
                    ┌────────────────▼────────────────┐
                    │       groundwork-*  skills      │
                    └────────────────┬────────────────┘
                                     │ reads/writes
   ┌─────────────────────────────────▼─────────────────────────────────┐
   │                        .groundwork/                               │
   │                                                                   │
   │  profile.md ◄──  rhythm, cadence, mode                            │
   │  artifacts/values.md ◄──  distilled, published-facing             │
   │  sessions/*.md ◄──  append-only raw interaction logs              │
   │  intake/research-findings.md ◄──  ingested material summary       │
   │  frameworks/*.md ◄──  inquiry tools                               │
   │  visuals/brand/brand.md ◄──  tokens for card/identity/hero        │
   └───────────────────────────────────────────────────────────────────┘

Primary loop:  ask → session → synthesize → artifact
Onboarding:    intake → ingest → seed → session
Rhythm:        scheduler → ask → session → synthesize (on cadence)
Review:        review → reads artifacts + sessions → surfaces drift
Visual:        brand → visual-card → reads artifacts + brand tokens → renders
```

## Skill inventory

Each skill ships with its own `SKILL.md`. The I/O contract is written at the top of each: what files it reads, what files it writes, what it returns.

**Onboarding skills:**

- `groundwork-intake` — first-run profile + cadence setup. Creates `.groundwork/profile.md`, chooses data-folder location, picks brand direction.
- `groundwork-ingest` — takes links, files, or keywords. Uses existing Firecrawl / YouTube / Instagram / Tavily infrastructure where applicable. Writes cached sources and `research-findings.md`.
- `groundwork-seed` — reads research findings + profile, proposes initial draft artifacts with source citations. User reviews keep/cut/sit-with; merges into real artifacts.

**Spine skills:**

- `groundwork-session` — deep dialogue on a named artifact. Uses timely questions from the framework library; writes session log; optionally invokes synthesize at end.
- `groundwork-ask` — poses a single wide question (used by scheduled pings and ambient mode). Short interaction, appends to session log.
- `groundwork-synthesize` — reads recent sessions, distills into an artifact update. Writes a new artifact version with changelog.
- `groundwork-review` — scheduled or on-demand review of drift, salience, unanswered questions. Cross-artifact.
- `groundwork-rhythm` — view/edit cadence config in Profile.
- `groundwork-framework` — pull a named framework into context for a session; or list available frameworks; or install a new framework file.

**Visual skills:**

- `groundwork-brand` — interactive brand-direction picker. Shows side-by-side samples from starter kits (Scriptorium, Studio, Fern, Ember, Ice), user picks, the skill writes `brand.md` with color tokens, typography rules, aesthetic notes.
- `groundwork-visual-card` — renders a named artifact as a share-ready card using brand tokens. Primary typography: EB Garamond with OpenType features (small caps, old-style figures, discretionary ligatures, swash caps). Secondary sans for labels. SVG + PNG output.

**v1 stretch (slide to v1.x if short on time):**

- `groundwork-visual-identity` — generative glyph per artifact, p5.js, seeded deterministically by content hash. Same inputs → same glyph. Leverages the user's existing `algorithmic-art` skill under the hood.
- `groundwork-visual-map` — relational visuals (audience map, offer ladder, positioning quadrant). Becomes useful once multi-element artifacts exist, so naturally aligns with v1.1.
- `groundwork-visual-hero` — AI-generated editorial cover art via nano banana (Gemini 2.5 Flash Image). Prompt seeded by artifact content + brand tokens.

## Framework library

Canonical frameworks live in `docs/frameworks/` and are copied into the user's `.groundwork/frameworks/` during intake so each user owns a local, editable copy.

**v1 seed set (chosen for Values-first scope):**

- **Coaching Habit 7Q** (Michael Bungay Stanier) — the widest, most-used wedge for self-inquiry
- **5 Prism Model** (Rybina & Muradyan) — Feelings/Thoughts/Paradoxes/Conflicts/Needs, deep values surface
- **Ikigai** — four-intersection, values-adjacent
- **Gleb's modes** — fractal overwhelm, drift, avoidance pattern, inside-out, additive-subtractive, context diet, salience, base layer — surfaced as questions that can fire at any time
- One of: GROW or T Coaching Model (TBD during implementation — pick whichever reads more naturally inside a skill)

**v1.x additions (for Audience and Offer):**

- Jobs to be Done
- Value Proposition Canvas (Osterwalder)
- Business Model Canvas
- Audience Avatar / Buyer Persona
- Wardley Mapping (advanced)
- Positioning Statement (April Dunford-style)

**Framework file structure:**

```markdown
---
name: Coaching Habit 7Q
slug: coaching-habit-7q
purpose: Surface what a person actually wants, cares about, avoids, or is learning
when_to_use:
  - early-values-work
  - mid-session-pivot
  - weekly-review
artifacts_served: [values, self-map, drift-log]
source: "Michael Bungay Stanier, The Coaching Habit"
questions:
  - slug: kickstart
    text: "What's on your mind?"
    tier: wide
  - slug: awe
    text: "And what else?"
    tier: deepen
  - slug: focus
    text: "What's the real challenge here for you?"
    tier: focus
  # ...
---

# Coaching Habit 7Q

(narrative body, usage notes, adaptation guidance)
```

Users and Gleb can add frameworks by dropping a new file in `frameworks/`. No code change, no release.

## Visual identity system

Two cleanly-separated layers.

**Layer A — Brand kit (Groundwork's own look, evolvable per user):**

- Typography: EB Garamond as the workhorse, with OpenType features (small caps, old-style figures, discretionary ligatures, swash caps). A secondary sans for small labels (pick during implementation — e.g., Inter, Söhne Breit, Neue Montreal)
- Palette: five starter directions shipping as editable stylesheets:
  - **Scriptorium** — ink black, paper cream, oxblood accent
  - **Studio** — warm whites, plum, mustard, charcoal
  - **Fern** — deep green, moss, bone, rust
  - **Ember** — near-black, ember orange, soft grey
  - **Ice** — porcelain, indigo, slate
- Personality: quirky, English, deliberate — small independent press aesthetic; not startup-SaaS
- Stored in `.groundwork/visuals/brand/brand.md` as CSS/SVG tokens + OpenType feature strings + aesthetic notes

**Layer B — Per-artifact visuals (using the brand):**

- `visual-card` — minimal vector cards per artifact, print- and share-ready
- `visual-identity` (stretch) — generative glyph per artifact, p5.js, deterministic
- `visual-map` (stretch) — relational visuals for multi-element artifacts
- `visual-hero` (stretch) — nano banana editorial cover art

All Layer-B skills read `brand.md` for tokens. Swap the brand → everything re-renders consistently.

## Composability contracts

Groundwork is designed so that a "processing system on top" (batch cohort processing, automation pipelines, external integrations) costs very little later. Every skill:

- **Reads files → writes files.** No database, no daemon, no hidden state.
- **Runs in two modes**: `interactive` (conversational; default) and `headless` (inputs supplied up front; no confirmation prompts; safe for batch).
- **Emits three output tiers**:
  - *Tier 1 — line* (~15 words): for status bars, bot notifications, voice pings
  - *Tier 2 — brief* (~40 words): for bot replies, voice summaries, daily-note insertions
  - *Tier 3 — full*: for terminal, artifact files, rich contexts
- Selected via a `--tier` argument; full is default.

**Artifact frontmatter contract** (all artifacts share this schema so downstream tools parse without heuristics):

```yaml
artifact_type: values                 # values | self-map | audience | offer | …
schema_version: 1
last_synthesized: 2026-05-01T18:23:00Z
source_sessions: [20260415, 20260420, 20260427]
speakable_summary: |
  A ~40-word voice-friendly summary, regenerated by synthesize every time.
owner: gleb
```

**Session file naming**: `sessions/YYYYMMDD-HHMM-<artifact>-<mode>.md` (e.g., `20260420-0730-values-scheduled.md`). Sessions are append-only; synthesize never rewrites them.

## Delivery and distribution

**Distribution:**

- Published at `github.com/glebis/groundwork` (or chosen org)
- Installed via `npx skills add glebis/groundwork`
- Users can install the whole pack or a subset via `--skill`
- Scope: global (`~/<agent>/skills/`) or project-local
- Updates via `npx skills update groundwork`

**Runtime support (tested in v1):**

- **Claude Code** — primary developer surface; Gleb's local flow
- **Claude Desktop** — same skills via agent directory; for audience B users who prefer the desktop app
- **Hermes Agent (Nous Research)** — primary community delivery; gives Telegram / Discord / Slack / WhatsApp / Signal coverage out of the box; scheduled cron delivers `ask` pings; voice-memo transcription handles voice input natively
- **Any other `npx skills`-compatible agent** — best-effort; expected to work since skills are `SKILL.md` format with no runtime-specific code

**Runtime detection**: the intake skill detects which runtime it's executing in and writes runtime-specific hints to the profile (e.g., "your scheduler is Hermes cron" vs. "your scheduler is Claude Code schedule skill"). Other skills read this to behave correctly per runtime.

## Voice and bot readiness

Design constraints baked in from v1, even though wrappers don't ship until later:

**Voice-ready:**

- Every question copy is a single speakable utterance — one idea, conversational, no mid-question bullet lists
- Session records tolerate rough transcript input (filler, self-repair); synthesize cleans before distilling
- All skill boundaries are plain text in / plain text out — a voice wrapper (Hermes's built-in; Pipecat later; a small custom wrapper alternatively) plugs in without touching core skill logic
- Artifacts carry a `speakable_summary` field regenerated on every synthesize

**Bot-ready:**

- Tier 1/2 outputs emit HTML (per Gleb's Telegram formatting preference); Tier 3 emits Markdown
- Ingest accepts a `.groundwork/intake/inbox/` folder where forwarded bot content lands; `ingest` processes it identically to URL inputs
- A later `groundwork-bot` bridge skill (v1.x) can wrap `ask` / `session` / `review` for Telegram / Slack / Discord delivery and capture replies back into sessions. Because the tiers and inbox folder are already in place, the bridge will be thin

**Hermes users**: voice and bot are both delivered "for free" by Hermes's gateway — Groundwork skills don't need to know voice is happening.

## Risks and open questions

Resolved in the implementation plan, not here:

1. **`npx skills` + Claude Desktop interop** — verify that skills installed via `npx skills add` load correctly in Claude Desktop (not only Claude Code). If divergence exists, ship a documented manual path.
2. **Hermes skill loading model** — confirm Hermes loads `SKILL.md` skills unmodified and supports multi-turn interactive dialogue (not only RPC-shaped short turns). An early implementation-plan step: author `groundwork-intake` and verify end-to-end in Hermes before building others.
3. **Profile location for Hermes** — Hermes profiles isolate state; confirm that pointing `.groundwork/` at a shared disk location works across profiles, or whether per-profile duplication is the right model.
4. **Scheduled-task dispatching portability** — the same `groundwork-ask` skill needs to be invocable by both Hermes's cron and Claude Code's scheduler; verify argument passing and exit-code conventions are compatible.
5. **nano banana cost/latency** — for `groundwork-visual-hero` (stretch), confirm generation cost and latency are acceptable for use inside a coaching flow. May need to move to off-loop generation.
6. **Brand file portability** — `brand.md` references fonts (EB Garamond); verify rendering works across runtimes and that non-tech users have a path to install / fall back gracefully.

## v1.x roadmap (rough order)

1. **v1.1 — Audience artifact.** Second full vertical slice. New frameworks: JTBD, Value Proposition Canvas, Audience Avatar.
2. **v1.2 — Offer artifact.** Third vertical slice. Frameworks: Offer ladder patterns, pricing-as-positioning.
3. **v1.3 — Voice wrapper for Claude Code users** (Pipecat or tiny wrapper). Parity with what Hermes users already have.
4. **v1.4 — Hosted Vercel Chat SDK variant.** For community members who cannot/will not install anything. Thin adapter over the same skills; skills run server-side; users open a Slack / Telegram / Discord link. Separate doc spec needed.
5. **v1.5 — Positioning, Principles, Drift Log artifacts.**
6. **v1.6 — Ambient mode.** Designed only after observing how deep + scheduled play out in real use.
7. **v2.0 — Community features.** Shared artifacts, moderator views, cohort-level synthesis. Separate design cycle.

## Success criteria

**Functional (must pass before declaring v1 complete):**

- A new user can run `npx skills add glebis/groundwork && <agent> 'run groundwork-intake'` and be in a working coaching rhythm within 20 minutes
- The Values artifact produced by a real end-to-end run (ingest → seed → 2 sessions → synthesize) is legibly *that user's* values, not a generic template
- A `groundwork-visual-card` rendering of Values is print-and-share-ready (not a placeholder)
- Scheduled `ask` pings land in at least one platform (Hermes Telegram OR Claude Code schedule) and their answers accumulate into sessions correctly
- Every skill operates headlessly with supplied inputs (for future batch pipelines)

**Experiential (what makes v1 worth shipping):**

- Gleb wants to use it in his own week, unprompted
- One Lab cohort member completes an intake + one deep session without hand-holding
- The Values card is the kind of thing someone would share, not hide

**Quality:**

- Zero placeholders in shipped skill prompts
- Every skill has a one-paragraph I/O contract at the top of its `SKILL.md`
- Framework files all validate against the frontmatter schema
- All outputs support the three tiers

## What this spec deliberately does not decide

- Final choice between GROW and T Coaching Model in the v1 seed frameworks (implementation-plan concern)
- Exact secondary sans for typography (pick during brand kit authoring)
- Whether `.groundwork/` uses Obsidian wiki-links by default in the template vault (likely yes; verified at implementation)
- Whether slash commands (`/values`, `/review`) ship in v1 — they're ergonomic sugar; skills are the substance
- The final org under which the GitHub repo lives (`glebis/groundwork`, `motka/groundwork`, or a community-owned org later)

## References

- Vercel Agent Skills — <https://vercel.com/docs/agent-resources/skills>
- `npx skills` CLI — <https://github.com/vercel-labs/skills>
- Skills directory — <https://skills.sh>
- Hermes Agent — <https://github.com/NousResearch/hermes-agent>
- obra/superpowers (inspiration) — <https://github.com/obra/superpowers>
- Related vault research: `ai-research/20260415-hermes-agent-nous-research.md`
- Related vault lexicon: `LEXICON.md` (fractal overwhelm, drift, avoidance pattern, inside-out, additive-subtractive)
