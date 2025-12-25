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

## 7. Operational TTPs for Engineer Productivity

### 7.1 Development Workflow Best Practices Within CUI Boundaries

The key to maintaining productivity is proper scoping. By creating a well-segmented CUI enclave, Furientis can significantly reduce in-scope assets—securing 20 workstations instead of 200, training 15 people instead of the entire workforce.

**Practical Implementation:**

1. **Segment Early, Segment Often**
   - Use network segmentation and access controls to create isolated environments for CUI work
   - Organizations with limited CUI benefit most from this approach
   - Keep compliance footprint small rather than spreading requirements across entire infrastructure

2. **Define Clear Data Flows**
   - SSP must map where CUI lives in systems and networks
   - Create CUI data flow diagram and asset inventory as foundational steps
   - Every asset in network diagram must correspond to entries in asset inventory

3. **Implement Zones of Trust**
   - Use VLANs, firewalls, and network separation tools
   - Logical separation using VLANs and firewall rules is more practical than complete physical separation

**Automation for Efficiency:**

Event-driven automation executes immediate responses to changes that would normally require manual input, all with documented evidence. Automating key compliance controls:
- Takes needless work off IT's shoulders
- Gives developers compliant resources faster
- Reduces pressure during assessments
- Handles repetitive tasks like configuration, testing, evidence collection, and reporting

### 7.2 Code Repository Management

**GitLab Dedicated for Government:**
- Achieved FedRAMP Moderate Authorization
- Satisfies DoD's FedRAMP equivalency requirements for handling CUI
- Reduces compliance costs through inherited security controls

**Key compliance features:**
- **RBAC:** Limit access to authorized users, implement separation of duties
- **SSO Integration:** SAML SSO for groups and instances
- **Immutable Audit Events:** Actions associated with individual users, immutable
- **Data Encryption:** Secure data in transit, IP address restrictions available

**GitHub Compliance Status (Important):**
- As of 2025, GitHub is **not compliant** for storing CUI in either cloud or self-hosted versions
- Main issue: Lack of FIPS 140-2 encryption support
- GitHub is actively pursuing FedRAMP authorization
- Until complete, contractors should avoid storing CUI on GitHub

**Recommended Approach:**
1. Use GitLab Dedicated for Government for CUI-related code
2. Self-hosted GitHub Enterprise Server in GovCloud (with additional controls)
3. Azure DevOps Server for Microsoft-centric environments

### 7.3 CI/CD Pipelines in Compliant Environments

**Policy-Driven Component Governance:**
- Block known-vulnerable or unapproved packages at consumption point
- Prevent license issues from reaching production
- Demonstrates proactive compliance with system integrity expectations under NIST 800-171

**Automated Evidence Collection:**
- CI/CD scan results captured centrally
- Policy blocks logged with ties to builds and personnel
- Creates verifiable evidence as side effect of normal work

**Cloud Service Requirements:**
- DFARS 252.204-7012 requires cloud providers meet FedRAMP Moderate baseline equivalency
- All CI/CD runners processing CUI must be in compliant environment
- Self-hosted runners in GovCloud for CUI pipelines

### 7.4 Remote Work Considerations

A CMMC-compliant program can include remote work with proper safeguards:

**Key Requirements:**

| Control | Requirement | Implementation |
|---------|-------------|----------------|
| AC.L2-3.1.12 | Monitor and control remote access | Encrypted VPN, authorized users/devices only |
| SC.L2-3.13.7 | Prevent split tunneling | Disable split tunneling in VPN settings |
| SC.L2-3.13.12 | Control collaborative computing devices | Indicator lights/notifications when cameras/mics active |

**Best Practices:**
1. **MFA Required** - For all network-based access to CUI
2. **Proper Session Routing** - Route all remote traffic through gateway firewall
3. **FIPS-Validated Encryption** - Required for any CUI crossing cloud connections
4. **MSSP Partnership** - For real-time log analysis and monitoring

**Important:** DoD contracts may levy more stringent requirements, including prohibiting remote work with CUI. Monitor contract wording closely.

### 7.5 Collaboration with External Partners

**Subcontractor Flow-down:**
- If CUI is passed to subcontractors, they must meet same CMMC level
- Compliance level depends on how CUI flows through supply chain
- If subcontractor only handles FCI, Level 1 may suffice

**External MSP/MSSP Partnerships:**
- Partner with qualified CMMC consultant or C3PAO
- Conduct gap analyses to evaluate current controls
- Most small businesses underestimate what's needed to sustain compliant operations

### 7.6 Managing the Boundary Between CUI and Non-CUI Work

