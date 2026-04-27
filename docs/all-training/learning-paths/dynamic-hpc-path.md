---
title: "Dynamic HPC Learning Path"
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

# Dynamic HPC Learning Path

This page is a prototype for richer learning-path front matter.

The key idea is:

- stages express the main progression from foundations toward more intensive material
- each stage groups one or more real course slugs
- connections add optional relationships such as `builds-on`, `related`, or `progression`

The generated explore page can use that front matter to render an ordered path plus a compact relationship summary without requiring custom data files outside markdown.
