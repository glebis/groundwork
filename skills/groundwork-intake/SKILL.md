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

6. **Copy the template vault.** Locate `template-vault/.groundwork/` bundled with this skill pack, then copy it recursively into `data_folder`. Preserve all files. Do not overwrite an existing `.groundwork/` — instead ask the user to confirm or pick a different folder.

   **Resolving the pack root.** Try these candidates in order and use the first one that contains `template-vault/.groundwork/`:

   ```bash
   for ROOT in \
       "${CLAUDE_PLUGIN_ROOT:-}" \
       "$HOME/.claude/plugins/groundwork" \
       "$HOME/.claude/plugins/groundwork-pack" \
       "$HOME/ai_projects/groundwork"; do
     [ -n "$ROOT" ] && [ -d "$ROOT/template-vault/.groundwork" ] && PACK_ROOT="$ROOT" && break
   done
   # Last-resort search (bounded to known roots):
   if [ -z "${PACK_ROOT:-}" ]; then
     PACK_ROOT="$(find "$HOME/.claude/plugins" "$HOME/ai_projects" -maxdepth 4 -type d -path '*/template-vault/.groundwork' 2>/dev/null | head -1 | sed 's|/template-vault/.groundwork||')"
   fi
   [ -z "${PACK_ROOT:-}" ] && { echo "template-vault not found — reinstall the groundwork skill pack"; exit 1; }
   cp -R "$PACK_ROOT/template-vault/.groundwork" "$DATA_FOLDER/.groundwork"
   ```

   If no candidate resolves, stop with the "No template vault found" error from the Failure modes section.

7. **Write profile and interpolate scaffold.** Rewrite `profile.md` frontmatter from the collected answers (`owner`, `data_folder` as absolute path, `mode`, `runtime`, `rhythm.*`, `schema_version: 1`, `active_artifacts: [values]`). Then substitute `{{owner_name}}` and `{{data_folder_path}}` across every markdown file under `data_folder` so artifact and framework templates pick up the user's identity:

   ```bash
   find "$DATA_FOLDER" -type f -name "*.md" -exec sed -i '' \
       -e "s|{{owner_name}}|$OWNER|g" \
       -e "s|{{data_folder_path}}|$DATA_FOLDER|g" {} \;
   ```

   (Linux: drop the `''` after `-i`.)

8. **Register rhythm with the runtime.** If `mode` is `scheduled` or `hybrid` and at least one rhythm field is non-null, invoke `groundwork-rhythm` in headless mode with the just-captured rhythm values. That skill translates the cadence into runtime-specific triggers (Claude Code `schedule`, Hermes cron, etc.). Skip if `mode` is `deep` or all rhythm fields are null.

9. **Offer ingest.** Ask: *"Want to seed your Values artifact with material you've already written or said somewhere? (y/n)"* — if yes, instruct the user to run `groundwork-ingest` next; if no, point them at `groundwork-session values` as the next step.

## Tiers

- **line**: `"profile written to {path}"`
- **brief**: profile path + one-line orientation
- **full**: profile path + changelog of what was set + next-step suggestion

## Headless mode

Accept all answers as a single JSON blob on stdin:

```json
{
  "owner": "Your Name",
  "data_folder": "~/.groundwork",
  "mode": "hybrid",
  "runtime": "claude-code",
  "rhythm": { "daily_anchor_time": "08:00", "weekly_review_day": "fri", "monthly_drift_day": 1, "quarterly_direction": true }
}
```

`data_folder` defaults to `~/.groundwork` but common choices include `$XDG_DATA_HOME/groundwork`, or a subfolder of an existing Obsidian vault (`~/path/to/vault/.groundwork`). The intake skill expands `~` to `$HOME` when writing the profile.

Write everything without prompting.

## Failure modes

- `.groundwork/` already exists → stop; do not overwrite. Ask the user to confirm or pick another path.
- No template vault found (installation broken) → stop with a clear error pointing to the reinstall command.
- Profile frontmatter fails schema validation after write → stop with the validation message; do not leave a partial profile.
