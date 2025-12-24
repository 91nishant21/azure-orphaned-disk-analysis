# azure-orphaned-disk-analysis
Analysis and automation framework to identify, validate & amp; optimize orphaned (unattached) azure managed disks for cost savings

---

## Problem Statement
In Azure environments, managed disks can remain **unattached** after VM deletion, migration, resize, or failed deployments. These orphaned disks continue to incur storage charges and may also increase operational risk if not governed properly.

---

## Goals
- Detect unattached/orphaned managed disks across subscriptions/resource groups
- Validate whether a disk is truly unused (avoid accidental deletion)
- Provide a safe, repeatable cleanup workflow
- Estimate potential cost savings from cleanup

---

## Approach (High Level)
This repository follows a **3-step decision flow**:

1. **Discover**
   - List all managed disks where `managedBy = null` (unattached)
2. **Validate**
   - Check disk age, tags, last known usage signals, and ownership
   - Apply exclusions (e.g., disks retained intentionally, DR/test, golden images)
3. **Act**
   - Recommend: delete / snapshot+delete / keep with proper tagging
   - Capture audit trail for governance

---

## Repository Structure
- `docs/` – Framework, decision matrix, and validation checklist  
- `scripts/` – Sample scripts (Azure CLI / PowerShell) for discovery and reporting  
- `templates/` – Tagging, reporting, and evidence templates  

---

## Safety & Governance Notes
Before deleting any disk:
- Confirm with application/VM owners
- Prefer **snapshot + retention** for critical workloads
- Use tags to mark ownership and retention intent
- Maintain an audit log of actions taken

---

## Disclaimer
This repository contains **generic examples only**.  
No client data, confidential identifiers, or environment-specific details are included.
