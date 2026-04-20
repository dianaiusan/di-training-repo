#!/usr/bin/env python3
"""Inject start_date and end_date in course frontmatter from body Dates line."""

from datetime import datetime
import re
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from course_utils import iter_course_files


def extract_dates_line(body: str) -> str | None:
    """Extract the value from a markdown Dates line."""
    match = re.search(r"^\*\*Dates\*\*:\s*(.+?)\s*$", body, re.MULTILINE)
    if match:
        return match.group(1).strip()

    # Some files use singular Date label.
    match = re.search(r"^\*\*Date\*\*:\s*(.+?)\s*$", body, re.MULTILINE)
    if match:
        return match.group(1).strip()

    return None


def to_iso_dates(date_text: str | None) -> tuple[str, str]:
    """Convert supported date expressions to ISO start/end dates."""
    if not date_text:
        return "", ""

    lowered = date_text.lower()
    if lowered in {"tbd", "to be announced", "to be determined"}:
        return "", ""

    # Pattern: "3 - 5 June 2026"
    m = re.search(r"^(\d{1,2})\s*-\s*(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})$", date_text)
    if m:
        d1, d2, month_name, year = m.groups()
        month = datetime.strptime(month_name, "%B").month
        return f"{year}-{month:02d}-{int(d1):02d}", f"{year}-{month:02d}-{int(d2):02d}"

    # Pattern: "20, 21, 27 and 28 May 2026" (first and last day)
    m = re.search(r"^([\d,\sand]+)\s+([A-Za-z]+)\s+(\d{4})$", date_text)
    if m:
        days_blob, month_name, year = m.groups()
        days = [int(x) for x in re.findall(r"\d{1,2}", days_blob)]
        if days:
            month = datetime.strptime(month_name, "%B").month
            return f"{year}-{month:02d}-{days[0]:02d}", f"{year}-{month:02d}-{days[-1]:02d}"

    # Pattern: "12 June 2026"
    m = re.search(r"^(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})$", date_text)
    if m:
        day, month_name, year = m.groups()
        month = datetime.strptime(month_name, "%B").month
        iso = f"{year}-{month:02d}-{int(day):02d}"
        return iso, iso

    return "", ""


def split_frontmatter(content: str) -> tuple[str, str] | tuple[None, None]:
    """Split markdown into raw frontmatter text and body."""
    if not content.startswith("---"):
        return None, None

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, None

    return parts[1].strip("\n"), parts[2]


def get_value(line: str) -> str:
    """Read YAML scalar value from a simple key: value line."""
    if ":" not in line:
        return ""
    raw = line.split(":", 1)[1].strip()
    if raw.startswith('"') and raw.endswith('"'):
        return raw[1:-1]
    if raw.startswith("'") and raw.endswith("'"):
        return raw[1:-1]
    return raw


def set_or_insert_dates(fm_text: str, start_iso: str, end_iso: str) -> str:
    """Ensure start_date and end_date keys exist and are populated when possible."""
    lines = fm_text.splitlines()
    start_idx = next((i for i, ln in enumerate(lines) if ln.strip().startswith("start_date:")), None)
    end_idx = next((i for i, ln in enumerate(lines) if ln.strip().startswith("end_date:")), None)

    def fmt(value: str) -> str:
        return f'"{value}"' if value else '""'

    if start_idx is not None:
        current = get_value(lines[start_idx])
        if not current and start_iso:
            lines[start_idx] = f"start_date: {fmt(start_iso)}"
    if end_idx is not None:
        current = get_value(lines[end_idx])
        if not current and end_iso:
            lines[end_idx] = f"end_date: {fmt(end_iso)}"

    insert_at = None
    for key in ("duration:", "format:", "status:"):
        idx = next((i for i, ln in enumerate(lines) if ln.strip().startswith(key)), None)
        if idx is not None:
            insert_at = idx + 1
            break
    if insert_at is None:
        insert_at = len(lines)

    if start_idx is None:
        lines.insert(insert_at, f"start_date: {fmt(start_iso)}")
        insert_at += 1
    if end_idx is None:
        lines.insert(insert_at, f"end_date: {fmt(end_iso)}")

    return "\n".join(lines)


def inject_dates(md_path) -> bool:
    """Inject date keys into one markdown file."""
    content = md_path.read_text(encoding="utf-8")
    fm_text, body = split_frontmatter(content)
    if fm_text is None:
        return False

    dates_line = extract_dates_line(body)
    start_iso, end_iso = to_iso_dates(dates_line)
    new_fm = set_or_insert_dates(fm_text, start_iso, end_iso)

    new_content = f"---\n{new_fm}\n---{body}"
    if new_content == content:
        return False

    md_path.write_text(new_content, encoding="utf-8")
    return True


def main():
    """Process all all-training markdown files."""
    updated = 0
    for md_file in iter_course_files():
        if inject_dates(md_file):
            updated += 1
            print(f"Updated {md_file.name}")
    print(f"Added/updated date fields in {updated} course file(s).")


if __name__ == "__main__":
    main()
