#!/usr/bin/env python3
"""Generate docs/explore/all-training/index.md with all courses and their status."""

from datetime import datetime
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from course_utils import load_courses


PAGE_PATH = Path("docs/explore/all-training/index.md")
SECTION_ORDER = ["upcoming", "past", "cancelled", "planned"]
SECTION_TITLE = {
    "upcoming": "Upcoming",
    "past": "Past",
    "cancelled": "Cancelled",
    "planned": "Planned",
}
SECTION_STATUSES = {
    "upcoming": {"upcoming"},
    "past": {"past"},
    "cancelled": {"cancelled"},
    # Keep "ongoing" visible in this section to avoid dropping entries.
    "planned": {"planned", "ongoing"},
}


def fmt_date_range(start_date: str, end_date: str) -> str:
    """Format ISO date range to a compact human-readable value."""
    if not start_date and not end_date:
        return "TBD"

    try:
        start = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
        end = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
    except ValueError:
        return "TBD"

    if start and end:
        if start.date() == end.date():
            return start.strftime("%d %b %Y")
        return f"{start.strftime('%d %b %Y')} - {end.strftime('%d %b %Y')}"
    if start:
        return start.strftime("%d %b %Y")
    return end.strftime("%d %b %Y")


def status_badge(status: str) -> str:
    """Render status as an ev-* badge."""
    normalized = (status or "unknown").strip().lower()
    if normalized in {"upcoming", "ongoing", "past", "cancelled"}:
        return f'<span class="ev-badge ev-badge-{normalized}">{normalized}</span>'
    return f'<span class="ev-format">{normalized or "unknown"}</span>'


def level_badge(level: str) -> str:
    """Render level using diff-* badge if present."""
    normalized = (level or "").strip().lower()
    if normalized in {"beginner", "intermediate", "advanced"}:
        return f'<span class="diff-badge diff-{normalized}">{normalized}</span>'
    return "-"


def collect_rows() -> list[dict]:
    """Collect normalized course rows for rendering."""
    rows = []
    for course in load_courses():
        fm = course["frontmatter"]
        rows.append(
            {
                "title": course["title"],
                "file": course["link"].split("/")[-1],
                "status": (fm.get("status") or "unknown").strip().lower(),
                "format": (fm.get("format") or "-").strip().lower() or "-",
                "level": fm.get("level", ""),
                "dates": fmt_date_range(
                    (fm.get("start_date") or "").strip(),
                    (fm.get("end_date") or "").strip(),
                ),
            }
        )

    rows.sort(key=lambda r: r["title"].lower())
    return rows


def build_body(rows: list[dict]) -> str:
    """Build page body markdown."""
    section_counts = {section: 0 for section in SECTION_ORDER}
    other_count = 0
    for row in rows:
        placed = False
        for section in SECTION_ORDER:
            if row["status"] in SECTION_STATUSES[section]:
                section_counts[section] += 1
                placed = True
                break
        if not placed:
            other_count += 1

    body = "# All Training\n\n"
    body += "Complete list of training material with current publication status.\n\n"
    body += f"**Total courses:** {len(rows)}  \n"
    body += (
        f"**Status breakdown:** upcoming {section_counts['upcoming']}, "
        f"past {section_counts['past']}, "
        f"cancelled {section_counts['cancelled']}, "
        f"planned {section_counts['planned']}"
    )
    if other_count:
        body += f", other {other_count}"
    body += "\n\n"

    for section in SECTION_ORDER:
        body += f"## {SECTION_TITLE[section]}\n\n"
        section_rows = [
            row
            for row in rows
            if row["status"] in SECTION_STATUSES[section]
        ]

        if not section_rows:
            body += "No courses currently in this status.\n\n"
            continue

        body += "| Course | Status | Level | Format | Dates |\n"
        body += "| --- | --- | --- | --- | --- |\n"
        for row in section_rows:
            body += (
                f"| [{row['title']}]({row['file']}) "
                f"| {status_badge(row['status'])} "
                f"| {level_badge(row['level'])} "
                f"| {row['format']} "
                f"| {row['dates']} |\n"
            )
        body += "\n"

    return body


def split_frontmatter(content: str) -> tuple[str, str]:
    """Split markdown into frontmatter and body."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm = "---" + parts[1] + "---"
            return fm, parts[2]
    return "", content


def write_page(body: str) -> None:
    """Write page while preserving frontmatter."""
    if PAGE_PATH.exists():
        current = PAGE_PATH.read_text(encoding="utf-8")
        frontmatter, _old_body = split_frontmatter(current)
    else:
        frontmatter = "---\nicon: lucide/book-open\n---"

    PAGE_PATH.write_text(f"{frontmatter}\n{body}", encoding="utf-8")


def main() -> None:
    rows = collect_rows()
    write_page(build_body(rows))
    print(f"Updated {PAGE_PATH} with {len(rows)} courses.")


if __name__ == "__main__":
    main()