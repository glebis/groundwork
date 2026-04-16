# Groundwork v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a universal skill pack (`groundwork`) distributed via `npx skills` that turns wide coach-shaped questions into a living Values artifact, verified end-to-end in Claude Code and Hermes Agent.

**Architecture:** Skills are markdown files (`SKILL.md`) per subdirectory, following the `npx skills` / Claude Code convention. Frameworks are content (markdown with frontmatter), not code. User state lives in a hidden `.groundwork/` folder at a user-chosen location. Tests are structural (schemas validated with pytest) and behavioral (manual end-to-end checklists per skill, since skills are LLM-executed prompts, not testable unit code).

**Tech Stack:**
- Python 3.11+ with pytest + pyyaml + jsonschema (schema validation)
- Markdown everywhere (skills, frameworks, artifacts, templates)
- Geist Sans/Mono (Google Fonts) + HTML/SVG (visual skills)
- `npx skills` (vercel-labs/skills CLI) as the distribution channel
- Gemini 2.5 Flash Image (nano banana) via existing `scripts/nano-banana.py`
- Runtime targets: Claude Code, Hermes Agent; best-effort in Cursor/Codex/Claude Desktop

**Scope:** v1 ships the **Values** vertical slice only. Audience, Offer, Positioning, Principles, Drift Log are stubs. Voice wrapper and Vercel Chat SDK adapter are deferred to v1.x per the spec.

**Spec reference:** `docs/specs/2026-04-16-groundwork-design.md`

---

## File Structure — what gets created

### Infrastructure
- `.gitignore` — ignore `.DS_Store`, `__pycache__`, test caches, generated visual output
- `LICENSE` — MIT
- `pyproject.toml` — pytest + pyyaml + jsonschema dev deps
- `tests/conftest.py` — shared fixtures
- `tests/test_framework_schema.py` — validates every `docs/frameworks/*.md`
- `tests/test_artifact_schema.py` — validates artifact frontmatter
- `tests/test_profile_schema.py` — validates profile frontmatter
- `tests/test_skill_manifests.py` — validates every `skills/*/SKILL.md` frontmatter
- `tests/fixtures/` — synthetic `.groundwork/` states used by skill walk-throughs
- `scripts/validate.py` — CLI entry for all schema checks (`python scripts/validate.py`)

### Schema definitions
- `docs/schemas/framework.schema.yaml` — framework frontmatter schema (JSON Schema in YAML)
- `docs/schemas/artifact.schema.yaml` — artifact frontmatter schema
- `docs/schemas/profile.schema.yaml` — profile frontmatter schema
- `docs/schemas/skill.schema.yaml` — SKILL.md frontmatter (name, description, etc.)

### Canonical framework library (source of truth — copied into template vault)
- `docs/frameworks/_README.md` — how frameworks work + how to add one
- `docs/frameworks/coaching-habit-7q.md`
- `docs/frameworks/5-prism.md`
- `docs/frameworks/ikigai.md`
- `docs/frameworks/gleb-modes.md`
- `docs/frameworks/grow.md`

### Template vault (shipped; copied to user's chosen location on intake)
- `template-vault/README.md` — user-facing onboarding
- `template-vault/.groundwork/profile.md` — profile + rhythm config, seeded stub
- `template-vault/.groundwork/artifacts/values.md` — seeded stub with frontmatter
- `template-vault/.groundwork/sessions/.gitkeep`
- `template-vault/.groundwork/intake/sources/.gitkeep`
- `template-vault/.groundwork/intake/research-findings.md` — empty skeleton
- `template-vault/.groundwork/frameworks/` — copies of canonical library + user `README.md`
- `template-vault/.groundwork/visuals/brand/brand.md` — copy of shipped brand kit
- `template-vault/.groundwork/visuals/brand/tokens.css` — copy of shipped tokens

### Skills (one SKILL.md per subdir)
- `skills/groundwork-intake/SKILL.md`
- `skills/groundwork-ingest/SKILL.md`
- `skills/groundwork-seed/SKILL.md`
- `skills/groundwork-session/SKILL.md`
- `skills/groundwork-ask/SKILL.md`
- `skills/groundwork-synthesize/SKILL.md`
- `skills/groundwork-review/SKILL.md`
- `skills/groundwork-rhythm/SKILL.md`
- `skills/groundwork-framework/SKILL.md`
- `skills/groundwork-brand/SKILL.md`
- `skills/groundwork-visual-card/SKILL.md`

### Docs
- `docs/runtime-notes.md` — per-runtime quirks found during verification
- `docs/manual-checklist.md` — human walk-through checklist for the Values slice

---

## Phase A — Scaffolding & validation infrastructure

### Task A1: Project scaffolding — .gitignore, LICENSE, pyproject.toml

**Files:**
- Create: `.gitignore`
- Create: `LICENSE`
- Create: `pyproject.toml`

- [ ] **Step 1: Write `.gitignore`**

```
# editor / OS
.DS_Store
.vscode/
.idea/

# python
__pycache__/
*.py[cod]
.pytest_cache/
.ruff_cache/
*.egg-info/

# brand visual output (user-generated)
docs/brand/samples/ai/*.png
!docs/brand/samples/ai/.gitkeep
docs/brand/samples/ai/*.prompt.txt
!docs/brand/samples/ai/.gitkeep

# secrets
.env
.env.*
!.env.example
```

Wait — the nano banana images that are already committed should stay. Adjust:

```
# editor / OS
.DS_Store
.vscode/
.idea/

# python
__pycache__/
*.py[cod]
.pytest_cache/
.ruff_cache/
*.egg-info/

# secrets
.env
.env.*
!.env.example
```

- [ ] **Step 2: Write `LICENSE` (MIT)**

```
MIT License

Copyright (c) 2026 Gleb Kalinin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 3: Write `pyproject.toml`**

```toml
[project]
name = "groundwork-tools"
version = "0.1.0"
description = "Validation tooling for the groundwork skill pack"
requires-python = ">=3.11"

