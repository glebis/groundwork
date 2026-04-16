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
    _load_schema()


def test_framework_files_validate(frameworks_dir):
    schema = _load_schema()
    files = [p for p in frameworks_dir.glob("*.md") if not p.name.startswith("_")]
    if not files:
        pytest.skip(f"no framework files in {frameworks_dir} yet (expected during Phase A)")
    for f in files:
        data = _split_frontmatter(f.read_text())
        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            pytest.fail(f"{f.name}: {e.message}")


def test_template_frameworks_validate(repo_root):
    schema = _load_schema()
    template_dir = repo_root / "template-vault" / ".groundwork" / "frameworks"
    if not template_dir.exists():
        pytest.skip("template vault frameworks not scaffolded yet")
    files = [p for p in template_dir.glob("*.md") if p.name != "README.md"]
    if not files:
        pytest.skip("no frameworks in template vault yet")
    for f in files:
        data = _split_frontmatter(f.read_text())
        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            pytest.fail(f"template/{f.name}: {e.message}")
