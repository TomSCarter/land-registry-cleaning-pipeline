## Part 5 - Pipeline

Refactored the cleaning and matching steps from Parts 2-4 into reusable functions in `src/cleaning/`, run in order by a pipeline class. The full pipeline runs from the raw files to the cleaned dataset with one command:

    python run_pipeline.py

(run from the project root, with the virtual environment active)

### Project structure

    Week_10_land_registry/
    ├── run_pipeline.py          # creates the pipeline, runs it, prints the report
    └── src/
        └── cleaning/
            ├── config.py
            ├── load.py
            ├── normalise.py
            ├── match.py
            ├── features.py
            ├── clean.py
            ├── save.py
            └── pipeline.py      # CleaningPipeline class

## Pipeline design

Functions return only the DataFrame. The pipeline class records counts after each step; expected values are in the validation table below.

### 0. config (config.py)

- **PROJECT_ROOT / DATA_PATH / PROCESSED_PATH**: built from the config file's own location, so paths work wherever the code is run from
- **PP_FILENAME**: glob pattern for Price Paid CSVs ('ppd_data*.csv')
- **EPC_FILENAME**: EPC CSV file name
- **PROCESSED_FILENAME**: output Parquet file name
- **EPC_COLS**: the 28 EPC columns kept in Part 1
- **TARGET_LOCAL_AUTHORITIES**: the five Oxfordshire district codes
- **PP_ADDRESS_COLS**: ['paon', 'saon', 'street', 'locality', 'postcode']
- **EPC_ADDRESS_COLS**: ['address1', 'address2', 'address3', 'postcode']
- **FINAL_COLS / RENAME_MAP**: columns kept after matching and their new names
- **AGE_BINS / AGE_LABELS**: EPC age band edges and labels
- **EPC_VALIDITY_YEARS**: 10
- **THRESHOLDS**: min floor area (9 sqm), large floor area rule (> 2000 sqm and <= 7 habitable rooms or rooms missing), min floor height (1.5 m), efficiency rule (> 110 and consumption > 200 for flats/maisonettes), min construction_age_band length (4 characters)
- **PLACEHOLDERS**: {'property_type': 'Not Recorded', 'built_form': 'Not Recorded', 'tenure': 'unknown'}

### 1. load (load.py)

#### Read Price Paid CSVs (all files), set dtypes
- **Name:** read_price_paid
- **Inputs:** data_path, pp_filename
- **Output:** pp DataFrame (deed_date as datetime)

#### Read EPC CSV, select columns, set dtypes (dates, UPRN as Int64)
- **Name:** read_epc
- **Inputs:** data_path, epc_filename, epc_cols
- **Output:** epc DataFrame

#### Filter EPC to the five target local authorities
- **Name:** filter_local_authorities
- **Inputs:** epc, target_local_authorities
- **Output:** filtered epc

### 2. normalise (normalise.py)

#### Strip whitespace
- **Name:** strip_whitespace
- **Inputs:** df
- **Output:** df with all string columns stripped

#### Remove commas from address columns
- **Name:** remove_commas
- **Inputs:** df, address_cols
- **Output:** df

#### Build combined address string (uppercase)
- **Name:** build_address
- **Inputs:** df, address_cols
- **Output:** df with 'address' column (runs of whitespace collapsed to one space)

#### Build token sets
- **Name:** build_tokens
- **Inputs:** df
- **Output:** df with 'address_tokens' column

### 3. match (match.py)

#### Postcode merge
- **Name:** merge_on_postcode
- **Inputs:** pp, epc
- **Output:** candidate pairs DataFrame

#### Subset test filter
- **Name:** filter_subset_matches
- **Inputs:** candidate pairs
- **Output:** pairs where PP tokens are a subset of EPC tokens

#### Remove ambiguous multi-UPRN matches
- **Name:** drop_ambiguous_matches
- **Inputs:** subset matches
- **Output:** matches with ambiguous unique_ids removed

#### Select closest pre-sale EPC
- **Name:** select_presale_epc
- **Inputs:** matches
- **Output:** one row per unique_id, with 'inspection_to_sale'. Ties broken by latest lodgement_date

#### Select/rename final columns (drops tokens and helper columns)
- **Name:** select_final_columns
- **Inputs:** df, final_cols, rename_map
- **Output:** df

### 4. features (features.py)

#### Convert EPC age to days and add age band
- **Name:** add_epc_age_band
- **Inputs:** df, age_bins, age_labels
- **Output:** df with 'inspection_to_sale' in days and 'EPC_age_band'

#### Add expired flag
- **Name:** add_expired_flag
- **Inputs:** df, epc_validity_years
- **Output:** df with 'EPC_expired'

