# Data Flow Work  Project

## 📌Project Overview
This project delivers a complete Data Pipeline built on the "Offline-First" principle. It focuses on transforming Raw Data (orders and users) into Analytics-Ready tables, ensuring data quality, reproducibility, and safety throughout the process.

## 🎯 Key Learning Objectives
- **Offline-First ETL:** Building a workflow that does not depend on the internet after initial setup, separating data into Raw and Processed stages.
- **Data Quality(Fail Fast):** Implementing data quality checks that stop execution immediately if critical errors (like missing columns or empty files) are detected.
- **Safe Joins:** Using safe join strategies (Validate Many-to-One) to prevent row explosions and ensure data integrity.
- **Advanced EDA:** Conducting exploratory analysis using Plotly for visualization and Bootstrap Intervals for uncertainty estimation.

## 1📂Repository Structure
The final project structure follows the standard Day 5 layout:
```text

├── data/
│   ├── raw/       # Immutable source files (CSV)
│   ├── cache/
│   ├── raw/
│   │    └── orders.csv
│   │    └── users.csv         
│   └── processed/    # Final, typed Parquet files (e.g., analytics_table.parquet)
├── notebooks/
│   └── eda.ipynb     # Main analysis
├── reports/
│   ├── figures/      #Plotly  visualizations 
│   ├── missngness_orders.csv
│   ├──data_summary.json
│   ├──revenue_by_country.csv
│   └── summary.md    # findings, caveats
├── scripts/
│   └── run_etl.py    # Main script to execute 
the entire ETL pipeline
│    └── run_day1_load.py
│    └── run_day2_clean.py
│    └── run_day3_build_analytics.py
├── src/data_workflom/
│            ├── config.py    # Centralized path │            management
│            ├── etl.py        # ETL Pipeline
│            ├──io.py
│            ├── joins.py     # Safe join │            operations 
│            └── quality.py    # Data quality 
│            └── viz.py        # Visualization │            Module
│            └── utils.py       # Resampling
│            └── transforms.py      # clean 
├── main.py
├── .gitignore
├── README.md
├── .pythom-version
└──  pyproject.toml


```    

## ⚙️Preraquisites and Installation :
 
 *Before running this project, make sure you have:* 
 - ensure you have Python 3.9+
 - A text editor (VS  Code) or any code  editor.

 1. Clone the repository:
 ```bash
https://github.com/yarayear2056-cmd/W2-pro.git
 ```

 2. Setup Virtual Environment:
 ```bash
uv sync
 ```
or
```bash
Windows: 
python -m venv .venv
.\.venv\Scripts\Activate.ps1

Mac/Linux:
python -m venv .venv
source .venv/bin/activate

```



## 🚀How To Run
You can run the project in two ways: executing the full Pipeline (Recommended) or running each stage individually.

 **Option 1: Run Full ETL (Recommended)**

*This script reads raw data, cleans it, joins it, and saves the final outputs and metadata.* 
```bash
python scripts/run_etl.py
```

**Option 2: Step-by-Step Workflow**

*Step 1: Load Raw Data **Day 1** Convert CSV files to Parquet while preserving data types (Typed I/O)* 

```bash
$env:PYTHONPATH = "src"       
uv run .\scripts\run_day1_load.py                                
```
*Step 2: Clean & Verify **Day 2**Apply quality rules, normalize text, and save the missingness report.* 

```bash
$env:PYTHONPATH = "src"       
uv run .\scripts\run_day2_clean.py                                
```
*Step 3: Build Analytics Table **Day 3** Handle dates, manage outliers, and merge tables using Safe Join.* 

```bash
$env:PYTHONPATH = "src"       
uv run .\scripts\run_day3_build_analytics.py                                
```


## 🔍 Features (Day by Day)
**Day 1: Foundations**
- Set up standard project structure.

- Implement config.py for path management using pathlib.

- Convert data to Parquet format to preserve Dtypes.

**Day 2: Data Quality & Cleaning**

- Fail Fast: Stop execution immediately if files are empty or columns are missing.


- Missingness: Generate automated reports for missing values instead of arbitrary deletion.


- Text Normalization: Standardize text cases (e.g., "Paid" and "paid" become "paid").

**Day 3: Feature Engineering & Joins**

- Time Parts: Extract Month, Day, and Hour from created_at.


- Safe Joins: Validate key uniqueness before merging (One-to-Many Validation).


- Outliers: Use Winsorization to handle extreme values in visualizations.

**Day 4: EDA & Visualization**
- Create eda.ipynb reading only from data/processed.

- Export charts as PNG files to the reports/figures folder.

- Compute Bootstrap Confidence Intervals to compare means.

**Day 5: Production Pipeline**
- Consolidate all steps into a single run_etl() function.

- Generate _run_meta.json containing run statistics to ensure traceability.

- Write the final summary.md




![image here](https://blog.bismart.com/hubfs/Imported_Blog_Media/ETL%20vs%20ELT%20proceso%20y%20arquitectura-Sep-26-2023-08-49-27-9469-AM.jpg)

