#!/usr/bin/env python3
"""Generate learning-path overview and detail page bodies from frontmatter."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from lucide_icons import render_lucide_img

ADVERTS_DIR = Path("docs/all-training/adverts")
PATHS_DIR = Path("docs/explore/learning-paths")
INDEX_FILE = PATHS_DIR / "index.md"

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


def iter_adverts() -> list[Path]:
    files: list[Path] = []
    for md_file in sorted(ADVERTS_DIR.rglob("*.md")):
        if md_file.name == "_template.md":
            continue
        files.append(md_file)
    return files


def load_course_titles() -> dict[str, str]:
    titles: dict[str, str] = {}
    for md_file in iter_adverts():
        frontmatter, _ = parse_frontmatter(md_file)
        if not frontmatter:
            continue
        slug = str(frontmatter.get("slug", "")).strip()
        title = str(frontmatter.get("title", "")).strip()
        if slug and title:
            titles[slug] = title
    return titles


def course_route(slug: str) -> str:
    return f"/explore/training-catalogue/{slug}/"


def humanize_slug(value: str) -> str:
    return value.replace("-", " ").title()


def phase_title(phase_slug: str) -> str:
    return phase_slug.replace("-", " ").title()


def render_detail_body(path_fm: dict[str, Any], path_lookup: dict[str, dict], course_titles: dict[str, str]) -> str:
    title = str(path_fm.get("title", "")).strip()
    description = str(path_fm.get("description", "")).strip()
    phases = path_fm.get("phases", {})
    related_paths = path_fm.get("related_paths", [])

    lines: list[str] = [f"## {title}", "", description, "", '<div class="lp-swimlane">']

    sequence = 1
    if isinstance(phases, dict):
        phase_items = list(phases.items())
        for idx, (phase_slug, course_slugs) in enumerate(phase_items):
            lines.extend(
                [
                    '  <div class="lp-phase">',
                    f'    <div class="lp-phase-header">{phase_title(str(phase_slug))}</div>',
                    '    <div class="lp-phase-body">',
                ]
            )

            if isinstance(course_slugs, list):
                for raw_slug in course_slugs:
                    course_slug = str(raw_slug).strip()
                    if not course_slug:
                        continue
                    course_title = course_titles.get(course_slug, humanize_slug(course_slug))
                    lines.append(
                        f'      <div class="lp-course-item"><span class="lp-course-num">{sequence}</span><a href="{course_route(course_slug)}">{course_title}</a></div>'
                    )
                    sequence += 1

            lines.extend(["    </div>", "  </div>"])
            if idx < len(phase_items) - 1:
                lines.append('  <div class="lp-phase-arrow">&darr;</div>')

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
    course_titles = load_course_titles()

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

        body = render_detail_body(frontmatter, path_meta, course_titles)
        file_path.write_text(f"{fm_block}\n{body}", encoding="utf-8")

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
