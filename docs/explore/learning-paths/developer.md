---
title: "Developer HPC Path"
slug: "developer"
description: "A deep technical path for developers building scalable, high-performance, and reproducible scientific software."
phases:
  foundation:
    - programming-formalisms
    - git-version-control
    - environment-management
  parallel-programming:
    - mpi-intro
    - openmp-intro
    - hybrid-mpi-openmp
    - parallel-python-mpi
  performance:
    - performance-tuning
    - performance-external
    - gpu-nodes
  production-workflows:
    - cloud-hpc
    - workflow-management
    - python-debugging
    - job-arrays
related_paths:
  - beginner
  - data-science
---
## Developer HPC Path

A deep technical path for developers building scalable, high-performance, and reproducible scientific software.

<style>.lp-swimlane {  display: flex;  flex-direction: column;  align-items: stretch;  max-width: 36rem;  gap: 0;  padding: 0.75rem 0 1.25rem 0;  margin: 1.25rem 0;}.lp-phase {  width: 100%;  border: 1px solid #ddd;  border-radius: 10px;  overflow: hidden;}.lp-phase-header {  background: var(--md-accent-fg-color, #526cfe);  color: #fff;  font-weight: 700;  font-size: 0.82rem;  text-transform: uppercase;  letter-spacing: 0.04em;  padding: 0.5rem 0.9rem;  text-align: center;}.lp-phase-body {  padding: 0.75rem 0.9rem;  background: #fff;  display: flex;  flex-direction: column;  gap: 0.5rem;}.lp-course-item {  display: flex;  align-items: flex-start;  gap: 0.5rem;  font: inherit;  line-height: 1.45;}.lp-course-num {  flex-shrink: 0;  width: 1.45em;  height: 1.45em;  border-radius: 50%;  background: var(--md-accent-fg-color, #526cfe);  color: #fff;  font-size: 0.74rem;  font-weight: 700;  display: flex;  align-items: center;  justify-content: center;  margin-top: 0.08em;}.lp-phase-arrow {  align-self: center;  font-size: 1.15rem;  color: var(--md-accent-fg-color, #526cfe);  padding: 0.25rem 0;  user-select: none;}@media (max-width: 640px) {  .lp-swimlane {    max-width: 100%;    margin: 1rem 0;  }  .lp-phase-header {    font-size: 0.78rem;    padding: 0.45rem 0.75rem;  }  .lp-phase-body {    padding: 0.65rem 0.75rem;  }  .lp-course-item {    line-height: 1.4;  }}</style>
<div class="lp-swimlane">
  <div class="lp-phase">
    <div class="lp-phase-header">Foundation</div>
    <div class="lp-phase-body">
      <div class="lp-course-item"><span class="lp-course-num">1</span><a href="../../../all-training/programming-formalisms/">Programming Formalisms</a></div>
      <div class="lp-course-item"><span class="lp-course-num">2</span><a href="../../../all-training/git-version-control/">Version Control and Reproducible Research with Git</a></div>
      <div class="lp-course-item"><span class="lp-course-num">3</span><a href="../../../all-training/environment-management/">Software Environment Management on HPC</a></div>
    </div>
  </div>
  <div class="lp-phase-arrow">&darr;</div>
  <div class="lp-phase">
    <div class="lp-phase-header">Parallel Programming</div>
    <div class="lp-phase-body">
      <div class="lp-course-item"><span class="lp-course-num">4</span><a href="../../../all-training/mpi-intro/">An introduction to parallel programming using Message Passing with MPI</a></div>
      <div class="lp-course-item"><span class="lp-course-num">5</span><a href="../../../all-training/openmp-intro/">Shared Memory Parallel Programming with OpenMP</a></div>
      <div class="lp-course-item"><span class="lp-course-num">6</span><a href="../../../all-training/hybrid-mpi-openmp/">Hybrid Parallel Programming with MPI and OpenMP</a></div>
      <div class="lp-course-item"><span class="lp-course-num">7</span><a href="../../../all-training/parallel-python-mpi/">Parallel Python with MPI</a></div>
    </div>
  </div>
  <div class="lp-phase-arrow">&darr;</div>
  <div class="lp-phase">
    <div class="lp-phase-header">Performance</div>
    <div class="lp-phase-body">
      <div class="lp-course-item"><span class="lp-course-num">8</span><a href="../../../all-training/performance-tuning/">HPC Performance Analysis and Tuning</a></div>
      <div class="lp-course-item"><span class="lp-course-num">9</span><a href="../../../all-training/performance-external/">Advanced Performance Engineering for HPC</a></div>
      <div class="lp-course-item"><span class="lp-course-num">10</span><a href="../../../all-training/gpu-nodes/">Efficient use of the Grace Hopper GPU nodes on Dardel and Arrhenius</a></div>
    </div>
  </div>
  <div class="lp-phase-arrow">&darr;</div>
  <div class="lp-phase">
    <div class="lp-phase-header">Production Workflows</div>
    <div class="lp-phase-body">
      <div class="lp-course-item"><span class="lp-course-num">11</span><a href="../../../all-training/cloud-hpc/">Cloud HPC: Integrating Cloud Resources with Traditional HPC</a></div>
      <div class="lp-course-item"><span class="lp-course-num">12</span><a href="../../../all-training/workflow-management/">Scientific Workflow Management on HPC</a></div>
      <div class="lp-course-item"><span class="lp-course-num">13</span><a href="../../../all-training/python-debugging/">Debugging and Profiling Python on HPC</a></div>
      <div class="lp-course-item"><span class="lp-course-num">14</span><a href="../../../all-training/job-arrays/">Scaling Experiments with SLURM Job Arrays</a></div>
    </div>
  </div>
</div>

### Related paths

<style>.lp-related-grid {  display: grid;  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));  gap: 0.8rem;  margin: 1rem 0 0 0;}.lp-related-card {  border: 1px solid #ddd;  border-radius: 10px;  padding: 0.8rem 0.9rem;  background: #fff;  transition: border-color 180ms ease, background-color 180ms ease;}.lp-related-card:hover {  border-color: var(--md-accent-fg-color, #526cfe);  background: var(--md-accent-fg-color--transparent, rgba(82, 108, 254, 0.12));}.lp-related-head {  display: flex;  align-items: center;  gap: 0.5rem;  margin: 0 0 0.35rem 0;}.lp-related-icon {  color: var(--md-accent-fg-color, #526cfe);  line-height: 1;}.lp-related-title {  margin: 0;  font: inherit;  font-weight: 700;}.lp-related-desc {  margin: 0;  font: inherit;  color: #4b5563;  line-height: 1.4;}.lp-related-card a, .lp-related-card a:visited {  color: var(--md-accent-fg-color, #526cfe);  text-decoration: none;}.lp-related-card:hover a {  text-decoration: underline;}@media (max-width: 640px) {  .lp-related-grid {    grid-template-columns: 1fr;    gap: 0.7rem;  }  .lp-related-card {    padding: 0.75rem 0.8rem;  }  .lp-related-head {    margin-bottom: 0.3rem;  }}</style>
<div class="lp-related-grid">
<div class="lp-related-card">
  <div class="lp-related-head">
    <span class="lp-related-icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="lucide lucide-sprout" viewBox="0 0 24 24" style="width: 1.4em; height: 1.4em; vertical-align: middle;"><path d="M14 9.536V7a4 4 0 0 1 4-4h1.5a.5.5 0 0 1 .5.5V5a4 4 0 0 1-4 4 4 4 0 0 0-4 4c0 2 1 3 1 5a5 5 0 0 1-1 3M4 9a5 5 0 0 1 8 4 5 5 0 0 1-8-4M5 21h14"/></svg></span>
    <p class="lp-related-title"><a href="../beginner/">Beginner HPC Path</a></p>
  </div>
  <p class="lp-related-desc">A structured introduction to practical HPC usage, from first login to reliable day-to-day workflows.</p>
</div>
<div class="lp-related-card">
  <div class="lp-related-head">
    <span class="lp-related-icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="lucide lucide-chart-line" viewBox="0 0 24 24" style="width: 1.4em; height: 1.4em; vertical-align: middle;"><path d="M3 3v16a2 2 0 0 0 2 2h16"/><path d="m19 9-5 5-4-4-3 3"/></svg></span>
    <p class="lp-related-title"><a href="../data-science/">Data Science on HPC Path</a></p>
  </div>
  <p class="lp-related-desc">A path for researchers and analysts who need scalable data analysis, AI, and reproducible pipelines on HPC platforms.</p>
</div>
</div>
