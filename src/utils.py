"""
Utility functions for Blood Supply Management Project
Team: IDGAF
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


# =============================================================================
# CONSTANTS - Based on Research Papers (NBCUS 2019, Nepal BPKIHS, WHO)
# =============================================================================

# Blood type distribution (WHO global averages)
BLOOD_TYPE_DISTRIBUTION = {
    'O+': 0.374,
    'A+': 0.276,
    'B+': 0.201,
    'AB+': 0.050,
    'O-': 0.066,
    'A-': 0.028,
    'B-': 0.015,
    'AB-': 0.010
}

# Age group distribution (NBCUS 2019 trends)
AGE_GROUP_DISTRIBUTION = {
    '16-18': 0.08,
    '19-24': 0.15,
    '25-34': 0.22,
    '35-44': 0.18,
    '45-54': 0.17,
    '55-64': 0.12,
    '65+': 0.08
}

# Gender distribution for donors
GENDER_DISTRIBUTION = {
    'Male': 0.54,
    'Female': 0.46
}

# Deferral reasons (NBCUS 2019)
DEFERRAL_REASONS = {
    'Low hemoglobin': 0.431,
    'Non-medical reasons': 0.214,
    'Blood pressure/pulse': 0.112,
    'Travel history': 0.089,
    'Medication': 0.072,
    'Recent tattoo/piercing': 0.045,
    'Other medical': 0.037
}

# Component shelf life (days)
COMPONENT_SHELF_LIFE = {
    'Whole Blood': 35,
    'Packed RBC': 42,
    'Platelets': 5,
    'Fresh Frozen Plasma': 365,
    'Cryoprecipitate': 365
}

# Wastage rates by component (Nepal BPKIHS study)
COMPONENT_WASTAGE_RATES = {
    'Packed RBC': 0.05,
    'Platelets': 0.15,  # Highest wastage due to short shelf life
    'Fresh Frozen Plasma': 0.04,
    'Cryoprecipitate': 0.06
}

# Utilization rate benchmark
UTILIZATION_RATE_TARGET = 0.929  # 92.9% from Nepal study

# RFM Segment definitions
RFM_SEGMENTS = {
    'Champions': {'R': [4, 5], 'F': [4, 5], 'M': [4, 5]},
    'Loyal': {'R': [3, 4], 'F': [3, 4, 5], 'M': [3, 4, 5]},
    'Potential': {'R': [3, 4, 5], 'F': [1, 2, 3], 'M': [1, 2, 3]},
    'At Risk': {'R': [1, 2], 'F': [3, 4, 5], 'M': [3, 4, 5]},
    'Hibernating': {'R': [1, 2], 'F': [1, 2], 'M': [1, 2]},
    'New': {'R': [4, 5], 'F': [1], 'M': [1]}
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def calculate_rfm_scores(df, recency_col='Recency', frequency_col='Frequency', monetary_col='Monetary'):
    """
    Calculate RFM scores (1-5) for each donor.
    Lower recency = better (more recent), so scoring is inverted.
    """
    df = df.copy()

    # Recency: Lower is better, so we invert the scoring
    df['R_Score'] = pd.qcut(df[recency_col], q=5, labels=[5, 4, 3, 2, 1], duplicates='drop')

    # Frequency: Higher is better
    df['F_Score'] = pd.qcut(df[frequency_col].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5], duplicates='drop')

    # Monetary: Higher is better
    df['M_Score'] = pd.qcut(df[monetary_col].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5], duplicates='drop')

    # Convert to int
    df['R_Score'] = df['R_Score'].astype(int)
    df['F_Score'] = df['F_Score'].astype(int)
    df['M_Score'] = df['M_Score'].astype(int)

    # Combined RFM Score
    df['RFM_Score'] = df['R_Score'].astype(str) + df['F_Score'].astype(str) + df['M_Score'].astype(str)

    return df


def assign_rfm_segment(row):
    """
    Assign donor segment based on RFM scores.
    """
    r, f, m = row['R_Score'], row['F_Score'], row['M_Score']

    if r >= 4 and f >= 4:
        return 'Champions'
    elif r >= 3 and f >= 3:
        return 'Loyal'
    elif r >= 4 and f == 1:
        return 'New'
    elif r <= 2 and f >= 3:
        return 'At Risk'
    elif r <= 2 and f <= 2:
        return 'Hibernating'
    else:
        return 'Potential'


def calculate_demand_features(df, date_col='date'):
    """
    Add time-based features for demand forecasting.
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])

    df['year'] = df[date_col].dt.year
    df['month'] = df[date_col].dt.month
    df['day'] = df[date_col].dt.day
    df['day_of_week'] = df[date_col].dt.dayofweek
    df['week_of_year'] = df[date_col].dt.isocalendar().week
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    df['quarter'] = df[date_col].dt.quarter

    # Seasonal indicators
    df['is_summer'] = df['month'].isin([6, 7, 8]).astype(int)
    df['is_winter'] = df['month'].isin([12, 1, 2]).astype(int)
    df['is_holiday_season'] = df['month'].isin([11, 12]).astype(int)

    return df


