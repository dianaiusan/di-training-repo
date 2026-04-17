---
title: "Cloud HPC: Integrating Cloud Resources with Traditional HPC"
slug: "cloud-hpc"  # Must match the file name without .md
status: "upcoming"  # Options: upcoming, ongoing, past, cancelled
format: "online"  # Options: online, on-site, hybrid, self-study
duration: "3 days"
short_description: "Learn to integrate cloud computing resources with traditional HPC systems for enhanced scalability and flexibility."
registration_url: ""

tags: ["cloud", "aws", "azure", "hybrid", "scalability", "intermediate", "hpc", "infrastructure"]
prerequisites: ["naiss-intro"]
scientific_domains: ["general-hpc"]
related: ["performance-tuning"]
learning_paths: ["developer"]

#external_url: "https://example.com/course"  # Optional external link
#provider: "ENCCS"  # Provider name if external

materials: []

icon: lucide/cloud
---

# Cloud HPC: Integrating Cloud Resources with Traditional HPC

Learn to leverage cloud computing resources alongside traditional HPC systems for enhanced scalability, flexibility, and cost-effectiveness.

## Course Details

**Dates**: TBD  
**Location**: Online  
**Duration**: 3 days  
**Level**: Intermediate

## Summary

This course explores the integration of cloud computing with traditional HPC infrastructure. You'll learn how to use cloud resources for burst computing, data analysis, and hybrid workflows that combine the best of both on-premises and cloud environments.

## Learning objectives

- Understand cloud HPC service offerings
- Design hybrid on-premises/cloud workflows
- Implement cloud bursting strategies
- Manage data transfer between environments
- Optimize costs for cloud HPC usage
- Ensure security in hybrid environments

## Topics Covered

### Day 1: Cloud HPC Fundamentals
- Cloud computing basics for HPC
- Major cloud providers (AWS, Azure, GCP)
- HPC-specific cloud services
- Cost models and pricing strategies
- Security considerations for cloud HPC

### Day 2: Hybrid Cloud Architectures
- On-premises/cloud integration patterns
- Data transfer and synchronization
- Container orchestration across environments
- Workflow portability between systems
- Monitoring and management of hybrid systems

### Day 3: Practical Implementation
- Cloud bursting with SLURM
- Serverless HPC with AWS Lambda/Azure Functions
- GPU cloud instances for AI/ML
- Cost optimization strategies
- Real-world case studies and best practices

## Prerequisites

- Experience with traditional HPC systems
- Basic understanding of cloud computing concepts
- Familiarity with Linux and command-line tools
- Knowledge of job schedulers (SLURM preferred)

## Target Audience

- HPC system administrators
- Computational scientists exploring cloud options
- IT managers planning hybrid infrastructures
- Researchers needing scalable computing resources

## Cloud Services Covered

- **AWS**: EC2, ParallelCluster, Batch, Lambda, S3
- **Azure**: Virtual Machines, CycleCloud, Batch, Functions
- **GCP**: Compute Engine, Cloud Life Sciences, AI Platform
- **Hybrid Tools**: Cloud bursting frameworks, data sync tools

## Materials

- Cloud account setup guides
- Hybrid workflow examples
- Cost calculation spreadsheets
- Security configuration templates

## Cloud HPC Use Cases

- **Burst Computing**: Handle peak workloads in cloud
- **Data Analysis**: Process large datasets cost-effectively
- **Development/Testing**: Isolated environments for code development
- **Global Collaboration**: Share resources across institutions
- **Disaster Recovery**: Backup HPC capabilities in cloud

## Integration Strategies

- **Seamless Access**: Single sign-on across environments
- **Unified Queuing**: Submit jobs to both local and cloud resources
- **Data Management**: Efficient transfer and caching strategies
- **Cost Control**: Automated scaling and budget management
- **Security**: Consistent policies across hybrid environments

## Related Courses

- [Container Workshop](singularity-workshop.md) - Container portability
- [Workflow Management](workflow-management.md) - Orchestrating hybrid workflows
- [File Transfer Advanced](file-transfer-201.md) - Data movement strategies
- [AI and HPC](ai-hpc.md) - GPU cloud resources for ML
