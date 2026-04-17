---
title: "Shared Memory Parallel Programming with OpenMP"
slug: "openmp-intro"  # Must match the file name without .md
status: "upcoming"  # Options: upcoming, ongoing, past, cancelled
format: "online"  # Options: online, on-site, hybrid, self-study
duration: "3 days"
short_description: "Introduction to shared memory parallel programming using OpenMP for multi-core systems."
registration_url: ""

tags: ["parallel", "openmp", "threading", "performance", "intermediate", "hpc"]
prerequisites: ["naiss-intro"]
scientific_domains: ["general-hpc", "computational-science"]
related: ["mpi-intro", "performance-tuning"]
learning_paths: ["developer"]

#external_url: "https://example.com/course"  # Optional external link
#provider: "ENCCS"  # Provider name if external

materials: []

icon: lucide/cpu
---

# Shared Memory Parallel Programming with OpenMP

Learn to harness the power of shared memory parallelism using OpenMP, the industry-standard API for parallel programming on multicore systems.

## Course Details

**Dates**: TBD  
**Location**: Online  
**Duration**: 3 days  
**Level**: Intermediate

## Summary

This course provides a comprehensive introduction to shared memory parallel programming using OpenMP. You'll learn how to parallelize existing serial code and write efficient parallel programs that scale across multiple CPU cores.

## Learning objectives

- Understand shared memory parallelism concepts
- Master OpenMP directives and clauses
- Implement common parallel patterns (loops, tasks, sections)
- Optimize parallel code performance
- Debug and profile OpenMP applications
- Combine OpenMP with MPI for hybrid parallelism

## Topics Covered

### Day 1: OpenMP Fundamentals
- Introduction to shared memory parallelism
- OpenMP execution model and memory model
- Basic OpenMP directives (parallel, for, sections)
- Work sharing constructs
- Data sharing attributes (private, shared, reduction)

### Day 2: Advanced OpenMP Features
- Task parallelism and task dependencies
- Synchronization constructs (critical, atomic, barriers)
- Loop scheduling and optimization
- Memory management and firstprivate/lastprivate
- Nested parallelism

### Day 3: Performance and Hybrid Programming
- Performance analysis and optimization
- Profiling OpenMP applications
- Common performance pitfalls and solutions
- Hybrid MPI + OpenMP programming
- Best practices and debugging techniques

## Prerequisites

- Programming experience in C, C++, or Fortran
- Basic understanding of parallel computing concepts
- Familiarity with Linux command line

## Target Audience

- Researchers and developers working with computationally intensive applications
- Students in computational science and engineering
- HPC users looking to optimize single-node performance

## Materials

- Course slides and examples
- OpenMP reference guide
- Performance profiling tools
- Access to HPC systems for hands-on exercises

## Related Courses

- [MPI Introduction](mpi-intro.md) - Distributed memory parallelism
- [Hybrid Programming with OpenMP and MPI](hybrid-programming.md) - Combined approaches
- [Performance Tuning](performance-tuning.md) - Advanced optimization techniques