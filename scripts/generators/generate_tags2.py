#!/usr/bin/env python3
"""
Generate dynamic single-select tags page for docs/explore/tags2/.
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from course_utils import load_courses
import json
from generate_tags import CATEGORY_ORDER, CATEGORY_META, TAG_TO_CATEGORY, group_tags

OUTPUT_DIR = Path("docs/explore/tags2")
OVERVIEW_FILE = OUTPUT_DIR / "index.md"
JSON_FILE = Path("docs/explore/tags/tags-courses.json")
TAXONOMY_JSON_FILE = Path("docs/explore/tags/tags-taxonomy.json")

def ensure_output_dir():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def render_category_summary(grouped):
    lines = ["## Tag Categories", ""]
    for category in CATEGORY_ORDER:
        tags_in_category = grouped.get(category, {})
        if not tags_in_category:
            continue
        title = CATEGORY_META[category]["title"]
        description = CATEGORY_META[category]["description"]
        lines.append(f"- **{title}**: {description}")
    lines.append("")
    return lines

def main():
    ensure_output_dir()
    # Generate tags-courses.json
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
    JSON_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(JSON_FILE, "w", encoding="utf-8") as jf:
        json.dump(tags, jf, indent=2, ensure_ascii=False)
    with open(TAXONOMY_JSON_FILE, "w", encoding="utf-8") as jf:
        json.dump(
            {
                "category_order": CATEGORY_ORDER,
                "category_meta": CATEGORY_META,
                "tag_to_category": TAG_TO_CATEGORY,
            },
            jf,
            indent=2,
            ensure_ascii=False,
        )
    # Write dynamic page (Markdown with JS)
    lines = [
        "---",
        'title: "Tags (Dynamic Single-Select)"',
        'icon: lucide/tag',
        "---",
        "",
        "# Tags (Dynamic Single-Select)",
        "",
        "Explore training tags. Select a tag to see courses.",
        "",
    ]
    lines.extend(render_category_summary(grouped))
    lines.extend([
        "<style>",
        "  .tag-list { display: flex; flex-wrap: wrap; gap: 0.5em; margin-bottom: 1.5em; }",
        "  .tag-btn { padding: 0.4em 1em; border: 1px solid #aaa; border-radius: 1em; background: #f8f8f8; cursor: pointer; transition: background 0.2s, color 0.2s; }",
        "  .tag-btn.selected { background: #0077cc; color: #fff; border-color: #0077cc; }",
        "  .course-list { list-style: none; padding: 0; }",
        "  .course-list li { margin-bottom: 0.5em; }",
        "</style>",
        "<div id=\"tags2-app\">",
        "  <div class=\"tag-list\" id=\"tagList\"></div>",
        "  <div id=\"selectedTagInfo\"></div>",
        "  <ul class=\"course-list\" id=\"courseList\"></ul>",
        "</div>",
        "<script src=\"../../assets/javascripts/tags2.js\"></script>",
    ])
    with open(OVERVIEW_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Wrote dynamic single-select tags page to {OVERVIEW_FILE}")

if __name__ == "__main__":
    main()
