import pandas as pd
from pathlib import Path

def read_price_paid(data_path, pp_filename):
    """Read Price Paid CSVs (all files), set dtypes"""

    folder = Path(data_path)
    files = sorted(folder.glob(pp_filename))

    if not files:
        raise FileNotFoundError(f"No price paid files found in {data_path} with {pp_filename}")
    
    out = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
    out['deed_date'] = out['deed_date'].astype('datetime64[ns]')
    return out

def read_epc(data_path, epc_filename, epc_cols):
    """Read EPC CSV, select columns, set dtypes (dates, UPRN as Int64)"""
    file = Path(data_path) / epc_filename
    if not file.exists():
        raise FileNotFoundError(f"No EPC file found in {data_path} with {epc_filename}")
    out = pd.read_csv(file, usecols= epc_cols)
    
    out['inspection_date'] = out['inspection_date'].astype('datetime64[ns]')
    out['lodgement_date'] = out['lodgement_date'].astype('datetime64[ns]')
    out['uprn'] = out['uprn'].astype('Int64') # pandas nullable integer type instead of int64 numpys which is not nullable
    return out

def filter_local_authorities(epc, target_local_authorities):
    """Filter EPC to the five target local authorities"""
    out = epc[epc['local_authority'].isin(target_local_authorities)]
    return out