import sys
import logging
from pathlib import Path


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
    ord = enforce_schema(read_orders_csv(paths.raw / "orders.csv"   ))

    write_parquet(ord, paths.processed / "orders.parquet")
    write_parquet(us, paths.processed / "users.parquet")

    logging.info("Row counts: orders=%s, users=%s", len(ord), len(us))
    logging.info("Output to:%s and %s", paths.processed/"orders.parquet", paths.processed / "users.parquet")

if __name__ == "__main__":
    main()





