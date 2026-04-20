#!/usr/bin/env python3
"""
Generate Scientific Domains overview and per-domain pages.
"""

from pathlib import Path
from collections import defaultdict
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from course_utils import load_courses
from link_utils import (
    scientific_domains_overview_to_domain_route,
    scientific_domain_detail_to_course_md,
)

OUTPUT_DIR = Path("docs/explore/scientific-domains")
OVERVIEW_FILE = OUTPUT_DIR / "index.md"

DOMAIN_ICON_KEYS = {
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

LUCIDE_PATHS = {
    "atom": '<circle cx="12" cy="12" r="1"/><path d="M20.2 20.2c2.04-2.03.02-7.36-4.5-11.9-4.54-4.52-9.87-6.54-11.9-4.5-2.04 2.03-.02 7.36 4.5 11.9 4.54 4.52 9.87 6.54 11.9 4.5"/><path d="M15.7 15.7c4.52-4.54 6.54-9.87 4.5-11.9-2.03-2.04-7.36-.02-11.9 4.5-4.52 4.54-6.54 9.87-4.5 11.9 2.03 2.04 7.36.02 11.9-4.5"/>',
    "brain": '<path d="M12 18V5"/><path d="M15 13a4.17 4.17 0 0 1-3-4 4.17 4.17 0 0 1-3 4"/><path d="M17.598 6.5A3 3 0 1 0 12 5a3 3 0 1 0-5.598 1.5"/><path d="M17.997 5.125a4 4 0 0 1 2.526 5.77"/><path d="M18 18a4 4 0 0 0 2-7.464"/><path d="M19.967 17.483A4 4 0 1 1 12 18a4 4 0 1 1-7.967-.517"/><path d="M6 18a4 4 0 0 1-2-7.464"/><path d="M6.003 5.125a4 4 0 0 0-2.526 5.77"/>',
    "earth": '<path d="M21.54 15H17a2 2 0 0 0-2 2v4.54"/><path d="M7 3.34V5a3 3 0 0 0 3 3a2 2 0 0 1 2 2c0 1.1.9 2 2 2a2 2 0 0 0 2-2c0-1.1.9-2 2-2h3.17"/><path d="M11 21.95V18a2 2 0 0 0-2-2a2 2 0 0 1-2-2v-1a2 2 0 0 0-2-2H2.05"/><circle cx="12" cy="12" r="10"/>',
    "flask-conical": '<path d="M14 2v6a2 2 0 0 0 .245.96l5.51 10.08A2 2 0 0 1 18 22H6a2 2 0 0 1-1.755-2.96l5.51-10.08A2 2 0 0 0 10 8V2"/><path d="M6.453 15h11.094"/><path d="M8.5 2h7"/>',
    "heart-pulse": '<path d="M2 9.5a5.5 5.5 0 0 1 9.591-3.676.56.56 0 0 0 .818 0A5.49 5.49 0 0 1 22 9.5c0 2.29-1.5 4-3 5.5l-5.492 5.313a2 2 0 0 1-3 .019L5 15c-1.5-1.5-3-3.2-3-5.5"/><path d="M3.22 13H9.5l.5-1 2 4.5 2-7 1.5 3.5h5.27"/>',
    "magnet": '<path d="m12 15 4 4"/><path d="M2.352 10.648a1.205 1.205 0 0 0 0 1.704l2.296 2.296a1.205 1.205 0 0 0 1.704 0l6.029-6.029a1 1 0 1 1 3 3l-6.029 6.029a1.205 1.205 0 0 0 0 1.704l2.296 2.296a1.205 1.205 0 0 0 1.704 0l6.365-6.367A1 1 0 0 0 8.716 4.282z"/><path d="m5 8 4 4"/>',
    "route": '<circle cx="6" cy="19" r="3"/><path d="M9 19h8.5a3.5 3.5 0 0 0 0-7h-11a3.5 3.5 0 0 1 0-7H15"/><circle cx="18" cy="5" r="3"/>',
    "stethoscope": '<path d="M11 2v2"/><path d="M5 2v2"/><path d="M5 3H4a2 2 0 0 0-2 2v4a6 6 0 0 0 12 0V5a2 2 0 0 0-2-2h-1"/><path d="M8 15a6 6 0 0 0 12 0v-3"/><circle cx="20" cy="10" r="2"/>',
    "compass": '<circle cx="12" cy="12" r="10"/><path d="m16.24 7.76-1.804 5.411a2 2 0 0 1-1.265 1.265L7.76 16.24l1.804-5.411a2 2 0 0 1 1.265-1.265z"/>',
    "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>',
    "file-terminal": '<path d="M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z"/><path d="M14 2v5a1 1 0 0 0 1 1h5"/><path d="m8 16 2-2-2-2"/><path d="M12 18h4"/>',
    "circuit-board": '<rect width="18" height="18" x="3" y="3" rx="2"/><path d="M11 9h4a2 2 0 0 0 2-2V3"/><circle cx="9" cy="9" r="2"/><path d="M7 21v-4a2 2 0 0 1 2-2h4"/><circle cx="15" cy="15" r="2"/>',
    "battery-charging": '<path d="m11 7-3 5h4l-3 5"/><path d="M14.856 6H16a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-2.935"/><path d="M22 14v-4"/><path d="M5.14 18H4a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h2.936"/>',

    "sprout": '<path d="M14 9.536V7a4 4 0 0 1 4-4h1.5a.5.5 0 0 1 .5.5V5a4 4 0 0 1-4 4 4 4 0 0 0-4 4c0 2 1 3 1 5a5 5 0 0 1-1 3M4 9a5 5 0 0 1 8 4 5 5 0 0 1-8-4M5 21h14"/>',

    "code-2": '<path d="m18 16 4-4-4-4M6 8l-4 4 4 4M14.5 4l-5 16"/>',
    "chart-line": '<path d="M3 3v16a2 2 0 0 0 2 2h16"/><path d="m19 9-5 5-4-4-3 3"/>',
    "chart-scatter": '<circle cx="7.5" cy="7.5" r=".5" fill="currentColor"/><circle cx="18.5" cy="5.5" r=".5" fill="currentColor"/><circle cx="11.5" cy="11.5" r=".5" fill="currentColor"/><circle cx="7.5" cy="16.5" r=".5" fill="currentColor"/><circle cx="17.5" cy="14.5" r=".5" fill="currentColor"/><path d="M3 3v16a2 2 0 0 0 2 2h16"/>',
    "message-circle-check": '<path d="M2.992 16.342a2 2 0 0 1 .094 1.167l-1.065 3.29a1 1 0 0 0 1.236 1.168l3.413-.998a2 2 0 0 1 1.099.092 10 10 0 1 0-4.777-4.719"/><path d="m9 12 2 2 4-4"/>',
    "text-search": '<path d="M21 5H3"/><path d="M10 12H3"/><path d="M10 19H3"/><circle cx="17" cy="15" r="3"/><path d="m21 19-1.9-1.9"/>',
    "computer": '<rect width="14" height="8" x="5" y="2" rx="2"/><rect width="20" height="8" x="2" y="14" rx="2"/><path d="M6 18h2"/><path d="M12 18h6"/>',
    "database": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 0 21 19V5"/><path d="M3 12A9 3 0 0 0 21 12"/>',
    "tag": '<path d="M12.586 2.586A2 2 0 0 0 11.172 2H4a2 2 0 0 0-2 2v7.172a2 2 0 0 0 .586 1.414l8.704 8.704a2.426 2.426 0 0 0 3.42 0l6.58-6.58a2.426 2.426 0 0 0 0-3.42z"/><circle cx="7.5" cy="7.5" r=".5" fill="currentColor"/>',
    "dna": '<path d="m10 16 1.5 1.5M14 8l-1.5-1.5M15 2c-1.798 1.998-2.518 3.995-2.807 5.993M16.5 10.5l1 1M17 6l-2.891-2.891M2 15c6.667-6 13.333 0 20-6M20 9l.891.891M3.109 14.109 4 15M6.5 12.5l1 1M7 18l2.891 2.891M9 22c1.798-1.998 2.518-3.995 2.807-5.993"/>',
}


def domain_slug(domain):
    return re.sub(r"[^a-z0-9]+", "-", str(domain).lower()).strip("-")


def domain_title(domain):
    """Normalize domain labels for headings/navigation."""
    title = str(domain).replace("-", " ").title()
    title = title.replace("Ai", "AI").replace("Hpc", "HPC")
    return title


def ensure_output_dir():
    """Migrate legacy single-file output to directory output."""
    legacy_file = Path("docs/explore/scientific-domains.md")
    if legacy_file.exists() and legacy_file.is_file():
        legacy_file.unlink()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def render_lucide_icon(icon_name, size_class="sd-card-icon-svg"):
    """Render an inline lucide SVG."""
    icon_key = str(icon_name or "atom")
    svg_paths = LUCIDE_PATHS.get(icon_key, LUCIDE_PATHS["atom"])
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" '
        f'stroke-linecap="round" stroke-linejoin="round" stroke-width="2" '
        f'class="lucide lucide-{icon_key} {size_class}" viewBox="0 0 24 24">{svg_paths}</svg>'
    )