[project.optional-dependencies]
dev = [
  "pytest>=8.0",
  "pyyaml>=6.0",
  "jsonschema>=4.21",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "-v"
```

- [ ] **Step 4: Install dev deps and verify**

```bash
cd ~/ai_projects/groundwork
pip install -e '.[dev]'
pytest --version
```

Expected: pytest 8.x shown.

- [ ] **Step 5: Commit**

```bash
git add .gitignore LICENSE pyproject.toml
git commit -m "scaffold: add gitignore, MIT license, pyproject with pytest toolchain"
```

---

### Task A2: Framework schema + validator + failing test

**Files:**
- Create: `docs/schemas/framework.schema.yaml`
- Create: `scripts/validate.py`
- Create: `tests/test_framework_schema.py`
- Create: `tests/conftest.py`

- [ ] **Step 1: Write the failing test**

Create `tests/conftest.py`:

```python
import pathlib
import pytest

REPO_ROOT = pathlib.Path(__file__).parent.parent


@pytest.fixture
def repo_root() -> pathlib.Path:
    return REPO_ROOT


@pytest.fixture
def frameworks_dir(repo_root) -> pathlib.Path:
    return repo_root / "docs" / "frameworks"
```

Create `tests/test_framework_schema.py`:

```python
import pathlib
import pytest
import yaml
from jsonschema import validate, ValidationError

SCHEMA_PATH = pathlib.Path(__file__).parent.parent / "docs" / "schemas" / "framework.schema.yaml"


def _load_schema():
    return yaml.safe_load(SCHEMA_PATH.read_text())


def _split_frontmatter(text: str) -> dict:
    if not text.startswith("---\n"):
        raise ValueError("no frontmatter delimiter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("no closing frontmatter delimiter")
    return yaml.safe_load(text[4:end])


def test_schema_file_exists():
    assert SCHEMA_PATH.exists(), f"missing {SCHEMA_PATH}"


def test_schema_is_valid_yaml():
    _load_schema()  # raises on bad yaml


def test_framework_files_validate(frameworks_dir):
    schema = _load_schema()
    files = [p for p in frameworks_dir.glob("*.md") if not p.name.startswith("_")]
    assert files, f"no framework files in {frameworks_dir}"
    for f in files:
        data = _split_frontmatter(f.read_text())
        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            pytest.fail(f"{f.name}: {e.message}")
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_framework_schema.py -v
```

Expected: FAIL — `docs/schemas/framework.schema.yaml` does not exist.

- [ ] **Step 3: Write the schema**

Create `docs/schemas/framework.schema.yaml`:

```yaml
$schema: "https://json-schema.org/draft/2020-12/schema"
title: Framework
type: object
required: [name, slug, purpose, when_to_use, artifacts_served, questions]
additionalProperties: true
properties:
  name:
    type: string
    minLength: 1
  slug:
    type: string
    pattern: "^[a-z0-9-]+$"
  purpose:
    type: string
    minLength: 1
  when_to_use:
    type: array
    items:
      type: string
      enum:
        - early-values-work
        - mid-session-pivot
        - daily-anchor
        - weekly-review
        - monthly-drift
        - quarterly-direction
        - audience-work
        - offer-work
        - positioning-work
    minItems: 1
  artifacts_served:
    type: array
    items:
      type: string
      enum: [values, self-map, audience, offer, positioning, principles, drift-log]
    minItems: 1
  source:
    type: string
  questions:
    type: array
    minItems: 1
    items:
      type: object
      required: [slug, text, tier]
      additionalProperties: false
      properties:
        slug:
          type: string
          pattern: "^[a-z0-9-]+$"
        text:
          type: string
          minLength: 1
        tier:
          type: string
          enum: [wide, deepen, focus, close]
```

- [ ] **Step 4: Run test — still fails because no framework files exist yet**

```bash
pytest tests/test_framework_schema.py -v
```

Expected: FAIL at `test_framework_files_validate` — "no framework files in …". This is expected; the next phase adds them. Mark the first two assertions as passing:

```bash
pytest tests/test_framework_schema.py::test_schema_file_exists tests/test_framework_schema.py::test_schema_is_valid_yaml -v
```

Expected: both PASS.

- [ ] **Step 5: Write the validator CLI**

Create `scripts/validate.py`:

```python
#!/usr/bin/env python3
"""Run all schema validations. Exit non-zero on first failure."""
import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).parent.parent


def main() -> int:
    result = subprocess.run(["pytest", str(REPO / "tests"), "-q"], cwd=REPO)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 6: Commit**

```bash
git add docs/schemas/framework.schema.yaml scripts/validate.py tests/conftest.py tests/test_framework_schema.py
git commit -m "test: add framework frontmatter schema + validator"
```

---

### Task A3: Artifact schema + test

**Files:**
- Create: `docs/schemas/artifact.schema.yaml`
- Create: `tests/test_artifact_schema.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_artifact_schema.py`:

```python
import pathlib
import pytest
import yaml
from jsonschema import validate, ValidationError

REPO = pathlib.Path(__file__).parent.parent
SCHEMA_PATH = REPO / "docs" / "schemas" / "artifact.schema.yaml"
TEMPLATE_ARTIFACTS = REPO / "template-vault" / ".groundwork" / "artifacts"


def _load_schema():
    return yaml.safe_load(SCHEMA_PATH.read_text())


def _split_frontmatter(text: str) -> dict:
    assert text.startswith("---\n")
    end = text.find("\n---\n", 4)
    assert end != -1
    return yaml.safe_load(text[4:end])


def test_schema_exists():
    assert SCHEMA_PATH.exists()


def test_all_template_artifacts_validate():
    schema = _load_schema()
    files = list(TEMPLATE_ARTIFACTS.glob("*.md"))
    assert files, f"no artifacts in {TEMPLATE_ARTIFACTS}"
    for f in files:
        data = _split_frontmatter(f.read_text())
        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            pytest.fail(f"{f.name}: {e.message}")
```

- [ ] **Step 2: Run test — fails (no schema)**

```bash
pytest tests/test_artifact_schema.py -v
```

Expected: FAIL.

- [ ] **Step 3: Write the schema**

Create `docs/schemas/artifact.schema.yaml`:

```yaml
$schema: "https://json-schema.org/draft/2020-12/schema"
title: Artifact
type: object
required: [artifact_type, schema_version, owner]
additionalProperties: true
properties:
  artifact_type:
    type: string
    enum: [values, self-map, audience, offer, positioning, principles, drift-log]
  schema_version:
    type: integer
    minimum: 1
  last_synthesized:
    type: string
    description: ISO-8601 timestamp; absent if never synthesized
  source_sessions:
    type: array
    items:
      type: string
      pattern: "^[0-9]{8}(-[0-9]{4})?$"
  speakable_summary:
    type: string
    maxLength: 400
  owner:
    type: string
    minLength: 1
  status:
    type: string
    enum: [seeded, drafting, active, archived]
```

- [ ] **Step 4: Run — first assertion passes, second still fails (no template artifacts yet)**

```bash
pytest tests/test_artifact_schema.py::test_schema_exists -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add docs/schemas/artifact.schema.yaml tests/test_artifact_schema.py
git commit -m "test: add artifact frontmatter schema"
```

---

### Task A4: Profile schema + test

**Files:**
- Create: `docs/schemas/profile.schema.yaml`
- Create: `tests/test_profile_schema.py`

- [ ] **Step 1: Write the test**

Create `tests/test_profile_schema.py`:

```python
import pathlib
import pytest
import yaml
from jsonschema import validate, ValidationError

REPO = pathlib.Path(__file__).parent.parent
SCHEMA_PATH = REPO / "docs" / "schemas" / "profile.schema.yaml"
TEMPLATE_PROFILE = REPO / "template-vault" / ".groundwork" / "profile.md"


def _split_frontmatter(text: str) -> dict:
    assert text.startswith("---\n")
    end = text.find("\n---\n", 4)
    assert end != -1
    return yaml.safe_load(text[4:end])


def test_schema_exists():
    assert SCHEMA_PATH.exists()


def test_template_profile_validates():
    schema = yaml.safe_load(SCHEMA_PATH.read_text())
    data = _split_frontmatter(TEMPLATE_PROFILE.read_text())
    try:
        validate(instance=data, schema=schema)
    except ValidationError as e:
        pytest.fail(f"profile: {e.message}")
```

- [ ] **Step 2: Run — fails**

```bash
pytest tests/test_profile_schema.py -v
```

Expected: FAIL.

- [ ] **Step 3: Write the schema**

Create `docs/schemas/profile.schema.yaml`:

```yaml
$schema: "https://json-schema.org/draft/2020-12/schema"
title: Profile
type: object
required: [schema_version, owner, data_folder, mode, runtime]
additionalProperties: true
properties:
  schema_version:
    type: integer
    minimum: 1
  owner:
    type: string
    minLength: 1
  data_folder:
    type: string
    description: Absolute or ~-prefixed path to the .groundwork/ directory
  mode:
    type: string
    enum: [deep, scheduled, hybrid, ambient]
  runtime:
    type: string
    enum: [claude-code, claude-desktop, hermes, cursor, codex, other]
  rhythm:
    type: object
    additionalProperties: false
    properties:
      daily_anchor_time:
        type: [string, "null"]
        description: HH:MM local time for daily ping; null disables
      weekly_review_day:
        type: [string, "null"]
        enum: [mon, tue, wed, thu, fri, sat, sun, null]
      monthly_drift_day:
        type: [integer, "null"]
        minimum: 1
        maximum: 28
      quarterly_direction:
        type: boolean
  active_artifacts:
    type: array
    items:
      type: string
      enum: [values, self-map, audience, offer, positioning, principles, drift-log]
  voice_preferences:
    type: object
    additionalProperties: true
    properties:
      language_autodetect:
        type: boolean
      tier_default:
        type: string
        enum: [line, brief, full]
```

- [ ] **Step 4: Commit**

```bash
git add docs/schemas/profile.schema.yaml tests/test_profile_schema.py
git commit -m "test: add profile frontmatter schema"
```

---

### Task A5: Skill manifest schema + test

**Files:**
- Create: `docs/schemas/skill.schema.yaml`
- Create: `tests/test_skill_manifests.py`

- [ ] **Step 1: Write the test**

Create `tests/test_skill_manifests.py`:

```python
import pathlib
import pytest
import yaml
from jsonschema import validate, ValidationError

REPO = pathlib.Path(__file__).parent.parent
SCHEMA_PATH = REPO / "docs" / "schemas" / "skill.schema.yaml"
SKILLS_DIR = REPO / "skills"


def _split_frontmatter(text: str) -> dict:
    assert text.startswith("---\n")
    end = text.find("\n---\n", 4)
    assert end != -1
    return yaml.safe_load(text[4:end])


def test_schema_exists():
    assert SCHEMA_PATH.exists()


def test_every_skill_has_manifest():
    schema = yaml.safe_load(SCHEMA_PATH.read_text())
    skills = [d for d in SKILLS_DIR.iterdir() if d.is_dir()] if SKILLS_DIR.exists() else []
    assert skills, f"no skills in {SKILLS_DIR}"
    for skill in skills:
        manifest = skill / "SKILL.md"
        assert manifest.exists(), f"{skill.name}: missing SKILL.md"
        data = _split_frontmatter(manifest.read_text())
        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            pytest.fail(f"{skill.name}: {e.message}")
```

- [ ] **Step 2: Run — fails**

```bash
pytest tests/test_skill_manifests.py -v
```

Expected: FAIL — schema missing.

- [ ] **Step 3: Write the schema**

Create `docs/schemas/skill.schema.yaml`:

```yaml
$schema: "https://json-schema.org/draft/2020-12/schema"
title: SkillManifest
type: object
required: [name, description]
additionalProperties: true
properties:
  name:
    type: string
    pattern: "^[a-z0-9-]+$"
    minLength: 3
    maxLength: 64
  description:
    type: string
    minLength: 10
    maxLength: 300
  io_contract:
    type: object
    additionalProperties: false
    properties:
      reads:
        type: array
        items: { type: string }
      writes:
        type: array
        items: { type: string }
      returns:
        type: string
  modes:
    type: array
    items:
      type: string
      enum: [interactive, headless]
  tiers:
    type: array
    items:
      type: string
      enum: [line, brief, full]
```

- [ ] **Step 4: Commit**

```bash
git add docs/schemas/skill.schema.yaml tests/test_skill_manifests.py
git commit -m "test: add SKILL.md manifest schema"
```

---

## Phase B — Framework library

Every framework file in this phase follows the `framework.schema.yaml` contract validated in Task A2.

### Task B1: Framework library README + _README.md

**Files:**
- Create: `docs/frameworks/_README.md`

- [ ] **Step 1: Write `_README.md`**

```markdown
# Frameworks

Frameworks are named inquiry tools. Each framework is a markdown file with:

- **frontmatter** conforming to `docs/schemas/framework.schema.yaml` (validated in tests)
- a **narrative body** describing the framework, when to use it, adaptation notes

The frontmatter's `questions` list is the atomic coaching unit — each question has a `tier` (wide / deepen / focus / close) and a `slug` used for reference in session logs.

## Adding a framework

1. Copy an existing framework file (e.g. `coaching-habit-7q.md`) and rename.
2. Edit the frontmatter: new `name`, new `slug`, new `purpose`, correct `when_to_use`, `artifacts_served`, and `questions`.
3. Run `python scripts/validate.py` — your file must validate.
4. Commit.

No code change needed. Frameworks are content, by design.

## Seed set (v1)

- `coaching-habit-7q.md` — Michael Bungay Stanier, 7 questions
- `5-prism.md` — Rybina & Muradyan, five surfaces of experience
- `ikigai.md` — four-intersection values/meaning framework
- `gleb-modes.md` — project-specific vocabulary (fractal overwhelm, drift, avoidance pattern…)
- `grow.md` — Goal / Reality / Options / Will
```

- [ ] **Step 2: Commit**

```bash
git add docs/frameworks/_README.md
git commit -m "docs: add frameworks library README"
```

---

### Task B2: Coaching Habit 7Q

**Files:**
- Create: `docs/frameworks/coaching-habit-7q.md`

- [ ] **Step 1: Write the framework**

```markdown
---
name: Coaching Habit 7Q
slug: coaching-habit-7q
purpose: Surface what a person actually wants, cares about, avoids, or is learning, using seven short, wide questions
when_to_use:
  - early-values-work
  - mid-session-pivot
  - weekly-review
artifacts_served: [values, self-map, drift-log]
source: "Michael Bungay Stanier, The Coaching Habit (2016)"
questions:
  - slug: kickstart
    text: "What's on your mind?"
    tier: wide
  - slug: awe
    text: "And what else?"
    tier: deepen
  - slug: focus
    text: "What's the real challenge here for you?"
    tier: focus
  - slug: foundation
    text: "What do you want?"
    tier: focus
  - slug: lazy
    text: "How can I help?"
    tier: close
  - slug: strategic
    text: "If you're saying yes to this, what are you saying no to?"
    tier: focus
  - slug: learning
    text: "What was most useful for you?"
    tier: close
---

# Coaching Habit 7Q

Seven wide questions that unlock conversations about what actually matters. The power is in their brevity: each is a single sentence, speakable in a breath, open enough to pull the person into their own answer rather than agreement with yours.

## When to use

- **early-values-work** — the Kickstart question ("What's on your mind?") is a good first touch when a user is intake-fresh and hasn't narrowed yet.
- **mid-session-pivot** — if a session is spinning, "And what else?" surfaces the thing that wasn't said.
- **weekly-review** — the Strategic and Learning questions close a week cleanly.

## Adaptation

The Lazy question ("How can I help?") is Stanier's anti-default — asked only after genuine listening. In groundwork, reserve `lazy` for the last beat of a deep session; never use it as a filler.

The Strategic question ("What are you saying no to?") is the closest to the drift check — it exposes hidden trade-offs. When a user answers with a long list, that's signal for `gleb-modes` → `additive-subtractive`.

## References

- Stanier, M. B. (2016). *The Coaching Habit*. Box of Crayons Press.
```

- [ ] **Step 2: Run framework schema test**

```bash
pytest tests/test_framework_schema.py -v
```

Expected: `test_framework_files_validate` PASSES for this file (others may still be missing — but if this file is the only one, the test should pass).

- [ ] **Step 3: Commit**

```bash
git add docs/frameworks/coaching-habit-7q.md
git commit -m "feat(frameworks): add Coaching Habit 7Q"
```

---

### Task B3: 5 Prism Model

**Files:**
- Create: `docs/frameworks/5-prism.md`

- [ ] **Step 1: Write the framework**

```markdown
---
name: 5 Prism Model
slug: 5-prism
purpose: Map a single situation across five surfaces — feelings, thoughts, paradoxes, conflicts, needs — to reach a fuller ground before action
when_to_use:
  - early-values-work
  - mid-session-pivot
  - monthly-drift
artifacts_served: [values, self-map, drift-log]
source: "Rybina & Muradyan, coaching prism model"
questions:
  - slug: feelings
    text: "What are you feeling right now as you hold this?"
    tier: wide
  - slug: thoughts
    text: "What thoughts keep circling?"
    tier: deepen
  - slug: paradoxes
    text: "Where are you holding two truths at once?"
    tier: deepen
  - slug: conflicts
    text: "Who or what is this in tension with?"
    tier: focus
  - slug: needs
    text: "Underneath this, what do you need?"
    tier: focus
---

# 5 Prism Model

Five lenses for one situation. Each surfaces a different layer — feelings, thoughts, paradoxes, conflicts, needs. Walking all five slows a user enough to let the actual ground show up before they move to decide.

## When to use

- **early-values-work** — a situation or decision the user keeps returning to often reveals a value through paradox or need.
- **mid-session-pivot** — when a user is stuck in thoughts only, shift to feelings or needs.
- **monthly-drift** — the Paradoxes question ("holding two truths at once") is the sharpest drift detector.

## Adaptation

For ADHD/fast-processing users, collapse to three lenses: feelings → paradoxes → needs. Paradox is the load-bearing one; the others orbit it.

When Paradox produces "both / and" statements, that's usually a values-dyad worth naming explicitly (e.g. "I value speed AND I value craft" → both go in the Values artifact).
```

- [ ] **Step 2: Validate**

```bash
pytest tests/test_framework_schema.py -v
```

Expected: PASS for both framework files.

- [ ] **Step 3: Commit**

```bash
git add docs/frameworks/5-prism.md
git commit -m "feat(frameworks): add 5 Prism model"
```

---

### Task B4: Ikigai

**Files:**
- Create: `docs/frameworks/ikigai.md`

- [ ] **Step 1: Write the framework**

```markdown
---
name: Ikigai
slug: ikigai
purpose: Four-intersection model — what you love, what you're good at, what the world needs, what you can be paid for — for values and offer alignment
when_to_use:
  - early-values-work
  - offer-work
  - quarterly-direction
artifacts_served: [values, offer, positioning]
source: "Japanese concept; popularized in the West via García & Miralles, Ikigai (2016)"
questions:
  - slug: love
    text: "What do you still do even when no one is watching?"
    tier: wide
  - slug: good-at
    text: "What comes easier to you than to most people around you?"
    tier: deepen
  - slug: world-needs
    text: "Where have you seen this world specifically need what you do?"
    tier: focus
  - slug: paid-for
    text: "What have people already paid you for — even once?"
    tier: focus
  - slug: intersection
    text: "Where do two or more of these overlap today?"
    tier: close
---

# Ikigai

Four circles: what you love, what you're good at, what the world needs, what you can be paid for. The intersection is a small zone, and usually only two or three circles overlap at a time. Groundwork uses Ikigai to triangulate between values (love, good-at) and offer/positioning (world-needs, paid-for).

## When to use

- **early-values-work** — the Love and Good-at questions surface values via behavior rather than declaration. Useful for users who freeze at "what are your values" but can answer "what do you do when no one is watching."
- **offer-work** — the full four-circle pass, weighted toward the right half (world-needs, paid-for), seeds the Offer artifact.
- **quarterly-direction** — re-running Ikigai quarterly reveals drift: the overlaps shift as a user grows.

## Adaptation

Ikigai as originally framed assumes a single overlap zone. In practice people carry multiple partial overlaps at any time — that's fine. Don't push a user to collapse to one. Record the overlaps as-is and let the Values + Offer artifacts hold the plurality.
```

- [ ] **Step 2: Validate + commit**

```bash
pytest tests/test_framework_schema.py -v
git add docs/frameworks/ikigai.md
git commit -m "feat(frameworks): add Ikigai"
```

---

### Task B5: Gleb's modes (project-specific vocabulary)

**Files:**
- Create: `docs/frameworks/gleb-modes.md`

- [ ] **Step 1: Write the framework**

```markdown
---
name: Modes (Gleb's Lexicon)
slug: gleb-modes
purpose: Project-specific vocabulary — named states and tendencies that let a user notice themselves faster mid-session
when_to_use:
  - mid-session-pivot
  - weekly-review
  - monthly-drift
artifacts_served: [values, self-map, drift-log, principles]
source: "Gleb Kalinin's LEXICON.md, distilled over 2024-2026"
questions:
  - slug: fractal-overwhelm
    text: "Are you holding the whole tree right now when you only need three anchors?"
    tier: focus
  - slug: drift
    text: "Compare what you've actually done this week to what you intended. Where did attention quietly diverge?"
    tier: focus
  - slug: salience
    text: "Of everything on your mind, what actually deserves the next hour — not what's loudest, what's most real?"
    tier: focus
  - slug: avoidance-pattern
    text: "What are you reorganizing right now that looks like work but isn't the work?"
    tier: focus
  - slug: additive-subtractive
    text: "Are you currently generating or cutting? Which does this moment need?"
    tier: deepen
  - slug: inside-out
    text: "Before you work on the edge, what's the core? Have you named it?"
    tier: wide
  - slug: context-diet
    text: "What could you stop reading, watching, or thinking about this week to hear yourself?"
    tier: focus
  - slug: base-layer
    text: "Before anything else: sleep, food, movement, people, body. Which is off?"
    tier: wide
---

# Modes

Eight named states, each a tool for self-observation. The power is in the naming: once a user can say *"I'm in fractal overwhelm"* or *"that's my avoidance pattern"*, the state is partially out of them and on the table.

Unlike the borrowed frameworks (7Q, Ikigai, 5 Prism), these are **project-coined** — Gleb's lexicon distilled over years of practice. They sit in groundwork as an invitation: any user can adopt them, adapt them, or replace them with their own named modes as the system grows.

## When to use

- **mid-session-pivot** — any mode question can break a stuck loop, especially `avoidance-pattern` and `fractal-overwhelm`.
- **weekly-review** — `drift` and `salience` are the closing pair.
- **monthly-drift** — run `drift`, then `inside-out`, then `base-layer`. The triplet re-anchors.

## Adaptation

Modes are a *starting* vocabulary, not a required one. Encourage users to name their own modes over time — when a user coins a phrase that captures a recurring state ("the 9pm compress," "sprint-then-silence"), add it to their local `gleb-modes.md` copy. Personal modes carry more weight than borrowed ones.

## The eight

- **fractal overwhelm** — holding the entire branching tree when three anchors would do. Compress.
- **drift** — gradual divergence between intention and attention. Inverse of salience.
- **salience** — what deserves attention, not what demands it.
- **avoidance pattern** — habitual deflection disguised as productivity.
- **additive–subtractive** — two phases, never both at once. Generate freely, cut ruthlessly.
- **inside-out** — start from the core, not the edge. Domain → thesis → principles → execution.
- **context diet** — intentional reduction of information intake.
- **base layer** — non-negotiables. Attention depends on them.
```

- [ ] **Step 2: Validate + commit**

```bash
pytest tests/test_framework_schema.py -v
git add docs/frameworks/gleb-modes.md
git commit -m "feat(frameworks): add Gleb's modes"
```

---

### Task B6: GROW

**Files:**
- Create: `docs/frameworks/grow.md`

- [ ] **Step 1: Write the framework**

```markdown
---
name: GROW
slug: grow
purpose: Four-step structure for a single conversation — Goal, Reality, Options, Will — when a user arrives with a decision to make
when_to_use:
  - early-values-work
  - mid-session-pivot
  - weekly-review
artifacts_served: [values, self-map]
source: "John Whitmore, Coaching for Performance (1992)"
questions:
  - slug: goal
    text: "What do you want to walk out of this session with?"
    tier: wide
  - slug: reality
    text: "Where are you actually, right now, with this?"
    tier: deepen
  - slug: options
    text: "What could you do — including the obvious, the uncomfortable, and the one you'd rather not name?"
    tier: focus
  - slug: will
    text: "Of those, which will you actually do, and by when?"
    tier: close
---

# GROW

A four-beat structure for sessions when a user arrives with a decision on the table. Start with the desired outcome (Goal), ground in current state (Reality), widen the set (Options — the third question prompts for the hidden option), narrow to commitment (Will).

## When to use

- **early-values-work** — GROW is less values-surfacing than 5 Prism or 7Q, but the Goal question often reveals an underlying value ("I want to walk out with clarity on X" → what does clarity mean to you here?).
- **mid-session-pivot** — when a session is spinning, "Where are you actually, right now?" (Reality) re-anchors.
- **weekly-review** — Will → the commitment statement for next week is a clean weekly closer.

## Adaptation

The Options question has a third clause deliberately: "the one you'd rather not name." This is the groundwork adaptation — vanilla GROW asks "what are the options?" which tends to surface the already-known two or three. The expanded phrasing reliably unearths a fourth option the user has been avoiding.
```

- [ ] **Step 2: Validate + commit**

```bash
pytest tests/test_framework_schema.py -v
git add docs/frameworks/grow.md
git commit -m "feat(frameworks): add GROW with adapted Options prompt"
```

---

## Phase C — Template vault

### Task C1: Profile template

**Files:**
- Create: `template-vault/.groundwork/profile.md`

- [ ] **Step 1: Write the profile template**

```markdown
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
- **mode** — your primary interaction style: `deep` (sessions on demand), `scheduled` (cadence pings), `hybrid` (both), `ambient` (listening during normal chat — v1.x only).
- **runtime** — which agent you're primarily using (`claude-code`, `claude-desktop`, `hermes`, `cursor`, `codex`, `other`). Affects how scheduled tasks dispatch.
- **rhythm** — your cadence. Nulls disable the corresponding ping.
- **active_artifacts** — which artifacts you're working on. v1 ships `values`; more come in v1.x.
- **voice_preferences** — tier defaults for voice/bot output.

Edit in-place or re-run `groundwork-rhythm` to adjust.
```

- [ ] **Step 2: Run profile schema test — should pass (but `{{owner_name}}` etc. are placeholders; the schema doesn't require them to be non-placeholder, just to be strings)**

```bash
pytest tests/test_profile_schema.py -v
```

Expected: PASS.

- [ ] **Step 3: Commit**

```bash
git add template-vault/.groundwork/profile.md
git commit -m "feat(template): add profile template with schema-valid frontmatter"
```

---

### Task C2: Values artifact template (seeded stub)

**Files:**
- Create: `template-vault/.groundwork/artifacts/values.md`

- [ ] **Step 1: Write the template**

```markdown
---
artifact_type: values
schema_version: 1
owner: "{{owner_name}}"
status: seeded
speakable_summary: "Values seeded but not yet synthesized. Run groundwork-session on values to begin."
---

# Values

*This artifact is seeded but not yet distilled. Run `groundwork-session values` to begin the first session, or `groundwork-ingest` + `groundwork-seed` to bootstrap from material you've already produced.*

## Candidate values

*(empty — populated by sessions or seeding)*

## Recent reflections

*(empty — populated by synthesize)*

## Changelog

*(empty)*
```

- [ ] **Step 2: Run artifact schema test**

```bash
pytest tests/test_artifact_schema.py -v
```

Expected: PASS.

- [ ] **Step 3: Commit**

```bash
git add template-vault/.groundwork/artifacts/values.md
git commit -m "feat(template): add values artifact seeded stub"
```

---

### Task C3: Session, intake, frameworks, visuals directories

**Files:**
- Create: `template-vault/.groundwork/sessions/.gitkeep`
- Create: `template-vault/.groundwork/intake/sources/.gitkeep`
- Create: `template-vault/.groundwork/intake/inbox/.gitkeep`
- Create: `template-vault/.groundwork/intake/research-findings.md`
- Create: `template-vault/.groundwork/frameworks/README.md`
- Create: `template-vault/README.md`

- [ ] **Step 1: Write `.gitkeep` placeholders**

```bash
cd ~/ai_projects/groundwork
mkdir -p template-vault/.groundwork/{sessions,intake/sources,intake/inbox,frameworks}
touch template-vault/.groundwork/sessions/.gitkeep
touch template-vault/.groundwork/intake/sources/.gitkeep
touch template-vault/.groundwork/intake/inbox/.gitkeep
```

- [ ] **Step 2: Write `research-findings.md` skeleton**

Create `template-vault/.groundwork/intake/research-findings.md`:

```markdown
# Research findings

*This file is populated by `groundwork-ingest` from material at `intake/sources/` and `intake/inbox/`. Sections below stay in fixed order so downstream skills (`seed`, `synthesize`) can parse reliably.*

## Declared values

*(direct statements by the user, with source citations)*

## Implied values

*(patterns observed across material)*

## Recurring themes

*(ideas that appear repeatedly)*

## Framings

*(how the user positions their work)*

## Audience signals

*(who the user talks to / for)*

## Voice samples

*(quotes with strong voice, for tone calibration during synthesis)*

## Contradictions and tensions

*(interesting misalignments worth sitting with)*

## Sources

*(an ingest run appends entries here: path, title, date, medium)*
```

- [ ] **Step 3: Write `frameworks/README.md`**

```markdown
# Your frameworks

This folder is your local, editable copy of the groundwork framework library. Add, remove, or rewrite any of these — they're yours.

Each framework is a markdown file with frontmatter describing when it applies and what questions it contains. To add a new one, copy any existing file, edit it, and run `groundwork-framework validate` to confirm it's well-formed.

The seed set:

- `coaching-habit-7q.md`
- `5-prism.md`
- `ikigai.md`
- `gleb-modes.md`
- `grow.md`
```

- [ ] **Step 4: Write `template-vault/README.md` (onboarding for audience C)**

```markdown
# your groundwork

This is where groundwork keeps your state. Everything here is yours; edit any of it by hand at any time.

## layout

```
.groundwork/
├── profile.md              you, your cadence, your runtime
├── artifacts/
│   └── values.md           the first living document
├── sessions/               raw session logs (append-only)
├── intake/
│   ├── sources/            material you've ingested
│   ├── inbox/              drop-folder for forwarded bot content
│   └── research-findings.md distilled reading of your material
├── frameworks/             your local coaching library
└── visuals/
    └── brand/              your brand kit (editable)
```

## quickstart

1. Run `groundwork-intake` to fill in your profile.
2. (Optional) Run `groundwork-ingest <url-or-path>` to load material you've produced.
3. Run `groundwork-session values` for your first deep session.
4. Run `groundwork-synthesize values` to distill sessions into the artifact.
5. Run `groundwork-visual-card values` to render a shareable card.

## principles

- append-only sessions — nothing you say here gets overwritten
- edit artifacts by hand any time; synthesize merges, never overwrites blindly
- your frameworks are yours — customize, rename, add your own

Questions? `groundwork-framework list` shows what's loaded; `groundwork-rhythm` edits your cadence.
```

- [ ] **Step 5: Commit**

```bash
git add template-vault/
git commit -m "feat(template): add directory scaffold, research-findings skeleton, onboarding README"
```

---

### Task C4: Copy canonical frameworks into template vault

**Files:**
- Copy: `docs/frameworks/*.md` → `template-vault/.groundwork/frameworks/`

- [ ] **Step 1: Write a helper script and copy**

Create `scripts/sync-frameworks.sh`:

```bash
#!/usr/bin/env bash
# Copy canonical frameworks into the template vault.
# Invoked during build and whenever docs/frameworks/ changes.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
cp "$REPO"/docs/frameworks/*.md "$REPO"/template-vault/.groundwork/frameworks/
# Do not copy the _README — the template has its own.
rm -f "$REPO"/template-vault/.groundwork/frameworks/_README.md
echo "synced canonical frameworks into template vault"
```

- [ ] **Step 2: Make executable and run**

```bash
chmod +x scripts/sync-frameworks.sh
scripts/sync-frameworks.sh
ls template-vault/.groundwork/frameworks/
```

Expected output: `5-prism.md coaching-habit-7q.md grow.md gleb-modes.md ikigai.md README.md`

- [ ] **Step 3: Re-run framework schema test on template copies**

Add to `tests/test_framework_schema.py`:

```python
def test_template_frameworks_validate(repo_root):
    schema = _load_schema()
    template_dir = repo_root / "template-vault" / ".groundwork" / "frameworks"
    files = [p for p in template_dir.glob("*.md") if p.name != "README.md"]
    assert files, f"no frameworks in {template_dir}"
    for f in files:
        data = _split_frontmatter(f.read_text())
        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            pytest.fail(f"template/{f.name}: {e.message}")
```

- [ ] **Step 4: Run**

```bash
pytest tests/test_framework_schema.py -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/sync-frameworks.sh template-vault/.groundwork/frameworks/ tests/test_framework_schema.py
git commit -m "feat(template): sync canonical frameworks into template vault + test"
```

---

### Task C5: Brand kit in template vault

**Files:**
- Copy: `docs/brand/brand.md` → `template-vault/.groundwork/visuals/brand/brand.md`
- Copy: `docs/brand/tokens.css` → `template-vault/.groundwork/visuals/brand/tokens.css`

- [ ] **Step 1: Copy brand kit into template**

```bash
mkdir -p template-vault/.groundwork/visuals/brand
cp docs/brand/brand.md template-vault/.groundwork/visuals/brand/
cp docs/brand/tokens.css template-vault/.groundwork/visuals/brand/
```

- [ ] **Step 2: Commit**

```bash
git add template-vault/.groundwork/visuals/brand/
git commit -m "feat(template): ship brand kit inside template vault"
```

---

## Phase D — Spine skills

Each skill is a markdown file with YAML frontmatter matching `skill.schema.yaml` and a prose body that an LLM agent will interpret. Skills are **not** code — so tests are:
1. Schema validation (frontmatter structure), enforced by `tests/test_skill_manifests.py`
2. Manual end-to-end walk-through per skill, captured as a checklist in `docs/manual-checklist.md` and filled in during Phase G

Each task in this phase: write the SKILL.md, run the manifest test, commit. The body prose is detailed and concrete — no placeholders.

### Task D1: groundwork-intake

**Files:**
- Create: `skills/groundwork-intake/SKILL.md`

- [ ] **Step 1: Write the skill**

```markdown
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

1. **Detect runtime.** Check for environment signals (`CLAUDECODE`, `HERMES_SESSION`, presence of `.cursor/`) and record the answer. If ambiguous, ask.

2. **Ask for identity.** One question: *"What name should appear on your artifacts? (a handle is fine)"* — this becomes `owner`.

3. **Ask for data-folder location.** Propose in order of preference:
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
```

- [ ] **Step 2: Run manifest test**

```bash
pytest tests/test_skill_manifests.py -v
```

Expected: PASS for `groundwork-intake`.

- [ ] **Step 3: Commit**

```bash
git add skills/groundwork-intake/SKILL.md
git commit -m "feat(skill): groundwork-intake — first-run profile setup"
```

---

### Task D2: groundwork-session

**Files:**
- Create: `skills/groundwork-session/SKILL.md`

- [ ] **Step 1: Write the skill**

```markdown
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
```

- [ ] **Step 2: Run manifest test + commit**

```bash
pytest tests/test_skill_manifests.py -v
git add skills/groundwork-session/SKILL.md
git commit -m "feat(skill): groundwork-session — deep dialog on an artifact"
```

---

### Task D3: groundwork-ask

**Files:**
- Create: `skills/groundwork-ask/SKILL.md`

- [ ] **Step 1: Write the skill**

```markdown
---
name: groundwork-ask
description: Pose a single wide question tied to an artifact and append the answer to a session log. Used by scheduled pings and ambient mode. Short interaction.
io_contract:
  reads:
    - "{data_folder}/profile.md"
    - "{data_folder}/frameworks/*.md"
    - "{data_folder}/artifacts/{artifact}.md"
    - "{data_folder}/sessions/*.md"
  writes:
    - "{data_folder}/sessions/{YYYYMMDD}-{HHMM}-{artifact}-ask.md"
  returns: "path to the new session file"
modes: [interactive, headless]
tiers: [line, brief, full]
---

# groundwork-ask

Single-question interaction. Used by scheduled pings ("daily anchor," "weekly review") and by ambient mode. Collects one short answer and logs it.

## When to use

- A scheduler (Hermes cron, Claude Code `schedule`) invoked you with a cadence reason.
- The user explicitly wants a light touch: `groundwork-ask values`.

## What you do

1. **Read context.** Profile, the target artifact, last 3 sessions on it.

2. **Pick the question.** Based on cadence reason (passed as argument `--reason` or inferred from time-of-day):
   - `daily-anchor` → a `wide` question from the artifact's frameworks, rotated so we don't repeat yesterday's.
   - `weekly-review` → `drift` from `gleb-modes` OR `learning` from `coaching-habit-7q`, alternating.
   - `monthly-drift` → `paradoxes` from `5-prism` OR `salience` from `gleb-modes`.
   - `ad-hoc` → Kickstart from Coaching Habit.

3. **Ask.** One sentence. Wait for the answer.

4. **Acknowledge.** A single short acknowledgment — no coaching follow-up. This is deliberately shallow; depth happens in `groundwork-session`.

5. **Write the log.** `{YYYYMMDD}-{HHMM}-{artifact}-ask.md` with frontmatter:

```yaml
---
session_type: ask
artifact: values
cadence_reason: daily-anchor
question_slug: kickstart
framework_slug: coaching-habit-7q
started_at: 2026-04-16T08:00:00Z
owner: gleb
---
```

Body: the question asked, the user's answer, verbatim.

6. **No synthesize prompt.** Ask skills accumulate; synthesis runs on a cadence or on explicit invocation.

## Tiers

- **line**: `"asked: {question[:40]}…"`
- **brief**: question slug + framework slug + where log is
- **full**: the above + one-sentence echo of the user's answer (for bot surfaces that allow a short reply)

## Headless mode

For scheduled automated pings: no user prompt, just write a pre-formed question and a `status: pending-answer` log file. The next interactive session will surface it.

## Failure modes

- Profile missing → silently stop (scheduled runs shouldn't crash; log the failure to stderr).
- Artifact missing → same.
```

- [ ] **Step 2: Run manifest + commit**

```bash
pytest tests/test_skill_manifests.py -v
git add skills/groundwork-ask/SKILL.md
git commit -m "feat(skill): groundwork-ask — single-question cadence touch"
```

---

### Task D4: groundwork-synthesize

**Files:**
- Create: `skills/groundwork-synthesize/SKILL.md`

- [ ] **Step 1: Write the skill**

```markdown
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
```

- [ ] **Step 2: Run manifest + commit**

```bash
pytest tests/test_skill_manifests.py -v
git add skills/groundwork-synthesize/SKILL.md
git commit -m "feat(skill): groundwork-synthesize — distill sessions into artifact"
```

---

### Task D5: groundwork-review

**Files:**
- Create: `skills/groundwork-review/SKILL.md`

- [ ] **Step 1: Write the skill**

```markdown
---
name: groundwork-review
description: Cross-artifact review. Surfaces drift between intentions and recent activity, unanswered questions, and stale artifacts. Runs on cadence (weekly, monthly, quarterly) or on demand.
io_contract:
  reads:
    - "{data_folder}/profile.md"
    - "{data_folder}/artifacts/*.md"
    - "{data_folder}/sessions/*.md"
  writes:
    - "{data_folder}/sessions/{YYYYMMDD}-{HHMM}-review-{scope}.md"
  returns: "drift summary + 1-3 suggestions"
modes: [interactive, headless]
tiers: [line, brief, full]
---

# groundwork-review

Cross-artifact reflection. Not an artifact-specific session; zoomed-out reading of the whole `.groundwork/` state.

## When to use

- Scheduled: weekly (Friday by default), monthly, quarterly.
- On demand: user wants a snapshot of where they are.

## What you do

1. **Read the whole `.groundwork/`.** Profile, all artifacts, all sessions in the review window (week/month/quarter).

2. **Compute drift.** For each active artifact:
   - What did the user *declare* they'd do (from Goal / Will answers in recent sessions)?
   - What did they *actually* do (from subsequent session answers about action)?
   - Score the gap qualitatively: `aligned`, `modest drift`, `significant drift`.

3. **Identify unanswered questions.** Any session log with a question but no answer (scheduled `ask` files that never got responded to). List them.

4. **Identify staleness.** Any active artifact with no session in the last 4 weeks (or longer than the user's declared cadence). Flag for re-engagement.

5. **Write the review log.** `sessions/{YYYYMMDD}-{HHMM}-review-{scope}.md`:

```yaml
---
session_type: review
scope: weekly  # or monthly, quarterly
started_at: 2026-04-17T18:00:00Z
artifacts_reviewed: [values]
owner: gleb
---
```

Body sections:
- `## Drift` — per-artifact summary
- `## Unanswered` — list of un-replied-to questions
- `## Stale` — artifacts not touched in window
- `## Suggestions` — 1 to 3 specific actions, each a single short sentence

6. **Don't lecture.** The review speaks in a single user-facing paragraph plus bullets. Never more than 300 words total visible content.

## Tiers

- **line**: `"reviewed: {drift_status}"`
- **brief**: drift status + top suggestion
- **full**: the whole paragraph + bullet sections

## Headless mode

Used by scheduled weekly/monthly triggers. Writes log without user prompt. If there are unanswered questions from scheduled asks, surface them via the runtime's notification mechanism (Hermes: multi-platform; Claude Code: stdout).

## Failure modes

- Review window has no sessions → still produce a review noting "quiet week" + base-layer check from gleb-modes.
```

- [ ] **Step 2: Manifest + commit**

```bash
pytest tests/test_skill_manifests.py -v
git add skills/groundwork-review/SKILL.md
git commit -m "feat(skill): groundwork-review — cross-artifact drift check"
```

---

### Task D6: groundwork-rhythm

**Files:**
- Create: `skills/groundwork-rhythm/SKILL.md`

- [ ] **Step 1: Write the skill**

```markdown
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
```

- [ ] **Step 2: Manifest + commit**

```bash
pytest tests/test_skill_manifests.py -v
git add skills/groundwork-rhythm/SKILL.md
git commit -m "feat(skill): groundwork-rhythm — cadence config + runtime reconciliation"
```

---

### Task D7: groundwork-framework

**Files:**
- Create: `skills/groundwork-framework/SKILL.md`

- [ ] **Step 1: Write the skill**

```markdown
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
```

- [ ] **Step 2: Manifest + commit**

```bash
pytest tests/test_skill_manifests.py -v
git add skills/groundwork-framework/SKILL.md
git commit -m "feat(skill): groundwork-framework — library management"
```

---

## Phase E — Onboarding skills

### Task E1: groundwork-ingest

**Files:**
- Create: `skills/groundwork-ingest/SKILL.md`

- [ ] **Step 1: Write the skill**

```markdown
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
```

- [ ] **Step 2: Manifest + commit**

```bash
pytest tests/test_skill_manifests.py -v
git add skills/groundwork-ingest/SKILL.md
git commit -m "feat(skill): groundwork-ingest — distill external material into research findings"
```

---

### Task E2: groundwork-seed

**Files:**
- Create: `skills/groundwork-seed/SKILL.md`

- [ ] **Step 1: Write the skill**

```markdown
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
```

- [ ] **Step 2: Manifest + commit**

```bash
pytest tests/test_skill_manifests.py -v
git add skills/groundwork-seed/SKILL.md
git commit -m "feat(skill): groundwork-seed — draft artifact from research findings"
```

---

## Phase F — Visual skills

### Task F1: groundwork-brand

**Files:**
- Create: `skills/groundwork-brand/SKILL.md`

- [ ] **Step 1: Write the skill**

```markdown
---
name: groundwork-brand
description: Interactive brand-direction picker/evolver. Writes brand.md tokens the visual skills use. D1 "The Terminal" is the starter direction; users can evolve palette, typography, and accent.
io_contract:
  reads:
    - "{data_folder}/visuals/brand/brand.md"
  writes:
    - "{data_folder}/visuals/brand/brand.md"
    - "{data_folder}/visuals/brand/tokens.css"
  returns: "summary of brand changes"
modes: [interactive]
tiers: [line, brief, full]
---

# groundwork-brand

Picks or evolves the user's brand tokens. D1 "The Terminal" is shipped as the default starter direction.

## When to use

- First run (via `groundwork-intake` → brand prompt).
- User wants to tweak colors, accent, or typography: `groundwork-brand`.

## What you do

1. **Read current brand.md.** If it's the default D1 version, offer the starter palette picker (Scriptorium / Studio / Fern / Ember / Ice). If the user has already customized, offer to evolve, not replace.

2. **Picker flow.**
   - Show each palette as a swatch row (mono chars in Geist Mono) with a one-line aesthetic note.
   - User picks one. Update `brand.md` palette section and `tokens.css` CSS variables.

3. **Evolver flow.**
   - Ask which aspect to change: color / typography / accent / personality words.
   - For color: ask for a single hex or a named accent. Validate contrast against the background.
   - For typography: constrain to Google Fonts families (to avoid missing-font rendering). Offer the approved list: Geist, Geist Mono, Instrument Serif, Space Mono, JetBrains Mono, Fraunces, Inter, Inconsolata.
   - For accent: enforce the "one accent per surface" rule by warning if the user tries to define multiple.
   - For personality words: free-text; stored as brand.md's "feel" paragraph.

4. **Always write both files.** `brand.md` (human-readable) and `tokens.css` (machine-readable) must stay in sync. Regenerate `tokens.css` from `brand.md`.

5. **Never silently replace.** Any change is confirmed before write.

## Tiers

- **line**: `"brand updated: {changed}"`
- **brief**: palette + accent + font stack after change
- **full**: the above + a regenerated sample card preview (ASCII, not HTML — for terminal surfaces)

## Failure modes

- User picks a palette not in the starter set → accept it as custom; mark `direction: custom` in brand.md.
- Font not on the approved list → warn; require explicit confirmation before writing.
- Accent contrast ratio against background < 4.5:1 → warn but allow.
```

- [ ] **Step 2: Manifest + commit**

```bash
pytest tests/test_skill_manifests.py -v
git add skills/groundwork-brand/SKILL.md
git commit -m "feat(skill): groundwork-brand — pick and evolve brand tokens"
```

---

### Task F2: groundwork-visual-card

**Files:**
- Create: `skills/groundwork-visual-card/SKILL.md`

- [ ] **Step 1: Write the skill**

```markdown
---
name: groundwork-visual-card
description: Render a named artifact as a share-ready card — SVG plus PNG — using the user's brand tokens. Print- and social-ready.
io_contract:
  reads:
    - "{data_folder}/profile.md"
    - "{data_folder}/artifacts/{artifact}.md"
    - "{data_folder}/visuals/brand/brand.md"
    - "{data_folder}/visuals/brand/tokens.css"
  writes:
    - "{data_folder}/visuals/output/{artifact}-{YYYYMMDD}.svg"
    - "{data_folder}/visuals/output/{artifact}-{YYYYMMDD}.png"
  returns: "paths to SVG and PNG"
modes: [interactive, headless]
tiers: [line, brief, full]
---

# groundwork-visual-card

Renders an artifact as a shareable card. D1 "The Terminal" card template: double-box ASCII frame, label + artifact body + dither footer, one accent highlight.

## When to use

- User wants to share their Values: `groundwork-visual-card values`.
- Cadence review wants a visual snapshot.

## What you do

1. **Read artifact + brand.** Parse the Values artifact (frontmatter + Candidate values list). Load brand tokens.

2. **Compose the card content.** Template:

```
╔══════════════════════════════════════════════════════════════╗
║  {ARTIFACT_TYPE_UPPER}                                       ║
║  ─────────                                                   ║
║                                                              ║
║  {BULLET}  {value_1_text}                                    ║
║  {BULLET}  {value_2_text}                                    ║
║  {BULLET}  {value_3_text}                                    ║
║  ...                                                         ║
║                                                              ║
║                       ░▒▓ {owner} · {YYYY-MM} ▓▒░            ║
╚══════════════════════════════════════════════════════════════╝
```

Pick exactly one value to highlight with the accent color (the one most recently added, or the one marked as `primary` if any).

3. **Render SVG.** Build an SVG document using brand tokens:
   - Background: `--bg` (`#0b0b0c`)
   - Foreground text: `--fg` (`#f5f4f0`)
   - Accent word: `--accent` (`#c17a53`)
   - Font: Geist Mono (embed as web-font link for SVG used in browser; rasterize with local font for PNG)
   - Preserve `font-variant-ligatures: none` so box-drawing glyphs render as glyphs.

4. **Render PNG.** From SVG, rasterize at 1600×1200 (share-ready dimensions). Use `cairosvg` if available; fall back to documenting a manual `rsvg-convert` command if not.

5. **Write both files.** `visuals/output/values-{YYYYMMDD}.svg` and `.png`.

6. **Surface the results.** Return the paths. If runtime allows, open the PNG preview.

## Tiers

- **line**: `"card → {png_path}"`
- **brief**: paths + dimensions
- **full**: paths + a renders ASCII-only preview (what the SVG card contains, minus styling) for terminal surfaces

## Headless mode

Non-interactive — just produce the card. Used by cadence reviews and scheduled exports.

## Failure modes

- Artifact has no values (status seeded, no candidates) → stop; suggest running a session first.
- `cairosvg` not installed → write only the SVG; print a note with the install command.
- Font not available locally for rasterization → use the closest web-safe fallback; warn.
```

- [ ] **Step 2: Manifest + commit**

```bash
pytest tests/test_skill_manifests.py -v
git add skills/groundwork-visual-card/SKILL.md
git commit -m "feat(skill): groundwork-visual-card — render share-ready artifact card"
```

---

## Phase G — Distribution & runtime verification

### Task G1: Manual end-to-end checklist

**Files:**
- Create: `docs/manual-checklist.md`

- [ ] **Step 1: Write the checklist**

Create `docs/manual-checklist.md`:

```markdown
# Manual end-to-end checklist (Values vertical slice)

The skills in this pack are LLM-executed prompts; behavior can't be unit-tested. This checklist is the human walk-through that proves a release works end-to-end. Run it before tagging a release.

## Setup

- [ ] Fresh machine or fresh data-folder location
- [ ] `npx skills add ./` from the repo root installs into `~/.claude/skills/`
- [ ] `ls ~/.claude/skills/groundwork-*` shows all 11 skills as symlinks

## Claude Code flow

- [ ] Invoke `groundwork-intake` in Claude Code
  - [ ] Skill prompts for name, data-folder, mode, rhythm
  - [ ] Profile written at chosen data-folder
  - [ ] Template vault fully copied into `.groundwork/`
  - [ ] Frontmatter passes `python scripts/validate.py` if run against data-folder
- [ ] Invoke `groundwork-ingest` with 2 sample URLs (one article, one YouTube)
  - [ ] Sources cached in `intake/sources/`
  - [ ] `research-findings.md` populated with all eight sections
- [ ] Invoke `groundwork-seed values`
  - [ ] 5-7 candidate values presented with source citations
  - [ ] Interactive keep/cut/sit-with flow works
  - [ ] `values.md` updated; seed session logged
- [ ] Invoke `groundwork-session values`
  - [ ] Session runs 3-7 exchange cycles
  - [ ] Framework selection feels appropriate
  - [ ] Session log written with full transcript
- [ ] Invoke `groundwork-synthesize values`
  - [ ] Artifact updated with new candidate values
  - [ ] Changelog entry appended
  - [ ] `speakable_summary` ≤ 40 words and reads well aloud
- [ ] Invoke `groundwork-visual-card values`
  - [ ] SVG and PNG produced
  - [ ] Card visibly reflects the brand (Geist Mono, monochrome, ember accent)

## Hermes flow (interop spike)

- [ ] `npx skills add ./ -a hermes` succeeds
- [ ] `hermes skills list` shows all 11 skills
- [ ] `groundwork-intake` invocable in `hermes chat`
- [ ] End-to-end same as Claude Code flow above

## Cadence

- [ ] `groundwork-rhythm` adds a daily anchor cron job
- [ ] Fire the cron manually; `groundwork-ask` runs and writes a session log
- [ ] `groundwork-review weekly` produces a drift read

## Bot surface (Hermes Telegram)

- [ ] Hermes Telegram gateway wired up
- [ ] Scheduled daily anchor ping arrives as a Telegram message
- [ ] Voice-memo reply transcribes and appends to the session log

Mark each box before tagging `v0.1.0`.
```

- [ ] **Step 2: Commit**

```bash
git add docs/manual-checklist.md
git commit -m "docs: add manual end-to-end checklist for values slice"
```

---

### Task G2: Local install verification (pre-publish)

**Files:**
- None created; this is a verification task.

- [ ] **Step 1: Verify local install path**

```bash
cd /tmp
mkdir -p groundwork-install-test
cd groundwork-install-test
npx skills add ~/ai_projects/groundwork --skill '*' -a claude-code --copy -y
```

Expected: `./claude-code/skills/groundwork-*` directories present.

- [ ] **Step 2: Verify global install**

```bash
npx skills add ~/ai_projects/groundwork --skill '*' -a claude-code -g -y
ls ~/.claude/skills/ | grep groundwork
```

Expected: `groundwork-intake`, `groundwork-ingest`, …, `groundwork-visual-card` — 11 entries.

- [ ] **Step 3: Run the manual checklist through Task G1**

Walk through `docs/manual-checklist.md`. Note any failures in `docs/runtime-notes.md` (to be created) and fix before proceeding.

- [ ] **Step 4: Create runtime-notes.md with findings**

Create `docs/runtime-notes.md` with a section per runtime — Claude Code, Hermes, Cursor — and record any quirks found. If everything worked, note that explicitly ("No quirks found; installation and invocation parity across all verified runtimes.").

- [ ] **Step 5: Commit**

```bash
git add docs/runtime-notes.md
git commit -m "docs: add runtime notes after local install verification"
```

---

### Task G3: Publish to GitHub

- [ ] **Step 1: Create remote repo**

```bash
gh repo create glebis/groundwork --public --source ~/ai_projects/groundwork --description "work on your core values. a universal skill pack distributed via npx skills." --push
```

Expected: repository visible at `https://github.com/glebis/groundwork`.

- [ ] **Step 2: Verify public install path**

```bash
cd /tmp
rm -rf groundwork-public-test
mkdir groundwork-public-test && cd groundwork-public-test
npx skills add glebis/groundwork --list
```

Expected: list of 11 skills visible.

- [ ] **Step 3: Install from the public source**

```bash
npx skills add glebis/groundwork --skill '*' -a claude-code -g -y
ls ~/.claude/skills/ | grep groundwork
```

Expected: 11 symlinks.

- [ ] **Step 4: Re-run a short version of the manual checklist against the published version**

Specifically: fresh intake → seed → one session → synthesize → visual-card, on a disposable data-folder. Confirm end-to-end works from the public install path.

- [ ] **Step 5: Tag v0.1.0**

```bash
git tag -a v0.1.0 -m "groundwork v0.1.0 — Values vertical slice, D1 Terminal brand, nano banana imagery pipeline"
git push origin v0.1.0
```

- [ ] **Step 6: Update README status strip**

Edit `README.md` status line from `◐` (scaffold) to `✓` (scaffold) + `◐` (skills) → `✓` (skills) + `◐` (release) → `✓` (release). Commit.

```bash
git add README.md
git commit -m "docs: v0.1.0 shipped — update status strip"
git push
```

---

## Self-Review

**Spec coverage** — mapping spec sections to tasks:

| Spec section | Task(s) |
|---|---|
| Six-noun object model | Schemas (A2-A5) + template vault (C1-C4) |
| Values vertical slice v1 | D1-D7, E1-E2, F1-F2 |
| Frameworks as content | B1-B6 |
| Append-only sessions | D2 (session), D3 (ask), D4 (synthesize rules) |
| Profile config | C1 + D6 (rhythm) + A4 (schema) |
| Three output tiers | Present in every skill's SKILL.md |
| Headless mode | Present in every skill |
| Artifact frontmatter contract | A3 (schema) + D4 (synthesize enforces) |
| npx skills distribution | G2, G3 |
| Claude Code + Hermes verification | G1, G2, G3 |
| Voice + bot readiness by contract | Covered in every SKILL.md (tiers, single-utterance rule, inbox folder) |
| Brand kit + visual-card | F1, F2 (visual-identity, visual-map, visual-hero deferred per spec) |

**Placeholders scan:** None. Every task has concrete code or concrete prose content.

**Type consistency:** Skill names used in cross-references (e.g. D6 mentions `groundwork-ask`, E2 mentions `groundwork-ingest`) match the canonical names in their SKILL.md files (D3, E1). Schema names (`framework.schema.yaml`, `artifact.schema.yaml`, etc.) are consistent across Phase A and all test files.

**Scope check:** The plan is large (~35 tasks) but a single vertical slice (Values) with no independent subsystems. A single plan is appropriate; subagent-driven execution is the right model.

One gap noticed on review: the **manifest test in A5** requires `skills/` to exist and contain at least one subdir to pass `test_every_skill_has_manifest`. The test will fail with "no skills in …" until Task D1 lands. That's expected behavior during Phase A; the test goes green once Task D1 is complete. Document this in a comment in the test.

Fixed inline — add to `tests/test_skill_manifests.py` after the existing asserts:

```python
# NOTE: this test fails with "no skills in …" during Phases A-C.
# First passes after Task D1 (groundwork-intake).
```

---

## Execution Handoff

**Plan complete and saved to `docs/plans/2026-04-16-groundwork-v1-implementation.md`. Two execution options:**

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
