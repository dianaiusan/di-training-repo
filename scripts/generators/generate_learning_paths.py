#!/usr/bin/env python3
"""Generate overview and detail pages from docs/explore/learning-paths/*.md definitions."""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from course_utils import load_courses
from learning_paths_utils import load_path_definitions, slug_to_title
from link_utils import (
    learning_path_page_to_course_route,
    learning_paths_overview_to_path_route,
    learning_path_detail_to_related_path_route,
)

OUTPUT_DIR = Path("docs/explore/learning-paths")
OVERVIEW_FILE = OUTPUT_DIR / "index.md"

LUCIDE_PATHS = {
    "route": '<circle cx="6" cy="19" r="3"/><path d="M9 19h8.5a3.5 3.5 0 0 0 0-7h-11a3.5 3.5 0 0 1 0-7H15"/><circle cx="18" cy="5" r="3"/>',
    "sprout": '<path d="M14 9.536V7a4 4 0 0 1 4-4h1.5a.5.5 0 0 1 .5.5V5a4 4 0 0 1-4 4 4 4 0 0 0-4 4c0 2 1 3 1 5a5 5 0 0 1-1 3M4 9a5 5 0 0 1 8 4 5 5 0 0 1-8-4M5 21h14"/>',
    "code-2": '<path d="m18 16 4-4-4-4M6 8l-4 4 4 4M14.5 4l-5 16"/>',
    "chart-line": '<path d="M3 3v16a2 2 0 0 0 2 2h16"/><path d="m19 9-5 5-4-4-3 3"/>',
    "dna": '<path d="m10 16 1.5 1.5M14 8l-1.5-1.5M15 2c-1.798 1.998-2.518 3.995-2.807 5.993M16.5 10.5l1 1M17 6l-2.891-2.891M2 15c6.667-6 13.333 0 20-6M20 9l.891.891M3.109 14.109 4 15M6.5 12.5l1 1M7 18l2.891 2.891M9 22c1.798-1.998 2.518-3.995 2.807-5.993"/>',
    "shield-plus": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="M9 12h6"/><path d="M12 9v6"/>',
}

# Card grid icons per path slug — decoupled from frontmatter so nav stays icon-free
PATH_CARD_ICONS = {
    "beginner": "sprout",
    "developer": "code-2",
    "data-science": "chart-line",
    "bioinformatics": "dna",
    "sensitive-data": "shield-plus",
}





def render_lucide_icon(icon_name, size_class="lp-card-icon-svg"):
    """Render an inline lucide SVG matching icons used in navigation."""
    icon_key = str(icon_name).split("/", 1)[-1] if icon_name else "route"
    svg_paths = LUCIDE_PATHS.get(icon_key, LUCIDE_PATHS["route"])
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" '
        f'stroke-linecap="round" stroke-linejoin="round" stroke-width="2" '
        f'class="lucide lucide-{icon_key} {size_class}" viewBox="0 0 24 24">{svg_paths}</svg>'
    )


def course_href(record):
    return learning_path_page_to_course_route(record["slug"])


def build_swimlane(path_def, course_map):
    """Build an HTML phase swimlane for one learning path."""
    ordered_slugs = []
    for slugs in path_def["phases"].values():
        if isinstance(slugs, list):
            ordered_slugs.extend(slugs)

    step_numbers = {slug: i + 1 for i, slug in enumerate(ordered_slugs)}
    phases = list(path_def["phases"].items())

    html_parts = ['<div class="lp-swimlane">']

    for phase_idx, (phase_name, slugs) in enumerate(phases):
        phase_label = slug_to_title(phase_name)
        items_html = []
        if isinstance(slugs, list):
            for slug in slugs:
                record = course_map.get(slug)
                title = record["title"] if record else f"Missing: {slug}"
                href = course_href(record) if record else "#"
                num = step_numbers[slug]
                items_html.append(
                    f'      <div class="lp-course-item">'
                    f'<span class="lp-course-num">{num}</span>'
                    f'<a href="{href}">{title}</a>'
                    f'</div>'
                )

        phase_html = (
            f'  <div class="lp-phase">\n'
            f'    <div class="lp-phase-header">{phase_label}</div>\n'
            f'    <div class="lp-phase-body">\n'
            + "\n".join(items_html) + "\n"
            + f'    </div>\n'
            + f'  </div>'
        )
        html_parts.append(phase_html)

        if phase_idx < len(phases) - 1:
            html_parts.append('  <div class="lp-phase-arrow">&darr;</div>')

    html_parts.append("</div>")
    return "\n".join(html_parts), ordered_slugs


