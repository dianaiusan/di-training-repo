#!/usr/bin/env python3
"""
Inject level: frontmatter field from level tags in courses,
then remove the level tags from the tags: list.

Idempotent: files that already have level: and no level tags are skipped.
"""

import json
import re
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from course_utils import iter_course_files

LEVEL_TAGS = {"beginner", "intermediate", "advanced"}
LEVEL_ORDER = ["beginner", "intermediate", "advanced"]


def split_frontmatter(content: str) -> tuple[str, str] | tuple[None, None]:
    if not content.startswith("---"):
        return None, None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, None
    return parts[1].strip("\n"), parts[2]


def get_scalar(line: str) -> str:
    if ":" not in line:
        return ""
    raw = line.split(":", 1)[1].strip()
    if raw.startswith('"') and raw.endswith('"'):
        return raw[1:-1]
    if raw.startswith("'") and raw.endswith("'"):
        return raw[1:-1]
    return raw


def parse_inline_tags(line: str) -> list[str] | None:
    """Parse an inline JSON array from a tags: line. Returns None if not parseable."""
    m = re.search(r":\s*(\[.*?\])\s*$", line)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


def parse_block_tags(lines: list[str], tags_idx: int) -> list[str] | None:
    """Parse YAML block-sequence tags starting after tags_idx. Returns list or None."""
    result = []
    for ln in lines[tags_idx + 1:]:
        m = re.match(r"^\s*-\s+(.+)$", ln)
        if m:
            result.append(m.group(1).strip().strip('"\"'))
        else:
            break  # end of block sequence
    return result if result else None


def inject_level(md_path: Path) -> bool:
    content = md_path.read_text(encoding="utf-8")
    fm_text, body = split_frontmatter(content)
    if fm_text is None:
        return False

    lines = fm_text.splitlines()

    # Find existing level: field
    level_idx = next(
        (i for i, ln in enumerate(lines) if re.match(r"^\s*level\s*:", ln)), None
    )

    # Find and parse the tags: line
    tags_idx = next(
        (i for i, ln in enumerate(lines) if re.match(r"^\s*tags\s*:", ln)), None
    )

    current_tags: list[str] = []
    if tags_idx is not None:
        current_tags = (
            parse_inline_tags(lines[tags_idx])
            or parse_block_tags(lines, tags_idx)
            or []
        )

    found_levels = [t for t in current_tags if t in LEVEL_TAGS]

    # Skip if already migrated: level: exists and no level tags remain in tags:
    if level_idx is not None and not found_levels:
        return False

    # Determine chosen level value (lowest entry-level requirement)
    chosen_level = (
        min(found_levels, key=lambda x: LEVEL_ORDER.index(x)) if found_levels else ""
    )

    modified = False

    # Insert or update level: field
    if level_idx is not None:
        current = get_scalar(lines[level_idx])
        if current != chosen_level:
            lines[level_idx] = f'level: "{chosen_level}"'
            modified = True
    else:
        # Insert after duration: or format: or status:
        insert_at = len(lines)
        for key in ("duration:", "format:", "status:"):
            idx = next(
                (i for i, ln in enumerate(lines) if ln.strip().startswith(key)), None
            )
            if idx is not None:
                insert_at = idx + 1
                break
        lines.insert(insert_at, f'level: "{chosen_level}"')
        modified = True

    # Remove level tags from tags: list
    if found_levels and tags_idx is not None:
        # Re-find after potential insert above
        tags_idx = next(
            (i for i, ln in enumerate(lines) if re.match(r"^\s*tags\s*:", ln)), None
        )
        if tags_idx is not None:
            new_tags = [t for t in current_tags if t not in LEVEL_TAGS]
            # Handle both inline and block sequence
            m = re.search(r":\s*(\[.*?\])\s*$", lines[tags_idx])
            if m:
                # Inline: rewrite the array on the same line
                prefix = lines[tags_idx][: m.start(1)]
                lines[tags_idx] = prefix + json.dumps(new_tags)
            else:
                # Block sequence: rebuild lines
                # Find how many block-sequence lines follow tags_idx
                block_end = tags_idx + 1
                while block_end < len(lines) and re.match(r"^\s*-\s+", lines[block_end]):
                    block_end += 1
                new_block = [f"- {t}" for t in new_tags]
                lines[tags_idx + 1 : block_end] = new_block
            modified = True

    if not modified:
        return False

    new_fm = "\n".join(lines)
    new_content = f"---\n{new_fm}\n---{body}"

    if new_content != content:
        md_path.write_text(new_content, encoding="utf-8")
        return True
    return False


def main() -> None:
    updated = 0
    skipped = 0
    for md_path in iter_course_files():
        if inject_level(md_path):
            updated += 1
            print(f"  Updated: {md_path.name}")
        else:
            skipped += 1
    print(f"\nLevel injection: {updated} files updated, {skipped} skipped.")


if __name__ == "__main__":
    main()
