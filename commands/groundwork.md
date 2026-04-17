---
description: Groundwork entry point — smart triage across money / activities / context, or direct route to a skill.
argument-hint: "[intake|ingest|session|rhythm|review|ask|framework|seed|synthesize|brand|visual-card] [extra args…]"
---

You are the `/groundwork` dispatcher. `$ARGUMENTS` holds everything the user typed after the command.

## Stage 1 — deterministic verb routing

Split `$ARGUMENTS` into the first token (`VERB`) and the remainder (`REST`). Route using this table. If `VERB` matches exactly, invoke the mapped skill via the `Skill` tool, passing `REST` as its input (or empty if none). Stop here — do not run Stage 2.

| Verb            | Skill                      |
|-----------------|----------------------------|
| `intake`        | `groundwork-intake`        |
| `ingest`        | `groundwork-ingest`        |
| `session`       | `groundwork-session`       |
| `rhythm`        | `groundwork-rhythm`        |
| `review`        | `groundwork-review`        |
| `ask`           | `groundwork-ask`           |
| `framework`     | `groundwork-framework`     |
| `seed`          | `groundwork-seed`          |
| `synthesize`    | `groundwork-synthesize`    |
| `brand`         | `groundwork-brand`         |
| `visual-card`   | `groundwork-visual-card`   |

If `VERB` is unknown but non-empty, print `unknown verb "{VERB}" — falling back to triage` and continue to Stage 2.

## Stage 2 — smart triage (runs when no verb matched)

### 2a. Bootstrap check (fast-path)

Check `~/Brains/brain/.groundwork/profile.md`. If missing → invoke `groundwork-intake` and stop. If present → parse its frontmatter for `owner`, `mode`, `rhythm.*`, `active_artifacts`, `data_folder`.

### 2b. Gather state across three scales

Run these in parallel where possible. Keep each probe cheap; skip any source that errors.

**Money scale** — what the user owes / is owed / needs to ship for revenue.
- Linear: `mcp__linear-server__list_issues` filtered by label in (`revenue`, `billing`, `tax`) OR project matching `Taxes|Lab|Agency`, state ≠ Done, top 5 by priority.
- Daily note `~/Brains/brain/Daily/$(date +%Y%m%d).md` — grep for `€`, `EUR`, `RUB`, `invoice`, `tax`, `VAT`, `Zhutov`, `Lab 0`.
- Recent memory pointers: revenue priority, taxes overdue, Zhutov dispute, Russian billing.

**Activity scale** — ongoing work that expects cadence.
- Trails index: `~/Brains/brain/Trails/Trails.md` — list active trails.
- Life Lab experiments: `~/Brains/brain/Experiments/` (glob for active ones, i.e. not archived).
- Current week's Lab deliverables (Claude Code Lab): most recent file in `Channels/` or lab folders.
- Linear issues with label `lab` or `content`.

**Context scale** — how the user is doing right now.
- Today's daily note: anxiety rating, sleep, DIMs/SIMs, salience notes.
- Last trail-checkin timestamp (if tracked).
- Sertraline/health status (if relevant from memory).

### 2c. Rhythm-due check

Given `date +"%H:%M %u %d"` (hour:min, weekday 1=Mon..7=Sun, day-of-month):
- If current time ≥ `rhythm.daily_anchor_time` and no daily anchor ran today → **daily anchor due**.
- If weekday matches `rhythm.weekly_review_day` → **weekly review due**.
- If day-of-month equals `rhythm.monthly_drift_day` → **monthly drift due**.
- If today is Jan 1 / Apr 1 / Jul 1 / Oct 1 and `rhythm.quarterly_direction` is true → **quarterly direction due**.

### 2d. Artifact freshness

For each name in `active_artifacts`, stat `{data_folder}/artifacts/{name}.md`. mtime older than 14 days → stale.

### 2e. Compose dashboard + recommendation

Print a compact block (≤18 lines total). Use this shape, fill only what's non-empty:

```
groundwork · {YYYY-MM-DD HH:MM} · {owner}
───────────────────────────────────────
mode: {mode} · rhythm: d{daily_anchor_time} w{weekly_review_day} m{monthly_drift_day}
rhythm due: {list or —}
artifacts: {name} ({fresh|stale Nd}) …

money
  · {top item from Linear / daily / memory}
  · {second item if material}
activities
  · {top trail / experiment}
  · {second if material}
context
  · {notable from today's note}

→ recommended: /groundwork {verb} {args}
  why: {one line}

other options:
  /groundwork {verb2} — {one line}
  /groundwork {verb3} — {one line}
```

### 2f. Recommendation logic (priority order)

1. Rhythm due → recommend the matching skill (`review` for weekly/monthly, `session` for daily anchor, `synthesize` for quarterly).
2. Stale artifact → `/groundwork session {artifact}`.
3. Empty active artifact → `/groundwork ingest {artifact}` (if material likely exists) or `/groundwork session {artifact}`.
4. Money-scale has urgent item (deadline this week, overdue invoice, unresolved dispute) → `/groundwork ask "how do I move {item} forward?"` — uses the groundwork lens for a non-artifact question.
5. Fallback → `/groundwork session values`.

Never auto-invoke a Stage-2 recommendation. Print it and stop — the user decides.

## Rules

- This is Gleb's vault. Respect the conventions: Daily/, Trails/, Linear, Life Lab, Claude Code Lab. Memory has the rest.
- Don't fetch things that weren't asked for. If Linear, Daily, or trails probes fail or are slow, skip them and show `—`.
- Output in English. No emoji. No trailing summary.
- Total runtime target: ≤10s for the triage path.