def calculate_inventory_metrics(demand, supply, shelf_life_days=42):
    """
    Calculate inventory optimization metrics.
    """
    metrics = {
        'total_demand': demand.sum(),
        'total_supply': supply.sum(),
        'utilization_rate': min(demand.sum() / supply.sum(), 1.0) if supply.sum() > 0 else 0,
        'shortage_risk': max(0, (demand.sum() - supply.sum()) / demand.sum()) if demand.sum() > 0 else 0,
        'wastage_risk': max(0, (supply.sum() - demand.sum()) / supply.sum()) if supply.sum() > 0 else 0
    }
    return metrics


def forecast_accuracy_metrics(y_true, y_pred):
    """
    Calculate forecasting accuracy metrics.
    """
    y_true, y_pred = np.array(y_true), np.array(y_pred)

    # Remove zeros to avoid division errors
    mask = y_true != 0
    y_true_masked = y_true[mask]
    y_pred_masked = y_pred[mask]

    mae = np.mean(np.abs(y_true - y_pred))
    rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))
    mape = np.mean(np.abs((y_true_masked - y_pred_masked) / y_true_masked)) * 100

    return {
        'MAE': round(mae, 2),
        'RMSE': round(rmse, 2),
        'MAPE': round(mape, 2)
    }


def get_outreach_recommendations(segment_df):
    """
    Generate targeted outreach recommendations based on donor segments.
    """
    recommendations = {
        'Champions': {
            'action': 'Retain & Reward',
            'strategy': 'VIP treatment, early access to donation drives, recognition programs',
            'frequency': 'Monthly touchpoints',
            'channel': 'Personal calls, exclusive emails'
        },
        'Loyal': {
            'action': 'Upsell & Engage',
            'strategy': 'Encourage referrals, milestone celebrations, loyalty rewards',
            'frequency': 'Bi-weekly engagement',
            'channel': 'Email, SMS reminders'
        },
        'Potential': {
            'action': 'Nurture & Convert',
            'strategy': 'Education about impact, flexible scheduling, convenience focus',
            'frequency': 'Weekly gentle reminders',
            'channel': 'Email campaigns, social media'
        },
        'At Risk': {
            'action': 'Reactivate Urgently',
            'strategy': 'Win-back campaigns, understand barriers, offer incentives',
            'frequency': 'Immediate outreach',
            'channel': 'Personal calls, targeted emails'
        },
        'Hibernating': {
            'action': 'Re-engage or Archive',
            'strategy': 'Last-chance campaigns, surveys to understand dropout reasons',
            'frequency': 'One-time campaign',
            'channel': 'Email, direct mail'
        },
        'New': {
            'action': 'Onboard & Educate',
            'strategy': 'Welcome series, first-donation follow-up, community building',
            'frequency': 'Weekly for first month',
            'channel': 'Email series, app notifications'
        }
    }
    return recommendations
