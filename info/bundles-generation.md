# Bundles Generation

Script: `scripts/generators/generate_bundles.py`

Outputs:
- `docs/explore/bundles/index.md`
- Regenerated detail bodies in `docs/explore/bundles/*.md` (except index)

Source data:
- Bundle frontmatter in each bundle file (`slug`, `title`, `description`, `audience`, `total_duration`, `modules`, `related_paths`)
- Advert frontmatter under `docs/all-training/adverts/` for course title lookups

Behavior:
- Keeps frontmatter blocks in bundle files
- Regenerates bundle track body from modules
- Regenerates overview card grid index
- Uses `/explore/training-catalogue/<slug>/` links for course references

Command:

```bash
.venv/bin/python scripts/generators/generate_bundles.py
```