Proper classification and boundary management is critical—most audit failures happen because scope was wrong.

**CUI Classification Guidelines:**
- Classifying CUI defines scope of assessment
- For each classification, the applicable CMMC requirements vary
- Determining factor: how the asset interacts with sensitive data

**Common Scoping Pitfalls to Avoid:**

| Pitfall | Impact | Mitigation |
|---------|--------|------------|
| Over-scoping | Unnecessary complexity and cost | Only include systems that actually process/store CUI |
| Under-scoping | Non-compliance findings | Thorough CUI flow analysis |
| Missing data flows | Compliance gaps | Document all CUI movement |
| Third-party services | Surprise assessment scope | Verify cloud provider FedRAMP status |

### 7.7 Training Programs That Don't Burden Productivity

CMMC Level 2 requires security awareness, insider threat, and role-based training for all employees with CUI access.

**Efficient Implementation:**

1. **Conduct Training Needs Assessment** - Gap analysis based on roles
2. **Select Appropriate Platforms** - KnowBe4, Proofpoint, SANS, or free DoD resources
3. **Leverage Technology** - LMS platforms, phishing simulations, compliance tracking
4. **Develop Role-Specific Plans** - Content and frequency based on duties

**Training Topics:**
- Insider threats
- Phishing awareness
- Password hygiene
- Incident reporting

**Cost:** Approximately $2-5 per person per month

**Documentation Requirements:** Keep records of training dates, topics, participants, evaluations, and results.

### 7.8 Common Friction Points and Mitigation

| Friction Point | Impact | Mitigation |
|---------------|--------|------------|
| Cultural Resistance | Talent loss, poor adoption | Involve engineers in design decisions, explain "why" |
| "Paper-Only" Policies | Assessment failures | Ensure SSP reflects actual implementation |
| Network Diagram Issues | Assessor findings | Living documentation, regular updates |
| Staff Burnout | Rushed work, errors | Plan 12-18 months, phased approach |
| Manual Evidence Collection | Slow, error-prone | Automate evidence capture in CI/CD |

---

## 8. Vendor Comparison

### 8.1 Managed Service Providers (MSPs) Specializing in CMMC

| Provider | Specialization | Key Strengths | Target Market |
|----------|----------------|---------------|---------------|
| **Summit 7** | CMMC, Azure, GCC High | 1,200+ clients in MS Gov Cloud, Azure Expert MSP | DoD contractors, SMBs |
| **Coalfire** | CMMC, FedRAMP, FISMA | Certified C3PAO and RPO, FedRAMP leader | Mid-large enterprises |
| **Pivot Point Security** | CMMC, GCC migration | Hybrid GCC/GCC High strategies, SMB focus | Small-mid contractors |
| **Mirai Security** | CMMC implementation | Implementation support, ongoing MSSP | SMB contractors |
| **Ariento** | CMMC managed security | Authorized C3PAO, full lifecycle support | Defense contractors |

**Recommendations:**
- **Best for Microsoft environments:** Summit 7
- **Best for complex/enterprise:** Coalfire
- **Best for small contractors:** Pivot Point Security, Mirai Security

### 8.2 GCC High Migration Partners

| Partner | Capabilities | Key Features |
|---------|--------------|--------------|
| **Agile IT** | One of first 6 AOS-G partners | Fixed pricing, Azure Government expertise |
| **Dox** | AOS-G partner, no 500-license minimum | Small business access |
| **ECF Data** | Microsoft-approved AOS-G | 14+ years experience, full transition support |
| **R3** | AvePoint migration platform | Exchange, Teams, SharePoint, OneDrive |
| **Nimbus Logic** | AOS-G partner, license reseller | 12/24/36-month terms |

**Important Notes:**
- Only 9 AOS-G partners authorized for GCC High
- Must purchase through AOS-G partner for ≤500 users
- Typical migration cost: $10,000-50,000

### 8.3 SIEM Solutions Comparison

| Solution | Deployment | Pricing Model | Best For |
|----------|------------|---------------|----------|
| **Microsoft Sentinel** | Cloud (GCC High) | Pay-per-GB | Microsoft environments |
| **Splunk Enterprise Security** | On-prem/cloud | ~$150/GB/day | Maximum customization |
| **Elastic SIEM** | Self-hosted/cloud | Open-source/hosted | Budget-conscious |
| **IBM QRadar** | On-prem/cloud | License-based | Regulated industries |

**Recommendation for Furientis:** Microsoft Sentinel - native integration with M365, free ingestion for M365/Entra ID logs

### 8.4 EDR Solutions Comparison

