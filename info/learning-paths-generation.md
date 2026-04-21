# Learning Paths Generation

Script: `scripts/generators/generate_learning_paths.py`

Outputs:
- `docs/explore/learning-paths/index.md`
- Regenerated detail bodies in `docs/explore/learning-paths/*.md` (except index)

Source data:
- Learning path frontmatter in each path file (`slug`, `title`, `description`, `phases`, `related_paths`)
- Advert frontmatter under `docs/all-training/adverts/` for course title lookups

Behavior:
- Keeps frontmatter blocks in path files
- Regenerates path body sections (swimlane + related paths)
- Regenerates overview card grid index
- Uses `/explore/training-catalogue/<slug>/` links for course references

Command:

```bash
.venv/bin/python scripts/generators/generate_learning_paths.py
```
