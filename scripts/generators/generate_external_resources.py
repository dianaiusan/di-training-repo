#!/usr/bin/env python3
"""Generate docs/external-resources.md from docs/all-training/external/*.md."""

from __future__ import annotations

import warnings
from pathlib import Path
from typing import Any

import yaml

from lucide_icons import render_lucide_img

SOURCE_DIR = Path("docs/all-training/external")
OUTPUT_FILE = Path("docs/external-resources.md")

RESOURCE_TYPE_ORDER = [
    "provider",
    "recordings",
    "tutorials",
    "domain-specific",
]

RESOURCE_TYPE_LABELS = {
    "provider": "Training Providers",
    "recordings": "Recorded Workshops & Materials",
    "tutorials": "Tutorial Collections",
    "domain-specific": "Domain-Specific Resources",
}

RESOURCE_TYPE_DEFAULT_ICONS = {
    "provider": "earth",
    "recordings": "images",
    "tutorials": "computer",
    "domain-specific": "database",
}


def split_frontmatter(content: str) -> tuple[str, str] | tuple[None, None]:
    if not content.startswith("---"):
        return None, None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, None
    return f"---{parts[1]}---\n", parts[2].lstrip("\n")



def parse_frontmatter(md_file: Path) -> dict[str, Any] | None:
    content = md_file.read_text(encoding="utf-8")
    fm_block, _ = split_frontmatter(content)
    if fm_block is None:
        return None
    try:
        data = yaml.safe_load(fm_block.strip("-\n"))
    except yaml.YAMLError as exc:
        warnings.warn(f"{md_file}: YAML parse error — {exc}")
        return None
    return data if isinstance(data, dict) else None



def load_resources() -> list[dict[str, str]]:
    resources: list[dict[str, str]] = []
    seen_slugs: set[str] = set()

    for md_file in sorted(SOURCE_DIR.glob("*.md")):
        if md_file.name == "_template.md":
            continue

        frontmatter = parse_frontmatter(md_file)
        if not frontmatter:
            warnings.warn(f"{md_file}: could not parse frontmatter — skipping")
            continue

        slug = str(frontmatter.get("slug", "")).strip()
        title = str(frontmatter.get("title", "")).strip()
        url = str(frontmatter.get("url", "")).strip()
        short_description = str(frontmatter.get("short_description", "")).strip()
        resource_type = str(frontmatter.get("resource_type", "provider")).strip()
        status = str(frontmatter.get("status", "draft")).strip()
        icon = str(frontmatter.get("icon", "")).strip()
        audience = str(frontmatter.get("audience", "")).strip()

        if status != "published":
            continue
        if not slug or not title or not url:
            warnings.warn(f"{md_file}: requires slug, title, and url — skipping")
            continue
        if slug in seen_slugs:
            warnings.warn(f"{md_file}: duplicate slug '{slug}' — skipping")
            continue

        seen_slugs.add(slug)
        resources.append(
            {
                "slug": slug,
                "title": title,
                "url": url,
                "short_description": short_description,
                "resource_type": resource_type,
                "icon": icon,
                "audience": audience,
            }
        )

    resources.sort(key=lambda item: (RESOURCE_TYPE_ORDER.index(item["resource_type"]) if item["resource_type"] in RESOURCE_TYPE_ORDER else len(RESOURCE_TYPE_ORDER), item["title"].lower()))
    return resources



def render_card(resource: dict[str, str]) -> list[str]:
    icon_name = resource["icon"] or RESOURCE_TYPE_DEFAULT_ICONS.get(resource["resource_type"], "earth")
    icon_img = render_lucide_img(
        icon_name,
        fallback_icon="earth",
        size_class="ev-landing-icon-img",
        src_prefix="./assets/images/icons",
    )

    lines = [
        f'<a class="ev-landing-card" href="{resource["url"]}">',
        f'  <div class="ev-landing-icon">{icon_img}</div>',
        f'  <h2>{resource["title"]}</h2>',
    ]

    description = resource["short_description"]
    if resource["audience"]:
        audience_text = f'Audience: {resource["audience"]}'
        description = f'{description} {audience_text}'.strip()

    if description:
        lines.append(f'  <p>{description}</p>')
    else:
        lines.append('  <p></p>')

    lines.append("</a>")
    return lines



def render_section(heading: str, resources: list[dict[str, str]]) -> list[str]:
    if not resources:
        return []

    lines = [f"## {heading}", "", '<div class="ev-landing-grid">']
    for resource in resources:
        lines.extend(render_card(resource))
        lines.append("")
    lines.extend(["</div>", ""])
    return lines



def render_page(resources: list[dict[str, str]]) -> str:
    lines: list[str] = [
        "---",
        "icon: lucide/external-link",
        "---",
        "",
        "# External Training Resources",
        "",
        "Links to external training materials and providers that complement the NAISS training catalogue.",
        "",
    ]

    if not resources:
        lines.extend([
            "No external resources have been published yet.",
            "",
        ])
        return "\n".join(lines)

    for resource_type in RESOURCE_TYPE_ORDER:
        matching = [item for item in resources if item["resource_type"] == resource_type]
        lines.extend(render_section(RESOURCE_TYPE_LABELS[resource_type], matching))

    extras = [item for item in resources if item["resource_type"] not in RESOURCE_TYPE_ORDER]
    if extras:
        lines.extend(render_section("Other External Resources", extras))

    return "\n".join(lines)



def main() -> int:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    resources = load_resources()
    OUTPUT_FILE.write_text(render_page(resources) + "\n", encoding="utf-8")
    print(f"Written {OUTPUT_FILE} ({len(resources)} resource(s)).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
