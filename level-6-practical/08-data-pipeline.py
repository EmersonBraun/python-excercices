"""
Level 6 - Exercise 08: Data Processing Pipeline
=================================================

Difficulty: 3/5 stars
Estimated time: 25 minutes

Build a complete data processing pipeline using only the Python
standard library:  csv, statistics, collections, etc.

The pipeline follows these stages:
    Generate -> Validate -> Transform -> Aggregate -> Report

Uses in-memory CSV data so no external files are needed.

Features
--------
- Generate realistic sample sales data.
- Validate and clean records (handle missing/bad data).
- Transform: compute derived fields (revenue, profit margin).
- Aggregate: group by category, month, region.
- Report: produce a formatted summary report.

Expected output (approximate):
------------------------------
    === Sales Report ===
    Total records:  500
    Total revenue:  $2,345,678.90
    Average order:  $4,691.36

    Top 5 products by revenue:
      1. Widget Pro     $234,567.00
      2. Gadget Ultra   $198,432.00
      ...
"""

import csv
import io
import random
import statistics
from collections import defaultdict
from datetime import datetime, timedelta


# ---------------------------------------------------------------------------
# 1. Data Generation
# ---------------------------------------------------------------------------
PRODUCTS = [
    {"name": "Widget Pro", "category": "Widgets", "base_price": 49.99},
    {"name": "Widget Basic", "category": "Widgets", "base_price": 29.99},
    {"name": "Gadget Ultra", "category": "Gadgets", "base_price": 99.99},
    {"name": "Gadget Lite", "category": "Gadgets", "base_price": 59.99},
    {"name": "Doohickey X", "category": "Doohickeys", "base_price": 149.99},
    {"name": "Doohickey Mini", "category": "Doohickeys", "base_price": 79.99},
    {"name": "Thingamajig", "category": "Misc", "base_price": 19.99},
    {"name": "Whatchamacallit", "category": "Misc", "base_price": 39.99},
]

REGIONS = ["North", "South", "East", "West"]
SALES_REPS = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"]


def generate_sales_data(num_records: int = 500, seed: int = 42) -> str:
    """Generate sample sales CSV data as a string.

    Returns CSV text with columns:
        date, product, category, region, sales_rep, quantity, unit_price, discount

    A small percentage of records will have intentional data quality issues
    (missing values, negative quantities) to exercise the validation stage.
    """
    rng = random.Random(seed)
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    days_range = (end_date - start_date).days

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "date", "product", "category", "region",
        "sales_rep", "quantity", "unit_price", "discount",
    ])

    for i in range(num_records):
        product = rng.choice(PRODUCTS)
        sale_date = start_date + timedelta(days=rng.randint(0, days_range))
        quantity = rng.randint(1, 50)
        # Slight price variation
        unit_price = round(product["base_price"] * rng.uniform(0.9, 1.1), 2)
        discount = round(rng.choice([0, 0, 0, 0.05, 0.10, 0.15, 0.20]), 2)

        # Introduce data quality issues (~3% of records)
        if rng.random() < 0.02:
            quantity = -quantity  # bad: negative quantity
        if rng.random() < 0.01:
            unit_price = ""      # bad: missing price

        writer.writerow([
            sale_date.strftime("%Y-%m-%d"),
            product["name"],
            product["category"],
            rng.choice(REGIONS),
            rng.choice(SALES_REPS),
            quantity,
            unit_price,
            discount,
        ])

    return output.getvalue()


# ---------------------------------------------------------------------------
# 2. Data Validation / Cleaning
# ---------------------------------------------------------------------------
def validate_records(csv_text: str) -> tuple[list[dict], list[dict]]:
    """Parse CSV and validate records.

    Returns (valid_records, rejected_records).
    Each record is a dict with typed values.
    """
    reader = csv.DictReader(io.StringIO(csv_text))
    valid = []
    rejected = []

    for row in reader:
        issues = []

        # Validate quantity
        try:
            qty = int(row["quantity"])
            if qty <= 0:
                issues.append(f"non-positive quantity: {qty}")
        except (ValueError, KeyError):
            issues.append("invalid quantity")
            qty = 0

        # Validate unit_price
        try:
            price = float(row["unit_price"])
            if price <= 0:
                issues.append(f"non-positive price: {price}")
        except (ValueError, KeyError):
            issues.append("invalid/missing price")
            price = 0.0

        # Validate discount
        try:
            discount = float(row.get("discount", 0))
            discount = max(0.0, min(1.0, discount))  # clamp
        except (ValueError, TypeError):
            discount = 0.0

        # Validate date
        try:
            sale_date = datetime.strptime(row["date"], "%Y-%m-%d").date()
        except (ValueError, KeyError):
            issues.append("invalid date")
            sale_date = None

        record = {
            "date": sale_date,
            "product": row.get("product", "Unknown"),
            "category": row.get("category", "Unknown"),
            "region": row.get("region", "Unknown"),
            "sales_rep": row.get("sales_rep", "Unknown"),
            "quantity": qty,
            "unit_price": price,
            "discount": discount,
        }

        if issues:
            record["issues"] = issues
            rejected.append(record)
        else:
            valid.append(record)

    return valid, rejected