#### Add calendar columns
- **Name:** add_calendar_features
- **Inputs:** df
- **Output:** df with dayofweek, day, month, quarter, year

### 5. clean (clean.py)

#### Convert invalid values to null
- **Name:** nullify_invalid_values
- **Inputs:** df, placeholders, min floor height
- **Output:** df

#### Apply exclusions (as rules)
- **Name:** apply_exclusions
- **Inputs:** df, thresholds
- **Output:** df

#### Impute floor height and add flag
- **Name:** impute_floor_height
- **Inputs:** df
- **Output:** df with 'floor_height_imputed'. Median is calculated from the whole dataset; Week 13 modelling should recalculate it from training data only

### 6. save (save.py)

#### Write to data/processed/ as Parquet
- **Name:** save_parquet
- **Inputs:** df, processed_path, processed_filename
- **Output:** Parquet file on disk (creates the folder if missing); returns the file path

### 7. pipeline (pipeline.py)

#### Run stages 1-6 in order and collect counts per step
- **Name:** CleaningPipeline (class with a run method)
- **Inputs:** config
- **Output:** final DataFrame and run report (rows per step, plus unique sales, expired count, null counts and imputed count where relevant)

## Implementation notes

- Functions return only a DataFrame; the pipeline class records counts after each step
- Functions work on a copy and never modify their input
- The pipeline reads every setting from the config passed in, so a different config (e.g. an older EPC extract) needs no code changes
- Missing input files raise FileNotFoundError with a clear message (tested deliberately)
- Price Paid files are read in sorted order so row order is reproducible
- UPRN cast to pandas nullable 'Int64' (NumPy int64 cannot hold nulls)
- EPC filtered to the five target local authorities (Part 1 decision, not applied in Parts 2-4): 4 rows dropped, final match count unchanged at 91,150, confirming these border properties never matched
- Combined address: runs of whitespace collapsed to one space (cosmetic; token sets unaffected)
- Pre-sale EPC selection: ties on inspection_to_sale broken by latest lodgement_date (likely a corrected certificate). Previously arbitrary. 670 sales (0.7%) had two or more certificates tied for closest pre-sale inspection. EPC features for these sales may differ from Part 4; this explains the small differences in the validation table (a later lodgement makes a certificate younger, so fewer expire)
- Exclusions expressed as rules rather than certificate IDs, so they apply to new data
- Rule simplification: all floor areas <= 9 sqm excluded (Part 1 proposed flagging 1-room flats); no effect on current data
- Output saved as Parquet (requires pyarrow), which keeps dtypes such as datetimes, Int64 and the ordered age band category; round-trip test passed
- Development used a checkpoint of the matched data to avoid re-running the slow subset test (ca. 2 min) on every change

## Validation against Parts 2-4

Final run from the terminal (`python run_pipeline.py`):

| Step | Measure | Expected | Pipeline | Match |
|---|---|---|---|---|
| read_price_paid | rows | 135,557 | 135,557 | ✓ |
| read_epc | rows | 216,054 | 216,054 | ✓ |
| filter_local_authorities | rows dropped | 4 | 4 | ✓ |
| filter_subset_matches | unique sales | 105,419 | 105,419 | ✓ |
| drop_ambiguous_matches | unique sales dropped | 975 | 975 | ✓ |
| select_presale_epc | rows | 91,150 | 91,150 | ✓ |
| select_final_columns | columns | 36 | 36 | ✓ |
| add_expired_flag | expired | 66 | 62 | ≈ tie-break |
| nullify_invalid_values | converted (heated rooms / floor height / property_type / tenure / built_form) | 134 / 1,429 / 0 / 21,458 / 27 | 134 / 1,427 / 0 / 21,458 / 27 | ≈ tie-break (floor height) |
| nullify_invalid_values | total nulls after (heated rooms / floor height / tenure / built_form) | 29,606 / 2,049 / 21,458 / 2,036 | 29,603 / 2,046 / 21,458 / 2,040 | ≈ tie-break |
| apply_exclusions | rows dropped | 7 (1 / 3 / 0 / 3 by rule) | 7 (total) | ✓ |
| impute_floor_height | imputed | 2,049 | 2,046 | ≈ tie-break |
| final | rows | 91,143 | 91,143 | ✓ |

All differences are small and explained by the tie-break rule. The 2,046 imputed values equal the floor height nulls after nullifying, confirming none of the 7 excluded rows had a missing floor height.

## Deferred

- Re-run with an EPC extract from 2012 to improve the early-year match rate: Week 21-22 (config change only)
- pytest unit tests for the cleaning functions: Week 15 testing primer
- Faster subset test (zip instead of row-wise apply): only if run time becomes a problem