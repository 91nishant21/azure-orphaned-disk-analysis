"""
===========================================================
Project   : Azure FinOps Optimization - Orphaned Disk Cleanup
Module    : AI Insights & Reporting
File      : email_helper.py
Version   : v1.0
Author    : Internal Use
Created   : 2026-04-26
Updated   : 2026-04-26

Description:
-----------------------------------------------------------
Generates AI-powered summaries and email-ready insights 
for orphaned disk cost optimization using FinOps data.

Key Functions:
-----------------------------------------------------------
- Extracts top subscriptions contributing to savings
- Identifies high severity orphaned disks (age-based)
- Calculates total monthly and annual savings
- Generates executive summary for stakeholders
- Prepares cleanup recommendation email content

Inputs:
-----------------------------------------------------------
- Data Source: samples/ (processed orphaned disk datasets)
- Parameters : Disk age threshold (default: 60 days)

Outputs:
-----------------------------------------------------------
- Console-based insights
- Executive summary text
- Email-ready cleanup recommendation content

Dependencies:
-----------------------------------------------------------
- FinOpsQueryEngine
- FinOpsLLMHelper

Notes:
-----------------------------------------------------------
- Designed for AI sidecar integration and reporting automation
- Can be extended for email service integration (SMTP/Logic Apps)
- No client-specific or sensitive data is used
===========================================================
"""
from src.ai.finops_query_engine import FinOpsQueryEngine
from src.ai.finops_llm_helper import FinOpsLLMHelper

engine = FinOpsQueryEngine()
helper = FinOpsLLMHelper()

top_subs = engine.get_top_subscriptions_by_savings()
high_severity = engine.get_high_severity_old_disks(60)
top_candidates = engine.get_top_cleanup_candidates()

print(helper.generate_top_subscriptions_answer(top_subs))
print()
print(helper.generate_high_severity_answer(high_severity, 60))
print()
print(
    helper.generate_total_savings_answer(
        engine.get_total_monthly_savings(),
        engine.get_total_annual_savings()
    )
)
print()
print(
    helper.generate_executive_summary(
        engine.get_total_disks(),
        engine.get_total_monthly_savings(),
        engine.get_total_annual_savings(),
        engine.get_pipeline_run_timestamp(),
        top_subs
    )
)
print()
print(
    helper.generate_cleanup_email(
        "Team",
        engine.get_total_disks(),
        engine.get_total_monthly_savings(),
        top_candidates
    )
)