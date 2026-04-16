---
name: groundwork-framework
description: List, inspect, validate, or add frameworks in the user's local framework library. Frameworks are content files — this skill is the librarian.
io_contract:
  reads:
    - "{data_folder}/frameworks/*.md"
  writes:
    - "{data_folder}/frameworks/{slug}.md (on 'add')"
  returns: "list / inspection / validation report / confirmation of add"
modes: [interactive, headless]
tiers: [line, brief, full]
---

# groundwork-framework

Manages the user's framework library.

## Subcommands

- `list` — list installed frameworks with slug + purpose
- `show {slug}` — print the full framework (frontmatter + body)
- `validate` — run the framework schema against every file in `frameworks/`; report any failures
- `add` — guide the user to author a new framework (interactive) or accept one via stdin (headless)
- `sync` — re-pull canonical frameworks from the installed skill pack's `template-vault/.groundwork/frameworks/`; ask before overwriting user-edited files

## `add` workflow

1. Ask the user what the framework is for (becomes `purpose`).
2. Ask `name` (human-facing) and `slug` (filename-safe).
3. Ask which `artifacts_served` and `when_to_use` tags apply (multi-select from the schema's enums).
4. Ask for 3-7 questions; for each: text + tier (wide/deepen/focus/close).
5. Write the file under `frameworks/{slug}.md`.
6. Run the schema validator against the new file; if it fails, show the error and let the user fix.

## `sync` workflow

1. Diff canonical vs. user's versions. Files only in canonical get copied. Files the user has edited get flagged — ask per-file before overwriting.
2. Never delete user-added frameworks.

## Tiers

- **line**: e.g. `"6 frameworks loaded"` or `"added: {slug}"`
- **brief**: `list` output as a short table
- **full**: full framework bodies for `show`; full validation report for `validate`

## Headless mode

Accept a JSON blob on stdin for `add`:

```json
{
  "name": "Deep Work",
  "slug": "deep-work",
  "purpose": "…",
  "when_to_use": ["weekly-review"],
  "artifacts_served": ["self-map"],
  "source": "Cal Newport",
  "questions": [ {"slug": "q1", "text": "...", "tier": "wide"} ]
}
```

## Failure modes

- `validate` finds a broken framework → list the failures; exit non-zero in headless mode.
- `add` input fails validation → show the error; in interactive mode, offer to edit; in headless mode, exit non-zero without writing.