def render_domain_card_grid(domains):
    """Render scientific domains as cards for overview browsing."""
    if not domains:
        return ""

    cards = []
    cards.append('<div class="sd-card-grid">')

    for domain in sorted(domains.keys()):
        slug = domain_slug(domain)
        label = domain_title(domain)
        icon_key = DOMAIN_ICON_KEYS.get(slug, "atom")
        icon_svg = render_lucide_icon(icon_key)
        href = scientific_domains_overview_to_domain_route(slug)
        count = len(domains[domain])
        unit = "course" if count == 1 else "courses"

        cards.append(
            f'<a class="sd-card-link" href="{href}">\n'
            f'  <div class="sd-card">\n'
            f'    <div class="sd-card-icon">{icon_svg}</div>\n'
            f'    <h3 class="sd-card-title">{label}</h3>\n'
            f'    <p class="sd-card-meta">{count} {unit}</p>\n'
            f"  </div>\n"
            f"</a>"
        )

    cards.append("</div>")
    return "\n".join(cards)

def generate_domains_dict():
    """Generate dictionary of scientific domains and their courses."""
    domains = defaultdict(list)

    for course in load_courses():
        frontmatter = course["frontmatter"]
        if "scientific_domains" in frontmatter:
            for domain in frontmatter["scientific_domains"]:
                domains[domain].append({
                    "title": course["title"],
                    "slug": course["slug"],
                    "link": course["link"],
                })

    for domain in domains:
        domains[domain].sort(key=lambda x: x["title"])

    return domains


