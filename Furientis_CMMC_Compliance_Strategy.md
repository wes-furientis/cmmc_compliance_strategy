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

## 5. IT Infrastructure Requirements

### 5.1 Endpoint Requirements

All endpoints accessing CUI must meet specific security requirements:

**Hardware Standards:**

| Component | Requirement | Notes |
|-----------|-------------|-------|
| Processor | Modern x86-64 or ARM | TPM 2.0 required for Windows 11 |
| TPM | TPM 2.0 | Required for BitLocker, secure boot |
| Storage | SSD with hardware encryption | Self-encrypting drives preferred |
| Memory | 16GB+ recommended | For security tools overhead |
| Webcam/Mic | Physical covers available | Privacy considerations |

**Recommended Laptop Models:**
- Dell Latitude 5000/7000 series (TAA compliant)
- Lenovo ThinkPad T/X series (TAA compliant)
- HP EliteBook 800 series (TAA compliant)

*Note: TAA (Trade Agreements Act) compliance is required for many government contracts.*

**Endpoint Security Stack:**

| Layer | Solution | Purpose |
|-------|----------|---------|
| OS Hardening | CIS Benchmarks, STIG | Baseline configuration |
| Disk Encryption | BitLocker (FIPS mode) | Data at rest protection |
| EDR/XDR | CrowdStrike Falcon GovCloud, Microsoft Defender for Endpoint | Threat detection and response |
| DLP | Microsoft Purview DLP | Prevent CUI exfiltration |
| VPN | Always-on VPN to enclave | Encrypted tunnel |
| Patch Management | WSUS, Intune, or SCCM | Timely security updates |

### 5.2 Identity and Access Management

**Core IAM Requirements (NIST 800-171):**

| Control | Requirement | Implementation |
|---------|-------------|----------------|
| 3.5.1 | Identify users and devices | Azure AD/Entra ID in GCC High |
| 3.5.2 | Authenticate users/devices | MFA required for all access |
| 3.5.3 | Multi-factor authentication | Microsoft Authenticator, FIDO2 keys |
| 3.5.7 | Password complexity | 14+ characters, complexity rules |
| 3.5.8 | Password reuse prevention | Remember 24 passwords |
| 3.5.10 | Session lock | 15-minute inactivity timeout |

**Recommended IAM Architecture:**

