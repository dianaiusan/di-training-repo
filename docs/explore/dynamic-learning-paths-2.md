---
title: "Dynamic Learning Paths 2"
icon: lucide/route
description: "Interactive relationship map for 2026 event courses."
---

# Dynamic Learning Paths 2

This page is generated from the 2026 event frontmatter. Prerequisites, related courses, and progression links shape the graph below.

> 13 courses and 11 connections are shown. Hover, focus, or tap a circle to inspect its neighborhood. Connections that point outside the 2026 event set are ignored.

<style>
  .dlp2-shell {
    --dlp2-prereq: #0b5fff;
    --dlp2-related: #d97706;
    --dlp2-progression: #0f766e;
    --dlp2-ink: #122033;
    --dlp2-muted: #5b677a;
    --dlp2-surface: linear-gradient(180deg, #fbfdff 0%, #f2f6fb 100%);
    --dlp2-border: rgba(18, 32, 51, 0.12);
    --dlp2-shadow: 0 18px 48px rgba(18, 32, 51, 0.14);
    margin: 1.75rem 0 2rem;
    padding: 1.25rem;
    border: 1px solid var(--dlp2-border);
    border-radius: 22px;
    background: var(--dlp2-surface);
    box-shadow: var(--dlp2-shadow);
  }
  .dlp2-toolbar {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 1rem;
  }
  .dlp2-kicker {
    margin: 0 0 0.35rem;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--dlp2-muted);
  }
  .dlp2-toolbar h2 {
    margin: 0 0 0.45rem;
    font-size: 1.4rem;
    line-height: 1.1;
    color: var(--dlp2-ink);
  }
  .dlp2-toolbar p {
    margin: 0;
    max-width: 40rem;
    color: var(--dlp2-muted);
  }
  .dlp2-seed-hint {
    margin-top: 0.45rem;
    font-size: 0.85rem;
  }
  .dlp2-legend {
    display: flex;
    flex-wrap: wrap;
    gap: 0.55rem;
    align-self: center;
  }
  .dlp2-legend-item {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.35rem 0.65rem;
    border-radius: 999px;
    border: 1px solid var(--dlp2-border);
    background: rgba(255, 255, 255, 0.84);
    color: var(--dlp2-ink);
    font-size: 0.82rem;
  }
  .dlp2-legend-swatch {
    display: inline-block;
    width: 1.8rem;
    height: 0.2rem;
    border-radius: 999px;
  }
  .dlp2-legend-swatch--prerequisite { background: var(--dlp2-prereq); }
  .dlp2-legend-swatch--related { background: var(--dlp2-related); }
  .dlp2-legend-swatch--progression { background: var(--dlp2-progression); }
  .dlp2-stage {
    display: grid;
    grid-template-columns: minmax(0, 1.8fr) minmax(16rem, 0.9fr);
    gap: 1rem;
    align-items: stretch;
  }
  .dlp2-graph {
    width: 100%;
    min-height: 22rem;
    border-radius: 18px;
    border: 1px solid rgba(18, 32, 51, 0.08);
    background:
      radial-gradient(circle at top, rgba(11, 95, 255, 0.08), transparent 38%),
      linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(240, 245, 252, 0.98));
  }
  .dlp2-edge {
    stroke-width: 2.25;
    stroke-linecap: round;
    opacity: 0.16;
    transition: opacity 160ms ease, stroke-width 160ms ease;
  }
  .dlp2-edge--prerequisite { stroke: var(--dlp2-prereq); }
  .dlp2-edge--related { stroke: var(--dlp2-related); stroke-dasharray: 6 5; }
  .dlp2-edge--progression { stroke: var(--dlp2-progression); }
  .dlp2-edge.is-active { opacity: 0.92; stroke-width: 4; }
  .dlp2-edge.is-muted { opacity: 0.06; }
  .dlp2-node { cursor: pointer; outline: none; }
  .dlp2-node-hit { fill: transparent; }
  .dlp2-node-dot {
    fill: #fff;
    stroke: #17304f;
    stroke-width: 2.5;
    transition: transform 160ms ease, fill 160ms ease, stroke 160ms ease, opacity 160ms ease;
    transform-origin: center;
  }
  .dlp2-node.is-active .dlp2-node-dot,
  .dlp2-node:focus .dlp2-node-dot {
    fill: #17304f;
    stroke: #17304f;
    transform: scale(1.22);
  }
  .dlp2-node.is-connected .dlp2-node-dot {
    fill: #e5edf8;
    stroke: #17304f;
    transform: scale(1.08);
  }
  .dlp2-node.is-muted .dlp2-node-dot { opacity: 0.28; }
  .dlp2-panel {
    padding: 1rem 1rem 1.1rem;
    border-radius: 18px;
    border: 1px solid rgba(18, 32, 51, 0.08);
    background: rgba(255, 255, 255, 0.86);
  }
  .dlp2-controls {
    display: flex;
    gap: 0.55rem;
    flex-wrap: wrap;
    margin-bottom: 0.75rem;
  }
  .dlp2-btn {
    border: 1px solid rgba(18, 32, 51, 0.2);
    border-radius: 999px;
    background: #fff;
    color: var(--dlp2-ink);
    padding: 0.36rem 0.8rem;
    font-size: 0.82rem;
    font-weight: 600;
    cursor: pointer;
  }
  .dlp2-btn.is-active {
    background: #17304f;
    color: #fff;
    border-color: #17304f;
  }
  .dlp2-panel h3 {
    margin: 0.2rem 0 0.4rem;
    font-size: 1.18rem;
    line-height: 1.2;
    color: var(--dlp2-ink);
  }
  .dlp2-panel p {
    margin: 0;
    color: var(--dlp2-muted);
  }
  .dlp2-panel-link { margin-top: 0.85rem; }
  .dlp2-panel-link a { font-weight: 600; }
  .dlp2-connection-list {
    margin: 0.9rem 0 0;
    padding: 0;
    list-style: none;
    display: grid;
    gap: 0.55rem;
  }
  .dlp2-connection-list li {
    padding: 0.55rem 0.7rem;
    border-radius: 12px;
    background: rgba(242, 246, 251, 0.9);
    color: var(--dlp2-ink);
    border: 1px solid rgba(18, 32, 51, 0.06);
    font-size: 0.9rem;
  }
  .dlp2-connection-list a { font-weight: 600; }
  .dlp2-connection-kind {
    display: inline-block;
    margin-right: 0.4rem;
    color: var(--dlp2-muted);
    font-size: 0.76rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
  }
  @media (max-width: 980px) {
    .dlp2-stage { grid-template-columns: 1fr; }
    .dlp2-graph { min-height: 26rem; }
  }
