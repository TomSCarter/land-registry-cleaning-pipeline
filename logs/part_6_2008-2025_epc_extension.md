# Part 6 - 2008-2025 EPC extension

- Re-running pipeline using a larger EPC dataset that goes back to 2008 (earliest available). Matching rate in the early years was < 10%, likely as the EPCs were not in the dataset used. This extension should improve matching rate for older sales, as EPCs could be lodged up to 10 years before sale.

Version control: v1 (2015-2025 EPCs) was tagged (v1-2015-epc) and a new branch (epc-2008-2025) was created. V1 output was renamed (data/processed/pp_epc_oxfordshire_2015_2025_v1.parquet)

Pipeline: A timestamped progress line was added _record in pipeline.py, giving realtime updates as the script runs.

## Comparing EPC datasets
- They contain the same column names and order
- nulls
    - tenure has a large number of missing values in the new set. These rows will be kept. Current cleaning only converts 'unknown' to null, should still work.
    - 339 rows with nulls in total_floor_area may need to be excluded if they make it through to the end
- datatypes
    - 2015-2025- float64(5), int64(5), str(18)
    - 2008-2025 - float64(8), int64(2), str(18)
    - 3 Int have become floats
        - total_floor_area
            - contains 339 nulls in 2008-2025 dataset (0.1%) none in 2015-2025
            - no decimals in remaining
        - heating_cost_current
            - no nulls
            - 5 decimals in remaining (247.240, 192.190, 1.804, 2.210, 163.710), 3 have NaN number_habitable_rooms and null or 0 total_floor area, 1 of the others (2.210) is a flat with 4 rooms and G current_energy_rating (suspect), and the last (1.804) has 25 rooms (such low heating cost makes no sense)
        - energy_consumption_current
            - no nulls
            - 4 decimals, 3 are in rows with 0 or null floor_area (will be filtered out). Remaining row was also flagged in heating_cost_current and is a Flat with 204m floor_height (impossible) [Not in final V2 output]
- New file has lodgements in every expected year, running from Sept 2008 to end of 2025. 2009 has most lodgements, which is plausible as new Home-Information-Packs for every sale were still in place until 2010.
- New dataset contains 2 fewer rows and 2 fewer unique certificate_number values than the old (in the 2015-2025 window)
- Both sets contain the 5 expected local authorities. The new set has an extra spurious row with E06000060 local authority.


## Pipeline output
- config updated with input file name and to output _v2 parquet.


```
                                step     rows  unique_sales  col_count  expired  floor_height_nulls  tenure_nulls  number_heated_rooms_nulls  built_form_nulls  imputed_count
0              load.read_price_paid   135557           NaN        NaN      NaN                 NaN           NaN                        NaN               NaN            NaN
1                     load.read_epc   338323           NaN        NaN      NaN                 NaN           NaN                        NaN               NaN            NaN
2     load.filter_local_authorities   338318           NaN        NaN      NaN                 NaN           NaN                        NaN               NaN            NaN
3   epc: normalise.strip_whitespace   338318           NaN        NaN      NaN                 NaN           NaN                        NaN               NaN            NaN
4      epc: normalise.remove_commas   338318           NaN        NaN      NaN                 NaN           NaN                        NaN               NaN            NaN
5      epc: normalise.build_address   338318           NaN        NaN      NaN                 NaN           NaN                        NaN               NaN            NaN
6       epc: normalise.build_tokens   338318           NaN        NaN      NaN                 NaN           NaN                        NaN               NaN            NaN
7    pp: normalise.strip_whitespace   135557           NaN        NaN      NaN                 NaN           NaN                        NaN               NaN            NaN
8       pp: normalise.remove_commas   135557           NaN        NaN      NaN                 NaN           NaN                        NaN               NaN            NaN
9       pp: normalise.build_address   135557           NaN        NaN      NaN                 NaN           NaN                        NaN               NaN            NaN
10       pp: normalise.build_tokens   135557           NaN        NaN      NaN                 NaN           NaN                        NaN               NaN            NaN
11          match.merge_on_postcode  4272749           NaN        NaN      NaN                 NaN           NaN                        NaN               NaN            NaN
12      match.filter_subset_matches   171240      119532.0        NaN      NaN                 NaN           NaN                        NaN               NaN            NaN
13     match.drop_ambiguous_matches   164823      118222.0        NaN      NaN                 NaN           NaN                        NaN               NaN            NaN
14         match.select_presale_epc   114490           NaN        NaN      NaN                 NaN           NaN                        NaN               NaN            NaN
15       match.select_final_columns   114490           NaN       36.0      NaN                 NaN           NaN                        NaN               NaN            NaN
16        features.add_epc_age_band   114490           NaN        NaN      NaN                 NaN           NaN                        NaN               NaN            NaN
17        features.add_expired_flag   114490           NaN        NaN   1151.0                 NaN           NaN                        NaN               NaN            NaN
18   features.add_calendar_features   114490           NaN        NaN      NaN                 NaN           NaN                        NaN               NaN            NaN
19     clean.nullify_invalid_values   114490           NaN        NaN      NaN              2575.0       35004.0                    32426.0            2507.0            NaN
20           clean.apply_exclusions   114424           NaN        NaN      NaN                 NaN           NaN                        NaN               NaN            NaN
21        clean.impute_floor_height   114424           NaN        NaN      NaN                 NaN           NaN                        NaN               NaN         2516.0
22                save.save_parquet   114424           NaN        NaN      NaN                 NaN           NaN                        NaN               NaN            NaN
```

