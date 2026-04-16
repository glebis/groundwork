---
name: groundwork-ask
description: Pose a single wide question tied to an artifact and append the answer to a session log. Used by scheduled pings and ambient mode. Short interaction.
io_contract:
  reads:
    - "{data_folder}/profile.md"
    - "{data_folder}/frameworks/*.md"
    - "{data_folder}/artifacts/{artifact}.md"
    - "{data_folder}/sessions/*.md"
  writes:
    - "{data_folder}/sessions/{YYYYMMDD}-{HHMM}-{artifact}-ask.md"
  returns: "path to the new session file"
modes: [interactive, headless]
tiers: [line, brief, full]
---

# groundwork-ask

Single-question interaction. Used by scheduled pings ("daily anchor," "weekly review") and by ambient mode. Collects one short answer and logs it.

## When to use

- A scheduler (Hermes cron, Claude Code `schedule`) invoked you with a cadence reason.
- The user explicitly wants a light touch: `groundwork-ask values`.

## What you do

1. **Read context.** Profile, the target artifact, last 3 sessions on it.

2. **Pick the question.** Based on cadence reason (passed as argument `--reason` or inferred from time-of-day):
   - `daily-anchor` → a `wide` question from the artifact's frameworks, rotated so we don't repeat yesterday's.
   - `weekly-review` → `drift` from `gleb-modes` OR `learning` from `coaching-habit-7q`, alternating.
   - `monthly-drift` → `paradoxes` from `5-prism` OR `salience` from `gleb-modes`.
   - `ad-hoc` → Kickstart from Coaching Habit.

3. **Ask.** One sentence. Wait for the answer.

4. **Acknowledge.** A single short acknowledgment — no coaching follow-up. This is deliberately shallow; depth happens in `groundwork-session`.

5. **Write the log.** `{YYYYMMDD}-{HHMM}-{artifact}-ask.md` with frontmatter:

```yaml
---
session_type: ask
artifact: values
cadence_reason: daily-anchor
question_slug: kickstart
framework_slug: coaching-habit-7q
started_at: 2026-04-16T08:00:00Z
owner: gleb
---
```

Body: the question asked, the user's answer, verbatim.

6. **No synthesize prompt.** Ask skills accumulate; synthesis runs on a cadence or on explicit invocation.

## Tiers

- **line**: `"asked: {question[:40]}…"`
- **brief**: question slug + framework slug + where log is
- **full**: the above + one-sentence echo of the user's answer (for bot surfaces that allow a short reply)

## Headless mode

For scheduled automated pings: no user prompt, just write a pre-formed question and a `status: pending-answer` log file. The next interactive session will surface it.

## Failure modes

- Profile missing → silently stop (scheduled runs shouldn't crash; log the failure to stderr).
- Artifact missing → same.
