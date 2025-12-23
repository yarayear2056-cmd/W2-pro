from __future__ import annotations
import logging
import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"src"))

from data_workflow.quality import require_columns, assert_non_empty, assert_unique_key
from data_workflow.transforms import parse_datetime, add_time_parts, winsorize, add_outlier_flag
from data_workflow.joins import safe_left_join
from data_workflow.config import make_paths
paths = make_paths(ROOT)
paths.reports.mkdir(parents=True, exist_ok=True)


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def main():
    log.info("Loading processed inputs")

    ord= pd.read_parquet(paths.processed/"orders_clean.parquet")
    us= pd.read_parquet(paths.processed/"users.parquet")

    require_columns(ord, ["order_id", "user_id", "amount", "quantity", "created_at", "sta_clean"])
    require_columns(us, ["user_id", "country", "signup_date"])

    assert_non_empty(ord, "orders_clean")
    assert_non_empty(us, "users")
    assert_unique_key(us, "user_id")

    ord_t= (ord.pipe(parse_datetime, col="created_at", utc=True).pipe(add_time_parts, ts_col="created_at"))

    n_missing_ts = int(ord_t["created_at"].isna().sum())
    log.info("Missing created_at after parse: %s / %s", n_missing_ts, len(ord_t))

    
    log.info("Joining orders with users...")
    joined = safe_left_join(
        ord_t,
        us,
        on="user_id",
        validate="many_to_one",
        suffixes=("", "_user"),
    )

    if len(joined) != len(ord_t):
        raise AssertionError("Row count changed on left join (join explosion?)")

    match_rate = 1.0 - float(joined["country"].isna().mean())
    log.info("Rows after join: %s | Country match rate: %.3f", len(joined), match_rate)

    log.info("Handling outliers in 'amount' column...")
    joined = joined.assign(amount_winsor=winsorize(joined["amount"]))
    joined = add_outlier_flag(joined, "amount", k=1.5)

    log.info("Generating revenue summary by country...")
    
    summ_st = (
        joined.groupby("country", dropna=False)
        .agg(
            n_orders=("order_id", "size"),
            total_revenue=("amount", "sum")
        )
        .reset_index()
        .sort_values("total_revenue", ascending=False)
    )
    
    print("\n--- Revenue Summary Table ---")
    print(summ_st.to_string(index=False))
    summ_st.to_csv(paths.reports / "revenue_by_country.csv", index=False)


    out_path = paths.processed / "analytics_table.parquet"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    joined.to_parquet(out_path, index=False)

    log.info(" Success! Analytics table written to: %s", out_path)

if __name__ == "__main__":
    main()