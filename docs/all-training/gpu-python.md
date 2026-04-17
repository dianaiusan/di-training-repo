---
title: "GPU Computing with Python: CuPy and JAX"
slug: "gpu-python"  # Must match the file name without .md
status: "upcoming"  # Options: upcoming, ongoing, past, cancelled
format: "online"  # Options: online, on-site, hybrid, self-study
duration: "1 day"
short_description: "Use CuPy and JAX to run GPU-accelerated Python code on NAISS systems without writing CUDA kernels."
registration_url: ""

tags: ["gpu", "python", "cupy", "jax", "machine-learning", "data-science", "intermediate", "hpc"]
prerequisites: ["python-hpc"]
scientific_domains: ["machine-learning", "data-science", "computational-physics", "computational-science"]
related: ["ai-hpc", "gpu-nodes", "performance-tuning", "python-debugging"]
learning_paths: ["developer", "data-science"]

#external_url: "https://example.com/course"  # Optional external link
#provider: "ENCCS"  # Provider name if external

materials: []

icon: lucide/zap
---

# GPU Computing with Python: CuPy and JAX

## Summary

Not all GPU computing requires writing CUDA kernels. CuPy provides a NumPy-compatible API that runs on NVIDIA GPUs, while JAX offers composable transformations (JIT, grad, vmap) for high-performance numerical computing. This course shows how to use both libraries on NAISS GPU nodes, understand when they give real speedups, and avoid common pitfalls like excessive host-device transfers.

## Learning objectives

- Understand the GPU programming model from a Python perspective
- Accelerate NumPy-style code with CuPy
- Use JAX for JIT compilation, automatic differentiation, and vectorisation
- Profile GPU code and interpret performance metrics
- Submit GPU Python jobs to SLURM on NAISS systems

## Prerequisites

- Python on HPC (python-hpc or equivalent)
- Basic familiarity with NumPy

## Practical information

- Date and time:
- Location:
- Registration:

## Materials

Links to slides, exercises, recordings, etc.

## Related training

- [AI and HPC](ai-hpc.md)
- [Efficient use of the Grace Hopper GPU nodes on Dardel and Arrhenius](gpu-nodes.md)
- [HPC Performance Analysis and Tuning](performance-tuning.md)

<!-- GENERATED:bundle-links:start -->
## Part of bundles

- [Data Science Bootcamp Week](../explore/bundles/data-science-bootcamp-week/)

<!-- GENERATED:bundle-links:end -->
