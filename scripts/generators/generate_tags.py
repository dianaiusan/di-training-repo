#!/usr/bin/env python3
"""Generate grouped tags pages under docs/explore/tags/."""

from collections import defaultdict
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json

from course_utils import display_tag, load_courses
from lucide_icons import render_lucide_img


OUTPUT_DIR = Path("docs/explore/tags")
OVERVIEW_FILE = OUTPUT_DIR / "index.md"
LEGACY_FILE = Path("docs/explore/tags.md")
TAXONOMY_JSON_FILE = OUTPUT_DIR / "tags-taxonomy.json"


def tags_overview_to_category_route(category_slug: str) -> str:
    """Link from /explore/tags/ to /explore/tags/<category>/."""
    return f"./{category_slug}/"


def tag_category_to_course_route(course_link: str) -> str:
    """Link from /explore/tags/<category>/ to a course page route."""
    if course_link.startswith("/"):
        return course_link
    return f"../../../{course_link.lstrip('/')}"


def tag_category_to_overview_route() -> str:
    """Link from /explore/tags/<category>/ to /explore/tags/."""
    return "../"


CATEGORY_META = {
    "programming-languages": {
        "title": "Programming Languages",
        "description": "Programming languages used across the training catalogue.",
    },
    "hpc-core": {
        "title": "HPC Core",
        "description": "Core HPC usage topics including systems, schedulers, modules, and environments.",
    },
    "parallel-performance": {
        "title": "Parallel & Performance",
        "description": "Parallel programming models, accelerators, profiling, and performance work.",
    },
    "data-ai": {
        "title": "Data & AI",
        "description": "Data analysis, machine learning, deep learning, and notebook-based workflows.",
    },
    "software-engineering": {
        "title": "Software Engineering",
        "description": "Programming, software structure, testing, and code quality.",
    },
    "data-management-security": {
        "title": "Data Management & Security",
        "description": "File movement, storage, sensitive data, and secure data handling environments.",
    },
    "numerical-visualization": {
        "title": "Numerical Methods & Visualization",
        "description": "Linear algebra, numerical computing, and scientific visualization methods.",
    },
    "tools-platforms": {
        "title": "Tools & Platforms",
        "description": "Named tools, libraries, and software platforms used in the courses.",
    },
    "other": {
        "title": "Other",
        "description": "Additional tags not yet categorized.",
    },
}


CATEGORY_ORDER = [
    "programming-languages",
    "hpc-core",
    "parallel-performance",
    "data-ai",
    "software-engineering",
    "data-management-security",
    "numerical-visualization",
    "tools-platforms",
    "other",
]


CATEGORY_ICON_KEYS = {
    "programming-languages": "code-2",
    "hpc-core": "server",
    "parallel-performance": "chart-no-axes-column-increasing",
    "data-ai": "database",
    "software-engineering": "notebook-pen",
    "data-management-security": "shield-check",
    "numerical-visualization": "chart-scatter",
    "tools-platforms": "wrench",
    "other": "tag",
}


TAG_TO_CATEGORY = {
    "algorithms": "software-engineering",
    "apptainer": "tools-platforms",
    "arm": "parallel-performance",
    "bianca": "data-management-security",
    "code-quality": "software-engineering",
    "containers": "tools-platforms",
    "cpp": "programming-languages",
    "cuda": "parallel-performance",
    "data-analysis": "data-ai",
    "data-management": "data-management-security",
    "data-structures": "software-engineering",
    "deep-learning": "data-ai",
    "distributed-memory": "parallel-performance",
    "eigen": "tools-platforms",
    "environment-management": "hpc-core",
    "file-transfer": "data-management-security",
    "gpu": "parallel-performance",
    "hpc-advanced": "hpc-core",
    "hpc-intro": "hpc-core",
    "jupyter": "data-ai",
    "linear-algebra": "numerical-visualization",
    "linux": "hpc-core",
    "machine-learning": "data-ai",
    "modular-programming": "software-engineering",
    "modules": "hpc-core",
    "mpi": "parallel-performance",
    "numerical-computing": "numerical-visualization",
    "paraview": "tools-platforms",
    "parallel-programming": "parallel-performance",
    "performance": "parallel-performance",
    "profiling": "parallel-performance",
    "programming": "software-engineering",
    "python": "programming-languages",
    "pytorch": "data-ai",
    "reproducibility": "software-engineering",
    "sensitive-data": "data-management-security",
    "singularity": "tools-platforms",
    "slurm": "hpc-core",
    "software-design": "software-engineering",
    "storage": "data-management-security",
    "testing": "software-engineering",
    "visualization": "numerical-visualization",
    "vtk": "tools-platforms",
    "ai-safety": "data-ai",
}
def render_tag_courses(tag_name: str, courses: list) -> str:
    """Render a single tag card with its courses."""
    courses_html = "\n".join(
        f'    <li><a class="tag-course-link" href="{tag_category_to_course_route(course["link"])}">{course["title"]}</a></li>'
        for course in courses
    )
    
    return (
        f'<div class="tag-card">\n'
        f'  <h4 class="tag-card-name">{display_tag(tag_name)}</h4>\n'
        f'  <ul class="tag-card-courses">\n'
        f'{courses_html}\n'
        f'  </ul>\n'
        f'</div>'
    )


def render_tags_grid(tags_in_category: dict) -> str:
    """Render all tags in a category as a grid of cards."""
    if not tags_in_category:
        return ""
    
    cards = ['<div class="tag-grid">']
    
    for tag in sorted(tags_in_category.keys()):
        cards.append(render_tag_courses(tag, tags_in_category[tag]))
    
    cards.append("</div>")
    return "\n".join(cards)


