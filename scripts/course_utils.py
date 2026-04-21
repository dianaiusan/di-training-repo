#!/usr/bin/env python3
"""
Shared helper utilities for course generation scripts.
"""

from pathlib import Path
import yaml

COURSE_DIRS = [Path("docs/all-training/adverts")]


TAG_DISPLAY_NAMES = {
    "ai": "AI",
    "apptainer": "Apptainer",
    "arm": "Arm",
    "cpu": "CPU",
    "command-line": "Command Line",
    "cpp": "C++",
    "cuda": "CUDA",
    "file-io": "File I/O",
    "gpu": "GPU",
    "grace-hopper": "Grace Hopper",
    "hpc": "HPC",
    "jupyter": "Jupyter",
    "machine-learning": "Machine Learning",
    "matplotlib": "Matplotlib",
    "nccl": "NCCL",
    "openmp": "OpenMP",
    "mpi": "MPI",
    "nsight": "Nsight",
    "parallel-programming": "Parallel Programming",
    "paraview": "ParaView",
    "performance-optimization": "Performance Optimization",
    "pytorch": "PyTorch",
    "pyvista": "PyVista",
    "scientific-visualization": "Scientific Visualization",
    "singularity": "Singularity",
    "slurm": "Slurm",
    "software-development": "Software Development",
    "vtk": "VTK",
    "vedo": "Vedo",
}


def parse_frontmatter(file_path: Path):
    """Parse YAML frontmatter from a markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if not content.startswith('---'):
        return None, content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return None, content

    frontmatter_str = parts[1]
    body = parts[2]

    try:
        frontmatter = yaml.safe_load(frontmatter_str)
        return frontmatter or {}, body
    except yaml.YAMLError:
        return None, content


def iter_course_files():
    """Yield all course markdown files from available course directories."""
    for course_dir in COURSE_DIRS:
        if not course_dir.exists() or not course_dir.is_dir():
            continue

        for md_file in course_dir.rglob('*.md'):
            normalized_stem = md_file.stem.lstrip('_').lower()
            if normalized_stem.startswith('template'):
                continue
            if md_file.name == 'index.md':
                continue
            yield md_file


def course_link(md_file: Path):
    """Return a docs-relative link for a course markdown file."""
    return md_file.relative_to('docs').as_posix()


def build_course_record(md_file: Path):
    """Build a course record using slug as the stable identifier."""
    frontmatter, _ = parse_frontmatter(md_file)
    if not frontmatter:
        return None

    slug = frontmatter.get('slug')
    if not slug:
        raise ValueError(f"Missing slug in {md_file}")

    return {
        'title': frontmatter.get('title', slug),
        'slug': slug,
        'link': course_link(md_file),
        'frontmatter': frontmatter,
        'source_path': md_file,
    }


def load_courses():
    """Load all courses and validate that slugs are unique."""
    courses = []
    seen_slugs = {}

    for md_file in iter_course_files():
        course = build_course_record(md_file)
        if not course:
            continue

        slug = course['slug']
        if slug in seen_slugs:
            raise ValueError(
                f"Duplicate slug '{slug}' in {md_file} and {seen_slugs[slug]}"
            )

        seen_slugs[slug] = md_file
        courses.append(course)

    return courses


def display_tag(tag: str) -> str:
    """Convert a canonical lowercase tag to a readable display label."""
    normalized = tag.strip().lower()
    if not normalized:
        return ""

    if normalized in TAG_DISPLAY_NAMES:
        return TAG_DISPLAY_NAMES[normalized]

    parts = normalized.split("-")
    rendered_parts = []
    for part in parts:
        rendered_parts.append(TAG_DISPLAY_NAMES.get(part, part.title()))

    return " ".join(rendered_parts)
