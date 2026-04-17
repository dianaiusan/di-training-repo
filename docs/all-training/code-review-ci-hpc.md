---
title: "Code Review and CI on HPC"
slug: "code-review-ci-hpc"  # Must match the file name without .md
status: "upcoming"  # Options: upcoming, ongoing, past, cancelled
format: "online"  # Options: online, on-site, hybrid, self-study
duration: "0.5 day"
short_description: "Branch strategies, pull requests, and continuous integration workflows adapted for HPC and research software projects."
registration_url: ""

tags: ["git", "ci-cd", "code-review", "reproducibility", "best-practices", "intermediate"]
prerequisites: ["git-version-control"]
scientific_domains: ["general-hpc", "computational-science"]
related: ["git-version-control", "programming-formalisms", "workflow-management"]
learning_paths: ["developer"]

#external_url: "https://example.com/course"  # Optional external link
#provider: "ENCCS"  # Provider name if external

materials: []

icon: lucide/git-pull-request
---

# Code Review and CI on HPC

## Summary

Reliable research software requires more than version control — it needs systematic review and automated testing. This half-day workshop covers practical code review workflows and CI/CD patterns adapted to the constraints of HPC environments: long-running jobs, cluster schedulers, and limited internet access on compute nodes.

## Learning objectives

- Apply a branch-based development strategy (feature branches, protected main)
- Open, review, and merge pull requests on GitHub/GitLab
- Write lightweight automated tests suitable for HPC code
- Configure GitHub Actions or GitLab CI pipelines to lint, test, and validate on push
- Adapt CI workflows for cluster-specific challenges (offline nodes, large input data, scheduler integration)

## Prerequisites

- Version control basics: [Version Control and Reproducible Research with Git](git-version-control.md)

## Course outline

### Part 1 — Branch strategies and pull requests (1.5 h)

- Feature-branch workflow and when to use it
- Writing useful commit messages and PR descriptions
- Giving and receiving constructive code review
- Protecting the main branch: required reviews, status checks

### Part 2 — Continuous integration on HPC (1.5 h)

- What CI gives you on a research project
- Setting up a minimal GitHub Actions / GitLab CI pipeline
- Testing strategies for code that depends on MPI, GPUs, or large files
- Caching dependencies and artefacts to keep pipelines fast
- Self-hosted runners on NAISS systems (overview)

## Practical exercises

Participants will add a CI pipeline to an existing research script repository, configure a branch protection rule, and complete a round of peer code review using a provided pull request.

## After this course

Consider these related courses to continue developing your software engineering practice:

- [Programming Formalisms](programming-formalisms.md)
- [Large Dataset Management for HPC](data-management-large.md)
- [Workflow Management for HPC](workflow-management.md)

<!-- GENERATED:bundle-links:start -->
## Part of bundles

- [Developer Bootcamp Week](../explore/bundles/developer-bootcamp-week/)

<!-- GENERATED:bundle-links:end -->
