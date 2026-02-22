import os
import pandas as pd

# Path setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, "data", "dataset.csv")

df = pd.read_csv(file_path, encoding="ISO-8859-1")

# Convert date
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

# Remove cancellations (InvoiceNo starting with C)
df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

# Remove negative quantities
df = df[df["Quantity"] > 0]

# Calculate revenue
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

report_lines = []
report_lines.append("=== SALES KPI REPORT ===\n")

# 1️⃣ Total Revenue
total_revenue = df["Revenue"].sum()
report_lines.append(f"Total Revenue: £{total_revenue:,.2f}\n")

# 2️⃣ Top 10 Products
top_products = (
    df.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

report_lines.append("Top 10 Products by Revenue:\n")
report_lines.append(str(top_products))
report_lines.append("\n")

# 3️⃣ Revenue by Country
revenue_by_country = (
    df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

report_lines.append("Revenue by Country:\n")
report_lines.append(str(revenue_by_country))
report_lines.append("\n")

# 4️⃣ Monthly Revenue Trend
df["YearMonth"] = df["InvoiceDate"].dt.to_period("M")

monthly_revenue = (
    df.groupby("YearMonth")["Revenue"]
    .sum()
)

report_lines.append("Monthly Revenue Trend:\n")
report_lines.append(str(monthly_revenue))

# Save report
report_path = os.path.join(BASE_DIR, "reports", "sales_kpi_report.txt")

with open(report_path, "w") as f:
    for line in report_lines:
        f.write(line + "\n")

print("Sales KPI report generated.")
