---
name: groundwork-intake
description: First-run profile setup for groundwork. Asks the user about cadence, runtime, data-folder location; writes profile.md and scaffolds the .groundwork/ directory.
io_contract:
  reads: []
  writes:
    - "{data_folder}/profile.md"
    - "{data_folder}/artifacts/values.md"
    - "{data_folder}/frameworks/*.md"
    - "{data_folder}/intake/research-findings.md"
    - "{data_folder}/visuals/brand/brand.md"
  returns: "path to profile.md + one-paragraph orientation"
modes: [interactive, headless]
tiers: [line, brief, full]
---

# groundwork-intake

First-run setup for the groundwork skill pack. Creates a user profile and scaffolds the `.groundwork/` directory at a user-chosen location.

## When to use

- The user has just installed groundwork and invokes this as their first action.
- The user wants to re-bootstrap at a different location (pass `--data-folder <new-path>`).

## What you do

1. **Detect runtime.** Check for environment signals (`CLAUDECODE`, `HERMES_SESSION`, presence of `.cursor/`) and record the answer. If ambiguous, ask the user which runtime they're in.

2. **Ask for identity.** One question: *"What name should appear on your artifacts? (a handle is fine)"* — this becomes `owner`.

3. **Ask for data-folder location.** Propose in this order of preference:
   - If an Obsidian vault is detected (look for `.obsidian/` in the user's home or a parent dir the user names), offer to drop `.groundwork/` inside the vault.
   - Otherwise, offer `~/Documents/groundwork/`.
   - Otherwise, ask explicitly.
   Confirm the path exists or can be created. Record as `data_folder` (absolute, ~-prefix expanded).

4. **Ask for mode.** Single question with three options: *"How do you want to work with groundwork? (1) deep sessions on demand, (2) scheduled touches from me, (3) both."* Record as `mode` (values: `deep`, `scheduled`, `hybrid`).

5. **If scheduled or hybrid, ask rhythm:**
   - Daily anchor time (HH:MM local, or "skip")
   - Weekly review day (mon/tue/wed/thu/fri/sat/sun, or "skip")
   - Monthly drift day (1-28, or "skip")
   Record each as `rhythm.*`. Nulls mean disabled.

6. **Copy the template vault.** From the installed skill pack's `template-vault/.groundwork/` into the chosen `data_folder`. Preserve all files. Do not overwrite an existing `.groundwork/` — instead ask the user to confirm or pick a different folder.

7. **Write profile.md.** Replace `{{owner_name}}` and `{{data_folder_path}}` placeholders with the user's answers. Set `schema_version: 1` and `active_artifacts: [values]`.

8. **Offer ingest.** Ask: *"Want to seed your Values artifact with material you've already written or said somewhere? (y/n)"* — if yes, instruct the user to run `groundwork-ingest` next; if no, point them at `groundwork-session values` as the next step.

## Tiers

- **line**: `"profile written to {path}"`
- **brief**: profile path + one-line orientation
- **full**: profile path + changelog of what was set + next-step suggestion

## Headless mode

Accept all answers as a single JSON blob on stdin:

```json
{
  "owner": "gleb",
  "data_folder": "~/Brains/brain/.groundwork",
  "mode": "hybrid",
  "runtime": "claude-code",
  "rhythm": { "daily_anchor_time": "08:00", "weekly_review_day": "fri", "monthly_drift_day": 1, "quarterly_direction": true }
}
```

Write everything without prompting.

## Failure modes

- `.groundwork/` already exists → stop; do not overwrite. Ask the user to confirm or pick another path.
- No template vault found (installation broken) → stop with a clear error pointing to the reinstall command.
- Profile frontmatter fails schema validation after write → stop with the validation message; do not leave a partial profile.
