# 📊 Sales Data Quality & Reporting System  
![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)
![Status](https://img.shields.io/badge/Project-Active-brightgreen.svg)

A compact, end‑to‑end data workflow demonstrating how raw transactional data can be cleaned, validated, stored, and transformed into business‑ready insights.  
Built as a practical BI‑style project using Python and MySQL.

---

## 🚀 Overview

This project simulates a lightweight Business Intelligence pipeline:

1. **Ingest** raw CSV data  
2. **Clean & validate** the dataset  
3. **Store** it in a relational database  
4. **Generate** automated data quality checks  
5. **Produce** revenue KPIs and text‑based reports  
6. **Visualise** key business metrics  

The dataset used is the *Online Retail* dataset, sourced from Kaggle:  
🔗 [https://www.kaggle.com/datasets/ulrikthygepedersen/online-retail-dataset](https://www.kaggle.com/datasets/ulrikthygepedersen/online-retail-dataset)

---

## 🛠️ Tech Stack

- **Python** (pandas, matplotlib)  
- **MySQL**  
- **VS Code**  
- **Git / GitHub**

---

## 🧱 Architecture

```
CSV → Cleaning → MySQL Storage → Quality Checks → KPI Analysis → Reports & Visuals
```

All processing steps are modularised inside the `src/` directory for clarity and reusability.

---

## ✨ Key Features

### 📥 1. Data Ingestion
- Reads large CSV files efficiently  
- Converts date formats safely  
- Handles missing and invalid values  
- Inserts cleaned data into MySQL  

### 🔍 2. Data Quality Validation
- Missing value detection  
- Duplicate row checks  
- Negative quantity detection  
- Zero/negative price checks  
- Basic country distribution checks  

### 📈 3. KPI Reporting
- Total revenue  
- Top 10 products by revenue  
- Revenue by country  
- Monthly revenue trend  
- Removal of cancellations and invalid transactions  

### 🖼️ 4. Visual Outputs
Saved to the `outputs/` directory:
- Monthly revenue trend  
- Top 10 products  
- Top 10 countries  

Charts are styled for readability and simplicity.

---

## 📊 Example Insights

- Total Revenue: **£10.6M**  
- Transactions across **38 countries**  
- Strong seasonal uplift in Q4  
- UK dominates overall revenue  

---

## 📁 Project Structure

```
project/
│
├── src/
│   ├── load_data.py
│   ├── data_quality.py
│   └── generate_report.py
│
├── data/
│   └── dataset.csv
│
├── reports/
│   ├── quality_report.txt
│   └── sales_kpi_report.txt
│
├── outputs/
│   ├── monthly_revenue_trend.png
│   ├── top_10_products.png
│   └── top_10_countries.png
│
└── notebooks/
    └── sales_analysis.ipynb
```


## 👤 Author

**Karan Homayounfar**  
MSc Data Science — UWE Bristol  
Focused on Data Engineering & Quantitative Systems

---

## 🔮 Future Improvements

- Add SQL‑based aggregation for performance comparison  
- Introduce logging instead of print statements  
- Add primary keys and duplicate constraints  
- Implement automated unit tests  
- Optional: build a small Streamlit dashboard  

---

## 📄 License

This project is released under the **MIT License**.  
You are free to use, modify, and build upon it.

