#!/usr/bin/env python3
"""Generate scientific domain overview + subpages from advert frontmatter."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import yaml

from lucide_icons import render_lucide_icon

ADVERTS_DIR = Path("docs/all-training/adverts")
OUTPUT_DIR = Path("docs/explore/scientific-domains")
INDEX_FILE = OUTPUT_DIR / "index.md"

DOMAIN_ICON_KEYS: dict[str, str] = {
    "ai": "brain",
    "big-data": "database",
    "bioinformatics": "file-terminal",
    "biomedical": "heart-pulse",
    "climate-science": "earth",
    "clinical-research": "stethoscope",
    "computational-biology": "leaf",
    "computational-chemistry": "flask-conical",
    "computational-physics": "magnet",
    "computational-science": "code-2",
    "data-science": "chart-line",
    "engineering": "circuit-board",
    "general-hpc": "computer",
    "genomics": "dna",
    "machine-learning": "text-search",
    "social-sciences": "message-circle-check",
    "statistics": "chart-scatter",
}

DOMAIN_META: dict[str, dict[str, str]] = {
    "ai": {"title": "AI"},
    "big-data": {"title": "Big Data"},
    "bioinformatics": {"title": "Bioinformatics"},
    "biomedical": {"title": "Biomedical"},
    "climate-science": {"title": "Climate Science"},
    "clinical-research": {"title": "Clinical Research"},
    "computational-biology": {"title": "Computational Biology"},
    "computational-chemistry": {"title": "Computational Chemistry"},
    "computational-physics": {"title": "Computational Physics"},
    "computational-science": {"title": "Computational Science"},
    "data-science": {"title": "Data Science"},
    "engineering": {"title": "Engineering"},
    "general-hpc": {"title": "General HPC"},
    "genomics": {"title": "Genomics"},
    "machine-learning": {"title": "Machine Learning"},
    "social-sciences": {"title": "Social Sciences"},
    "statistics": {"title": "Statistics"},
}

DOMAIN_ORDER = list(DOMAIN_META.keys())


def parse_frontmatter(md_file: Path) -> dict | None:
    content = md_file.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return None

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None

    try:
        frontmatter = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None

    return frontmatter if isinstance(frontmatter, dict) else None


def iter_advert_files() -> list[Path]:
    files: list[Path] = []
    for md_file in sorted(ADVERTS_DIR.rglob("*.md")):
        if md_file.name == "_template.md":
            continue
        files.append(md_file)
    return files


def resolve_course_url(frontmatter: dict, slug: str) -> str:
    url_value = frontmatter.get("url")
    if isinstance(url_value, str):
        value = url_value.strip()
        if value:
            if value.startswith(("http://", "https://", "/")):
                return value
            return f"/{value}"
    return f"/explore/training-catalogue/{slug}/"


def load_domain_courses() -> tuple[dict[str, list[dict]], set[str]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    seen_domains: set[str] = set()

    for md_file in iter_advert_files():
        frontmatter = parse_frontmatter(md_file)
        if not frontmatter:
            continue

        title = str(frontmatter.get("title", "")).strip()
        slug = str(frontmatter.get("slug", "")).strip()
        domains = frontmatter.get("scientific_domains", [])

        if not title or not slug or not isinstance(domains, list):
            continue

        course = {
            "title": title,
            "slug": slug,
            "url": resolve_course_url(frontmatter, slug),
        }

        for item in domains:
            domain_slug = str(item).strip()
            if not domain_slug or domain_slug == "...":
                continue
            seen_domains.add(domain_slug)
            grouped[domain_slug].append(course)

    for domain_slug in grouped:
        grouped[domain_slug].sort(key=lambda c: c["title"].lower())

    return grouped, seen_domains


def humanize_slug(value: str) -> str:
    return value.replace("-", " ").title()


def ensure_domain_meta(domain_slug: str) -> None:
    if domain_slug not in DOMAIN_META:
        DOMAIN_META[domain_slug] = {"title": humanize_slug(domain_slug)}


def write_index(grouped: dict[str, list[dict]], domains: list[str]) -> None:
    lines: list[str] = [
        "---",
        'title: "Scientific Domains"',
        "icon: lucide/atom",
        "---",
        "",
        "# Scientific Domains",
        "",
        "Explore training courses organized by scientific domain:",
        "",
        '<div class="sd-card-grid">',
    ]

    for domain_slug in domains:
        title = DOMAIN_META[domain_slug]["title"]
        icon_key = DOMAIN_ICON_KEYS.get(domain_slug, "atom")
        icon_svg = render_lucide_icon(icon_key, fallback_icon="atom", size_class="sd-card-icon-svg")
        count = len(grouped.get(domain_slug, []))
        course_label = "course" if count == 1 else "courses"
        lines.extend(
            [
                f'<a class="sd-card-link" href="./{domain_slug}/">',
                '  <div class="sd-card">',
                f'    <div class="sd-card-icon">{icon_svg}</div>',
                f'    <h3 class="sd-card-title">{title}</h3>',
                f'    <p class="sd-card-meta">{count} {course_label}</p>',
                "  </div>",
                "</a>",
            ]
        )

    lines.extend(["</div>", ""])
    INDEX_FILE.write_text("\n".join(lines), encoding="utf-8")


def write_domain_page(domain_slug: str, courses: list[dict]) -> None:
    title = DOMAIN_META[domain_slug]["title"]
    lines: list[str] = [
        "---",
        f'title: "{title}"',
        "---",
        "",
        f"# {title}",
        "",
        f"Courses tagged under {title}:",
        "",
    ]

    if courses:
        for course in courses:
            lines.append(f'- [{course["title"]}]({course["url"]})')
    else:
        lines.append("No courses currently mapped to this domain.")

    lines.extend(["", "[Back to Scientific Domains Overview](./index.md)", ""])

    out_file = OUTPUT_DIR / f"{domain_slug}.md"
    out_file.write_text("\n".join(lines), encoding="utf-8")


def cleanup_stale_domain_pages(expected: set[str]) -> None:
    for file_path in OUTPUT_DIR.glob("*.md"):
        if file_path.name == "index.md":
            continue
        if file_path.stem not in expected:
            file_path.unlink()


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    grouped, seen_domains = load_domain_courses()

    for domain_slug in seen_domains:
        ensure_domain_meta(domain_slug)

    ordered = [slug for slug in DOMAIN_ORDER if slug in DOMAIN_META]
    for domain_slug in sorted(seen_domains):
        if domain_slug not in ordered:
            ordered.append(domain_slug)

    write_index(grouped, ordered)

    expected_pages: set[str] = set()
    for domain_slug in ordered:
        write_domain_page(domain_slug, grouped.get(domain_slug, []))
        expected_pages.add(domain_slug)

    cleanup_stale_domain_pages(expected_pages)
    print(
        f"Generated scientific domains overview + {len(expected_pages)} subpage(s)."
    )


if __name__ == "__main__":
    main()
