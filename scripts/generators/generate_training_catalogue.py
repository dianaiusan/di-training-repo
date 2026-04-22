#!/usr/bin/env python3
"""
Generate a merged all-training card grid page from events and self-study sources.
"""

from pathlib import Path
import sys
import yaml
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from course_utils import parse_frontmatter

EVENTS_DIR = Path("docs/all-training/events/2026")
SELF_STUDY_DIR = Path("docs/all-training/self-study")
OUTPUT_FILE = Path("docs/explore/training-catalogue/index.md")

# Utility: load all markdown files except _template.md
def load_markdown_files(directory):
    return [f for f in directory.glob("*.md") if f.name != "_template.md"]

# Utility: parse frontmatter for all files
def load_items(directory):
    items = {}
    for md_file in load_markdown_files(directory):
        fm, _ = parse_frontmatter(md_file)
        if not fm:
            continue
        slug = fm.get("slug")
        if slug:
            items[slug] = {"frontmatter": fm, "file": md_file}
    return items

# Merge event and self-study items by slug
def merge_items(events, self_study):
    merged = {}
    all_slugs = set(events) | set(self_study)
    for slug in sorted(all_slugs):
        merged[slug] = {
            "event": events.get(slug),
            "self_study": self_study.get(slug)
        }
    return merged

# Sorting: both-source first, then event-only, then self-study-only, alpha within
def sort_slugs(merged):
    def sort_key(slug):
        e = merged[slug]["event"] is not None
        s = merged[slug]["self_study"] is not None
        return (-(e and s), -e, slug)
    return sorted(merged, key=sort_key)

# Render a single card (stub)
def render_card(slug, entry):
    event = entry["event"]
    self_study = entry["self_study"]
    fm_event = event["frontmatter"] if event else {}
    fm_self = self_study["frontmatter"] if self_study else {}

    # Title precedence: event > self-study
    title = fm_event.get("title") or fm_self.get("title") or slug
    # Description precedence: event > self-study
    desc = fm_event.get("short_description") or fm_self.get("short_description") or ""

    # Badges/links
    badges = []
    if event:
        event_url = fm_event.get("url", "#")
        badges.append(f'<a class="ev-tag ev-tag-event" href="{event_url}">event</a>')
    if self_study:
        self_url = fm_self.get("url", "#")
        badges.append(f'<a class="ev-tag ev-tag-self-study" href="{self_url}">self-study</a>')

    # Level: union if both, else whichever exists
    levels = set()
    if fm_event.get("level"): levels.add(str(fm_event["level"]))
    if fm_self.get("level"): levels.add(str(fm_self["level"]))
    level_str = ", ".join(sorted(levels)) if levels else "-"

    # Tags: union if both, else whichever exists
    tags = set()
    for taglist in (fm_event.get("tags"), fm_self.get("tags")):
        if isinstance(taglist, list):
            tags.update(str(t) for t in taglist)
    tags_str = ", ".join(sorted(tags)) if tags else "-"

    # Event date chip (only for event-backed slugs)
    date_chip = ""
    if event and fm_event.get("start_date"):
        date_chip = f'<span class="ev-card-date">{fm_event["start_date"]}</span>'

    # Card HTML
    return f"""
    <div class='ev-card'>
      {date_chip}
      <div class='ev-card-title'>{title}</div>
      <div class='ev-card-desc'>{desc}</div>
      <div>{' '.join(badges)}</div>
      <div class='ev-card-meta'>Level: {level_str} | Tags: {tags_str}</div>
    </div>
    """

# Main generator logic
def main():
    events = load_items(EVENTS_DIR)
    self_study = load_items(SELF_STUDY_DIR)
    merged = merge_items(events, self_study)
    sorted_slugs = sort_slugs(merged)
    # Page header
    lines = [
        "---",
        "title: 'Training Catalogue'",
        "icon: lucide/layers",
        "---",
        "",
        "# Training Catalogue",
        "",
        "A unified catalogue of all events and self-study training resources.",
        "",
        "<div class='ev-card-grid'>"
    ]
    for slug in sorted_slugs:
        lines.append(render_card(slug, merged[slug]))
    lines.append("</div>")
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"Written {OUTPUT_FILE} ({len(sorted_slugs)} cards)")

if __name__ == "__main__":
    main()
