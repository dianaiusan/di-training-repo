#!/usr/bin/env python3
"""Validate all-training course date metadata consistency."""

from datetime import datetime
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from course_utils import load_courses

ALLOWED_STATUS = {"upcoming", "ongoing", "past", "cancelled"}
ALLOWED_FORMAT = {"online", "on-site", "hybrid", "self-study"}


def parse_iso_date(raw: str):
    """Parse YYYY-MM-DD date strings, returning a date or None for empty values."""
    value = (raw or "").strip()
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return "INVALID"


def validate() -> int:
    errors = []
    warnings = []

    courses = load_courses()
    for course in courses:
        path = course["source_path"]
        fm = course["frontmatter"]

        status = (fm.get("status") or "").strip()
        fmt = (fm.get("format") or "").strip()
        start_raw = (fm.get("start_date") or "").strip()
        end_raw = (fm.get("end_date") or "").strip()

        if status not in ALLOWED_STATUS:
            errors.append(f"{path}: invalid status '{status}'")
        if fmt not in ALLOWED_FORMAT:
            errors.append(f"{path}: invalid format '{fmt}'")

        start_date = parse_iso_date(start_raw)
        end_date = parse_iso_date(end_raw)

        if start_date == "INVALID":
            errors.append(f"{path}: invalid start_date '{start_raw}', expected YYYY-MM-DD")
            start_date = None
        if end_date == "INVALID":
            errors.append(f"{path}: invalid end_date '{end_raw}', expected YYYY-MM-DD")
            end_date = None

        if start_date and end_date and end_date < start_date:
            errors.append(
                f"{path}: end_date '{end_raw}' is earlier than start_date '{start_raw}'"
            )

        if fmt == "self-study":
            # Self-study may legitimately omit scheduled dates.
            continue

        # Non-self-study checks are warnings to allow TBD planning states.
        if status in {"upcoming", "ongoing"} and not start_raw:
            warnings.append(
                f"{path}: status '{status}' is missing start_date (TBD allowed)"
            )

        if status == "ongoing" and not end_raw:
            warnings.append(f"{path}: status 'ongoing' is missing end_date")

        if status == "past" and not end_raw:
            warnings.append(
                f"{path}: status 'past' missing end_date (allowed fallback per policy)"
            )

        if end_raw and not start_raw:
            warnings.append(f"{path}: has end_date but no start_date")

    if warnings:
        print("Date validation warnings:")
        for warning in warnings:
            print(f"- {warning}")

    if errors:
        print("Date validation errors:")
        for err in errors:
            print(f"- {err}")
        print(f"Date validation failed with {len(errors)} error(s).")
        return 1

    print(
        f"Course date validation passed with {len(warnings)} warning(s) across {len(courses)} course file(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(validate())
