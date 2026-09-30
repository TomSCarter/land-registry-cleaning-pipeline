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
