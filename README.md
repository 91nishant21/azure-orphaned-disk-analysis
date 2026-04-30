Azure Orphaned Disk FinOps Optimization with AI Insights
Overview

This project is an end-to-end FinOps optimization solution designed to identify, analyze, and reduce cloud storage waste caused by orphaned Azure managed disks.

It combines:

Azure data extraction (PowerShell)
Data processing (Python)
Cost analytics (Pandas)
Visualization (Power BI)
AI-driven insights (Streamlit-based assistant)
Problem Statement

Orphaned disks (unattached Azure managed disks) continue to incur costs even when not in use.

This project helps:

Identify unused disks
Estimate cost savings
Prioritize cleanup
Provide actionable insights via dashboard and AI assistant
Project Architecture
Azure → PowerShell → Python Processing → CSV Outputs → Power BI / AI Layer → Insights
Execution Flow
1. Disk Discovery
src/discovery/orphaned_disk_discovery.ps1
Connects to Azure
Extracts disk metadata
Identifies unattached disks
2. Data Processing & Enrichment
python src/processing/orphaned_disk_enrichment.py
Cleans raw data
Classifies disks (High / Medium / Low severity)
Calculates cost savings
Generates outputs:
samples/
├── orphaned_disk_recommendations.csv
├── orphaned_disk_summary.csv
├── top_cleanup_candidates.csv
3. Query Engine (Core Logic)
src/ai/finops_query_engine.py

Provides structured methods:

Total disks
Monthly savings
Annual savings
Top subscriptions
High severity disks
4. Validation Layer
python -m src.tests.test_engine
Validates correctness of query engine outputs
5. AI Layer
src/ai/finops_llm_helper.py
Converts data into human-readable insights
Generates summaries, recommendations, and email content
6. Reporting Layer
python -m src.reporting.email_helper
Generates stakeholder-ready summaries
7. Interactive AI Assistant (Streamlit)
python -m streamlit run src/app/streamlit_app.py

Features:

Natural language queries
Cost insights
Cleanup recommendations
Executive summaries
Example Queries
Which subscriptions have the highest orphaned disk savings?
Show high severity disks older than 60 days.
What is the total annual savings opportunity?
Which disks should be deleted first?
Generate an executive summary.
Generate a cleanup email.
Power BI Dashboard

Located in:

powerbi/

Includes:

Executive summary KPIs
Savings analysis
Disk classification
Cleanup prioritization
Tech Stack
Azure – Resource data extraction
PowerShell – Disk discovery
Python (Pandas) – Data processing and enrichment
Power BI – Visualization and dashboarding
Streamlit – AI assistant interface
Data & Security
No real client data is included
All datasets are sample/mock data
Designed following secure and compliant practices
Key Features
End-to-end FinOps pipeline
Modular architecture (src-based structure)
AI-powered insights
Business-friendly outputs
Scalable and reusable design
Project Structure
azure-orphaned-disk-finops/
│
├── src/
│   ├── discovery/
│   ├── processing/
│   ├── ai/
│   ├── reporting/
│   ├── app/
│   └── tests/
│
├── samples/
├── powerbi/
├── docs/
├── README.md
Future Enhancements
Azure Advisor integration
Automated cleanup scripts
Scheduling via Airflow or ADF
Real-time monitoring dashboard
Multi-cloud support
Conclusion

This project demonstrates how cloud cost optimization can be automated using a combination of:

engineering best practices
data analytics
AI-driven insights

It serves as a scalable template for enterprise-level FinOps initiatives.