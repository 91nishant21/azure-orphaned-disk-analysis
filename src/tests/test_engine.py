"""
===========================================================
Project   : Azure FinOps Optimization - Orphaned Disk Cleanup
Module    : Testing & Validation
File      : test_engine.py
Version   : v1.0
Author    : Internal Use
Created   : 2026-04-26
Updated   : 2026-04-26

Description:
-----------------------------------------------------------
Test and validation script for FinOpsQueryEngine to verify 
data processing logic, query outputs, and integration with 
AI-based response generation.

Key Functions:
-----------------------------------------------------------
- Validates query engine outputs using sample datasets
- Tests key metrics (disk count, savings, classifications)
- Verifies high severity and cleanup candidate logic
- Ensures compatibility with AI response generation layer
- Supports debugging and development validation

Inputs:
-----------------------------------------------------------
- Data Source: samples/ (enriched datasets)
- Test Queries : Predefined queries for validation

Outputs:
-----------------------------------------------------------
- Console-based validation results
- Debug logs for query outputs and correctness checks

Dependencies:
-----------------------------------------------------------
- FinOpsQueryEngine
- FinOpsLLMHelper (if used)
- pandas (if applicable)

Notes:
-----------------------------------------------------------
- Intended for development and testing purposes only
- Not part of production pipeline execution
- Can be extended to unit test frameworks (pytest/unittest)
- No client-specific or sensitive data is used
===========================================================
"""
from src.ai.finops_query_engine import FinOpsQueryEngine

engine = FinOpsQueryEngine()

print("Total Disks:", engine.get_total_disks())
print("Monthly Savings:", engine.get_total_monthly_savings())
print("Annual Savings:", engine.get_total_annual_savings())
print("Pipeline Run Timestamp:", engine.get_pipeline_run_timestamp())

print("\nTop subscriptions by savings:")
print(engine.get_top_subscriptions_by_savings())

print("\nHigh severity disks older than 60 days:")
print(engine.get_high_severity_old_disks(60))

print("\nTop cleanup candidates:")
print(engine.get_top_cleanup_candidates())