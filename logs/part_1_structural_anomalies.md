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
- Downloaded from https://get-energy-performance-data.communities.gov.uk/
- Shape: (216054, 93)
- 3 empty columns to be dropped: 'floor_level', 'sheating_energy_eff', 'sheating_env_eff'

**Columns in/out of scope**:

**Identity/linkage** — essential:
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

**Definitions of kept columns** (from Domestic EPC Data Dictionary found here https://get-energy-performance-data.communities.gov.uk/guidance/data-dictionary):
- **certificate_number**: The unique reference number assigned to the Energy Performance Certificate.
- **address1**: The first line of the property address.
- **address2**: The second line of the property address.
- **address3**: The third line of the property address.
- **postcode**: The postcode of the property.
- **posttown**: The post town of the property address.
- **address**: The full address of the property.
- **local_authority**: The local authority code associated with the property.
- **local_authority_label**: The official name of the local authority.
- **built_form**: Describes the built form or structural layout of the property (e.g., Detached, Semi-Detached, Terraced).
- **construction_age_band**: Describes the construction period or age band during which the property was built.
- **current_energy_efficiency**: The estimated current energy efficiency rating score of the property.
- **current_energy_rating**: How energy efficient the property currently is on the A–G band scale.
- **energy_consumption_current**: An estimate of current primary energy consumption of the property.
- **extension_count**: The total number of extensions added to the property.
- **flat_storey_count**: The total number of storeys in the block containing the flat.
- **floor_height**: The average room height of the property.
- **heating_cost_current**: An estimate of current heating cost for the property.
- **inspection_date**: The date when information was collected during the property inspection.
- **lodgement_date**: The date the energy performance certificate was lodged on the register.
- **number_habitable_rooms**: The total number of habitable rooms in the property.
- **number_heated_rooms**: The total number of heated rooms in the property.
- **potential_energy_efficiency**: The estimated potential energy efficiency rating score after recommendations are implemented.
- **property_type**: Describes the kind of property (e.g., House, Flat, Bungalow, Maisonette).
- **tenure**: Describes the tenure type of the property (e.g., Owner-occupied, Rented).
- **total_floor_area**: The total enclosed floor area of the property in square metres.
- **transaction_type**: States why the energy performance certificate was created (e.g., market for sale, rental).
- **uprn**: The Unique Property Reference Number assigned to the address.
- **uprn_source**: The method or source by which the UPRN was generated or matched.


**Data audit**
- Core numeric features
    - total_floor_area
        - mean = 97, median = 83, min = 3, max = 5133, 75% = 111
        - There are 27 records with < 10 sqm floor areas and 8 with > 2000 sqm
            - 19 records are flats in the same building (7 or 9 sqm) with 1 habitable room
            - 1 is a room of 3 sqm
            - 7 are records with 2-4 habitable rooms but 5-9 sqm floor area (each room <= 3 sqm)
                - 3 are house or maisonette, size is too small to be real, exclude
                - 4 are flats.
                -  This is well below any plausible bedroom size. *Proposed: Exclude these 7 records with multiple rooms and < 9 sqm. Exclude the record with 3 sqm. Flag the 19 records that are 1 room flats (7-9 sqm) and check sale prices after join before deciding.*
        - There are 8 records with > 2000 sqm
            - 2 have NaN habitable rooms
            - 5 have 3 - 7 habitable rooms (implausible)
            - 1 has 39 habitable rooms (plausible)
            - perhaps average floor area per habitable room would be a good measure. These have up to 1209 sqm per room.
                - On full dataset it ranges from 0.8 sqm/room to 1209 sqm/room, median 20 sqm, mean 21 sqm.
            - *Proposed: Exclude the 7 records with >2000 sqm and <= 7 rooms (8206-7322-4290-4245-7906, 0552-3041-5201-3644-6204, 1032-5920-2209-0815-0202, 0044-2876-6518-9608-3961, 8171-6324-5580-7887-6996, 3434-1132-3000-0328-7226, 5135-0635-7000-0689-9206)*
        - Small areas will have a larger effect on £ per sqm calculations later, so important to clean.
    - 'number_habitable_rooms', 'number_heated_rooms', 'extension_count', 'flat_storey_count', 'floor_height'
        - The range of values for number_habitable_rooms is 1.0 to 81.0, with median of 4.0
        - The range of values for number_heated_rooms is 0.0 to 55.0, with median of 4.0
            - Max room counts will need floor size to audit (or my sqm/room calculation), but 81 or 55 rooms is high
            - Zero heated rooms is implausible (338 records). *Proposed: Treat records with 0 heated rooms as value is missing.*
        - The range of values for 'extension_count' is 0.0 to 4.0, with median of 0.0
            - Reasonable
        - The range of values for 'flat_storey_count' is 1.0 to 9.0, with median of 2.0
            - null in only 5016 records
            - 430 records with 'flat_storey_count' > 3 (428 Houses). 11 records with 'flat_storey_count' > 4 (11 Houses, up to 9 storeys). 
            - Refering to the Official Data Dictionary (https://get-energy-performance-data.communities.gov.uk/guidance/data-dictionary) defines this column as "The total number of floors in the apartment block, including the ground floor and any basement levels.
            ". 
                - Given this is only null in 5016 records, when it would be expected to be null in all Houses (ca. 151,000), it is likely that assessors are inputting the properties storey count. *Proposed: Drop. Appears to be systematically misused outside of its defined scope.*
        - The range of values for 'floor_height' is 0.0 to 8.87, with median of 2.38
            - 53 records with 'floor height' > 5m. Many are built <1900. Believable for say converted churches or houses with mezzanine?
            - There are 2516 records with 'floor height' < 1.5m. Including 98 records with 'floor height' < 1m. *Proposed: Treat records with floor height < 1.5m as missing.*
        - Nulls
            - There are 49419 records with null for all of 'number_habitable_rooms', 'number_heated_rooms', 'extension_count'
                - These are disproportionately new dwellings (91% vs 21% new dwellings in wider sample)
                - All New dwelling records ('transaction_type') have null 'number_heated_rooms'. This is consistent with a different type of assessment for new builds.
                - Remaining ca. 4400 null records are unexplained. *Proposed: Revisit on Part 4*
            - 'flat_storey_count' is null in 5016 cases
                - Distribution of 'property_type' (e.g. flat vs house etc) slightly skewed toward flats (21 vs 32%)
            - 'floor_height'
                - 1615 null values. 99% are for Flats where the 'floor_height' is likely to be very standardised. *Proposed: Fill flat nulls with the median flat floor_height and add an imputed flag column.*
    - 'certificate_number' is unique with no missing values. None flagged as duplicated
    - Each 'uprn' has up to 50 'certificate_number' associated with it. 26776 flagged as duplicated
        - *Proposed: select one certificate per UPRN in Day 3 (most likely most recent inspection_date at or before the sale)*
- Categorical values
| Column | Unique values | Top values | Placeholders / anomalies | Proposed treatment |
|---|---|---|---|---|
| `property_type` | 5|House, Flat |'Not Recorded'  (1305, 0.6%)  |None needed|
| `built_form` | 7|Semi-Detached, Detached | | |
| `construction_age_band` | 67|England and Wales: 1950-1966, England and Wales: 1967-1975 |Mixture of bands and specific years. 201 as year|Convert single years into bands and exclude 201 as an error|
| `tenure` |4 |owner-occupied, rented (private) | | |
| `transaction_type` |14 |Marketed sale, Rental  |Contains 'None of the above' |Likely none needed as less common types may not correspond to a sale |
| `current_energy_rating` | 7|C, D, B | | |
| `uprn_source` |2 |Energy Assessor, Address Matched  | | |
- 'inspection_date' & 'lodgement_date'
    - format: YYYY-MM-DD
    - 'lodgement_date' fully within intended 2015-01-01 - 2015-12-31 limits
    - 468 records where the 'inspection_date' falls in 2014 but 'lodgement_date' is in 2015
    - No 'inspection_date' after 2025-12-31
    - No 'inspection_date' or 'lodgement_date' records are null
- Can confirm 'address' is a combination of 'address1', 'address2' and 'address3'
- Mapping of EPC 'property_type' codes to Price Paid 'property_type' deferred to part 2
- Checking 'current_energy_rating' against 'current_energy_efficiency'
    - Calculated energy ratings from efficiency. Perfect agreement between.
    - Worth noting that the efficiency can go over 100 if a property generates more energy (ultra-modern properties with renewable energy generation) than it uses. There are 417 records with efficiency > 100 inc 41 with efficiency > 110.
    - There are 6 records with an efficiencies over 110 but with positive 'energy_consumption_current'. These are edge cases, unusual but plausible as they may still use a large amount of energy in winter months. Two have energy_consumption_current >200 and are Maisonette/Flat which flags them as likely errors. *Proposed: Exclude 2051-7735-3040-1307-9975 and 0061-1212-2504-8687-0900*