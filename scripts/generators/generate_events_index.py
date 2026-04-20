#!/usr/bin/env python3
"""
Script to generate the Events index page from course metadata.
"""

from pathlib import Path
from collections import defaultdict
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from course_utils import load_courses
from link_utils import (
    events_to_course_md,
    events_to_learning_path_md,
    events_to_tags_index_md,
)


def infer_level(tags):
    """Infer level from tags."""
    tags_set = set(tags or [])
    if "beginner" in tags_set:
        return "Beginner"
    if "intermediate" in tags_set:
        return "Intermediate"
    if "advanced" in tags_set:
        return "Advanced"
    return "Unspecified"


def anchor_for_tag(tag):
    """Create a stable markdown anchor for a tag heading."""
    return tag.lower().replace(" ", "-")


def collect_courses():
    """Load and normalize course metadata for rendering."""
    courses = []
    for course in load_courses():
        fm = course["frontmatter"]
        tags = fm.get("tags", [])
        courses.append(
            {
                "title": course["title"],
                "link": events_to_course_md(course["link"]),
                "duration": fm.get("duration", ""),
                "summary": fm.get("short_description", ""),
                "tags": tags,
                "level": infer_level(tags),
            }
        )

    courses.sort(key=lambda x: x["title"].lower())
    return courses


def build_tags_index(courses):
    """Build tag -> course list mapping."""
    tags = defaultdict(list)
    for course in courses:
        for tag in course["tags"]:
            tags[tag].append(course)

    for tag in tags:
        tags[tag].sort(key=lambda x: x["title"].lower())

    return dict(sorted(tags.items(), key=lambda x: x[0].lower()))


def generate_events_index(courses, tags_map):
    """Generate markdown content for docs/events/index.md body."""
    body = "\n# Courses & Workshops\n\n"
    body += "Explore all available training courses for HPC users.\n\n"
    body += "---\n\n"

    body += "## Filter by Tag\n\n"
    for tag in tags_map:
        body += f"- [{tag}](#tag-{anchor_for_tag(tag)})\n"
    body += "\n---\n\n"

    body += "## All Courses\n\n"
    for course in courses:
        body += f"### {course['title']}\n\n"
        body += f"**Level:** {course['level']}  \n"
        body += f"**Duration:** {course['duration']}\n\n"

        if course["summary"]:
            body += f"{course['summary']}\n\n"

        body += "**Tags:**\n"
        if course["tags"]:
            body += " ".join(f"`{tag}`" for tag in course["tags"]) + "\n\n"
        else:
            body += "None\n\n"

        body += f"[View course ->]({course['link']})\n\n"
        body += "---\n\n"

    body += "## By Tag\n\n"
    for tag, tagged_courses in tags_map.items():
        body += f"### Tag: {tag}\n\n"
        for course in tagged_courses:
            body += f"- [{course['title']}]({course['link']}) ({course['level']})\n"
        body += "\n---\n\n"

    body += "- **Self-study materials**: Available anytime\n"
    body += "- **Past course materials**: Access recordings and resources\n\n"

    body += "## Need Help Choosing?\n\n"
    body += (
        f"- **New to HPC?** Start with [NAISS Introduction]({events_to_course_md('explore/all-training/naiss-intro.md')}) "
        f"or the [Beginner Path]({events_to_learning_path_md('beginner')})\\n"
    )
    body += f"- **Programmer?** Check the [Developer Path]({events_to_learning_path_md('developer')})\\n"
    body += f"- **Data scientist?** Explore the [Data Science Path]({events_to_learning_path_md('data-science')})\\n"
    body += f"- **Specific topic?** Use the [tag browser]({events_to_tags_index_md()})\\n"

    return body


def update_events_index_page(content):
    """Update docs/events/index.md while preserving frontmatter."""
    page = Path("docs/events/index.md")

    if not page.exists():
        print(f"Error: {page} does not exist.")
        return

    current = page.read_text(encoding="utf-8")

    frontmatter = ""
    if current.startswith("---"):
        parts = current.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[0] + "---" + parts[1] + "---"

    page.write_text(frontmatter + content, encoding="utf-8")


if __name__ == "__main__":
    all_courses = collect_courses()
    tags_index = build_tags_index(all_courses)
    new_content = generate_events_index(all_courses, tags_index)
    update_events_index_page(new_content)
    print(
        f"Updated docs/events/index.md with {len(all_courses)} courses and {len(tags_index)} tags."
    )