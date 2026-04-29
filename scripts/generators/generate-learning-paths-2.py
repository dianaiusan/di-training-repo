#!/usr/bin/env python3
"""Generate a dynamic course relationship map from 2026 event frontmatter."""

from __future__ import annotations

from collections import defaultdict, deque
from pathlib import Path
import html
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from course_utils import build_course_record


EVENTS_DIR = Path("docs/all-training/events/2026")
OUTPUT_FILE = Path("docs/explore/dynamic-learning-paths-2.md")
DEFAULT_SEED_SLUG = "naiss-intro-days"

DIRECTED_EDGE_TYPES = {"prerequisite", "progression"}
EDGE_LABELS = {
    "prerequisite": "Prerequisite",
    "related": "Related",
    "progression": "Progression",
}


def normalize_slug_list(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        stripped = value.strip()
        return [stripped] if stripped else []
    if not isinstance(value, list):
        return []

    normalized: list[str] = []
    for item in value:
        if item is None:
            continue
        slug = str(item).strip()
        if slug:
            normalized.append(slug)
    return normalized


def load_courses() -> list[dict[str, object]]:
    courses: list[dict[str, object]] = []
    for md_file in sorted(EVENTS_DIR.glob("*.md")):
        normalized_stem = md_file.stem.lstrip("_").lower()
        if md_file.name == "index.md" or normalized_stem.startswith("template"):
            continue
        course = build_course_record(md_file)
        if course:
            courses.append(course)
    return courses


def build_edges(courses_by_slug: dict[str, dict[str, object]]) -> tuple[list[dict[str, str]], int]:
    edges: list[dict[str, str]] = []
    skipped_references = 0
    seen_directed: set[tuple[str, str, str]] = set()
    seen_related: set[tuple[str, str, str]] = set()

    def add_edge(source: str, target: str, edge_type: str) -> None:
        nonlocal skipped_references

        if source == target:
            skipped_references += 1
            return
        if source not in courses_by_slug or target not in courses_by_slug:
            skipped_references += 1
            return

        if edge_type == "related":
            dedupe_key = tuple(sorted((source, target))) + (edge_type,)
            if dedupe_key in seen_related:
                return
            seen_related.add(dedupe_key)
        else:
            dedupe_key = (source, target, edge_type)
            if dedupe_key in seen_directed:
                return
            seen_directed.add(dedupe_key)

        edges.append(
            {
                "source": source,
                "target": target,
                "type": edge_type,
                "label": EDGE_LABELS[edge_type],
            }
        )

    for slug, course in courses_by_slug.items():
        frontmatter = course.get("frontmatter", {})
        if not isinstance(frontmatter, dict):
            continue

        for prereq_slug in normalize_slug_list(frontmatter.get("prerequisites")):
            add_edge(prereq_slug, slug, "prerequisite")

        for related_slug in normalize_slug_list(frontmatter.get("related")):
            add_edge(slug, related_slug, "related")

        for next_slug in normalize_slug_list(frontmatter.get("progression")):
            add_edge(slug, next_slug, "progression")

    edges.sort(key=lambda edge: (edge["type"], edge["source"], edge["target"]))
    return edges, skipped_references


def assign_levels(
    courses_by_slug: dict[str, dict[str, object]], edges: list[dict[str, str]]
) -> dict[str, int]:
    adjacency: dict[str, set[str]] = defaultdict(set)
    indegree: dict[str, int] = {slug: 0 for slug in courses_by_slug}

    for edge in edges:
        if edge["type"] not in DIRECTED_EDGE_TYPES:
            continue
        source = edge["source"]
        target = edge["target"]
        if target in adjacency[source]:
            continue
        adjacency[source].add(target)
        indegree[target] += 1

    queue = deque(sorted((slug for slug, count in indegree.items() if count == 0)))
    levels = {slug: 0 for slug in courses_by_slug}
    visited: set[str] = set()

    while queue:
        slug = queue.popleft()
        visited.add(slug)
        next_level = levels[slug] + 1
        for target in sorted(adjacency[slug]):
            if next_level > levels[target]:
                levels[target] = next_level
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)

    if len(visited) != len(courses_by_slug):
        remaining = sorted(set(courses_by_slug) - visited)
        for slug in remaining:
            levels.setdefault(slug, 0)

    return levels


