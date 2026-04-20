#!/usr/bin/env python3
"""Generate bundle overview/detail pages and course backlinks."""

from pathlib import Path
import re
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from bundles_utils import load_bundle_definitions, slug_to_title
from course_utils import load_courses
from link_utils import (
    bundle_page_to_course_route,
    bundle_page_to_learning_path_route,
    course_page_to_bundle_route,
)

OUTPUT_DIR = Path("docs/explore/bundles")
OVERVIEW_FILE = OUTPUT_DIR / "index.md"

GENERATED_START = "<!-- GENERATED:bundle-links:start -->"
GENERATED_END = "<!-- GENERATED:bundle-links:end -->"



def normalize_module(raw_module):
    """Normalize a bundle module into a uniform shape."""
    if not isinstance(raw_module, dict):
        return None

    if raw_module.get("course"):
        return {
            "type": "course",
            "course_slug": str(raw_module.get("course")),
            "label": raw_module.get("label", "").strip(),
            "duration": raw_module.get("duration", "").strip(),
            "description": raw_module.get("description", "").strip(),
            "optional": bool(raw_module.get("optional", False)),
        }

    module_title = raw_module.get("module") or raw_module.get("title")
    if module_title:
        return {
            "type": "module",
            "title": str(module_title),
            "duration": raw_module.get("duration", "").strip(),
            "description": raw_module.get("description", "").strip(),
            "optional": bool(raw_module.get("optional", False)),
        }

    return None


def render_bundle_modules(bundle_def, course_map):
    """Render ordered module list for a bundle detail page."""
    parts = ['<div class="bd-track">']
    normalized = []

    for idx, raw_module in enumerate(bundle_def["modules"], start=1):
        module = normalize_module(raw_module)
        if not module:
            continue

        normalized.append(module)

        badges = []
        if module.get("optional"):
            badges.append('<span class="bd-badge">Optional</span>')

        if module["type"] == "course":
            course = course_map.get(module["course_slug"])
            title = course["title"] if course else f"Missing course: {module['course_slug']}"
            href = bundle_page_to_course_route(module["course_slug"]) if course else "#"
            badges.insert(0, '<span class="bd-badge bd-badge-core">Standalone course</span>')
            display = module["label"] or title
            subtitle = title if module["label"] and module["label"] != title else ""
            if module.get("duration"):
                badges.append(f'<span class="bd-badge">{module["duration"]}</span>')

            subtitle_html = f'<p class="bd-meta">{subtitle}</p>' if subtitle else ""
            desc_html = (
                f'<p class="bd-desc">{module["description"]}</p>'
                if module["description"]
                else ""
            )
            badges_html = "".join(badges)

            parts.append(
                f'<div class="bd-item">\n'
                f'  <div class="bd-item-head">\n'
                f'    <span class="bd-num">{idx}</span>\n'
                f'    <div class="bd-main">\n'
                f'      <p class="bd-title"><a href="{href}">{display}</a></p>\n'
                f'      {subtitle_html}\n'
                f'      {badges_html}\n'
                f'      {desc_html}\n'
                f'    </div>\n'
                f'  </div>\n'
                f'</div>'
            )
        else:
            if module.get("duration"):
                badges.append(f'<span class="bd-badge">{module["duration"]}</span>')
            badges.insert(0, '<span class="bd-badge">Bundle-only module</span>')

            desc_html = (
                f'<p class="bd-desc">{module["description"]}</p>'
                if module["description"]
                else ""
            )
            badges_html = "".join(badges)

            parts.append(
                f'<div class="bd-item">\n'
                f'  <div class="bd-item-head">\n'
                f'    <span class="bd-num">{idx}</span>\n'
                f'    <div class="bd-main">\n'
                f'      <p class="bd-title">{module["title"]}</p>\n'
                f'      {badges_html}\n'
                f'      {desc_html}\n'
                f'    </div>\n'
                f'  </div>\n'
                f'</div>'
            )

    parts.append("</div>")
    return "\n".join(parts), normalized


def render_related_paths(related_paths):
    if not related_paths:
        return ""
    links = [
        f"- [{slug_to_title(slug)}]({bundle_page_to_learning_path_route(slug)})"
        for slug in related_paths
    ]
    return "\n".join(["### Related learning paths", ""] + links + [""])


def render_bundle_section(bundle_def, course_map):
    modules_html, modules = render_bundle_modules(bundle_def, course_map)
    standalone_count = sum(1 for m in modules if m["type"] == "course")

    lines = [
        f"## {bundle_def['title']}",
        "",
        bundle_def["description"],
        "",
    ]

    topline_bits = []
    if bundle_def.get("audience"):
        topline_bits.append(f"Audience: {bundle_def['audience']}")
    if bundle_def.get("total_duration"):
        topline_bits.append(f"Duration: {bundle_def['total_duration']}")
    if topline_bits:
        lines.append(f'<p class="bd-topline">{" | ".join(topline_bits)}</p>')
        lines.append("")

    lines.append(modules_html)
    lines.append("")
    lines.append(f"Includes {len(modules)} modules, with {standalone_count} reusable standalone course(s).")
    lines.append("")

    related = render_related_paths(bundle_def.get("related_paths", []))
    if related:
        lines.append(related)

    return "\n".join(lines), modules


