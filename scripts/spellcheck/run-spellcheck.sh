#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO_ROOT"

# Run cspell with explicit target globs. Uses npx so no global install is required.
npx --yes cspell lint \
	--config scripts/spellcheck/cspell.json \
	"docs/**/*.md" \
	"scripts/**/*.py" \
	"files/**/*.md"
