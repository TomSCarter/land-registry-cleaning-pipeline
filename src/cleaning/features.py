import pandas as pd

def add_epc_age_band(df, age_bins, age_labels):
    """Convert EPC age to days and add age band"""
    out = df.copy()
    out['inspection_to_sale'] = out['inspection_to_sale'].dt.days
    out['EPC_age_band'] = pd.cut(out['inspection_to_sale'], bins=age_bins, labels=age_labels, include_lowest=True)
    return out

def add_expired_flag(df, epc_validity_years):
    """Add expired flag"""
    out = df.copy()
    out['EPC_expired'] = ((out['deed_date'] > (out['lodgement_date'] + pd.DateOffset(years=epc_validity_years))))
    return out

def add_calendar_features(df):
    """Add calendar columns"""
    out = df.copy()
    out['dayofweek'] = out['deed_date'].dt.dayofweek
    out['day'] = out['deed_date'].dt.day
    out['month'] = out['deed_date'].dt.month
    out['quarter'] = out['deed_date'].dt.quarter
    out['year'] = out['deed_date'].dt.year
    return out