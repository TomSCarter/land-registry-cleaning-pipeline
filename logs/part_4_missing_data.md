# Land registry price data (& EPC) analysis

## Part 4 - Missing data 

### Summary table

| Column | Missing (joined table) | Cause | Treatment |
|---|---|---|---|
| 'number_heated_rooms' | 29,606 (32.5%) | 27,473 new-dwelling certificates (structural: not recorded); 2,130 others, over-represented in transaction_type 'None of the above' (26% vs 0.6%); includes 134 zero values converted to missing | Leave null. Filling from the same property's other certificates recovers only 2.1%, so not implemented. Future regression: use 'total_floor_area' as the main size feature |
| 'number_habitable_rooms' | 29,472 (32.3%) | As above, without the zero conversions | As above |
| 'extension_count' | 29,472 (32.3%) | As above | Leave null |
| 'tenure' | 21,458 (23.5%) | 'unknown' converted to missing | Leave null. Large gap; not a core price feature |
| 'floor_height' | 2,049 (2.2%), now imputed | 1,429 values < 1.5 m converted to missing (70%); 620 original nulls (30%) | Imputed with overall median (2.37 m); middle half of values span 2.30-2.41 m. 'floor_height_imputed' flag. Low-variance feature, may be dropped in future regression |
| 'built_form' | 2,036 (2.2%) | Not recorded | Converted 'Not Recorded' to missing for consistency; leave null |
| 'uprn', 'uprn_source' | 171 (0.2%) | Not assigned on certificate | Leave null; ID only, not a feature |
| 'transaction_type' | 14 (0.02%) | Not recorded | Leave null |
| 'property_type' | 8 (0.01%) | Missing in source ('Not Recorded' count in joined table was 0) | Leave null |
| 'street' | 1,719 (1.9%) | Structural: e.g. farms, named rural properties | Leave null; address field, not a feature |
| 'saon', 'locality' | 93.5%, 59.6% | Structural: most properties have no secondary name or locality | Leave null; address fields, not features |
| All other columns | 0 | Complete | None needed |

### Notes

- Copied across cells to generate matched data with added EPC_age_band, EPC_expired flag and calendar features from Part 3

- Converting invalid values to null
    - Zero number_heated_rooms, 134 records
        - *Decision:* Replaced with NaN
    - 'floor_height' < 1.5m, 1429 records
        - *Decision:* Replaced with NaN
    - 'property_type' as 'Not Recorded'
        - No records, must have been filtered out in matching and date/duplicate filters
        - Only 8 NaN
    - 'tenure' is 'unknown', 21458 records
        - *Decision:* Replaced with NaN
    - 'built_form' is 'Not Recorded', 27 values 
        - *Decision:* Replaced with NaN

- Exclusions from part 1
    - Checked for properties with 'total_floor_area' <= 9 sqm
        - *Decision:* Only 1, it has 2 rooms, excluded.
        - The 19 tiny 1-room flats noted in Part 1 audit are not in the joined set
    - Checked for the 7 high floor area records flagged for exclusion (>2000 sqm and <= 7 rooms)
        - *Decision:* 3 in dataset, excluded
    - Checked for two records with current_energy_efficiency > 110, energy_consumption_current >200 and are Maisonette/Flat
        - Not in dataset
    - Checked 'construction_age_band' for values < 4 characters long
        - *Decision:*  excluded 3 records with '201'
    
- Investigated if rows with missing rooms could be filled from post-sale EPC records
    - In part 1 it was found that New dwellings ('transaction_type') systematically have no value for 'number_heated_rooms', 'number_habitable_rooms' and 'extension_count'
    - There are 27473 New dwellings in the joined set with no value for 'number_heated_rooms'
    - Filtering for these properties (via uprn) in the raw EPC set finds 583 properties that could be used for filling. This represents only 2.1% of the New dwelling properties with missing values. *Decision:* Filling not implemented.
    - New dwellings are over-represented in the joined set (ca. 30% vs 21% in raw EPC data)
        - 'total_floor_area' will be the main size feature used in future work
        - 31% of properties labelled New dwelling (from EPC) are not flagged as new_build (from price paid)
            - Possible they were new when the inspection took place but not when sold

- Missing 'floor_height' values
    - The nulls are a mixture of the original nulls (99% flats in raw EPC data) and created nulls (mostly houses, where floor_height was <1.5m)
    - Distribution of 'floor_height' in Houses/Flats/Bungalow and all property_types is similar (median 2.37m/2.38m/2.39m/2.37m), with middle half spans tight (11cm/13cm/10cm/11cm)
        - box plot shows a tight distribution but with a lot of outliers in all property types (except Park Home)
        - *Decision:* Imputed missing 'floor_height' with median values and add a floor_height_imputed flag
        - Not a lot of information contained in this feature due to the lack of variation

- Analysis of remaining properties with missing rooms
    - With transaction_type = 'New dwelling' excluded. Comparing properties with missing rooms against those without missing rooms:
        - transaction_type = 'None of the above' is over-represented (26% vs 0.6%) and all others under-represented
        - property_type is more likely to be House (86% vs 80%) and less likely to be Bungalow (1.6% vs 9%) or Maisonette (0.4% vs 1.3%)
        - built_form is more likely to be Detached (51% vs 31%) and less likely to be all others particularly Mid-Terrace (10% vs 21%)
        - Median total floor area is a little higher in missing set (98 sqm vs 88 sqm)
        - No clear explanation, leaving these as missing and unexplained


