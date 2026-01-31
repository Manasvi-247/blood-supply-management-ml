# Data Sources

## Google Drive Link
**[INSERT YOUR GOOGLE DRIVE LINK HERE]**

Upload the following files to Google Drive and paste the link above.

---

## Datasets Included

### 1. UCI Blood Transfusion Dataset (`uci_transfusion.csv`)
- **Source:** [UCI ML Repository](https://archive.ics.uci.edu/dataset/176/blood+transfusion+service+center)
- **Records:** 748
- **Description:** Real donor data from Taiwan blood bank

| Column | Description |
|--------|-------------|
| Recency | Months since last donation |
| Frequency | Total number of donations |
| Monetary | Total blood donated (cc) |
| Time | Months since first donation |
| Donated | Target: donated in March 2007 |

### 2. Synthetic Donor Registry (`donor_registry.csv`)
- **Records:** 10,000
- **Based on:** NBCUS 2019 statistics, WHO blood type distributions

| Column | Description |
|--------|-------------|
| donor_id | Unique identifier |
| name, email, phone | Contact info |
| age, gender | Demographics |
| blood_type | ABO/Rh type |
| city | Location |
| registration_date | First registration |
| last_donation_date | Most recent donation |
| total_donations | Lifetime donation count |
| total_volume_cc | Lifetime volume donated |
| availability_status | Current eligibility |
| is_first_time_donor | Boolean |
| has_deferral_history | Boolean |
| deferral_reason | If applicable |

### 3. RFM Dataset (`rfm_dataset.csv`)
- **Records:** 10,000
- **Derived from:** Donor registry

| Column | Description |
|--------|-------------|
| donor_id | Unique identifier |
| Recency | Months since last donation |
| Frequency | Total donations |
| Monetary | Total volume (cc) |
| Time | Months since first donation |
| donated_last_quarter | Target variable |

### 4. Demand Time-Series (`demand_daily.csv`)
- **Period:** 2021-01-01 to 2023-12-31
- **Records:** 4,380 (daily by component)

| Column | Description |
|--------|-------------|
| date | Date |
| component | Blood component type |
| demand_units | Daily demand |
| day_of_week | 0=Mon, 6=Sun |
| month | 1-12 |
| is_weekend | Boolean |
| is_holiday_season | Nov-Dec flag |

### 5. Detailed Demand (`demand_detailed.csv`)
- **Records:** 35,040
- **Granularity:** Daily by component by blood type

### 6. Supply Inventory (`supply_inventory.csv`)
- **Records:** 4,380

| Column | Description |
|--------|-------------|
| date | Date |
| component | Blood component |
| supply_units | Units available |
| demand_units | Units demanded |
| utilized_units | Units used |
| wasted_units | Units expired/wasted |
| utilization_rate | % utilized |
| wastage_rate | % wasted |

---

## Data Generation

Synthetic data was generated using statistics from:
1. **NBCUS 2019** - US blood collection survey
2. **Nepal BPKIHS Study** - Wastage rates
3. **WHO Standards** - Blood type distributions

To regenerate:
```bash
python src/generate_datasets.py
```
