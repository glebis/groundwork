#!/usr/bin/env bash
# Copy canonical frameworks into the template vault.
# Run whenever docs/frameworks/ changes.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
cp "$REPO"/docs/frameworks/*.md "$REPO"/template-vault/.groundwork/frameworks/
rm -f "$REPO"/template-vault/.groundwork/frameworks/_README.md
echo "synced canonical frameworks into template vault"
