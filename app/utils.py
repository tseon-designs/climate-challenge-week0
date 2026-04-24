"""
utils.py — Utility functions for the Streamlit dashboard.
Handles data loading and aggregation for interactive visualizations.
"""

import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go

# ── Color palette for all 5 countries ──────────────────────────────────────────
COUNTRY_COLORS = {
    "Ethiopia": "#E63946",
    "Kenya":    "#2A9D8F",
    "Sudan":    "#E9C46A",
    "Tanzania": "#F4A261",
    "Nigeria":  "#6A4C93",
}

COUNTRIES = ["Ethiopia", "Kenya", "Sudan", "Tanzania", "Nigeria"]


# Graceful caching — works with or without Streamlit
def st_cache_if_available(func):
    try:
        import streamlit as st
        return st.cache_data(func)
    except Exception:
        return func


def get_data_path(country: str) -> str:
    """Return the path to the cleaned CSV for a given country."""
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "data", f"{country.lower()}_clean.csv")


@st_cache_if_available
def load_all_countries() -> pd.DataFrame:
    """
    Load and concatenate all 5 cleaned country CSVs.
    Returns None if data files are not found.
    """
    dfs = []
    for country in COUNTRIES:
        path = get_data_path(country)
        if os.path.exists(path):
            df = pd.read_csv(path, parse_dates=["Date"])
            df["Country"] = country
            dfs.append(df)
    if not dfs:
        return None
    return pd.concat(dfs, ignore_index=True)


def filter_data(df: pd.DataFrame, countries: list, year_range: tuple) -> pd.DataFrame:
    """Filter the combined DataFrame by country list and year range."""
    mask = (
        df["Country"].isin(countries) &
        (df["YEAR"] >= year_range[0]) &
        (df["YEAR"] <= year_range[1])
    )
    return df[mask].copy()


def monthly_agg(df: pd.DataFrame, variable: str) -> pd.DataFrame:
    """Compute monthly average of a variable, grouped by Country."""
    df = df.copy()
    df["YearMonth"] = df["Date"].dt.to_period("M").dt.to_timestamp()
    return df.groupby(["Country", "YearMonth"])[variable].mean().reset_index()


def annual_agg(df: pd.DataFrame, variable: str) -> pd.DataFrame:
    """Compute annual average of a variable, grouped by Country."""
    return df.groupby(["Country", "YEAR"])[variable].mean().reset_index()


def temperature_trend_chart(df: pd.DataFrame, variable: str = "T2M") -> go.Figure:
    """Plotly line chart of monthly average temperature by country."""
    monthly = monthly_agg(df, variable)
    fig = px.line(
        monthly,
        x="YearMonth", y=variable,
        color="Country",
        color_discrete_map=COUNTRY_COLORS,
        title=f"Monthly Average {variable} by Country",
        labels={"YearMonth": "Date", variable: f"{variable} (°C)"}
    )
    fig.update_layout(
        plot_bgcolor="#1e293b",
        paper_bgcolor="#0f172a",
        font_color="#e2e8f0",
        legend=dict(bgcolor="#1e293b"),
        hovermode="x unified"
    )
    return fig


def precipitation_boxplot(df: pd.DataFrame) -> go.Figure:
    """Plotly boxplot of PRECTOTCORR by country."""
    fig = px.box(
        df,
        x="Country", y="PRECTOTCORR",
        color="Country",
        color_discrete_map=COUNTRY_COLORS,
        title="Precipitation Distribution by Country",
        labels={"PRECTOTCORR": "Precipitation (mm/day)"},
        log_y=True
    )
    fig.update_layout(
        plot_bgcolor="#1e293b",
        paper_bgcolor="#0f172a",
        font_color="#e2e8f0",
        showlegend=False
    )
    return fig


def extreme_heat_bar(df: pd.DataFrame) -> go.Figure:
    """Bar chart of extreme heat days (T2M_MAX > 35°C) per year per country."""
    heat = df[df["T2M_MAX"] > 35].groupby(["Country", "YEAR"]).size().reset_index(name="Extreme Heat Days")
    fig = px.bar(
        heat,
        x="YEAR", y="Extreme Heat Days",
        color="Country",
        color_discrete_map=COUNTRY_COLORS,
        barmode="group",
        title="Extreme Heat Days (T2M_MAX > 35°C) per Year",
        labels={"YEAR": "Year"}
    )
    fig.update_layout(
        plot_bgcolor="#1e293b",
        paper_bgcolor="#0f172a",
        font_color="#e2e8f0"
    )
    return fig


def summary_stats_table(df: pd.DataFrame, variable: str) -> pd.DataFrame:
    """Return a summary table of mean, median, std for a variable by country."""
    return df.groupby("Country")[variable].agg(
        Mean="mean", Median="median", Std="std"
    ).round(2).reset_index()



