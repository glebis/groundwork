---
name: groundwork-review
description: Cross-artifact review. Surfaces drift between intentions and recent activity, unanswered questions, and stale artifacts. Runs on cadence (weekly, monthly, quarterly) or on demand.
io_contract:
  reads:
    - "{data_folder}/profile.md"
    - "{data_folder}/artifacts/*.md"
    - "{data_folder}/sessions/*.md"
  writes:
    - "{data_folder}/sessions/{YYYYMMDD}-{HHMM}-review-{scope}.md"
  returns: "drift summary + 1-3 suggestions"
modes: [interactive, headless]
tiers: [line, brief, full]
---

# groundwork-review

Cross-artifact reflection. Not an artifact-specific session; zoomed-out reading of the whole `.groundwork/` state.

## When to use

- Scheduled: weekly (Friday by default), monthly, quarterly.
- On demand: user wants a snapshot of where they are.

## What you do

1. **Read the whole `.groundwork/`.** Profile, all artifacts, all sessions in the review window (week/month/quarter).

2. **Compute drift.** For each active artifact:
   - What did the user *declare* they'd do (from Goal / Will answers in recent sessions)?
   - What did they *actually* do (from subsequent session answers about action)?
   - Score the gap qualitatively: `aligned`, `modest drift`, `significant drift`.

3. **Identify unanswered questions.** Any session log with a question but no answer (scheduled `ask` files that never got responded to). List them.

4. **Identify staleness.** Any active artifact with no session in the last 4 weeks (or longer than the user's declared cadence). Flag for re-engagement.

5. **Write the review log.** `sessions/{YYYYMMDD}-{HHMM}-review-{scope}.md`:

```yaml
---
session_type: review
scope: weekly  # or monthly, quarterly
started_at: 2026-04-17T18:00:00Z
artifacts_reviewed: [values]
owner: gleb
---
```

Body sections:
- `## Drift` — per-artifact summary
- `## Unanswered` — list of un-replied-to questions
- `## Stale` — artifacts not touched in window
- `## Suggestions` — 1 to 3 specific actions, each a single short sentence

6. **Don't lecture.** The review speaks in a single user-facing paragraph plus bullets. Never more than 300 words total visible content.

## Tiers

- **line**: `"reviewed: {drift_status}"`
- **brief**: drift status + top suggestion
- **full**: the whole paragraph + bullet sections

## Headless mode

Used by scheduled weekly/monthly triggers. Writes log without user prompt. If there are unanswered questions from scheduled asks, surface them via the runtime's notification mechanism (Hermes: multi-platform; Claude Code: stdout).

## Failure modes

- Review window has no sessions → still produce a review noting "quiet week" + base-layer check from gleb-modes.