</style>
<div class="dlp2-shell">
  <div class="dlp2-toolbar">
    <div>
      <p class="dlp2-kicker">2026 event graph</p>
      <h2>Course relationship map</h2>
      <p>Each circle is a course. Hover, focus, or tap one to highlight the connections derived from its frontmatter.</p>
      <p class="dlp2-seed-hint" id="dlp2-seed-hint"></p>
    </div>
    <div class="dlp2-legend" aria-label="Connection legend">
      <span class="dlp2-legend-item"><span class="dlp2-legend-swatch dlp2-legend-swatch--prerequisite"></span>Prerequisite</span>
      <span class="dlp2-legend-item"><span class="dlp2-legend-swatch dlp2-legend-swatch--related"></span>Related</span>
      <span class="dlp2-legend-item"><span class="dlp2-legend-swatch dlp2-legend-swatch--progression"></span>Progression</span>
    </div>
  </div>
  <div class="dlp2-stage">
    <svg class="dlp2-graph" viewBox="0 0 760 942" role="img" aria-labelledby="dlp2-graph-title dlp2-graph-desc">
  <title id="dlp2-graph-title">Dynamic learning paths map</title>
  <desc id="dlp2-graph-desc">Interactive course relationship graph built from prerequisite, related, and progression fields.</desc>
  <g class="dlp2-edge-layer">
    <line class="dlp2-edge dlp2-edge--prerequisite" data-edge-id="edge-1" data-source="mpi-intro" data-target="grace-hopper-gpu" data-type="prerequisite" x1="110" y1="88.0" x2="290" y2="88.0" />
    <line class="dlp2-edge dlp2-edge--prerequisite" data-edge-id="edge-2" data-source="naiss-intro-days" data-target="python-intro" data-type="prerequisite" x1="110" y1="668.5" x2="290" y2="862.0" />
    <line class="dlp2-edge dlp2-edge--progression" data-edge-id="edge-3" data-source="python-hpc" data-target="ai-hpc" data-type="progression" x1="470" y1="471.0" x2="650" y2="471.0" />
    <line class="dlp2-edge dlp2-edge--progression" data-edge-id="edge-4" data-source="python-intro" data-target="python-hpc" data-type="progression" x1="290" y1="862.0" x2="470" y2="471.0" />
    <line class="dlp2-edge dlp2-edge--related" data-edge-id="edge-5" data-source="eigen-cpp" data-target="mpi-intro" data-type="related" x1="110" y1="184.75" x2="110" y2="88.0" />
    <line class="dlp2-edge dlp2-edge--related" data-edge-id="edge-6" data-source="eigen-cpp" data-target="programming-formalisms" data-type="related" x1="110" y1="184.75" x2="110" y2="765.25" />
    <line class="dlp2-edge dlp2-edge--related" data-edge-id="edge-7" data-source="naiss-intro-days" data-target="file-transfer-201" data-type="related" x1="110" y1="668.5" x2="110" y2="475.0" />
    <line class="dlp2-edge dlp2-edge--related" data-edge-id="edge-8" data-source="python-hpc" data-target="combined-python-intro-and-python-hpc" data-type="related" x1="470" y1="471.0" x2="110" y2="571.75" />
    <line class="dlp2-edge dlp2-edge--related" data-edge-id="edge-9" data-source="python-intro" data-target="combined-python-intro-and-python-hpc" data-type="related" x1="290" y1="862.0" x2="110" y2="571.75" />
    <line class="dlp2-edge dlp2-edge--related" data-edge-id="edge-10" data-source="singularity-apptainer" data-target="bianca-intermediate" data-type="related" x1="110" y1="281.5" x2="110" y2="378.25" />
    <line class="dlp2-edge dlp2-edge--related" data-edge-id="edge-11" data-source="singularity-apptainer" data-target="naiss-intro-days" data-type="related" x1="110" y1="281.5" x2="110" y2="668.5" />
  </g>
  <g class="dlp2-node-layer">
    <g class="dlp2-node" data-slug="mpi-intro" tabindex="0" transform="translate(110 88.0)">
      <title>An introduction to parallel programming using Message Passing with MPI</title>
      <circle class="dlp2-node-hit" r="20"></circle>
      <circle class="dlp2-node-dot" r="10"></circle>
    </g>
    <g class="dlp2-node" data-slug="eigen-cpp" tabindex="0" transform="translate(110 184.75)">
      <title>Array computing in C++ using Eigen</title>
      <circle class="dlp2-node-hit" r="20"></circle>
      <circle class="dlp2-node-dot" r="10"></circle>
    </g>
    <g class="dlp2-node" data-slug="singularity-apptainer" tabindex="0" transform="translate(110 281.5)">
      <title>Basic Singularity/Apptainer</title>
      <circle class="dlp2-node-hit" r="20"></circle>
      <circle class="dlp2-node-dot" r="10"></circle>
    </g>
    <g class="dlp2-node" data-slug="bianca-intermediate" tabindex="0" transform="translate(110 378.25)">
      <title>Bianca In-Depth Workshop/Hackathon: Improve Your Handling of Sensitive Research Data</title>
      <circle class="dlp2-node-hit" r="20"></circle>
      <circle class="dlp2-node-dot" r="10"></circle>
    </g>
    <g class="dlp2-node" data-slug="file-transfer-201" tabindex="0" transform="translate(110 475.0)">
      <title>File Transfer 201</title>
      <circle class="dlp2-node-hit" r="20"></circle>
      <circle class="dlp2-node-dot" r="10"></circle>
    </g>
    <g class="dlp2-node" data-slug="combined-python-intro-and-python-hpc" tabindex="0" transform="translate(110 571.75)">
      <title>Introduction to Python and Using Python in an HPC environment</title>
      <circle class="dlp2-node-hit" r="20"></circle>
      <circle class="dlp2-node-dot" r="10"></circle>
    </g>
    <g class="dlp2-node" data-slug="naiss-intro-days" tabindex="0" transform="translate(110 668.5)">
      <title>NAISS Introduction Training Days</title>
      <circle class="dlp2-node-hit" r="20"></circle>
      <circle class="dlp2-node-dot" r="10"></circle>
    </g>
    <g class="dlp2-node" data-slug="programming-formalisms" tabindex="0" transform="translate(110 765.25)">
      <title>Programming Formalisms</title>
      <circle class="dlp2-node-hit" r="20"></circle>
      <circle class="dlp2-node-dot" r="10"></circle>
    </g>
    <g class="dlp2-node" data-slug="paraview" tabindex="0" transform="translate(110 862.0)">
      <title>Scientific Visualization with ParaView</title>
      <circle class="dlp2-node-hit" r="20"></circle>
      <circle class="dlp2-node-dot" r="10"></circle>
    </g>
    <g class="dlp2-node" data-slug="grace-hopper-gpu" tabindex="0" transform="translate(290 88.0)">
      <title>Efficient Use of the Grace Hopper GPU Nodes on Dardel and Arrhenius</title>
      <circle class="dlp2-node-hit" r="20"></circle>
      <circle class="dlp2-node-dot" r="10"></circle>
    </g>
    <g class="dlp2-node" data-slug="python-intro" tabindex="0" transform="translate(290 862.0)">
      <title>Intro to Python for HPC</title>
      <circle class="dlp2-node-hit" r="20"></circle>
      <circle class="dlp2-node-dot" r="10"></circle>
    </g>
    <g class="dlp2-node" data-slug="python-hpc" tabindex="0" transform="translate(470 471.0)">
      <title>Using Python in an HPC Environment</title>
      <circle class="dlp2-node-hit" r="20"></circle>
      <circle class="dlp2-node-dot" r="10"></circle>
    </g>
    <g class="dlp2-node" data-slug="ai-hpc" tabindex="0" transform="translate(650 471.0)">
      <title>AI and HPC</title>
      <circle class="dlp2-node-hit" r="20"></circle>
      <circle class="dlp2-node-dot" r="10"></circle>
    </g>
  </g>
