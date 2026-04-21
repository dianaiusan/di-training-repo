# British English spellcheck

This folder contains spellcheck setup for the repository using cspell and British English.

## Files

- `cspell.json`: main cspell configuration (`en-GB`)
- `cspell-words.txt`: project-specific dictionary words
- `cspell-ignore.txt`: path patterns to ignore
- `run-spellcheck.sh`: convenience script to run the spellcheck

## Run

From repository root:

```bash
bash scripts/spellcheck/run-spellcheck.sh
```

Or directly:

```bash
npx cspell lint --config scripts/spellcheck/cspell.json
```

## Requirements

- Node.js and npm (provides `npx`)

## Notes

- Add accepted domain terms to `cspell-words.txt`.
- Keep `site/` and generated artifacts ignored; check source files under `docs/`, `scripts/`, and `files/`.
- The runner uses `npx --yes` to avoid interactive install prompts.
