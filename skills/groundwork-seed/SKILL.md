---
name: groundwork-seed
description: Read research-findings.md and frameworks, propose an initial draft of an artifact (Values in v1), confirm with user, merge into the artifact file. Eliminates the blank-page problem.
io_contract:
  reads:
    - "{data_folder}/profile.md"
    - "{data_folder}/intake/research-findings.md"
    - "{data_folder}/frameworks/*.md"
    - "{data_folder}/artifacts/{artifact}.md"
  writes:
    - "{data_folder}/artifacts/{artifact}.md"
  returns: "summary of what was seeded"
modes: [interactive]
tiers: [line, brief, full]
---

# groundwork-seed

Reads distilled research findings and proposes an initial draft of the target artifact. For v1, `values` is the only target.

## When to use

- After `groundwork-ingest` produced a non-empty `research-findings.md`.
- The user wants to warm the artifact before running a real session.

## What you do

1. **Read context.** Profile, research-findings.md, frameworks with `artifacts_served: [values]`.

2. **Propose candidates.** From the declared + implied values in research-findings, plus any tensions, propose 5-7 candidate values. For each:
   - A short phrase (3-7 words — "truth over comfort," "kin over scale")
   - A one-line rationale grounded in one or more source citations
   - A tag: `declared` (user said this explicitly) or `implied` (pattern-inferred)

3. **Present to user as a review list.** Format:

```
Values candidates seeded from your material:

  1. truth over comfort           [declared · sources: s03, s07]
     "I'd rather be right and alone than agreeable and wrong."

  2. kin over scale               [implied · sources: s01, s02, s05]
     You return often to friction over scale-first thinking.

  3. …

Mark each: keep (k), cut (c), or sit-with (s).
```

Ask the user to mark each. Interactive, not headless.

4. **Merge into the artifact.** For each kept: add to `## Candidate values` with the rationale and source slugs. For each sit-with: add under a `## Sitting with` subsection. Cut ones are recorded in the Changelog as "considered and rejected" but not in the main list.

5. **Update frontmatter.** Set `status: drafting`. Regenerate `speakable_summary` (40 words). Do not set `last_synthesized` — seeding is not synthesis.

6. **Log the seed.** Write `sessions/{YYYYMMDD}-{HHMM}-values-seed.md` with the user's keep/cut/sit-with decisions (for audit).

## Tiers

- **line**: `"seeded {n} candidates"`
- **brief**: the count + the kept list
- **full**: the kept + sit-with + cut lists with rationales

## Failure modes

- `research-findings.md` empty → stop; tell user to run `groundwork-ingest` first.
- User declines all candidates → that's a signal, not an error. Log the seed session anyway; suggest a real session.
