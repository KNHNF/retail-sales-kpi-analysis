import os
import pandas as pd

# Get file path properly
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, "data", "dataset.csv")

df = pd.read_csv(file_path, encoding="ISO-8859-1")

# Convert date
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

report_lines = []

report_lines.append("=== DATA QUALITY REPORT ===\n")

# 1️⃣ Missing values
report_lines.append("Missing Values Per Column:\n")
report_lines.append(str(df.isnull().sum()))
report_lines.append("\n")

# 2️⃣ Duplicate rows
duplicates = df.duplicated().sum()
report_lines.append(f"Duplicate Rows: {duplicates}\n")

# 3️⃣ Negative quantities (returns or errors)
negative_qty = (df["Quantity"] < 0).sum()
report_lines.append(f"Negative Quantities: {negative_qty}\n")

# 4️⃣ Zero or negative prices
bad_prices = (df["UnitPrice"] <= 0).sum()
report_lines.append(f"Zero or Negative Prices: {bad_prices}\n")

# 5️⃣ Unique countries
unique_countries = df["Country"].nunique()
report_lines.append(f"Number of Countries: {unique_countries}\n")

# Save report
report_path = os.path.join(BASE_DIR, "reports", "quality_report.txt")

with open(report_path, "w") as f:
    for line in report_lines:
        f.write(line + "\n")

print("Data quality report generated.")
