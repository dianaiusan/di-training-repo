#!/usr/bin/env python3
"""Generate learning-path overview and detail page bodies from frontmatter."""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Any

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from course_utils import load_course_lookup
from lucide_icons import render_lucide_img

EVENTS_DIR = Path("docs/all-training/events")
PATHS_DIR = Path("docs/all-training/learning-paths")  # source input
OUTPUT_PATHS_DIR = Path("docs/explore/learning-paths")         # generated output
INDEX_FILE = OUTPUT_PATHS_DIR / "index.md"

PATH_ICONS = {
    "beginner": "sprout",
    "bioinformatics": "dna",
    "data-science": "chart-line",
    "developer": "code-2",
    "sensitive-data": "shield-plus",
}


def split_frontmatter(content: str) -> tuple[str, str] | tuple[None, None]:
    if not content.startswith("---"):
        return None, None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, None
    return f"---{parts[1]}---\n", parts[2].lstrip("\n")


def parse_frontmatter(md_file: Path) -> tuple[dict | None, str | None]:
    content = md_file.read_text(encoding="utf-8")
    fm_block, _ = split_frontmatter(content)
    if fm_block is None:
        return None, None
    try:
        frontmatter = yaml.safe_load(fm_block.strip("-\n"))
    except yaml.YAMLError:
        return None, None
    return frontmatter if isinstance(frontmatter, dict) else None, fm_block


def iter_EVENTS() -> list[Path]:
    files: list[Path] = []
    for md_file in sorted(EVENTS_DIR.rglob("*.md")):
        if md_file.name == "_template.md":
            continue
        files.append(md_file)
    return files


def humanize_slug(value: str) -> str:
    return value.replace("-", " ").title()


def phase_title(phase_slug: str) -> str:
    return phase_slug.replace("-", " ").title()


def normalize_course_entry(raw_course: Any) -> dict[str, Any] | None:
    if isinstance(raw_course, str):
        slug = raw_course.strip()
        return {"slug": slug} if slug else None

    if isinstance(raw_course, dict):
        slug = str(raw_course.get("slug", "")).strip()
        if not slug:
            return None
        return {
            "slug": slug,
            "title": str(raw_course.get("title", "")).strip(),
            "note": str(raw_course.get("note", "")).strip(),
        }

    return None


def normalize_stages(path_fm: dict[str, Any]) -> list[dict[str, Any]]:
    stages = path_fm.get("stages")
    if isinstance(stages, list):
        normalized: list[dict[str, Any]] = []
        for index, raw_stage in enumerate(stages):
            if not isinstance(raw_stage, dict):
                continue

            title = str(raw_stage.get("title", "")).strip()
            stage_id = str(raw_stage.get("id", "")).strip()
            if not title:
                title = phase_title(stage_id) if stage_id else f"Stage {index + 1}"

            raw_courses = raw_stage.get("courses", [])
            courses: list[dict[str, Any]] = []
            if isinstance(raw_courses, list):
                for raw_course in raw_courses:
                    course = normalize_course_entry(raw_course)
                    if course:
                        courses.append(course)

            normalized.append(
                {
                    "title": title,
                    "intensity": str(raw_stage.get("intensity", "")).strip(),
                    "courses": courses,
                }
            )

        return normalized

    phases = path_fm.get("phases", {})
    normalized = []
    if isinstance(phases, dict):
        for phase_slug, course_slugs in phases.items():
            courses: list[dict[str, Any]] = []
            if isinstance(course_slugs, list):
                for raw_slug in course_slugs:
                    course = normalize_course_entry(raw_slug)
                    if course:
                        courses.append(course)

            normalized.append(
                {
                    "title": phase_title(str(phase_slug)),
                    "intensity": "",
                    "courses": courses,
                }
            )

    return normalized


def normalize_connections(path_fm: dict[str, Any]) -> list[dict[str, str]]:
    raw_connections = path_fm.get("connections", [])
    if not isinstance(raw_connections, list):
        return []

    normalized: list[dict[str, str]] = []
    for raw_connection in raw_connections:
        if not isinstance(raw_connection, dict):
            continue

        from_slug = str(raw_connection.get("from", "")).strip()
        to_slug = str(raw_connection.get("to", "")).strip()
        if not from_slug or not to_slug:
            continue

        normalized.append(
            {
                "from": from_slug,
                "to": to_slug,
                "type": str(
                    raw_connection.get("type", raw_connection.get("kind", "related"))
                ).strip()
                or "related",
                "label": str(raw_connection.get("label", "")).strip(),
            }
        )

    return normalized


def course_display(course_slug: str, course_meta: dict[str, Any], courses_by_slug: dict[str, dict[str, Any]]) -> tuple[str, str]:
    course = courses_by_slug.get(course_slug, {})
    course_title = str(course_meta.get("title") or course.get("title") or humanize_slug(course_slug))
    course_link = str(course.get("link") or "#")
    return course_title, course_link


