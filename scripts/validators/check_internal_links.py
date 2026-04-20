#!/usr/bin/env python3
"""Validate internal links in rendered site output.

Checks href targets across site/**/*.html and fails if unresolved local links
are found. External URLs (http/https/mailto/tel/javascript/hash) are ignored.
"""

from collections import Counter
from pathlib import Path
from urllib.parse import urljoin
import re
import sys

SITE_DIR = Path("site")


def is_ignored_href(href: str) -> bool:
    return href.startswith(("http://", "https://", "mailto:", "tel:", "#", "javascript:"))


def normalize_path(path: str) -> str:
    """Normalize local route aliases used by dev/gh-pages style paths."""
    if path.startswith("/di-training-repo/"):
        return path[len("/di-training-repo") :]
    if path == "/di-training-repo":
        return "/"
    return path


def resolves_to_local_target(path: str) -> bool:
    p = SITE_DIR / path.lstrip("/")
    if path == "/":
        return (SITE_DIR / "index.html").exists()
    if p.is_file():
        return True
    if p.is_dir() and (p / "index.html").exists():
        return True
    if not p.suffix and (SITE_DIR / path.lstrip("/") / "index.html").exists():
        return True
    return False


def main() -> int:
    if not SITE_DIR.exists():
        print("Error: site/ directory not found. Run zensical build first.")
        return 1

    errors = []
    checked = 0

    for html in sorted(SITE_DIR.rglob("*.html")):
        page_url = "/" + html.relative_to(SITE_DIR).parent.as_posix() + "/"
        text = html.read_text(encoding="utf-8", errors="ignore")

        for href in re.findall(r'href="([^\"]+)"', text):
            if is_ignored_href(href):
                continue

            target = urljoin("http://localhost" + page_url, href)
            path = normalize_path(target.split("http://localhost", 1)[-1])

            checked += 1
            if not resolves_to_local_target(path):
                errors.append((str(html.relative_to(SITE_DIR)), href, path))

    print(f"Checked {checked} internal links.")

    if errors:
        print(f"Found {len(errors)} unresolved internal link(s).")
        by_page = Counter(page for page, _, _ in errors)
        for page, count in by_page.most_common(10):
            print(f"- {page}: {count} unresolved")
        print("Sample unresolved links:")
        for page, href, path in errors[:30]:
            print(f"- {page}: {href} -> {path}")
        return 1

    print("No unresolved internal links found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