def update_domains_overview(domains):
    """Write overview page linking to all domain pages."""
    body = [
        "---",
        'title: "Scientific Domains"',
        'icon: lucide/atom',
        "---",
        "",
        "# Scientific Domains",
        "",
    ]

    if domains:
        body.append("Explore training courses organized by scientific domain:")
        body.append("")
        body.append(render_domain_card_grid(domains))
        body.append("")
    else:
        body.append("No courses with scientific domains found.")
        body.append("")

    with open(OVERVIEW_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(body))


def update_domain_pages(domains):
    """Write one markdown page per domain."""
    generated_files = set()

    for domain in sorted(domains.keys()):
        slug = domain_slug(domain)
        label = domain_title(domain)
        domain_file = OUTPUT_DIR / f"{slug}.md"
        generated_files.add(domain_file.name)

        lines = [
            "---",
            f'title: "{label}"',
            "---",
            "",
            f"# {label}",
            "",
            f"Courses tagged under {label}:",
            "",
        ]

        for course in domains[domain]:
            lines.append(
                f"- [{course['title']}]({scientific_domain_detail_to_course_md(course['slug'])})"
            )

        lines.append("")
        lines.append("[Back to Scientific Domains Overview](./index.md)")
        lines.append("")

        with open(domain_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    for md_file in OUTPUT_DIR.glob("*.md"):
        if md_file.name != "index.md" and md_file.name not in generated_files:
            md_file.unlink()

def update_domains_pages(domains):
    ensure_output_dir()
    update_domains_overview(domains)
    update_domain_pages(domains)

    total_courses = sum(len(courses) for courses in domains.values())
    print(
        f"Updated {OVERVIEW_FILE} and {len(domains)} domain page(s) with {total_courses} course entries."
    )

if __name__ == "__main__":
    domains = generate_domains_dict()
    update_domains_pages(domains)