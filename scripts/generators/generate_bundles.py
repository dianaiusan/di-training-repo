#!/usr/bin/env python3
"""Generate bundle overview and detail page bodies from bundle frontmatter."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ADVERTS_DIR = Path("all-training-input/events")
BUNDLES_DIR = Path("all-training-input/bundles")  # source input
OUTPUT_BUNDLES_DIR = Path("docs/explore/bundles")       # generated output
INDEX_FILE = OUTPUT_BUNDLES_DIR / "index.md"


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


def humanize_slug(value: str) -> str:
    return value.replace("-", " ").title()


def course_route(slug: str) -> str:
    return f"/explore/training-catalogue/{slug}/"


def render_bundle_body(bundle_fm: dict[str, Any], course_titles: dict[str, str]) -> tuple[str, int, int]:
    title = str(bundle_fm.get("title", "")).strip()
    description = str(bundle_fm.get("description", "")).strip()
    audience = str(bundle_fm.get("audience", "")).strip()
    total_duration = str(bundle_fm.get("total_duration", "")).strip()
    modules = bundle_fm.get("modules", [])
    related_paths = bundle_fm.get("related_paths", [])

    lines: list[str] = [f"## {title}", "", description, ""]
    if audience or total_duration:
        lines.append(
            f'<p class="bd-topline">Audience: {audience or "TBD"} | Duration: {total_duration or "TBD"}</p>'
        )
        lines.append("")

    lines.append('<div class="bd-track">')
    module_count = 0
    standalone_count = 0

    if isinstance(modules, list):
        for idx, module in enumerate(modules, start=1):
            if not isinstance(module, dict):
                continue
            module_count += 1
            course_slug = str(module.get("course", "")).strip()
            module_label = str(module.get("label", "")).strip()
            module_name = str(module.get("module", "")).strip()
            duration = str(module.get("duration", "")).strip()
            module_desc = str(module.get("description", "")).strip()

            title_text = module_label or module_name or humanize_slug(course_slug)
            lines.extend(
                [
                    '<div class="bd-item">',
                    '  <div class="bd-item-head">',
                    f'    <span class="bd-num">{idx}</span>',
                    '    <div class="bd-main">',
                ]
            )

            if course_slug:
                standalone_count += 1
                course_title = course_titles.get(course_slug, humanize_slug(course_slug))
                lines.append(
                    f'      <p class="bd-title"><a href="{course_route(course_slug)}">{title_text}</a></p>'
                )
                lines.append(f'      <p class="bd-meta">{course_title}</p>')
                lines.append('      <span class="bd-badge bd-badge-core">Standalone course</span>')
            else:
                lines.append(f'      <p class="bd-title">{title_text}</p>')
                lines.append('      <span class="bd-badge">Bundle-only module</span>')
                if duration:
                    lines.append(f'      <span class="bd-badge">{duration}</span>')

            if module_desc:
                lines.append(f'      <p class="bd-desc">{module_desc}</p>')

            lines.extend(['    </div>', '  </div>', '</div>'])

    lines.append('</div>')
    lines.append("")
    lines.append(
        f"Includes {module_count} modules, with {standalone_count} reusable standalone course(s)."
    )
    lines.append("")
    lines.append("### Related learning paths")
    lines.append("")

    if isinstance(related_paths, list) and related_paths:
        for item in related_paths:
            path_slug = str(item).strip()
            if not path_slug:
                continue
            lines.append(f"- [{humanize_slug(path_slug)}](/explore/learning-paths/{path_slug}/)")
    else:
        lines.append("- None")

    lines.append("")
    return "\n".join(lines), module_count, standalone_count


def render_index(cards: list[dict[str, str]]) -> str:
    lines: list[str] = [
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

    for card in sorted(cards, key=lambda c: c["title"].lower()):
        lines.extend(
            [
                f'<a class="bd-card-link" href="./{card["slug"]}/">',
                '  <div class="bd-card">',
                f'    <h3>{card["title"]}</h3>',
                f'    <p>{card["description"]}</p>',
                f'    <p>{card["module_count"]} modules</p>',
                f'    <p>{card["standalone_count"]} standalone course reference(s)</p>',
                "  </div>",
                "</a>",
            ]
        )

    lines.extend(["</div>", ""])
    return "\n".join(lines)


def main() -> None:
    course_titles = load_course_titles()
    bundle_files = sorted(
        [p for p in BUNDLES_DIR.glob("*.md") if p.name != "index.md"],
        key=lambda p: p.name,
    )

    cards: list[dict[str, str]] = []

    for file_path in bundle_files:
        frontmatter, fm_block = parse_frontmatter(file_path)
        if not frontmatter or not fm_block:
            continue

        title = str(frontmatter.get("title", file_path.stem)).strip()
        slug = str(frontmatter.get("slug", file_path.stem)).strip()
        description = str(frontmatter.get("description", "")).strip()

        body, module_count, standalone_count = render_bundle_body(frontmatter, course_titles)
        out_file = OUTPUT_BUNDLES_DIR / file_path.name
        out_file.write_text(f"{fm_block}\n{body}", encoding="utf-8")

        cards.append(
            {
                "slug": slug,
                "title": title,
                "description": description,
                "module_count": str(module_count),
                "standalone_count": str(standalone_count),
            }
        )

    INDEX_FILE.write_text(render_index(cards), encoding="utf-8")
    print(f"Generated bundles overview + {len(cards)} detail page(s).")


if __name__ == "__main__":
    main()
