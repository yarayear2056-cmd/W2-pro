# Data Work Flow Project


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
