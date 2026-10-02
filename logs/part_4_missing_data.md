# Land registry price data (& EPC) analysis

## Part 4 - Missing data 

- Copied across cells to generate matched data with added EPC_age_band, EPC_expired flag and calendar features from Part 3

- Converting invalid values to null
    - Zero number_heated_rooms, 138 records
        - Replaced with NaN
    - 'floor_height' < 1.5m, 1429 records
        - Replaced with NaN
    - 'property_type' as 'Not Recorded'
        - No records, must have been filtered out in matching and date/duplicate filters
        - Only 8 NaN
    - 'tenure' is 'unknown', 21458 records
        - Replaced with NaN

- Missingness of fields
    - 12 of 43 columns with missing values
                                    missing
            field_name                  
            unique_id               0.00
            saon                   93.52
            street                  1.89
            locality               59.61
            built_form              2.20
            extension_count        32.33
            floor_height            2.25
            number_heated_rooms    32.48
            property_type           0.01
            tenure                 23.54
            transaction_type        0.02
            uprn                    0.19

- Exclusions from part 1
    - Checked for properties with 'total_floor_area' <= 9 sqm
        - Only 1, it has 2 rooms, excluded.
    - Checked for the 7 high floor area records flagged for exclusion (>2000 sqm and <= 7 rooms)
        - 3 in dataset, excluded
    - Checked for two records with current_energy_efficiency > 110, energy_consumption_current >200 and are Maisonette/Flat
        - Not in dataset
    - Checked 'construction_age_band' for values < 4 characters long
        - excluded 3 records with '201'