
import pandas as pd
from src.cleaning import load, normalise, match
from src.selection import clean, features, save

class CleaningPipeline:
    """Merges Land Registry Price Paid records with Energy Performance Certificate records, cleans and adds features"""

    def __init__(self, config):
        self.config = config
        self.report = []

    def _record(self, step, data, extra=None):
        row = {'step': step, 'rows': len(data)}
        if extra is not None:
            row.update(extra)
        self.report.append(row)

    def run(self):
        pp = load.read_price_paid(self.config.DATA_PATH, self.config.PP_FILENAME)
        self._record('load.read_price_paid', pp)
        epc = load.read_epc(self.config.DATA_PATH, self.config.EPC_FILENAME, self.config.EPC_COLS)
        self._record('load.read_epc', epc)
        epc = load.filter_local_authorities(epc, self.config.TARGET_LOCAL_AUTHORITIES)
        self._record('load.filter_local_authorities', epc)
        epc = normalise.strip_whitespace(epc)
        self._record('epc: normalise.strip_whitespace', epc)
        epc = normalise.remove_commas(epc, self.config.EPC_ADDRESS_COLS)
        self._record('epc: normalise.remove_commas', epc)
        epc = normalise.build_address(epc, self.config.EPC_ADDRESS_COLS)
        self._record('epc: normalise.build_address', epc)
        epc = normalise.build_tokens(epc)
        self._record('epc: normalise.build_tokens', epc)
        pp = normalise.strip_whitespace(pp)
        self._record('pp: normalise.strip_whitespace', pp)
        pp = normalise.remove_commas(pp, self.config.PP_ADDRESS_COLS)
        self._record('pp: normalise.remove_commas', pp)
        pp = normalise.build_address(pp, self.config.PP_ADDRESS_COLS)
        self._record('pp: normalise.build_address', pp)
        pp = normalise.build_tokens(pp)
        self._record('pp: normalise.build_tokens', pp)
        df = match.merge_on_postcode(pp, epc)
        self._record('match.merge_on_postcode', df)
        df = match.filter_subset_matches(df)
        self._record('match.filter_subset_matches', df, {'unique_sales': df['unique_id'].nunique()})
        df = match.drop_ambiguous_matches(df)
        self._record('match.drop_ambiguous_matches', df, {'unique_sales': df['unique_id'].nunique()})
        df = match.select_presale_epc(df)
        self._record('match.select_presale_epc', df)
        df = match.select_final_columns(df, self.config.FINAL_COLS, self.config.RENAME_MAP)
        self._record('match.select_final_columns', df, {'col_count': df.shape[1]})
        df = features.add_epc_age_band(df, self.config.AGE_BINS, self.config.AGE_LABELS)
        self._record('features.add_epc_age_band', df)
        df = features.add_expired_flag(df, self.config.EPC_VALIDITY_YEARS)
        self._record('features.add_expired_flag', df, {'expired': df['EPC_expired'].sum()})
        df = features.add_calendar_features(df)
        self._record('features.add_calendar_features', df)
        df = clean.nullify_invalid_values(df, self.config.PLACEHOLDERS, self.config.THRESHOLDS['min_floor_height'])
        self._record('clean.nullify_invalid_values', df, {
            'floor_height_nulls': df['floor_height'].isna().sum(), 
            'tenure_nulls': df['tenure'].isna().sum(), 
            'number_heated_rooms_nulls': df['number_heated_rooms'].isna().sum(), 
            'built_form_nulls': df['built_form'].isna().sum()})
        df = clean.apply_exclusions(df, self.config.THRESHOLDS)
        self._record('clean.apply_exclusions', df)
        df = clean.impute_floor_height(df)
        self._record('clean.impute_floor_height', df, {'imputed_count': df['floor_height_imputed'].sum()})
        save.save_parquet(df, self.config.PROCESSED_PATH, self.config.PROCESSED_FILENAME)
        self._record('save.save_parquet', df)
        return df, pd.DataFrame(self.report)

