# Oxfordshire house sales joined to energy certificates

This project links every residential sale in Oxfordshire from 2015 to 2025 (HM Land Registry Price Paid Data) to the property's Energy Performance Certificate (EPC), so that each sale has floor area, room counts, energy rating and building age with its price. Price Paid Data alone has no information about the size or condition of a property, so the join is to make later analysis like £/m² possible.

The two datasets share no common ID for historical sales, so they are matched on address. The pipeline cleans both datasets, matches them, picks the most relevant EPC record for each sale and writes out a single cleaned table.

I built this as the Week 10 project of a data science training plan. The working notes for each stage are in `logs/`.

## Data

Neither dataset is included in the repo. To reproduce the results:

**Price Paid Data.** Use the [report builder](https://landregistry.data.gov.uk/app/ppd) and run one search per district: Cherwell, Oxford, South Oxfordshire, Vale of White Horse and West Oxfordshire. Set the dates to 1 Jan 2015 to 31 Dec 2025, choose "all" results, and download as CSV with headers. Save the five files in `data/raw/` with names starting `ppd_data` (unchanged from downloads). Field definitions are on the [Land Registry guidance page](https://www.gov.uk/guidance/about-the-price-paid-data).

**Energy Performance Certificates.** Download from [Get energy performance of buildings data](https://get-energy-performance-data.communities.gov.uk/) (you need a GOV.UK One Login account). Select domestic certificates lodged between Jan 2015 and Dec 2025 for the same five local authorities. Save the CSV in `data/raw/` as `EDC_OXFORDSHIRE_2015_2025.csv`, or change `EPC_FILENAME` in `src/cleaning/config.py`. A data dictionary with definitions for the columns can be found at [Link to Domestic EPC Data Dictionary](https://get-energy-performance-data.communities.gov.uk/guidance/data-dictionary).

Contains HM Land Registry data, Crown copyright and database right 2021. This data is licensed under the Open Government Licence v3.0.

## Running it

Python 3.14 with pandas and pyarrow:

```
pip install -r requirements.txt
python run_pipeline.py
```

Run from the project root. It takes a few minutes, mostly spent on the address matching. The cleaned table (91,143 sales, 44 columns) is saved as Parquet in `data/processed/`, and a report of row counts at each step is printed to the terminal.

## How the matching works

1. Address fields on both sides are tidied (whitespace, commas, case) and each address is turned into a set of words, including the postcode.
2. Every sale is paired with every certificate at the same postcode.
3. A pair counts as a match if all the words in the Land Registry address appear in the EPC address. A subset test rather than an exact match is needed because EPC addresses sometimes include extra words such as the post town.
4. Sales that match more than one distinct property are dropped as ambiguous.
5. Where a property has several certificates, the one inspected closest before the sale is kept. Certificates from after the sale are not used, since the property may have changed.
6. Invalid values are set to missing, a few implausible records are excluded, and missing floor heights are filled with the median (with a flag column).

## Results

| | Sales | % of all sales |
|---|---|---|
| All sales 2015–2025 | 135,557 | 100% |
| Address matched to an EPC | 105,419 | 77.8% |
| After dropping ambiguous matches | 104,444 | 77.0% |
| With a certificate from before the sale | 91,150 | 67.2% |
| Final, after exclusions | 91,143 | 67.2% |

For comparison, a published linkage of the same two datasets by UCL researchers reached 79%, though with a different scope and method.
Chi, B., Dennett, A., Oléron-Evans, T. and Morphet, R. (2021). "A new attribute-linked residential property price dataset for England and Wales, 2011–2019." UCL Open: Environment, 2(7), 1–25. [DOI link to paper at publisher](https://doi.org/10.14324/111.444/ucloe.000019) [Repository version](https://pmc.ncbi.nlm.nih.gov/articles/PMC10208353/pdf/ucloe-03-019.pdf)

## Limitations

- **The match rate depends on sale year.** It is under 4% for early 2015 and about 88% by 2025. Certificates are valid for 10 years, so many early sales relied on certificates issued before 2015, which aren't in this extract. Analysis using EPC features should lean on later years, or the pipeline should be re-run with an older EPC download.
- **Matching on word sets loses repeated words.** An address like "Riverside Court 9 9 West Way" becomes the same set as the block's address without the flat number, which makes it ambiguous. These cases are dropped rather than resolved.
- **Short addresses can match unrelated longer ones** at the same postcode (for example "4 Churchill Road" and "Apartment 4, The Lofts, 7 Churchill Road"). Most of these show up as ambiguous and are dropped.
- **New-build certificates don't record room counts,** so about 32% of the final table has no room count. Floor area is complete and is the better size measure.
- **Tenure is missing for about 23.5% of sales.**
- **670 sales had two certificates tied for closest inspection date.** The more recently lodged one is used.

## Structure

```
├── run_pipeline.py        # runs the full pipeline
├── requirements.txt
├── src/cleaning/          # config, load, normalise, match, features, clean, save, pipeline
├── notebooks/             # exploration and development, one per stage
├── logs/                  # notes and decisions for each stage
└── data/                  # raw, interim and processed (not tracked)
```