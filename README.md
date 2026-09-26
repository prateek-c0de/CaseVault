# 🔐 CaseVault

### Cryptographically Secured Digital Evidence Management Platform

> **Built for Smart India Hackathon 2026**

CaseVault is a secure digital evidence management platform designed for law enforcement and judicial workflows.

The platform addresses evidence tampering and broken chain-of-custody issues by combining **SHA-256 cryptographic hashing, remote cloud storage, role-based access control, dual-consent evidence transfers, and immutable hash-chained audit logs**.

---

## 🎯 Project Overview

Digital evidence must remain authentic, traceable, and verifiable throughout its entire lifecycle.

CaseVault provides a centralized platform where authorized officers can:

- Register digital evidence
- Securely store evidence in the cloud
- Generate cryptographic fingerprints
- Verify evidence integrity remotely
- Transfer evidence between authorized officers
- Maintain a cryptographically linked chain of custody
- Track every important system action
- Detect potential evidence tampering

The system is designed around the principle:

> **Store the evidence remotely, verify its integrity cryptographically, and make every custody action traceable.**

---

# 🚀 Core Features

### 🔐 1. Role-Based Access Control

CaseVault provides authenticated access for different roles involved in evidence management.

## Primary Roles

- **Administrator**
- **Investigating Officer**
- **Forensic Analyst**

Access to protected functionality is enforced through authentication middleware and role-based authorization.

---

### ☁️ 2. Cloud Evidence Registry

Evidence files are stored remotely using **Cloudinary** rather than relying solely on the local application server.

## Upload Workflow

    Evidence File
          │
          ▼
    Calculate SHA-256
          │
          ▼
    Upload to Cloudinary
          │
          ▼
    Receive Secure Cloud URL
          │
          ▼
    Store URL + Hash in Database
The database stores the secure cloud URL along with the cryptographic fingerprint of the original file.

### 🔑 3. SHA-256 Integrity Verification
Every uploaded evidence file receives a SHA-256 cryptographic hash.
The hash is calculated in memory before cloud upload

    Evidence File
          │
          ▼
    SHA-256
          │
          ▼
    Original Hash
          │
          ├───────────────┐
          │               │
          ▼               ▼
    Cloud Storage      Database
                        │
                        └── SHA-256 Hash
The original hash becomes the reference fingerprint for future integrity verification.

### 🔍 4. Remote Integrity Verification
CaseVault can verify evidence without relying on a local copy of the file.
When an officer selects Verify:

    Cloudinary URL
          │
          ▼
    Stream File
          │
          ▼
    Calculate SHA-256
          │
          ▼
    Compare With Stored Hash
          │
          ├───────────────┐
          │               │
          ▼               ▼
       MATCH          MISMATCH
          │               │
          ▼               ▼
      VERIFIED      TAMPER_DETECTED
Verification Result
If the calculated hash matches the registered hash:

    Original Hash == Current Hash
    
    ✅ VERIFIED
If even a single byte of the file has changed:

    Original Hash != Current Hash
    
    🚨 TAMPER DETECTED
This provides cryptographic evidence-integrity verification.

### 🔄 5. Cryptographic Chain of Custody
Evidence transfers use a dual-consent workflow.

    Officer A
       │
       │ Initiate Transfer
       ▼
    Pending Transfer
       │
       │ Accept
       ▼
    Officer B
A transfer is not completed until the receiving officer accepts it.
Every transfer generates a CustodyEvent.

## ⛓️ Hash-Chained Custody Events
Each custody event contains the hash of the previous event.

    Event 1
       │
       └── Hash 1
              │
              ▼
    Event 2 + Previous Hash
       │
       └── Hash 2
              │
              ▼
    Event 3 + Previous Hash
       │
       └── Hash 3
Conceptually:

    Current Event Hash =
    SHA-256(Current Event Data + Previous Event Hash)
This creates a cryptographically linked custody history.

### 🧾 6. Immutable Audit Trail
CaseVault records important system activities in an AuditLog.
Examples include:
- Login
- Evidence upload
- Evidence verification
- Evidence transfer
- Custody actions
- Other security-sensitive operations
The audit trail begins with a GENESIS entry and subsequent records are hash-chained.

      GENESIS
         │
         ▼
      Audit Event 1
         │
         ▼
      Audit Event 2
         │
         ▼
      Audit Event 3
         │
         ▼
      Audit Event N
Each event contains:
- Event type
- User
- Event data
- Previous hash
- Current hash
This creates a tamper-evident audit history.

### 🧠 7. Cryptographic Security Model
CaseVault uses multiple layers of integrity protection.

                     CASEVAULT
                         │
            ┌────────────┼────────────┐
            │            │            │
            ▼            ▼            ▼
        Evidence      Custody       Audit
          Hash         Hash          Hash
            │            │            │
            ▼            ▼            ▼
         SHA-256    Hash Chain    Hash Chain
# Evidence Integrity
Protects the integrity of the actual evidence file.
# Custody Integrity
Protects the sequence of evidence transfers.
# Audit Integrity
Protects the history of important system actions.

## 🗃️ Database Architecture
CaseVault uses SQLAlchemy ORM with:
- SQLite for development
- PostgreSQL-ready architecture for production
Core Models
User

      id
      name
      email
      password_hash
      role_id
Case

    id
    case_number
    title
    description
    status
Evidence

    id
    evidence_id
    case_id
    name
    storage_path
    sha256_hash
    status
    collector_id
    current_custodian_id
CustodyEvent

    id
    evidence_id
    sender_id
    receiver_id
    action
    previous_event_hash
    current_event_hash
AuditLog

    id
    event_type
    user_id
    event_data
    previous_hash
    current_hash
