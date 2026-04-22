#!/usr/bin/env python3
"""Generate the self-study landing page from docs/all-training/self-study/*.md."""

from __future__ import annotations

import sys
import warnings
from pathlib import Path
from typing import Any

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from course_utils import display_tag

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

SELF_STUDY_DIR = Path("docs/all-training/self-study")
EVENTS_DIR = Path("docs/all-training/events")
OUTPUT_FILE = Path("docs/explore/self-study/index.md")

# ---------------------------------------------------------------------------
# Frontmatter parsing (mirrors the pattern used by generate_learning_paths.py)
# ---------------------------------------------------------------------------


def split_frontmatter(content: str) -> tuple[str, str] | tuple[None, None]:
    if not content.startswith("---"):
        return None, None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, None
    return f"---{parts[1]}---\n", parts[2].lstrip("\n")


def parse_frontmatter(md_file: Path) -> dict | None:
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


# ---------------------------------------------------------------------------
# Advert slug index (for related_event_slugs validation)
# ---------------------------------------------------------------------------


def load_advert_slugs() -> set[str]:
    slugs: set[str] = set()
    for md_file in EVENTS_DIR.rglob("*.md"):
        if md_file.name == "_template.md":
            continue
        fm = parse_frontmatter(md_file)
        if fm:
            slug = str(fm.get("slug", "")).strip()
            if slug:
                slugs.add(slug)
    return slugs


# ---------------------------------------------------------------------------
# Load self-study items
# ---------------------------------------------------------------------------


def load_items() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    seen_slugs: dict[str, Path] = {}

    for md_file in sorted(SELF_STUDY_DIR.glob("*.md")):
        if md_file.name == "_template.md":
            continue
        fm = parse_frontmatter(md_file)
        if not fm:
            warnings.warn(f"{md_file}: could not parse frontmatter — skipping")
            continue
        slug = str(fm.get("slug", "")).strip()
        if not slug:
            warnings.warn(f"{md_file}: missing `slug` — skipping")
            continue
        if slug in seen_slugs:
            warnings.warn(
                f"{md_file}: duplicate slug '{slug}' (first seen in {seen_slugs[slug]}) — skipping"
            )
            continue
        seen_slugs[slug] = md_file

        status = str(fm.get("status", "draft")).strip()
        if status != "published":
            continue  # Only render published items

        fm["_source_file"] = md_file
        items.append(fm)

    return items


# ---------------------------------------------------------------------------
# HTML rendering helpers
# ---------------------------------------------------------------------------


def resolve_card_href(item: dict[str, Any]) -> str:
    """Prefer external_url, then url, then the first material link."""
    external_url = str(item.get("external_url", "")).strip()
    if external_url:
        return external_url

    url = str(item.get("url", "")).strip()
    if url:
        return url

    materials = item.get("materials") or []
    for mat in materials:
        if isinstance(mat, dict) and mat.get("url"):
            material_url = str(mat["url"]).strip()
            if material_url:
                return material_url

    return "#"


def render_level_badge(level: str) -> str:
    normalized = level.strip().lower()
    if not normalized:
        return ""

    if normalized == "introductory":
        badge_class = "diff-beginner"
    elif normalized in {"beginner", "intermediate", "advanced"}:
        badge_class = f"diff-{normalized}"
    else:
        badge_class = "diff-beginner"

    return f'<span class="diff-badge {badge_class}">{normalized}</span>'


def render_tags(tags: object) -> list[str]:
    if not isinstance(tags, list):
        return []

    rendered_tags: list[str] = []
    for tag in tags:
        normalized = str(tag).strip()
        if not normalized or normalized == "...":
            continue
        rendered_tags.append(f'<span class="ev-tag">{display_tag(normalized)}</span>')

    return rendered_tags


def render_card(item: dict[str, Any], advert_slugs: set[str]) -> list[str]:
    title = str(item.get("title", "Untitled")).strip()
    slug = str(item.get("slug", "")).strip()
    short_desc = str(item.get("short_description", "")).strip()
    format_type = str(item.get("format", "")).strip()
    level = str(item.get("level", "")).strip()
    related_event_slugs = item.get("related_event_slugs") or []
    tags = render_tags(item.get("tags", []))

    # Validate related_event_slugs
    for rel_slug in related_event_slugs:
        if str(rel_slug).strip() not in advert_slugs:
            warnings.warn(
                f"Self-study '{slug}': related_event_slug '{rel_slug}' not found in EVENTS"
            )

    meta_parts: list[str] = []
    if format_type:
        meta_parts.append(f'<span class="ev-format">{format_type}</span>')
    if level:
        meta_parts.append(render_level_badge(level))
    meta_parts.extend(tags)

    card_href = resolve_card_href(item)

    lines: list[str] = [
        '<div class="ss-card">',
        f'  <h3 class="ss-card-title"><a href="{card_href}">{title}</a></h3>',
        f'  <p class="ss-card-desc">{short_desc}</p>' if short_desc else "",
        '  <div class="ss-card-meta">' if meta_parts else "",
        f'    {" ".join(meta_parts)}' if meta_parts else "",
        "  </div>" if meta_parts else "",
        "</div>",
    ]
    return [ln for ln in lines if ln != ""]


def render_section(heading: str, items: list[dict[str, Any]], advert_slugs: set[str]) -> list[str]:
    if not items:
        return []
    lines: list[str] = [f"## {heading}", "", '<div class="ss-card-grid">']
    for item in items:
        lines.extend(render_card(item, advert_slugs))
    lines.extend(["</div>", ""])
    return lines


# ---------------------------------------------------------------------------
# Page assembly
# ---------------------------------------------------------------------------


def render_index(items: list[dict[str, Any]], advert_slugs: set[str]) -> str:
    header = [
        "---",
        'title: "Self-Study Materials"',
        "icon: lucide/notebook-pen",
        "---",
        "",
        "# Self-Study Materials",
        "",
        "Browse tutorials, recordings, and documentation you can work through at your own pace.",
        "",
    ]

    if not items:
        no_content = [
            "!!! note",
            "    No self-study materials have been published yet.",
            "    Check back soon or browse the [Events](../events/index.md) page for upcoming training.",
            "",
        ]
        return "\n".join(header + no_content)

    # Partition: items with a related event vs. standalone
    with_event = [i for i in items if i.get("related_event_slugs")]
    standalone = [i for i in items if not i.get("related_event_slugs")]

    lines: list[str] = header

    if with_event:
        lines.extend(render_section("Related to a Scheduled Event", with_event, advert_slugs))

    if standalone:
        lines.extend(render_section("Standalone Materials", standalone, advert_slugs))

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> int:
    if not SELF_STUDY_DIR.exists():
        print(f"Warning: {SELF_STUDY_DIR} does not exist — no self-study items to process.")
        SELF_STUDY_DIR.mkdir(parents=True, exist_ok=True)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    advert_slugs = load_advert_slugs()
    items = load_items()

    if not items:
        print("No published self-study items found.")

    page = render_index(items, advert_slugs)
    OUTPUT_FILE.write_text(page, encoding="utf-8")
    print(f"Written {OUTPUT_FILE} ({len(items)} item(s)).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
