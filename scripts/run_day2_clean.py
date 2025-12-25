import logging
import sys
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from data_workflow.config import make_paths
from data_workflow.io import read_orders_csv, read_users_csv, write_parquet
from data_workflow.transforms import enforce_schema, missingness_report, add_missing_flags, normalize_text, apply_mapping
from data_workflow.quality import require_columns, assert_non_empty, assert_in_range, assert_unique_key

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main():
    P= make_paths(ROOT)
    log.info("Loading row inputs")
    ord= read_orders_csv(P.raw / "orders.csv")
    us= read_users_csv(P.raw / "users.csv")
    log.info("rows: orders=%s , users=%s", len(ord), len(us))

    require_columns(ord, ["order_id", "user_id", "amount", "quantity", "status", "created_at"])
    require_columns(us, ["user_id", "country", "signup_date"])
    assert_non_empty(ord, "orders")
    assert_non_empty(us, "users")

    assert_unique_key(us, "user_id")  #optional Day2


    ord= enforce_schema(ord)

    rep = missingness_report(ord)
    rep_path = P.reports / "missingness_orders.csv"
    rep.to_csv(rep_path)
    log.info("saved in report %s", rep_path)

    sta_nor= normalize_text(ord["status"])
    mapping= {"paid":"paid", "pending":"pending", "canceled":"canceled", "cancelled":"canceled", "refunded":"refund"}
    sta_clean= apply_mapping(sta_nor, mapping)

    ord_clean= (
        ord.assign(sta_clean=sta_clean)
        .pipe(add_missing_flags, cols=["amount", "quantity"])
    )

    assert_in_range(ord_clean["amount"],lo=0,name= 'amount')
    assert_in_range(ord_clean["quantity"],lo=0,name= 'quantity')

    #optional Day2
    summary = {
        "row_count":{
            "ord_raw":len(ord),
            "ord_clean":len(ord_clean),
            "users":len(us),
        },
        "top_3_missing_cols": rep['p_missing'].head(3).to_dict()
    }
    summary_path = P.reports / "data_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    log.info("Saved data summary to %s", summary_path)

    write_parquet(ord_clean, P.processed / "orders_clean.parquet")
    write_parquet(us, P.processed / "users.parquet")
    log.info("Wrote processed outputs to %s ", P.processed / "orders_clean.parquet")

if __name__ == "__main__":
    main()
