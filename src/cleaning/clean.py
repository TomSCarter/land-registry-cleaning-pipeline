import pandas as pd
import numpy as np

def nullify_invalid_values(df, placeholders, min_floor_height):
    """Convert invalid values to null"""
    out = df.copy()
    for col, value in placeholders.items():
        out.loc[out[col] == value, col] = np.nan
    out.loc[out['number_heated_rooms'] == 0, 'number_heated_rooms'] = np.nan
    out.loc[out['floor_height'] < min_floor_height, 'floor_height'] = np.nan
    return out

def apply_exclusions(df, thresholds):
    """Apply exclusions (as rules)"""
    out = df.copy()
    out = out[(out['total_floor_area'] > thresholds['min_floor_area'])]
    out = out[~(
        (out['total_floor_area'] > thresholds['large_floor_area']) 
        & ((out['number_habitable_rooms'] <= thresholds['large_floor_area_rooms']) 
        | (out['number_habitable_rooms'].isna()))
        )]
    out = out[~(
        (out['current_energy_efficiency'] > thresholds['eff_cutoff']) 
               & (out['energy_consumption_current'] > thresholds['consump_cutoff']) 
               & (out['property_type'].isin(thresholds['eff_cutoff_types']))
                  )]
    out = out[out['construction_age_band'].str.len() >= thresholds['const_age_len_min']]
    return out

def impute_floor_height(df):
    """Impute floor height and add flag"""
    out = df.copy()
    out['floor_height_imputed'] = out['floor_height'].isna()
    out['floor_height'] = out['floor_height'].fillna(out['floor_height'].median())
    return out