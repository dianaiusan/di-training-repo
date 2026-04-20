---
# Course/Workshop Template
# Copy this file to create new course/workshop pages in docs/explore/all-training/
# The frontmatter fields below will be used by scripts to generate lists

title: "Course or Workshop Title"
slug: "course-slug" # Use the target course file name without .md in docs/explore/all-training/

start_date="" # YYYY-MM-DD
end_date="" # YYYY-MM-DD
dates=""
duration: ""  # Free text: e.g., "2 hours", "1 day", "4 weeks"
status: "upcoming"  # Options: upcoming, past, cancelled, planned
format: "online"  # Options: online, on-site, hybrid, self-study

short_description: "One-sentence summary of the training"
registration_url: ""
prerequisites: ["...", "..."]  # Array of prerequisite course IDs or skills
related: ["...", "..."]  # Array of related course IDs

scientific_domains: ["...", "..."]  # Array of scientific domain IDs
learning_paths: ["...", "..."]  # Array of learning path IDs
tags: ["...", "...", "..."]  # Array of tags for filtering

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

Include the taget audience.

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

## Instructors / Partners

- Instructor 1
- Instructor 2

## Related training

- [Related Course 1](related-course1.md)
- [Related Course 2](related-course2.md)

## Questions

Comments and questions on the training event should be sent to NAISS using [the support form in SUPR](https://supr.naiss.se/support/). Please select "Question about a training event" as "Problem or Questions Type".

The NAISS support form in SUPR (on supr.naiss.se).

{% if external_url %}
## External Resources

More information available at: [{{ external_provider }}]({{ external_url }})
{% endif %}