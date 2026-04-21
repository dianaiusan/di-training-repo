#!/usr/bin/env python3
"""Generate grouped tags pages under docs/explore/tags/."""

from collections import defaultdict
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from course_utils import display_tag, load_courses


OUTPUT_DIR = Path("docs/explore/tags")
OVERVIEW_FILE = OUTPUT_DIR / "index.md"
LEGACY_FILE = Path("docs/explore/tags.md")


def tags_overview_to_category_route(category_slug: str) -> str:
    """Link from /explore/tags/ to /explore/tags/<category>/."""
    return f"./{category_slug}/"


def tag_category_to_course_route(course_slug: str) -> str:
    """Link from /explore/tags/<category>/ to /explore/training-catalogue/<course>/."""
    return f"../../../explore/training-catalogue/{course_slug}/"


def tag_category_to_overview_route() -> str:
    """Link from /explore/tags/<category>/ to /explore/tags/."""
    return "../"


CATEGORY_META = {
    "hpc-infrastructure": {
        "title": "HPC & Infrastructure",
        "description": "Systems, platforms, environments, and operations.",
    },
    "parallel-performance": {
        "title": "Parallel & Performance",
        "description": "Scaling, profiling, and high-performance programming.",
    },
    "gpu": {
        "title": "GPU",
        "description": "GPU hardware, acceleration stacks, and related workflows.",
    },
    "data-ai": {
        "title": "Data & AI",
        "description": "Data workflows, machine learning, and analytics.",
    },
    "software-development": {
        "title": "Software Development",
        "description": "Languages, tooling, testing, and engineering practice.",
    },
    "workflow-automation": {
        "title": "Workflow & Automation",
        "description": "Pipelines, scheduling, and reproducible orchestration.",
    },
    "foundations-levels": {
        "title": "Foundations & Levels",
        "description": "Introductory tracks and skill progression tags.",
    },
    "domains-visualization": {
        "title": "Domains & Visualization",
        "description": "Domain methods, math, and scientific visualization.",
    },
    "security-sensitive-data": {
        "title": "Security & Sensitive Data",
        "description": "Secure computing and sensitive data handling.",
    },
    "other": {
        "title": "Other",
        "description": "Additional tags not yet categorized.",
    },
}


CATEGORY_ORDER = [
    "hpc-infrastructure",
    "parallel-performance",
    "gpu",
    "data-ai",
    "software-development",
    "workflow-automation",
    "foundations-levels",
    "domains-visualization",
    "security-sensitive-data",
    "other",
]


CATEGORY_ICON_KEYS = {
    "hpc-infrastructure": "server",
    "parallel-performance": "chart-no-axes-column-increasing",
    "gpu": "gpu",
    "data-ai": "database",
    "software-development": "code-2",
    "workflow-automation": "workflow",
    "foundations-levels": "graduation-cap",
    "domains-visualization": "images",
    "security-sensitive-data": "shield-check",
    "other": "tag",
}


LUCIDE_PATHS = {
    "server": '<rect width="20" height="8" x="2" y="2" rx="2" ry="2"/><rect width="20" height="8" x="2" y="14" rx="2" ry="2"/><line x1="6" x2="6.01" y1="6" y2="6"/><line x1="6" x2="6.01" y1="18" y2="18"/>',
    "chart-no-axes-column-increasing": '<path d="M5 21v-6"/><path d="M12 21V9"/><path d="M19 21V3"/>',
    "gpu": '<path d="M2 17h18a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2H2"/><path d="M2 21V3"/><path d="M7 17v3a1 1 0 0 0 1 1h5a1 1 0 0 0 1-1v-3"/><circle cx="16" cy="11" r="2"/><circle cx="8" cy="11" r="2"/>',
    "database": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 0 21 19V5"/><path d="M3 12A9 3 0 0 0 21 12"/>',
    "code-2": '<path d="m18 16 4-4-4-4M6 8l-4 4 4 4M14.5 4l-5 16"/>',
    "workflow": '<rect width="8" height="8" x="3" y="3" rx="2"/><path d="M7 11v4a2 2 0 0 0 2 2h4"/><rect width="8" height="8" x="13" y="13" rx="2"/>',
    "graduation-cap": '<path d="M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z"/><path d="M22 10v6"/><path d="M6 12.5V16a6 3 0 0 0 12 0v-3.5"/>',
    "images": '<path d="m22 11-1.296-1.296a2.4 2.4 0 0 0-3.408 0L11 16"/><path d="M4 8a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2"/><circle cx="13" cy="7" r="1" fill="currentColor"/><rect x="8" y="2" width="14" height="14" rx="2"/>',
    "shield-check": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "tag": '<path d="M12.586 2.586A2 2 0 0 0 11.172 2H4a2 2 0 0 0-2 2v7.172a2 2 0 0 0 .586 1.414l8.704 8.704a2.426 2.426 0 0 0 3.42 0l6.58-6.58a2.426 2.426 0 0 0 0-3.42z"/><circle cx="7.5" cy="7.5" r=".5" fill="currentColor"/>',
}


