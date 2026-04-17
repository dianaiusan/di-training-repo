---
title: "Developer HPC Path"
slug: "developer"
description: "A deep technical path for developers building scalable, high-performance, and reproducible scientific software."
icon: lucide/code-2
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

### Progression map

```mermaid
graph LR
  subgraph Foundation
    n_programming_formalisms["Programming Formalisms"]
    n_git_version_control["Version Control and Reproducible Research with Git"]
    n_environment_management["Software Environment Management on HPC"]
  end
  subgraph Parallel Programming
    n_mpi_intro["An introduction to parallel programming using Message Passing with MPI"]
    n_openmp_intro["Shared Memory Parallel Programming with OpenMP"]
    n_hybrid_mpi_openmp["Hybrid Parallel Programming with MPI and OpenMP"]
    n_parallel_python_mpi["Parallel Python with MPI"]
  end
  subgraph Performance
    n_performance_tuning["HPC Performance Analysis and Tuning"]
    n_performance_external["Advanced Performance Engineering for HPC"]
    n_gpu_nodes["Efficient use of the Grace Hopper GPU nodes on Dardel and Arrhenius"]
  end
  subgraph Production Workflows
    n_cloud_hpc["Cloud HPC: Integrating Cloud Resources with Traditional HPC"]
    n_workflow_management["Scientific Workflow Management on HPC"]
    n_python_debugging["Debugging and Profiling Python on HPC"]
    n_job_arrays["Scaling Experiments with SLURM Job Arrays"]
  end
  n_programming_formalisms --> n_git_version_control
  n_git_version_control --> n_environment_management
  n_environment_management --> n_mpi_intro
  n_mpi_intro --> n_openmp_intro
  n_openmp_intro --> n_hybrid_mpi_openmp
  n_hybrid_mpi_openmp --> n_parallel_python_mpi
  n_parallel_python_mpi --> n_performance_tuning
  n_performance_tuning --> n_performance_external
  n_performance_external --> n_gpu_nodes
  n_gpu_nodes --> n_cloud_hpc
  n_cloud_hpc --> n_workflow_management
  n_workflow_management --> n_python_debugging
  n_python_debugging --> n_job_arrays
```

### Recommended order

1. [Programming Formalisms](/all-training/programming-formalisms.md)
2. [Version Control and Reproducible Research with Git](/all-training/git-version-control.md)
3. [Software Environment Management on HPC](/all-training/environment-management.md)
4. [An introduction to parallel programming using Message Passing with MPI](/all-training/mpi-intro.md)
5. [Shared Memory Parallel Programming with OpenMP](/all-training/openmp-intro.md)
6. [Hybrid Parallel Programming with MPI and OpenMP](/all-training/hybrid-mpi-openmp.md)
7. [Parallel Python with MPI](/all-training/parallel-python-mpi.md)
8. [HPC Performance Analysis and Tuning](/all-training/performance-tuning.md)
9. [Advanced Performance Engineering for HPC](/all-training/performance-external.md)
10. [Efficient use of the Grace Hopper GPU nodes on Dardel and Arrhenius](/all-training/gpu-nodes.md)
11. [Cloud HPC: Integrating Cloud Resources with Traditional HPC](/all-training/cloud-hpc.md)
12. [Scientific Workflow Management on HPC](/all-training/workflow-management.md)
13. [Debugging and Profiling Python on HPC](/all-training/python-debugging.md)
14. [Scaling Experiments with SLURM Job Arrays](/all-training/job-arrays.md)

### Phase breakdown

#### Foundation
- [Programming Formalisms](/all-training/programming-formalisms.md)
- [Version Control and Reproducible Research with Git](/all-training/git-version-control.md)
- [Software Environment Management on HPC](/all-training/environment-management.md)

#### Parallel Programming
- [An introduction to parallel programming using Message Passing with MPI](/all-training/mpi-intro.md)
- [Shared Memory Parallel Programming with OpenMP](/all-training/openmp-intro.md)
- [Hybrid Parallel Programming with MPI and OpenMP](/all-training/hybrid-mpi-openmp.md)
- [Parallel Python with MPI](/all-training/parallel-python-mpi.md)

#### Performance
- [HPC Performance Analysis and Tuning](/all-training/performance-tuning.md)
- [Advanced Performance Engineering for HPC](/all-training/performance-external.md)
- [Efficient use of the Grace Hopper GPU nodes on Dardel and Arrhenius](/all-training/gpu-nodes.md)

#### Production Workflows
- [Cloud HPC: Integrating Cloud Resources with Traditional HPC](/all-training/cloud-hpc.md)
- [Scientific Workflow Management on HPC](/all-training/workflow-management.md)
- [Debugging and Profiling Python on HPC](/all-training/python-debugging.md)
- [Scaling Experiments with SLURM Job Arrays](/all-training/job-arrays.md)

### Related paths

- [Beginner](./beginner.md)
- [Data Science](./data-science.md)
