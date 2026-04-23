
from typing import Any
import pandas as pd


class FinOpsLLMHelper:
    def format_currency(self, value: float) -> str:
        return f"${value:,.2f}"

    def dataframe_to_text(self, df: pd.DataFrame, max_rows: int = 10) -> str:
        if df is None or df.empty:
            return "No matching records found."

        trimmed_df = df.head(max_rows).copy()
        return trimmed_df.to_string(index=False)

    def generate_top_subscriptions_answer(self, df: pd.DataFrame) -> str:
        if df is None or df.empty:
            return "I could not find any subscription-level savings data."

        lines = ["The subscriptions with the highest orphaned disk savings are:"]
        for _, row in df.iterrows():
            lines.append(
                f"- {row['SubscriptionName']}: {self.format_currency(float(row['EstimatedMonthlyCost']))} per month"
            )
        return "\n".join(lines)

    def generate_high_severity_answer(self, df: pd.DataFrame, days: int) -> str:
        if df is None or df.empty:
            return f"No high severity disks older than {days} days were found."

        lines = [f"I found {len(df)} high severity disks older than {days} days:"]
        for _, row in df.head(10).iterrows():
            lines.append(
                f"- {row['DiskName']} | Subscription: {row['SubscriptionName']} | "
                f"Age: {row['AgeDays']} days | Monthly Cost: {self.format_currency(float(row['EstimatedMonthlyCost']))}"
            )
        return "\n".join(lines)

    def generate_total_savings_answer(self, monthly_savings: float, annual_savings: float) -> str:
        return (
            f"The total orphaned disk savings opportunity is "
            f"{self.format_currency(monthly_savings)} per month and "
            f"{self.format_currency(annual_savings)} per year."
        )

    def generate_cleanup_priority_answer(self, df: pd.DataFrame) -> str:
        if df is None or df.empty:
            return "I could not find any cleanup candidates."

        lines = ["These disks should be reviewed first for cleanup priority:"]
        for _, row in df.head(10).iterrows():
            lines.append(
                f"- {row['DiskName']} | Severity: {row['Severity']} | "
                f"Age: {row['AgeDays']} days | Monthly Cost: {self.format_currency(float(row['EstimatedMonthlyCost']))}"
            )
        return "\n".join(lines)

    def generate_executive_summary(
        self,
        total_disks: int,
        monthly_savings: float,
        annual_savings: float,
        run_timestamp: str,
        top_subscriptions_df: pd.DataFrame,
    ) -> str:
        summary_lines = [
            "Executive Summary",
            f"- Total orphaned disks identified: {total_disks}",
            f"- Estimated monthly savings: {self.format_currency(monthly_savings)}",
            f"- Estimated annual savings: {self.format_currency(annual_savings)}",
            f"- Pipeline run timestamp: {run_timestamp}",
        ]

        if top_subscriptions_df is not None and not top_subscriptions_df.empty:
            top_row = top_subscriptions_df.iloc[0]
            summary_lines.append(
                f"- Highest savings subscription: {top_row['SubscriptionName']} "
                f"at {self.format_currency(float(top_row['EstimatedMonthlyCost']))} per month"
            )

        summary_lines.append(
            "- Recommended action: prioritize older high-severity disks with the highest monthly cost impact."
        )

        return "\n".join(summary_lines)

    def generate_cleanup_email(
        self,
        recipient_group: str,
        total_disks: int,
        monthly_savings: float,
        top_candidates_df: pd.DataFrame,
    ) -> str:
        lines = [
            f"Subject: Orphaned Disk Cleanup Recommendation",
            "",
            f"Hi {recipient_group},",
            "",
            f"We have identified {total_disks} orphaned disks with an estimated monthly savings opportunity of "
            f"{self.format_currency(monthly_savings)} if cleaned up.",
            "",
            "The top candidates for review are:",
        ]

        if top_candidates_df is not None and not top_candidates_df.empty:
            for _, row in top_candidates_df.head(5).iterrows():
                lines.append(
                    f"- {row['DiskName']} | Subscription: {row['SubscriptionName']} | "
                    f"Severity: {row['Severity']} | Monthly Cost: {self.format_currency(float(row['EstimatedMonthlyCost']))}"
                )
        else:
            lines.append("- No top candidates available.")

        lines.extend(
            [
                "",
                "Please review these disks for validation and deletion approval where applicable.",
                "",
                "Regards,",
                "FinOps Optimization Team",
            ]
        )

        return "\n".join(lines)