"""
clean.py — Reusable data cleaning functions for NASA POWER climate data.

Used by all country-level EDA notebooks to ensure consistent preprocessing.
"""

import pandas as pd
import numpy as np
from scipy import stats


# NASA sentinel value for missing / out-of-range data
NASA_SENTINEL = -999


def load_and_parse(filepath: str, country_name: str) -> pd.DataFrame:
    """
    Load a NASA POWER CSV, add a Country column, replace -999 sentinels
    with NaN, and parse YEAR + DOY into a proper datetime column.

    Parameters
    ----------
    filepath : str
        Path to the raw CSV file.
    country_name : str
        Human-readable country name (e.g. 'Ethiopia').

    Returns
    -------
    pd.DataFrame
        DataFrame with a 'Date' column and a 'Month' column added.
    """
    df = pd.read_csv(filepath)

    # Add country identifier
    df["Country"] = country_name

    # Replace NASA sentinel with NaN
    df.replace(NASA_SENTINEL, np.nan, inplace=True)

    # Build proper date from YEAR + DOY (day-of-year)
    df["Date"] = pd.to_datetime(
        df["YEAR"].astype(int) * 1000 + df["DOY"].astype(int),
        format="%Y%j"
    )

    # Extract month for seasonal analysis
    df["Month"] = df["Date"].dt.month

    return df


def report_missing(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute the count and percentage of missing values per column.

    Returns a summary DataFrame sorted by percentage descending.
    """
    total = len(df)
    missing_count = df.isna().sum()
    missing_pct = (missing_count / total * 100).round(2)
    summary = pd.DataFrame({
        "missing_count": missing_count,
        "missing_pct": missing_pct
    }).sort_values("missing_pct", ascending=False)
    return summary[summary["missing_count"] > 0]


def flag_outliers(df: pd.DataFrame, columns: list, z_threshold: float = 3.0) -> pd.Series:
    """
    Flag rows where the absolute Z-score exceeds `z_threshold`
    in ANY of the specified columns.

    Returns a boolean Series (True = outlier row).
    """
    z_scores = df[columns].apply(
        lambda col: np.abs(stats.zscore(col.dropna()))
    )
    # Re-index to match original df (NaNs get False)
    outlier_mask = pd.Series(False, index=df.index)
    for col in columns:
        valid_idx = df[col].dropna().index
        z = np.abs(stats.zscore(df.loc[valid_idx, col]))
        outlier_mask.loc[valid_idx] |= (z > z_threshold)
    return outlier_mask


def clean_dataframe(
    df: pd.DataFrame,
    outlier_cols: list,
    z_threshold: float = 3.0,
    outlier_action: str = "retain",
    fill_method: str = "ffill",
    missing_row_threshold: float = 0.30
) -> pd.DataFrame:
    """
    Full cleaning pipeline:
    1. Drop duplicate rows.
    2. Flag outliers using Z-score.
    3. Handle outliers (drop / cap / retain).
    4. Drop rows with > missing_row_threshold fraction of NaNs.
    5. Forward-fill remaining missing values.

    Parameters
    ----------
    df : pd.DataFrame
    outlier_cols : list
        Columns to compute Z-scores on.
    z_threshold : float
        Z-score threshold to flag outliers.
    outlier_action : str
        One of 'drop', 'cap', 'retain'.
    fill_method : str
        'ffill' or 'bfill'.
    missing_row_threshold : float
        Drop rows where the fraction of missing values exceeds this.

    Returns
    -------
    pd.DataFrame
        Cleaned DataFrame.
    """
    original_len = len(df)

    # 1. Drop duplicates
    n_duplicates = df.duplicated().sum()
    df = df.drop_duplicates()
    print(f"  [clean] Dropped {n_duplicates} duplicate rows.")

    # 2. Flag outliers
    outlier_mask = flag_outliers(df, outlier_cols, z_threshold)
    n_outliers = outlier_mask.sum()
    print(f"  [clean] Found {n_outliers} outlier rows (|Z| > {z_threshold}).")

    # 3. Handle outliers
    if outlier_action == "drop":
        df = df[~outlier_mask]
        print(f"  [clean] Dropped {n_outliers} outlier rows.")
    elif outlier_action == "cap":
        for col in outlier_cols:
            lower = df[col].quantile(0.01)
            upper = df[col].quantile(0.99)
            df[col] = df[col].clip(lower, upper)
        print(f"  [clean] Capped outlier values to 1st–99th percentile.")
    else:
        print(f"  [clean] Retained outlier rows (action='{outlier_action}').")

    # 4. Drop rows with too many missing values
    row_missing_frac = df.isna().mean(axis=1)
    n_high_missing = (row_missing_frac > missing_row_threshold).sum()
    df = df[row_missing_frac <= missing_row_threshold]
    print(f"  [clean] Dropped {n_high_missing} rows with >{missing_row_threshold*100:.0f}% missing values.")

    # 5. Forward-fill remaining NaNs
    df = df.sort_values("Date").reset_index(drop=True)
    df[outlier_cols] = df[outlier_cols].ffill()
    print(f"  [clean] Applied '{fill_method}' to fill remaining NaNs.")
    print(f"  [clean] Final shape: {len(df)} rows (from {original_len}).")

    return df


def export_clean(df: pd.DataFrame, output_path: str) -> None:
    """Save cleaned DataFrame to CSV."""
    df.to_csv(output_path, index=False)
    print(f"  [export] Saved cleaned data to '{output_path}'")
