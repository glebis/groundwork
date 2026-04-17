# contributing

Thanks for being here. Groundwork is a small, opinionated project and it grows mostly by careful addition — one framework, one artifact, one skill at a time.

```
░▒▓█▓▒░
```

## the shape of contributions we want

- **new frameworks** — inquiry tools distilled from a coaching/therapy lineage (ACT, Motivational Interviewing, Internal Family Systems, Clean Language, BMC, JTBD, Wardley Mapping…). Each framework is a single markdown file with a question library. See `template-vault/.groundwork/frameworks/` for the format
- **new artifact types** (v1.x) — audience, offer, positioning, principles are already planned. Other candidates: weekly-rhythms, decision-log, archetype-map
- **new agent runtimes** — wiring skills into Cursor, Codex, Continue, Windsurf, etc. Each runtime usually needs a small section in `groundwork-session`'s Runtime Adaptation
- **voice stacks** — wrappers for Pipecat, LiveKit, OpenAI Realtime, etc. Skills don't need to know voice is happening; stacks need to know how to call skills and speak tiered text
- **bug fixes and rough edges** — anything you hit while using the pack
- **translations** — skill docstrings, prompts, and framework question text into other languages. The core voice pipeline already auto-detects user language; translated frameworks let the coach voice match

Please **don't** open PRs for:
- personal framework content (coin your own modes in your local `frameworks/` folder; only frameworks with broad applicability belong in the seed set)
- AI-assisted content dumps without human curation — keep PRs human-signed
- scope expansion that breaks the 11-skill spine (open an issue first)

```
░▒▓█▓▒░
```

## dev setup

```bash
git clone https://github.com/glebis/groundwork ~/ai_projects/groundwork
cd ~/ai_projects/groundwork

# link skills into your agent for live testing
mkdir -p ~/.claude/skills
for d in skills/groundwork-*; do
  ln -s "$PWD/$d" ~/.claude/skills/"$(basename "$d")"
done
```

Edits to `skills/*/SKILL.md` propagate immediately — no reinstall. Same applies to frameworks under `template-vault/.groundwork/frameworks/` once you've run intake and your local `.groundwork/` is sourced from (or symlinked to) the repo copy.

Test in your agent of choice:

```
▸ /groundwork session values
```

```
░▒▓█▓▒░
```

## skill design conventions

Every skill is a markdown file with frontmatter. The frontmatter is the contract:

```yaml
---
name: groundwork-something
description: one line — what it does and when to use it
io_contract:
  reads:
    - "{data_folder}/path/to/input.md"
  writes:
    - "{data_folder}/path/to/output.md"
  returns: "brief description of return value"
modes: [interactive, headless]       # most skills support both
tiers: [line, brief, full]           # output length tiers
---
```

**Rules:**

- Use `{data_folder}` placeholder, never absolute paths
- Skills are near-pure functions — read files, write files, return a summary. No global state
- Every skill supports a `headless` mode that takes JSON on stdin and writes without prompting. This is how cadence automation runs
- Every skill emits output in three tiers (see README voice-mode section)
- Sessions are append-only; only artifacts get rewritten
- If you depend on a tool beyond read/write/message, add it to the Runtime Adaptation section so non-Claude-Code agents still work

**Don't:**

- Hard-code user identifiers (no "Gleb", no "/Users/..."). Use `{{owner_name}}` / `{{data_folder_path}}` placeholders resolved at intake
- Paste whole frameworks into chat — frameworks are scaffolding for the agent, not content for the user
- Skip the tiers — even if all three are identical, declare them explicitly

```
░▒▓█▓▒░
```

## framework contribution format

A framework is a single markdown file with a question library. Frontmatter spec:

```yaml
---
name: Human-readable name
slug: kebab-case-identifier
purpose: one-line description of what it surfaces
when_to_use:
  - trigger-situation-1
  - trigger-situation-2
artifacts_served: [values, audience, offer]   # which artifacts this helps with
source: "Attribution — book, paper, tradition, author"
questions:
  - slug: unique-question-id
    text: "The actual question, written as the agent will ask it"
    tier: wide | deepen | focus | close
---
```

Body of the file: short narrative on when and how to use it, and any adaptation notes.

Validate with:

```
▸ /groundwork framework validate path/to/your-framework.md
```

Personal/project-coined frameworks go under `template-vault/.groundwork/frameworks/examples/` with a `.example` suffix and a banner explaining they're templates.

```
░▒▓█▓▒░
```

## PR guidelines

- One topic per PR. A new framework, a runtime adapter, and a bug fix are three PRs
- If it touches a skill contract, link the design-spec section it's aligned with (`docs/specs/2026-04-16-groundwork-design.md` + line range)
- Add or update a manual checklist entry in `docs/manual-checklist.md` if your change affects end-to-end flow
- Changes to the seed framework set need a brief rationale: why this belongs in the default pack vs. `examples/`
- Keep commit messages in the existing style (`feat(skills): …`, `docs: …`, `feat(frameworks): …`). No AI-coauthor tags unless the work was substantially AI-assisted

```
░▒▓█▓▒░
```

## code of conduct

Be kind. Assume good faith. The project is values-adjacent — treat each other the way the skills ask users to treat themselves. Harassment, bad-faith argumentation, or ideological purity tests don't belong here. If something's off, open an issue and tag the maintainer.

```
░▒▓█▓▒░
```

## license

Contributions are accepted under the same MIT license as the rest of the project. By opening a PR you agree your work can be redistributed under those terms.

```
                                                  ░▒▓ thanks for building  ▓▒░
```

```
                              ░░▒▒▓▓▓▓▒▒░░
                         ░░▒▒▓▓████████████▓▓▒▒░░
                     ░░▒▒▓▓██████████████████████▓▓▒▒░░
                ░░▒▒▓▓████████████████████████████████▓▓▒▒░░
           ░░▒▒▓▓██████████████████████████████████████████▓▓▒▒░░
       ░░▒▒▓▓██████████████████████████████████████████████████▓▓▒▒░░
    ░░▒▒▓▓████████████████████████████████████████████████████████▓▓▒▒░░
 ░░▒▒▓▓██████████████████████████████████████████████████████████████▓▓▒▒░░
░▒▓████████████████████████████████████████████████████████████████████▓▒░
░▓████████████████████████████████████████████████████████████████████████▓░
░▒▓████████████████████████████████████████████████████████████████████▓▒░
 ░░▒▒▓▓██████████████████████████████████████████████████████████████▓▓▒▒░░
    ░░▒▒▓▓████████████████████████████████████████████████████████▓▓▒▒░░
       ░░▒▒▓▓████▓▓▒▒░░    ░░▒▒▓▓████████▓▓▒▒░░    ░░▒▒▓▓████▓▓▒▒░░
            ░▒▒░              ░▒▒▓▓▒▒░              ░▒▒░
```

