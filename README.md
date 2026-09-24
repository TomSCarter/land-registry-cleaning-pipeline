# Week 10: Processing Complex, Messy Real-World Data

Cleaning pipeline for HM Land Registry Price Paid Data (2025), built as part of a structured data analyst / analytics engineer training curriculum. Focus: real-world data quality issues — structural anomalies, inconsistent text, messy datetimes, missing data — resolved into a reusable, auditable cleaning pipeline.

## Dataset

- **Source:** [HM Land Registry Price Paid Data](https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads)
- **Scope:** 2025 single-year extract (~129MB)
- **Location:** `data/raw/` (not tracked in git — see Setup)

## Project Structure
```
week10_land_registry/
├── data/
│ ├── raw/ # Original downloaded CSV — never modified
│ └── processed/ # Cleaned outputs
├── notebooks/ # Daily exploration and development work
├── src/
│ └── cleaning/ # Reusable pipeline classes/functions
├── logs/ # Anomaly documentation, run logs
├── .gitignore
└── README.md
```

## Approach

Each day builds one stage of the eventual pipeline, culminating in a consolidated cleaning script:

| Day | Stage |
|---|---|
| 1 | Structural anomaly documentation |
| 2 | Regex-based text field cleaning |
| 3 | Datetime standardisation |
| 4 | Missing data handling |
| 5 | Refactor into a reusable pipeline class |
| 6–7 | Capstone: full automated cleaning script (standardised addresses, prices, dates, Oxfordshire isolation) |

## Setup

1. Download the 2025 Price Paid Data CSV from the link above and place it in `data/raw/`.
2. Column definitions/field guide: [link to HM Land Registry field guide once confirmed].
3. (Add environment/dependency setup here once established — e.g. `requirements.txt` or `conda` env.)

## Status

In progress — Day 1: structural anomaly audit.