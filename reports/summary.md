# Analysis Summary

## Key Findings

- The analytics dataset contains **5** rows and **18** columns after processing.
- Total revenue varies by country; **SA** generated the highest cumulative revenue of  **145.5**.
- Monthly revenue shows a **(NAL)** trend over time, with a peak in .
- Order amounts are right-skewed; winsorization reduces the impact of extreme outliers while preserving the overall distribution.
- Refund behavior differs between Saudi Arabia (SA) and United Arab Emirates (AE):
  - Difference in mean refund rate (SA − AE): **(0)**  
  - 95% bootstrap confidence interval: **[(0)، (0)]**
---

## Definitions

- **Revenue**: Sum of the `amount` column.
- **Monthly revenue**: Revenue aggregated by the `month` column.
- **Winsorized amount (`amount_winsor`)**: Order amounts capped at extreme values to limit outlier influence.
- **Refund indicator**: Binary variable equal to 1 when `status == "refund"`, otherwise 0.
- **Bootstrap difference in means**: A resampling-based method used to estimate the difference in average refund rates between SA and AE.

---

## Data Quality Caveats

- **Missingness**:
  - Missing values were observed in the following columns:
    - `amount_winsor`: **(1)**
    - `quantity`: **(1)**
    - `created_at`: **(1)**
    - `date `: **(1)**
    - `year`: **(1)**
    - `month`: **(1)**
    - `hour `: **(1)**
    - `dow`: **(1)**
    - `amount__is_outlierh`: **(1)**


    
- **Duplicates**:
  - No explicit duplicate removal was applied; the analysis assumes upstream data is already de-duplicated.
- **Join coverage**:
  - Aggregations used `dropna=False`, so records with missing country or month values were retained.
- **Outliers**:
  - Extreme values in the raw `amount` column exist; winsorization was applied to mitigate their impact.

---

## Next Questions

- How do refund rates change over time within each country?
- Are revenue trends consistent when analyzed at a weekly granularity?
- What share of total revenue is driven by the top 5% of orders?
- Is there a relationship between order amount and refund likelihood?

## Technical Notes

- **ETL Pipeline**: Run `uv run python scripts/run_etl.py` to reproduce processed outputs
- **Run Metadata**: See `data/processed/_run_meta.json` for run details
- **Data Source**: Raw data in `data/raw/`, processed outputs in `data/processed/`
- **EDA Notebook**: See `notebooks/eda.ipynb` for detailed analysis