```
┌────────────────────────────────────────────────────────────────────┐
│                    Identity Architecture                            │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              Azure AD (Entra ID) - GCC High Tenant          │   │
│  │                                                             │   │
│  │  • Primary identity provider for CUI enclave                │   │
│  │  • Conditional Access policies                              │   │
│  │  • MFA enforcement                                          │   │
│  │  • Privileged Identity Management (PIM) for admins          │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
│  │  M365 GCC High   │  │  AWS GovCloud    │  │  On-Prem Apps    │  │
│  │  (SSO via SAML)  │  │  (SSO via SAML)  │  │  (SAML/OIDC)     │  │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘  │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

**MFA Options:**
1. **Microsoft Authenticator** - Push notifications, number matching (Recommended)
2. **FIDO2 Security Keys** - YubiKey 5 series, phishing-resistant
3. **Hardware Tokens** - RSA SecurID (legacy, if required)
4. **SMS/Phone** - Not recommended, but available as backup

### 5.3 Shared Storage and File Collaboration

**Primary Recommendation: SharePoint Online (GCC High)**

| Feature | Capability |
|---------|------------|
| Storage | 1TB+ per user, shared team sites |
| Collaboration | Real-time co-authoring in Office apps |
| Security | DLP policies, sensitivity labels, encryption |
| Compliance | eDiscovery, retention policies, audit logs |
| External Sharing | Disabled by default for CUI; enable selectively with controls |

**Alternative: AWS FSx for Windows File Server**
- Traditional SMB file shares in GovCloud
- Integrates with on-premises Active Directory
- Useful for legacy applications requiring mapped drives

**File Sharing Security Controls:**
1. **Sensitivity Labels** - Auto-classify documents containing CUI
2. **DLP Policies** - Block sharing of labeled content externally
3. **Conditional Access** - Require compliant device for access
4. **Audit Logging** - Track all file access and sharing
5. **Encryption** - Files encrypted at rest and in transit

### 5.4 Email and Collaboration

**Microsoft 365 GCC High is Required** for email handling CUI:

| Service | Commercial M365 | GCC | GCC High |
|---------|-----------------|-----|----------|
| DFARS 7012 Compliant | No | Partial | Yes |
| Data Residency | Global | US | US (Azure Gov) |
| Personnel | Global | US persons | US persons + screening |
| FedRAMP | N/A | Moderate | High |
| CMMC L2 Suitable | No | Limited | Yes |

**GCC High Email Configuration:**
- Enable S/MIME or Microsoft Purview Message Encryption for CUI
- Configure transport rules to enforce encryption for external recipients
- Implement email DLP policies
- Enable advanced threat protection (Defender for Office 365)

**Teams for Collaboration:**
- GCC High Teams supports private channels for sensitive discussions
- Meeting recordings stored in compliant SharePoint
- Guest access disabled or tightly controlled
- Chat retention policies aligned with record requirements

### 5.5 Remote Access and VPN

**Always-On VPN Architecture:**

| Solution | Pros | Cons |
|----------|------|------|
| Windows Always On VPN | Native, integrates with Intune | Windows only |
| Cisco AnyConnect | Mature, cross-platform | Additional licensing |
| Palo Alto GlobalProtect | Integrates with NGFW | Vendor lock-in |
| Zscaler Private Access | Zero trust, cloud-native | Subscription cost |

**Recommendation for Furientis:** Start with Windows Always On VPN for Windows endpoints; evaluate Zscaler for zero-trust architecture as organization scales.

**Remote Access Security Controls:**
1. **Device Compliance** - Only compliant, managed devices can connect
2. **MFA** - Required for all VPN connections
3. **Split Tunneling** - Disabled for CUI access; all traffic through VPN
4. **Geo-restrictions** - Block connections from high-risk countries
5. **Session Limits** - Maximum session duration, re-authentication required

### 5.6 SIEM and Security Monitoring

**CMMC Level 2 Audit Requirements:**
- AU.2.041: Ensure actions can be traced to individual users
- AU.2.042: Create and retain audit logs
- AU.3.045: Review and analyze audit logs
- AU.3.046: Alert on audit process failures

**SIEM Options Comparison:**

| Solution | Deployment | Cost Model | Strengths |
|----------|------------|------------|-----------|
| Microsoft Sentinel | Cloud (GCC High) | Per-GB ingested | Native M365 integration |
| Splunk Cloud (GovCloud) | Cloud | Per-GB indexed | Powerful analytics |
| Elastic SIEM | Self-hosted | Per-node | Open source flexibility |
| LogRhythm | On-prem/Cloud | Per-device | SOAR included |

**Recommendation:** Microsoft Sentinel in GCC High tenant for seamless integration with M365 and Azure security tools.

**Required Log Sources:**
- Azure AD sign-in and audit logs
- M365 audit logs (Exchange, SharePoint, Teams)
- Endpoint logs (Defender for Endpoint)
- AWS CloudTrail (GovCloud)
- VPN authentication logs
- Firewall/NGFW logs

### 5.7 Endpoint Detection and Response (EDR)

**EDR is Required** for CMMC Level 2 (SI.2.216, SI.2.217):

| Solution | FedRAMP Status | Integration | Key Features |
|----------|----------------|-------------|--------------|
| Microsoft Defender for Endpoint | P1/P2 in GCC High | Native M365 | Included with E5 |
| CrowdStrike Falcon GovCloud | FedRAMP High | API-based | Industry-leading detection |
| SentinelOne Singularity | FedRAMP Moderate | API-based | AI-driven response |
| Carbon Black Cloud | FedRAMP Moderate | API-based | VMware ecosystem |

**Recommendation for Furientis:**
- **Budget-conscious:** Microsoft Defender for Endpoint (included with M365 E5)
- **Best-in-class:** CrowdStrike Falcon GovCloud

### 5.8 Mobile Device Management

If mobile devices access CUI (generally discouraged):

| Requirement | Implementation |
|-------------|----------------|
| Device Enrollment | Microsoft Intune (GCC High) |
| Encryption | Device-level encryption required |
| Remote Wipe | Capability required |
| App Protection | MAM policies for M365 apps |
| Jailbreak Detection | Block jailbroken/rooted devices |

**Best Practice:** Minimize mobile access to CUI. Use virtual desktop (WorkSpaces) from mobile when necessary.

---

## 6. Software Requirements and Approved Versions

### 6.1 Microsoft 365 Licensing

**GCC High License Tiers:**

| License | Key Features | Per User/Month (Est.) |
|---------|--------------|----------------------|
| M365 E3 | Core productivity, basic security | $35-40 |
| M365 E5 | Advanced security, Defender, eDiscovery | $55-60 |
| E5 Security Add-on | Add E5 security to E3 base | $15-20 |

**Minimum Recommendation:** M365 E3 for all CUI users + E5 Security add-on

**Required M365 Components:**
- Exchange Online (Plan 2)
- SharePoint Online (Plan 2)
- Teams
- OneDrive for Business
- Azure AD Premium P1 (P2 for PIM)
- Microsoft Defender for Endpoint P1

### 6.2 Operating System Requirements

**Supported Operating Systems for CUI Enclave:**

| OS | Version | Notes |
|----|---------|-------|
| Windows 11 Enterprise | 23H2+ | Recommended; required for new hardware |
| Windows 10 Enterprise | 22H2 | Supported until Oct 2025 |
| Windows Server | 2019/2022 | For server workloads |
| macOS | Monterey (12) or later | With Intune enrollment |
| Linux | RHEL 8/9, Ubuntu 22.04 LTS | For development; requires additional controls |

**Windows Hardening:**
- Apply DISA STIG or CIS Benchmarks
- Enable Credential Guard
- Configure Windows Defender Application Control (WDAC)
- BitLocker with TPM + PIN
- Disable SMBv1, enable SMB signing

### 6.3 Development Tools

**Approved Development Tools:**

| Category | Tool | Compliance Notes |
|----------|------|------------------|
| IDE | VS Code, Visual Studio, JetBrains IDEs | Disable telemetry, no cloud sync for CUI projects |
| Source Control | GitHub Enterprise Server (self-hosted) | In GovCloud; or Azure DevOps Server |
| CI/CD | GitHub Actions (self-hosted runners), Jenkins | Runners in GovCloud |
| Containers | Docker, Podman | Images scanned before deployment |
| Kubernetes | EKS in GovCloud, OpenShift | Managed K8s in compliant environment |

**Git/Source Control Best Practices:**
1. **No GitHub.com for CUI code** - Use self-hosted GitHub Enterprise or Azure DevOps
2. **Pre-commit hooks** - Scan for secrets, CUI markers
3. **Branch protection** - Require code review, signed commits
4. **Audit logs** - Track all repository access

### 6.4 Browser Requirements

| Browser | Approved for CUI | Notes |
|---------|------------------|-------|
| Microsoft Edge | Yes | Recommended; Intune managed |
| Google Chrome | Yes | Enterprise managed |
| Firefox ESR | Yes | Enterprise managed |
| Safari | Conditional | macOS only, limited management |

**Browser Hardening:**
- Managed via Intune or Group Policy
- Disable password sync to personal accounts
- Configure site isolation
- Enable SmartScreen/Safe Browsing
- Block known-bad extensions

### 6.5 Video Conferencing

| Solution | CUI Suitable | Notes |
|----------|--------------|-------|
| Microsoft Teams (GCC High) | Yes | Recommended |
| Zoom Gov | Yes | FedRAMP authorized |
| Webex FedRAMP | Yes | FedRAMP authorized |
| Google Meet | No | Not authorized for CUI |
| Standard Zoom/Teams | No | Commercial versions not suitable |

**Teams Meeting Security:**
- Enable lobby for external participants
- Disable anonymous join
- Watermark shared content
- Meeting recording only to compliant storage

### 6.6 Other Business Software

| Category | Approved Options |
|----------|------------------|
| Password Manager | Keeper Enterprise (FedRAMP), 1Password Business |
| Note-taking | OneNote (GCC High), SharePoint |
| Project Management | Microsoft Planner, Azure DevOps Boards |
| Documentation | SharePoint, Confluence Data Center (self-hosted) |
| Diagramming | Visio (GCC High), draw.io (self-hosted) |
| PDF | Adobe Acrobat DC (managed) |

---