| Solution | Annual Cost (per endpoint) | Strengths |
|----------|---------------------------|-----------|
| **CrowdStrike Falcon Go** | $60 | Industry leader, lightweight |
| **CrowdStrike Falcon Pro** | $100 | + Firewall management |
| **SentinelOne Control** | $80 | AI/ML autonomous response |
| **Microsoft Defender P1** | Included in E5 | Native M365 integration |

**Recommendation:**
- **Budget-conscious:** Microsoft Defender (if E5 licensed)
- **Best-in-class:** CrowdStrike Falcon Pro

### 8.5 Compliance Management Platforms

| Platform | Frameworks | Annual Cost | Key Features |
|----------|------------|-------------|--------------|
| **Drata** | CMMC, SOC 2, ISO 27001 | $18,000-24,000 | 350+ integrations, 24×5 support |
| **Sprinto** | CMMC, SOC 2, ISO 27001 | $15,000-30,000 | Multi-framework efficiency |
| **Secureframe** | CMMC, SOC 2, FedRAMP | $25,000+ | 80+ native connectors |
| **Vanta** | CMMC, SOC 2, HIPAA | $20,000-35,000 | Continuous monitoring |

**Recommendation for Furientis:** Drata or Sprinto for SMB value and automation

---

## 9. Cost Estimates

### 9.1 First-Year Cost Summary

| Category | Low | Mid | High |
|----------|-----|-----|------|
| **GCC High Licensing (25 users)** | $6,600 | $10,800 | $21,600 |
| **AWS GovCloud Infrastructure** | $7,200 | $15,000 | $30,000 |
| **C3PAO Assessment** | $40,000 | $55,000 | $75,000 |
| **MSSP Services** | $40,000 | $55,000 | $75,000 |
| **EDR/Endpoint Protection** | $2,000 | $5,000 | $9,000 |
| **SIEM Solution** | $8,000 | $15,000 | $25,000 |
| **Training** | $10,000 | $18,000 | $30,000 |
| **Consulting/Gap Assessment** | $30,000 | $50,000 | $80,000 |
| **Additional Tools** | $20,000 | $35,000 | $60,000 |
| **Hardware/One-time Upgrades** | $15,000 | $35,000 | $85,000 |
| **TOTAL FIRST YEAR** | **$178,800** | **$293,800** | **$490,600** |

### 9.2 Ongoing Annual Costs (Years 2-3)

| Category | Low | Mid | High |
|----------|-----|-----|------|
| **GCC High Licensing** | $6,600 | $10,800 | $21,600 |
| **AWS GovCloud** | $7,200 | $15,000 | $30,000 |
| **Annual Affirmation** | $1,459 | $1,459 | $1,459 |
| **MSSP Services** | $24,000 | $36,000 | $50,000 |
| **EDR/SIEM/Tools** | $25,000 | $45,000 | $75,000 |
| **Training Refreshers** | $5,000 | $10,000 | $15,000 |
| **Compliance Platform** | $18,000 | $24,000 | $30,000 |
| **Continuous Monitoring** | $6,500 | $9,000 | $13,000 |
| **TOTAL ANNUAL** | **$93,759** | **$151,259** | **$235,059** |

### 9.3 Three-Year Total Investment

| Scenario | 3-Year Total | Annual Average |
|----------|--------------|----------------|
| Low (Good Starting Posture) | $366,318 | $122,106 |
| Mid (Typical) | $596,318 | $198,773 |
| High (Significant Remediation) | $960,718 | $320,239 |

### 9.4 Cost Optimization Strategies

| Strategy | Potential Savings | Implementation |
|----------|-------------------|----------------|
| **Hybrid GCC High** | 30-50% on licensing | Only CUI users on GCC High |
| **Right-Size Cloud** | 20-30% on cloud | Reserved instances, auto-scaling |
| **Leverage Microsoft Stack** | $5,000-15,000/year | Use included Defender, Sentinel |
| **Phased Implementation** | Spread costs | 12-18 month timeline |
| **MSSP vs. FTE** | Variable | MSSP more cost-effective <100 employees |

---

## 10. Implementation Roadmap

### 10.1 Phase 1: Assessment & Planning (Months 1-2)

**Objectives:**
- Understand current security posture
- Define CUI scope and boundaries
- Develop remediation roadmap

**Key Activities:**
- [ ] Engage CMMC consultant/RPO for gap assessment
- [ ] Inventory all systems that touch CUI
- [ ] Create CUI data flow diagrams
- [ ] Develop asset inventory
- [ ] Select technology vendors
- [ ] Establish project governance

**Deliverables:**
- Gap assessment report
- Remediation priority list
- Vendor selection decisions
- Project plan and budget

