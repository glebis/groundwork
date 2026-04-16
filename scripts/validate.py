#!/usr/bin/env python3
"""Run all schema validations. Exit non-zero on first failure."""
import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).parent.parent


def main() -> int:
    result = subprocess.run(["python3", "-m", "pytest", str(REPO / "tests"), "-q"], cwd=REPO)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
