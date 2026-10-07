import pandas as pd

def merge_on_postcode(pp, epc):
    """Postcode merge"""
    postcode_match = pp.merge(epc, on='postcode', how='inner')
    return postcode_match

def filter_subset_matches(merged_df):
    """Subset test filter"""
    def compare(row):
        return row['address_tokens_x'].issubset(row['address_tokens_y'])
    subset_matches = merged_df[merged_df.apply(compare, axis=1)]
    return subset_matches

def drop_ambiguous_matches(subset_matches):
    """Remove ambiguous multi-UPRN matches"""
    multi_match = subset_matches.groupby('unique_id')['uprn'].nunique()
    multi_uprn = multi_match[multi_match > 1]
    matches = subset_matches[~subset_matches['unique_id'].isin(multi_uprn.index)]
    return matches

def select_presale_epc(matches):
    """Select closest pre-sale EPC (creates inspection-to-sale gap)"""
    out = matches.copy()
    out['inspection_to_sale'] = out['deed_date'] - out['inspection_date']
    drop_neg = out[out['inspection_to_sale'] >= '0 days']
    out = drop_neg.sort_values(by=['inspection_to_sale', 'lodgement_date'], ascending=[True, False]).drop_duplicates(subset='unique_id')
    return out

def select_final_columns(df, final_cols, rename_map):
    """Select/rename final columns (drops tokens and helper columns)"""
    out = df[final_cols] # selecting cols creates a new df
    out = out.rename(columns=rename_map)
    return out