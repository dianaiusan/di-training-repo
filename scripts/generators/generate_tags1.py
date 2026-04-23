#!/usr/bin/env python3
"""
Generate static tags page (no dynamic JS) for docs/explore/tags1/.
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from course_utils import display_tag, load_courses
from generate_tags import (
    CATEGORY_ORDER, CATEGORY_META, TAG_TO_CATEGORY, group_tags, render_tags_grid
)

OUTPUT_DIR = Path("docs/explore/tags1")
OVERVIEW_FILE = OUTPUT_DIR / "index.md"

def ensure_output_dir():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    ensure_output_dir()
    tags = {}
    for course in load_courses():
        frontmatter = course["frontmatter"]
        if "tags" not in frontmatter:
            continue
        for tag in frontmatter["tags"]:
            tags.setdefault(tag, []).append({
                "title": course["title"],
                "slug": course["slug"],
                "link": course["link"]
            })
    for tag in tags:
        tags[tag].sort(key=lambda x: x["title"])
    grouped = group_tags(tags)
    # Write static overview page
    lines = [
        "---",
        'title: "Tags (Static)"',
        'icon: lucide/tag',
        "---",
        "",
        "# Tags (Static)",
        "",
        "Explore training tags grouped into broader categories:",
        "",
    ]
    for category in CATEGORY_ORDER:
        tags_in_category = grouped.get(category, {})
        if not tags_in_category:
            continue
        title = CATEGORY_META[category]["title"]
        description = CATEGORY_META[category]["description"]
        lines.append(f"## {title}\n\n{description}\n")
        lines.append(render_tags_grid(tags_in_category))
        lines.append("")
    with open(OVERVIEW_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Wrote static tags page to {OVERVIEW_FILE}")

if __name__ == "__main__":
    main()
