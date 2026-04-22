# Frontmatter Fields Used By Generators

This file lists the frontmatter fields that are currently read by the page-generation scripts in `scripts/generators/`.

It is intended as a practical reference for maintaining templates and content files.

## Events

Used by:
- `scripts/generators/generate_events.py`
- `scripts/generators/generate_scientific_domains.py`
- `scripts/generators/generate_training_catalogue.py`
- `scripts/generators/generate_tags.py` via `scripts/course_utils.py`

Fields currently used:
- `title`
- `slug`
- `url`
- `external_url`
- `start_date`
- `end_date`
- `dates`
- `format`
- `level`
- `short_description`
- `tags`
- `scientific_domains`

## Self-Study

Used by:
- `scripts/generators/generate_self_study.py`
- `scripts/generators/generate_training_catalogue.py`
- `scripts/generators/generate_tags.py` via `scripts/course_utils.py`

Fields currently used:
- `title`
- `slug`
- `status`
- `external_url`
- `url`
- `materials`
- `materials[].url`
- `short_description`
- `format`
- `level`
- `related_event_slugs`
- `tags`

## Learning Paths

Used by:
- `scripts/generators/generate_learning_paths.py`

Fields currently used:
- `slug`
- `title`
- `description`
- `phases`
- `related_paths`

## Bundles

Used by:
- `scripts/generators/generate_bundles.py`

Fields currently used:
- `slug`
- `title`
- `description`
- `audience`
- `total_duration`
- `modules`
- `modules[].course`
- `modules[].label`
- `modules[].module`
- `modules[].duration`
- `modules[].description`
- `related_paths`

## External Resources

Used by:
- `scripts/generators/generate_external_resources.py`

Fields currently used:
- `slug`
- `title`
- `url`
- `short_description`
- `resource_type`
- `status`
- `icon`
- `audience`

## Unique Field List

Across all current generators, these frontmatter fields are used:

- `audience`
- `dates`
- `description`
- `end_date`
- `external_url`
- `format`
- `icon`
- `level`
- `materials`
- `modules`
- `phases`
- `related_event_slugs`
- `related_paths`
- `resource_type`
- `scientific_domains`
- `short_description`
- `slug`
- `start_date`
- `status`
- `tags`
- `title`
- `total_duration`
- `url`

## Present But Not Currently Used For Generation

These fields appear in content files or templates but are not currently read by the active page generators:

- `duration`
- `kind`
- `learning_paths`
- `prerequisites`
- `registration_url`
- `related`

This list reflects the current generator code and may change if the scripts are updated.
