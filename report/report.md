# Intelligent Blood Supply Management
## Demand Forecasting, Donor Segmentation & Recommender System

---

## 1. Problem Background

Blood transfusion is life-saving with no synthetic substitute. Blood banks face a dual challenge:
- **Shortage Risk**: Unpredictable demand spikes cause critical shortages
- **Wastage Risk**: Perishable components (platelets: 5 days, RBCs: 42 days)

**NBCUS 2019**: 13M donors, 10.8M RBC units transfused, 5-15% wastage. **Nepal BPKIHS**: 7.13% wastage.

| Objective | Technique | Target |
|-----------|-----------|--------|
| Demand Forecasting | SARIMA, Prophet, ML | MAPE < 20% |
| Donor Segmentation | RFM + K-Means | Silhouette > 0.35 |
| Recommender System | Hybrid Scoring | Beat random |
| Anomaly Detection | Z-score | Detect spikes |

---

## 2. Dataset Description

| Dataset | Records | Type | Source |
|---------|---------|------|--------|
| UCI Blood Transfusion | 748 | Real | UCI ML Repository |
| Kaggle Blood Demand/Donor | - | Real | Kaggle |
| Synthetic Donor Registry | 10,000 | Synthetic | NBCUS 2019 |
| Demand Time-Series | 4,380 | Synthetic | 3 years daily |

**Synthetic data based on:** WHO blood types (O+: 37%, A+: 28%, B+: 20%, O-: 6%), NBCUS demographics (30% first-time, 54% male), 15% deferral rate.

---

## 3. Methodology

### 3.1 Demand Forecasting

| Model | Configuration |
|-------|---------------|
| SARIMA | (1,1,1)(1,1,1,7) |
| Prophet | Weekly + yearly seasonality |
| Random Forest | 100 trees, depth=10 |
| Gradient Boosting | 100 estimators |

**Features:** lag_1, lag_7, rolling_mean_7/14/30, day_of_week, is_weekend

### 3.2 Donor Segmentation (RFM + K-Means)

- **Recency**: Months since last donation
- **Frequency**: Total donations
- **Monetary**: Total volume donated

### 3.3 Hybrid Recommender System

```
Score = 0.4×RFM + 0.2×Availability + 0.2×Segment + 0.1×Blood + 0.1×Urgency
```

### 3.4 Anomaly Detection

Rolling Z-score (window=30, threshold=2.5σ)

---

## 4. Results

### 4.1 Forecasting Performance

| Model | MAE | MAPE | R² |
|-------|-----|------|-----|
| **Random Forest** | **19.68** | **12.14%** | **0.45** |
| SARIMA | 22.19 | 12.40% | 0.20 |
| Gradient Boosting | 22.11 | 13.75% | 0.28 |

**Patterns:** 30% lower weekends, +15% winter peak, +20-25% holidays

### 4.2 Segmentation Results

**Silhouette: 0.41** (Target: >0.35) ✓

| Segment | % | Strategy |
|---------|---|----------|
| Champions | 11.5% | Retain & Reward |
| Loyal | 22.3% | Referral Programs |
| Potential | 28.5% | Nurture & Convert |
| At Risk | 19.6% | Urgent Reactivation |
| Hibernating | 18.1% | Last-chance Campaign |

### 4.3 Recommender Results

| Campaign | Target | Urgency |
|----------|--------|---------|
| Winter Blood Drive | Champions, Loyal | High |
| O-Negative Emergency | All eligible | Critical |
| Platelet Week | Champions | High |
| Summer Stock | Potential | Medium |
| Lapsed Reactivation | At Risk | Medium |

**Simulation (100 donors, 5 campaigns):**

| Strategy | Donations | Improvement |
|----------|-----------|-------------|
| Random | ~45 | baseline |
| RFM-based | ~58 | +29% |
| **Hybrid** | **~66** | **+47%** |

---

## 5. Business Insights

| Pattern | Finding | Action |
|---------|---------|--------|
| Weekly | 30% lower weekends | Reduce weekend drives |
| Winter | +15% (Dec-Feb) | Pre-stock November |
| Holidays | +20-25% spikes | Emergency reserves |

**Inventory:** Platelets (12.3% wastage) → Just-in-time; Packed RBC (5.2%) → 7-day buffer; O-negative → Priority collection

**Projected Impact:** Wastage 8.8%→5% (~$150K savings), +47% donor yield with recommender

---

## 6. Limitations & Future

**Limitations:** Synthetic data needs real validation; emergencies unpredictable; external factors not modeled

**Future:** Deep Learning (LSTM), Reinforcement Learning, IoT monitoring, Multi-center optimization

---

## 7. Conclusion

| Objective | Target | Achieved |
|-----------|--------|----------|
| Forecasting | MAPE < 20% | **12.14%** ✓ |
| Segmentation | Silhouette > 0.35 | **0.41** ✓ |
| Recommender | Beat random | **+47%** ✓ |

> *"Advanced ML is about discovering structure, extracting insights, and supporting decision-making in complex data."*

---

## References

1. NBCUS (2019). National Blood Collection Survey. US DHHS.
2. Singh et al. (2023). Blood wastage at BPKIHS. J Pathology Nepal.
3. UCI ML Repository. Blood Transfusion Dataset.
4. WHO. Blood Safety Fact Sheet.
5. Kaggle. Blood Demand & Donor Datasets.

*Code: 5 notebooks | Data: Google Drive*
