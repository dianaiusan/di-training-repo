#!/usr/bin/env python3
"""Remove legacy in-body tag badge sections from course markdown files."""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from course_utils import iter_course_files, parse_frontmatter
import re


def remove_tags_section_from_file(md_file: Path, frontmatter: dict) -> bool:
    """
    Remove legacy in-body ## Tags badge section in a course file.
    Returns True if the file was modified, False otherwise.
    """

    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split frontmatter and body
    if not content.startswith('---'):
        return False

    parts = content.split('---', 2)
    if len(parts) < 3:
        return False

    frontmatter_block = parts[1]
    body = parts[2]

    # Remove one legacy ## Tags HTML block if present.
    tags_pattern = r'\n?## Tags\s*\n\s*<div class="tag-list">\s*\n.*?</div>\s*\n?'
    new_body = re.sub(tags_pattern, "\n\n", body, count=1, flags=re.DOTALL)

    # Reconstruct the file
    new_content = f"---{frontmatter_block}---{new_body}"

    # Write back if changed
    if new_content != content:
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True

    return False


def main():
    """Remove legacy in-body tag badge sections from all course files."""
    updated_count = 0

    for md_file in iter_course_files():
        frontmatter, _ = parse_frontmatter(md_file)
        if not frontmatter:
            continue

        if remove_tags_section_from_file(md_file, frontmatter):
            updated_count += 1
            print(f"Updated {md_file.name}")

    print(f"Updated {updated_count} course file(s) by removing legacy tags sections.")


if __name__ == "__main__":
    main()