def render_card_grid(path_definitions):
    """Render a grid of path cards as HTML for quick overview."""
    if not path_definitions:
        return ""

    cards = []
    cards.append(
        '<div class="lp-card-grid">'
    )

    for path_def in path_definitions:
        icon_svg = render_lucide_icon(PATH_CARD_ICONS.get(path_def["slug"], "route"))
        href = learning_paths_overview_to_path_route(path_def["slug"])
        cards.append(
            f'<a class="lp-card-link" href="{href}">\n'
            f'  <div class="lp-card">\n'
            f'    <div class="lp-card-icon">{icon_svg}</div>\n'
            f'    <h3 class="lp-card-title">{path_def["title"]}</h3>\n'
            f'    <p class="lp-card-desc">{path_def["description"]}</p>\n'
            f"  </div>\n"
            f"</a>"
        )

    cards.append("</div>")
    return "\n".join(cards)


def render_related_paths_grid(path_def, path_by_slug):
    """Render related learning paths as a compact card grid."""
    if not path_def["related_paths"]:
        return ""

    cards = []
    cards.append('<div class="lp-related-grid">')

    for related_slug in path_def["related_paths"]:
        related = path_by_slug.get(related_slug)
        title = related["title"] if related else slug_to_title(related_slug)
        desc = related["description"] if related else ""
        icon_svg = render_lucide_icon(
            PATH_CARD_ICONS.get(related_slug, "route"),
            size_class="lp-related-icon-svg",
        )
        cards.append(
            f'<div class="lp-related-card">\n'
            f'  <div class="lp-related-head">\n'
            f'    <span class="lp-related-icon">{icon_svg}</span>\n'
            f'    <p class="lp-related-title"><a href="{learning_path_detail_to_related_path_route(related_slug)}">{title}</a></p>\n'
            f'  </div>\n'
            f'  <p class="lp-related-desc">{desc}</p>\n'
            f'</div>'
        )

    cards.append("</div>")
    return "\n".join(cards)


def render_path_section(path_def, course_map, path_by_slug):
    swimlane, ordered_slugs = build_swimlane(path_def, course_map)
    missing = [slug for slug in ordered_slugs if slug not in course_map]

    section = []
    section.append(f"## {path_def['title']}")
    section.append("")
    if path_def["description"]:
        section.append(path_def["description"])
        section.append("")

    section.append(swimlane)
    section.append("")

    if path_def["related_paths"]:
        section.append("### Related paths")
        section.append("")
        section.append(render_related_paths_grid(path_def, path_by_slug))
        section.append("")

    return "\n".join(section), len(ordered_slugs), len(missing)


def update_learning_paths_overview(path_definitions):
    """Update docs/explore/learning-paths/index.md with card grid overview."""
    body_lines = [
        "---",
        'title: "Learning Paths Overview"',
        'icon: lucide/route',
        "---",
        "",
        "# Learning Paths Overview",
        "",
        "Choose a learning path tailored to your role and goals:",
        "",
    ]

    card_grid = render_card_grid(path_definitions)
    if card_grid:
        body_lines.append(card_grid)
        body_lines.append("")

    with open(OVERVIEW_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(body_lines))


def update_path_file(path_def, section):
    """Update individual path file with full content for sidebar navigation."""
    path_file = OUTPUT_DIR / f"{path_def['slug']}.md"
    if not path_file.exists():
        return

    with open(path_file, "r", encoding="utf-8") as f:
        content = f.read()

    if content.startswith("---"):
        parts = content.split("---", 2)
        frontmatter = parts[0] + "---" + parts[1] + "---" if len(parts) >= 3 else ""
    else:
        frontmatter = ""

    with open(path_file, "w", encoding="utf-8") as f:
        f.write(frontmatter + "\n" + section)


def generate_learning_paths(path_definitions):
    course_map = {course["slug"]: course for course in load_courses()}
    path_by_slug = {path_def["slug"]: path_def for path_def in path_definitions}

    total_positions = 0
    total_missing = 0

    if path_definitions:
        for path_def in path_definitions:
            section, positions, missing = render_path_section(path_def, course_map, path_by_slug)
            total_positions += positions
            total_missing += missing
            update_path_file(path_def, section)

    update_learning_paths_overview(path_definitions)

    print(
        f"Updated {OVERVIEW_FILE} with {len(path_definitions)} paths, "
        f"{total_positions} ordered positions, {total_missing} missing course slugs."
    )


if __name__ == "__main__":
    definitions, load_errors = load_path_definitions()
    if load_errors:
        print("Learning path load errors:")
        for err in load_errors:
            print(f"- {err}")
        raise SystemExit(1)

    generate_learning_paths(definitions)
