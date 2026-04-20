#!/usr/bin/env bash
set -euo pipefail

npx cspell --config scripts/spellcheck/cspell.json "$@"
