---
name: groundwork-ingest
description: Ingest material (URLs, files, keywords, Telegram inbox) and distill into research-findings.md. Warms the Values artifact's first seed with material the user has already produced.
io_contract:
  reads:
    - "{data_folder}/intake/sources/**"
    - "{data_folder}/intake/inbox/**"
    - "{data_folder}/profile.md"
  writes:
    - "{data_folder}/intake/sources/**"
    - "{data_folder}/intake/research-findings.md"
  returns: "count of sources ingested + section-by-section summary of research-findings"
modes: [interactive, headless]
tiers: [line, brief, full]
---

# groundwork-ingest

Takes a mixed bag of inputs (URLs, local files, keywords, or content already dropped in the inbox) and produces a distilled `research-findings.md`.

## Inputs accepted

- **URLs**: articles, interviews (YouTube), Instagram posts, Twitter/X posts. Delegated to existing tools:
  - Articles → `firecrawl` (CLAUDE.md rule: "Article scraping: Firecrawl only")
  - YouTube → `youtube-transcript` skill
  - Instagram → `instagram-transcribe` skill
- **Local files**: any markdown/text/PDF in `intake/sources/`. Copy to `intake/sources/` verbatim if supplied via path.
- **Keywords**: run `tavily-search` for "{user owner name} {keyword}" to find articles by/about the user. Cache to sources.
- **Inbox**: anything the user has forwarded via Hermes / Telegram into `intake/inbox/` since last ingest.

## What you do

1. **Collect inputs.** From arguments, interactive prompts, or the inbox folder. Cache all fetched content under `intake/sources/{slug}.md` with a brief frontmatter (`source_url`, `fetched_at`, `medium`).

2. **Distill.** Read all sources (new + existing). Write sectioned findings to `intake/research-findings.md`:
   - **Declared values** — direct statements ("I believe…", "I value…"). Include a source citation for each.
   - **Implied values** — patterns across three or more sources (e.g. every talk mentions kin-scale). Include a list of supporting source slugs.
   - **Recurring themes** — ideas the user returns to.
   - **Framings** — how the user positions their work. Quote the key phrases.
   - **Audience signals** — who the user talks to / for.
   - **Voice samples** — 5-10 quotes with strong voice, for tone calibration later.
   - **Contradictions and tensions** — places two sources disagree; interesting.
   - **Sources** — append metadata for every source ingested.

3. **Merge, don't overwrite.** If `research-findings.md` already has content, merge additively. Existing entries stay; new material appends under each section. Sources list is append-only with dedup by URL.

4. **Respect the structure.** The section headers are fixed because `groundwork-seed` parses them. Don't reorder; don't rename.

## Tiers

- **line**: `"ingested {n} sources"`
- **brief**: `line` + counts per section (declared, implied, themes, etc.)
- **full**: `brief` + a short excerpt from each section

## Headless mode

Accept a JSON list on stdin:

```json
[
  {"type": "url", "value": "https://…"},
  {"type": "file", "value": "/abs/path.md"},
  {"type": "keyword", "value": "personal OS"}
]
```

Ingest all without prompting.

## Failure modes

- A URL fails to fetch → log the failure, skip it, continue with the rest.
- The inbox folder doesn't exist → silently skip (it's fine).
- No sources collected at all → stop; return "nothing to ingest."
- `firecrawl` / `tavily-search` / `youtube-transcript` not available → instruct the user how to install; skip affected sources.
