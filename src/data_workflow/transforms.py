import pandas as pd
import re

def enforce_schema(df:pd.DataFrame)->pd.DataFrame:
    return df.assign(
        order_id=df["order_id"].astype("string"),
        user_id=df["user_id"].astype("string"),
        amount=pd.to_numeric(df["amount"], errors="coerce").astype("Float64"),
        quantity=pd.to_numeric(df["quantity"], errors="coerce").astype("Int64"),
    )

def missingness_report(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.isna().sum()
        .rename("n_missing")
        .to_frame()
        .assign(p_missing=lambda t: t["n_missing"] / len(df))
        .sort_values("p_missing", ascending=False)
    )




def add_missing_flags(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    out = df.copy()
    for c in cols:
        out[f"{c}__isna"] = out[c].isna()
    return out

def normalize_text(s: pd.Series) -> pd.Series:
    _ws = re.compile(r"\s+")
    return (
        s.astype("string")
        .str.strip()
        .str.casefold()
        .str.replace(_ws, " ", regex=True)
    )

def apply_mapping(s: pd.Series, mapping: dict[str, str]) -> pd.Series:
    return  s.map(lambda x: mapping.get(x, x))


def dedupe_keep_latest(df: pd.DataFrame, key_cols: list[str], ts_col: str) -> pd.DataFrame:
    sorted= df.sort_values(ts_col, ascending=False)
    deduped= sorted.drop_duplicates(subset=key_cols, keep="first")
    return deduped.reset_index(drop=True)


def parse_datetime(df: pd.DataFrame, col: str, *, utc: bool = True) -> pd.DataFrame:
   return df.assign(**{
        col: pd.to_datetime(df[col], errors="coerce", utc=utc)
    })

def add_time_parts(df: pd.DataFrame, ts_col: str) -> pd.DataFrame:
    ts = df[ts_col]
    return df.assign(
        date = ts.dt.date,
        month = ts.dt.to_period("M"),
        year = ts.dt.year,
        dow= ts.dt.day_name(),
        hour= ts.dt.hour,
    )


def iqr_bounds(s: pd.Series, k: float = 1.5) -> tuple[float, float]:
    Q1 = s.quantile(0.25)
    Q3 = s.quantile(0.75)
    IQR = Q3 - Q1
    low = Q1 - k * IQR
    up = Q3 + k * IQR
    return float(low), float(up)


def winsorize(s: pd.Series, lo: float = 0.01, hi: float = 0.99) -> pd.Series:
    l =s.quantile(lo)
    u = s.quantile(hi)
    return s.clip(lower= l, upper= u)

def add_outlier_flag(df: pd.DataFrame, col: str, *, k: float = 1.5) -> pd.DataFrame:
    df = df.copy()
    low, up = iqr_bounds(df[col], k=k)
    df = df.assign(**{f"{col}__is_outlier": (df[col] < low) | (df[col] > up)})
    return df






