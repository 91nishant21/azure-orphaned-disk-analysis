#  Azure FinOps Optimization – Solution Architecture

This document describes the **end-to-end architecture** of the Azure Orphaned Disk Optimization solution, including data flow, components, and integration with AI-powered insights.

---

##  Objective

The goal of this solution is to:

- Identify **orphaned Azure managed disks**
- Estimate **cost savings opportunities**
- Classify disks based on **risk and severity**
- Provide **actionable insights via Power BI**
- Enable **natural language querying using AI (Streamlit app)**

---

##  High-Level Architecture

###  Flow Overview

Azure Environment  
↓  
Disk Discovery Script (Python)  
↓  
Data Enrichment Layer  
↓  
CSV Outputs (Data Layer)  
↓  
Power BI Dashboard  
↓  
AI Layer (Streamlit + LLM)  
↓  
User Insights & Decision Making  

---

##  Architecture Components

### Azure Data Source Layer

- Managed Disks
- VM associations
- Metadata (Size, SKU, Region, Creation Date)

---

### Data Processing Layer (Python)

**Script Location:**
processing/orphaned_disk_enrichment.py

**Responsibilities:**
- Fetch disk inventory
- Detect orphaned disks
- Calculate disk age
- Estimate cost savings
- Classify severity

**Outputs:**
- samples/orphaned_disk_recommendations.csv
- samples/orphaned_disk_summary.csv
- samples/top_cleanup_candidates.csv

---

### Data Storage Layer

- CSV-based lightweight storage
- Used by Power BI and AI engine
- Portable and simple design

---

### Visualization Layer – Power BI

**Data Source:**
/samples folder

**Dashboard Pages:**
- Project Summary
- Executive Summary
- Cleanup Candidates

**Insights:**
- Total orphaned disks
- Monthly & annual savings
- Disk classification
- Subscription breakdown

---

### AI Insight Layer (Streamlit + LLM)

**Components:**
- finops_query_engine.py
- finops_llm_helper.py
- streamlit_app.py

**Capabilities:**
- Natural language queries
- Dynamic insights generation

**Example Queries:**
- Which subscriptions have highest savings?
- Show high severity disks older than 60 days
- What is total annual savings opportunity?

---

##  Integration Flow

Python Script → CSV → Power BI  
                      ↓  
                Streamlit App  
                      ↓  
                 LLM Engine  
                      ↓  
              Natural Language Insights  

---

##  Deployment Options

| Component       | Option 1          | Option 2             |
|-----------------|-------------------|----------------------|
| Python Script   | Local Run         | Azure Automation     |
| Data Storage    | CSV               | Blob Storage         |
| Power BI        | Desktop           | Power BI Service     |
| Streamlit       | Local             | Azure Web App        |

---

##  Security & Governance

- Read-only access to Azure resources
- No direct deletion
- Recommendation-based system
- Extendable with RBAC & audit logging

---

##  Future Enhancements

- Replace CSV with database (SQL / Snowflake)
- Automate pipeline execution
- Integrate approval workflows
- Add real-time monitoring dashboards
