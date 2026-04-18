---
# Course/Workshop Template
# Copy this file to create new course/workshop pages in docs/all-training/
# The frontmatter fields below will be used by scripts to generate lists

title: "Course or Workshop Title"
slug: "course-slug" # Use the target course file name without .md in docs/all-training/

start_date="" # YYYY-MM-DD
end_date="" # YYYY-MM-DD
duration: "2 hours"  # Free text: e.g., "2 hours", "1 day", "4 weeks"
status: "upcoming"  # Options: upcoming, past, cancelled, planned
format: "online"  # Options: online, on-site, hybrid, self-study

short_description: "One-sentence summary of the training"
registration_url: ""
prerequisites: ["basic-linux", "python-basics"]  # Array of prerequisite course IDs or skills
related: ["advanced-hpc", "parallel-computing"]  # Array of related course IDs

scientific_domains: ["computational-chemistry", "bioinformatics"]  # Array of scientific domain IDs
learning_paths: ["introduction-to-hpc", "data-analysis"]  # Array of learning path IDs
tags: ["hpc", "beginner", "python"]  # Array of tags for filtering

#external_url: "https://example.com/course"  # Optional external link
#provider: "ENCCS"  # Provider name if external

materials: []  # List of self-study materials, e.g.:
# materials:
#   - title: "Slides"
#     url: "https://example.com/slides.pdf"
#   - title: "Video recording"
#     url: "https://example.com/recording.mp4"
#   - title: "Exercise files"
#     url: "https://github.com/naiss/exercises"

icon: lucide/book-open  # Lucide icon for the page
---

# {{ title }}

## Summary

Provide a detailed description of the course or workshop content, objectives, and what participants will learn.

## Learning objectives

- Objective 1
- Objective 2
- Objective 3

## Prerequisites

- {{ prerequisites | join(', ') }}

## Practical information

- Date and time:
- Location: 
- Registration: {{ registration_url }}

## Materials

Links to slides, exercises, recordings, etc.

## Related training

- [Related Course 1](related-course1.md)
- [Related Course 2](related-course2.md)

{% if external_url %}
## External Resources

More information available at: [{{ external_provider }}]({{ external_url }})
{% endif %}