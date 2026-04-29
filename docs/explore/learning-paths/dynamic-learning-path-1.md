---
title: "Dynamic Learning Path"
slug: "dynamic-hpc-path"
description: "A prototype learning path that starts with HPC foundations and increases in intensity as skills build."
stages:
  - id: foundations
    title: "Foundations"
    intensity: 1
    courses:
      - slug: "naiss-intro-days"
        note: "Platform basics, Linux, file transfer, modules, and job submission."
      - slug: "combined-python-intro-and-python-hpc"
        note: "A practical bridge from Python basics into HPC workflows."
  - id: core-workflows
    title: "Core Workflows"
    intensity: 2
    courses:
      - slug: "file-transfer-201"
        note: "Deepens data movement and storage workflows for regular HPC use."
      - slug: "programming-formalisms"
        note: "Strengthens code structure and software design before scaling up."
  - id: parallel-and-accelerated
    title: "Parallel and Accelerated Computing"
    intensity: 3
    courses:
      - slug: "mpi-intro"
        note: "Introduces distributed-memory parallel programming."
      - slug: "grace-hopper-gpu"
        note: "Moves into heterogeneous systems and GPU-aware optimization."
connections:
  - from: "naiss-intro-days"
    to: "file-transfer-201"
    type: "builds-on"
    label: "Builds on"
  - from: "combined-python-intro-and-python-hpc"
    to: "programming-formalisms"
    type: "related"
    label: "Related follow-up"
  - from: "programming-formalisms"
    to: "mpi-intro"
    type: "builds-on"
    label: "Foundation for"
  - from: "mpi-intro"
    to: "grace-hopper-gpu"
    type: "progression"
    label: "Progresses to"
related_paths:
  - beginner
  - developer
  - data-science
---

## Dynamic HPC Learning Path

A prototype learning path that starts with HPC foundations and increases in intensity as skills build.

<div class="lp-swimlane">
  <div class="lp-phase">
    <div class="lp-phase-header">
      <span class="lp-phase-title">Foundations</span>
      <span class="lp-phase-intensity">Intensity 1</span>
    </div>
    <div class="lp-phase-body">
      <div class="lp-course-item">
        <span class="lp-course-num">1</span>
        <div class="lp-course-copy">
          <a href="/all-training/events/2026/naiss-intro-days/">NAISS Introduction Training Days</a>
          <p class="lp-course-note">Platform basics, Linux, file transfer, modules, and job submission.</p>
        </div>
      </div>
      <div class="lp-course-item">
        <span class="lp-course-num">2</span>
        <div class="lp-course-copy">
          <a href="/all-training/events/2026/combined-python-intro-and-python-hpc/">Introduction to Python and Using Python in an HPC environment</a>
          <p class="lp-course-note">A practical bridge from Python basics into HPC workflows.</p>
        </div>
      </div>
    </div>
  </div>
  <div class="lp-phase-arrow">&darr;</div>
  <div class="lp-phase">
    <div class="lp-phase-header">
      <span class="lp-phase-title">Core Workflows</span>
      <span class="lp-phase-intensity">Intensity 2</span>
    </div>
    <div class="lp-phase-body">
      <div class="lp-course-item">
        <span class="lp-course-num">3</span>
        <div class="lp-course-copy">
          <a href="/all-training/events/2026/file-transfer-201/">File Transfer 201</a>
          <p class="lp-course-note">Deepens data movement and storage workflows for regular HPC use.</p>
        </div>
      </div>
      <div class="lp-course-item">
        <span class="lp-course-num">4</span>
        <div class="lp-course-copy">
          <a href="/all-training/events/2026/programming-formalisms/">Programming Formalisms</a>
          <p class="lp-course-note">Strengthens code structure and software design before scaling up.</p>
        </div>
      </div>
    </div>
  </div>
  <div class="lp-phase-arrow">&darr;</div>
  <div class="lp-phase">
    <div class="lp-phase-header">
      <span class="lp-phase-title">Parallel and Accelerated Computing</span>
      <span class="lp-phase-intensity">Intensity 3</span>
    </div>
    <div class="lp-phase-body">
      <div class="lp-course-item">
        <span class="lp-course-num">5</span>
        <div class="lp-course-copy">
          <a href="/all-training/events/2026/mpi-intro/">An introduction to parallel programming using Message Passing with MPI</a>
          <p class="lp-course-note">Introduces distributed-memory parallel programming.</p>
        </div>
      </div>
      <div class="lp-course-item">
        <span class="lp-course-num">6</span>
        <div class="lp-course-copy">
          <a href="/all-training/events/2026/grace-hopper-gpu/">Efficient Use of the Grace Hopper GPU Nodes on Dardel and Arrhenius</a>
          <p class="lp-course-note">Moves into heterogeneous systems and GPU-aware optimization.</p>
        </div>
      </div>
    </div>
  </div>
</div>

### Course connections

<div class="lp-connection-grid">
<div class="lp-connection-card">
  <p class="lp-connection-type">Builds on</p>
  <p class="lp-connection-route">
    <a href="/all-training/events/2026/naiss-intro-days/">NAISS Introduction Training Days</a> <span class="lp-connection-arrow">&rarr;</span> <a href="/all-training/events/2026/file-transfer-201/">File Transfer 201</a>
  </p>
</div>
<div class="lp-connection-card">
  <p class="lp-connection-type">Related follow-up</p>
  <p class="lp-connection-route">
    <a href="/all-training/events/2026/combined-python-intro-and-python-hpc/">Introduction to Python and Using Python in an HPC environment</a> <span class="lp-connection-arrow">&rarr;</span> <a href="/all-training/events/2026/programming-formalisms/">Programming Formalisms</a>
  </p>
</div>
<div class="lp-connection-card">
  <p class="lp-connection-type">Foundation for</p>
  <p class="lp-connection-route">
    <a href="/all-training/events/2026/programming-formalisms/">Programming Formalisms</a> <span class="lp-connection-arrow">&rarr;</span> <a href="/all-training/events/2026/mpi-intro/">An introduction to parallel programming using Message Passing with MPI</a>
  </p>
</div>
<div class="lp-connection-card">
  <p class="lp-connection-type">Progresses to</p>
  <p class="lp-connection-route">
    <a href="/all-training/events/2026/mpi-intro/">An introduction to parallel programming using Message Passing with MPI</a> <span class="lp-connection-arrow">&rarr;</span> <a href="/all-training/events/2026/grace-hopper-gpu/">Efficient Use of the Grace Hopper GPU Nodes on Dardel and Arrhenius</a>
  </p>
</div>
</div>

### Related paths

<div class="lp-related-grid">
<div class="lp-related-card">
  <div class="lp-related-head">
    <p class="lp-related-title"><a href="../beginner/">Beginner HPC Path</a></p>
  </div>
  <p class="lp-related-desc">A structured introduction to practical HPC usage, from first login to reliable day-to-day workflows.</p>
</div>
<div class="lp-related-card">
  <div class="lp-related-head">
    <p class="lp-related-title"><a href="../developer/">Developer HPC Path</a></p>
  </div>
  <p class="lp-related-desc">A deep technical path for developers building scalable, high-performance, and reproducible scientific software.</p>
</div>
<div class="lp-related-card">
  <div class="lp-related-head">
    <p class="lp-related-title"><a href="../data-science/">Data Science on HPC Path</a></p>
  </div>
  <p class="lp-related-desc">A path for researchers and analysts who need scalable data analysis, AI, and reproducible pipelines on HPC platforms.</p>
</div>
</div>
