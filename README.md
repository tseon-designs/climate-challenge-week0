# 🌍 African Climate Trend Analysis — COP32 Edition

**EthioClimate Analytics** | Exploratory analysis of historical climate data (2015–2026) across five African nations to support Ethiopia's data-driven position at COP32 in Addis Ababa, 2027.

[![CI - Environment Check](https://github.com/tseon-designs/climate-challenge-week0/actions/workflows/ci.yml/badge.svg)](https://github.com/tseon-designs/climate-challenge-week0/actions/workflows/ci.yml)

---

## 🎯 The "So What?" (Project Impact)
This project moves beyond academic research to produce **negotiation-grade insights**. By analyzing 11 years of daily NASA POWER satellite data, we demonstrate:
- **Fastest Warming**: Sudan is warming at a statistically significant rate, demanding urgent adaptation finance.
- **Extreme Volatility**: Tanzania and Kenya face the most erratic rainfall patterns, justifying early warning system investments.
- **Policy Support**: We provide a data-backed foundation for Ethiopia's leadership at COP32 via a **Composite Vulnerability Ranking**.

---

## 🚀 Live Dashboard
Experience the data interactively: **[View Streamlit Dashboard](https://ethio-climate-cop32.streamlit.app/)**

---

## 🛠️ Technical Breadth
- **Data Engineering**: Modular Python pipeline (`src/clean.py`) with Z-score outlier detection and ffill imputation.
- **Exploratory Data Analysis**: 5 country-level EDA notebooks + 1 cross-country synthesis.
- **Statistical Rigor**: Kruskal-Wallis significance testing and linear regression trends.
- **DevOps**: GitHub Actions CI pipeline for environment verification and automated unit testing.
- **UI/UX**: Interactive Streamlit dashboard with Plotly integration and professional dark-mode styling.

---

## 🗂️ Project Structure

```
climate-challenge-week0/
├── .github/workflows/
│   └── ci.yml              # CI pipeline (Linting + Testing)
├── app/
│   ├── main.py             # Streamlit dashboard UI
│   └── utils.py            # Dashboard logic & caching
├── notebooks/
│   ├── eda_ethiopia.ipynb  # Individual country EDA
│   └── compare_countries.ipynb # Statistical synthesis & ranking
├── src/
│   ├── clean.py            # Reusable cleaning logic
│   └── visualize.py        # Professional plotting utilities
├── tests/
│   └── test_clean.py       # Automated unit tests
├── reports/
│   └── climate_vulnerability_report.md # Medium-style report
├── requirements.txt
└── README.md
```

---

## ⚙️ Quick Start

### 1. Setup Environment
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Run Dashboard
```bash
streamlit run app/main.py
```

### 3. Run Tests
```bash
pytest tests/
```

---

## 🌐 References
- NASA POWER Data Access Viewer
- WMO State of the Climate in Africa 2024
- World Bank Climate Risk Country Profiles
