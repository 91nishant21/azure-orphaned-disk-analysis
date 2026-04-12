import os
import pandas as pd


class FinOpsQueryEngine:
    def __init__(self, data_path="samples"):
        self.data_path = data_path

        self.recommendations = pd.read_csv(
            os.path.join(data_path, "orphaned_disk_recommendations.csv")
        )
        self.summary = pd.read_csv(
            os.path.join(data_path, "orphaned_disk_summary.csv")
        )
        self.top_candidates = pd.read_csv(
            os.path.join(data_path, "top_cleanup_candidates.csv")
        )

        # Clean column names
        self.recommendations.columns = self.recommendations.columns.str.strip()
        self.summary.columns = self.summary.columns.str.strip()
        self.top_candidates.columns = self.top_candidates.columns.str.strip()

    # -------------------------------
    # BASIC METRICS
    # -------------------------------

    def get_total_disks(self):
        return int(self.summary["TotalDisks"].sum())

    def get_total_monthly_savings(self):
        return float(self.summary["EstimatedMonthlyCost"].sum())

    def get_total_annual_savings(self):
        return float(self.summary["EstimatedMonthlyCost"].sum()) * 12

    def get_pipeline_run_timestamp(self):
        return str(self.summary["PipelineRunTimestamp"].iloc[0])

    # -------------------------------
    # BUSINESS QUESTIONS
    # -------------------------------

    def get_top_subscriptions_by_savings(self, top_n=5):
        df = (
            self.top_candidates.groupby("SubscriptionName")["EstimatedMonthlyCost"]
            .sum()
            .reset_index()
        )
        df = df.sort_values(by="EstimatedMonthlyCost", ascending=False).head(top_n)
        return df

    def get_high_severity_old_disks(self, days=60):
        df = self.top_candidates[
            (self.top_candidates["Severity"] == "High") &
            (self.top_candidates["AgeDays"] >= days)
        ]
        return df

    def get_top_cleanup_candidates(self, top_n=10):
        df = self.top_candidates.sort_values(
            by="EstimatedMonthlyCost", ascending=False
        ).head(top_n)
        return df

    def get_subscription_savings_summary(self):
        df = (
            self.top_candidates.groupby("SubscriptionName")["EstimatedMonthlyCost"]
            .sum()
            .reset_index()
        )
        df = df.sort_values(by="EstimatedMonthlyCost", ascending=False)
        return df