def compute_layout(nodes: list[dict[str, object]]) -> tuple[int, int, dict[str, tuple[float, float]]]:
    columns: dict[int, list[dict[str, object]]] = defaultdict(list)
    for node in nodes:
        columns[int(node["level"])].append(node)

    for column_nodes in columns.values():
        column_nodes.sort(key=lambda item: str(item["title"]).lower())

    ordered_levels = sorted(columns)
    total_columns = max(len(ordered_levels), 1)
    max_rows = max((len(column) for column in columns.values()), default=1)

    horizontal_gap = 180
    width = 220 + horizontal_gap * max(total_columns - 1, 0)
    height = max(420, 150 + max_rows * 88)

    positions: dict[str, tuple[float, float]] = {}
    top_margin = 88
    bottom_margin = 80

    for column_index, level in enumerate(ordered_levels or [0]):
        level_nodes = columns.get(level, [])
        if total_columns == 1:
            x = width / 2
        else:
            x = 110 + column_index * horizontal_gap

        usable_height = max(height - top_margin - bottom_margin, 1)
        if len(level_nodes) == 1:
            y_positions = [height / 2]
        else:
            step = usable_height / (len(level_nodes) - 1)
            y_positions = [top_margin + index * step for index in range(len(level_nodes))]

        for node, y in zip(level_nodes, y_positions):
            positions[str(node["slug"])] = (round(x, 2), round(y, 2))

    return width, height, positions


def build_nodes(
    courses_by_slug: dict[str, dict[str, object]], levels: dict[str, int]
) -> list[dict[str, object]]:
    nodes: list[dict[str, object]] = []
    for slug, course in courses_by_slug.items():
        frontmatter = course.get("frontmatter", {})
        short_description = ""
        if isinstance(frontmatter, dict):
            short_description = str(frontmatter.get("short_description", "")).strip()
        nodes.append(
            {
                "slug": slug,
                "title": str(course.get("title", slug)),
                "link": str(course.get("link", "#")),
                "summary": short_description,
                "level": levels.get(slug, 0),
            }
        )

    nodes.sort(key=lambda item: (int(item["level"]), str(item["title"]).lower()))
    return nodes


def render_svg(
    nodes: list[dict[str, object]],
    edges: list[dict[str, str]],
    positions: dict[str, tuple[float, float]],
    width: int,
    height: int,
) -> str:
    lines = [
        f'<svg class="dlp2-graph" viewBox="0 0 {width} {height}" role="img" aria-labelledby="dlp2-graph-title dlp2-graph-desc">',
        '  <title id="dlp2-graph-title">Dynamic learning paths map</title>',
        '  <desc id="dlp2-graph-desc">Interactive course relationship graph built from prerequisite, related, and progression fields.</desc>',
        '  <g class="dlp2-edge-layer">',
    ]

    for edge_index, edge in enumerate(edges, start=1):
        source_x, source_y = positions[edge["source"]]
        target_x, target_y = positions[edge["target"]]
        lines.extend(
            [
                (
                    '    <line class="dlp2-edge dlp2-edge--{edge_type}" '
                    'data-edge-id="edge-{edge_index}" data-source="{source}" '
                    'data-target="{target}" data-type="{edge_type}" '
                    'x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" />'
                ).format(
                    edge_type=edge["type"],
                    edge_index=edge_index,
                    source=edge["source"],
                    target=edge["target"],
                    x1=source_x,
                    y1=source_y,
                    x2=target_x,
                    y2=target_y,
                )
            ]
        )

    lines.append("  </g>")
    lines.append('  <g class="dlp2-node-layer">')
    for node in nodes:
        slug = str(node["slug"])
        x, y = positions[slug]
        title = html.escape(str(node["title"]))
        lines.extend(
            [
                f'    <g class="dlp2-node" data-slug="{slug}" tabindex="0" transform="translate({x} {y})">',
                f'      <title>{title}</title>',
                '      <circle class="dlp2-node-hit" r="20"></circle>',
                '      <circle class="dlp2-node-dot" r="10"></circle>',
                '    </g>',
            ]
        )
    lines.extend(["  </g>", "</svg>"])
    return "\n".join(lines)


