# Furientis CMMC Level 2 Compliance Strategy

## A Comprehensive Guide to CMMC Certification, Dual-Echelon Architecture, and Operational Excellence

**Version:** 1.0
**Date:** December 2025
**Prepared for:** Furientis Leadership
**Classification:** Internal Use Only

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [CMMC Level 2 Requirements Overview](#2-cmmc-level-2-requirements-overview)
3. [Dual-Echelon Architecture: Government vs. Commercial Operations](#3-dual-echelon-architecture)
4. [Cloud Infrastructure Strategy](#4-cloud-infrastructure-strategy)
5. [IT Infrastructure Requirements](#5-it-infrastructure-requirements)
6. [Software Requirements and Approved Versions](#6-software-requirements)
7. [Operational TTPs for Engineer Productivity](#7-operational-ttps)
8. [Vendor Comparison](#8-vendor-comparison)
9. [Cost Estimates](#9-cost-estimates)
10. [Implementation Roadmap](#10-implementation-roadmap)
11. [Risk Assessment and Common Pitfalls](#11-risk-assessment)
12. [Appendices](#12-appendices)

---

## 1. Executive Summary

### Purpose

This document provides Furientis with a comprehensive strategy for achieving Cybersecurity Maturity Model Certification (CMMC) Level 2 compliance while maintaining operational agility for both government and commercial work streams. As a startup pursuing Department of Defense (DoD) contracts involving Controlled Unclassified Information (CUI), Furientis must implement 110 security practices aligned with NIST SP 800-171 Rev. 2.

### Key Findings

**Compliance Landscape:**
- CMMC 2.0 Phase 1 became effective November 10, 2025
- Level 2 certification requires third-party assessment by an accredited C3PAO
- Conditional certification available with 80% compliance score (180 days to remediate)
- Average preparation timeline: 6-18 months for organizations starting from scratch

**Strategic Recommendations:**

1. **Implement a CUI Enclave Architecture** - Isolate government work from commercial operations to reduce compliance scope and cost while maintaining flexibility for non-regulated work.

2. **Adopt Microsoft 365 GCC High** - While not technically required, GCC High is Microsoft's recommended platform for CMMC Level 2 and is the only Microsoft environment meeting DFARS 7012 paragraphs (c)-(g).

3. **Leverage AWS GovCloud** - Utilize FedRAMP High-authorized infrastructure for compute, storage, and AI/ML workloads requiring CUI access.

4. **Establish Clear Separation** - Physical and logical network segmentation between government (CUI) and commercial operations prevents scope creep and simplifies compliance evidence collection.

### Document Scope

This strategy addresses:
- Technical requirements for CMMC Level 2 certification
- Architecture for separating government and commercial work streams
- Cloud infrastructure selection and configuration
- IT infrastructure including endpoints, shared storage, and collaboration tools
- Software and tooling requirements
- Operational procedures that maintain engineer productivity within compliance constraints
- Vendor options, cost estimates, and implementation timeline

---

## 2. CMMC Level 2 Requirements Overview

### 2.1 What is CMMC?

The Cybersecurity Maturity Model Certification (CMMC) is the DoD's verification mechanism to ensure that contractors implement adequate cybersecurity practices to protect sensitive information. CMMC 2.0, finalized in 2024 and enforced beginning November 2025, streamlined the original five-tier model into three levels:

| Level | Description | Assessment Type | Practices | Data Type |
|-------|-------------|-----------------|-----------|-----------|
| Level 1 | Foundational | Annual Self-Assessment | 17 | FCI |
| Level 2 | Advanced | Third-Party (C3PAO) | 110 | CUI |
| Level 3 | Expert | Government-led (DCMA) | 110+ | Critical CUI |

### 2.2 Level 2 Requirements Detail

CMMC Level 2 directly maps to NIST SP 800-171 Revision 2, requiring implementation of 110 security practices across 14 domains:

| Domain | Abbrev | Practice Count | Key Focus Areas |
|--------|--------|----------------|-----------------|
| Access Control | AC | 22 | Least privilege, session management, remote access |
| Awareness & Training | AT | 3 | Security awareness, role-based training |
| Audit & Accountability | AU | 9 | Logging, audit review, audit protection |
| Configuration Management | CM | 9 | Baseline configs, change control |
| Identification & Authentication | IA | 11 | MFA, password policies, device auth |
| Incident Response | IR | 3 | IR capability, reporting, testing |
| Maintenance | MA | 6 | Controlled maintenance, remote maintenance |
| Media Protection | MP | 9 | Media handling, sanitization, transport |
| Personnel Security | PS | 2 | Screening, personnel actions |
| Physical Protection | PE | 6 | Physical access, visitor control |
| Risk Assessment | RA | 3 | Risk assessments, vulnerability scanning |
| Security Assessment | CA | 4 | Security assessments, POA&M |
| System & Communications Protection | SC | 16 | Boundary protection, encryption, CUI handling |
| System & Information Integrity | SI | 7 | Flaw remediation, malware protection, monitoring |

### 2.3 Assessment Process

**Third-Party Assessment (C3PAO):**
- Required for most Level 2 certifications involving prioritized CUI
- Conducted by CMMC Third-Party Assessment Organizations accredited by CyberAB
- Assessments valid for 3 years
- Scoring based on 320 assessment objectives derived from NIST 800-171A

**Conditional Certification:**
- Available if organization achieves at least 80% compliance score
- Must satisfy all "essential" cybersecurity controls
- 180-day window to remediate remaining findings via POA&M
- POA&M closeout assessment required

### 2.4 Key Documentation Requirements

1. **System Security Plan (SSP)** - Comprehensive description of security controls implementation
2. **Plan of Action and Milestones (POA&M)** - Remediation plan for any gaps
3. **Network Diagram** - Current and accurate network architecture
4. **Data Flow Diagrams** - How CUI moves through your systems
5. **Policies and Procedures** - Written policies for each control family
6. **Evidence of Implementation** - Screenshots, logs, configurations proving control implementation

---

## 3. Dual-Echelon Architecture: Government vs. Commercial Operations

### 3.1 Strategic Rationale

Furientis operates in two distinct contexts: government contracts involving CUI and commercial/research projects without government data or funding. Implementing a **dual-echelon architecture** provides significant advantages:

| Benefit | Description |
|---------|-------------|
| **Reduced Compliance Scope** | Only the government echelon requires CMMC controls, reducing overall cost and complexity |
| **Operational Flexibility** | Commercial work proceeds without compliance constraints |
| **Clear Accountability** | Distinct environments make evidence collection and audit trails simpler |
| **Risk Isolation** | A breach in one environment doesn't automatically compromise the other |
| **Cost Optimization** | Expensive GCC High licensing only for personnel handling CUI |

### 3.2 Recommended Architecture: Physical and Logical Separation

Based on Furientis's needs and the complexity of mixed AI/ML, software development, and data analytics work, we recommend **hybrid separation** combining both physical and logical controls:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FURIENTIS NETWORK ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────┐    ┌─────────────────────────────────┐ │
│  │     GOVERNMENT ECHELON          │    │      COMMERCIAL ECHELON         │ │
│  │     (CUI Environment)           │    │      (Non-regulated)            │ │
│  │                                 │    │                                 │ │
│  │  ┌───────────────────────────┐  │    │  ┌───────────────────────────┐  │ │
│  │  │ Microsoft 365 GCC High    │  │    │  │ Microsoft 365 Commercial  │  │ │
│  │  │ - Exchange Online         │  │    │  │ - Standard M365 suite     │  │ │
│  │  │ - SharePoint              │  │    │  │ - Teams                   │  │ │
│  │  │ - Teams                   │  │    │  │ - OneDrive                │  │ │
│  │  │ - OneDrive for Business   │  │    │  └───────────────────────────┘  │ │
│  │  └───────────────────────────┘  │    │                                 │ │
│  │                                 │    │  ┌───────────────────────────┐  │ │
│  │  ┌───────────────────────────┐  │    │  │ AWS Commercial            │  │ │
│  │  │ AWS GovCloud              │  │    │  │ - EC2/EKS                 │  │ │
│  │  │ - EC2 (GPU instances)     │  │    │  │ - S3                      │  │ │
│  │  │ - S3 (CUI storage)        │  │    │  │ - Bedrock (public models) │  │ │
│  │  │ - Bedrock (Claude, etc.)  │  │    │  │ - SageMaker               │  │ │
│  │  │ - SageMaker               │  │    │  └───────────────────────────┘  │ │
│  │  └───────────────────────────┘  │    │                                 │ │
│  │                                 │    │  ┌───────────────────────────┐  │ │
│  │  ┌───────────────────────────┐  │    │  │ Development Tools         │  │ │
│  │  │ Dedicated Endpoints       │  │    │  │ - GitHub.com              │  │ │
│  │  │ - Gov-issued laptops      │  │    │  │ - Standard IDE configs    │  │ │
│  │  │ - FIPS-validated crypto   │  │    │  │ - Open source tools       │  │ │
│  │  │ - EDR/XDR                 │  │    │  └───────────────────────────┘  │ │
│  │  │ - DLP enabled             │  │    │                                 │ │
│  │  └───────────────────────────┘  │    │  ┌───────────────────────────┐  │ │
│  │                                 │    │  │ Standard Endpoints        │  │ │
│  │  ┌───────────────────────────┐  │    │  │ - BYOD allowed            │  │ │
│  │  │ GitHub Enterprise Server  │  │    │  │ - Basic security          │  │ │
│  │  │ (Self-hosted in GovCloud) │  │    │  └───────────────────────────┘  │ │
│  │  └───────────────────────────┘  │    │                                 │ │
│  │                                 │    │                                 │ │
│  └─────────────────────────────────┘    └─────────────────────────────────┘ │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │                        BOUNDARY CONTROLS                                ││
│  │  • Firewall/NGFW between echelons           • Zero Trust gateway       ││
│  │  • No direct data transfer paths            • Separate VLANs           ││
│  │  • Separate identity providers              • Air-gap where possible   ││
│  └─────────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.3 CUI Enclave Design Principles

The government echelon functions as a **CUI Enclave** with the following characteristics:

**Definition (per CyberAB):** *"A set of system resources that operate within the same security domain and that share the protection of a single, common, and continuous security perimeter."*

**Key Design Principles:**

1. **Strict Boundary Definition**
   - All CUI processing occurs within the enclave
   - Clear documentation of what systems are in/out of scope
   - Network segmentation enforced at multiple layers (VLAN, firewall, zero-trust)

2. **Data Flow Controls**
   - No automated data transfer between echelons
   - Manual, audited processes for any necessary data movement
   - Data Loss Prevention (DLP) policies at all egress points

3. **Access Control**
   - Separate identity provider (Azure AD in GCC High tenant)
   - Personnel require explicit authorization to access enclave
   - MFA required for all enclave access
   - Privileged access management for administrators

4. **Monitoring and Audit**
   - SIEM collecting logs from all enclave systems
   - Real-time alerting on suspicious activity
   - 90-day log retention minimum (contract may require longer)

### 3.4 Personnel and Role Separation

Not all employees need access to the CUI enclave. This reduces licensing costs and simplifies compliance:

| Role Type | Enclave Access | GCC High License | Training Required |
|-----------|----------------|------------------|-------------------|
| Government Project Engineers | Full | Yes (E3/E5) | CMMC Awareness + Role-based |
| Government Project Managers | Full | Yes (E3/E5) | CMMC Awareness |
| Commercial-only Engineers | None | No | Basic Security Awareness |
| IT Administrators | Full (privileged) | Yes (E5) | CMMC + Privileged User |
| Executive Leadership | Limited (read) | Yes (E3) | CMMC Awareness |
| HR/Finance (if handling CUI) | Limited | Yes (E3) | CMMC Awareness |

### 3.5 Handling Cross-Echelon Scenarios

Some scenarios require careful handling when work spans both environments:

**Scenario 1: Engineer works on both government and commercial projects**
- **Solution:** Separate devices or virtual desktop for government work
- Use dedicated government laptop that never connects to commercial systems
- Alternative: Virtual Desktop Infrastructure (VDI) via AWS WorkSpaces in GovCloud

**Scenario 2: Reusing code/IP from commercial project on government contract**
- **Solution:** One-way, audited transfer process
- Code review before transfer to ensure no CUI contamination in reverse direction
- Document the transfer in change management system

**Scenario 3: Training ML models that might be used in both contexts**
- **Solution:** Train in commercial environment with synthetic/public data
- Transfer only the trained model (not training data) to government enclave
- Re-validate model in enclave before use with CUI

**Scenario 4: Collaboration with subcontractors**
- **Solution:** Subcontractors accessing CUI must be CMMC certified themselves
- Establish secure collaboration channels (GCC High Teams, encrypted file sharing)
- Flow down DFARS 252.204-7012 requirements contractually

### 3.6 Implementation Approach

**Phase 1: Foundation (Months 1-2)**
- Procure GCC High tenant and licenses for identified personnel
- Establish AWS GovCloud account
- Deploy initial network segmentation

**Phase 2: Build (Months 3-4)**
- Configure GCC High services (Exchange, SharePoint, Teams)
- Deploy compliant endpoints to government team
- Implement identity and access management

**Phase 3: Secure (Months 5-6)**
- Deploy EDR/XDR on all enclave endpoints
- Configure SIEM and logging
- Implement DLP policies

**Phase 4: Validate (Months 7-8)**
- Conduct internal gap assessment
- Remediate findings
- Prepare documentation for C3PAO assessment

---

## 4. Cloud Infrastructure Strategy

### 4.1 Cloud Provider Selection: AWS GovCloud

For Furientis's government echelon, **AWS GovCloud (US)** is the recommended primary cloud infrastructure provider for the following reasons:

| Factor | AWS GovCloud Advantage |
|--------|------------------------|
| **FedRAMP Authorization** | FedRAMP High baseline - highest level for unclassified workloads |
| **AI/ML Capabilities** | Amazon Bedrock available with Claude, Llama, and other models |
| **GPU Compute** | Full range of NVIDIA GPU instances (P4d, P5, G5) for ML workloads |
| **Data Residency** | All data remains in US, operated by US persons on US soil |
| **ITAR/EAR Support** | Designed for export-controlled data handling |
| **Ecosystem** | Extensive service portfolio matches commercial AWS |

### 4.2 AWS GovCloud Services for Furientis

**Compute Resources:**

| Service | Use Case | Instance Types |
|---------|----------|----------------|
| EC2 | General compute, application hosting | m5, c5, r5 families |
| EC2 (GPU) | ML training, inference | p4d.24xlarge, g5.xlarge-48xlarge |
| EKS | Container orchestration | Managed Kubernetes |
| Lambda | Serverless functions | N/A |
| AWS WorkSpaces | Virtual desktops for remote access | Various bundles |

**AI/ML Services:**

| Service | Availability in GovCloud | Notes |
|---------|--------------------------|-------|
| Amazon Bedrock | Available | Claude 3.5 Sonnet, Llama 3 models available |
| Amazon SageMaker | Full availability | Model training, hosting, MLOps |
| SageMaker JumpStart | Available | Pre-trained open-weight models |
| AWS Trainium | Coming 2026 | Custom AI accelerator chips |

**Storage Services:**

| Service | Use Case | Encryption |
|---------|----------|------------|
| S3 | Object storage, data lakes | SSE-S3, SSE-KMS (FIPS 140-2) |
| EBS | Block storage for EC2 | AES-256 encryption at rest |
| EFS | Shared file systems | Encryption in transit and at rest |
| FSx for Windows | Windows file shares | Integrates with AD |

**Key AWS GovCloud Capabilities for CMMC:**

1. **Amazon Bedrock in GovCloud** - Enables generative AI workloads with CUI:
   - Anthropic Claude 3.5 Sonnet for advanced reasoning
   - Meta Llama 3 for open-weight model deployment
   - Guardrails for responsible AI implementation
   - Data never leaves the GovCloud boundary

2. **GPU Compute for ML Training:**
   - P4d instances with NVIDIA A100 GPUs for large model training
   - G5 instances with NVIDIA A10G for inference and smaller training jobs
   - Spot instances available for cost optimization on interruptible workloads

3. **Data Lake Architecture:**
   ```
   ┌─────────────────────────────────────────────────────────────────┐
   │                    AWS GovCloud Data Lake                       │
   ├─────────────────────────────────────────────────────────────────┤
   │                                                                 │
   │  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐  │
   │  │ S3 Raw Zone │───▶│S3 Processed │───▶│ S3 Curated/Analytics│  │
   │  │ (Ingestion) │    │   Zone      │    │        Zone         │  │
   │  └─────────────┘    └─────────────┘    └─────────────────────┘  │
   │         │                  │                      │             │
   │         ▼                  ▼                      ▼             │
   │  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐  │
   │  │   Glue      │    │   Athena    │    │    QuickSight       │  │
   │  │  Catalog    │    │   Query     │    │   Visualization     │  │
   │  └─────────────┘    └─────────────┘    └─────────────────────┘  │
   │                                                                 │
   │  All buckets: SSE-KMS encryption, versioning, access logging   │
   └─────────────────────────────────────────────────────────────────┘
   ```

### 4.3 Azure Government Alternative

While AWS GovCloud is recommended, **Azure Government** is a viable alternative, particularly if Furientis prioritizes Microsoft ecosystem integration:

| Capability | AWS GovCloud | Azure Government |
|------------|--------------|------------------|
| FedRAMP Level | High | High |
| M365 Integration | Separate systems | Native with GCC High |
| AI Services | Bedrock, SageMaker | Azure OpenAI (limited models) |
| GPU Options | P4d, P5, G5 | NC, ND series |
| Pricing | Generally lower | Competitive |
| CMMC Tools | Config rules, Security Hub | Azure Policy, Defender |

**Recommendation:** Use AWS GovCloud for compute/AI workloads and Microsoft GCC High for productivity suite. This hybrid approach leverages strengths of both platforms.

### 4.4 FedRAMP and Compliance Inheritance

Understanding FedRAMP authorization levels is critical for CMMC compliance:

| FedRAMP Baseline | Impact Level | Suitable For |
|------------------|--------------|--------------|
| Low | Low | Public, non-sensitive data |
| Moderate | Moderate | Most CUI categories |
| High | High | Most sensitive CUI, law enforcement, emergency services |

**For CMMC Level 2:** Cloud providers must meet FedRAMP Moderate baseline at minimum. For export-controlled CUI (ITAR/EAR), FedRAMP High is required.

**Compliance Inheritance Benefits:**
- AWS GovCloud provides ~60% of NIST 800-171 controls as inherited
- Reduces Furientis's direct implementation burden
- Documented in AWS's Customer Responsibility Matrix
- Must still implement customer-responsible controls (access management, data classification, etc.)

### 4.5 Network Architecture in GovCloud

```
┌────────────────────────────────────────────────────────────────────────────┐
│                        AWS GovCloud VPC Architecture                        │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                          VPC (10.0.0.0/16)                           │  │
│  │                                                                      │  │
│  │  ┌────────────────────┐  ┌────────────────────┐  ┌────────────────┐  │  │
│  │  │  Public Subnet     │  │  Private Subnet    │  │ Data Subnet    │  │  │
│  │  │  10.0.1.0/24       │  │  10.0.2.0/24       │  │ 10.0.3.0/24    │  │  │
│  │  │                    │  │                    │  │                │  │  │
│  │  │  • ALB             │  │  • EC2 Compute     │  │ • RDS          │  │  │
│  │  │  • NAT Gateway     │  │  • EKS Nodes       │  │ • ElastiCache  │  │  │
│  │  │  • Bastion Host    │  │  • Lambda          │  │ • S3 Endpoint  │  │  │
│  │  └────────────────────┘  └────────────────────┘  └────────────────┘  │  │
│  │                                                                      │  │
│  │  Security Groups: Least-privilege, deny-by-default                   │  │
│  │  NACLs: Additional network-level filtering                           │  │
│  │  VPC Flow Logs: All traffic logged to S3 for audit                   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
│  ┌───────────────────┐     ┌───────────────────┐                          │
│  │  AWS Direct       │     │  Site-to-Site VPN │                          │
│  │  Connect          │ OR  │  (IPsec)          │                          │
│  │  (Dedicated)      │     │  (Encrypted)      │                          │
│  └─────────┬─────────┘     └─────────┬─────────┘                          │
│            │                         │                                     │
│            └─────────────┬───────────┘                                     │
│                          ▼                                                 │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                    Furientis On-Premises / CUI Enclave                │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────┘
```

### 4.6 AI/ML Workload Architecture

For Furientis's AI/ML work involving CUI:

**Model Development Workflow:**

1. **Data Ingestion** - CUI data lands in encrypted S3 bucket
2. **Data Preparation** - SageMaker Processing jobs clean and transform data
3. **Model Training** - SageMaker Training on GPU instances (P4d/G5)
4. **Model Evaluation** - Automated testing in SageMaker Pipelines
5. **Model Deployment** - SageMaker Endpoints or Bedrock custom models
6. **Inference** - API calls from applications within GovCloud

**Using Amazon Bedrock with CUI:**

```python
# Example: Using Claude in GovCloud for CUI analysis
import boto3

bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-gov-west-1'  # GovCloud region
)

response = bedrock.invoke_model(
    modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
    body=json.dumps({
        "messages": [{"role": "user", "content": cui_document_text}],
        "max_tokens": 4096
    })
)
# All data remains within GovCloud boundary
```

### 4.7 Cost Optimization Strategies

AWS GovCloud pricing is typically 20-40% higher than commercial regions. Strategies to manage costs:

| Strategy | Potential Savings | Implementation |
|----------|-------------------|----------------|
| Reserved Instances | 30-60% | Commit to 1-3 year terms for steady-state workloads |
| Spot Instances | Up to 90% | Use for ML training that can handle interruption |
| Right-sizing | 20-40% | Regular review of instance utilization |
| S3 Lifecycle Policies | 50%+ on storage | Move cold data to Glacier |
| Scheduled Scaling | Variable | Scale down dev/test environments off-hours |

---

