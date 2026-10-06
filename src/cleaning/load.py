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
    


def filter_local_authorities(epc, target_local_authorities):