import pandas as pd
from analytics.growth import calculate_growth_series


def build_metrics_df(metrics_list: list[dict]) -> pd.DataFrame:
    """
    Convert a list of metric dicts (from DB) into a clean sorted DataFrame.

    Steps:
        1. Convert to DataFrame
        2. Sort by month ascending
        3. Fill missing values with 0
    """
    if not metrics_list:
        return pd.DataFrame()

    df = pd.DataFrame(metrics_list)
    df["month"] = pd.to_datetime(df["month"])
    df = df.sort_values("month").reset_index(drop=True)

    # fill any missing metric fields with 0
    numeric_cols = ["monthly_users", "monthly_revenue", "employee_count",
                    "funding_raised", "burn_rate"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    return df


def add_growth_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add month-over-month growth rate columns to the metrics DataFrame.

    Adds:
        - user_growth
        - revenue_growth
        - employee_growth
    """
    if df.empty:
        return df

    df["user_growth"]     = calculate_growth_series(df["monthly_users"].tolist())
    df["revenue_growth"]  = calculate_growth_series(df["monthly_revenue"].tolist())
    df["employee_growth"] = calculate_growth_series(df["employee_count"].tolist())

    return df


def calculate_momentum(df: pd.DataFrame, col: str = "revenue_growth") -> float:
    """
    Calculate startup momentum using the last two growth values.

    Formula:
        momentum = recent_growth * 0.6 + previous_growth * 0.4

    A startup accelerating gets a higher score than one slowing down.
    Returns 0.0 if not enough data.
    """
    if df.empty or col not in df.columns or len(df) < 2:
        return 0.0

    growth_col = df[col].tolist()
    recent   = growth_col[-1]
    previous = growth_col[-2]

    momentum = (recent * 0.6) + (previous * 0.4)
    return round(momentum, 4)


def get_latest_metrics(df: pd.DataFrame) -> dict:
    """
    Return the most recent month's metrics as a plain dict.
    Useful for dashboard summary cards.
    """
    if df.empty:
        return {}
    return df.iloc[-1].to_dict()