</svg>
    <aside class="dlp2-panel" id="dlp2-panel">
      <div class="dlp2-controls" aria-label="Graph view controls">
        <button class="dlp2-btn" id="dlp2-show-all" type="button">Show all courses</button>
        <button class="dlp2-btn" id="dlp2-reset-seed" type="button">Reset to intro path</button>
      </div>
      <p class="dlp2-kicker">Selected course</p>
      <h3 id="dlp2-course-name">Hover a course circle</h3>
      <p id="dlp2-course-summary">The course title and its connected neighbors will appear here.</p>
      <p class="dlp2-panel-link"><a id="dlp2-course-link" href="#" hidden>Open course page</a></p>
      <ul class="dlp2-connection-list" id="dlp2-course-connections"></ul>
    </aside>
  </div>
</div>
<script id="dlp2-data" type="application/json">
{
  "nodes": [
    {
      "slug": "mpi-intro",
      "title": "An introduction to parallel programming using Message Passing with MPI",
      "link": "/all-training/events/2026/mpi-intro/",
      "summary": "Message Passing is a widely deployed model in massively parallel high-performance computing. This course introduces distributed memory concepts and core MPI calls.",
      "level": 0
    },
    {
      "slug": "eigen-cpp",
      "title": "Array computing in C++ using Eigen",
      "link": "/all-training/events/2026/eigen-cpp/",
      "summary": "This course introduces students to high-performance array computing in C++ using the Eigen library, a versatile template library for linear algebra, matrices, and vectors.",
      "level": 0
    },
    {
      "slug": "singularity-apptainer",
      "title": "Basic Singularity/Apptainer",
      "link": "/all-training/events/2026/singularity-apptainer/",
      "summary": "An introduction to the basic concepts of containerised software environment solution within the Singularity/Apptainer framework (run, build, etc.)",
      "level": 0
    },
    {
      "slug": "bianca-intermediate",
      "title": "Bianca In-Depth Workshop/Hackathon: Improve Your Handling of Sensitive Research Data",
      "link": "/all-training/events/2026/bianca-intermediate/",
      "summary": "Terminal login, file transfer from a terminal, advanced Slurm, and installing custom software and packages.",
      "level": 0
    },
    {
      "slug": "file-transfer-201",
      "title": "File Transfer 201",
      "link": "/all-training/events/2026/file-transfer-201/",
      "summary": "Transfer with terminal tools, including cluster to cluster.",
      "level": 0
    },
    {
      "slug": "combined-python-intro-and-python-hpc",
      "title": "Introduction to Python and Using Python in an HPC environment",
      "link": "/all-training/events/2026/combined-python-intro-and-python-hpc/",
      "summary": "A brief, but comprehensive introduction to using Python in a Swedish academic High-Performance Computing (HPC) environment.",
      "level": 0
    },
    {
      "slug": "naiss-intro-days",
      "title": "NAISS Introduction Training Days",
      "link": "/all-training/events/2026/naiss-intro-days/",
      "summary": "Aimed at new users, covering: Linux, connecting, file transfer, software use and batch systems.",
      "level": 0
    },
    {
      "slug": "programming-formalisms",
      "title": "Programming Formalisms",
      "link": "/all-training/events/2026/programming-formalisms/",
      "summary": "Developing academic software that you can trust to be 'good enough'.",
      "level": 0
    },
    {
      "slug": "paraview",
      "title": "Scientific Visualization with ParaView",
      "link": "/all-training/events/2026/paraview/",
      "summary": "Participants will first learn the fundamentals of ParaView, including data loading, basic visualization techniques, and essential features for scientific data exploration. During the training, several example data sets will be examined and visualized.",
      "level": 0
    },
    {
      "slug": "grace-hopper-gpu",
      "title": "Efficient Use of the Grace Hopper GPU Nodes on Dardel and Arrhenius",
      "link": "/all-training/events/2026/grace-hopper-gpu/",
      "summary": "Efficient use of the Grace Hopper GPU nodes on Dardel and Arrhenius.",
      "level": 1
    },
    {
      "slug": "python-intro",
      "title": "Intro to Python for HPC",
      "link": "/all-training/events/2026/python-intro/",
      "summary": "This 1-day course lets you write and run Python code on an HPC cluster.",
      "level": 1
    },
    {
      "slug": "python-hpc",
      "title": "Using Python in an HPC Environment",
      "link": "/all-training/events/2026/python-hpc/",
      "summary": "Python HPC",
      "level": 2
    },
    {
      "slug": "ai-hpc",
      "title": "AI and HPC",
      "link": "/all-training/events/2026/ai-hpc/",
      "summary": "Introduction to deep learning concepts and practical AI workloads on HPC systems, including parallel execution.",
      "level": 3
    }
  ],
  "edges": [
    {
      "source": "mpi-intro",
      "target": "grace-hopper-gpu",
      "type": "prerequisite",
      "label": "Prerequisite"
    },
    {
      "source": "naiss-intro-days",
      "target": "python-intro",
      "type": "prerequisite",
      "label": "Prerequisite"
    },
    {
      "source": "python-hpc",
      "target": "ai-hpc",
      "type": "progression",
      "label": "Progression"
    },
    {
      "source": "python-intro",
      "target": "python-hpc",
      "type": "progression",
      "label": "Progression"
    },
    {
      "source": "eigen-cpp",
      "target": "mpi-intro",
      "type": "related",
      "label": "Related"
    },
    {
      "source": "eigen-cpp",
      "target": "programming-formalisms",
      "type": "related",
      "label": "Related"
    },
    {
      "source": "naiss-intro-days",
      "target": "file-transfer-201",
      "type": "related",
      "label": "Related"
    },
    {
      "source": "python-hpc",
      "target": "combined-python-intro-and-python-hpc",
      "type": "related",
      "label": "Related"
    },
    {
      "source": "python-intro",
      "target": "combined-python-intro-and-python-hpc",
      "type": "related",
      "label": "Related"
    },
    {
      "source": "singularity-apptainer",
      "target": "bianca-intermediate",
      "type": "related",
      "label": "Related"
    },
    {
      "source": "singularity-apptainer",
      "target": "naiss-intro-days",
      "type": "related",
      "label": "Related"
    }
  ],
  "meta": {
    "courseCount": 13,
    "connectionCount": 11,
    "skippedReferences": 17
  }
}
</script>
<script>
(() => {
  const dataElement = document.getElementById("dlp2-data");
  if (!dataElement) {
    return;
  }

  const graph = JSON.parse(dataElement.textContent);
  const nodeElements = new Map();
  const edgeElements = [];
  const nodeData = new Map(graph.nodes.map((node) => [node.slug, node]));
  const connectionsBySlug = new Map(graph.nodes.map((node) => [node.slug, []]));
  const defaultSeed = "naiss-intro-days";
  const urlSeed = new URLSearchParams(window.location.search).get("seed");
  const seedSlug = (urlSeed && nodeData.has(urlSeed)) ? urlSeed : (nodeData.has(defaultSeed) ? defaultSeed : null);
  let mode = "all";
  let lockedSlug = null;

  document.querySelectorAll(".dlp2-node").forEach((element) => {
    nodeElements.set(element.dataset.slug, element);
  });

  document.querySelectorAll(".dlp2-edge").forEach((element) => {
    const edge = {
      element,
      source: element.dataset.source,
      target: element.dataset.target,
      type: element.dataset.type,
    };
    edgeElements.push(edge);
    connectionsBySlug.get(edge.source).push(edge);
    connectionsBySlug.get(edge.target).push(edge);
  });

  const nameElement = document.getElementById("dlp2-course-name");
  const summaryElement = document.getElementById("dlp2-course-summary");
  const linkElement = document.getElementById("dlp2-course-link");
  const connectionListElement = document.getElementById("dlp2-course-connections");
  const seedHintElement = document.getElementById("dlp2-seed-hint");
  const showAllButton = document.getElementById("dlp2-show-all");
  const resetSeedButton = document.getElementById("dlp2-reset-seed");
  const graphElement = document.querySelector(".dlp2-graph");

  function relationText(edge, slug) {
    if (edge.type === "prerequisite") {
      return edge.source === slug ? ["Prerequisite for", edge.target] : ["Requires", edge.source];
    }
    if (edge.type === "progression") {
      return edge.source === slug ? ["Progresses to", edge.target] : ["Previous step", edge.source];
    }
    return ["Related to", edge.source === slug ? edge.target : edge.source];
  }

  function renderConnections(slug) {
    connectionListElement.innerHTML = "";
    const connections = connectionsBySlug.get(slug) || [];
    if (connections.length === 0) {
      const item = document.createElement("li");
      item.textContent = "No mapped neighbors for this course.";
      connectionListElement.appendChild(item);
      return;
    }

    const sortedConnections = [...connections].sort((left, right) => {
      const leftMeta = relationText(left, slug);
      const rightMeta = relationText(right, slug);
      return leftMeta[0].localeCompare(rightMeta[0]) || leftMeta[1].localeCompare(rightMeta[1]);
    });

    sortedConnections.forEach((edge) => {
      const [label, otherSlug] = relationText(edge, slug);
      const otherNode = nodeData.get(otherSlug);
      if (!otherNode) {
        return;
      }
      const item = document.createElement("li");
      const kind = document.createElement("span");
      kind.className = "dlp2-connection-kind";
      kind.textContent = label;
      const link = document.createElement("a");
      link.href = otherNode.link;
      link.textContent = otherNode.title;
      item.appendChild(kind);
      item.appendChild(link);
      connectionListElement.appendChild(item);
    });
  }

  function resetPanel() {
    nameElement.textContent = "Hover a course circle";
    summaryElement.textContent = "The course title and its connected neighbors will appear here.";
    linkElement.hidden = true;
    linkElement.href = "#";
    connectionListElement.innerHTML = "";
  }

  function renderAllState() {
    nodeElements.forEach((element) => {
      element.classList.remove("is-active", "is-connected", "is-muted");
    });
    edgeElements.forEach((edge) => {
      edge.element.classList.remove("is-active", "is-muted");
    });
    nameElement.textContent = "All courses";
    summaryElement.textContent = "All courses are visible. Hover a circle to inspect one course and its direct neighbors.";
    linkElement.hidden = true;
    linkElement.href = "#";
    connectionListElement.innerHTML = "";
  }

  function syncControlState() {
    if (showAllButton) {
      showAllButton.classList.toggle("is-active", mode === "all");
    }
    if (resetSeedButton) {
      resetSeedButton.classList.toggle("is-active", mode === "seeded");
      resetSeedButton.disabled = !seedSlug;
    }
    if (seedHintElement) {
      if (!seedSlug) {
        seedHintElement.textContent = "Start view shows all courses. Hover a course to highlight its direct neighbors.";
      } else if (urlSeed && nodeData.has(urlSeed)) {
        seedHintElement.textContent = `Start view shows all courses. Reset to intro path will focus URL seed: ${seedSlug}.`;
      } else {
        seedHintElement.textContent = `Start view shows all courses. Use Reset to intro path to focus ${seedSlug}.`;
      }
    }
  }

  function applySelection(slug) {
    if (!slug || !nodeData.has(slug)) {
      if (mode === "all") {
        renderAllState();
      } else if (seedSlug) {
        applySelection(seedSlug);
      } else {
        renderAllState();
      }
      return;
    }

    const connectedNodes = new Set([slug]);
    edgeElements.forEach((edge) => {
      const touchesNode = edge.source === slug || edge.target === slug;
      edge.element.classList.toggle("is-active", touchesNode);
      edge.element.classList.toggle("is-muted", !touchesNode);
      if (touchesNode) {
        connectedNodes.add(edge.source);
        connectedNodes.add(edge.target);
      }
    });

    nodeElements.forEach((element, nodeSlug) => {
      const isActive = nodeSlug === slug;
      const isConnected = connectedNodes.has(nodeSlug) && !isActive;
      element.classList.toggle("is-active", isActive);
      element.classList.toggle("is-connected", isConnected);
      element.classList.toggle("is-muted", !connectedNodes.has(nodeSlug));
    });

    const activeNode = nodeData.get(slug);
    nameElement.textContent = activeNode.title;
    summaryElement.textContent = activeNode.summary || "No short description is set for this course.";
    linkElement.hidden = false;
    linkElement.href = activeNode.link;
    renderConnections(slug);
  }

  nodeElements.forEach((element, slug) => {
    element.addEventListener("mouseenter", () => {
      if (lockedSlug) {
        return;
      }
      applySelection(slug);
    });

    element.addEventListener("focus", () => {
      applySelection(slug);
    });

    element.addEventListener("click", () => {
      lockedSlug = lockedSlug === slug ? null : slug;
      applySelection(lockedSlug || slug);
      if (!lockedSlug) {
        applySelection(null);
      }
    });

    element.addEventListener("keydown", (event) => {
      if (event.key !== "Enter" && event.key !== " ") {
        return;
      }
      event.preventDefault();
      lockedSlug = lockedSlug === slug ? null : slug;
      if (lockedSlug) {
        applySelection(lockedSlug);
      } else {
        applySelection(null);
      }
    });
  });

  if (graphElement) {
    graphElement.addEventListener("mouseleave", () => {
      if (!lockedSlug) {
        applySelection(null);
      }
    });
  }

  if (showAllButton) {
    showAllButton.addEventListener("click", () => {
      mode = "all";
      lockedSlug = null;
      syncControlState();
      renderAllState();
    });
  }

  if (resetSeedButton) {
    resetSeedButton.addEventListener("click", () => {
      if (!seedSlug) {
        mode = "all";
        renderAllState();
        return;
      }
      mode = "seeded";
      lockedSlug = null;
      syncControlState();
      applySelection(seedSlug);
    });
  }

  syncControlState();
  if (mode === "seeded" && seedSlug) {
    applySelection(seedSlug);
  } else {
    renderAllState();
  }
})();
</script>
