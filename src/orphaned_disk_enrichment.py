import csv
from pathlib import Path

INPUT_FILE = Path("samples/orphaned_disks_sample.csv")
OUTPUT_FILE = Path("samples/orphaned_disk_recommendations.csv")
SUMMARY_FILE = Path("samples/orphaned_disk_summary.csv")
TOP_FILE = Path("samples/top_cleanup_candidates.csv")

SKU_RATES = {
    "Premium_LRS": 0.12,
    "StandardSSD_LRS": 0.08,
    "Standard_LRS": 0.05
}

def get_rate(sku):
    return SKU_RATES.get(sku, 0.06)

rows = []
total_cost = 0

with open(INPUT_FILE) as f:
    reader = csv.DictReader(f)

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

        rows.append(r)
        total_cost += cost

rows.sort(key=lambda x: x["EstimatedMonthlyCost"], reverse=True)

with open(OUTPUT_FILE,"w",newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

with open(SUMMARY_FILE,"w",newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["TotalDisks","EstimatedMonthlyCost"])
    writer.writerow([len(rows), round(total_cost,2)])

top = rows[:10]

with open(TOP_FILE,"w",newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(top)

print("Files generated successfully")