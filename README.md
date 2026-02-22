# Sales Data Quality & Reporting System

## Overview
This project simulates a small Business Intelligence workflow using Python and MySQL.

It demonstrates:
- Data ingestion from CSV
- Structured storage in MySQL
- Automated data validation checks
- Revenue KPI calculation
- Business-focused reporting

The dataset used is the Online Retail dataset (UK-based transactional data).

---

## Tech Stack
- Python (pandas)
- MySQL
- Git / GitHub
- VS Code

---

## Project Architecture

CSV → Data Cleaning → MySQL Storage → Validation → KPI Analysis → Text Reports

---

## Key Features

### 1. Data Ingestion
- Reads large CSV dataset
- Converts date formats safely
- Handles missing values
- Inserts into relational database

### 2. Data Quality Validation
- Missing value detection
- Duplicate detection
- Negative quantity detection (returns)
- Price anomaly checks
- Country diversity check

### 3. KPI Reporting
- Total revenue calculation
- Top 10 products by revenue
- Revenue by country
- Monthly revenue trend analysis
- Removal of cancellations and invalid transactions

---

## Example Insights

- Total Revenue: £10.6M
- 38 countries involved
- Strong Q4 seasonal growth
- UK dominates revenue distribution

---

## Author
Karan Homayounfar
MSc Data Science Student - UWE Bristol
Focused on Data Engineering & Quantitative Systems