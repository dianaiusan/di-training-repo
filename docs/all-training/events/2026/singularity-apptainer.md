---
title: "Basic Singularity/Apptainer"
slug: "singularity-apptainer" # Use the target course file name without .md in docs/explore/all-training/
url: "/all-training/events/2026/singularity-apptainer/"
external_url: "https://uppmax.github.io/Basic_Singularity_Apptainer/"
#provider: "NAISS"  # Provider name if external

start_date: "2026-02-09"
end_date: "2026-02-09"
dates: ["2026-02-09"]
duration: "1 day"

format: "online"
level: "beginner"

short_description: "An introduction to the basic concepts of containerised software environment solution within the Singularity/Apptainer framework (run, build, etc.)"
registration_url: ""

prerequisites: ["linux-command-line", "hpc-basics"]
related: ["naiss-intro-days", "bianca-intermediate"]

#learning_paths: ["beginner", "developer"]

scientific_domains: ["chemistry", "engineering", "physics"]
tags: ["apptainer", "containers", "environment-management", "hpc-intro", "reproducibility", "singularity"]

icon: lucide/book-open  # Lucide icon for the page
---



# **Why [Singularity](https://sylabs.io)/[Apptainer](https://apptainer.org/)?**

---

- **A secure, single-file based container format**  
SIF&trade; (Singularity Image Format) is a single executable file based container image, cryptographically signed, auditable, secure, and easy to move using existing data mobility paradigms.
- **Support for data-intensive workloads**  
The elegance of Singularity's architecture bridges the gap between HPC and AI, deep learning/machine learning, and predictive analytics.
- **Extreme mobility**  
Use standard file and object copy tools to transport, share, or distribute a Singularity container. Any endpoint with Singularity installed can run the container.
- **Compatibility**  
Designed to support complex architectures and workflows, Singularity is easily adaptable to almost any environment.
- **[More ...](https://sylabs.io/singularity)**
- **[More from the "User documentation" ...](https://sylabs.io/guides/latest/user-guide/introduction.html#why-use-singularityce)**

## **What is Singularity/Apptainer.**

Singularity is not the only [OS level virtualization](https://en.wikipedia.org/wiki/OS-level_virtualization) implementation around. One of the main uses of Singularity is to bring containers and reproducibility to scientific computing and the high-performance computing (HPC) world[^1].

[More on Wikipedia](https://en.wikipedia.org/wiki/Singularity_(software))

## **What is Singularity/Apptainer - an alternative view.**

Singularity runs in the user space i.e. which allows you to run Singularity containers in systems where you have only user rights - common situation on public and government computer resources.

Since your home folder gets automatically mounted/exposed to your virtual environment you can look at it as an **alternative way to expose your data to different complete setups with pre-installed and configured software**.

## **Purpose**
This workshop material aims to demonstrate and exercise some commonly used features by simple interactive tutorials. Thus, this is not complete manual or documentation for Singularity.

The "[Singularity user documentation](https://sylabs.io/guides/latest/user-guide/)"  and "[Apptainer user documentation](https://apptainer.org/documentation/)" are excellent reference sources with basic examples in well-ordered fashion and always up to date.

[^1]: Kurtzer, Gregory M; Sochat, Vanessa; Bauer, Michael W (2017). "Singularity: Scientific containers for mobility of compute". PLOS ONE. 12 (5): e0177459. Bibcode:2017PLoSO..1277459K. [doi:10.1371/journal.pone.0177459](https://doi.org/10.1371%2Fjournal.pone.0177459). PMC [5426675](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5426675). PMID [28494014](https://pubmed.ncbi.nlm.nih.gov/28494014)
