---
title: "Debugging and Profiling Clinic"
slug: "debugging-profiling-clinic"  # Must match the file name without .md
status: ""  # Options: upcoming, ongoing, past, cancelled
format: "online"  # Options: online, on-site, hybrid, self-study
duration: "0.5 day"
level: "intermediate"
start_date: ""
end_date: ""
short_description: "Hands-on troubleshooting and profiling clinic for HPC code — find bugs and bottlenecks before optimising."
registration_url: ""

tags: ["debugging", "profiling", "performance", "hpc"]
prerequisites: ["naiss-intro"]
scientific_domains: ["general-hpc", "computational-science"]
related: ["performance-tuning", "python-debugging", "mpi-intro", "openmp-intro"]
learning_paths: ["developer"]

#external_url: "https://example.com/course"  # Optional external link
#provider: "ENCCS"  # Provider name if external

materials: []

icon: lucide/bug
verification_status: to-be-verified
---

# Debugging and Profiling Clinic

## Summary

Before optimising, you must understand what your code is actually doing. This half-day clinic provides a structured workflow for diagnosing bugs and identifying performance bottlenecks in HPC applications. Participants bring their own code or work on provided examples to practise with real tools used on NAISS systems.

## Learning objectives

- Apply a systematic debugging strategy to serial and parallel code
- Use GDB, Valgrind, and compiler sanitisers to locate memory and logic errors
- Collect and interpret profiles with `perf`, `gprof`, and Score-P / Scalasca
- Identify the dominant cost in a profile (compute bound, memory bound, communication bound)
- Decide when code is ready to optimise (and when it is not)

## Prerequisites

- HPC basics: [Introduction and Orientation to NAISS](naiss-intro.md)

## Course outline

### Part 1 — Debugging strategies (1.5 h)

- Reproducible bug reports: minimal examples, seed control, deterministic replay
- Serial debugging with GDB: breakpoints, watchpoints, backtraces
- Memory errors: Valgrind Memcheck and AddressSanitizer
- Debugging parallel code: rank-specific gdb attach, DDT/TotalView overview
- Common MPI and OpenMP pitfalls (race conditions, deadlocks)

### Part 2 — Profiling and hotspot analysis (1.5 h)

- Sampling vs. instrumentation profiling
- `perf stat` and `perf record` for quick hardware counter profiles
- `gprof` for serial Fortran/C/C++ code
- Score-P and Scalasca for MPI/OpenMP applications
- Reading a flame graph
- Roofline model: where does your code sit?

## Practical exercises

Each participant (or pair) picks a buggy or slow code snippet and works through the debugging/profiling workflow with instructor support. Common patterns are debrief as a group.

## After this course

Ready to move from profiling to optimisation? Continue with:

- [HPC Performance Analysis and Tuning](performance-tuning.md)
- [Parallel Python with MPI](parallel-python-mpi.md)

<!-- GENERATED:bundle-links:start -->
## Part of bundles

- [Developer Bootcamp Week](../bundles/developer-bootcamp-week/)

<!-- GENERATED:bundle-links:end -->
