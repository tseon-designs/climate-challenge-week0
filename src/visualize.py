"""
visualize.py — Reusable plotting functions for climate EDA and comparison.

All functions return matplotlib Figure objects so notebooks can display
and save them independently.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from matplotlib.lines import Line2D

# ──────────────────────────────────────────────────────────────────────────────
# Shared style
# ──────────────────────────────────────────────────────────────────────────────

COUNTRY_COLORS = {
    "Ethiopia": "#E63946",
    "Kenya":    "#2A9D8F",
    "Sudan":    "#E9C46A",
    "Tanzania": "#F4A261",
    "Nigeria":  "#6A4C93",
}

def set_style():
    """Apply a clean, dark-background style for all plots."""
    plt.rcParams.update({
        "figure.facecolor":  "#0f172a",
        "axes.facecolor":    "#1e293b",
        "axes.edgecolor":    "#334155",
        "axes.labelcolor":   "#e2e8f0",
        "xtick.color":       "#94a3b8",
        "ytick.color":       "#94a3b8",
        "text.color":        "#e2e8f0",
        "grid.color":        "#334155",
        "grid.linestyle":    "--",
        "grid.alpha":        0.5,
        "font.family":       "sans-serif",
        "axes.titlesize":    13,
        "axes.labelsize":    11,
    })


# ──────────────────────────────────────────────────────────────────────────────
# Time Series
# ──────────────────────────────────────────────────────────────────────────────

def plot_monthly_temperature(df: pd.DataFrame, country: str) -> plt.Figure:
    """
    Line chart of monthly average T2M (2015–2026).
    Annotates the warmest and coolest months.
    """
    set_style()
    monthly = df.groupby(df["Date"].dt.to_period("M"))["T2M"].mean()
    monthly.index = monthly.index.to_timestamp()

    fig, ax = plt.subplots(figsize=(14, 5))
    color = COUNTRY_COLORS.get(country, "#60a5fa")
    ax.plot(monthly.index, monthly.values, color=color, linewidth=1.8, label="Monthly avg T2M")
    ax.fill_between(monthly.index, monthly.values, alpha=0.15, color=color)

    # Annotate extremes
    warmest = monthly.idxmax()
    coolest = monthly.idxmin()
    ax.annotate(f"Warmest\n{warmest.strftime('%b %Y')}\n{monthly[warmest]:.1f}°C",
                xy=(warmest, monthly[warmest]),
                xytext=(20, 12), textcoords="offset points",
                arrowprops=dict(arrowstyle="->", color="#f97316"),
                color="#f97316", fontsize=9)
    ax.annotate(f"Coolest\n{coolest.strftime('%b %Y')}\n{monthly[coolest]:.1f}°C",
                xy=(coolest, monthly[coolest]),
                xytext=(20, -20), textcoords="offset points",
                arrowprops=dict(arrowstyle="->", color="#38bdf8"),
                color="#38bdf8", fontsize=9)

    ax.set_title(f"{country} — Monthly Average Temperature (2015–2026)", fontweight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel("T2M (°C)")
    ax.grid(True)
    fig.tight_layout()
    return fig


def plot_monthly_precipitation(df: pd.DataFrame, country: str) -> plt.Figure:
    """
    Bar chart of monthly total precipitation with peak rainy season annotated.
    """
    set_style()
    monthly = df.groupby(df["Date"].dt.to_period("M"))["PRECTOTCORR"].sum()
    monthly.index = monthly.index.to_timestamp()

    fig, ax = plt.subplots(figsize=(14, 5))
    color = COUNTRY_COLORS.get(country, "#34d399")
    ax.bar(monthly.index, monthly.values, color=color, alpha=0.8, width=25)

    # Annotate top-3 rainy months
    top3 = monthly.nlargest(3)
    for date, val in top3.items():
        ax.annotate(f"{date.strftime('%b %Y')}\n{val:.0f} mm",
                    xy=(date, val),
                    xytext=(0, 8), textcoords="offset points",
                    ha="center", fontsize=8, color="#fde68a")

    ax.set_title(f"{country} — Monthly Total Precipitation (2015–2026)", fontweight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel("PRECTOTCORR (mm/month)")
    ax.grid(True, axis="y")
    fig.tight_layout()
    return fig


# ──────────────────────────────────────────────────────────────────────────────
# Correlation & Distribution
# ──────────────────────────────────────────────────────────────────────────────

def plot_correlation_heatmap(df: pd.DataFrame, country: str) -> plt.Figure:
    """Heatmap of Pearson correlations across all numeric columns."""
    set_style()
    numeric_cols = df.select_dtypes(include=np.number).drop(
        columns=["YEAR", "DOY", "Month"], errors="ignore"
    )
    corr = numeric_cols.corr()

    fig, ax = plt.subplots(figsize=(11, 9))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f",
                cmap="coolwarm", center=0, vmin=-1, vmax=1,
                linewidths=0.5, ax=ax, cbar_kws={"shrink": 0.8})
    ax.set_title(f"{country} — Correlation Heatmap", fontweight="bold")
    fig.tight_layout()
    return fig


def plot_scatter_t2m_rh2m(df: pd.DataFrame, country: str) -> plt.Figure:
    """Scatter plot of T2M vs RH2M."""
    set_style()
    color = COUNTRY_COLORS.get(country, "#a78bfa")
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(df["T2M"], df["RH2M"], alpha=0.3, s=10, color=color)
    ax.set_title(f"{country} — Temperature vs Relative Humidity", fontweight="bold")
    ax.set_xlabel("T2M (°C)")
    ax.set_ylabel("RH2M (%)")
    ax.grid(True)
    fig.tight_layout()
    return fig


def plot_precipitation_histogram(df: pd.DataFrame, country: str) -> plt.Figure:
    """Log-scale histogram of daily precipitation."""
    set_style()
    color = COUNTRY_COLORS.get(country, "#34d399")
    data = df["PRECTOTCORR"].dropna()
    data_nonzero = data[data > 0]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(np.log1p(data_nonzero), bins=60, color=color, alpha=0.8, edgecolor="#0f172a")
    ax.set_title(f"{country} — Precipitation Distribution (log scale)", fontweight="bold")
    ax.set_xlabel("log(1 + PRECTOTCORR)  [log mm/day]")
    ax.set_ylabel("Frequency")
    ax.grid(True, axis="y")
    fig.tight_layout()
    return fig


def plot_bubble_chart(df: pd.DataFrame, country: str) -> plt.Figure:
    """Bubble chart: T2M vs RH2M, bubble size = PRECTOTCORR."""
    set_style()
    color = COUNTRY_COLORS.get(country, "#fb923c")
    sample = df.sample(min(1000, len(df)), random_state=42)
    sizes = (sample["PRECTOTCORR"].fillna(0) + 1) * 8

    fig, ax = plt.subplots(figsize=(10, 7))
    sc = ax.scatter(sample["T2M"], sample["RH2M"],
                    s=sizes, alpha=0.5, c=sample["T2M"],
                    cmap="plasma", edgecolors="none")
    plt.colorbar(sc, ax=ax, label="T2M (°C)")
    ax.set_title(f"{country} — T2M vs RH2M (bubble = precipitation)", fontweight="bold")
    ax.set_xlabel("T2M (°C)")
    ax.set_ylabel("RH2M (%)")
    ax.grid(True)
    fig.tight_layout()
    return fig


# ──────────────────────────────────────────────────────────────────────────────
# Cross-Country Comparison
# ──────────────────────────────────────────────────────────────────────────────

def plot_multi_country_temperature(df_all: pd.DataFrame) -> plt.Figure:
    """
    Multi-line chart of monthly average T2M for all 5 countries (2015–2026).
    """
    set_style()
    fig, ax = plt.subplots(figsize=(16, 6))

    for country, group in df_all.groupby("Country"):
        monthly = group.groupby(group["Date"].dt.to_period("M"))["T2M"].mean()
        monthly.index = monthly.index.to_timestamp()
        color = COUNTRY_COLORS.get(country, "#ffffff")
        ax.plot(monthly.index, monthly.values, label=country,
                color=color, linewidth=1.8)

    ax.set_title("Monthly Average Temperature — All Countries (2015–2026)", fontweight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel("T2M (°C)")
    ax.legend(facecolor="#1e293b", edgecolor="#334155")
    ax.grid(True)
    fig.tight_layout()
    return fig


def plot_precipitation_boxplots(df_all: pd.DataFrame) -> plt.Figure:
    """Side-by-side boxplots of daily PRECTOTCORR for all countries."""
    set_style()
    fig, ax = plt.subplots(figsize=(12, 6))
    countries = df_all["Country"].unique()
    palette = {c: COUNTRY_COLORS.get(c, "#ffffff") for c in countries}
    sns.boxplot(data=df_all, x="Country", y="PRECTOTCORR",
                palette=palette, fliersize=2, linewidth=1.2, ax=ax)
    ax.set_title("Precipitation Variability — All Countries", fontweight="bold")
    ax.set_xlabel("Country")
    ax.set_ylabel("PRECTOTCORR (mm/day)")
    ax.set_yscale("symlog")
    ax.grid(True, axis="y")
    fig.tight_layout()
    return fig


def plot_extreme_heat_days(heat_counts: pd.DataFrame) -> plt.Figure:
    """Bar chart: number of days per year where T2M_MAX > 35°C."""
    set_style()
    fig, ax = plt.subplots(figsize=(13, 5))
    for country in heat_counts["Country"].unique():
        subset = heat_counts[heat_counts["Country"] == country]
        color = COUNTRY_COLORS.get(country, "#ffffff")
        ax.bar(subset["YEAR"].astype(str) + f"\n{country[:3]}",
               subset["extreme_heat_days"], color=color, label=country, alpha=0.85)
    ax.set_title("Extreme Heat Days (T2M_MAX > 35°C) per Year", fontweight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Days")
    ax.legend(facecolor="#1e293b", edgecolor="#334155")
    ax.grid(True, axis="y")
    fig.tight_layout()
    return fig
