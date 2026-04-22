---
# Self-Study Material Template
# Copy this file and rename it to <slug>.md in docs/all-training/self-study/
# Do NOT edit _template.md itself.

title: "Material Title"
slug: "material-slug"  # Unique identifier; used in URLs and cross-references

# What kind of resource is this?
# Options: tutorial | external-docs | recording | exercise-set | reading
kind: "tutorial"

# Visibility; only "published" items appear on the landing page
# Options: draft | published | archived
status: "draft"

format: "self-study"  # Always self-study for items in this directory

# Difficulty level
# Options: introductory | beginner | intermediate | advanced
level: "beginner"

short_description: "One-sentence summary visible on the landing page."

# Rough time commitment shown on the card (free text)
estimated_time: "2 hours"

# Link to the primary material (external URL or relative path).
# Leave blank if the material is listed under `materials` below.
url: ""

# Optional: slugs of related event adverts (from docs/all-training/adverts/).
# The generator will warn if a slug cannot be resolved.
related_event_slugs: []
#  - "intro-hpc-2026-01"

# Set to true if a recording of a live session is available in `materials`.
has_recording: false

# Set to true if there is no local page — all content lives at external URLs.
external_only: false

# Categorisation (same controlled vocabulary as adverts)
tags: []
#  - "hpc-fundamentals"
#  - "python"

learning_paths: []
#  - "beginner"

scientific_domains: []
#  - "general-hpc"

# List of individual resources (slides, videos, notebooks, exercises, …).
# `type` is used for badge styling; choose from:
#   slides | video | recording | notebook | exercises | external-docs | code | other
materials: []
#  - type: "slides"
#    title: "Lecture slides"
#    url: "https://example.com/slides.pdf"
#  - type: "video"
#    title: "Video walkthrough"
#    url: "https://example.com/video"
#  - type: "exercises"
#    title: "Hands-on exercises"
#    url: "https://github.com/naiss/exercises"

# Lucide icon name (without the lucide/ prefix).
# Browse icons at https://lucide.dev/icons/
icon: "book-open"
---

# {{ title }}

## Overview

Provide a concise description of the material, its purpose, and what the learner
will gain.

## Learning outcomes

- Outcome 1
- Outcome 2
- Outcome 3

## Prerequisites

- None (or list prerequisites)

## Materials

<!-- Links are generated from the `materials` frontmatter list above.
     You may also add inline links here for additional context. -->

## Notes

Any additional notes, tips, or caveats for learners.
