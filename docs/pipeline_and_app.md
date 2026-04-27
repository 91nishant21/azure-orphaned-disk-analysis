#  Pipeline & Application – Azure FinOps Optimization

This document explains the internal working of the pipeline, scripts, AI engine, and Streamlit application used in the project.

---

##  Overview

The solution follows a modular pipeline architecture:

Input Data → Processing → AI Engine → Reporting → Visualization → App

---

#  End-to-End Pipeline Flow

CSV Input → Python Enrichment → AI Query Engine → Reporting → Power BI → Streamlit App

---

#  Project Modules

src/
├── processing/
├── ai/
├── reporting/
├── app/
pipeline/

---

#  1. Data Input Layer

##  Input File

input/orphaned_disks_sample.csv

### Description
- Contains raw disk data
- Used as input for processing layer
- Simulates Azure orphaned disk dataset

---

#  2. Processing Layer (Data Enrichment)

##  Script

src/processing/orphaned_disk_enrichment.py

---

##  Key Functions

- Cleans raw disk data  
- Calculates disk age (in days)  
- Estimates monthly cost savings  
- Classifies disks into:
  - SAFE  
  - REVIEW  
  - EXCLUDE  

---

##  Output Files

Generated in:

samples/

Files:

- orphaned_disk_recommendations.csv  
- orphaned_disk_summary.csv  
- top_cleanup_candidates.csv  

---

##  Logic Highlights

- Age-based classification  
- Cost-based prioritization  
- Severity tagging (High / Medium / Low)  

---

#  3. AI Engine Layer

##  Core Files

src/ai/finops_query_engine.py  
src/ai/finops_llm_helper.py

---

##  Purpose

Provides intelligent querying and insight generation over processed data.

---

##  Capabilities

- Retrieve top subscriptions by savings  
- Identify high severity disks  
- Calculate total monthly & annual savings  
- Generate natural language summaries  

---

##  Example Queries

- "Which subscriptions have highest savings?"  
- "Show high severity disks older than 60 days"  
- "What is total annual savings?"  

---

#  4. Reporting Layer

##  Script

src/reporting/email_helper.py

---

##  Purpose

Generates executive-level summaries and email-ready reports.

---

##  Output

- Summary insights printed in console  
- Email-style recommendation message  

---

#  5. Pipeline Orchestration

##  Script

pipeline/run_local_pipeline.py

---

##  Execution Command

python -m pipeline.run_local_pipeline

---

##  Pipeline Steps

1. Validate project structure  
2. Run enrichment script  
3. Generate reporting summary  
4. Prompt manual Power BI refresh  
5. Launch Streamlit application  

---

##  Key Features

- One-click execution  
- Modular design  
- Local execution (no Azure dependency)  

---

#  6. Streamlit Application

##  Script

src/app/streamlit_app.py

---

##  Access

http://localhost:8501

---

##  Features

- Interactive dashboard  
- AI-powered query interface  
- Displays processed data insights  
- Real-time exploration of savings  

---

##  Functionality

- Connects to processed CSV files  
- Uses AI engine for query responses  
- Displays KPIs and recommendations  

---

#  Data Flow Summary

CSV Input
   ↓
Processing (Enrichment)
   ↓
AI Engine (Insights)
   ↓
Reporting (Email Summary)
   ↓
Power BI Dashboard
   ↓
Streamlit App

---

#  Design Considerations

- Read-only solution (no deletion)  
- No dependency on live Azure environment  
- Safe for demo and enterprise usage  
- Modular and extensible architecture  

---

#  Key Highlights

- End-to-end FinOps pipeline  
- AI-powered insight generation  
- One-click execution  
- Integration of Python + Power BI + Streamlit  

---

#  Conclusion

This project demonstrates how cloud cost optimization can be achieved using:

- Data processing  
- AI-based insights  
- Visualization tools  
- Automated pipelines  
