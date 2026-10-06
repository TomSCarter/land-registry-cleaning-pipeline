## Pipeline design

### 0. config (config.py)

- **data_path**: relative path to data/raw/
- **processed_path**: relative path to data/processed/
- **pp_filename**: glob pattern for Price Paid CSVs ('ppd_data*.csv')
- **epc_filename**: EPC CSV file name
- **epc_cols**: the 28 EPC columns kept in Part 1
- **target_local_authorities**: the five Oxfordshire district codes
- **pp_address_cols**: ['paon', 'saon', 'street', 'locality', 'postcode']
- **epc_address_cols**: ['address1', 'address2', 'address3', 'postcode']
- **final_cols / rename_map**: columns kept after matching and their new names
- **age_bins / age_labels**: EPC age band edges and labels
- **epc_validity_years**: 10
- **thresholds**: min floor area (9 sqm), large floor area rule (> 2000 sqm and <= 7 rooms), min floor height (1.5 m), efficiency rule (> 110 and consumption > 200 for flats/maisonettes)
- **placeholders**: {'property_type': 'Not Recorded', 'built_form': 'Not Recorded', 'tenure': 'unknown'}

### 1. load (load.py)

#### Read Price Paid CSVs (all files), set dtypes
- **Name:** read_price_paid
- **Inputs:** data_path, pp_filename
- **Output:** pp DataFrame (deed_date as datetime)
- **Reports:** row count

#### Read EPC CSV, select columns, set dtypes (dates, UPRN as Int64)
- **Name:** read_epc
- **Inputs:** data_path, epc_filename, epc_cols
- **Output:** epc DataFrame
- **Reports:** row count

#### Filter EPC to the five target local authorities
- **Name:** filter_local_authorities
- **Inputs:** epc, target_local_authorities
- **Output:** filtered epc
- **Reports:** rows dropped (expect 4)

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
- **Output:** df with 'address' column

#### Build token sets
- **Name:** build_tokens
- **Inputs:** df
- **Output:** df with 'address_tokens' column

### 3. match (match.py)

#### Postcode merge
- **Name:** merge_on_postcode
- **Inputs:** pp, epc
- **Output:** candidate pairs DataFrame
- **Reports:** candidate pair count

#### Subset test filter
- **Name:** filter_subset_matches
- **Inputs:** candidate pairs
- **Output:** pairs where PP tokens are a subset of EPC tokens
- **Reports:** matched unique_ids (expect 105,419)

#### Remove ambiguous multi-UPRN matches
- **Name:** drop_ambiguous_matches
- **Inputs:** subset matches
- **Output:** matches with ambiguous unique_ids removed
- **Reports:** unique_ids dropped (expect 975)

#### Select closest pre-sale EPC (creates inspection-to-sale gap)
- **Name:** select_presale_epc
- **Inputs:** matches
- **Output:** one row per unique_id
- **Reports:** rows remaining (expect 91,150)

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
- **Reports:** expired count (expect 66)

#### Add calendar columns
- **Name:** add_calendar_features
- **Inputs:** df
- **Output:** df with dayofweek, day, month, quarter, year

### 5. clean (clean.py)

#### Convert invalid values to null
- **Name:** nullify_invalid_values
- **Inputs:** df, placeholders, min floor height
- **Output:** df
- **Reports:** values converted per column

#### Apply exclusions (as rules)
- **Name:** apply_exclusions
- **Inputs:** df, thresholds
- **Output:** df
- **Reports:** rows dropped per rule (expect 1, 3, 0, 3)

#### Impute floor height and add flag
- **Name:** impute_floor_height
- **Inputs:** df
- **Output:** df with 'floor_height_imputed'
- **Reports:** values imputed (expect 2,049)

### 6. save (save.py)

#### Write to data/processed/ as Parquet
- **Name:** save_parquet
- **Inputs:** df, processed_path
- **Output:** file on disk

### 7. pipeline (pipeline.py)

#### Run stages 1-6 in order and collect row counts per step
- **Name:** CleaningPipeline (class with a run method)
- **Inputs:** config
- **Output:** final DataFrame and run report    