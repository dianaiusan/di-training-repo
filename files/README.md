# NAISS Training (DI's WIP)

Rendered page: https://dianaiusan.github.io/di-training-repo/

## Maintainer Docs

- Repository architecture and rendering: [repo-architecture.md](repo-architecture.md)
- Content authoring and maintenance workflow: [content-maintenance-guide.md](content-maintenance-guide.md)

## Collaborator Workflow

Use this workflow whenever you update content in docs/all-training, docs/explore, docs/events, or any generator script under scripts.

### 1. Activate the environment

```bash
source .venv/bin/activate
```

### 2. Regenerate generated content + build + link-check

```bash
.venv/bin/python scripts/generate_all.py
```

What this command now does:
- runs all generator scripts in order
- builds the site with zensical
- validates internal links in rendered output
- fails with non-zero exit code if any step fails

### 3. Optional: run a clean build

Use this if you want to verify from a clean output directory.

```bash
.venv/bin/zensical build --clean
```

### 4. Optional: preview locally

```bash
.venv/bin/zensical serve -a localhost:8001
```

Open: http://localhost:8001/

Important:
- If zensical is "command not found", use .venv/bin/zensical explicitly (as above).
- If port 8001 is busy, pick another port (for example localhost:8002).
- For local preview, use URLs without the GitHub Pages prefix.

## When You Must Run scripts/generate_all.py

Run it after changes to any of these:
- docs/all-training/*.md
- docs/explore/**/*.md
- docs/events/**/*.md
- scripts/*.py

Reason: several pages are generated and cross-linked automatically (events indexes, tags, scientific domains, learning paths, bundles, and backlinks).

## Quick PR Checklist

Before pushing:
- run .venv/bin/python scripts/generate_all.py
- verify no failures in generation, build, or link check
- review generated file diffs before commit
