#!/usr/bin/env python3
"""Shared link helpers for docs generators.

Keep route/link construction centralized to avoid path regressions when
navigation depth or page layout changes.
"""


def events_to_course_md(course_link: str) -> str:
    """Link from docs/events/*.md to a docs/explore/all-training/*.md source page."""
    return f"../{course_link}"


def events_to_learning_path_md(path_slug: str) -> str:
    """Link from docs/events/*.md to docs/explore/learning-paths/<slug>.md."""
    return f"../explore/learning-paths/{path_slug}.md"


def events_to_tags_index_md() -> str:
    """Link from docs/events/*.md to docs/explore/tags/index.md."""
    return "../explore/tags/index.md"


def learning_path_page_to_course_route(course_slug: str) -> str:
    """Link from /explore/learning-paths/<path>/ to /explore/all-training/<course>/."""
    return f"../../../explore/all-training/{course_slug}/"


def learning_paths_overview_to_path_route(path_slug: str) -> str:
    """Link from /explore/learning-paths/ to /explore/learning-paths/<path>/."""
    return f"./{path_slug}/"


def learning_path_detail_to_related_path_route(path_slug: str) -> str:
    """Link from /explore/learning-paths/<path>/ to sibling /<related>/ page."""
    return f"../{path_slug}/"


def bundle_page_to_course_route(course_slug: str) -> str:
    """Link from /explore/bundles/<bundle>/ to /explore/all-training/<course>/."""
    return f"../../../explore/all-training/{course_slug}/"


def bundle_page_to_learning_path_route(path_slug: str) -> str:
    """Link from /explore/bundles/<bundle>/ to /explore/learning-paths/<path>/."""
    return f"../learning-paths/{path_slug}/"


def course_page_to_bundle_route(bundle_slug: str) -> str:
    """Link from /explore/all-training/<course>/ to /explore/bundles/<bundle>/."""
    return f"../bundles/{bundle_slug}/"


def tags_overview_to_category_route(category_slug: str) -> str:
    """Link from /explore/tags/ to /explore/tags/<category>/."""
    return f"./{category_slug}/"


def tag_category_to_course_route(course_slug: str) -> str:
    """Link from /explore/tags/<category>/ to /explore/all-training/<course>/."""
    return f"../../../explore/all-training/{course_slug}/"


def tag_category_to_overview_route() -> str:
    """Link from /explore/tags/<category>/ to /explore/tags/."""
    return "../"


def scientific_domains_overview_to_domain_route(domain_slug: str) -> str:
    """Link from /explore/scientific-domains/ to /.../<domain>/."""
    return f"./{domain_slug}/"


def scientific_domain_detail_to_course_md(course_slug: str) -> str:
    """Link from docs/explore/scientific-domains/<domain>.md to all-training md."""
    return f"../../explore/all-training/{course_slug}.md"
