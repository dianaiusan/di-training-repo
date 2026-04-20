---
title: "Hybrid Parallel Programming with MPI and OpenMP"
slug: "hybrid-mpi-openmp"  # Must match the file name without .md
status: ""  # Options: upcoming, ongoing, past, cancelled
format: "online"  # Options: online, on-site, hybrid, self-study
duration: "2 days"
level: "advanced"
start_date: ""
end_date: ""
short_description: "Combine MPI for distributed memory and OpenMP for shared memory parallelism to fully exploit modern multi-node, multi-core HPC systems."
registration_url: ""

tags: ["mpi", "openmp", "parallel", "hybrid", "hpc", "performance"]
prerequisites: ["mpi-intro", "openmp-intro"]
scientific_domains: ["general-hpc", "computational-science", "computational-physics"]
related: ["mpi-intro", "openmp-intro", "performance-tuning"]
learning_paths: ["developer"]

#external_url: "https://example.com/course"  # Optional external link
#provider: "ENCCS"  # Provider name if external

materials: []

icon: lucide/cpu
verification_status: to-be-verified
---

# Hybrid Parallel Programming with MPI and OpenMP

## Summary

Modern HPC clusters consist of many nodes, each with multiple cores sharing memory. Pure MPI programs use one process per core and ignore shared memory; pure OpenMP programs cannot span nodes. Hybrid MPI+OpenMP combines both: MPI for inter-node communication, OpenMP for intra-node threading. This course teaches how to write, tune, and debug hybrid programs that exploit the full hardware hierarchy of NAISS systems.

## Learning objectives

- Understand the motivation for hybrid MPI+OpenMP programming
- Structure a hybrid program correctly
- Launch hybrid jobs with SLURM (tasks per node, threads per task)
- Avoid common pitfalls: thread safety, over-subscription, NUMA effects
- Profile and tune hybrid applications

## Prerequisites

- MPI programming (mpi-intro)
- OpenMP programming (openmp-intro)

## Practical information

- Date and time:
- Location:
- Registration:

## Materials

Links to slides, exercises, recordings, etc.

## Related training

- [An introduction to parallel programming using Message Passing with MPI](mpi-intro.md)
- [Shared Memory Parallel Programming with OpenMP](openmp-intro.md)
- [HPC Performance Analysis and Tuning](performance-tuning.md)

<!-- GENERATED:bundle-links:start -->
## Part of bundles

- [Developer Bootcamp Week](../bundles/developer-bootcamp-week/)

<!-- GENERATED:bundle-links:end -->
