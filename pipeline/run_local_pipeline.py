"""
===========================================================
Project   : Azure FinOps Optimization – Orphaned Disk Cleanup
Module    : Local Pipeline Orchestration
File      : run_local_pipeline.py
Version   : v1.1

Description:
-----------------------------------------------------------
Runs the local pipeline after CSV input is available.
Skips live Azure discovery and manual Power BI refresh.
===========================================================
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
SAMPLES_DIR = BASE_DIR / "samples"
LOGS_DIR = BASE_DIR / "logs"


def run_command(command: list[str], step_name: str) -> None:
    print("\n" + "=" * 70)
    print(step_name)
    print("=" * 70)
    print("Command:", " ".join(command))

    result = subprocess.run(
        command,          # IMPORTANT: keep this as list, not string
        cwd=str(BASE_DIR),
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"Pipeline failed at: {step_name}")

    print(f"Completed: {step_name}")


def validate_project() -> None:
    print("\nValidating project structure...")

    required_folders = [
        SAMPLES_DIR,
        BASE_DIR / "src",
        BASE_DIR / "src" / "processing",
        BASE_DIR / "src" / "reporting",
        BASE_DIR / "src" / "app",
    ]

    for folder in required_folders:
        if not folder.exists():
            raise FileNotFoundError(f"Missing folder: {folder}")

    LOGS_DIR.mkdir(exist_ok=True)

    print("Project structure validation completed.")


def show_manual_powerbi_step() -> None:
    print("\n" + "=" * 70)
    print("MANUAL STEP - POWER BI REFRESH")
    print("=" * 70)
    print("1. Open the Power BI file from the powerbi folder.")
    print("2. Click Refresh.")
    print("3. Validate KPIs, charts, and tables.")
    print("4. Save the PBIX file after refresh.")


def main() -> None:
    print("=" * 70)
    print("Azure Orphaned Disk FinOps - Local Pipeline")
    print("=" * 70)
    print(f"Pipeline started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Project root: {BASE_DIR}")

    validate_project()

    run_command(
        [sys.executable, "-m", "src.processing.orphaned_disk_enrichment"],
        "STEP 1 - Run Python enrichment"
    )

    run_command(
        [sys.executable, "-m", "src.reporting.email_helper"],
        "STEP 2 - Generate email/reporting summary"
    )

    show_manual_powerbi_step()

    run_command(
        [sys.executable, "-m", "streamlit", "run", str(BASE_DIR / "src" / "app" / "streamlit_app.py")],
        "STEP 3 - Launch Streamlit app"
    )

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()