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

