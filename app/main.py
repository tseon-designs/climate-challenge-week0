"""
main.py — Streamlit Interactive Dashboard
EthioClimate Analytics — COP32 Climate Vulnerability Dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils import (
    COUNTRIES, COUNTRY_COLORS,
    load_all_countries, filter_data,
    temperature_trend_chart, precipitation_boxplot,
    extreme_heat_bar, summary_stats_table
)

# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EthioClimate Analytics — COP32",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Dark theme overrides */
    .stApp { background-color: #0f172a; color: #e2e8f0; }
    .stSidebar { background-color: #1e293b; }
    .metric-card {
        background: linear-gradient(135deg, #1e293b, #334155);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        border-left: 4px solid #E63946;
        margin-bottom: 0.5rem;
    }
    h1, h2, h3 { color: #f8fafc !important; }
    .stSelectbox label, .stMultiSelect label, .stSlider label {
        color: #94a3b8 !important;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .insight-box {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 1.5rem 0 0.5rem 0;'>
  <h1 style='font-size:2.2rem; background: linear-gradient(90deg, #E63946, #F4A261, #2A9D8F);
             -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
    🌍 EthioClimate Analytics
  </h1>
  <p style='color:#94a3b8; font-size:1.05rem; margin-top:-0.5rem;'>
    African Climate Vulnerability Dashboard — Supporting Ethiopia's COP32 Position
  </p>
</div>
""", unsafe_allow_html=True)
st.divider()

# ── Load Data ─────────────────────────────────────────────────────────────────
df_all = load_all_countries()

if df_all is None:
    st.error("""
    ⚠️ **No data files found.**

    Please place cleaned CSV files in the `data/` directory:
    - `data/ethiopia_clean.csv`
    - `data/kenya_clean.csv`
    - `data/sudan_clean.csv`
    - `data/tanzania_clean.csv`
    - `data/nigeria_clean.csv`

    Run the EDA notebooks first to generate these files.
    """)
    st.stop()

# ── Sidebar Controls ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎛️ Dashboard Controls")
    st.markdown("---")

    selected_countries = st.multiselect(
        "Country Selector",
        options=COUNTRIES,
        default=COUNTRIES,
        help="Select one or more countries to compare"
    )

    year_min = int(df_all["YEAR"].min())
    year_max = int(df_all["YEAR"].max())
    year_range = st.slider(
        "Year Range",
        min_value=year_min,
        max_value=year_max,
        value=(year_min, year_max),
        step=1,
        help="Zoom into a specific time period"
    )

    variable_map = {
        "Mean Temperature (T2M)": "T2M",
        "Max Temperature (T2M_MAX)": "T2M_MAX",
        "Min Temperature (T2M_MIN)": "T2M_MIN",
        "Diurnal Range (T2M_RANGE)": "T2M_RANGE",
        "Relative Humidity (RH2M)": "RH2M",
        "Wind Speed (WS2M)": "WS2M",
        "Specific Humidity (QV2M)": "QV2M",
    }
    selected_var_label = st.selectbox(
        "Variable Selector",
        options=list(variable_map.keys()),
        index=0,
        help="Select the climate variable to visualize"
    )
    selected_var = variable_map[selected_var_label]

    st.markdown("---")
    st.markdown("""
    <div style='color:#64748b; font-size:0.78rem; line-height:1.6;'>
    📡 Data: NASA POWER (2015–2026)<br>
    🗺️ Countries: 5 African nations<br>
    📅 Frequency: Daily observations<br>
    🎯 Purpose: COP32 Position Paper
    </div>
    """, unsafe_allow_html=True)

# ── Filter Data ───────────────────────────────────────────────────────────────
if not selected_countries:
    st.warning("Please select at least one country from the sidebar.")
    st.stop()

df_filtered = filter_data(df_all, selected_countries, year_range)

# ── KPI Metrics Row ───────────────────────────────────────────────────────────
st.markdown("### 📊 Key Metrics")
cols = st.columns(4)

with cols[0]:
    avg_temp = df_filtered["T2M"].mean()
    st.metric("Avg Temperature", f"{avg_temp:.1f} °C", delta=None)

with cols[1]:
    total_days = len(df_filtered)
    st.metric("Total Observations", f"{total_days:,}")

with cols[2]:
    extreme_heat = (df_filtered["T2M_MAX"] > 35).sum()
    st.metric("Extreme Heat Days (>35°C)", f"{extreme_heat:,}")

with cols[3]:
    dry_days = (df_filtered["PRECTOTCORR"] < 1).sum()
    dry_pct = dry_days / total_days * 100
    st.metric("Dry Days (<1mm)", f"{dry_days:,} ({dry_pct:.0f}%)")

st.divider()

# ── Temperature Trend Chart ───────────────────────────────────────────────────
st.markdown(f"### 📈 {selected_var_label} — Monthly Trend (2015–{year_range[1]})")
fig_temp = temperature_trend_chart(df_filtered, selected_var)
st.plotly_chart(fig_temp, use_container_width=True)

# ── Two-Column: Boxplot + Heat Days ──────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🌧️ Precipitation Distribution")
    fig_precip = precipitation_boxplot(df_filtered)
    st.plotly_chart(fig_precip, use_container_width=True)

with col2:
    st.markdown("### 🔥 Extreme Heat Days per Year")
    fig_heat = extreme_heat_bar(df_filtered)
    st.plotly_chart(fig_heat, use_container_width=True)

st.divider()

# ── Summary Statistics Tables ─────────────────────────────────────────────────
st.markdown("### 📋 Summary Statistics")
tab1, tab2 = st.tabs(["🌡️ Temperature", "🌧️ Precipitation"])

with tab1:
    temp_stats = summary_stats_table(df_filtered, "T2M")
    st.dataframe(temp_stats, use_container_width=True, hide_index=True)

with tab2:
    precip_stats = summary_stats_table(df_filtered, "PRECTOTCORR")
    st.dataframe(precip_stats, use_container_width=True, hide_index=True)

st.divider()

# ── COP32 Insight Panel ───────────────────────────────────────────────────────
st.markdown("### 🎯 COP32 Negotiation-Grade Insights")
st.markdown("""
<div class='insight-box'>
<b style='color:#E63946;'>Layer 1 — What is changing?</b><br>
Mean temperature across all selected countries is <b>{:.1f}°C</b>, observed over {:,} daily records from {} to {}.
</div>
<div class='insight-box'>
<b style='color:#F4A261;'>Layer 2 — What did it cause?</b><br>
<b>{:,}</b> extreme heat days (T2M_MAX > 35°C) were recorded — each one a day when outdoor labor becomes 
physiologically dangerous and crop transpiration stress reaches critical levels.
</div>
<div class='insight-box'>
<b style='color:#2A9D8F;'>Layer 3 — What does it demand?</b><br>
The data supports an urgent policy ask for <b>adaptation finance, early warning systems, and loss & damage 
mechanisms</b> aligned with the Bridgetown Initiative and Africa's Addis Ababa Declaration for COP32.
</div>
""".format(
    avg_temp,
    total_days,
    year_range[0],
    year_range[1],
    extreme_heat
), unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#475569; font-size:0.8rem;'>
EthioClimate Analytics | Built for COP32 — Addis Ababa 2027 | 
Data: NASA POWER | Dashboard: Streamlit + Plotly
</div>
""", unsafe_allow_html=True)
