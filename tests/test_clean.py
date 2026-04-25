import pytest
import pandas as pd
import numpy as np
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.clean import load_and_parse, report_missing, flag_outliers, clean_dataframe

@pytest.fixture
def sample_df():
    """Create a sample NASA-style dataframe for testing."""
    data = {
        "YEAR": [2020, 2020, 2020],
        "DOY": [1, 2, 3],
        "T2M": [25.0, -999, 27.0],
        "T2M_MAX": [30.0, 31.0, 45.0],  # 45 is an outlier
        "PRECTOTCORR": [0.0, 5.0, 0.0]
    }
    return pd.DataFrame(data)

def test_load_and_parse_sentinels(sample_df, tmp_path):
    """Test that -999 is correctly replaced by NaN."""
    csv_path = tmp_path / "test.csv"
    sample_df.to_csv(csv_path, index=False)
    
    df_loaded = load_and_parse(str(csv_path), "TestCountry")
    
    assert df_loaded["T2M"].isna().iloc[1]
    assert df_loaded["Country"].iloc[0] == "TestCountry"
    assert "Date" in df_loaded.columns
    assert df_loaded["Date"].iloc[0] == pd.Timestamp("2020-01-01")

def test_flag_outliers():
    """Test Z-score outlier detection."""
    df = pd.DataFrame({"val": [10, 10.1, 10.2, 10, 50]}) # 50 is an outlier
    mask = flag_outliers(df, ["val"], z_threshold=1.5)
    assert mask.iloc[4] == True
    assert mask.iloc[0] == False

def test_clean_dataframe_ffill():
    """Test that missing values are forward-filled."""
    df = pd.DataFrame({
        "Date": pd.to_datetime(["2020-01-01", "2020-01-02", "2020-01-03"]),
        "T2M": [25.0, np.nan, 27.0],
        "YEAR": [2020, 2020, 2020]
    })
    
    df_clean = clean_dataframe(
        df, 
        outlier_cols=["T2M"], 
        outlier_action="retain",
        fill_method="ffill",
        missing_row_threshold=0.50
    )
    
    assert df_clean["T2M"].iloc[1] == 25.0