def generate_tags_dict():
    """Generate dictionary of tags and their courses."""
    tags = defaultdict(list)

    for course in load_courses():
        frontmatter = course["frontmatter"]
        if "tags" not in frontmatter:
            continue
        for tag in frontmatter["tags"]:
            tags[tag].append(
                {
                    "title": course["title"],
                    "slug": course["slug"],
                    "link": course["link"],
                }
            )

    for tag in tags:
        tags[tag].sort(key=lambda x: x["title"])

    return tags


def group_tags(tags):
    """Group tags by broader category."""
    grouped = defaultdict(dict)

    for tag in sorted(tags.keys()):
        category = TAG_TO_CATEGORY.get(tag, "other")
        grouped[category][tag] = tags[tag]

    return grouped


def ensure_output_dir():
    """Create docs/explore/tags/ and remove legacy flat file if present."""
    if LEGACY_FILE.exists() and LEGACY_FILE.is_file():
        LEGACY_FILE.unlink()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def render_category_card_grid(grouped):
    """Render category cards for the tags overview page."""
    non_empty = [key for key in CATEGORY_ORDER if grouped.get(key)]
    if not non_empty:
        return ""

    cards = []
    cards.append('<div class="tg-card-grid">')

    for category in non_empty:
        title = CATEGORY_META[category]["title"]
        description = CATEGORY_META[category]["description"]
        tag_count = len(grouped[category])
        course_count = sum(len(courses) for courses in grouped[category].values())
        tag_label = "tag" if tag_count == 1 else "tags"
        course_label = "course reference" if course_count == 1 else "course references"
        icon_key = CATEGORY_ICON_KEYS.get(category, "tag")
        icon_img = render_lucide_img(
            icon_key,
            fallback_icon="tag",
            size_class="tg-card-icon-img",
            src_prefix="../../assets/images/icons",
        )

        cards.append(
            f'<a class="tg-card-link" href="{tags_overview_to_category_route(category)}">\n'
            f'<div class="tg-card">\n'
            f'  <div class="tg-card-icon">{icon_img}</div>\n'
            f'  <h3 class="tg-card-title">{title}</h3>\n'
            f'  <p class="tg-card-desc">{description}</p>\n'
            f'  <p class="tg-card-meta">{tag_count} {tag_label} · {course_count} {course_label}</p>\n'
            f'</div>\n'
            f'</a>'
        )

    cards.append("</div>")
    return "\n".join(cards)


def write_overview(grouped):
    """Write tags overview page with links to category pages."""
    lines = [
        "---",
        'title: "Tags"',
        "icon: lucide/tag",
        "---",
        "",
        "# Tags",
        "",
        "Explore training tags grouped into broader categories:",
        "",
    ]

    if not any(grouped.get(key) for key in CATEGORY_ORDER):
        lines.append("No tags found.")
        lines.append("")
    else:
        lines.append(render_category_card_grid(grouped))
        lines.append("")

    with open(OVERVIEW_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def write_category_pages(grouped):
    """Write one page per non-empty category."""
    expected = set()

    for category in CATEGORY_ORDER:
        tags_in_category = grouped.get(category, {})
        if not tags_in_category:
            continue

        title = CATEGORY_META[category]["title"]
        description = CATEGORY_META[category]["description"]
        category_file = OUTPUT_DIR / f"{category}.md"
        expected.add(category_file.name)

        lines = [
            "---",
            f'title: "{title}"',
            "---",
            "",
            f"# {title}",
            "",
            description,
            "",
            f'<a class="tag-page-link" href="{tag_category_to_overview_route()}">← Back to Tags overview</a>',
            "",
        ]

        lines.append(render_tags_grid(tags_in_category))
        lines.append("")

        with open(category_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    expected.add(OVERVIEW_FILE.name)
    for path in OUTPUT_DIR.glob("*.md"):
        if path.name not in expected:
            path.unlink()


def main():
    ensure_output_dir()
    tags = generate_tags_dict()
    grouped = group_tags(tags)
    write_overview(grouped)
    write_category_pages(grouped)

    # Write tags and courses as JSON for dynamic rendering
    tags_json = {}
    for tag, courses in tags.items():
        tags_json[tag] = [
            {
                "title": course["title"],
                "slug": course["slug"],
                "link": course["link"]
            }
            for course in courses
        ]
    json_path = Path("docs/explore/tags/tags-courses.json")
    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(tags_json, jf, indent=2, ensure_ascii=False)

    taxonomy_json = {
        "category_order": CATEGORY_ORDER,
        "category_meta": CATEGORY_META,
        "tag_to_category": TAG_TO_CATEGORY,
    }
    with open(TAXONOMY_JSON_FILE, "w", encoding="utf-8") as jf:
        json.dump(taxonomy_json, jf, indent=2, ensure_ascii=False)

    total_tags = sum(len(v) for v in grouped.values())
    total_courses = sum(len(courses) for courses in tags.values())
    written_categories = sum(1 for key in CATEGORY_ORDER if grouped.get(key))
    print(
        f"Updated {OVERVIEW_FILE} and {written_categories} category page(s) "
        f"with {total_tags} tags and {total_courses} course references."
    )

    print(f"Wrote tags JSON to {json_path}")
    print(f"Wrote taxonomy JSON to {TAXONOMY_JSON_FILE}")


if __name__ == "__main__":
    main()
