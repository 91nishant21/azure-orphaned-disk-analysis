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