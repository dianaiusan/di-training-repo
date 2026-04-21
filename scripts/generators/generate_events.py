#!/usr/bin/env python3
"""Generate docs/events/upcoming.md and docs/events/past-events.md from advert frontmatter."""

from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
import sys

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from course_utils import display_tag

ADVERTS_DIR = Path("docs/all-training/adverts")
UPCOMING_PAGE = Path("docs/events/upcoming.md")
PAST_PAGE = Path("docs/events/past-events.md")


def parse_iso_date(value: str | None) -> date | None:
    """Parse an ISO date string safely."""
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def format_date_range(start_date: date, end_date: date) -> str:
    """Format date range for display."""
    if start_date == end_date:
        return start_date.strftime("%e %B %Y").strip()
    if start_date.month == end_date.month and start_date.year == end_date.year:
        return f"{start_date.day} - {end_date.strftime('%e %B %Y').strip()}"
    return f"{start_date.strftime('%e %B').strip()} - {end_date.strftime('%e %B %Y').strip()}"


def parse_dates_field(value: object) -> list[date]:
    """Parse the optional explicit dates frontmatter field."""
    if isinstance(value, str):
        parsed = parse_iso_date(value)
        return [parsed] if parsed else []

    if not isinstance(value, list):
        return []

    parsed_dates: list[date] = []
    seen: set[date] = set()
    for item in value:
        if not isinstance(item, str):
            continue
        parsed = parse_iso_date(item)
        if parsed and parsed not in seen:
            parsed_dates.append(parsed)
            seen.add(parsed)

    return sorted(parsed_dates)


def group_consecutive_dates(explicit_dates: list[date]) -> list[tuple[date, date]]:
    """Group explicit dates into consecutive runs."""
    if not explicit_dates:
        return []

    groups = []
    run_start = explicit_dates[0]
    run_end = explicit_dates[0]

    for current in explicit_dates[1:]:
        if current.toordinal() == run_end.toordinal() + 1:
            run_end = current
            continue
        groups.append((run_start, run_end))
        run_start = current
        run_end = current

    groups.append((run_start, run_end))
    return groups


def format_explicit_dates(explicit_dates: list[date]) -> str:
    """Format explicit event dates while preserving gaps in the schedule."""
    if not explicit_dates:
        return ""
    if len(explicit_dates) == 1:
        return explicit_dates[0].strftime("%e %B %Y").strip()

    groups = group_consecutive_dates(explicit_dates)
    same_year = all(item.year == explicit_dates[0].year for item in explicit_dates)
    same_month = same_year and all(
        item.month == explicit_dates[0].month for item in explicit_dates
    )

    if same_month:
        segments = []
        for start_group, end_group in groups:
            if start_group == end_group:
                segments.append(f"{start_group.day}")
            else:
                segments.append(f"{start_group.day}-{end_group.day}")
        return f"{', '.join(segments)} {explicit_dates[0].strftime('%B %Y')}"

    if same_year:
        segments = []
        for start_group, end_group in groups:
            if start_group == end_group:
                segments.append(start_group.strftime("%e %B").strip())
            elif start_group.month == end_group.month:
                segments.append(
                    f"{start_group.day}-{end_group.day} {start_group.strftime('%B')}"
                )
            else:
                segments.append(
                    f"{start_group.strftime('%e %B').strip()} - {end_group.strftime('%e %B').strip()}"
                )
        return f"{', '.join(segments)} {explicit_dates[0].year}"

    segments = []
    for start_group, end_group in groups:
        if start_group == end_group:
            segments.append(start_group.strftime("%e %B %Y").strip())
        else:
            segments.append(
                f"{start_group.strftime('%e %B %Y').strip()} - {end_group.strftime('%e %B %Y').strip()}"
            )
    return ", ".join(segments)


def format_event_dates(start_date: date, end_date: date, explicit_dates: list[date]) -> str:
    """Format event dates, preferring explicit frontmatter dates when available."""
    if explicit_dates:
        return format_explicit_dates(explicit_dates)
    return format_date_range(start_date, end_date)


def resolve_event_url(url_value: object, slug: str) -> str:
    """Resolve preferred URL for card links with sane fallbacks."""
    if isinstance(url_value, str):
        url = url_value.strip()
        if url:
            if url.startswith(("http://", "https://", "/")):
                return url
            return f"/{url}"

    return f"/explore/training-catalogue/{slug}/"


def parse_frontmatter(md_file: Path) -> dict | None:
    """Parse YAML frontmatter from a markdown file."""
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

    if not isinstance(frontmatter, dict):
        return None

    return frontmatter


def iter_advert_files() -> list[Path]:
    """Collect all advert markdown files except templates."""
    files: list[Path] = []
    for md_file in sorted(ADVERTS_DIR.rglob("*.md")):
        if md_file.name == "_template.md":
            continue
        files.append(md_file)
    return files


