---
name: groundwork-session
description: Run a deep coaching session on a named artifact (Values in v1). Uses timely questions from the framework library; appends a session log; optionally invokes synthesize at the end.
io_contract:
  reads:
    - "{data_folder}/profile.md"
    - "{data_folder}/frameworks/*.md"
    - "{data_folder}/artifacts/{artifact}.md"
    - "{data_folder}/sessions/*.md"
  writes:
    - "{data_folder}/sessions/{YYYYMMDD}-{HHMM}-{artifact}-deep.md"
  returns: "path to the new session file + brief summary"
modes: [interactive]
tiers: [line, brief, full]
---

# groundwork-session

Runs a deep (20-40 minute) guided coaching dialogue on a named artifact. In v1, the only artifact is `values`.

## When to use

- User invokes it explicitly: `groundwork-session values`.
- After `groundwork-intake` and (optionally) `groundwork-seed`, as the first real session.

## What you do

1. **Read context.** Load profile.md, the target artifact file, the most recent 3 sessions on this artifact (if any), and all frameworks whose `artifacts_served` includes this artifact.

2. **Choose an opening framework.** Based on:
   - If the artifact has `status: seeded` and no prior sessions → use **Coaching Habit 7Q's Kickstart question** ("What's on your mind?") to start wide.
   - If the artifact has been synthesized at least once → use **5 Prism's Feelings question** to ground before widening.
   - If the user has declared something to work on in recent sessions → use **GROW's Goal question**.

3. **Ask the opening question.** Single sentence. Wait for the user's answer. Never paste the whole framework into the chat — a framework is scaffolding for you, not content for the user.

4. **Deepen.** Based on the answer, pick the next question by these rules:
   - If the answer was short (< 30 words): use a `deepen`-tier question from the same framework ("and what else?").
   - If the answer revealed emotion without clarity: switch to 5 Prism (Feelings → Thoughts → Needs).
   - If the answer revealed a conflict or avoidance: switch to `gleb-modes` and ask the matching mode question.
   - If the answer reached a decision point: use GROW's Options question with the adapted third clause.

5. **Continue for 3-7 exchange cycles.** Don't run a script; respond to what the user actually says.

6. **Close.** Use either the Coaching Habit's Learning question ("What was most useful?") or, if the user is in generative energy, `additive-subtractive` ("Are we generating or cutting right now?").

7. **Write the session log.** Create `{data_folder}/sessions/{YYYYMMDD}-{HHMM}-{artifact}-deep.md` with frontmatter:

```yaml
---
session_type: deep
artifact: values
started_at: 2026-04-16T14:02:00Z
ended_at: 2026-04-16T14:38:00Z
framework_slugs_used: [coaching-habit-7q, 5-prism]
question_slugs_asked: [kickstart, awe, feelings, needs, learning]
owner: gleb
---
```

Then the full transcript of the dialog, as-is. Do not paraphrase the user's words.

8. **Offer to synthesize.** End by asking: *"Want me to roll this into your Values artifact now, or let it sit for a while?"* If yes, invoke `groundwork-synthesize values`. If no, do nothing more — the session log is enough.

## Tiers

- **line**: `"session logged → {path}"`
- **brief**: frameworks used + question slugs asked + where the log is
- **full**: the above + a three-sentence read of what felt alive in the session (your own summary, clearly marked as yours)

## Failure modes

- Profile missing → stop; tell the user to run `groundwork-intake` first.
- Artifact file missing → stop; tell the user the intake step didn't complete.
- No frameworks loaded for this artifact → stop; tell the user to run `groundwork-framework sync`.
