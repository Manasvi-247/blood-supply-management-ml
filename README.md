# Intelligent Blood Supply Management

**Demand Forecasting and Donor Segmentation for Inventory Optimization**

Team: **IDGAF** (Section A & B)

---

## Project Overview

This project addresses the critical challenge of blood shortage and wastage in healthcare through:

1. **Demand Forecasting** - Predicting blood demand using time-series analysis (SARIMA, Prophet, ML)
2. **Donor Segmentation** - Clustering donors using RFM metrics (K-Means)
3. **Recommender System** - Donor-Campaign matching for targeted outreach
4. **Anomaly Detection** - Change point detection in demand patterns

### Key Results

| Metric | Target | Achieved |
|--------|--------|----------|
| Forecast MAPE | <20% | ✓ |
| Silhouette Score | >0.35 | ✓ |

---

## Folder Structure

```
blood-supply-management/
├── data/
│   ├── uci_transfusion.csv      # UCI real dataset (748 records)
│   ├── donor_registry.csv       # Synthetic donors (10K records)
│   ├── rfm_dataset.csv          # RFM features for segmentation
│   ├── demand_daily.csv         # Daily demand time-series
│   ├── demand_detailed.csv      # Demand by blood type
│   └── supply_inventory.csv     # Supply and wastage data
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_demand_forecasting.ipynb
│   ├── 03_donor_segmentation.ipynb
│   ├── 04_insights_recommendations.ipynb
│   └── 05_recommender_system.ipynb
├── src/
│   ├── utils.py                 # Helper functions
│   └── generate_datasets.py     # Data generation script
├── report/
│   └── (generated figures)
├── requirements.txt
└── README.md
```

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- Jupyter Notebook/Lab

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Required Libraries
- pandas, numpy
- matplotlib, seaborn, plotly
- scikit-learn
- statsmodels
- prophet (optional, for Prophet forecasting)
- faker (for data generation)

---

## How to Run

### 1. Generate Synthetic Data (if not present)

```bash
python src/generate_datasets.py
```

This creates realistic synthetic datasets based on:
- NBCUS 2019 Survey statistics
- WHO blood type distributions
- Nepal BPKIHS wastage study

### 2. Run Notebooks in Order

1. **01_data_exploration.ipynb** - Understand all datasets
2. **02_demand_forecasting.ipynb** - Train SARIMA, Prophet, ML models
3. **03_donor_segmentation.ipynb** - RFM analysis and clustering
4. **04_insights_recommendations.ipynb** - Business insights
5. **05_recommender_system.ipynb** - Donor-Campaign recommender + anomaly detection

```bash
jupyter notebook notebooks/
```

---

## Datasets

### 1. UCI Blood Transfusion Dataset (Real Data)
- **Source:** UCI ML Repository
- **Records:** 748
- **Features:** Recency, Frequency, Monetary, Time, Donated (target)

### 2. Synthetic Donor Registry
- **Records:** 10,000
- **Features:** Demographics, donation history, blood type, deferral history
- **Based on:** NBCUS 2019 statistics

### 3. Demand Time-Series
- **Period:** 3 years (2021-2023)
- **Granularity:** Daily
- **Components:** Packed RBC, Platelets, FFP, Cryoprecipitate
- **Patterns:** Weekly, seasonal, holiday effects

---

## Methodology

### Demand Forecasting
- **SARIMA** - Seasonal ARIMA for time-series decomposition
- **Prophet** - Facebook's forecasting with automatic seasonality
- **Random Forest** - Feature-based ML with lag/rolling features
- **Gradient Boosting** - Ensemble method for demand prediction

### Donor Segmentation
- **RFM Scoring** - Quintile-based scoring (1-5)
- **K-Means Clustering** - Optimal K via elbow/silhouette
- **Segment Labels:** Champions, Loyal, Potential, At-Risk, Hibernating, New

### Recommender System
- **Hybrid Approach** - Rule-based filtering + weighted scoring
- **Donor-Campaign Matching** - Match donors to blood drives based on RFM, blood type, availability
- **Change Point Detection** - Rolling Z-score for demand anomalies

---

## Key Findings

### Demand Patterns
- **Weekend Effect:** ~30% lower demand (reduced elective surgeries)
- **Winter Peak:** +15% demand (Dec-Feb: accidents, flu season)
- **Holiday Spikes:** Diwali, Christmas/New Year periods

### Inventory Performance
- **Benchmark:** 92.9% utilization, 7.1% wastage (Nepal BPKIHS)
- **Platelets:** Highest wastage risk (5-day shelf life)
- **Packed RBC:** Most demanded component (~55%)

### Donor Segments
- **Champions:** High frequency, recent donors - retain & reward
- **At-Risk:** Previously active, now lapsed - urgent reactivation
- **New Donors:** First-time donors - onboarding & education

---

## Business Recommendations

1. **Deploy ML forecasting** for 7-14 day predictions
2. **Pre-stock before winter** (+15% buffer Dec-Feb)
3. **Just-in-time ordering** for platelets (5-day expiry)
4. **Targeted outreach** based on RFM segments
5. **Prioritize O-negative** collection (universal donor, only 6% of pool)

---

## References

1. NBCUS 2019 - National Blood Collection and Utilization Survey
2. Nepal BPKIHS Study - Blood component utilization and wastage
3. UCI ML Repository - Blood Transfusion Service Center Dataset
4. WHO Blood Type Distribution Standards

---

## Team

| Name | Roll Number |
|------|-------------|
| Jasleen (Leader) | 10045 |
| Manasvi | 10406 |
| Akshat | 10060 |
| Ankita | 10062 |
| Antara | 10106 |

---

## License

This project is for educational purposes as part of the Advanced ML course.

---

*"Advanced ML is not about prediction accuracy alone. It is about discovering structure, extracting insights, and supporting decision-making in complex data."*
