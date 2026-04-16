---
schema_version: 1
owner: "{{owner_name}}"
data_folder: "{{data_folder_path}}"
mode: hybrid
runtime: claude-code
rhythm:
  daily_anchor_time: null
  weekly_review_day: fri
  monthly_drift_day: 1
  quarterly_direction: true
active_artifacts:
  - values
voice_preferences:
  language_autodetect: true
  tier_default: full
---

# Profile

This file is your groundwork profile. It's read by every skill and edited by the `groundwork-rhythm` and `groundwork-intake` skills.

- **owner** — your name (or handle). Used in artifact footers.
- **data_folder** — the absolute path to this `.groundwork/` directory.
- **mode** — your primary interaction style: `deep` (sessions on demand), `scheduled` (cadence pings), `hybrid` (both), `ambient` (v1.x).
- **runtime** — which agent you're primarily using (`claude-code`, `claude-desktop`, `hermes`, `cursor`, `codex`, `other`).
- **rhythm** — your cadence. Nulls disable the corresponding ping.
- **active_artifacts** — which artifacts you're working on. v1 ships `values`; more in v1.x.
- **voice_preferences** — tier defaults for voice/bot output.

Edit in place or re-run `groundwork-rhythm` to adjust.
