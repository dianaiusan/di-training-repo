#!/usr/bin/env python3
"""
Script to generate the Past Events page with styled event cards.
"""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from course_utils import load_courses
from datetime import date, datetime


def events_relative_link(course_link: str) -> str:
    """Convert docs-root course links to absolute URLs from site root."""
    # course_link is like "explore/all-training/ai-hpc.md"
    # Convert to "/" root-relative: "/explore/all-training/ai-hpc/"
    slug = course_link.replace('.md', '')
    return f"/{slug}/"


def parse_iso_date(value: str | None) -> date | None:
    """Parse an ISO date string safely."""
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def format_date_range(start_date: str, end_date: str) -> str:
    """Format date range from ISO dates (YYYY-MM-DD)."""
    if not start_date or not end_date:
        return "TBD"
    
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        if start == end:
            return start.strftime("%e %B %Y").strip()
        elif start.month == end.month:
            return f"{start.day} – {end.strftime('%e %B %Y').strip()}"
        else:
            return f"{start.strftime('%e %B').strip()} – {end.strftime('%e %B %Y').strip()}"
    except (ValueError, TypeError):
        return "TBD"


def render_event_card(course: dict) -> str:
    """Render a single event card."""
    frontmatter = course['frontmatter']
    title = course['title']
    link = events_relative_link(course['link'])
    
    start_date = frontmatter.get('start_date')
    end_date = frontmatter.get('end_date')
    status = frontmatter.get('status', 'past')
    format_type = frontmatter.get('format', 'unknown')
    level = frontmatter.get('level', '')

    date_str = format_date_range(start_date, end_date)

    # Build metadata badges
    badges = f'<span class="ev-badge ev-badge-{status}">{status}</span>'
    if format_type:
        badges += f' <span class="ev-format">{format_type}</span>'
    if level:
        badges += f' <span class="diff-badge diff-{level}">{level}</span>'
    
    return f"""<div class="ev-card">
  <div class="ev-card-date">{date_str}</div>
  <h3 class="ev-card-title"><a href="{link}">{title}</a></h3>
  <div class="ev-card-meta">
    {badges}
  </div>
</div>"""


def generate_past_list():
    """Generate list of past courses using end_date and status fallback."""
    past_courses = []
    today = date.today()

    for course in load_courses():
        frontmatter = course['frontmatter']
        end = parse_iso_date(frontmatter.get('end_date'))
        status = frontmatter.get('status')

        if end and end < today:
            past_courses.append(course)
        elif not end and status == 'past':
            past_courses.append(course)

    def sort_key(course: dict):
        fm = course['frontmatter']
        end = parse_iso_date(fm.get('end_date'))
        # Dated past events first (descending end_date), then status-past without end_date.
        if end:
            return (0, -end.toordinal(), course['title'])
        return (1, 0, course['title'])

    past_courses.sort(key=sort_key)
    return past_courses


def update_past_page(courses):
    """Update the past-events.md file with styled event cards."""
    past_file = Path("docs/events/past-events.md")

    if not past_file.exists():
        print(f"Error: {past_file} does not exist.")
        return

    # Read current content
    with open(past_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split frontmatter and body
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[0] + '---' + parts[1] + '---'
        else:
            frontmatter = ''
    else:
        frontmatter = ''

    # Generate new body with styled cards
    new_body = "\n# Past Events\n\n"
    if courses:
        new_body += "Here are the past training courses:\n\n"
        cards = "\n".join(render_event_card(c) for c in courses)
        new_body += f'<div class="ev-card-grid">\n{cards}\n</div>\n'
    else:
        new_body += "No past courses at the moment.\n\n"

    # Write back
    with open(past_file, 'w', encoding='utf-8') as f:
        f.write(frontmatter + new_body)

    print(f"Updated {past_file} with {len(courses)} past courses.")


if __name__ == "__main__":
    courses = generate_past_list()
    update_past_page(courses)
