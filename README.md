# Intelligent Blood Supply Management

**Demand Forecasting, Donor Segmentation & Recommender System for Inventory Optimization**

Team: **IDGAF** | Section: A & B

---

## Project Overview

This project addresses the critical challenge of **blood shortage and wastage** in healthcare through advanced ML techniques:

| Component | Technique | Domain |
|-----------|-----------|--------|
| **Demand Forecasting** | SARIMA, Prophet, Random Forest, Gradient Boosting | Time Series |
| **Donor Segmentation** | RFM Analysis, K-Means Clustering | Unsupervised Learning |
| **Recommender System** | Hybrid Donor-Campaign Matching | Recommender Systems |
| **Anomaly Detection** | Change Point Detection (Z-score) | Unsupervised Learning |

---

## Key Results

| Metric | Target | Achieved |
|--------|--------|----------|
| Forecast MAPE | <20% | **12.14%** |
| Silhouette Score | >0.35 | **0.41** |
| Recommender Improvement | - | **+47%** vs random |

---

## Folder Structure

```
blood-supply-management/
├── data/
│   ├── uci_transfusion.csv          # UCI real dataset (748 records)
│   ├── donor_registry.csv           # Synthetic donors (10K records)
│   ├── rfm_dataset.csv              # RFM features
│   ├── demand_daily.csv             # Daily demand (3 years)
│   ├── demand_detailed.csv          # Demand by blood type
│   ├── supply_inventory.csv         # Supply and wastage
│   ├── donor_segments.csv           # Segmented donors
│   ├── recommendations_C001-C005.csv # Campaign recommendations
│   └── campaign_metrics.csv         # Campaign performance
├── notebooks/
│   ├── 01_data_exploration.ipynb    # EDA & visualization
│   ├── 02_demand_forecasting.ipynb  # SARIMA, Prophet, ML models
│   ├── 03_donor_segmentation.ipynb  # RFM + K-Means clustering
│   ├── 04_insights_recommendations.ipynb  # Business insights
│   └── 05_recommender_system.ipynb  # Donor-Campaign recommender
├── src/
│   ├── utils.py                     # Helper functions
│   └── generate_datasets.py         # Synthetic data generation
├── report/
│   ├── report.pdf                   # Final report (9 pages)
│   └── *.png                        # 27 visualizations
├── requirements.txt
└── README.md
```

---

## Installation & Setup

```bash
# Clone repository
git clone https://github.com/Manasvi-247/blood-supply-management-ml.git
cd blood-supply-management-ml

# Install dependencies
pip install -r requirements.txt

# Run notebooks
jupyter lab notebooks/
```

### Requirements
- Python 3.8+
- pandas, numpy, matplotlib, seaborn
- scikit-learn, statsmodels
- prophet (optional)

---

## Datasets

| Dataset | Records | Type | Source |
|---------|---------|------|--------|
| UCI Blood Transfusion | 748 | Real | UCI ML Repository |
| Donor Registry | 10,000 | Synthetic | NBCUS 2019 stats |
| Demand Time-Series | 4,380 | Synthetic | 3 years daily |
| Supply/Inventory | 4,380 | Synthetic | Nepal BPKIHS study |

**Data Generation Based On:**
- NBCUS 2019 Survey (US blood collection statistics)
- WHO blood type distributions
- Nepal BPKIHS wastage study (7.1% benchmark)

---

## Methodology

### 1. Time Series Forecasting

| Model | MAPE | R² |
|-------|------|-----|
| **Random Forest** | **12.14%** | **0.45** |
| SARIMA | 12.40% | 0.20 |
| Gradient Boosting | 13.75% | 0.28 |

**Key Features:** lag_1, rolling_mean_7, day_of_week, seasonal patterns

### 2. Donor Segmentation (Unsupervised)

| Segment | % of Donors | Strategy |
|---------|-------------|----------|
| Champions | 11.5% | Retain & Reward |
| Loyal | 22.3% | Referral Programs |
| Potential | 28.5% | Nurture & Convert |
| At Risk | 19.6% | Urgent Reactivation |
| Hibernating | 18.1% | Last-chance Campaign |

**Clustering:** K-Means with Silhouette Score = 0.41

### 3. Recommender System (Hybrid)

```
Score = 0.4×RFM + 0.2×Availability + 0.2×Segment_Match + 0.1×Blood_Match + 0.1×Urgency
```

**Campaigns Generated:**
- Winter Blood Drive (high demand)
- O-Negative Emergency (critical shortage)
- Platelet Donation Week
- Summer Stock Building
- Lapsed Donor Reactivation

### 4. Anomaly Detection

- **Method:** Rolling Z-score (window=30, threshold=2.5σ)
- **Purpose:** Detect demand spikes and operational disruptions

---

## Key Findings

### Demand Patterns
- **Weekend Effect:** 30% lower demand (reduced surgeries)
- **Winter Peak:** +15% demand (Dec-Feb)
- **Holiday Spikes:** +20-25% (Diwali, Christmas)

### Simulation Results
| Strategy | Avg Donations | Improvement |
|----------|---------------|-------------|
| Random | ~45 | baseline |
| RFM-based | ~58 | +29% |
| Recommender | ~66 | +47% |

---

## Business Recommendations

1. **Deploy ML forecasting** for 7-14 day demand predictions
2. **Pre-stock before winter** (+15% buffer in Nov)
3. **Just-in-time for platelets** (5-day shelf life)
4. **Targeted outreach** using recommender system (+47% yield)
5. **Prioritize O-negative** collection (universal donor, only 6%)

---

## References

1. NBCUS (2019). National Blood Collection and Utilization Survey
2. Singh et al. (2023). Blood component wastage at BPKIHS. J Pathology Nepal
3. UCI ML Repository. Blood Transfusion Service Center Dataset
4. WHO. Blood Safety and Availability Fact Sheet

---

## Team

| Name | Roll Number |
|------|-------------|
| Jasleen | 10045 |
| Manasvi | 10406 |
| Akshat | 10060 |
| Ankita | 10062 |
| Antara | 10106 |

---

## License

Educational project for Advanced ML Course.

---

> *"Advanced ML is not about prediction accuracy alone. It is about discovering structure, extracting insights, and supporting decision-making in complex data."*
