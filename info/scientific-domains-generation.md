# Scientific Domains Generation

Script: `scripts/generators/generate_scientific_domains.py`

Outputs:
- `docs/explore/scientific-domains/index.md`
- `docs/explore/scientific-domains/<domain>.md` (one per configured domain)

Source data:
- Advert frontmatter files under `docs/all-training/adverts/`
- Reads `scientific_domains`, `title`, `slug`, and optional `url`

Behavior:
- Builds overview cards for domains
- Builds corresponding domain subpages
- Links courses to `/explore/training-catalogue/<slug>/` by default
- Cleans stale generated domain subpages

Command:

```bash
.venv/bin/python scripts/generators/generate_scientific_domains.py
```
