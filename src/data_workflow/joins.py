from __future__ import annotations
import pandas as pd

def safe_left_join(left: pd.DataFrame, right: pd.DataFrame, on, validate, suffixes=("_l", "_r")) -> pd.DataFrame:
    join = left.merge(
        right,
        how="left",
        on=on,
        validate=validate,
        suffixes=suffixes,
    )
    return join