# ---------------------------------------------------------------------------
# 3. Transformation (derived fields)
# ---------------------------------------------------------------------------
def transform_records(records: list[dict]) -> list[dict]:
    """Add computed fields to each record.

    New fields:
        - gross_revenue: quantity * unit_price
        - net_revenue:   gross_revenue * (1 - discount)
        - month:         YYYY-MM string
        - quarter:       Q1..Q4
    """
    for r in records:
        r["gross_revenue"] = round(r["quantity"] * r["unit_price"], 2)
        r["net_revenue"] = round(r["gross_revenue"] * (1 - r["discount"]), 2)

        if r["date"]:
            r["month"] = r["date"].strftime("%Y-%m")
            quarter = (r["date"].month - 1) // 3 + 1
            r["quarter"] = f"Q{quarter}"
        else:
            r["month"] = "Unknown"
            r["quarter"] = "Unknown"

    return records


# ---------------------------------------------------------------------------
# 4. Aggregation
# ---------------------------------------------------------------------------
def aggregate_by(records: list[dict], key: str) -> dict[str, dict]:
    """Group records by *key* and compute aggregates.

    Returns dict mapping key_value -> {count, total_revenue, avg_revenue, total_qty}.
    """
    groups = defaultdict(list)
    for r in records:
        groups[r[key]].append(r)

    result = {}
    for group_key, group_records in sorted(groups.items()):
        revenues = [r["net_revenue"] for r in group_records]
        quantities = [r["quantity"] for r in group_records]
        result[group_key] = {
            "count": len(group_records),
            "total_revenue": round(sum(revenues), 2),
            "avg_revenue": round(statistics.mean(revenues), 2),
            "total_quantity": sum(quantities),
            "median_revenue": round(statistics.median(revenues), 2),
        }
    return result


def top_n(records: list[dict], key: str, metric: str = "net_revenue",
          n: int = 5) -> list[tuple[str, float]]:
    """Return top N items by summed metric, grouped by key."""
    totals = defaultdict(float)
    for r in records:
        totals[r[key]] += r[metric]
    sorted_items = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    return [(name, round(val, 2)) for name, val in sorted_items[:n]]