TAG_TO_CATEGORY = {
    "advanced": "foundations-levels",
    "ai": "data-ai",
    "apptainer": "hpc-infrastructure",
    "automation": "workflow-automation",
    "aws": "hpc-infrastructure",
    "azure": "hpc-infrastructure",
    "beginner": "foundations-levels",
    "benchmarking": "parallel-performance",
    "best-practices": "software-development",
    "bianca": "security-sensitive-data",
    "big-data": "data-ai",
    "cloud": "hpc-infrastructure",
    "conda": "hpc-infrastructure",
    "containers": "hpc-infrastructure",
    "cpp": "software-development",
    "cuda": "gpu",
    "cupy": "gpu",
    "data-analysis": "data-ai",
    "data-management": "data-ai",
    "data-science": "data-ai",
    "debugging": "software-development",
    "deep-learning": "data-ai",
    "distributed-computing": "parallel-performance",
    "dvc": "data-ai",
    "eigen": "software-development",
    "environments": "hpc-infrastructure",
    "external-resource": "hpc-infrastructure",
    "file-transfer": "hpc-infrastructure",
    "filesystems": "hpc-infrastructure",
    "git": "software-development",
    "gpu": "gpu",
    "grace-hopper": "gpu",
    "hdf5": "data-ai",
    "hpc": "hpc-infrastructure",
    "hybrid": "parallel-performance",
    "infrastructure": "hpc-infrastructure",
    "intermediate": "foundations-levels",
    "introduction": "foundations-levels",
    "jax": "gpu",
    "job-arrays": "workflow-automation",
    "julia": "software-development",
    "linear-algebra": "domains-visualization",
    "linux": "hpc-infrastructure",
    "machine-learning": "data-ai",
    "modules": "hpc-infrastructure",
    "mpi": "parallel-performance",
    "nextflow": "workflow-automation",
    "openmp": "parallel-performance",
    "optimization": "parallel-performance",
    "parallel": "parallel-performance",
    "parallel-computing": "parallel-performance",
    "paraview": "domains-visualization",
    "past": "other",
    "performance": "parallel-performance",
    "profiling": "parallel-performance",
    "programming": "software-development",
    "python": "software-development",
    "r": "software-development",
    "reproducibility": "software-development",
    "scalability": "parallel-performance",
    "scientific-computing": "domains-visualization",
    "security": "security-sensitive-data",
    "sensitive-data": "security-sensitive-data",
    "singularity": "hpc-infrastructure",
    "slurm": "hpc-infrastructure",
    "snakemake": "workflow-automation",
    "software": "software-development",
    "software-engineering": "software-development",
    "statistics": "domains-visualization",
    "storage": "hpc-infrastructure",
    "testing": "software-development",
    "threading": "parallel-performance",
    "version-control": "software-development",
    "visualization": "domains-visualization",
    "workflow": "workflow-automation",
}
def render_tag_courses(tag_name: str, courses: list) -> str:
    """Render a single tag card with its courses."""
    courses_html = "\n".join(
        f'    <li><a class="tag-course-link" href="{tag_category_to_course_route(course["slug"])}">{course["title"]}</a></li>'
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


def render_lucide_icon(icon_name, size_class="tg-card-icon-svg"):
    """Render an inline lucide SVG."""
    icon_key = str(icon_name or "tag")
    svg_paths = LUCIDE_PATHS.get(icon_key, LUCIDE_PATHS["tag"])
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" '
        f'stroke-linecap="round" stroke-linejoin="round" stroke-width="2" '
        f'class="lucide lucide-{icon_key} {size_class}" viewBox="0 0 24 24">{svg_paths}</svg>'
    )


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
        icon_svg = render_lucide_icon(icon_key)

        cards.append(
            f'<a class="tg-card-link" href="{tags_overview_to_category_route(category)}">\n'
            f'<div class="tg-card">\n'
            f'  <div class="tg-card-icon">{icon_svg}</div>\n'
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

    total_tags = sum(len(v) for v in grouped.values())
    total_courses = sum(len(courses) for courses in tags.values())
    written_categories = sum(1 for key in CATEGORY_ORDER if grouped.get(key))
    print(
        f"Updated {OVERVIEW_FILE} and {written_categories} category page(s) "
        f"with {total_tags} tags and {total_courses} course references."
    )


if __name__ == "__main__":
    main()
