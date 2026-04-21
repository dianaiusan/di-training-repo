#!/usr/bin/env python3
"""Generate the self-study landing page from docs/all-training/self-study/*.md."""

from __future__ import annotations

import sys
import warnings
from pathlib import Path
from typing import Any

import yaml

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

SELF_STUDY_DIR = Path("all-training-input/self-study")
ADVERTS_DIR = Path("all-training-input/events")
OUTPUT_FILE = Path("docs/explore/self-study/index.md")

# ---------------------------------------------------------------------------
# Icon map — lucide icon name per kind
# ---------------------------------------------------------------------------

KIND_ICONS: dict[str, str] = {
    "tutorial": "graduation-cap",
    "external-docs": "external-link",
    "recording": "video",
    "exercise-set": "flask-conical",
    "reading": "book-open",
}
DEFAULT_ICON = "book-open"

KIND_LABELS: dict[str, str] = {
    "tutorial": "Tutorial",
    "external-docs": "External Docs",
    "recording": "Recording",
    "exercise-set": "Exercises",
    "reading": "Reading",
}

MATERIAL_TYPE_LABELS: dict[str, str] = {
    "slides": "Slides",
    "video": "Video",
    "recording": "Recording",
    "notebook": "Notebook",
    "exercises": "Exercises",
    "external-docs": "Docs",
    "code": "Code",
    "other": "Link",
}

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
    for md_file in ADVERTS_DIR.rglob("*.md"):
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


def _badge(css_class: str, text: str) -> str:
    return f'<span class="ss-badge ss-badge--{css_class}">{text}</span>'


def _level_badge(level: str) -> str:
    level = level.strip().lower() if level else ""
    labels = {
        "introductory": ("intro", "Introductory"),
        "beginner": ("beginner", "Beginner"),
        "intermediate": ("intermediate", "Intermediate"),
        "advanced": ("advanced", "Advanced"),
    }
    css, label = labels.get(level, ("beginner", level.title() or "Beginner"))
    return _badge(f"level-{css}", label)


def _kind_badge(kind: str) -> str:
    kind = kind.strip().lower() if kind else "tutorial"
    label = KIND_LABELS.get(kind, kind.title())
    return _badge(f"kind-{kind}", label)


def _time_badge(estimated_time: str) -> str:
    return _badge("time", f"&#128336; {estimated_time}")


def _material_links(materials: list) -> str:
    if not materials:
        return ""
    parts: list[str] = []
    for mat in materials:
        if not isinstance(mat, dict):
            continue
        mat_type = str(mat.get("type", "other")).strip()
        mat_title = str(mat.get("title", MATERIAL_TYPE_LABELS.get(mat_type, "Link"))).strip()
        mat_url = str(mat.get("url", "")).strip()
        if not mat_url:
            continue
        label = MATERIAL_TYPE_LABELS.get(mat_type, mat_title)
        parts.append(
            f'<a class="ss-material-link ss-material-link--{mat_type}" href="{mat_url}">{label}</a>'
        )
    if not parts:
        return ""
    return '<div class="ss-material-links">' + "".join(parts) + "</div>"


def render_card(item: dict[str, Any], advert_slugs: set[str]) -> list[str]:
    title = str(item.get("title", "Untitled")).strip()
    slug = str(item.get("slug", "")).strip()
    short_desc = str(item.get("short_description", "")).strip()
    kind = str(item.get("kind", "tutorial")).strip()
    level = str(item.get("level", "")).strip()
    estimated_time = str(item.get("estimated_time", "")).strip()
    has_recording = bool(item.get("has_recording", False))
    url = str(item.get("url", "")).strip()
    materials = item.get("materials") or []
    related_event_slugs = item.get("related_event_slugs") or []
    external_only = bool(item.get("external_only", False))

    # Validate related_event_slugs
    for rel_slug in related_event_slugs:
        if str(rel_slug).strip() not in advert_slugs:
            warnings.warn(
                f"Self-study '{slug}': related_event_slug '{rel_slug}' not found in adverts"
            )

    # Determine card href
    if url:
        card_href = url
    elif materials:
        first_url = ""
        for mat in materials:
            if isinstance(mat, dict) and mat.get("url"):
                first_url = str(mat["url"]).strip()
                break
        card_href = first_url or "#"
    else:
        card_href = "#"

    icon_name = str(item.get("icon", KIND_ICONS.get(kind, DEFAULT_ICON))).strip()
    # Strip lucide/ prefix if present (template stores bare name already, but be defensive)
    if icon_name.startswith("lucide/"):
        icon_name = icon_name[7:]

    lines: list[str] = [
        f'<div class="ss-card">',
        f'  <div class="ss-card-header">',
        f'    <div class="ss-card-badges">',
        f"      {_kind_badge(kind)}",
        f"      {_level_badge(level)}" if level else "",
        f"      {_time_badge(estimated_time)}" if estimated_time else "",
        f'      {_badge("recording", "&#127909; Recording")}' if has_recording else "",
        f"    </div>",
        f'    <h3 class="ss-card-title"><a href="{card_href}">{title}</a></h3>',
        f'    <p class="ss-card-desc">{short_desc}</p>' if short_desc else "",
        f"  </div>",
    ]

    mat_html = _material_links(materials if isinstance(materials, list) else [])
    if mat_html:
        lines.append(f'  <div class="ss-card-footer">{mat_html}</div>')

    if related_event_slugs:
        rel_links = ", ".join(
            f'<a href="/explore/training-catalogue/{str(rs).strip()}/">{str(rs).strip()}</a>'
            for rs in related_event_slugs
            if str(rs).strip()
        )
        lines.append(
            f'  <div class="ss-card-related">Related event: {rel_links}</div>'
        )

    lines.append("</div>")
    # Remove empty strings (from conditional empty lines)
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
