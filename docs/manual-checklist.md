# Manual end-to-end checklist (Values vertical slice)

The skills in this pack are LLM-executed prompts; behavior can't be unit-tested. This checklist is the human walk-through that proves a release works end-to-end. Run it before tagging a release.

## Setup

- [ ] Fresh machine or fresh data-folder location
- [ ] `npx skills add ./` from the repo root installs into `~/.claude/skills/`
- [ ] `ls ~/.claude/skills/groundwork-*` shows all 11 skills

## Claude Code flow

- [ ] Invoke `groundwork-intake` in Claude Code
  - [ ] Skill prompts for name, data-folder, mode, rhythm
  - [ ] Profile written at chosen data-folder
  - [ ] Template vault fully copied into `.groundwork/`
  - [ ] Frontmatter passes `python scripts/validate.py` if run against data-folder
- [ ] Invoke `groundwork-ingest` with 2 sample URLs (one article, one YouTube)
  - [ ] Sources cached in `intake/sources/`
  - [ ] `research-findings.md` populated with all eight sections
- [ ] Invoke `groundwork-seed values`
  - [ ] 5-7 candidate values presented with source citations
  - [ ] Interactive keep/cut/sit-with flow works
  - [ ] `values.md` updated; seed session logged
- [ ] Invoke `groundwork-session values`
  - [ ] Session runs 3-7 exchange cycles
  - [ ] Framework selection feels appropriate
  - [ ] Session log written with full transcript
- [ ] Invoke `groundwork-synthesize values`
  - [ ] Artifact updated with new candidate values
  - [ ] Changelog entry appended
  - [ ] `speakable_summary` ≤ 40 words and reads well aloud
- [ ] Invoke `groundwork-visual-card values`
  - [ ] SVG and PNG produced
  - [ ] Card visibly reflects the brand (Geist Mono, monochrome, ember accent)

## Hermes flow (interop spike)

- [ ] `npx skills add ./ -a hermes` succeeds (once Hermes is added to the skills registry)
- [ ] `hermes skills list` shows all 11 skills
- [ ] `groundwork-intake` invocable in `hermes chat`
- [ ] End-to-end same as Claude Code flow above

## Cadence

- [ ] `groundwork-rhythm` adds a daily anchor cron job
- [ ] Fire the cron manually; `groundwork-ask` runs and writes a session log
- [ ] `groundwork-review weekly` produces a drift read

## Bot surface (Hermes Telegram)

- [ ] Hermes Telegram gateway wired up
- [ ] Scheduled daily anchor ping arrives as a Telegram message
- [ ] Voice-memo reply transcribes and appends to the session log

Mark each box before tagging `v0.1.0`.