def render_page(
    nodes: list[dict[str, object]],
    edges: list[dict[str, str]],
    width: int,
    height: int,
    positions: dict[str, tuple[float, float]],
    skipped_references: int,
) -> str:
    graph_data = {
        "nodes": nodes,
        "edges": edges,
        "meta": {
            "courseCount": len(nodes),
            "connectionCount": len(edges),
            "skippedReferences": skipped_references,
        },
    }
    graph_json = json.dumps(graph_data, ensure_ascii=False, indent=2).replace("</", "<\\/")

    stat_line = (
        f"{len(nodes)} courses and {len(edges)} connections are shown. "
        "Hover, focus, or tap a circle to inspect its neighborhood. "
        "Connections that point outside the 2026 event set are ignored."
    )

    lines = [
        "---",
        'title: "Dynamic Learning Paths 2"',
        'icon: lucide/route',
        'description: "Interactive relationship map for 2026 event courses."',
        "---",
        "",
        "# Dynamic Learning Paths 2",
        "",
        "This page is generated from the 2026 event frontmatter. Prerequisites, related courses, and progression links shape the graph below.",
        "",
        f"> {stat_line}",
        "",
        "<style>",
        "  .dlp2-shell {",
        "    --dlp2-prereq: #0b5fff;",
        "    --dlp2-related: #d97706;",
        "    --dlp2-progression: #0f766e;",
        "    --dlp2-ink: #122033;",
        "    --dlp2-muted: #5b677a;",
        "    --dlp2-surface: linear-gradient(180deg, #fbfdff 0%, #f2f6fb 100%);",
        "    --dlp2-border: rgba(18, 32, 51, 0.12);",
        "    --dlp2-shadow: 0 18px 48px rgba(18, 32, 51, 0.14);",
        "    margin: 1.75rem 0 2rem;",
        "    padding: 1.25rem;",
        "    border: 1px solid var(--dlp2-border);",
        "    border-radius: 22px;",
        "    background: var(--dlp2-surface);",
        "    box-shadow: var(--dlp2-shadow);",
        "  }",
        "  .dlp2-toolbar {",
        "    display: flex;",
        "    flex-wrap: wrap;",
        "    gap: 1rem;",
        "    align-items: flex-start;",
        "    justify-content: space-between;",
        "    margin-bottom: 1rem;",
        "  }",
        "  .dlp2-kicker {",
        "    margin: 0 0 0.35rem;",
        "    font-size: 0.78rem;",
        "    font-weight: 700;",
        "    letter-spacing: 0.08em;",
        "    text-transform: uppercase;",
        "    color: var(--dlp2-muted);",
        "  }",
        "  .dlp2-toolbar h2 {",
        "    margin: 0 0 0.45rem;",
        "    font-size: 1.4rem;",
        "    line-height: 1.1;",
        "    color: var(--dlp2-ink);",
        "  }",
        "  .dlp2-toolbar p {",
        "    margin: 0;",
        "    max-width: 40rem;",
        "    color: var(--dlp2-muted);",
        "  }",
        "  .dlp2-seed-hint {",
        "    margin-top: 0.45rem;",
        "    font-size: 0.85rem;",
        "  }",
        "  .dlp2-legend {",
        "    display: flex;",
        "    flex-wrap: wrap;",
        "    gap: 0.55rem;",
        "    align-self: center;",
        "  }",
        "  .dlp2-legend-item {",
        "    display: inline-flex;",
        "    align-items: center;",
        "    gap: 0.45rem;",
        "    padding: 0.35rem 0.65rem;",
        "    border-radius: 999px;",
        "    border: 1px solid var(--dlp2-border);",
        "    background: rgba(255, 255, 255, 0.84);",
        "    color: var(--dlp2-ink);",
        "    font-size: 0.82rem;",
        "  }",
        "  .dlp2-legend-swatch {",
        "    display: inline-block;",
        "    width: 1.8rem;",
        "    height: 0.2rem;",
        "    border-radius: 999px;",
        "  }",
        "  .dlp2-legend-swatch--prerequisite { background: var(--dlp2-prereq); }",
        "  .dlp2-legend-swatch--related { background: var(--dlp2-related); }",
        "  .dlp2-legend-swatch--progression { background: var(--dlp2-progression); }",
        "  .dlp2-stage {",
        "    display: grid;",
        "    grid-template-columns: minmax(0, 1.8fr) minmax(16rem, 0.9fr);",
        "    gap: 1rem;",
        "    align-items: stretch;",
        "  }",
        "  .dlp2-graph {",
        "    width: 100%;",
        "    min-height: 22rem;",
        "    border-radius: 18px;",
        "    border: 1px solid rgba(18, 32, 51, 0.08);",
        "    background:",
        "      radial-gradient(circle at top, rgba(11, 95, 255, 0.08), transparent 38%),",
        "      linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(240, 245, 252, 0.98));",
        "  }",
        "  .dlp2-edge {",
        "    stroke-width: 2.25;",
        "    stroke-linecap: round;",
        "    opacity: 0.16;",
        "    transition: opacity 160ms ease, stroke-width 160ms ease;",
        "  }",
        "  .dlp2-edge--prerequisite { stroke: var(--dlp2-prereq); }",
        "  .dlp2-edge--related { stroke: var(--dlp2-related); stroke-dasharray: 6 5; }",
        "  .dlp2-edge--progression { stroke: var(--dlp2-progression); }",
        "  .dlp2-edge.is-active { opacity: 0.92; stroke-width: 4; }",
        "  .dlp2-edge.is-muted { opacity: 0.06; }",
        "  .dlp2-node { cursor: pointer; outline: none; }",
        "  .dlp2-node-hit { fill: transparent; }",
        "  .dlp2-node-dot {",
        "    fill: #fff;",
        "    stroke: #17304f;",
        "    stroke-width: 2.5;",
        "    transition: transform 160ms ease, fill 160ms ease, stroke 160ms ease, opacity 160ms ease;",
        "    transform-origin: center;",
        "  }",
        "  .dlp2-node.is-active .dlp2-node-dot,",
        "  .dlp2-node:focus .dlp2-node-dot {",
        "    fill: #17304f;",
        "    stroke: #17304f;",
        "    transform: scale(1.22);",
        "  }",
        "  .dlp2-node.is-connected .dlp2-node-dot {",
        "    fill: #e5edf8;",
        "    stroke: #17304f;",
        "    transform: scale(1.08);",
        "  }",
        "  .dlp2-node.is-muted .dlp2-node-dot { opacity: 0.28; }",
        "  .dlp2-panel {",
        "    padding: 1rem 1rem 1.1rem;",
        "    border-radius: 18px;",
        "    border: 1px solid rgba(18, 32, 51, 0.08);",
        "    background: rgba(255, 255, 255, 0.86);",
        "  }",
        "  .dlp2-controls {",
        "    display: flex;",
        "    gap: 0.55rem;",
        "    flex-wrap: wrap;",
        "    margin-bottom: 0.75rem;",
        "  }",
        "  .dlp2-btn {",
        "    border: 1px solid rgba(18, 32, 51, 0.2);",
        "    border-radius: 999px;",
        "    background: #fff;",
        "    color: var(--dlp2-ink);",
        "    padding: 0.36rem 0.8rem;",
        "    font-size: 0.82rem;",
        "    font-weight: 600;",
        "    cursor: pointer;",
        "  }",
        "  .dlp2-btn.is-active {",
        "    background: #17304f;",
        "    color: #fff;",
        "    border-color: #17304f;",
        "  }",
        "  .dlp2-panel h3 {",
        "    margin: 0.2rem 0 0.4rem;",
        "    font-size: 1.18rem;",
        "    line-height: 1.2;",
        "    color: var(--dlp2-ink);",
        "  }",
        "  .dlp2-panel p {",
        "    margin: 0;",
        "    color: var(--dlp2-muted);",
        "  }",
        "  .dlp2-panel-link { margin-top: 0.85rem; }",
        "  .dlp2-panel-link a { font-weight: 600; }",
        "  .dlp2-connection-list {",
        "    margin: 0.9rem 0 0;",
        "    padding: 0;",
        "    list-style: none;",
        "    display: grid;",
        "    gap: 0.55rem;",
        "  }",
        "  .dlp2-connection-list li {",
        "    padding: 0.55rem 0.7rem;",
        "    border-radius: 12px;",
        "    background: rgba(242, 246, 251, 0.9);",
        "    color: var(--dlp2-ink);",
        "    border: 1px solid rgba(18, 32, 51, 0.06);",
        "    font-size: 0.9rem;",
        "  }",
        "  .dlp2-connection-list a { font-weight: 600; }",
        "  .dlp2-connection-kind {",
        "    display: inline-block;",
        "    margin-right: 0.4rem;",
        "    color: var(--dlp2-muted);",
        "    font-size: 0.76rem;",
        "    font-weight: 700;",
        "    letter-spacing: 0.05em;",
        "    text-transform: uppercase;",
        "  }",
        "  @media (max-width: 980px) {",
        "    .dlp2-stage { grid-template-columns: 1fr; }",
        "    .dlp2-graph { min-height: 26rem; }",
        "  }",
        "</style>",
        '<div class="dlp2-shell">',
        '  <div class="dlp2-toolbar">',
        '    <div>',
        '      <p class="dlp2-kicker">2026 event graph</p>',
        '      <h2>Course relationship map</h2>',
        '      <p>Each circle is a course. Hover, focus, or tap one to highlight the connections derived from its frontmatter.</p>',
        '      <p class="dlp2-seed-hint" id="dlp2-seed-hint"></p>',
        '    </div>',
        '    <div class="dlp2-legend" aria-label="Connection legend">',
        '      <span class="dlp2-legend-item"><span class="dlp2-legend-swatch dlp2-legend-swatch--prerequisite"></span>Prerequisite</span>',
        '      <span class="dlp2-legend-item"><span class="dlp2-legend-swatch dlp2-legend-swatch--related"></span>Related</span>',
        '      <span class="dlp2-legend-item"><span class="dlp2-legend-swatch dlp2-legend-swatch--progression"></span>Progression</span>',
        '    </div>',
        '  </div>',
        '  <div class="dlp2-stage">',
        f'    {render_svg(nodes, edges, positions, width, height)}',
        '    <aside class="dlp2-panel" id="dlp2-panel">',
        '      <div class="dlp2-controls" aria-label="Graph view controls">',
        '        <button class="dlp2-btn" id="dlp2-show-all" type="button">Show all courses</button>',
        '        <button class="dlp2-btn" id="dlp2-reset-seed" type="button">Reset to intro path</button>',
        '      </div>',
        '      <p class="dlp2-kicker">Selected course</p>',
        '      <h3 id="dlp2-course-name">Hover a course circle</h3>',
        '      <p id="dlp2-course-summary">The course title and its connected neighbors will appear here.</p>',
        '      <p class="dlp2-panel-link"><a id="dlp2-course-link" href="#" hidden>Open course page</a></p>',
        '      <ul class="dlp2-connection-list" id="dlp2-course-connections"></ul>',
        '    </aside>',
        '  </div>',
        '</div>',
        '<script id="dlp2-data" type="application/json">',
        graph_json,
        '</script>',
        '<script>',
        '(() => {',
        '  const dataElement = document.getElementById("dlp2-data");',
        '  if (!dataElement) {',
        '    return;',
        '  }',
        '',
        '  const graph = JSON.parse(dataElement.textContent);',
        '  const nodeElements = new Map();',
        '  const edgeElements = [];',
        '  const nodeData = new Map(graph.nodes.map((node) => [node.slug, node]));',
        '  const connectionsBySlug = new Map(graph.nodes.map((node) => [node.slug, []]));',
        f'  const defaultSeed = "{DEFAULT_SEED_SLUG}";',
        '  const urlSeed = new URLSearchParams(window.location.search).get("seed");',
        '  const seedSlug = (urlSeed && nodeData.has(urlSeed)) ? urlSeed : (nodeData.has(defaultSeed) ? defaultSeed : null);',
        '  let mode = "all";',
        '  let lockedSlug = null;',
        '',
        '  document.querySelectorAll(".dlp2-node").forEach((element) => {',
        '    nodeElements.set(element.dataset.slug, element);',
        '  });',
        '',
        '  document.querySelectorAll(".dlp2-edge").forEach((element) => {',
        '    const edge = {',
        '      element,',
        '      source: element.dataset.source,',
        '      target: element.dataset.target,',
        '      type: element.dataset.type,',
        '    };',
        '    edgeElements.push(edge);',
        '    connectionsBySlug.get(edge.source).push(edge);',
        '    connectionsBySlug.get(edge.target).push(edge);',
        '  });',
        '',
        '  const nameElement = document.getElementById("dlp2-course-name");',
        '  const summaryElement = document.getElementById("dlp2-course-summary");',
        '  const linkElement = document.getElementById("dlp2-course-link");',
        '  const connectionListElement = document.getElementById("dlp2-course-connections");',
        '  const seedHintElement = document.getElementById("dlp2-seed-hint");',
        '  const showAllButton = document.getElementById("dlp2-show-all");',
        '  const resetSeedButton = document.getElementById("dlp2-reset-seed");',
        '  const graphElement = document.querySelector(".dlp2-graph");',
        '',
        '  function relationText(edge, slug) {',
        '    if (edge.type === "prerequisite") {',
        '      return edge.source === slug ? ["Prerequisite for", edge.target] : ["Requires", edge.source];',
        '    }',
        '    if (edge.type === "progression") {',
        '      return edge.source === slug ? ["Progresses to", edge.target] : ["Previous step", edge.source];',
        '    }',
        '    return ["Related to", edge.source === slug ? edge.target : edge.source];',
        '  }',
        '',
        '  function renderConnections(slug) {',
        '    connectionListElement.innerHTML = "";',
        '    const connections = connectionsBySlug.get(slug) || [];',
        '    if (connections.length === 0) {',
        '      const item = document.createElement("li");',
        '      item.textContent = "No mapped neighbors for this course.";',
        '      connectionListElement.appendChild(item);',
        '      return;',
        '    }',
        '',
        '    const sortedConnections = [...connections].sort((left, right) => {',
        '      const leftMeta = relationText(left, slug);',
        '      const rightMeta = relationText(right, slug);',
        '      return leftMeta[0].localeCompare(rightMeta[0]) || leftMeta[1].localeCompare(rightMeta[1]);',
        '    });',
        '',
        '    sortedConnections.forEach((edge) => {',
        '      const [label, otherSlug] = relationText(edge, slug);',
        '      const otherNode = nodeData.get(otherSlug);',
        '      if (!otherNode) {',
        '        return;',
        '      }',
        '      const item = document.createElement("li");',
        '      const kind = document.createElement("span");',
        '      kind.className = "dlp2-connection-kind";',
        '      kind.textContent = label;',
        '      const link = document.createElement("a");',
        '      link.href = otherNode.link;',
        '      link.textContent = otherNode.title;',
        '      item.appendChild(kind);',
        '      item.appendChild(link);',
        '      connectionListElement.appendChild(item);',
        '    });',
        '  }',
        '',
        '  function resetPanel() {',
        '    nameElement.textContent = "Hover a course circle";',
        '    summaryElement.textContent = "The course title and its connected neighbors will appear here.";',
        '    linkElement.hidden = true;',
        '    linkElement.href = "#";',
        '    connectionListElement.innerHTML = "";',
        '  }',
        '',
        '  function renderAllState() {',
        '    nodeElements.forEach((element) => {',
        '      element.classList.remove("is-active", "is-connected", "is-muted");',
        '    });',
        '    edgeElements.forEach((edge) => {',
        '      edge.element.classList.remove("is-active", "is-muted");',
        '    });',
        '    nameElement.textContent = "All courses";',
        '    summaryElement.textContent = "All courses are visible. Hover a circle to inspect one course and its direct neighbors.";',
        '    linkElement.hidden = true;',
        '    linkElement.href = "#";',
        '    connectionListElement.innerHTML = "";',
        '  }',
        '',
        '  function syncControlState() {',
        '    if (showAllButton) {',
        '      showAllButton.classList.toggle("is-active", mode === "all");',
        '    }',
        '    if (resetSeedButton) {',
        '      resetSeedButton.classList.toggle("is-active", mode === "seeded");',
        '      resetSeedButton.disabled = !seedSlug;',
        '    }',
        '    if (seedHintElement) {',
        '      if (!seedSlug) {',
        '        seedHintElement.textContent = "Start view shows all courses. Hover a course to highlight its direct neighbors.";',
        '      } else if (urlSeed && nodeData.has(urlSeed)) {',
        '        seedHintElement.textContent = `Start view shows all courses. Reset to intro path will focus URL seed: ${seedSlug}.`;',
        '      } else {',
        '        seedHintElement.textContent = `Start view shows all courses. Use Reset to intro path to focus ${seedSlug}.`;',
        '      }',
        '    }',
        '  }',
        '',
        '  function applySelection(slug) {',
        '    if (!slug || !nodeData.has(slug)) {',
        '      if (mode === "all") {',
        '        renderAllState();',
        '      } else if (seedSlug) {',
        '        applySelection(seedSlug);',
        '      } else {',
        '        renderAllState();',
        '      }',
        '      return;',
        '    }',
        '',
        '    const connectedNodes = new Set([slug]);',
        '    edgeElements.forEach((edge) => {',
        '      const touchesNode = edge.source === slug || edge.target === slug;',
        '      edge.element.classList.toggle("is-active", touchesNode);',
        '      edge.element.classList.toggle("is-muted", !touchesNode);',
        '      if (touchesNode) {',
        '        connectedNodes.add(edge.source);',
        '        connectedNodes.add(edge.target);',
        '      }',
        '    });',
        '',
        '    nodeElements.forEach((element, nodeSlug) => {',
        '      const isActive = nodeSlug === slug;',
        '      const isConnected = connectedNodes.has(nodeSlug) && !isActive;',
        '      element.classList.toggle("is-active", isActive);',
        '      element.classList.toggle("is-connected", isConnected);',
        '      element.classList.toggle("is-muted", !connectedNodes.has(nodeSlug));',
        '    });',
        '',
        '    const activeNode = nodeData.get(slug);',
        '    nameElement.textContent = activeNode.title;',
        '    summaryElement.textContent = activeNode.summary || "No short description is set for this course.";',
        '    linkElement.hidden = false;',
        '    linkElement.href = activeNode.link;',
        '    renderConnections(slug);',
        '  }',
        '',
        '  nodeElements.forEach((element, slug) => {',
        '    element.addEventListener("mouseenter", () => {',
        '      if (lockedSlug) {',
        '        return;',
        '      }',
        '      applySelection(slug);',
        '    });',
        '',
        '    element.addEventListener("focus", () => {',
        '      applySelection(slug);',
        '    });',
        '',
        '    element.addEventListener("click", () => {',
        '      lockedSlug = lockedSlug === slug ? null : slug;',
        '      applySelection(lockedSlug || slug);',
        '      if (!lockedSlug) {',
        '        applySelection(null);',
        '      }',
        '    });',
        '',
        '    element.addEventListener("keydown", (event) => {',
        '      if (event.key !== "Enter" && event.key !== " ") {',
        '        return;',
        '      }',
        '      event.preventDefault();',
        '      lockedSlug = lockedSlug === slug ? null : slug;',
        '      if (lockedSlug) {',
        '        applySelection(lockedSlug);',
        '      } else {',
        '        applySelection(null);',
        '      }',
        '    });',
        '  });',
        '',
        '  if (graphElement) {',
        '    graphElement.addEventListener("mouseleave", () => {',
        '      if (!lockedSlug) {',
        '        applySelection(null);',
        '      }',
        '    });',
        '  }',
        '',
        '  if (showAllButton) {',
        '    showAllButton.addEventListener("click", () => {',
        '      mode = "all";',
        '      lockedSlug = null;',
        '      syncControlState();',
        '      renderAllState();',
        '    });',
        '  }',
        '',
        '  if (resetSeedButton) {',
        '    resetSeedButton.addEventListener("click", () => {',
        '      if (!seedSlug) {',
        '        mode = "all";',
        '        renderAllState();',
        '        return;',
        '      }',
        '      mode = "seeded";',
        '      lockedSlug = null;',
        '      syncControlState();',
        '      applySelection(seedSlug);',
        '    });',
        '  }',
        '',
        '  syncControlState();',
        '  if (mode === "seeded" && seedSlug) {',
        '    applySelection(seedSlug);',
        '  } else {',
        '    renderAllState();',
        '  }',
        '})();',
        '</script>',
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    courses = load_courses()
    courses_by_slug = {str(course["slug"]): course for course in courses}
    edges, skipped_references = build_edges(courses_by_slug)
    levels = assign_levels(courses_by_slug, edges)
    nodes = build_nodes(courses_by_slug, levels)
    width, height, positions = compute_layout(nodes)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        render_page(nodes, edges, width, height, positions, skipped_references),
        encoding="utf-8",
    )

    print(
        f"Wrote {OUTPUT_FILE} with {len(nodes)} courses and {len(edges)} connections "
        f"({skipped_references} skipped references)."
    )


if __name__ == "__main__":
    main()