def load_adverts() -> tuple[list[dict], list[str]]:
    """Load advert metadata needed for event page generation."""
    events: list[dict] = []
    warnings: list[str] = []

    for md_file in iter_advert_files():
        frontmatter = parse_frontmatter(md_file)
        if not frontmatter:
            warnings.append(f"Skipping {md_file}: invalid or missing frontmatter")
            continue

        title = frontmatter.get("title")
        slug = frontmatter.get("slug")
        url_value = frontmatter.get("url")
        start = parse_iso_date(frontmatter.get("start_date"))
        end = parse_iso_date(frontmatter.get("end_date"))
        if end is None and start is not None:
            end = start
        explicit_dates = parse_dates_field(frontmatter.get("dates"))
        format_type = frontmatter.get("format", "")
        level = frontmatter.get("level", "")
        short_description = frontmatter.get("short_description", "")
        tags = frontmatter.get("tags", [])

        clean_tags: list[str] = []
        if isinstance(tags, list):
            clean_tags = [
                str(tag).strip()
                for tag in tags
                if str(tag).strip() and str(tag).strip() != "..."
            ]

        if not title or not slug or not start:
            warnings.append(
                f"Skipping {md_file}: requires title, slug, start_date"
            )
            continue

        events.append(
            {
                "title": str(title),
                "slug": str(slug),
                "url": resolve_event_url(url_value, str(slug)),
                "start": start,
                "end": end,
                "display_dates": format_event_dates(start, end, explicit_dates),
                "format": str(format_type) if format_type is not None else "",
                "level": str(level) if level is not None else "",
                "short_description": (
                    str(short_description) if short_description is not None else ""
                ),
                "tags": clean_tags,
            }
        )

    return events, warnings


def classify_events(events: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
    """Classify events by date relation to today."""
    today = date.today()
    ongoing: list[dict] = []
    upcoming: list[dict] = []
    past: list[dict] = []

    for event in events:
        start = event["start"]
        end = event["end"]

        if start <= today <= end:
            ongoing.append(event)
        elif start > today:
            upcoming.append(event)
        elif end < today:
            past.append(event)

    ongoing.sort(key=lambda e: (e["start"], e["title"]))
    upcoming.sort(key=lambda e: (e["start"], e["title"]))
    past.sort(key=lambda e: (e["end"], e["title"]), reverse=True)

    return ongoing, upcoming, past


def render_event_card(event: dict) -> str:
    """Render a single event card."""
    badges = []
    description_html = ""

    if event["format"]:
        badges.append(f'<span class="ev-format">{event["format"]}</span>')
    if event["level"]:
        badges.append(
            f'<span class="diff-badge diff-{event["level"]}">{event["level"]}</span>'
        )
    for tag in event["tags"]:
        badges.append(f'<span class="ev-tag">{display_tag(tag)}</span>')

    if event["short_description"]:
        description_html = (
            f'\n  <p class="ev-card-desc">{event["short_description"]}</p>'
        )

    badges_html = " ".join(badges)

    return f"""<div class=\"ev-card\">\n  <div class=\"ev-card-date\">{event['display_dates']}</div>\n  <h3 class=\"ev-card-title\"><a href=\"{event['url']}\">{event['title']}</a></h3>{description_html}\n  <div class=\"ev-card-meta\">\n    {badges_html}\n  </div>\n</div>"""


def split_frontmatter(content: str) -> tuple[str, str]:
    """Split markdown into frontmatter and body."""
    if not content.startswith("---"):
        return "", content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return "", content

    frontmatter = f"---{parts[1]}---"
    body = parts[2]
    return frontmatter, body


def write_upcoming_page(ongoing: list[dict], upcoming: list[dict]) -> None:
    """Rewrite docs/events/upcoming.md with ongoing + upcoming sections."""
    existing = UPCOMING_PAGE.read_text(encoding="utf-8")
    frontmatter, _ = split_frontmatter(existing)

    lines = ["", "# Upcoming Events", ""]

    if ongoing:
        lines.append("## Ongoing Courses")
        lines.append("")
        lines.append('<div class="ev-card-grid">')
        lines.append("\n".join(render_event_card(event) for event in ongoing))
        lines.append("</div>")
        lines.append("")

    if upcoming:
        lines.append("## Upcoming Courses")
        lines.append("")
        lines.append('<div class="ev-card-grid">')
        lines.append("\n".join(render_event_card(event) for event in upcoming))
        lines.append("</div>")
        lines.append("")

    if not ongoing and not upcoming:
        lines.append("No ongoing or upcoming courses at the moment.")
        lines.append("")

    UPCOMING_PAGE.write_text(frontmatter + "\n".join(lines) + "\n", encoding="utf-8")


def write_past_page(past: list[dict]) -> None:
    """Rewrite docs/events/past-events.md with past section."""
    existing = PAST_PAGE.read_text(encoding="utf-8")
    frontmatter, _ = split_frontmatter(existing)

    lines = ["", "# Past Events", ""]

    if past:
        lines.append("Here are the past training courses:")
        lines.append("")
        lines.append('<div class="ev-card-grid">')
        lines.append("\n".join(render_event_card(event) for event in past))
        lines.append("</div>")
        lines.append("")
    else:
        lines.append("No past courses at the moment.")
        lines.append("")

    PAST_PAGE.write_text(frontmatter + "\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    events, warnings = load_adverts()
    for warning in warnings:
        print(f"Warning: {warning}")

    ongoing, upcoming, past = classify_events(events)
    write_upcoming_page(ongoing, upcoming)
    write_past_page(past)

    print(
        "Updated event pages from adverts: "
        f"{len(ongoing)} ongoing, {len(upcoming)} upcoming, {len(past)} past."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