def update_bundle_file(bundle_def, section):
    """Update individual bundle file while preserving frontmatter."""
    bundle_file = OUTPUT_DIR / f"{bundle_def['slug']}.md"
    if not bundle_file.exists():
        return

    content = bundle_file.read_text(encoding="utf-8")
    if content.startswith("---"):
        parts = content.split("---", 2)
        frontmatter = parts[0] + "---" + parts[1] + "---" if len(parts) >= 3 else ""
    else:
        frontmatter = ""

    bundle_file.write_text(frontmatter + "\n" + section, encoding="utf-8")


def update_overview(bundle_defs, bundle_stats):
    """Write bundles overview page."""
    lines = [
        "---",
        'title: "Bundles Overview"',
        "icon: lucide/layers-3",
        "---",
        "",
        "# Bundles Overview",
        "",
        "Delivery-focused collections of modules and courses that can be run as coherent workshop packages.",
        "",
        '<div class="bd-card-grid">',

    ]

    for bundle_def in bundle_defs:
        stats = bundle_stats.get(bundle_def["slug"], {"modules": 0, "standalone": 0})
        href = f"./{bundle_def['slug']}/"
        lines.extend([
            f'<a class="bd-card-link" href="{href}">',
            '  <div class="bd-card">',
            f"    <h3>{bundle_def['title']}</h3>",
            f"    <p>{bundle_def['description']}</p>",
            f"    <p>{stats['modules']} modules</p>",
            f"    <p>{stats['standalone']} standalone course reference(s)</p>",
            "  </div>",
            "</a>",
        ])

    lines.extend(["</div>", ""])
    OVERVIEW_FILE.write_text("\n".join(lines), encoding="utf-8")


def remove_generated_bundle_section(text):
    pattern = re.compile(
        rf"\n?{re.escape(GENERATED_START)}.*?{re.escape(GENERATED_END)}\n?",
        re.DOTALL,
    )
    return re.sub(pattern, "\n", text).rstrip() + "\n"


def update_course_backlinks(course_to_bundles, course_map):
    """Append generated 'Part of bundles' section to referenced courses."""
    updated = 0

    for course_slug, course in course_map.items():
        source_path = course["source_path"]
        content = source_path.read_text(encoding="utf-8")
        has_generated_block = GENERATED_START in content and GENERATED_END in content
        clean = remove_generated_bundle_section(content) if has_generated_block else content

        bundle_refs = sorted(course_to_bundles.get(course_slug, []), key=lambda x: x["title"])
        if bundle_refs:
            lines = [
                GENERATED_START,
                "## Part of bundles",
                "",
            ]
            for ref in bundle_refs:
                lines.append(f"- [{ref['title']}]({course_page_to_bundle_route(ref['slug'])})")
            lines.extend(["", GENERATED_END])
            new_content = clean.rstrip() + "\n\n" + "\n".join(lines) + "\n"
        else:
            if not has_generated_block:
                continue
            new_content = clean

        if new_content != content:
            source_path.write_text(new_content, encoding="utf-8")
            updated += 1

    return updated


def generate_bundles(bundle_definitions):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    courses = load_courses()
    course_map = {course["slug"]: course for course in courses}

    course_to_bundles = {}
    bundle_stats = {}

    for bundle_def in bundle_definitions:
        section, modules = render_bundle_section(bundle_def, course_map)
        update_bundle_file(bundle_def, section)

        standalone = 0
        for module in modules:
            if module["type"] != "course":
                continue
            standalone += 1
            slug = module["course_slug"]
            course_to_bundles.setdefault(slug, []).append({
                "slug": bundle_def["slug"],
                "title": bundle_def["title"],
            })

        bundle_stats[bundle_def["slug"]] = {
            "modules": len(modules),
            "standalone": standalone,
        }

    update_overview(bundle_definitions, bundle_stats)
    updated_courses = update_course_backlinks(course_to_bundles, course_map)

    total_modules = sum(stats["modules"] for stats in bundle_stats.values())
    print(
        f"Updated {OVERVIEW_FILE}, {len(bundle_definitions)} bundle page(s), "
        f"{total_modules} module entries, and {updated_courses} course backlink page(s)."
    )


if __name__ == "__main__":
    definitions, load_errors = load_bundle_definitions()
    if load_errors:
        print("Bundle load errors:")
        for err in load_errors:
            print(f"- {err}")
        raise SystemExit(1)

    generate_bundles(definitions)
