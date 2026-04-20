#!/usr/bin/env python3
"""Shared helpers for loading bundle definitions."""

from pathlib import Path
from course_utils import parse_frontmatter

BUNDLE_DEFINITIONS_DIR = Path("docs/explore/bundles")


def iter_bundle_files():
    """Yield bundle definition markdown files in deterministic order."""
    if not BUNDLE_DEFINITIONS_DIR.exists():
        return

    for bundle_file in sorted(BUNDLE_DEFINITIONS_DIR.glob("*.md")):
        normalized_stem = bundle_file.stem.lstrip("_").lower()
        if normalized_stem.startswith("template") or bundle_file.name == "index.md":
            continue
        yield bundle_file


def slug_to_title(value):
    return str(value).replace("-", " ").title()


def load_bundle_definitions():
    """Load bundle definitions and return (definitions, errors)."""
    definitions = []
    errors = []

    for bundle_file in iter_bundle_files() or []:
        frontmatter, _ = parse_frontmatter(bundle_file)
        if not frontmatter:
            errors.append(f"{bundle_file}: missing or invalid frontmatter")
            continue

        slug = frontmatter.get("slug") or bundle_file.stem
        title = frontmatter.get("title") or slug_to_title(slug)
        modules = frontmatter.get("modules", [])
        if not isinstance(modules, list):
            errors.append(f"{bundle_file}: modules must be a list")
            continue

        definitions.append({
            "slug": slug,
            "title": title,
            "description": frontmatter.get("description", ""),
            "audience": frontmatter.get("audience", ""),
            "total_duration": frontmatter.get("total_duration", ""),
            "related_paths": frontmatter.get("related_paths", []),
            "modules": modules,
            "source_path": bundle_file,
        })

    return definitions, errors
