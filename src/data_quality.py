import os
import pandas as pd


def run_quality_checks():
    """
    Loads dataset and performs data quality checks.
    Saves a quality report to /reports.
    """

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(BASE_DIR, "data", "dataset.csv")

    reports_dir = os.path.join(BASE_DIR, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    df = pd.read_csv(file_path, encoding="ISO-8859-1")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

    report_lines = []
    report_lines.append("=== DATA QUALITY REPORT ===\n")

    # Missing values
    report_lines.append("Missing Values Per Column:\n")
    report_lines.append(str(df.isnull().sum()))
    report_lines.append("\n")

    # Duplicates
    duplicates = df.duplicated().sum()
    report_lines.append(f"Duplicate Rows: {duplicates}\n")

    # Negative quantities
    negative_qty = (df["Quantity"] < 0).sum()
    report_lines.append(f"Negative Quantities: {negative_qty}\n")

    # Bad prices
    bad_prices = (df["UnitPrice"] <= 0).sum()
    report_lines.append(f"Zero or Negative Prices: {bad_prices}\n")

    # Save report
    report_path = os.path.join(reports_dir, "quality_report.txt")

    with open(report_path, "w") as f:
        for line in report_lines:
            f.write(line + "\n")

    print("Data quality report generated.")

    return df
