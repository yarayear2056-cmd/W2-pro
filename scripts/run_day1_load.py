from pathlib import Path
import sys
import json
from datetime import datetime, timezone
import logging


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from data_workflow.config import make_paths
from data_workflow.io import read_orders_csv,read_users_csv, write_parquet
from data_workflow.transforms import enforce_schema


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def main() -> None:
    paths = make_paths(ROOT)
    us= read_users_csv(paths.raw / "users.csv")
    ord = enforce_schema(read_orders_csv(paths.raw / "orders.csv"))

    out_ord = paths.processed / "orders.parquet"
    out_us = paths.processed / "users.parquet"

    write_parquet(ord, out_ord)
    write_parquet(us, out_us)
    
    meta = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "rows": {"orders": int(len(ord)), "users": int(len(us))},
        "outputs": {"orders": str(out_ord), "users": str(out_us)},}
    
    (paths.processed / "_run_meta.json").write_text(json.dumps(meta, indent=2))

    log.info("Row counts: orders=%s, users=%s", len(ord), len(us))
    log.info("Run metadata saved to _run_meta.json")


if __name__ == "__main__":
    main()