**Budget:** $20,000-35,000

### 10.2 Phase 2: Foundation Build (Months 3-4)

**Objectives:**
- Establish compliant infrastructure
- Begin migration to GCC High
- Deploy core security tools

**Key Activities:**
- [ ] Procure GCC High licenses
- [ ] Establish AWS GovCloud account
- [ ] Migrate email to GCC High Exchange
- [ ] Deploy network segmentation
- [ ] Configure identity management (Azure AD)
- [ ] Implement MFA organization-wide

**Deliverables:**
- GCC High tenant operational
- Network segmentation in place
- Identity management configured

**Budget:** $35,000-60,000

### 10.3 Phase 3: Security Implementation (Months 5-6)

**Objectives:**
- Deploy security monitoring and protection
- Complete GCC High migration
- Begin documentation development

**Key Activities:**
- [ ] Migrate SharePoint, Teams, OneDrive to GCC High
- [ ] Deploy EDR on all endpoints
- [ ] Configure SIEM and log collection
- [ ] Implement DLP policies
- [ ] Deploy endpoint encryption (BitLocker)
- [ ] Begin SSP documentation

**Deliverables:**
- Full GCC High migration complete
- EDR and SIEM operational
- Draft SSP

**Budget:** $40,000-70,000

### 10.4 Phase 4: Control Completion (Months 7-8)

**Objectives:**
- Complete all 110 NIST 800-171 controls
- Finalize documentation
- Conduct employee training

**Key Activities:**
- [ ] Complete remaining technical controls
- [ ] Finalize policies and procedures
- [ ] Complete SSP and POA&M
- [ ] Conduct security awareness training
- [ ] Implement continuous monitoring
- [ ] Deploy compliance management platform

**Deliverables:**
- All 110 controls implemented
- Complete SSP and supporting documentation
- Training records

**Budget:** $30,000-50,000

### 10.5 Phase 5: Validation (Months 9-10)

**Objectives:**
- Internal assessment and remediation
- Prepare for C3PAO assessment

**Key Activities:**
- [ ] Conduct internal mock assessment
- [ ] Remediate any identified gaps
- [ ] Verify all evidence is collected
- [ ] Review documentation for completeness
- [ ] Engage C3PAO and schedule assessment

**Deliverables:**
- Mock assessment report
- Remediation complete
- C3PAO scheduled

**Budget:** $15,000-30,000

### 10.6 Phase 6: Certification (Months 11-12)

**Objectives:**
- Achieve CMMC Level 2 certification

**Key Activities:**
- [ ] C3PAO pre-assessment
- [ ] C3PAO formal assessment
- [ ] Address any findings
- [ ] Receive certification
- [ ] Submit to SPRS

**Deliverables:**
- CMMC Level 2 certification
- SPRS submission complete

**Budget:** $40,000-75,000 (C3PAO assessment)

### 10.7 Ongoing: Maintain Certification

**Annual Requirements:**
- [ ] Submit annual affirmation to SPRS
- [ ] Conduct continuous monitoring
- [ ] Update documentation as environment changes
- [ ] Conduct annual security training
- [ ] Perform regular vulnerability scanning
- [ ] Review and update POA&M

**Triennial Requirements:**
- [ ] Schedule recertification assessment 6 months before expiration
- [ ] Conduct comprehensive review of all controls
- [ ] Update SSP and evidence
- [ ] Complete C3PAO recertification

---

## 11. Risk Assessment and Common Pitfalls

### 11.1 Common CMMC Certification Failures

**Scoping Failures (Primary Cause):**
Most audit failures occur due to scope-related issues:
- Over-scoping: Including systems that don't process CUI
- Under-scoping: Missing necessary systems
- Undefined CUI data flows
- Forgotten third-party services

**Documentation Failures:**
- SSP doesn't match actual implementation
- Incomplete asset inventories
- Missing policies and procedures
- Insufficient evidence
- Outdated documentation

**Pre-Assessment Failures:**
- Scope couldn't be determined
- Lack of preliminary mock assessment
- Unprepared subject matter experts

### 11.2 Scope Creep Issues

| Cause | Impact | Mitigation |
|-------|--------|------------|
| Inadequate segmentation | Entire network becomes in-scope | Strong boundary enforcement |
| Poorly defined CUI boundaries | Systems inadvertently touch CUI | Rigorous data flow documentation |
| Shared infrastructure | Shared components become in-scope | Proper isolation or controlled access |
| Third-party service sprawl | Discovery of more in-scope services | Assess before adding services |

### 11.3 Supply Chain and Subcontractor Risks

