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
    if not TEMPLATE_PROFILE.exists():
        pytest.skip("template profile not scaffolded yet")
    schema = yaml.safe_load(SCHEMA_PATH.read_text())
    data = _split_frontmatter(TEMPLATE_PROFILE.read_text())
    try:
        validate(instance=data, schema=schema)
    except ValidationError as e:
        pytest.fail(f"profile: {e.message}")
