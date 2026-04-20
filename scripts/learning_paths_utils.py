#!/usr/bin/env python3
"""Shared helpers for loading learning path definitions."""

from pathlib import Path
from course_utils import parse_frontmatter

PATH_DEFINITIONS_DIR = Path("docs/explore/learning-paths")


def iter_path_files():
    """Yield learning path markdown definition files in deterministic order."""
    if not PATH_DEFINITIONS_DIR.exists():
        return

    for path_file in sorted(PATH_DEFINITIONS_DIR.glob("*.md")):
        if path_file.name.startswith("template") or path_file.name == "index.md":
            continue
        yield path_file


def slug_to_title(value):
    return str(value).replace("-", " ").title()


def load_path_definitions():
    """Load path definitions and return (definitions, errors)."""
    definitions = []
    errors = []

    for path_file in iter_path_files() or []:
        frontmatter, _ = parse_frontmatter(path_file)
        if not frontmatter:
            errors.append(f"{path_file}: missing or invalid frontmatter")
            continue

        slug = frontmatter.get("slug") or path_file.stem
        title = frontmatter.get("title") or slug_to_title(slug)

        definitions.append({
            "slug": slug,
            "title": title,
            "description": frontmatter.get("description", ""),
            "icon": frontmatter.get("icon", "lucide/route"),
            "phases": frontmatter.get("phases", {}),
            "related_paths": frontmatter.get("related_paths", []),
            "source_path": path_file,
        })

    return definitions, errors
