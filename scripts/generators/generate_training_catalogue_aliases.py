#!/usr/bin/env python3
"""Generate alias pages under docs/explore/training-catalogue/ from advert frontmatter URLs."""

from __future__ import annotations

from pathlib import Path

import yaml

ADVERTS_DIR = Path("docs/all-training/adverts")
DOCS_DIR = Path("docs")
TRAINING_PREFIX = "/explore/training-catalogue/"


def parse_frontmatter(md_file: Path) -> dict | None:
    """Parse frontmatter from a markdown file."""
    content = md_file.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return None

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None

    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None

    return data if isinstance(data, dict) else None


def docs_route_from_file(md_file: Path) -> str:
    """Convert docs/<path>.md to a site route /<path>/."""
    rel = md_file.relative_to(DOCS_DIR).as_posix()
    return f"/{rel[:-3]}/"


def alias_file_from_url(url: str) -> Path | None:
    """Map an internal training-catalogue URL to docs markdown file path."""
    if not url.startswith(TRAINING_PREFIX):
        return None

    path = url.strip("/")
    if not path:
        return None

    return DOCS_DIR / f"{path}.md"


def detect_target_url(frontmatter: dict, source_file: Path, alias_url: str) -> str:
    """Choose where alias page should point."""
    external_url = frontmatter.get("external_url")
    if isinstance(external_url, str):
        external_url = external_url.strip()
        if external_url.startswith(("http://", "https://")):
            return external_url

    source_route = docs_route_from_file(source_file)
    if source_route != alias_url:
        return source_route

    slug = str(frontmatter.get("slug", "")).strip()
    if slug:
        return f"/all-training/{slug}/"

    return "/explore/training-catalogue/"


def render_alias_page(title: str, target_url: str) -> str:
    """Render alias page content with fast redirect and fallback link."""
    return f"""---
title: \"{title}\"
---

<meta http-equiv=\"refresh\" content=\"0; url={target_url}\"> 

# Redirecting

If you are not redirected automatically, open [the course page]({target_url}).
"""


def main() -> int:
    generated = 0

    for md_file in sorted(ADVERTS_DIR.rglob("*.md")):
        if md_file.name == "_template.md":
            continue

        frontmatter = parse_frontmatter(md_file)
        if not frontmatter:
            continue

        title = str(frontmatter.get("title", "")).strip()
        url = str(frontmatter.get("url", "")).strip()
        if not title or not url:
            continue

        alias_file = alias_file_from_url(url)
        if not alias_file:
            continue

        target_url = detect_target_url(frontmatter, md_file, url)
        alias_file.parent.mkdir(parents=True, exist_ok=True)
        alias_file.write_text(render_alias_page(title, target_url), encoding="utf-8")
        generated += 1

    print(f"Generated {generated} training-catalogue alias page(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
