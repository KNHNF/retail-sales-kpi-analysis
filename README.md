# Retail Sales KPI Analysis

A practical, end‑to‑end data engineering and analytics workflow that transforms raw retail transactions into validated, structured, and business‑ready insights. The project demonstrates ingestion, cleaning, MySQL storage, automated data quality checks, KPI generation, and visual reporting.

---

## Overview

This project simulates a lightweight BI and data‑engineering pipeline. It takes raw CSV data, cleans and validates it, loads it into a relational database, performs automated quality checks, and generates revenue‑focused KPIs along with visual summaries. The goal is to show how messy transactional data can be turned into reliable business insights.

---

## Why This Project Matters

Retail data is often inconsistent, duplicated, and difficult to analyse without proper preprocessing. This project demonstrates a practical approach to:

- cleaning and validating raw data  
- storing it in a structured format  
- generating meaningful KPIs  
- producing clear visual summaries  
- designing a modular Python workflow  

It reflects the type of work done in analytics, BI engineering, and data‑driven decision‑making roles.

---

## Tech Stack

- Python (pandas, matplotlib)  
- MySQL 8.0  
- VS Code  
- Git and GitHub  

---

## Setup Instructions

1. Download the dataset from Kaggle and place it in the `data` folder.  
   Dataset: Online Retail (2010–2011)

2. Create a virtual environment  
   ```
   python -m venv venv
   ```

3. Activate it  
   Windows:  
   ```
   venv\Scripts\activate
   ```

4. Install dependencies  
   ```
   pip install -r requirements.txt
   ```

5. Update MySQL connection details inside `load_data.py`.

6. Run the pipeline  
   ```
   python src/load_data.py
   python src/data_quality.py
   python src/generate_report.py
   ```

Reports and visual outputs will be saved in the `reports` and `outputs` directories.

---

## Architecture Summary

The workflow follows this sequence:

**CSV → Cleaning → MySQL Storage → Quality Checks → KPI Analysis → Reports and Visuals**

Each step is modularised inside the `src` directory for clarity and reusability.

---

## Key Features

### Data Ingestion
- Efficient CSV loading  
- Safe datetime parsing  
- Handling of missing and invalid values  
- Inserts cleaned data into MySQL  

### Data Quality Validation
- Missing value checks  
- Duplicate detection  
- Negative quantity and price checks  
- Country distribution checks  

### KPI Reporting
- Total revenue  
- Top products  
- Revenue by country  
- Monthly revenue trend  
- Removal of cancellations and invalid transactions  

### Visual Outputs
Generated charts include:

- Monthly revenue trend  
- Top 10 products  
- Top 10 countries  

All visuals are saved in the `outputs` directory.

---

## Example Insights

- Total revenue: approximately £10.6M  
- Transactions across 38 countries  
- Strong seasonal uplift in Q4  
- The UK is the dominant revenue source  

---

## Limitations

- Dataset is historical (2010–2011)  
- No customer‑level segmentation  
- No product hierarchy  
- No currency conversion  
- MySQL schema is intentionally simple for demonstration  

---

## Future Improvements

- Add SQL‑based aggregation for performance comparison  
- Introduce logging  
- Add primary keys and duplicate constraints  
- Implement automated unit tests  
- Optional: build a Streamlit dashboard  

---

## Author

Karan Homayounfar  
MSc Data Science — UWE Bristol  
Focused on data engineering and quantitative systems

---

## License

Released under the MIT License. Free to use, modify, and build upon.
