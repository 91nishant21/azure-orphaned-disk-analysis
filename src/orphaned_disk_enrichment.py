import csv
from pathlib import Path

INPUT_FILE = Path("samples/orphaned_disks_sample.csv")
OUTPUT_FILE = Path("samples/orphaned_disk_recommendations.csv")
SUMMARY_FILE = Path("samples/orphaned_disk_summary.csv")

SKU_RATES = {
    "Premium_LRS": 0.12,
    "PremiumV2_LRS": 0.14,
    "StandardSSD_LRS": 0.08,
    "StandardSSD_ZRS": 0.09,
    "Standard_LRS": 0.05,
    "Standard_ZRS": 0.06,
}

SEVERITY_SCORES = {
    "High": 3,
    "Medium": 2,
    "Low": 1,
    "Excluded": 0,
}


def get_rate(sku: str) -> float:
    return SKU_RATES.get((sku or "").strip(), 0.06)


def to_int(value: str, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def get_severity(classification: str, age_days: int, size_gb: int, sku: str) -> str:
    classification = (classification or "").strip()

    if classification == "EXCLUDE":
        return "Excluded"

    if classification == "REVIEW":
        return "Low"

    if classification == "SAFE" and age_days >= 30 and size_gb >= 128 and "Premium" in (sku or ""):
        return "High"

    if classification == "SAFE":
        return "Medium"

    return "Low"


def get_priority_score(severity: str, age_days: int, size_gb: int) -> int:
    sev_score = SEVERITY_SCORES.get(severity, 0)
    age_score = 2 if age_days >= 60 else 1 if age_days >= 30 else 0
    size_score = 2 if size_gb >= 512 else 1 if size_gb >= 128 else 0
    return sev_score + age_score + size_score


def get_action(classification: str, severity: str) -> str:
    if classification == "EXCLUDE":
        return "Retain / ignore"
    if classification == "REVIEW":
        return "Review before deletion"
    if severity in ["High", "Medium"]:
        return "Validate and delete"
    return "Review"


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    rows = []
    total_disks = 0
    total_estimated_monthly_cost = 0.0
    safe_count = 0
    review_count = 0
    exclude_count = 0
    high_count = 0
    medium_count = 0
    low_count = 0

    with INPUT_FILE.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            total_disks += 1

            age_days = to_int(row.get("AgeDays"))
            size_gb = to_int(row.get("DiskSizeGB"))
            sku = (row.get("DiskSku") or "").strip()
            classification = (row.get("Classification") or "").strip()

            estimated_monthly_cost = round(size_gb * get_rate(sku), 2)
            severity = get_severity(classification, age_days, size_gb, sku)
            priority_score = get_priority_score(severity, age_days, size_gb)
            action = get_action(classification, severity)

            if classification == "SAFE":
                safe_count += 1
            elif classification == "REVIEW":
                review_count += 1
            elif classification == "EXCLUDE":
                exclude_count += 1

            if severity == "High":
                high_count += 1
            elif severity == "Medium":
                medium_count += 1
            elif severity == "Low":
                low_count += 1

            total_estimated_monthly_cost += estimated_monthly_cost

            row["EstimatedMonthlyCost"] = estimated_monthly_cost
            row["Severity"] = severity
            row["PriorityScore"] = priority_score
            row["RecommendedAction"] = action

            rows.append(row)

    rows.sort(
        key=lambda x: (
            to_int(str(x.get("PriorityScore", 0))),
            float(x.get("EstimatedMonthlyCost", 0)),
        ),
        reverse=True,
    )

    for index, row in enumerate(rows, start=1):
        row["Rank"] = index

    fieldnames = list(rows[0].keys()) if rows else []

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    with SUMMARY_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "TotalDisks",
                "SafeCount",
                "ReviewCount",
                "ExcludeCount",
                "HighSeverityCount",
                "MediumSeverityCount",
                "LowSeverityCount",
                "EstimatedTotalMonthlyCost",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "TotalDisks": total_disks,
                "SafeCount": safe_count,
                "ReviewCount": review_count,
                "ExcludeCount": exclude_count,
                "HighSeverityCount": high_count,
                "MediumSeverityCount": medium_count,
                "LowSeverityCount": low_count,
                "EstimatedTotalMonthlyCost": round(total_estimated_monthly_cost, 2),
            }
        )

    print(f"Enriched file created: {OUTPUT_FILE}")
    print(f"Summary file created: {SUMMARY_FILE}")


if __name__ == "__main__":
    main()