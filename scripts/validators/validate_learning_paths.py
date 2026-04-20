#!/usr/bin/env python3
"""Validate docs/explore/learning-paths definitions against available course slugs."""

from collections import defaultdict
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from course_utils import load_courses
from learning_paths_utils import iter_path_files, load_path_definitions


def validate() -> int:
    errors = []
    warnings = []

    course_slugs = {course["slug"] for course in load_courses()}
    path_files = list(iter_path_files() or [])
    path_definitions, load_errors = load_path_definitions()
    errors.extend(load_errors)

    if not path_files:
        warnings.append("No path definition files found in docs/explore/learning-paths.")

    slug_to_file = {}
    referenced_path_slugs = defaultdict(list)

    for path_def in path_definitions:
        path_file = path_def["source_path"]
        path_slug = path_def["slug"]
        phases = path_def["phases"]
        related_paths = path_def["related_paths"]

        if path_slug in slug_to_file:
            errors.append(
                f"Duplicate path slug '{path_slug}' in {path_file} and {slug_to_file[path_slug]}"
            )
        else:
            slug_to_file[path_slug] = path_file

        if not isinstance(phases, dict) or not phases:
            errors.append(f"{path_file}: 'phases' must be a non-empty mapping")
            continue

        seen_in_path = set()
        for phase_name, phase_slugs in phases.items():
            if not isinstance(phase_slugs, list):
                errors.append(f"{path_file}: phase '{phase_name}' must be a list")
                continue

            if not phase_slugs:
                warnings.append(f"{path_file}: phase '{phase_name}' is empty")

            for course_slug in phase_slugs:
                if course_slug in seen_in_path:
                    errors.append(
                        f"{path_file}: duplicate course slug '{course_slug}' appears multiple times"
                    )
                seen_in_path.add(course_slug)

                if course_slug not in course_slugs:
                    errors.append(
                        f"{path_file}: unknown course slug '{course_slug}' in phase '{phase_name}'"
                    )

        if not isinstance(related_paths, list):
            errors.append(f"{path_file}: 'related_paths' must be a list")
        else:
            for related_slug in related_paths:
                referenced_path_slugs[related_slug].append(path_file)

    # Validate related_paths references after all path slugs are collected.
    for related_slug, source_files in referenced_path_slugs.items():
        if related_slug not in slug_to_file:
            for source_file in source_files:
                errors.append(
                    f"{source_file}: related path '{related_slug}' does not exist"
                )

    if warnings:
        print("Validation warnings:")
        for warning in warnings:
            print(f"- {warning}")

    if errors:
        print("Validation errors:")
        for err in errors:
            print(f"- {err}")
        print(f"Validation failed with {len(errors)} error(s).")
        return 1

    print(
        f"Learning paths validation passed for {len(path_files)} path file(s) and "
        f"{len(course_slugs)} course slug(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(validate())
