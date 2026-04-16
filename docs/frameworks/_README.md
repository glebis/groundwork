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
