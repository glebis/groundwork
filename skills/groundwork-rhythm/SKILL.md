---
name: groundwork-rhythm
description: View or edit the user's cadence configuration in profile.md. Registers or unregisters scheduled tasks with the active runtime (Hermes cron, Claude Code schedule).
io_contract:
  reads:
    - "{data_folder}/profile.md"
  writes:
    - "{data_folder}/profile.md"
  returns: "current rhythm + a summary of any scheduled tasks registered"
modes: [interactive, headless]
tiers: [line, brief, full]
---

# groundwork-rhythm

Edits the `rhythm:` block of `profile.md` and reconciles scheduled tasks with the active runtime.

## When to use

- User says: "change my weekly review day to Sunday."
- User wants to turn off daily pings: "stop the daily anchor."
- User wants to see the current schedule: invoke with no arguments.

## What you do

1. **View mode (no arguments).** Print the current `rhythm:` block in a readable table. Also list scheduled tasks currently registered with the runtime (if the runtime is Hermes, run `hermes cron list`; if Claude Code, run `schedule list`). Compare and flag any divergence.

2. **Edit mode.** Ask the user which cadence they want to change (daily anchor / weekly review / monthly drift / quarterly direction). Confirm the new value or "off." Validate against the profile schema before writing.

3. **Reconcile with runtime.**
   - Hermes: call `hermes cron ...` with the new schedule (`hermes cron add groundwork-ask ...` for each active cadence). Remove old tasks that no longer apply.
   - Claude Code: use the `schedule` skill to register each cadence as a cron trigger that invokes `groundwork-ask` with `--reason`.
   - Other runtimes: print the user-visible instructions for setting up cron manually; don't attempt.

4. **Never silently change profile.** Always confirm the user wants the edit before writing. Never proceed when the user says "not yet."

## Tiers

- **line**: `"rhythm updated: {changed_field}"`
- **brief**: the full current rhythm block
- **full**: the above + diff of what was registered/deregistered with the runtime

## Headless mode

Accept a JSON patch on stdin:

```json
{"weekly_review_day": "sun", "daily_anchor_time": null}
```

Apply without prompting. Used by `groundwork-intake` during first-run setup and by test harnesses.

## Failure modes

- Profile missing → instruct the user to run `groundwork-intake` first.
- Runtime doesn't support scheduling (e.g., Cursor) → write the profile anyway, print manual-instructions text.
- Hermes cron command fails → roll back the profile change and surface the error.
