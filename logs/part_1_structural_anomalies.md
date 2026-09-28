# Land Registry Price Data Analysis

## Part 1 - Structural audit

- Scope changes: Scope was changed from 2025 national prices to 2015-2025 Oxfordshire only, but with joining of Energy Performance Certificate (EPC) dataset.

### Single year 2025 national price data audit

- part_1_LRPD_anomalies_2025.ipynb

- Loaded data and added header of column names
    - Column descriptions and names here: https://www.gov.uk/guidance/about-the-price-paid-data#explanations-of-column-headers-in-the-ppd
- shape: (954145, 16)
- Column by column audit
    - transaction_id (str)
        - Bracketed hexadecimal
        - 0 null
        - all unique
    - price (int64)
        - Integer numbers
        - 0 null
        - 30301 unique
        - No starting symbols (£ etc)
        - 540 <£1000 inc 5 for £1
        - 8 > £100 million, inc 1 at £793 million
    - date_of_transfer (str)
        - should be timestamp
        - 0 null
        - 364 unique
        - No sales on 27th December
    - postcode (str)
        - 2339 null
        - 548539 unique
        - All 6-8 characters
        - Performed regex check and found no incorrectly formatted postcodes ("^[A-Z]{1,2}\d[A-Z0-9]? \d[A-Z]{2}$")
    - property_type (str)
        - 0 null
        - 5 unique (T, S, D, F, O)
    - old_new (str)
        - 0 null
        - 2 unique
    - duration (str)
        - 0 null
        - 2 unique (F or L)
    - paon (str) - House number or name
        - could be int
        - 0 null
        - 80138 unique
    - saon (str) - second address object (e.g. Flat 2)
        - 840679 null
        - 7624 unique
    - street (str)
        - 15688 null
        - 185840 unique
        - Contains 11 with a comma (e.g. FOURTH STREET, WATLING STREET BUNGALOWS)
    - locality (str)
        - 587665 null
        - 16521 unique
        - 9 for Westward Ho!
    - town_city (str)
        - 0 null
        - 1146 unique
    - district (str)
        - 0 null
        - 318 unique
        - BOURNEMOUTH, CHRISTCHURCH AND POOLE
    - county (str)
        - 0 null
        - 113 unique
        - BOURNEMOUTH, CHRISTCHURCH AND POOLE
    - ppd_category_type (str)
        - 0 null
        - 2 unique
    - record_status (str)
        - 0 null
        - 1 unique (all A)
- No fully duplicated rows

