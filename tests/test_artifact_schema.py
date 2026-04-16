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


def test_schema_loads():
    _load_schema()


def test_all_template_artifacts_validate():
    if not TEMPLATE_ARTIFACTS.exists():
        pytest.skip("template artifacts not scaffolded yet")
    schema = _load_schema()
    files = list(TEMPLATE_ARTIFACTS.glob("*.md"))
    if not files:
        pytest.skip("no template artifacts yet")
    for f in files:
        data = _split_frontmatter(f.read_text())
        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            pytest.fail(f"{f.name}: {e.message}")
