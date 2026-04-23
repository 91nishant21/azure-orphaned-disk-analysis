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