- Special characters in street, town_city, locality, district, county
    - Special characters exist but are legitimate
        - Commas in compound place names
        - Westward Ho!
    - Only  comma and exclamation mark were found outside my allowed characters ([^&a-zA-Z0-9'.\s-])
    - Accented characters would be flagged.
    - No non-standard or accented characters were detected 


### 2015-2025 Oxfordshire only price data audit

- The 2025 data was found to not require cleaning and did not contain sufficient parameters for future prediction and analysis projects (including ML, segmentation etc). It was therefore decided to take a 10 year slice for Oxfordshire and join it with domestic Energy Performance Certificate (EPC) data.

- UPRN (Unique Property Reference Number) is contained in the EPC data but unfortunately the UPRN lookup table availible on Land Registry site only covers Aug 2026 onward. Therefore the join will require address matching.

- There is a paper detailing this method (reference to add) which obtained a 79% matching rate. This will be a good benchmark to work toward.

- part_1_LRPD_anomalies_2015_2025.ipynb

- Downloaded data from HM Land Regisry Open Data report builder
    https://landregistry.data.gov.uk/app/ppd
- Loaded data 
    - Columns have changed slightly compared to above. saon/paon switched places. now includes url in place of record_status. ppd_category_type is now transaction_category
- shape: (135557, 16)
- Column by column audit
    - unique_id (str)
        - Bracketed hexadecimal
        - 0 null
        - all unique
    - price_paid (int64)
        - Integer numbers
        - 0 null
        - 8779 unique
        - No starting symbols (£ etc)
        - 20 <£1000
        - 1 > £100 million, at £414 million
            - Far less ultra-expensive properties than in the national dataset
    - deed_date (str)
        - should be timestamp
        - 0 null
        - 3002 unique (ca. 300 per year)
        - breakdown by days of week
            - 45% sales on Friday close to 3 times any other day
            - 0.1% on each of Sat and Sun
        - unique deed_dates per month each year vary from 18 to 28, rather than the expected 28-31
        - It is likely the missing days are weekends (ca. 100 possible missing days per year)
    - postcode (str)
        - 442 null
        - 16536 unique
        - Performed regex check and found no incorrectly formatted postcodes ("^[A-Z]{1,2}\d[A-Z0-9]? \d[A-Z]{2}$")
    - property_type (str)
        - 0 null
        - 5 unique (T, S, D, F, O)
    - new_build (str)
        - 0 null
        - 2 unique
    - estate_type (str)
        - 0 null
        - 2 unique (F or L)
    - saon (str) - second address object (e.g. Flat 2)
        - 123737 null
        - 1151 unique
    - paon (str) - House number or name
        - could be int
        - 0 null
        - 11542 unique
    - street (str)
        - 3255 null
        - 8178 unique
    - locality (str)
        - 77985 null
        - 496 unique
    - town (str)
        - 0 null
        - 26 unique
    - district (str)
        - 0 null
        - 5 unique
    - county (str)
        - 0 null
        - 1 unique
    - transaction_category (str)
        - 0 null
        - 2 unique
    - linked_data_url (str)
        - 0 null
        - 135557 unique (links to land registry website)
- No fully duplicated rows

- No unallowed special characters in street, town, locality, district, county
    - Allowed characters ([^&a-zA-Z0-9'.\s-])
    - Accented characters would be flagged.
    - No non-standard or accented characters were detected 

  ### EPC Structural Audit

- Shape: (216054, 93)
- 3 empty columns to be dropped: 'floor_level', 'sheating_energy_eff', 'sheating_env_eff'
- Columns in/out of scope:

**Identity/linkage — essential:**
'certificate_number', 'address1', 'address2', 'address3', 'postcode', 'posttown', 'address', 'local_authority', 'local_authority_label', 'uprn', 'uprn_source'.

- 'constituency', 'constituency_label', 'region' and 'country' not needed
    - 'country' can be dropped (1 value)
    - 'region' can be dropped (only 4 in a second value)
    - 'constituency' shows parliamentary constituencies that cut across boundaries (drop)
    - 'local_authority' lines up with 'district' in the price paid set, keep
    - Lone 4 values in Banbury on Warwickshire border with unique 'local_authority' to drop as outside 5 target districts

**Core structural features — whole purpose of adding EPC:**
- 'total_floor_area', 'number_habitable_rooms', 'number_heated_rooms', 'property_type', 'built_form', 'construction_age_band', 'tenure', 'current_energy_rating', 'current_energy_efficiency', 'flat_storey_count', 'extension_count', 'floor_height'. Directly linked to future regression and prediction goals, to be audited carefully.
    - 'number_heated_rooms' == 'number_habitable_rooms' in 75% of cases and only exceeds it in 1 case. Keep

**Dates:**
- 'inspection_date', 'lodgement_date', 'lodgement_datetime'
    - 54% of 'lodgement_date' values match 'inspection_date'
    - 'lodgement_datetime' appears to just be 'lodgement_date' with extra precision (time). There's no time in the price paid database
    - Keep 'inspection_date' and 'lodgement_date'
    - time between inspection and lodgement is median 0 days, mean 8 days with min 0 days, max of 549 days and 75 percentile 2 days. So some very long delays are distorting the average, none are lodged before their inspections.

**Energy/cost/CO2 figures:**
- 'co2_emissions_current', 'co2_emissions_potential', 'co2_emiss_curr_per_floor_area', 'energy_consumption_current', 'energy_consumption_potential', 'environment_impact_current', 'environment_impact_potential', 'potential_energy_rating', 'heating_cost_current', 'heating_cost_potential', 'hot_water_cost_current', 'hot_water_cost_potential', 'lighting_cost_current', 'lighting_cost_potential'.
    - drop the 'potential' columns ('potential_energy_rating', 'co2_emissions_potential', 'energy_consumption_potential', 'environment_impact_potential', 'heating_cost_potential', 'hot_water_cost_potential', 'lighting_cost_potential') except 'potential_energy_efficiency', to still give an optional measure of room of improvement
    - drop 'environment_impact_current' (corr 0.92 with 'current_energy_efficiency')
    - do costs correlate strongly with 'total_floor_area'?
        - moderately (ca. 0.65)
        - Keep 'heating_cost_current' as it's an intuitive running cost for a buyer
        - drop 'co2_emissions_current' (correlates 0.82 with 'heating_cost_current' and -0.68 with 'current_energy_efficiency'), drop 'co2_emiss_curr_per_floor_area', drop 'lighting_cost_current' (small and correlated 0.66 with 'total_floor_area'), drop 'hot_water_cost_current' (small)
        - keep 'current_energy_efficiency' and 'energy_consumption_current' (size-independent)

**Component-level efficiency ratings — drop all**
- 'floor_energy_eff', 'floor_env_eff', 'walls_energy_eff', 'walls_env_eff', 'roof_energy_eff', 'roof_env_eff', 'windows_energy_eff', 'windows_env_eff', 'mainheat_energy_eff', 'mainheat_env_eff', 'mainheatc_energy_eff', 'mainheatc_env_eff', 'hot_water_energy_eff', 'hot_water_env_eff', 'lighting_energy_eff', 'lighting_env_eff' - redundant with the overall 'current_energy_rating'.

**Free-text description fields — could be interesting at a later date:**
- 'floor_description', 'roof_description', 'walls_description', 'windows_description', 'mainheat_description', 'mainheatcont_description', 'hotwater_description', 'lighting_description', 'secondheat_description'. Unstructured strings (e.g. likely things like "Cavity wall, filled cavity" or similar), could pull structured sub-features out of them (insulation type, glazing description) at a later date.

'transaction_type'
- Useful info on reason for assessment (37% for Marketed sale and 21% for New dwelling) keep

**Drop — low relevance to goals:**
'energy_tariff', 'flat_top_storey', 'glazed_area', 'glazed_type', 'heat_loss_corridor', 'mains_gas_flag', 'mechanical_ventilation', 'multi_glaze_proportion', 'number_open_fireplaces', 'photo_supply', 'solar_water_heating_flag', 'unheated_corridor_length', 'wind_turbine_count', 'main_fuel', 'main_heating_controls', 'report_type', 'fixed_lighting_outlets_count', 'low_energy_lighting', 'low_energy_fixed_lighting_outlets_count'. Mostly building-physics detail unlikely to matter for the price-drivers/segmentation project