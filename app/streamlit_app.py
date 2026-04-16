import os
import sys
import streamlit as st

# Make project root importable when running from app folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from finops_query_engine import FinOpsQueryEngine
from finops_llm_helper import FinOpsLLMHelper


st.set_page_config(page_title="FinOps AI Assistant", layout="wide")

engine = FinOpsQueryEngine(data_path="samples")
helper = FinOpsLLMHelper()


def detect_days_from_query(query: str, default: int = 60) -> int:
    words = query.lower().split()
    for i, word in enumerate(words):
        if word.isdigit():
            return int(word)
        if word.endswith("days"):
            number = word.replace("days", "")
            if number.isdigit():
                return int(number)
    return default


def handle_query(query: str) -> str:
    q = query.lower().strip()

    if "subscription" in q and ("saving" in q or "cost" in q or "highest" in q):
        df = engine.get_top_subscriptions_by_savings()
        return helper.generate_top_subscriptions_answer(df)

    if "high severity" in q or "older than" in q or "age" in q:
        days = detect_days_from_query(q, default=60)
        df = engine.get_high_severity_old_disks(days)
        return helper.generate_high_severity_answer(df, days)

    if "annual savings" in q or "total annual" in q:
        return helper.generate_total_savings_answer(
            engine.get_total_monthly_savings(),
            engine.get_total_annual_savings(),
        )

    if "monthly savings" in q:
        monthly = engine.get_total_monthly_savings()
        return f"The total estimated monthly savings opportunity is {helper.format_currency(monthly)}."

    if "delete first" in q or "cleanup" in q or "top candidates" in q:
        df = engine.get_top_cleanup_candidates()
        return helper.generate_cleanup_priority_answer(df)

    if "summary" in q or "executive summary" in q:
        return helper.generate_executive_summary(
            engine.get_total_disks(),
            engine.get_total_monthly_savings(),
            engine.get_total_annual_savings(),
            engine.get_pipeline_run_timestamp(),
            engine.get_top_subscriptions_by_savings(),
        )

    if "email" in q or "mail" in q:
        return helper.generate_cleanup_email(
            "Team",
            engine.get_total_disks(),
            engine.get_total_monthly_savings(),
            engine.get_top_cleanup_candidates(),
        )

    if "total disks" in q or "how many disks" in q:
        return f"The pipeline identified {engine.get_total_disks()} orphaned disks."

    return (
        "I could not understand that question yet. Try asking about subscriptions, "
        "high severity disks, annual savings, cleanup candidates, executive summary, or email generation."
    )


st.title("Azure Orphaned Disk FinOps AI Assistant")
st.caption("Ask questions about orphaned disks, savings opportunities, and cleanup priorities.")

example_questions = [
    "Which subscriptions have the highest orphaned disk savings?",
    "Show high severity disks older than 60 days.",
    "What is the total annual savings opportunity?",
    "Which disks should be deleted first?",
    "Generate an executive summary.",
    "Generate a cleanup email.",
]

with st.expander("Example questions"):
    for item in example_questions:
        st.write(f"- {item}")

user_query = st.text_input("Ask your question")

if user_query:
    try:
        response = handle_query(user_query)
        st.text_area("Assistant Response", response, height=320)
    except Exception as e:
        st.error(f"Something went wrong while processing the query: {e}")

with st.sidebar:
    st.subheader("Current Snapshot")
    try:
        st.write(f"**Total Disks:** {engine.get_total_disks()}")
        st.write(f"**Monthly Savings:** {helper.format_currency(engine.get_total_monthly_savings())}")
        st.write(f"**Annual Savings:** {helper.format_currency(engine.get_total_annual_savings())}")
        st.write(f"**Pipeline Run:** {engine.get_pipeline_run_timestamp()}")
    except Exception as e:
        st.warning(f"Could not load sidebar summary: {e}")