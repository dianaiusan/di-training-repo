# Tags Generation

Script: `scripts/generators/generate_tags.py`

Outputs:
- `docs/explore/tags/index.md`
- `docs/explore/tags/<category>.md` for non-empty categories

Source data:
- Advert frontmatter files under `docs/all-training/adverts/`
- Reads `tags`, `title`, `slug`

Behavior:
- Groups tags into curated categories
- Builds category overview cards and category detail pages
- Uses readable display labels while keeping canonical lowercase tag values in frontmatter
- Links courses to `/explore/training-catalogue/<slug>/`

Command:

```bash
.venv/bin/python scripts/generators/generate_tags.py
```