# ---------------------------------------------------------------------------
# 5. Report Generation
# ---------------------------------------------------------------------------
def generate_report(records: list[dict], rejected: list[dict]) -> str:
    """Produce a formatted text report from transformed records."""
    lines = []

    total_rev = sum(r["net_revenue"] for r in records)
    total_qty = sum(r["quantity"] for r in records)

    lines.append("=" * 60)
    lines.append("SALES REPORT 2024")
    lines.append("=" * 60)
    lines.append(f"  Total valid records:    {len(records):,}")
    lines.append(f"  Rejected records:       {len(rejected):,}")
    lines.append(f"  Total net revenue:      ${total_rev:,.2f}")
    lines.append(f"  Total units sold:       {total_qty:,}")
    if records:
        lines.append(f"  Average order revenue:  ${total_rev / len(records):,.2f}")
    lines.append("")

    # Top products
    lines.append("-" * 60)
    lines.append("TOP 5 PRODUCTS BY REVENUE")
    lines.append("-" * 60)
    for i, (name, rev) in enumerate(top_n(records, "product"), 1):
        lines.append(f"  {i}. {name:<25} ${rev:>12,.2f}")
    lines.append("")

    # By category
    lines.append("-" * 60)
    lines.append("REVENUE BY CATEGORY")
    lines.append("-" * 60)
    by_cat = aggregate_by(records, "category")
    for cat, agg in sorted(by_cat.items(), key=lambda x: x[1]["total_revenue"],
                           reverse=True):
        lines.append(f"  {cat:<20} ${agg['total_revenue']:>12,.2f}  "
                     f"({agg['count']} orders, {agg['total_quantity']} units)")
    lines.append("")

    # By region
    lines.append("-" * 60)
    lines.append("REVENUE BY REGION")
    lines.append("-" * 60)
    by_region = aggregate_by(records, "region")
    for region, agg in sorted(by_region.items(),
                              key=lambda x: x[1]["total_revenue"], reverse=True):
        lines.append(f"  {region:<20} ${agg['total_revenue']:>12,.2f}  "
                     f"(avg ${agg['avg_revenue']:,.2f}/order)")
    lines.append("")

    # By quarter
    lines.append("-" * 60)
    lines.append("REVENUE BY QUARTER")
    lines.append("-" * 60)
    by_quarter = aggregate_by(records, "quarter")
    for q in ("Q1", "Q2", "Q3", "Q4"):
        if q in by_quarter:
            agg = by_quarter[q]
            lines.append(f"  {q}  ${agg['total_revenue']:>12,.2f}  "
                         f"({agg['count']} orders)")
    lines.append("")

    # Top sales reps
    lines.append("-" * 60)
    lines.append("TOP SALES REPRESENTATIVES")
    lines.append("-" * 60)
    for i, (name, rev) in enumerate(top_n(records, "sales_rep"), 1):
        lines.append(f"  {i}. {name:<20} ${rev:>12,.2f}")
    lines.append("")

    # Monthly trend
    lines.append("-" * 60)
    lines.append("MONTHLY REVENUE TREND")
    lines.append("-" * 60)
    by_month = aggregate_by(records, "month")
    max_rev = max((a["total_revenue"] for a in by_month.values()), default=1)
    for month in sorted(by_month.keys()):
        agg = by_month[month]
        bar_len = int(40 * agg["total_revenue"] / max_rev) if max_rev else 0
        bar = "#" * bar_len
        lines.append(f"  {month}  ${agg['total_revenue']:>10,.2f}  {bar}")
    lines.append("")

    # Data quality
    if rejected:
        lines.append("-" * 60)
        lines.append("DATA QUALITY ISSUES")
        lines.append("-" * 60)
        issue_counts = defaultdict(int)
        for r in rejected:
            for issue in r.get("issues", []):
                issue_counts[issue] += 1
        for issue, count in sorted(issue_counts.items(),
                                   key=lambda x: x[1], reverse=True):
            lines.append(f"  {issue}: {count} record(s)")
        lines.append("")

    lines.append("=" * 60)
    lines.append("END OF REPORT")
    lines.append("=" * 60)

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 6. Export to CSV
# ---------------------------------------------------------------------------
def export_to_csv(records: list[dict]) -> str:
    """Export transformed records to CSV string."""
    output = io.StringIO()
    if not records:
        return ""

    fieldnames = [
        "date", "product", "category", "region", "sales_rep",
        "quantity", "unit_price", "discount", "gross_revenue",
        "net_revenue", "month", "quarter",
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    for r in records:
        row = dict(r)
        row["date"] = str(row["date"]) if row["date"] else ""
        writer.writerow(row)

    return output.getvalue()


# ===================================================================
# Demo / self-test
# ===================================================================
if __name__ == "__main__":

    print("Stage 1: Generating sample data...")
    raw_csv = generate_sales_data(num_records=500, seed=42)
    # Show first few lines
    preview_lines = raw_csv.split("\n")[:4]
    for line in preview_lines:
        print(f"  {line}")
    print(f"  ... ({raw_csv.count(chr(10)) - 1} total records)\n")

    print("Stage 2: Validating and cleaning...")
    valid, rejected = validate_records(raw_csv)
    print(f"  Valid records:    {len(valid)}")
    print(f"  Rejected records: {len(rejected)}")
    if rejected:
        print(f"  Sample rejection: {rejected[0].get('issues', [])}\n")
    else:
        print()

    print("Stage 3: Transforming (adding derived fields)...")
    records = transform_records(valid)
    sample = records[0]
    print(f"  Sample record: {sample['product']}")
    print(f"    quantity={sample['quantity']}, price=${sample['unit_price']}")
    print(f"    gross=${sample['gross_revenue']}, net=${sample['net_revenue']}")
    print(f"    month={sample['month']}, quarter={sample['quarter']}\n")

    print("Stage 4: Aggregating...")
    by_cat = aggregate_by(records, "category")
    print(f"  Categories: {list(by_cat.keys())}")
    by_region = aggregate_by(records, "region")
    print(f"  Regions: {list(by_region.keys())}\n")

    print("Stage 5: Generating report...\n")
    report = generate_report(records, rejected)
    print(report)

    print("\nStage 6: Exporting to CSV...")
    csv_output = export_to_csv(records)
    csv_lines = csv_output.split("\n")
    print(f"  Exported {len(csv_lines) - 2} records")
    print(f"  Header: {csv_lines[0]}")
    print(f"  First row: {csv_lines[1]}")
    print("\nPipeline complete.")
