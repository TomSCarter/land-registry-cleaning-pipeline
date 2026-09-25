# Land Registry Price Data Analysis

## Part 1 - Structural audit

- Scope changes: Scope was changed from 2025 national prices to 2015-2025 Oxfordshire only, but with joining of Energy Performance Certificate (EPC) dataset.

### Single year 2025 national price data audit

- part_1_anomalies.ipynb

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

### EPC Structural Audit