### Comparison to pipeline with 2015-2025 set:

| Step | v1 (2015 EPCs) | v2 (2008 EPCs) |
|---|---|---|
| Address matched | 105,419 (77.8%) | 119,532 (88.2%) |
| After dropping ambiguous | 104,444 (77.0%) | 118,222 (87.2%) |
| With a pre-sale certificate | 91,150 (67.2%) | 114,490 (84.5%) |
| Final | 91,143 (67.2%) | 114,424 (84.4%) |

- Biggest change is in the pre-sale certificate step (as intended) with an additional 23,340 sales (+17.3 percentage points).
- In v1 ca. 13,300 sales were matched but the only certificates were from after the sale. In v2 this is reduced to ca. 3700.
- Number of ambigious matches dropped rose from 975 to 1310
- Local authority filter removed 5 rows as expected
- Missing 
    - Missing tenure values rose from 23.5% to 30.5%
    - Missing room counts fell from 32% to 28.1%
        - Likely as the proportion of new builds fell (which do not include room counts)
- Exclusions up from 7 to 66
    - The additional 59 match exactly the drop in tenure and floor_height nulls accross the exclusion step
- Are floor area nulls in the final table?
    - There are no missing values in total_floor_area in the final output
    - They are excluded by the total_floor_area > 9 sqm rule. Added a comment in config file
- Expired certificates rose from 62 to 1,151, flagged with the exisiting EPC_expired column

## Match rate over time comparison
[match_rate_vs_date_v2]

Comparing the match rate over time in the v1 and v2 outputs.
- The new output shows a roughly flat match rate over time, a marked improvement on the upward trend in v1. The improvement is particularly strong at older years (e.g. 4% to 84% (+80 points) in Jan 2015)
- A small gain is seen even in later years ca. +1 percentage points in 2025

| Year | Sales | Matched (v1) | Matched (v2) | Match rate v1 (%) | Match rate v2 (%) | Difference (pp) |
|---|--:|--:|--:|--:|--:|--:|
| 2015 | 12,060 | 4,283 | 9,874 | 35.51 | 81.87 | 46.36 |
| 2016 | 12,254 | 6,485 | 10,021 | 52.92 | 81.78 | 28.86 |
| 2017 | 12,088 | 6,858 | 9,935 | 56.73 | 82.19 | 25.45 |
| 2018 | 12,306 | 7,532 | 10,295 | 61.21 | 83.66 | 22.45 |
| 2019 | 11,844 | 7,808 | 10,091 | 65.92 | 85.20 | 19.28 |
| 2020 | 11,246 | 8,044 | 9,626 | 71.53 | 85.59 | 14.07 |
| 2021 | 16,722 | 11,986 | 14,218 | 71.68 | 85.03 | 13.35 |
| 2022 | 13,463 | 10,300 | 11,527 | 76.51 | 85.62 | 9.11 |
| 2023 | 10,764 | 8,463 | 9,012 | 78.62 | 83.72 | 5.10 |
| 2024 | 11,337 | 9,391 | 9,743 | 82.83 | 85.94 | 3.10 |
| 2025 | 11,473 | 9,993 | 10,082 | 87.10 | 87.88 | 0.78 |

- v2 still rises around 6 points over the period, probably from early sales whose EPC predate the dataset