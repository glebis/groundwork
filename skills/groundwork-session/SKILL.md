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

## Session goals (the finish line)

A session is successful only if, by the time the user closes, you have produced **all** of:

1. **2-4 candidate values**, each a short phrase (2-5 words) paired with at least one concrete episode or behavior.
2. **At least one tension or contradiction** — between declared and lived values, or between two values competing under constraint.
3. **One direction-not-goal translation** — take one candidate value and name a behavior the user will keep moving toward this week. Not a SMART goal. A direction.
4. **A user-confirmed summary** — the user has corrected or approved your read-back before close.

If by exchange 4 you don't have (1), pull toward concrete episodes with `behavior-test`, `free-hour`, or "give me the last time that happened." If by exchange 6 you don't have (2), ask directly: "What feels in tension here?" If you near the close without (3), ask it explicitly. Never let the session drift to close without a confirmed summary.

## What you do

1. **Read context.** Load profile.md (also captures `runtime` for tool adaptation — see §Runtime adaptation), the target artifact file, the most recent 3 sessions on this artifact (if any), and all frameworks whose `artifacts_served` includes this artifact.

2. **Choose an opening framework.** Artifact-specific, not generic:
   - **`values` artifact, seeded + no prior sessions** → use **ACT values clarification** (`act-values`). Open with `peak-moment` if user energy is reflective; `domain-pick` if restless/in-action. **Never open a values session with Coaching Habit 7Q's generic kickstart** — it surfaces context, not values.
   - **`values` artifact, synthesized at least once** → use **5 Prism's Feelings** to ground, then return to `act-values` `frustration-reveal` or `behavior-test` to check declared vs. lived values.
   - **`values` artifact, user arrives with a declared tension** → use **GROW's Goal** to frame the tension, then `act-values` `direction-not-goal` to translate into movable direction.
   - **Future artifacts (offer, positioning)** → follow each artifact's `artifacts_served` mapping in the frameworks directory.

3. **Ask the opening question directly.** Single sentence, concrete, answerable. Rules:
   - Do NOT describe what you're about to do. Do NOT offer menus of approaches unless the user explicitly asks for options.
   - Do NOT open with wide kickstarts like "what's on your mind" for values sessions — ask a values-clarifying question on turn one.
   - Never paste the whole framework into the chat — a framework is scaffolding for you, not content for the user.
   - Every assistant turn in the session MUST end with a question. No turn is just commentary.

4. **Deepen with values-generating moves.** Based on the answer, pick the next question:
   - **Answer was short (< 30 words)** → `act-values` deepen-tier question (`peak-moment-meaning`, `frustration-reveal`, `no-payoff`) or Coaching Habit's "and what else?".
   - **User named an abstract label** ("freedom", "growth", "honesty") → immediately concretize: `behavior-test`, `free-hour`, or "give me an episode from the last month where that value showed up — or got violated."
   - **Answer revealed emotion without clarity** → switch to 5 Prism (Feelings → Thoughts → Needs).
   - **Answer revealed a conflict, avoidance, or fractal overwhelm** → switch to `gleb-modes` and ask the matching mode question.
   - **User declared a value + an action** → close that thread with `act-values` `direction-not-goal` to verify it's a direction (not a checkable goal) and surface one concrete behavior for the next week.
   - **User reached a decision point** → GROW's Options with the adapted third clause.

5. **Generate content, don't just converse.** The session is valuable only if it produces material the Values artifact can absorb. By exchange 3, you should have at least one concrete episode (not an abstraction) on record. By the close, aim for:
   - 2-4 named candidate values, each with a concrete episode or behavior attached.
   - At least one contradiction or tension between declared and lived values.
   - One direction-not-goal translation for the next week.

6. **Continue for 3-7 exchange cycles.** Don't run a script; respond to what the user actually says. But keep pulling toward concrete episodes and behaviors — if the user drifts into theory, pull back with `behavior-test` or "give me the last time that happened."

7. **Close.** Use either the Coaching Habit's Learning question ("What was most useful?") or, if the user is in generative energy, `additive-subtractive` ("Are we generating or cutting right now?"). Before asking the close question, summarize back to the user the candidate values, episodes, and tensions you heard — so they can correct or confirm. This summary becomes the seed for `groundwork-synthesize`.

8. **Write the session log.** Create `{data_folder}/sessions/{YYYYMMDD}-{HHMM}-{artifact}-deep.md` with frontmatter:

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

9. **Offer to synthesize.** End by asking: *"Want me to roll this into your Values artifact now, or let it sit for a while?"* If yes, invoke `groundwork-synthesize values`. If no, do nothing more — the session log is enough.

## Tiers

- **line**: `"session logged → {path}"`
- **brief**: frameworks used + question slugs asked + where the log is
- **full**: the above + a three-sentence read of what felt alive in the session (your own summary, clearly marked as yours)

## Offering options (limited-list moves)

Whenever you give the user a bounded choice (pick a domain, pick peak-moment vs. domain-pick opener, pick which candidate value to translate into a direction), structure it as a **short enumerated list** — 2-5 options, each one line.

- **If the runtime exposes `AskUserQuestion`** (Claude Code), use it so the user gets a native selector. Provide the question, options list, and a free-form "other" escape when sensible.
- **If the runtime has no structured-question tool** (Hermes, OpenClaw, plain chat, Telegram relay, voice), present the options as a numbered list in plain text and ask the user to reply with the number or a short phrase. Accept either.
- **Never offer more than 5 options at once.** More than that, ask an open question instead.
- **Never offer options as a stall.** Only offer a bounded list when the next move truly branches. Default to asking a real question.

Example — domain pick (works in any runtime):

```
Which domain feels most alive or most uncomfortable right now?
1. work / craft
2. intimate relationship
3. family
4. friendships / community
5. growth / learning
(or name another — body, play, contribution, something else)
```

## Runtime adaptation (agent-friendly)

This skill must run under multiple agents — Claude Code, Hermes, OpenClaw, plain-chat relays, voice. Read `profile.md` `runtime` field and adapt:

- **`runtime: claude-code`** — use `AskUserQuestion` for bounded choices; full file-system I/O available; write session logs directly.
- **`runtime: hermes`** — no `AskUserQuestion`; use numbered-list plain text. File I/O available via Hermes' write tool. If the user's message is voice-transcribed, accept loose matches to option numbers ("the first one", "growth").
- **`runtime: openclaw`** — treat like Hermes: plain-text options, numbered list. If file I/O unavailable, return the session log as a chat message at close and instruct the user where to save it.
- **`runtime: other` / unknown** — degrade to the most conservative mode: plain-text numbered lists, emit session log as a chat-visible code block at close, do not assume any tool beyond read/write files.

Never hard-depend on tools beyond: read file, write file, send/receive message. Everything else is an optional enhancement.

## Failure modes

- Profile missing → stop; tell the user to run `groundwork-intake` first.
- Artifact file missing → stop; tell the user the intake step didn't complete.
- No frameworks loaded for this artifact → stop; tell the user to run `groundwork-framework sync`.
- Runtime blocks file writes → emit the full session log inline at close, with a one-line instruction on the expected path.
- User ends the session before session-goal (1) is reached → write the partial log anyway with `status: incomplete` in frontmatter; skip synthesize offer.
