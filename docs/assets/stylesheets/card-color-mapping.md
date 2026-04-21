# Card color mapping by Markdown file

Source of truth for class styles: `docs/assets/stylesheets/extra.css`

## Shared card shell (used by bd/lp/tg/sd/ev-landing/tag cards)

- Background: `#ffffff`
- Border: `#d4d8e0`
- Hover border: `#010088`
- Hover background: `rgba(1, 0, 136, 0.07)`
- Title text: `#1a2332`
- Body/meta text: `#4a5568`

## File to color mapping

### `docs/events/index.md`

- Classes: `ev-landing-card`, `ev-landing-grid`
- Colors:
  - Card shell: shared card shell
  - Title: `#1a2332`
  - Description: `#4a5568`

### `docs/explore/index.md`

- Classes: `ev-landing-card`, `ev-landing-grid`
- Colors:
  - Card shell: shared card shell
  - Title: `#1a2332`
  - Description: `#4a5568`

### `docs/home.md`

- Classes: `tg-card`, `tg-card-grid`, `tg-card-title`, `tg-card-desc`
- Colors:
  - Card shell: shared card shell
  - Title/icon: `#1a2332`
  - Description (home override): `#6b7280`

### `docs/explore/scientific-domains/index.md`

- Classes: `sd-card`, `sd-card-grid`, `sd-card-title`, `sd-card-meta`
- Colors:
  - Card shell: shared card shell
  - Title: `#1a2332`
  - Meta: `#4a5568`
  - Links: `#010088`

### `docs/explore/learning-paths/index.md`

- Classes: `lp-card`, `lp-card-grid`, `lp-card-title`, `lp-card-desc`
- Colors:
  - Card shell: shared card shell
  - Title: `#1a2332`
  - Description: `#4a5568`
  - Links: `#010088`

### `docs/explore/tags/index.md`

- Classes: `tg-card`, `tg-card-grid`, `tg-card-title`, `tg-card-desc`
- Colors:
  - Card shell: shared card shell
  - Title: `#1a2332`
  - Description/meta: `#4a5568`
  - Links: `#010088`

### `docs/explore/bundles/index.md`

- Classes: `bd-card`, `bd-card-grid`
- Colors:
  - Card shell: shared card shell
  - Title: `#1a2332`
  - Description: `#4a5568`
  - Links: `#010088`

### `docs/explore/bundles/data-science-bootcamp-week.md`
### `docs/explore/bundles/developer-bootcamp-week.md`
### `docs/explore/bundles/intro-hpc-week.md`

- Classes: `bd-track`, `bd-item`, `bd-badge`, `bd-badge-core`
- Colors:
  - Item card bg/border: `#ffffff` / `#d4d8e0`
  - Number circle: `#010088` with `#ffffff` text
  - Base badge: bg `#f9fafb`, border `#d1d5db`, text `#4a5568`
  - Core badge: text `#010088`, bg `rgba(1, 0, 136, 0.08)`, border `rgba(46, 95, 163, 0.30)`

### `docs/explore/learning-paths/beginner.md`
### `docs/explore/learning-paths/bioinformatics.md`
### `docs/explore/learning-paths/data-science.md`
### `docs/explore/learning-paths/developer.md`
### `docs/explore/learning-paths/sensitive-data.md`

- Classes: `lp-swimlane`, `lp-phase`, `lp-phase-header`, `lp-phase-body`, `lp-course-num`, `lp-related-card`
- Colors:
  - Phase border/bg: `#d4d8e0` / `#ffffff`
  - Header + course number circles: `#010088` with `#ffffff` text
  - Related card: bg `#ffffff`, border `#d4d8e0`
  - Related card hover: border `#010088`, bg `rgba(1, 0, 136, 0.08)`
  - Supporting text: `#4a5568`

### `docs/explore/tags/data-ai.md`
### `docs/explore/tags/domains-visualization.md`
### `docs/explore/tags/gpu.md`
### `docs/explore/tags/hpc-infrastructure.md`
### `docs/explore/tags/other.md`
### `docs/explore/tags/parallel-performance.md`
### `docs/explore/tags/security-sensitive-data.md`
### `docs/explore/tags/software-development.md`

- Classes: `tag-card`, `tag-grid`, `tag-course-link`
- Colors:
  - Card shell: shared card shell
  - Card title: `#1a2332`
  - Hovered course links: `#010088`

### `docs/events/upcoming.md`
### `docs/events/past-events.md`

- Classes: `ev-card`, `ev-card-grid`, `ev-card-date`, `ev-card-title`, `ev-card-desc`, `ev-card-meta`, `ev-format`, `ev-tag`, `diff-badge`
- Colors:
  - Event card bg/border: `#ffffff` / `#d4d8e0`
  - Event card hover border: `#010088`
  - Date chip: text `#010088`, bg `rgba(1, 0, 136, 0.08)`
  - Title/body: `#1a2332` / `#4a5568`
  - Meta divider: `#e8eaed`
  - Format chip: text `#4a5568`, bg `rgba(74, 85, 104, 0.08)`, border `rgba(74, 85, 104, 0.20)`
  - Tag chip: text `#010088`, bg `rgba(46, 95, 163, 0.08)`, border `rgba(46, 95, 163, 0.20)`
  - Difficulty chips (`diff-beginner`, `diff-intermediate`, `diff-advanced`):
    - text `#3d5a80`, bg `rgba(61, 90, 128, 0.08)`, border `rgba(61, 90, 128, 0.22)`

### `docs/explore/training-catalogue/index.md`

- Classes: `ev-badge`, `ev-badge-upcoming`, `ev-badge-past`, `diff-badge`, `diff-beginner`, `diff-intermediate`, `diff-advanced`
- Colors:
  - Upcoming status badge: text `#1e6b5e`, bg `rgba(30, 107, 94, 0.10)`, border `rgba(30, 107, 94, 0.28)`
  - Past status badge: text `#4a5568`, bg `rgba(74, 85, 104, 0.10)`, border `rgba(74, 85, 104, 0.25)`
  - Difficulty badges (all levels currently same visual style):
    - text `#3d5a80`, bg `rgba(61, 90, 128, 0.08)`, border `rgba(61, 90, 128, 0.22)`
