# Land registry price data (& EPC) analysis

## Part 2 - Regex and joining

- This part will focus on building the address-matching join between the Land Registry Price Paid data (PP) and the Energy Performance Certificate (EPC) data

- A published UCL paper achieved 79% matching, this acts as a benchmark

- Comparing address fields in both datasets
    - PP data is in full caps vs EPC data in capital case
    - pp_'locality' is typically epc_'address3' but can be epc_'address2', depending on how the address is split
    - pp_'saon', pp_'saon'+pp_'paon' or pp_'paon' can be epc_'address1'
    - pp_'town' is generally epc_'post_town'
    - Both appear use 'FLAT 8' vs 'Flat 8'
    - Both appear to use Street and Road in the records checked
    - It would be informative to convert to upper case and try a join based on postcode and address1, but would need to match with paon or saon
    - For properties with multiple EPC records, the record most closely preceeding the 'deed_date' should give the best connection to the 'price_paid'

- Initial clean
    - Created copies of the tables
    - Removed trailing/leading whitespace from all string fields in both tables
    - Removed commas from epc_'address1'

- Initial join
    - Generated combined address fields (space sep) for both tables and upper case epc_'address'
    - Created an 'address_tokens' field in both tables, splitting the combined addresses into frozensets
    - Inner join on 'address_tokens' gives a table with 107935 rows. But due to the multiple EPC per property, properties are duplicated. 96461 unique property rows ('unique_id') corresponding to a 71.2% match rate.

- Second join
    - Removed commas from all matching fields
    - 110478 rows, 98784 properties with EPC matches, match rate 72.9% of properties matched to an EPC.

- Filtering to properties with an EPC before sale
    - Gives 91240 matches of properties with EPCs inspected before sale. 
    - Leaving 19238 rows with after sale EPCs
        - If we take this set and drop all but the EPC with closest date to the sale we get 18140 rows (these properties could also have rows with pre-sale EPCs in the other set)
            - median days after sale is 1418 day (ca. 4 years), 75th percentile of 630 days.
            - *Decision: Drop all properties with EPCs after sale. Return to filter more specifically if time allows.*

- Funnel
    - 135,557 total Price Paid property transactions
        - 216,054 EPC records
    - 98,784 found exact address-token match (72.9%)
    - 86,358 have a usable pre-sale EPC (63.7%)
    - 12,426 matched an address but have no usable pre-sale EPC (9.2%)
    - 36,773 were not address matched to an EPC record (27.1%)

- Investigating unmatched set
    - Sample of 10 transactions from price paid set
        - 11 Harrier Drive OX11 6BU
            - sold in 2017 and 2022
            - No 11 in EPC set
            - 2014 certificate found in pre-2015
        - 1  WESTMINSTER WAY  OX2 0PZ
            - sold in 2018
            - Postcode not in EPC set
            - No result found in pre-2015
        - 64  EDGEWORTH DRIVE  OX18 3LW
            - sold in 2018
            - No 64 in EPC set
            - 2012 certificate found in pre-2015
        - 12  PARKERS CIRCUS  OX7 5LZ
            - sold 2018
            - No 12 in EPC set
            - 2009 certificate found in pre-2015
        - PERPETUAL HOUSE 2 STATION ROAD  RG9 1AF
            - Found in EPC set. Did not match due to inclusion of 'HENLEY-ON-THAMES' in address3 in the EPC (and not in locality in PP)
            - sold 2015
        - HAZLETON HOUSE 15 1 HIGH STREET  OX9 2BZ
            - sold 2015
            - No 15 or hazleton house in EPC set
            - 2012 certificate for 15c in pre-2015
        - 5A  OAKS ROAD SHIPLAKE RG9 3JH
            - sold 2021
            - Found in EPC set. Did not match due to inclusion of 'HENLEY-ON-THAMES' in address3 in the EPC (in addition to the Shiplake locality in PP)
        - LASHLAKE HOUSE  AYLESBURY ROAD  OX9 3AU
            - sold 2015
            - No Lashlake house in EPC set
            - No certificate in pre-2015
        - 1  CANTOR ROW  OX14 2FY
            - sold 2024
            - No 1 in EPC set or pre-2015
        - 57  BALLARD CHASE  OX14 1XQ
            - sold 2015
            - No 57 in EPC set
            - 2014 certificate in pre-2015
        - Searched epc set by postcode
        - 3 postcodes no present in epc set
        - 7 postcodes present, but no matching house name or number
    - Comparing null fields in full price paid set and unmatched set
        - non-null saon enriched in unmatched set (ca 1.5x)
        - null postcode enriched in unmatched set (ca. 3.7x). But only 442 records to start with
    - Within the unmatched PP set there are 2269 records whose postcodes are no in the EPC dataset (6% of unmatched)
    - A meaningful share of the unmatched price paid records are likely to have no counterpart in the 2015-2025 EPC dataset
        - EPCs are valid for 10 years, so it is possible they may have a certificate issued before 2015 that was still valid at the time of the sale. In the sample above 40-50% did have a valid pre-2015 certificate at the date of sale.
    - Unmatched set contains slightly more expensive (median 370000 vs 365000, mean 663000 vs 513000) sales, that are less likely to be new builds (18% vs 10%) and have slightly older deed_dates (mean = 2019-12-06 vs 2020-07-01).
    - The 5A OAKS ROAD and PERPETUAL HOUSE 2 examples show that exact matching of the address tokens is not ideal. They are failing to match due to an additional token in the EPC set (HENLEY-ON-THAMES). Subset matching would improve this

= Third join (subset matching)
    - Matched on postcode then on PP address_tokens being a subset of EPC address_tokens
    - Gave 105419 matches (77.8% match rate)
    - But contains duplicates due to multiple EPCs for a single property
    - Filtered to EPCs with inspection_date closest to deed_date (but not after)
    - 91938 matches, 67.8% match rate
    - Subset matching recovered 5580 additional usable matches over exact matching.