## 🏗️ System Architecture
                         ┌──────────────────┐
                         │      User        │
                         └────────┬─────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │ HTML / CSS / JS     │
                       │     Frontend        │
                       └──────────┬──────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │    Flask Backend    │
                       └──────────┬──────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
       ┌─────────────┐    ┌───────────────┐   ┌──────────────┐
       │ SQLAlchemy  │    │  Cloudinary   │   │   Services   │
       │     ORM     │    │ Cloud Storage │   │              │
       └──────┬──────┘    └───────┬───────┘   └──────┬───────┘
              │                   │                  │
              ▼                   ▼                  ├─ Hash
       ┌─────────────┐       Evidence Files          ├─ Audit
       │ SQLite /    │                               ├─ Storage
       │ PostgreSQL  │                               └─ QR
       └─────────────┘

## 🛠️ Technology Stack
Layer                    Technology
Backend	                 Python 3
Web Framework	           Flask
ORM	                     SQLAlchemy
Development Database	   SQLite
Production Database	     PostgreSQL-ready
Cloud Storage	           Cloudinary
Frontend	               HTML5
Styling	                 CSS3
Client-side Logic	       Vanilla JavaScript
Integrity	               SHA-256
Authentication	         Flask authentication middleware
QR Generation	           QR Service
Architecture	           Flask Blueprints + Services


## 📁 Project Structure
    Casevault/
    │
    ├── app/
    │   ├── __init__.py
    │   │
    │   ├── models/
    │   │   ├── user.py
    │   │   ├── case.py
    │   │   ├── evidence.py
    │   │   ├── custody.py
    │   │   └── audit.py
    │   │
    │   ├── routes/
    │   │   ├── evidence.py
    │   │   ├── custody.py
    │   │   └── ...
    │   │
    │   ├── services/
    │   │   ├── storage_service.py
    │   │   ├── hash_service.py
    │   │   ├── audit_service.py
    │   │   └── qr_service.py
    │   │
    │   ├── static/
    │   │   ├── css/
    │   │   ├── js/
    │   │   └── images/
    │   │
    │   └── templates/
    │
    ├── instance/
    │   └── SQLite database
    │
    ├── run.py
    └── README.md

## 🎨 UI / UX
CaseVault uses a custom Light Enterprise design system.
Visual Design
- Clean enterprise interface
- Glassmorphism components
- Responsive layouts
- Custom animations
- Interactive navigation
- Investigation-oriented dashboard

## 🔄 Complete Evidence Lifecycle
              ┌─────────────────┐
              │ Evidence Upload │
              └────────┬────────┘
                       ▼
              ┌─────────────────┐
              │ Calculate Hash  │
              └────────┬────────┘
                       ▼
              ┌─────────────────┐
              │ Cloudinary      │
              │ Upload          │
              └────────┬────────┘
                       ▼
              ┌─────────────────┐
              │ Store URL +     │
              │ SHA-256         │
              └────────┬────────┘
                       ▼
              ┌─────────────────┐
              │ Evidence        │
              │ Registered      │
              └────────┬────────┘
                       ▼
              ┌─────────────────┐
              │ Custody Transfer│
              └────────┬────────┘
                       ▼
              ┌─────────────────┐
              │ Dual Consent    │
              └────────┬────────┘
                       ▼
              ┌─────────────────┐
              │ Hash-Chained    │
              │ Custody Event   │
              └────────┬────────┘
                       ▼
              ┌─────────────────┐
              │ Remote Verify   │
              └────────┬────────┘
                       ▼
              ┌─────────────────┐
              │ VERIFIED /      │
              │ TAMPER DETECTED │
              └─────────────────┘

## 🗄️ Database Configuration
# Development
CaseVault uses SQLite for local development.
# Production
The architecture is prepared for PostgreSQL deployment.
Configure the database through environment variables according to the application's configuration.

## 🔐 Security Considerations
CaseVault is designed around cryptographic integrity and controlled evidence handling.
Key security mechanisms include:
- SHA-256 evidence hashing
- Remote hash verification
- Role-based access control
- Authenticated access
- Dual-consent custody transfers
- Hash-chained custody events
- Hash-chained audit logs
- Cloud-based evidence storage
- Separation of evidence files and database metadata
  
## ⚠️ Important Security Note
CaseVault is a hackathon/academic prototype.
It should not be used with real confidential evidence, personally identifiable information, or sensitive law-enforcement records without appropriate security audits, compliance controls, infrastructure hardening, and authorization.
For demonstrations, use synthetic or non-sensitive evidence.

## 🚀 Future Enhancements
Potential future improvements include:
- PostgreSQL production deployment
- Advanced cloud-storage security
- Stronger fine-grained authorization
- Multi-factor authentication
- Digital signatures
- Encrypted evidence at rest
- Advanced forensic reporting
- Evidence retention policies
- Automated backup and disaster recovery
- Production monitoring and alerting
- Advanced document search
- Additional compliance controls
  
## 🏆 Smart India Hackathon 2026
Project: CaseVault

Event: Smart India Hackathon 2026

Purpose: Secure digital evidence management and cryptographic chain of custody

## 👥 Team
Team Name: Error:404

Built with ❤️ for Smart India Hackathon 2026.

## 📜 Disclaimer
CaseVault is a prototype created for educational and hackathon purposes.
Cryptographic hashing provides file-integrity verification but does not, by itself, establish legal admissibility, authenticity, authorship, or compliance with a particular jurisdiction's evidentiary standards.

## 📄 License
This project is currently intended as a Smart India Hackathon prototype.
Add an appropriate open-source license if you intend to distribute the source code publicly.
