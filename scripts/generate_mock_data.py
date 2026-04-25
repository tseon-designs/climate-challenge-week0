import pandas as pd
import numpy as np
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.clean import load_and_parse, clean_dataframe, export_clean

def generate_realistic_data(country, base_temp, rain_prob):
    print(f"Generating data for {country}...")
    dates = pd.date_range(start="2015-01-01", end="2026-03-01", freq="D")
    n = len(dates)
    
    # Base temperature with seasonal sine wave and slight warming trend
    days_from_start = np.arange(n)
    seasonal = 3 * np.sin(2 * np.pi * dates.dayofyear / 365.25)
    trend = days_from_start * (0.05 / 365) # 0.5 degree per decade
    
    t2m = base_temp + seasonal + trend + np.random.normal(0, 1.5, n)
    t2m_max = t2m + np.random.uniform(3, 8, n)
    t2m_min = t2m - np.random.uniform(3, 8, n)
    t2m_range = t2m_max - t2m_min
    
    # Precipitation (log-normal, many zero days)
    is_raining = np.random.random(n) < rain_prob
    precip = np.zeros(n)
    precip[is_raining] = np.random.lognormal(mean=1.5, sigma=1.0, size=is_raining.sum())
    
    df = pd.DataFrame({
        "YEAR": dates.year,
        "DOY": dates.dayofyear,
        "T2M": t2m,
        "T2M_MAX": t2m_max,
        "T2M_MIN": t2m_min,
        "T2M_RANGE": t2m_range,
        "PRECTOTCORR": precip,
        "RH2M": np.clip(np.random.normal(60, 15, n), 10, 100),
        "WS2M": np.random.lognormal(mean=1.0, sigma=0.5, size=n),
        "WS2M_MAX": np.random.lognormal(mean=1.5, sigma=0.5, size=n),
        "PS": np.random.normal(90, 5, size=n),
        "QV2M": np.random.normal(10, 3, size=n)
    })
    
    # Add some NASA sentinels (-999) to test cleaning
    drop_idx = np.random.choice(n, size=int(n*0.01), replace=False)
    df.loc[drop_idx, "T2M"] = -999
    
    os.makedirs("data", exist_ok=True)
    raw_path = f"data/{country.lower()}.csv"
    df.to_csv(raw_path, index=False)
    return raw_path

def main():
    countries = {
        "Ethiopia": (22.0, 0.3),
        "Kenya": (24.0, 0.25),
        "Sudan": (29.0, 0.05),
        "Tanzania": (25.0, 0.35),
        "Nigeria": (27.0, 0.4)
    }
    
    WEATHER_COLS = ['T2M', 'T2M_MAX', 'T2M_MIN', 'PRECTOTCORR', 'RH2M', 'WS2M', 'WS2M_MAX']
    
    for country, (temp, rain) in countries.items():
        raw_path = generate_realistic_data(country, temp, rain)
        
        # Now clean it using the project's own pipeline!
        print(f"Cleaning {country} using src.clean...")
        df_raw = load_and_parse(raw_path, country)
        df_clean = clean_dataframe(
            df_raw,
            outlier_cols=WEATHER_COLS,
            z_threshold=3.0,
            outlier_action='retain',
            fill_method='ffill',
            missing_row_threshold=0.30
        )
        clean_path = f"data/{country.lower()}_clean.csv"
        export_clean(df_clean, clean_path)
        print("---")

if __name__ == "__main__":
    main()
