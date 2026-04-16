---
name: groundwork-synthesize
description: Read recent session logs for an artifact and distill them into the artifact's refined form. Writes a new version of the artifact file with an updated changelog and regenerated speakable_summary.
io_contract:
  reads:
    - "{data_folder}/profile.md"
    - "{data_folder}/artifacts/{artifact}.md"
    - "{data_folder}/sessions/*.md"
    - "{data_folder}/intake/research-findings.md"
  writes:
    - "{data_folder}/artifacts/{artifact}.md"
  returns: "summary of changes made + updated speakable_summary"
modes: [interactive, headless]
tiers: [line, brief, full]
---

# groundwork-synthesize

Distills raw session logs into a refined artifact. The artifact is rewritten in place with a fresh changelog entry and regenerated `speakable_summary`.

## When to use

- After a `groundwork-session` that produced meaningful content.
- On a cadence — monthly works for Values.
- Explicitly by the user when they want to see the current state cleaned up.

## What you do

1. **Read context.** The artifact file, all session files since `last_synthesized` (or all of them if never synthesized), the research-findings file.

2. **Extract candidates.** From sessions, pull out:
   - Declared values (explicit user statements: "I value X")
   - Implied values (patterns across multiple sessions: three times the user chose X over Y)
   - Tensions (values held in explicit conflict)
   - Principles-in-waiting (operating rules the user stated about *how* they work)

3. **Merge with existing.** The artifact has an existing Candidate values list. Merge by:
   - Keep values the user hasn't contradicted.
   - Add new values with a note of which session(s) they came from.
   - Mark values the user has spoken against with `~~strikethrough~~` and a note — don't delete (audit trail).
   - If a new session reframes an existing value, add the new phrasing alongside the old and mark the old as `[superseded by {date}]`.

4. **Write the artifact.** Rewrite `artifacts/{artifact}.md` with:
   - Updated frontmatter: `last_synthesized: {now-iso}`, `source_sessions: [...all session slugs included]`, regenerated `speakable_summary` (40 words max).
   - `## Candidate values` section with the merged list.
   - `## Recent reflections` section with 2-3 things that surfaced in the most recent sessions, in the user's own words (quoted).
   - `## Changelog` section: append a new entry with date, what changed, which sessions drove it.

5. **Never overwrite sessions.** Sessions are append-only input. This skill only writes the artifact file.

6. **Validate before writing.** Run the artifact schema check on the frontmatter you're about to write. If it fails, stop; emit the validation error and don't write.

## Tiers

- **line**: `"synthesized: {n} new values, {m} tensions, {updated} existing"`
- **brief**: the above + the new `speakable_summary`
- **full**: the above + a diff-style changelog of what moved in this pass

## Headless mode

Accept `--since {date}` or `--sessions {file1,file2,...}` to limit scope. Write without prompting. Used by monthly cadence automation.

## Failure modes

- No sessions since last_synthesized → stop; return "nothing to synthesize."
- Schema validation fails on the generated frontmatter → stop; do not write partial artifact.
- Artifact file has unexpected manual edits that conflict with existing changelog structure → merge conservatively: place new changes at the top and leave manual edits alone. Flag the conflict in the return summary.
