import pandas as pd

def strip_whitespace(df):
    """Strip whitespace"""
    out = df.copy()
    for c in out.select_dtypes(include=['string']).columns:
        out[c] = out[c].str.strip()
    return out

def remove_commas(df, address_cols):
    """Remove commas from address columns"""
    out = df.copy()
    for c in address_cols:
        out[c] = out[c].str.replace(',', '', regex=False)
    return out

def build_address(df, address_cols):
    """Build combined address string (uppercase)"""
    out = df.copy()
    out['address'] = out[address_cols[0]].str.cat(out[address_cols[1:]], sep=' ', na_rep='')
    out['address'] = out['address'].str.upper() # pandas vectorised instead of .apply(str.upper) working on each value
    out['address'] = out['address'].str.replace(r"\s+", " ", regex=True).str.strip() # replace double(+) spaces with single and remove any trailing spaces
    return out

def build_tokens(df):
    """Build token sets"""
    out = df.copy()
    out['address_tokens'] = out['address'].str.split().apply(frozenset)
    return out