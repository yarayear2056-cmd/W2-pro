import logging
import sys
from pathlib import Path

from data_workflow.config import make_paths
from data_workflow.io import read_orders_csv, read_parquet, read_users_csv, write_parquet
from data_workflow.transforms import enforce_schema, missingness_report, add_missing_flags, normalize_text, apply_mapping
from data_workflow.quality import require_columns, assert_non_empty, assert_in_range

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def main():
    r= make_paths(ROOT)
    log.info("Loading row inputs")
    ord= read_orders_csv(r.raw / "orders.csv")
    us= read_users_csv(r.raw / "users.csv")
    log.info("rows: orders=%s , users=%s", len(ord), len(us))

    require_columns(ord, ["order_id", "user_id", "amount", "quantity", "status", "created_at"])
    require_columns(us, ["user_id", "country", "signup_date"])
    assert_non_empty(ord, "orders")
    assert_non_empty(us, "users")

    ord= enforce_schema(ord)

    rp= missingness_report(ord)
    rep_dir= ROOT / "reports"
    rep_dir.mkdir(parents=True, exist_ok=True)
    r_path= rep_dir/"orders_missingness.csv"
    rp.to_csv(r_path, index=True)
    log.info("wrote missingness report to %s", r_path)

    sta_nor= normalize_text(ord["status"])
    mapping= {"paid":"paid", "pending":"pending", "canceled":"canceled", "cancelled":"canceled", "refunded":"refund"}
    sta_clean= apply_mapping(sta_nor, mapping)

    ord_clean= (
        ord.assign(sta_clean=sta_clean)
        .pipe(add_missing_flags, cols=["amount", "quantity"])
    )

    assert_in_range(ord_clean["amount"],lo=0,name= 'amount')
    assert_in_range(ord_clean["quantity"],lo=0,name= 'quantity')

    write_parquet(ord_clean, r.processed / "orders_clean.parquet")
    write_parquet(us, r.processed / "users.parquet")
    log.info("Wrote processed outputs to %s ", r.processed / "orders_clean.parquet")

if __name__ == "__main__":
    main()
