import pathlib

import pytest
import yaml
from jsonschema import validate, ValidationError

REPO = pathlib.Path(__file__).parent.parent
SCHEMA_PATH = REPO / "docs" / "schemas" / "skill.schema.yaml"
SKILLS_DIR = REPO / "skills"

# NOTE: this test skips with "no skills yet" during Phases A-C.
# First actually runs after Task D1 (groundwork-intake) lands.


def _split_frontmatter(text: str) -> dict:
    assert text.startswith("---\n")
    end = text.find("\n---\n", 4)
    assert end != -1
    return yaml.safe_load(text[4:end])


def test_schema_exists():
    assert SCHEMA_PATH.exists()


def test_every_skill_has_manifest():
    if not SKILLS_DIR.exists():
        pytest.skip("no skills/ directory yet")
    skills = [d for d in SKILLS_DIR.iterdir() if d.is_dir()]
    if not skills:
        pytest.skip("no skills yet")
    schema = yaml.safe_load(SCHEMA_PATH.read_text())
    for skill in skills:
        manifest = skill / "SKILL.md"
        assert manifest.exists(), f"{skill.name}: missing SKILL.md"
        data = _split_frontmatter(manifest.read_text())
        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            pytest.fail(f"{skill.name}: {e.message}")
