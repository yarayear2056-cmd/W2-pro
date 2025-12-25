# Data Work Flow Project

## Project Overview
This project implements a professional, "offline-first" data pipeline designed to process raw business data and transform it into actionable insights. The focus is on building a reproducible ETL (Extract, Transform, Load) workflow and performing thorough Exploratory Data Analysis (EDA) using high-quality visualization and statistical uncertainty.

## Key Learning Objectives
- **Reproducible ETL:** Building a pipeline that runs from raw data to processed outputs with a single command.
- **Data Quality:** Implementing fail-fast checks to ensure data integrity.
- **Advanced EDA:** Using Plotly for interactive charts and Bootstrap for confidence intervals (CIs).
- **Handoff Quality:** Maintaining a professional repository structure and documentation.

## Repository Structure
```text

├── data/
│   ├── raw/          # Immutable source files (CSV/Excel)
│   ├── cache/        # Cached API responses/downloads
│   └── processed/    # Final, typed Parquet files (e.g., analytics_table.parquet)
├── notebooks/
│   └── eda.ipynb     # Main analysis notebook (reads from processed data)
├── reports/
│   ├── figures/      # Exported Plotly visualizations 
│   └── summary.md    # Business findings, caveats, and next steps
├── scripts/
│   └── run_etl.py    # Main script to execute the entire ETL pipeline
└── src/data_workfram/
    ├── config.py     # Centralized path management
    ├── etl.py        # Core transformation and loading logic
    ├── joins.py      # Safe join operations and validation
    └── quality.py    # Data quality and cleaning functions
```    

## How To Run 
 **1.Environment Setup:**

 >source .venv/bin/activate  
 ### Or 
> .venv\Scripts\Activate.ps1 on Windows [cite: 82]
pip install -r requirements.txt

**2.Execute the Pipeline:**
>python scripts/run_etl.py


### More Info 

## Day 1


This project focuses on the initial steps of organizing and cleaning order and user data. The goal is to convert standard CSV files into professional, high-performance Parquet files.


## Project Structure


* **data/raw** 

>Stores immutable input data (original files).

* **data/processed**

> Stores cleaned, analysis-ready outputs.


* **scripts**

 >Contains the executable run scripts.


* **src**
>The core logic and data transformation.

 -----

## Day 2


**Data Quality Assurance & Refinement**



Implemented a robust validation framework to transition from basic data structuring to ensuring complete data integrity and logical consistency.



###  What's New?


1. **Quality Guards**:
 The pipeline now "fails fast" if it detects empty files or missing required columns.


2. **Range Validation**: 
Automated checks to ensure amounts and quantities are never negative.


3. **Missingness Reports**: 
Generates a `missingness_orders.csv` report showing the count and percentage of missing data per column.


4. **Text Normalization**:
Standardized text fields (e.g., converting "PAID " and "paid" into a uniform "paid" status).

------


## How to Run

Open your Terminal in the project root directory and use the command for your operating system:

### For Windows Users:

```
powershell
$env:PYTHONPATH="src"
python scripts/run_day1_load.py
```
```
day2:

$env:PYTHONPATH = "src"
python scripts/run_day2_clean.py
```


### For Mac & Linux Users

```
export PYTHONPATH=src
python3 scripts/run_day1_load.py
```

```
day2:

export PYTHONPATH=src
python3 scripts/run_day2_clean.py
```
