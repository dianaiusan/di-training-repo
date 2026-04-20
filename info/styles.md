# Styles Inventory and Category Contract

This file documents the custom style families in use and the category contract for tag badge colors.

## Source of truth

- Shared stylesheet: docs/assets/stylesheets/extra.css
- Category metadata and tag-to-category mapping: scripts/generate_tags.py

## Style families currently in use

- bd-* : bundle tracks, bundle cards, and badge pills
- lp-* : learning-path card grids, swimlanes, and related cards
- tg-* : tag category overview cards
- tag-* : tag detail grids and links
- sd-* : scientific-domain card grids
- tag-list : per-course tag pill container

## Category contract

Use stable slug names for categories. Treat slug renames as breaking changes.

| Category slug | Display label | Badge class | Color intent |
| --- | --- | --- | --- |
| hpc-infrastructure | HPC and Infrastructure | bd-badge-hpc-infrastructure | Blue |
| parallel-performance | Parallel and Performance | bd-badge-parallel-performance | Green |
| gpu | GPU | bd-badge-gpu | Violet |
| data-ai | Data and AI | bd-badge-data-ai | Orange |
| software-development | Software Development | bd-badge-software-development | Amber |
| workflow-automation | Workflow and Automation | bd-badge-workflow-automation | Teal |
| foundations-levels | Foundations and Levels | bd-badge-foundations-levels | Slate |
| domains-visualization | Domains and Visualization | bd-badge-domains-visualization | Pink |
| security-sensitive-data | Security and Sensitive Data | bd-badge-security-sensitive-data | Red |
| other | Other | bd-badge (neutral fallback) | Neutral gray |

## Change workflow

### Change only colors

1. Edit badge color rules in docs/assets/stylesheets/extra.css.
2. Run zensical build.

### Add or change category assignment for tags

1. Update TAG_TO_CATEGORY in scripts/generate_tags.py.
2. Ensure matching badge class exists in docs/assets/stylesheets/extra.css.
3. Regenerate pages and build:
	- python3 scripts/generate_tags.py
	- zensical build

### Add a new category slug

1. Add slug and metadata in scripts/generate_tags.py.
2. Add a badge class in docs/assets/stylesheets/extra.css.
3. Update this file table.
4. Regenerate and build.

## Course frontmatter fields for events/styling

- `status`: upcoming | ongoing | past | cancelled
- `format`: online | on-site | hybrid | self-study
- `duration`: human-readable duration (e.g., "3 days", "1.5 hours")
- `start_date`: ISO date YYYY-MM-DD (extracted from "**Dates**:" line in body)
- `end_date`: ISO date YYYY-MM-DD (extracted from "**Dates**:" line in body)
- `registration_url`: optional registration link