def render_detail_body(path_fm: dict[str, Any], path_lookup: dict[str, dict], courses_by_slug: dict[str, dict[str, Any]]) -> str:
    title = str(path_fm.get("title", "")).strip()
    description = str(path_fm.get("description", "")).strip()
    stages = normalize_stages(path_fm)
    connections = normalize_connections(path_fm)
    related_paths = path_fm.get("related_paths", [])

    lines: list[str] = [f"## {title}", "", description, "", '<div class="lp-swimlane">']

    sequence = 1
    if stages:
        for idx, stage in enumerate(stages):
            stage_title = str(stage.get("title", "")).strip() or f"Stage {idx + 1}"
            stage_intensity = str(stage.get("intensity", "")).strip()
            lines.extend(['  <div class="lp-phase">', '    <div class="lp-phase-header">'])
            lines.append(f'      <span class="lp-phase-title">{stage_title}</span>')
            if stage_intensity:
                lines.append(
                    f'      <span class="lp-phase-intensity">Intensity {stage_intensity}</span>'
                )
            lines.extend(["    </div>", '    <div class="lp-phase-body">'])

            for course_meta in stage.get("courses", []):
                course_slug = str(course_meta.get("slug", "")).strip()
                if not course_slug:
                    continue
                course_title, course_link = course_display(course_slug, course_meta, courses_by_slug)
                lines.extend(
                    [
                        '      <div class="lp-course-item">',
                        f'        <span class="lp-course-num">{sequence}</span>',
                        '        <div class="lp-course-copy">',
                        f'          <a href="{course_link}">{course_title}</a>',
                    ]
                )
                if course_meta.get("note"):
                    lines.append(f'          <p class="lp-course-note">{course_meta["note"]}</p>')
                lines.extend(["        </div>", "      </div>"])
                sequence += 1

            lines.extend(["    </div>", "  </div>"])
            if idx < len(stages) - 1:
                lines.append('  <div class="lp-phase-arrow">&darr;</div>')

    lines.append("</div>")

    if connections:
        lines.extend(["", "### Course connections", "", '<div class="lp-connection-grid">'])
        for connection in connections:
            from_title, from_link = course_display(connection["from"], {}, courses_by_slug)
            to_title, to_link = course_display(connection["to"], {}, courses_by_slug)
            connection_type = connection["type"].replace("-", " ").title()
            label = connection["label"] or connection_type
            lines.extend(
                [
                    '<div class="lp-connection-card">',
                    f'  <p class="lp-connection-type">{label}</p>',
                    '  <p class="lp-connection-route">',
                    f'    <a href="{from_link}">{from_title}</a> <span class="lp-connection-arrow">&rarr;</span> <a href="{to_link}">{to_title}</a>',
                    "  </p>",
                    "</div>",
                ]
            )
        lines.append("</div>")

    lines.extend(["", "### Related paths", ""])
    lines.append('<div class="lp-related-grid">')
    if isinstance(related_paths, list) and related_paths:
        for raw_slug in related_paths:
            rel_slug = str(raw_slug).strip()
            if not rel_slug:
                continue
            rel_meta = path_lookup.get(rel_slug, {})
            rel_title = str(rel_meta.get("title") or humanize_slug(rel_slug))
            rel_desc = str(rel_meta.get("description") or "")
            lines.extend(
                [
                    '<div class="lp-related-card">',
                    '  <div class="lp-related-head">',
                    f'    <p class="lp-related-title"><a href="../{rel_slug}/">{rel_title}</a></p>',
                    "  </div>",
                    f'  <p class="lp-related-desc">{rel_desc}</p>' if rel_desc else '  <p class="lp-related-desc"></p>',
                    "</div>",
                ]
            )
    else:
        lines.append('<div class="lp-related-card"><p class="lp-related-desc">No related paths configured.</p></div>')
    lines.append("</div>")
    lines.append("")

    return "\n".join(lines)


def render_index(paths: list[dict[str, str]]) -> str:
    lines: list[str] = [
        "---",
        'title: "Learning Paths Overview"',
        "icon: lucide/route",
        "---",
        "",
        "# Learning Paths Overview",
        "",
        "Choose a learning path tailored to your role and goals:",
        "",
        '<div class="lp-card-grid">',
    ]

    for item in sorted(paths, key=lambda p: p["title"].lower()):
        icon_name = PATH_ICONS.get(item["slug"], "route")
        icon_img = render_lucide_img(
            icon_name,
            fallback_icon="route",
            size_class="lp-card-icon-img",
            src_prefix="../../assets/images/icons",
        )
        lines.extend(
            [
                f'<a class="lp-card-link" href="./{item["slug"]}/">',
                '  <div class="lp-card">',
                f'    <div class="lp-card-icon">{icon_img}</div>',
                f'    <h3 class="lp-card-title">{item["title"]}</h3>',
                f'    <p class="lp-card-desc">{item["description"]}</p>',
                "  </div>",
                "</a>",
            ]
        )

    lines.extend(["</div>", ""])
    return "\n".join(lines)


def main() -> None:
    courses_by_slug = load_course_lookup()

    path_files = sorted(
        [p for p in PATHS_DIR.glob("*.md") if p.name != "index.md"],
        key=lambda p: p.name,
    )

    path_meta: dict[str, dict] = {}
    fm_by_file: dict[Path, tuple[dict, str]] = {}
    for file_path in path_files:
        frontmatter, frontmatter_block = parse_frontmatter(file_path)
        if not frontmatter or not frontmatter_block:
            continue
        slug = str(frontmatter.get("slug", "")).strip()
        if not slug:
            continue
        path_meta[slug] = frontmatter
        fm_by_file[file_path] = (frontmatter, frontmatter_block)

    paths_for_index: list[dict[str, str]] = []

    for file_path, (frontmatter, fm_block) in fm_by_file.items():
        slug = str(frontmatter.get("slug", "")).strip()
        title = str(frontmatter.get("title", humanize_slug(slug))).strip()
        description = str(frontmatter.get("description", "")).strip()

        body = render_detail_body(frontmatter, path_meta, courses_by_slug)
        out_file = OUTPUT_PATHS_DIR / file_path.name
        out_file.write_text(f"{fm_block}\n{body}", encoding="utf-8")

        paths_for_index.append(
            {
                "slug": slug,
                "title": title,
                "description": description,
            }
        )

    INDEX_FILE.write_text(render_index(paths_for_index), encoding="utf-8")
    print(
        f"Generated learning paths overview + {len(paths_for_index)} detail page(s)."
    )


if __name__ == "__main__":
    main()
