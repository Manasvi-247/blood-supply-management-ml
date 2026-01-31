"""
Synthetic Dataset Generator for Blood Supply Management Project
Team: IDGAF

Generates realistic synthetic datasets based on:
- NBCUS 2019 Survey (US blood collection statistics)
- Nepal BPKIHS Study (wastage and utilization rates)
- WHO blood type distributions
- UCI Blood Transfusion RFM patterns
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker
import random
import os

# Set seeds for reproducibility
np.random.seed(42)
random.seed(42)
fake = Faker()
Faker.seed(42)

# =============================================================================
# CONSTANTS FROM RESEARCH PAPERS
# =============================================================================

BLOOD_TYPE_DISTRIBUTION = {
    'O+': 0.37, 'A+': 0.28, 'B+': 0.20, 'AB+': 0.05,
    'O-': 0.06, 'A-': 0.025, 'B-': 0.015, 'AB-': 0.01
}  # Sums to 1.0

AGE_GROUP_RANGES = {
    '16-18': (16, 18, 0.08),
    '19-24': (19, 24, 0.15),
    '25-34': (25, 34, 0.22),
    '35-44': (35, 44, 0.18),
    '45-54': (45, 54, 0.17),
    '55-64': (55, 64, 0.12),
    '65+': (65, 75, 0.08)
}

CITIES = [
    'Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata',
    'Hyderabad', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow',
    'Chandigarh', 'Bhopal', 'Indore', 'Nagpur', 'Kochi'
]

DEFERRAL_REASONS = {
    'Low hemoglobin': 0.431,
    'Non-medical reasons': 0.214,
    'Blood pressure/pulse': 0.112,
    'Travel history': 0.089,
    'Medication': 0.072,
    'Recent tattoo/piercing': 0.045,
    'Other medical': 0.037
}


def generate_demand_timeseries(start_date='2021-01-01', periods=1095, freq='D'):
    """
    Generate synthetic blood demand time-series data.

    Features:
    - Daily demand for different blood components
    - Seasonal patterns (summer low, winter high, holiday spikes)
    - Weekly patterns (lower weekends)
    - Random emergency spikes
    - Blood type specific demand

    Based on NBCUS 2019: ~30,000 units/day national average
    Scaled to regional blood bank: ~50-200 units/day
    """
    print("Generating demand time-series dataset...")

    dates = pd.date_range(start=start_date, periods=periods, freq=freq)
    data = []

    base_demand = {
        'Packed RBC': 80,
        'Platelets': 30,
        'Fresh Frozen Plasma': 25,
        'Cryoprecipitate': 10
    }

    for date in dates:
        day_of_week = date.dayofweek
        month = date.month
        day = date.day

        for component, base in base_demand.items():
            # Base demand with noise
            demand = base + np.random.normal(0, base * 0.15)

            # Weekly pattern: lower on weekends (elective surgeries down)
            if day_of_week >= 5:
                demand *= 0.7

            # Seasonal pattern
            # Summer (Jun-Aug): lower donations, slightly higher demand
            if month in [6, 7, 8]:
                demand *= 1.1

            # Winter (Dec-Feb): holiday accidents, flu season
            if month in [12, 1, 2]:
                demand *= 1.15

            # Holiday spikes (accidents)
            if (month == 12 and day >= 20) or (month == 1 and day <= 5):
                demand *= 1.25

            # Diwali period (Oct-Nov) - accidents
            if month in [10, 11] and 15 <= day <= 30:
                demand *= 1.2

            # Random emergency spikes (accidents, disasters) - 2% chance
            if np.random.random() < 0.02:
                demand *= np.random.uniform(1.5, 2.5)

            # Ensure positive demand
            demand = max(1, int(demand))

            # Blood type breakdown for this demand
            for blood_type, proportion in BLOOD_TYPE_DISTRIBUTION.items():
                type_demand = max(1, int(demand * proportion + np.random.normal(0, 1)))

                data.append({
                    'date': date,
                    'component': component,
                    'blood_type': blood_type,
                    'demand_units': type_demand,
                    'day_of_week': day_of_week,
                    'month': month,
                    'is_weekend': 1 if day_of_week >= 5 else 0,
                    'is_holiday_season': 1 if month in [11, 12] else 0
                })

    df = pd.DataFrame(data)

    # Aggregate to daily totals by component
    df_daily = df.groupby(['date', 'component']).agg({
        'demand_units': 'sum',
        'day_of_week': 'first',
        'month': 'first',
        'is_weekend': 'first',
        'is_holiday_season': 'first'
    }).reset_index()

    print(f"  Generated {len(df)} detailed records, {len(df_daily)} daily aggregates")
    return df, df_daily


def generate_donor_registry(n_donors=10000):
    """
    Generate synthetic donor registry with realistic distributions.

    Based on:
    - NBCUS 2019 demographics
    - WHO blood type distributions
    - RFM patterns from UCI dataset
    """
    print(f"Generating donor registry with {n_donors} records...")

    donors = []

    for i in range(n_donors):
        # Generate age based on NBCUS distribution
        age_group = np.random.choice(
            list(AGE_GROUP_RANGES.keys()),
            p=[v[2] for v in AGE_GROUP_RANGES.values()]
        )
        age_min, age_max, _ = AGE_GROUP_RANGES[age_group]
        age = np.random.randint(age_min, age_max + 1)

        # Gender (NBCUS: 54% male donors)
        gender = np.random.choice(['Male', 'Female'], p=[0.54, 0.46])

        # Blood type (normalize probabilities to avoid floating point issues)
        bt_probs = np.array(list(BLOOD_TYPE_DISTRIBUTION.values()))
        bt_probs = bt_probs / bt_probs.sum()
        blood_type = np.random.choice(
            list(BLOOD_TYPE_DISTRIBUTION.keys()),
            p=bt_probs
        )

        # Donor type based on NBCUS
        # 30% first-time, 70% repeat
        is_first_time = np.random.random() < 0.30

        if is_first_time:
            total_donations = 1
            months_since_first = np.random.randint(0, 6)
            months_since_last = months_since_first
        else:
            # Repeat donors: follow power law distribution
            total_donations = int(np.random.pareto(1.5) * 3) + 2
            total_donations = min(total_donations, 50)  # Cap at 50
            months_since_first = total_donations * np.random.randint(3, 8)
            months_since_first = min(months_since_first, 120)  # Cap at 10 years
            months_since_last = int(np.random.exponential(6))
            months_since_last = min(months_since_last, months_since_first)

        # Monetary (cc donated) - 450cc per donation typically
        total_volume_cc = total_donations * 450

        # Calculate registration date
        reg_date = datetime.now() - timedelta(days=months_since_first * 30)

        # Last donation date
        last_donation = datetime.now() - timedelta(days=months_since_last * 30)

        # Availability status
        # Must wait 56 days (8 weeks) between donations
        days_since_last = (datetime.now() - last_donation).days
        if days_since_last >= 56:
            availability = 'Available'
        else:
            availability = 'Not Eligible'

        # Deferral history (some donors have been deferred before)
        has_deferral = np.random.random() < 0.15  # 15% deferral rate
        if has_deferral:
            def_probs = np.array(list(DEFERRAL_REASONS.values()))
            def_probs = def_probs / def_probs.sum()
            deferral_reason = np.random.choice(
                list(DEFERRAL_REASONS.keys()),
                p=def_probs
            )
            # Women more likely to have low hemoglobin deferral
            if gender == 'Female' and np.random.random() < 0.3:
                deferral_reason = 'Low hemoglobin'
        else:
            deferral_reason = None

        donors.append({
            'donor_id': f'D{str(i+1).zfill(5)}',
            'name': fake.name(),
            'age': age,
            'gender': gender,
            'blood_type': blood_type,
            'city': np.random.choice(CITIES),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'registration_date': reg_date.strftime('%Y-%m-%d'),
            'last_donation_date': last_donation.strftime('%Y-%m-%d'),
            'total_donations': total_donations,
            'total_volume_cc': total_volume_cc,
            'months_since_first_donation': months_since_first,
            'months_since_last_donation': months_since_last,
            'availability_status': availability,
            'is_first_time_donor': is_first_time,
            'has_deferral_history': has_deferral,
            'deferral_reason': deferral_reason
        })

    df = pd.DataFrame(donors)
    print(f"  Generated {len(df)} donor records")
    return df


def generate_rfm_dataset(donor_df):
    """
    Create RFM dataset from donor registry for segmentation.
    Similar structure to UCI Blood Transfusion dataset.
    """
    print("Generating RFM dataset...")

    rfm_df = donor_df[['donor_id', 'months_since_last_donation',
                        'total_donations', 'total_volume_cc',
                        'months_since_first_donation']].copy()

    rfm_df.columns = ['donor_id', 'Recency', 'Frequency', 'Monetary', 'Time']

    # Add target variable: donated in last 3 months (similar to UCI target)
    rfm_df['donated_last_quarter'] = (rfm_df['Recency'] <= 3).astype(int)

    print(f"  Generated RFM dataset with {len(rfm_df)} records")
    return rfm_df


def generate_supply_data(demand_df, utilization_rate=0.929, wastage_rate=0.071):
    """
    Generate supply data based on demand with realistic utilization/wastage.
    Based on Nepal BPKIHS study: 92.9% utilization, 7.1% wastage.
    """
    print("Generating supply dataset...")

    supply_data = []

    for _, row in demand_df.iterrows():
        # Supply slightly higher than demand to account for buffer
        # But not too high to avoid wastage
        buffer_factor = np.random.uniform(1.05, 1.20)
        supply = int(row['demand_units'] * buffer_factor)

        # Calculate actual utilization and wastage
        utilized = min(supply, row['demand_units'])
        wasted = max(0, supply - row['demand_units'])

        # Some wastage due to expiry regardless of demand
        expiry_wastage = int(supply * np.random.uniform(0.01, 0.05))
        wasted += expiry_wastage

        supply_data.append({
            'date': row['date'],
            'component': row['component'],
            'supply_units': supply,
            'demand_units': row['demand_units'],
            'utilized_units': utilized,
            'wasted_units': wasted,
            'utilization_rate': utilized / supply if supply > 0 else 0,
            'wastage_rate': wasted / supply if supply > 0 else 0
        })

    df = pd.DataFrame(supply_data)
    print(f"  Generated supply dataset with {len(df)} records")
    return df


def main():
    """Generate all datasets and save to data folder."""

    # Create data directory if not exists
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    os.makedirs(data_dir, exist_ok=True)

    print("\n" + "="*60)
    print("BLOOD SUPPLY MANAGEMENT - SYNTHETIC DATA GENERATION")
    print("="*60 + "\n")

    # 1. Generate demand time-series (3 years of daily data)
    demand_detailed, demand_daily = generate_demand_timeseries(
        start_date='2021-01-01',
        periods=1095  # 3 years
    )
    demand_detailed.to_csv(os.path.join(data_dir, 'demand_detailed.csv'), index=False)
    demand_daily.to_csv(os.path.join(data_dir, 'demand_daily.csv'), index=False)

    # 2. Generate donor registry
    donor_df = generate_donor_registry(n_donors=10000)
    donor_df.to_csv(os.path.join(data_dir, 'donor_registry.csv'), index=False)

    # 3. Generate RFM dataset
    rfm_df = generate_rfm_dataset(donor_df)
    rfm_df.to_csv(os.path.join(data_dir, 'rfm_dataset.csv'), index=False)

    # 4. Generate supply data
    supply_df = generate_supply_data(demand_daily)
    supply_df.to_csv(os.path.join(data_dir, 'supply_inventory.csv'), index=False)

    print("\n" + "="*60)
    print("DATA GENERATION COMPLETE")
    print("="*60)
    print(f"\nFiles saved to: {data_dir}")
    print("\nDatasets generated:")
    print(f"  1. demand_detailed.csv   - {len(demand_detailed):,} records")
    print(f"  2. demand_daily.csv      - {len(demand_daily):,} records")
    print(f"  3. donor_registry.csv    - {len(donor_df):,} records")
    print(f"  4. rfm_dataset.csv       - {len(rfm_df):,} records")
    print(f"  5. supply_inventory.csv  - {len(supply_df):,} records")

    return {
        'demand_detailed': demand_detailed,
        'demand_daily': demand_daily,
        'donor_registry': donor_df,
        'rfm_dataset': rfm_df,
        'supply_inventory': supply_df
    }


if __name__ == '__main__':
    datasets = main()
