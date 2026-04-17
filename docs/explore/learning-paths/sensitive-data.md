---
title: "Sensitive Data Path"
slug: "sensitive-data"
description: "A practical route for working safely with sensitive data and secure HPC workflows."
icon: lucide/shield-plus
phases:
  foundation:
    - intro
    - naiss-intro
  secure-workflow:
    - bianca-sensitive-data
    - environment-management
  operations:
    - file-transfer-201
    - filesystems-storage
    - git-version-control
related_paths:
  - beginner
  - developer
---
## Sensitive Data Path

A practical route for working safely with sensitive data and secure HPC workflows.

### Progression map

```mermaid
graph LR
  subgraph Foundation
    n_intro["Intro to HPC"]
    n_naiss_intro["NAISS Introduction training days"]
  end
  subgraph Secure Workflow
    n_bianca_sensitive_data["Bianca In-Depth: Improve Your Handling of Sensitive Research Data"]
    n_environment_management["Software Environment Management on HPC"]
  end
  subgraph Operations
    n_file_transfer_201["File Transfer 201"]
    n_filesystems_storage["HPC Filesystems and Storage Management"]
    n_git_version_control["Version Control and Reproducible Research with Git"]
  end
  n_intro --> n_naiss_intro
  n_naiss_intro --> n_bianca_sensitive_data
  n_bianca_sensitive_data --> n_environment_management
  n_environment_management --> n_file_transfer_201
  n_file_transfer_201 --> n_filesystems_storage
  n_filesystems_storage --> n_git_version_control
```

### Recommended order

1. [Intro to HPC](/all-training/intro.md)
2. [NAISS Introduction training days](/all-training/naiss-intro.md)
3. [Bianca In-Depth: Improve Your Handling of Sensitive Research Data](/all-training/bianca-sensitive-data.md)
4. [Software Environment Management on HPC](/all-training/environment-management.md)
5. [File Transfer 201](/all-training/file-transfer-201.md)
6. [HPC Filesystems and Storage Management](/all-training/filesystems-storage.md)
7. [Version Control and Reproducible Research with Git](/all-training/git-version-control.md)

### Phase breakdown

#### Foundation
- [Intro to HPC](/all-training/intro.md)
- [NAISS Introduction training days](/all-training/naiss-intro.md)

#### Secure Workflow
- [Bianca In-Depth: Improve Your Handling of Sensitive Research Data](/all-training/bianca-sensitive-data.md)
- [Software Environment Management on HPC](/all-training/environment-management.md)

#### Operations
- [File Transfer 201](/all-training/file-transfer-201.md)
- [HPC Filesystems and Storage Management](/all-training/filesystems-storage.md)
- [Version Control and Reproducible Research with Git](/all-training/git-version-control.md)

### Related paths

- [Beginner](./beginner.md)
- [Developer](./developer.md)