**Current State:**
- Only 28.7% of organizations have completed Level 2 assessment
- Fewer than 0.6% (459 organizations) certified as of November 2025
- Creates significant supply chain risk

**Mitigation:**
- Assess subcontractor readiness early
- Include compliance provisions in subcontracts
- Verify cloud provider compliance documentation
- Build redundancy in supply chain
- Monitor subcontractor certification status

### 11.4 Technical Debt from Rushed Implementations

**Forms of Technical Debt:**
- "Quick fix" security controls
- Incomplete integration
- Fragmented systems
- Poorly architected enclaves
- Neglected automation

**Impact:**
- Staff burnout
- Incomplete documentation
- Higher long-term costs (20-30% increase)

**Mitigation:**
- Allow adequate timeline (12-18 months)
- Phased implementation approach
- Build automation from the start
- Schedule technical debt remediation

### 11.5 Cultural Resistance

**Sources of Resistance:**
- Perceived inefficiency
- Lack of context on why controls matter
- Poor implementation creating excessive burden
- Change fatigue
- Insufficient training

**Mitigation:**
1. Lead with "why" - business necessity, protective value
2. Involve engineers early in design decisions
3. Minimize friction through automation
4. Implement gradually
5. Provide adequate training
6. Celebrate milestones

### 11.6 Maintaining Certification Over Time

**Three-Year Certification Cycle:**
- Self-assessments every three years
- Annual affirmations required
- Senior executive must affirm all 320 objectives still met

**Consequences of Lapses:**
- Certification may lapse
- Contracts at risk
- Must remediate before bidding on new contracts

**Best Practices:**
1. Treat documentation as living artifacts
2. Conduct continuous monitoring
3. Schedule recertification 6 months before expiration
4. Track all 320 assessment objectives
5. Budget for ongoing costs ($5,000-30,000 annually)
6. Stay current with requirement changes

---

## 12. Appendices

### Appendix A: NIST 800-171 Control Families Quick Reference

| Family | ID | Control Count | Key Areas |
|--------|-----|---------------|-----------|
| Access Control | AC | 22 | Least privilege, remote access, session controls |
| Awareness & Training | AT | 3 | Security awareness, role-based training |
| Audit & Accountability | AU | 9 | Logging, review, protection |
| Configuration Management | CM | 9 | Baselines, change control |
| Identification & Authentication | IA | 11 | MFA, passwords, device auth |
| Incident Response | IR | 3 | Capability, reporting, testing |
| Maintenance | MA | 6 | Controlled, remote maintenance |
| Media Protection | MP | 9 | Handling, sanitization, transport |
| Personnel Security | PS | 2 | Screening, actions |
| Physical Protection | PE | 6 | Access, visitor control |
| Risk Assessment | RA | 3 | Assessments, vulnerability scanning |
| Security Assessment | CA | 4 | Assessments, POA&M |
| System & Communications | SC | 16 | Boundary, encryption, CUI handling |
| System & Information Integrity | SI | 7 | Flaw remediation, malware, monitoring |

### Appendix B: Key Acronyms

| Acronym | Definition |
|---------|------------|
| C3PAO | CMMC Third-Party Assessment Organization |
| CUI | Controlled Unclassified Information |
| DFARS | Defense Federal Acquisition Regulation Supplement |
| DIB | Defense Industrial Base |
| EDR | Endpoint Detection and Response |
| FCI | Federal Contract Information |
| GCC High | Government Community Cloud High |
| MFA | Multi-Factor Authentication |
| MSSP | Managed Security Service Provider |
| NIST | National Institute of Standards and Technology |
| POA&M | Plan of Action and Milestones |
| RPO | Registered Provider Organization |
| SIEM | Security Information and Event Management |
| SPRS | Supplier Performance Risk System |
| SSP | System Security Plan |

### Appendix C: Key Resources

**Official Sources:**
- [CMMC Program Website](https://dodcio.defense.gov/CMMC/)
- [CyberAB (CMMC Accreditation Body)](https://cyberab.org/)
- [NIST SP 800-171](https://csrc.nist.gov/publications/detail/sp/800-171/rev-2/final)
- [CMMC Assessment Guide Level 2](https://dodcio.defense.gov/Portals/0/Documents/CMMC/AssessmentGuideL2v2.pdf)

**Training Resources:**
- DoD Insider Threat Awareness Course
- CISA Cybersecurity Training
- SANS Security Awareness

---

**Document Version:** 1.0
**Last Updated:** December 2025
**Next Review:** March 2026

---

*This document is intended for internal planning purposes. Consult with qualified CMMC consultants and legal counsel for specific compliance decisions.*
