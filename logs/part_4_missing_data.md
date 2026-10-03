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
    
- Investigated if rows with missing rooms could be filled from post-sale EPC records
    - In part 1 it was found that New dwellings systematically have no value for 'number_heated_rooms', 'number_habitable_rooms' and 'extension_count'
    - There are 27473 New dwellings in the joined set with no value for 'number_heated_rooms'
    - Filtering for these properties (via uprn) in the raw EPC set finds 583 properties that could be used for filling. This represents only 2.1% of the New dwelling properties with missing values. Filling not implemented.
    - New dwellings are over-represented in the joined set (ca. 30% vs 21% in raw EPC data)
        - 'total_floor_area' will be the main size feature used in future work
        - 31% of properties labelled New dwelling (from EPC) are not flagged as new_build (from price paid)
            - Possible they were new viewed as new at the time of sale?

- Missing 'floor_height' values
    - 1615 null values. 99% are for Flats where the 'floor_height' is likely to be very standardised.
    - Distribution of 'floor_height' in Flats and all property_types is similar (median 2.38m and 2.37m), with middle half spans tight (13cm and 11cm)
    - *Proposal: Impute missing 'floor_height' with median values and add a floor_height_imputed flag*
        - Not a lot of information contained in this feaure due to the lack of variation