# 🌍 African Climate Trend Analysis — COP32 Edition

**EthioClimate Analytics** | Exploratory analysis of historical climate data across five African nations to support Ethiopia's data-driven position at COP32 in Addis Ababa, 2027.

[![CI](https://github.com/YOUR_USERNAME/climate-challenge-week0/actions/workflows/unittests.yml/badge.svg)](https://github.com/YOUR_USERNAME/climate-challenge-week0/actions/workflows/unittests.yml)

---

## 📋 Project Overview

This project analyzes NASA POWER satellite-derived climate data (2015–2026) for:
- 🇪🇹 Ethiopia
- 🇰🇪 Kenya
- 🇸🇩 Sudan
- 🇹🇿 Tanzania
- 🇳🇬 Nigeria

The goal is to produce **negotiation-grade insights** — evidence that answers:
1. **What is changing?** (trend + baseline + uncertainty)
2. **What did it cause?** (impact stat — yields, displacement, GDP)
3. **What does it demand?** (the policy/finance ask)

---

## 🗂️ Project Structure

```
climate-challenge-week0/
├── .github/
│   └── workflows/
│       └── unittests.yml       # CI pipeline
├── .vscode/
│   └── settings.json
├── app/
│   ├── __init__.py
│   ├── main.py                 # Streamlit dashboard
│   └── utils.py                # Utility functions
├── data/                       # ⚠️ IGNORED — place CSV files here
├── notebooks/
│   ├── __init__.py
│   ├── eda_ethiopia.ipynb
│   ├── eda_kenya.ipynb
│   ├── eda_sudan.ipynb
│   ├── eda_tanzania.ipynb
│   ├── eda_nigeria.ipynb
│   └── compare_countries.ipynb
├── scripts/
│   ├── __init__.py
│   └── README.md
├── src/
│   ├── __init__.py
│   ├── clean.py                # Reusable cleaning functions
│   └── visualize.py            # Reusable plotting functions
├── tests/
│   └── __init__.py
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Environment Setup

### Prerequisites
- Python 3.10+
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/climate-challenge-week0.git
cd climate-challenge-week0
```

### 2. Create a Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Add Data Files
Place the NASA POWER CSV files in the `data/` directory:
```
data/
├── ethiopia.csv
├── kenya.csv
├── sudan.csv
├── tanzania.csv
└── nigeria.csv
```
> ⚠️ **Never commit data files to GitHub.** The `data/` folder is in `.gitignore`.

### 5. Run Notebooks
```bash
jupyter notebook notebooks/
```

### 6. Run the Streamlit Dashboard
```bash
streamlit run app/main.py
```

---

## 📊 Dataset

**Source:** NASA Prediction of Worldwide Energy Resources (NASA POWER)
**Period:** January 2015 – March 2026
**Frequency:** Daily

| Column | Unit | Description |
|--------|------|-------------|
| YEAR | — | Year of observation |
| DOY | — | Day of year (1–365/366) |
| T2M | °C | Mean daily air temperature at 2m |
| T2M_MAX | °C | Maximum daily temperature at 2m |
| T2M_MIN | °C | Minimum daily temperature at 2m |
| T2M_RANGE | °C | Daily temperature range |
| PRECTOTCORR | mm/day | Bias-corrected total daily precipitation |
| RH2M | % | Relative humidity at 2m |
| WS2M | m/s | Mean daily wind speed at 2m |
| WS2M_MAX | m/s | Maximum daily wind speed at 2m |
| PS | kPa | Atmospheric surface pressure |
| QV2M | g/kg | Specific humidity |

---

## 🌐 References
- [NASA POWER Data Access Viewer](https://power.larc.nasa.gov/data-access-viewer/)
- [WMO State of the Climate in Africa 2024](https://wmo.int/publication-series/state-of-climate-africa-2024)
- [World Bank Climate Risk Country Profiles](https://climateknowledgeportal.worldbank.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
