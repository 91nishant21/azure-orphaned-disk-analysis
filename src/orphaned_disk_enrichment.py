import csv
import logging
from pathlib import Path
from datetime import datetime

# ===============================
# File Paths
# ===============================

INPUT_FILE = Path("input/orphaned_disks_sample.csv")
OUTPUT_FILE = Path("samples/orphaned_disk_recommendations.csv")
SUMMARY_FILE = Path("samples/orphaned_disk_summary.csv")
TOP_FILE = Path("samples/top_cleanup_candidates.csv")

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "orphaned_disk_run.log"

# ===============================
# Logging Setup
# ===============================

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# ===============================
# Pricing Model
# ===============================

SKU_RATES = {
    "Premium_LRS": 0.12,
    "StandardSSD_LRS": 0.08,
    "Standard_LRS": 0.05
}

def get_rate(sku):
    return SKU_RATES.get(sku, 0.06)

# ===============================
# Pipeline Execution
# ===============================

try:

    run_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    logging.info("Pipeline started")
    logging.info(f"Input file: {INPUT_FILE}")

    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    rows = []
    total_cost = 0

    with open(INPUT_FILE) as f:

        reader = csv.DictReader(f)

        required_columns = ["DiskName","SubscriptionName","ResourceGroup","Location","DiskSku","DiskSizeGB","AgeDays"]

        for col in required_columns:
            if col not in reader.fieldnames:
                raise ValueError(f"Missing required column: {col}")

        for r in reader:

            size = int(r["DiskSizeGB"])
            sku = r["DiskSku"]
            age = int(r["AgeDays"])

            cost = round(size * get_rate(sku),2)

            if age > 60:
                severity = "High"
            elif age > 30:
                severity = "Medium"
            else:
                severity = "Low"

            r["EstimatedMonthlyCost"] = cost
            r["Severity"] = severity
            r["PipelineRunTimestamp"] = run_timestamp

            rows.append(r)
            total_cost += cost

    if len(rows) == 0:
        raise ValueError("No records processed from input file")

    logging.info(f"Total disks processed: {len(rows)}")

    rows.sort(key=lambda x: float(x["EstimatedMonthlyCost"]), reverse=True)

    # ===============================
    # Write Recommendations
    # ===============================

    with open(OUTPUT_FILE,"w",newline="") as f:

        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    logging.info(f"Recommendations file written: {OUTPUT_FILE}")

    # ===============================
    # Write Summary
    # ===============================

    with open(SUMMARY_FILE,"w",newline="") as f:

        writer = csv.writer(f)
        writer.writerow(["TotalDisks","EstimatedMonthlyCost","PipelineRunTimestamp"])
        writer.writerow([len(rows), round(total_cost,2), run_timestamp])

    logging.info(f"Summary file written: {SUMMARY_FILE}")

    # ===============================
    # Write Top Candidates
    # ===============================

    top = rows[:10]

    with open(TOP_FILE,"w",newline="") as f:

        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(top)

    logging.info(f"Top cleanup candidates written: {TOP_FILE}")
    logging.info(f"Top candidates count: {len(top)}")

    logging.info("Pipeline completed successfully")

    print("Files generated successfully")

except Exception as e:

    logging.exception(f"Pipeline failed: {e}")
    print(f"Pipeline failed: {e}")