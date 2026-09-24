# Land Registry Price Data (2025)

## Day 1 - Structural audit

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
- No duplicated rows
Steps to work through:

Load and inspect without assumptions. Open the file and check: does it load cleanly with default settings, or does something choke (encoding error, wrong delimiter, extra/missing header row)? Note whatever goes wrong before you fix it.

Column-by-column audit. For each column, ask: what data type do I expect, and does what's actually there match? Look for mixed types in one column (numbers stored as text, stray currency symbols in a price field), inconsistent categorical values ("Detached" vs "D" vs "detached "), and unexpected NaN/null representations (empty string vs "NULL" vs "N/A" vs a genuinely blank cell).

Character-level check. Land Registry data pulls in address/locality text, which is a classic source of encoding corruption — look for mangled apostrophes, stray accented characters, or replacement-character glyphs (often shows as �). Note where these appear, not just that they exist.

Duplicate and structural row checks. Are there fully duplicated rows? Rows with a wrong number of fields (a stray comma inside an unquoted address breaking column alignment)?

Write the log. For each issue: what it is, which column(s), roughly how many rows affected (a count, even approximate), and a one-line note on what it implies for cleaning later (e.g. "will need .str.extract() for postcode" — but don't build that yet, just flag it).

A concrete deliverable for today: a markdown or text file, day1_anomaly_log.md, listing every issue found, evidence (row examples), and severity/frequency — nothing else touched or modified.

One general technique worth knowing generically (not solving your task, just the pattern): to count how many non-ASCII characters exist in a text column without altering anything, you inspect each string's byte/character composition against the ASCII range and tally matches — that's the general idea behind step 3; how you implement it against your actual columns is your part.